#!/usr/bin/env python3
"""
weather_current: Get current weather conditions for a location.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.weather_engine import get_current_conditions

parameters = {
    "type": "object",
    "properties": {
        "location_id": {
            "type": "string",
            "pattern": "^LOC\\d{3}$",
            "description": "Location ID (e.g., LOC001)"
        }
    },
    "required": ["location_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get current weather conditions.

    Args:
        params:
            - location_id: Location ID (required)

    Returns:
        {"status": "success", "data": {...current conditions...}} or
        {"status": "error", "error": "..."}
    """
    location_id = params.get("location_id")
    if not location_id:
        return {"status": "error", "error": "Missing required parameter: location_id"}

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        locations = data_store.load_locations()
        conditions = data_store.load_current_conditions()

        # Verify location exists
        location = None
        for loc in locations:
            if loc.location_id == location_id:
                location = loc
                break

        if not location:
            return {"status": "error", "error": f"Location {location_id} not found"}

        current = get_current_conditions(location_id, conditions)

        if not current:
            return {"status": "error", "error": f"No current conditions available for {location.name}"}

        result = current.model_dump(mode="json")
        result["location_name"] = location.name

        return {"status": "success", "data": result}

    except Exception as e:
        return {"status": "error", "error": f"Failed to get current conditions: {str(e)}"}
