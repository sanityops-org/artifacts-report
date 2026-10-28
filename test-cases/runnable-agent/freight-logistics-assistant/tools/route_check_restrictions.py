#!/usr/bin/env python3
"""route_check_restrictions: Check if cargo type is allowed on a route.

Use this tool when the user needs to verify if a specific cargo type can be transported
on a particular route. Returns whether the cargo is allowed, any requirements, and
alternative routes if available.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.route_optimizer import check_route_restrictions

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cargo_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20,
            "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
            "description": "Cargo category to check. Required.",
        },
        "route_id": {
            "type": "string",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^R\\d{3}$",
            "description": "Route identifier to check (format: R followed by 3 digits, e.g., R001). Required if origin/destination not provided.",
        },
        "origin": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Origin city. Letters, digits, spaces, and common punctuation only. Used with destination if route_id not provided.",
        },
        "destination": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Destination city. Letters, digits, spaces, and common punctuation only. Used with origin if route_id not provided.",
        },
    },
    "required": ["cargo_type"],
    "anyOf": [
        {"required": ["route_id"]},
        {"required": ["origin", "destination"]},
    ],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check route restrictions for cargo type.

    Args:
        params: {"cargo_type": str, "route_id": str, "origin": str, "destination": str}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    cargo_type = params.get("cargo_type")
    if not cargo_type:
        return {"status": "error", "error": "Missing required parameter: cargo_type"}

    route_id = params.get("route_id")
    origin = params.get("origin")
    destination = params.get("destination")

    if not route_id and (not origin or not destination):
        return {"status": "error", "error": "Either route_id or both origin and destination must be provided"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        result = check_route_restrictions(
            cargo_type=cargo_type,
            data_store=data_store,
            route_id=route_id,
            origin=origin,
            destination=destination,
        )

        return {
            "status": "success",
            "data": {
                "cargo_category": result.cargo_category.value,
                "route_id": result.route_id,
                "origin": result.origin,
                "destination": result.destination,
                "allowed": result.allowed,
                "requirements": result.requirements,
                "alternative_routes": result.alternative_routes,
                "notes": result.notes,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to check restrictions: {str(e)}"}


if __name__ == "__main__":
    print(execute({"cargo_type": "hazardous", "route_id": "R001"}))