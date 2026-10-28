#!/usr/bin/env python3
"""shipment_get_status: Query current shipment status by tracking number.

Use this tool when the user provides a tracking number and wants to know the current
status of their shipment. Returns current location, status, ETA, and carrier information.
This tool is read-only and does not modify any shipment data.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.tracking_engine import get_shipment_status

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
    Query shipment status by tracking number.

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
        result = get_shipment_status(tracking_number, data_store)

        if not result.found:
            return {"status": "error", "error": result.error}

        shipment = result.shipment
        return {
            "status": "success",
            "data": {
                "tracking_number": shipment.tracking_number,
                "origin": shipment.origin,
                "destination": shipment.destination,
                "status": shipment.status.value,
                "carrier": {
                    "id": shipment.carrier_id,
                    "name": shipment.carrier_name,
                },
                "cargo_type": shipment.cargo_type.value,
                "weight_kg": shipment.weight_kg,
                "current_location": shipment.current_location,
                "pickup_date": shipment.pickup_date.isoformat() if shipment.pickup_date else None,
                "eta": shipment.eta.isoformat() if shipment.eta else None,
                "actual_delivery": shipment.actual_delivery.isoformat() if shipment.actual_delivery else None,
                "last_update": shipment.last_update.isoformat(),
                "notes": shipment.notes,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to query shipment status: {str(e)}"}


if __name__ == "__main__":
    print(execute({"tracking_number": "FR20260930000123"}))