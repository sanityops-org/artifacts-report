#!/usr/bin/env python3
"""
accommodation_details: Get detailed information about a specific accommodation.
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
        "accommodation_id": {
            "type": "string",
            "pattern": "^ACCOM\\d{4}$",
            "description": "Accommodation ID (e.g., ACCOM0001)"
        }
    },
    "required": ["accommodation_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Get detailed information about an accommodation.

    Args:
        params:
            - accommodation_id: Accommodation ID (required)

    Returns:
        {"status": "success", "data": {...accommodation details...}} or
        {"status": "error", "error": "..."}
    """
    accommodation_id = params.get("accommodation_id")
    if not accommodation_id:
        return {"status": "error", "error": "Missing required parameter: accommodation_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        accommodations = store.load_accommodations()

        accommodation = next((a for a in accommodations if a.accommodation_id == accommodation_id), None)

        if not accommodation:
            return {"status": "error", "error": f"Accommodation {accommodation_id} not found"}

        return {
            "status": "success",
            "data": accommodation.model_dump(mode="json")
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get accommodation details: {str(e)}"}
