#!/usr/bin/env python3
"""
itinerary_create: Create a travel itinerary for a destination.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.destination_engine import DestinationEngine
from apis.itinerary_planner import ItineraryPlanner

parameters = {
    "type": "object",
    "properties": {
        "destination_id": {
            "type": "string",
            "pattern": "^DEST\\d{3}$",
            "description": "Destination ID (e.g., DEST001)"
        },
        "duration_days": {
            "type": "integer",
            "description": "Trip duration in days (1-14)"
        },
        "theme": {
            "type": "string",
            "description": "Travel theme preference (beach, mountain, city, culture, adventure, family, romantic, foodie)"
        },
        "start_date": {
            "type": "string",
            "description": "Start date in YYYY-MM-DD format (optional, defaults to today)"
        }
    },
    "required": ["destination_id", "duration_days"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Create a travel itinerary.

    Args:
        params:
            - destination_id: Destination ID (required)
            - duration_days: Trip duration (required)
            - theme: Travel theme (optional)
            - start_date: Start date (optional)

    Returns:
        {"status": "success", "data": {...itinerary details...}} or
        {"status": "error", "error": "..."}
    """
    destination_id = params.get("destination_id")
    duration_days = params.get("duration_days")

    if not destination_id:
        return {"status": "error", "error": "Missing required parameter: destination_id"}
    if not duration_days:
        return {"status": "error", "error": "Missing required parameter: duration_days"}

    try:
        store = get_data_store(str(project_root / "data"))
        destinations = store.load_destinations()
        attractions = store.load_attractions()

        engine = DestinationEngine(destinations, attractions)
        destination = engine.get_destination(destination_id)

        if not destination:
            return {"status": "error", "error": f"Destination {destination_id} not found"}

        planner = ItineraryPlanner(attractions)
        itinerary = planner.create_itinerary(
            destination=destination,
            duration_days=duration_days,
            theme=params.get("theme"),
            start_date=params.get("start_date"),
            itinerary_id=store.next_itinerary_id()
        )

        # Save itinerary
        store.save_itinerary(itinerary)

        return {
            "status": "success",
            "data": itinerary.model_dump(mode="json")
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to create itinerary: {str(e)}"}
