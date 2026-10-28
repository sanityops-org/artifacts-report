#!/usr/bin/env python3
"""
accommodation_search: Search accommodations in a destination with filters.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from models.enums import AccommodationType

parameters = {
    "type": "object",
    "properties": {
        "destination_id": {
            "type": "string",
            "pattern": "^DEST\\d{3}$",
            "description": "Destination ID (e.g., DEST001)"
        },
        "type": {
            "type": "string",
            "description": "Filter by type (hotel, hostel, resort, apartment)"
        },
        "max_price": {
            "type": "number",
            "description": "Maximum price per night in USD"
        },
        "min_rating": {
            "type": "number",
            "description": "Minimum rating (1.0-5.0)"
        }
    },
    "required": ["destination_id"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Search accommodations in a destination.

    Args:
        params:
            - destination_id: Destination ID (required)
            - type: Accommodation type filter (optional)
            - max_price: Maximum price filter (optional)
            - min_rating: Minimum rating filter (optional)

    Returns:
        {"status": "success", "data": {"accommodations": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    destination_id = params.get("destination_id")
    if not destination_id:
        return {"status": "error", "error": "Missing required parameter: destination_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        accommodations = store.load_accommodations()

        # Filter by destination
        results = [a for a in accommodations if a.destination_id == destination_id]

        # Filter by type
        if params.get("type"):
            try:
                type_enum = AccommodationType(params["type"].lower())
                results = [a for a in results if a.type == type_enum]
            except ValueError:
                pass

        # Filter by max price
        if params.get("max_price") is not None:
            results = [a for a in results if a.price_per_night_usd <= params["max_price"]]

        # Filter by min rating
        if params.get("min_rating") is not None:
            results = [a for a in results if a.rating >= params["min_rating"]]

        # Sort by rating
        results.sort(key=lambda a: a.rating, reverse=True)

        return {
            "status": "success",
            "data": {
                "accommodations": [a.model_dump(mode="json") for a in results],
                "count": len(results)
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to search accommodations: {str(e)}"}
