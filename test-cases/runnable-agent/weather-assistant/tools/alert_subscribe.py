#!/usr/bin/env python3
"""
alert_subscribe: Subscribe to alerts for a location (simulated).
"""

import sys
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore

# In-memory subscription storage (simulated)
_subscriptions = []
_next_sub_id = 1

parameters = {
    "type": "object",
    "properties": {
        "location_id": {
            "type": "string",
            "pattern": "^LOC\\d{3}$",
            "description": "Location ID to subscribe to"
        }
    },
    "required": ["location_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Subscribe to alerts (simulated).

    Args:
        params:
            - location_id: Location ID (required)

    Returns:
        {"status": "success", "data": {"subscription_id": ..., "message": ...}} or
        {"status": "error", "error": "..."}
    """
    global _next_sub_id

    location_id = params.get("location_id")
    if not location_id:
        return {"status": "error", "error": "Missing required parameter: location_id"}

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        locations = data_store.load_locations()

        # Verify location exists
        location = None
        for loc in locations:
            if loc.location_id == location_id:
                location = loc
                break

        if not location:
            return {"status": "error", "error": f"Location {location_id} not found"}

        # Create subscription (simulated)
        subscription_id = f"SUB{_next_sub_id:03d}"
        _next_sub_id += 1

        subscription = {
            "subscription_id": subscription_id,
            "location_id": location_id,
            "location_name": location.name,
            "created_at": datetime.now().isoformat()
        }
        _subscriptions.append(subscription)

        return {
            "status": "success",
            "data": {
                "subscription_id": subscription_id,
                "message": f"You will receive alerts for {location.name}"
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to subscribe: {str(e)}"}
