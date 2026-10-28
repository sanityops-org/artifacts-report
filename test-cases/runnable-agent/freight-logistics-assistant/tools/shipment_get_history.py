#!/usr/bin/env python3
"""shipment_get_history: Get full tracking history for a shipment.

Use this tool when the user wants to see the complete tracking history for a shipment,
including all events from pickup to delivery. Requires a valid tracking number.
This tool is read-only and returns historical tracking events.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.tracking_engine import get_shipment_history

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "tracking_number": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16,
            "pattern": "^FR\\d{14}$",
            "description": "The shipment tracking number. Format: FR followed by exactly 14 digits (e.g., FR20260930000123).",
        },
    },
    "required": ["tracking_number"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get full tracking history for a shipment.

    Args:
        params: {"tracking_number": str}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    tracking_number = params.get("tracking_number")
    if not tracking_number:
        return {"status": "error", "error": "Missing required parameter: tracking_number"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        result = get_shipment_history(tracking_number, data_store)

        if not result.found:
            return {"status": "error", "error": result.error}

        shipment = result.shipment
        events = []
        for event in shipment.tracking_history:
            events.append({
                "timestamp": event.timestamp.isoformat(),
                "location": event.location,
                "status": event.status.value,
                "description": event.description,
            })

        return {
            "status": "success",
            "data": {
                "tracking_number": shipment.tracking_number,
                "origin": shipment.origin,
                "destination": shipment.destination,
                "current_status": shipment.status.value,
                "carrier_name": shipment.carrier_name,
                "tracking_history": events,
                "total_events": len(events),
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get tracking history: {str(e)}"}


if __name__ == "__main__":
    print(execute({"tracking_number": "FR20260930000123"}))