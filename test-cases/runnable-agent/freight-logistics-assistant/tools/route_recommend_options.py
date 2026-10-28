#!/usr/bin/env python3
"""route_recommend_options: Recommend optimal routes between origin and destination.

Use this tool when the user wants to find the best routes for shipping freight between
two locations. Returns multiple route options with distance, estimated time, and cost.
Can consider cargo type restrictions and optimize for cost, time, or balanced approach.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.route_optimizer import recommend_routes

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "origin": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Origin city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "destination": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Destination city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "cargo_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20,
            "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
            "description": "Cargo category. Optional. Used to filter routes with restrictions.",
        },
        "priority": {
            "type": "string",
            "minLength": 4,
            "maxLength": 8,
            "enum": ["cost", "time", "balanced"],
            "default": "balanced",
            "description": "Optimization priority: 'cost' for cheapest, 'time' for fastest, 'balanced' for trade-off.",
        },
    },
    "required": ["origin", "destination"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recommend optimal routes between origin and destination.

    Args:
        params: {"origin": str, "destination": str, "cargo_type": str, "priority": str}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    origin = params.get("origin")
    destination = params.get("destination")

    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        result = recommend_routes(
            origin=origin,
            destination=destination,
            data_store=data_store,
            cargo_type=params.get("cargo_type"),
            priority=params.get("priority", "balanced"),
        )

        options = []
        for opt in result.options:
            options.append({
                "route_id": opt.route_id,
                "name": opt.name,
                "distance_km": opt.distance_km,
                "estimated_hours": opt.estimated_hours,
                "estimated_cost": opt.estimated_cost,
                "waypoints_count": opt.waypoints_count,
                "restrictions": opt.restrictions,
            })

        return {
            "status": "success",
            "data": {
                "origin": result.origin,
                "destination": result.destination,
                "total_options": len(options),
                "recommended_route": result.recommended,
                "options": options,
                "note": result.note,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to recommend routes: {str(e)}"}


if __name__ == "__main__":
    print(execute({"origin": "Shanghai", "destination": "Beijing"}))