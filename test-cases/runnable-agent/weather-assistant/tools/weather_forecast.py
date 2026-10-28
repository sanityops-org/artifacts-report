#!/usr/bin/env python3
"""
weather_forecast: Get multi-day weather forecast for a location.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.weather_engine import get_forecast

parameters = {
    "type": "object",
    "properties": {
        "location_id": {
            "type": "string",
            "pattern": "^LOC\\d{3}$",
            "description": "Location ID (e.g., LOC001)"
        },
        "days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 7,
            "description": "Number of forecast days (1-7, default 5)"
        }
    },
    "required": ["location_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get weather forecast.

    Args:
        params:
            - location_id: Location ID (required)
            - days: Number of days, 1-7 (optional, default 5)

    Returns:
        {"status": "success", "data": {"location_name": ..., "forecast_days": N, "daily_forecasts": [...]}} or
        {"status": "error", "error": "..."}
    """
    location_id = params.get("location_id")
    if not location_id:
        return {"status": "error", "error": "Missing required parameter: location_id"}

    days = params.get("days", 5)

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        locations = data_store.load_locations()
        forecasts = data_store.load_forecasts()

        # Verify location exists
        location = None
        for loc in locations:
            if loc.location_id == location_id:
                location = loc
                break

        if not location:
            return {"status": "error", "error": f"Location {location_id} not found"}

        daily_forecasts = get_forecast(location_id, days, forecasts)

        if not daily_forecasts:
            return {"status": "error", "error": f"No forecast available for {location.name}"}

        return {
            "status": "success",
            "data": {
                "location_name": location.name,
                "forecast_days": len(daily_forecasts),
                "daily_forecasts": [f.model_dump(mode="json") for f in daily_forecasts]
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to get forecast: {str(e)}"}
