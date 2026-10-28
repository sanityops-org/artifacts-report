#!/usr/bin/env python3
"""
destination_details: Get detailed information about a specific destination.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.destination_engine import DestinationEngine

parameters = {
    "type": "object",
    "properties": {
        "destination_id": {
            "type": "string",
            "pattern": "^DEST\\d{3}$",
            "description": "Destination ID (e.g., DEST001)"
        }
    },
    "required": ["destination_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Get detailed information about a destination.

    Args:
        params:
            - destination_id: Destination ID (required)

    Returns:
        {"status": "success", "data": {"destination": {...}, "attractions_count": N}} or
        {"status": "error", "error": "..."}
    """
    destination_id = params.get("destination_id")
    if not destination_id:
        return {"status": "error", "error": "Missing required parameter: destination_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        destinations = store.load_destinations()
        attractions = store.load_attractions()

        engine = DestinationEngine(destinations, attractions)
        destination = engine.get_destination(destination_id)

        if not destination:
            return {"status": "error", "error": f"Destination {destination_id} not found"}

        # Get attractions count
        attractions_list = engine.get_attractions_for_destination(destination_id)

        return {
            "status": "success",
            "data": {
                "destination": destination.model_dump(mode="json"),
                "attractions_count": len(attractions_list)
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get destination details: {str(e)}"}
