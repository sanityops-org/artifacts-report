#!/usr/bin/env python3
"""
attraction_details: Get detailed information about a specific attraction.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store

parameters = {
    "type": "object",
    "properties": {
        "attraction_id": {
            "type": "string",
            "pattern": "^ATTR\\d{4}$",
            "description": "Attraction ID (e.g., ATTR0001)"
        }
    },
    "required": ["attraction_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Get detailed information about an attraction.

    Args:
        params:
            - attraction_id: Attraction ID (required)

    Returns:
        {"status": "success", "data": {...attraction details...}} or
        {"status": "error", "error": "..."}
    """
    attraction_id = params.get("attraction_id")
    if not attraction_id:
        return {"status": "error", "error": "Missing required parameter: attraction_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        attractions = store.load_attractions()

        attraction = next((a for a in attractions if a.attraction_id == attraction_id), None)

        if not attraction:
            return {"status": "error", "error": f"Attraction {attraction_id} not found"}

        return {
            "status": "success",
            "data": attraction.model_dump(mode="json")
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get attraction details: {str(e)}"}
