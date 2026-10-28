"""Shipment tracking skill handler."""

from typing import Any, Dict

from apis.data_store import DataStore
from apis.tracking_engine import (
    get_shipment_status,
    get_shipment_history,
    list_shipments_by_route,
    ShipmentFilter,
)
from pathlib import Path

project_root = Path(__file__).parent.parent.parent


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute shipment tracking skill.

    Args:
        params: {"intent": str, ...}

    Supported intents:
        - get_status: {"intent": "get_status", "tracking_number": str}
        - get_history: {"intent": "get_history", "tracking_number": str}
        - list_by_route: {"intent": "list_by_route", "origin": str, "destination": str, ...}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    intent = params.get("intent")
    if not intent:
        return {"status": "error", "error": "Missing required parameter: intent"}

    data_store = DataStore(data_dir=project_root / "data")

    if intent == "get_status":
        return _handle_get_status(params, data_store)
    elif intent == "get_history":
        return _handle_get_history(params, data_store)
    elif intent == "list_by_route":
        return _handle_list_by_route(params, data_store)
    else:
        return {"status": "error", "error": f"Unknown intent: {intent}"}


def _handle_get_status(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle get_status intent."""
    tracking_number = params.get("tracking_number")
    if not tracking_number:
        return {"status": "error", "error": "Missing required parameter: tracking_number"}

    result = get_shipment_status(tracking_number, data_store)
    if not result.found:
        return {"status": "error", "error": result.error}

    shipment = result.shipment
    return {
        "status": "success",
        "data": {
            "tracking_number": shipment.tracking_number,
            "origin": shipment.origin,
            "destination": shipment.destination,
            "status": shipment.status.value,
            "carrier_name": shipment.carrier_name,
            "current_location": shipment.current_location,
            "eta": shipment.eta.isoformat() if shipment.eta else None,
        },
    }


def _handle_get_history(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle get_history intent."""
    tracking_number = params.get("tracking_number")
    if not tracking_number:
        return {"status": "error", "error": "Missing required parameter: tracking_number"}

    result = get_shipment_history(tracking_number, data_store)
    if not result.found:
        return {"status": "error", "error": result.error}

    shipment = result.shipment
    events = [
        {
            "timestamp": e.timestamp.isoformat(),
            "location": e.location,
            "status": e.status.value,
            "description": e.description,
        }
        for e in shipment.tracking_history
    ]

    return {
        "status": "success",
        "data": {
            "tracking_number": shipment.tracking_number,
            "tracking_history": events,
            "total_events": len(events),
        },
    }


def _handle_list_by_route(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle list_by_route intent."""
    filter_params = ShipmentFilter()
    if params.get("origin"):
        filter_params.origin = params["origin"]
    if params.get("destination"):
        filter_params.destination = params["destination"]

    shipments = list_shipments_by_route(filter_params, data_store)

    results = [
        {
            "tracking_number": s.tracking_number,
            "origin": s.origin,
            "destination": s.destination,
            "status": s.status.value,
        }
        for s in shipments
    ]

    return {
        "status": "success",
        "data": {
            "shipments": results,
            "total_count": len(results),
        },
    }