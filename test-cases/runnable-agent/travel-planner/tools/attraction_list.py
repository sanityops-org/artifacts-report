#!/usr/bin/env python3
"""
attraction_list: List attractions in a destination with optional filters.
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
        },
        "category": {
            "type": "string",
            "description": "Filter by category (nature, culture, adventure, food, shopping, relaxation)"
        },
        "min_rating": {
            "type": "number",
            "description": "Minimum rating filter (1.0-5.0)"
        }
    },
    "required": ["destination_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    List attractions in a destination.

    Args:
        params:
            - destination_id: Destination ID (required)
            - category: Category filter (optional)
            - min_rating: Minimum rating filter (optional)

    Returns:
        {"status": "success", "data": {"attractions": [...], "count": N}} or
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
        results = engine.get_attractions_for_destination(
            destination_id,
            category=params.get("category"),
            min_rating=params.get("min_rating")
        )

        return {
            "status": "success",
            "data": {
                "attractions": [a.model_dump(mode="json") for a in results],
                "count": len(results)
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to list attractions: {str(e)}"}
