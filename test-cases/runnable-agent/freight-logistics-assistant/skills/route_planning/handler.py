"""Route planning skill handler."""

from typing import Any, Dict
from pathlib import Path

from apis.data_store import DataStore
from apis.route_optimizer import (
    recommend_routes,
    get_route_details,
    check_route_restrictions,
)
from models.enums import CargoCategory

project_root = Path(__file__).parent.parent.parent


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute route planning skill.

    Args:
        params: {"intent": str, ...}

    Supported intents:
        - recommend_options: {"intent": "recommend_options", "origin": str, "destination": str, ...}
        - get_details: {"intent": "get_details", "route_id": str}
        - check_restrictions: {"intent": "check_restrictions", "cargo_type": str, ...}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    intent = params.get("intent")
    if not intent:
        return {"status": "error", "error": "Missing required parameter: intent"}

    data_store = DataStore(data_dir=project_root / "data")

    if intent == "recommend_options":
        return _handle_recommend(params, data_store)
    elif intent == "get_details":
        return _handle_details(params, data_store)
    elif intent == "check_restrictions":
        return _handle_restrictions(params, data_store)
    else:
        return {"status": "error", "error": f"Unknown intent: {intent}"}


def _handle_recommend(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle recommend_options intent."""
    origin = params.get("origin")
    destination = params.get("destination")
    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

    cargo_type = None
    if params.get("cargo_type"):
        cargo_type = CargoCategory(params["cargo_type"])

    result = recommend_routes(
        origin=origin,
        destination=destination,
        data_store=data_store,
        cargo_type=cargo_type,
        priority=params.get("priority", "balanced"),
    )

    options = [
        {
            "route_id": o.route_id,
            "name": o.name,
            "distance_km": o.distance_km,
            "estimated_hours": o.estimated_hours,
            "estimated_cost": o.estimated_cost,
        }
        for o in result.options
    ]

    return {
        "status": "success",
        "data": {
            "options": options,
            "recommended": result.recommended,
            "note": result.note,
        },
    }


def _handle_details(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle get_details intent."""
    route_id = params.get("route_id")
    if not route_id:
        return {"status": "error", "error": "Missing required parameter: route_id"}

    route = get_route_details(route_id, data_store)
    if not route:
        return {"status": "error", "error": f"Route not found: {route_id}"}

    return {
        "status": "success",
        "data": {
            "route_id": route.route_id,
            "name": route.name,
            "distance_km": route.distance_km,
            "estimated_hours": route.estimated_hours,
            "waypoints": [w.model_dump() for w in route.waypoints],
        },
    }


def _handle_restrictions(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle check_restrictions intent."""
    cargo_type = params.get("cargo_type")
    if not cargo_type:
        return {"status": "error", "error": "Missing required parameter: cargo_type"}

    result = check_route_restrictions(
        cargo_type=CargoCategory(cargo_type),
        data_store=data_store,
        route_id=params.get("route_id"),
        origin=params.get("origin"),
        destination=params.get("destination"),
    )

    return {
        "status": "success",
        "data": {
            "allowed": result.allowed,
            "requirements": result.requirements,
            "notes": result.notes,
        },
    }