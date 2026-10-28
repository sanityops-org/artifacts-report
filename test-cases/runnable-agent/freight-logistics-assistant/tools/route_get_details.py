#!/usr/bin/env python3
"""route_get_details: Get detailed route information by route ID.

Use this tool when the user wants complete details about a specific route, including
all waypoints, service stations, road types, and restrictions. Requires a route ID
from a previous route recommendation.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.route_optimizer import get_route_details

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "route_id": {
            "type": "string",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^R\\d{3}$",
            "description": "Route identifier from route recommendation. Format: R followed by 3 digits (e.g., R001).",
        },
    },
    "required": ["route_id"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed route information.

    Args:
        params: {"route_id": str}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    route_id = params.get("route_id")
    if not route_id:
        return {"status": "error", "error": "Missing required parameter: route_id"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        route = get_route_details(route_id, data_store)

        if not route:
            return {"status": "error", "error": f"Route not found: {route_id}"}

        waypoints = []
        for wp in route.waypoints:
            waypoints.append({
                "sequence": wp.sequence,
                "location": wp.location,
                "facility": wp.facility,
                "estimated_arrival": wp.estimated_arrival,
                "estimated_departure": wp.estimated_departure,
            })

        restrictions = []
        for r in route.restrictions:
            restrictions.append({
                "cargo_category": r.cargo_category.value,
                "allowed": r.allowed,
                "requirements": r.requirements,
                "notes": r.notes,
            })

        return {
            "status": "success",
            "data": {
                "route_id": route.route_id,
                "name": route.name,
                "origin": route.origin,
                "destination": route.destination,
                "distance_km": route.distance_km,
                "estimated_hours": route.estimated_hours,
                "waypoints": waypoints,
                "road_types": route.road_types,
                "service_stations": route.service_stations,
                "restrictions": restrictions,
                "toll_cost": route.toll_cost,
                "average_speed_kmh": route.average_speed_kmh,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get route details: {str(e)}"}


if __name__ == "__main__":
    print(execute({"route_id": "R001"}))