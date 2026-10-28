#!/usr/bin/env python3
"""
itinerary_details: Get details of a saved itinerary.
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
        "itinerary_id": {
            "type": "string",
            "pattern": "^ITIN\\d{4}$",
            "description": "Itinerary ID (e.g., ITIN0001)"
        }
    },
    "required": ["itinerary_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Get details of a saved itinerary.

    Args:
        params:
            - itinerary_id: Itinerary ID (required)

    Returns:
        {"status": "success", "data": {...itinerary details...}} or
        {"status": "error", "error": "..."}
    """
    itinerary_id = params.get("itinerary_id")
    if not itinerary_id:
        return {"status": "error", "error": "Missing required parameter: itinerary_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        itinerary = store.get_itinerary(itinerary_id)

        if not itinerary:
            return {"status": "error", "error": f"Itinerary {itinerary_id} not found"}

        return {
            "status": "success",
            "data": itinerary.model_dump(mode="json")
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get itinerary details: {str(e)}"}
