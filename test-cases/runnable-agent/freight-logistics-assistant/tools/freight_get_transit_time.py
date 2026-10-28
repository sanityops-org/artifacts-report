#!/usr/bin/env python3
"""freight_get_transit_time: Get estimated transit time between locations.

Use this tool when the user wants to know how long a shipment will take to travel
between origin and destination. Returns minimum, maximum, and average transit days
based on distance and service level.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.pricing_engine import get_transit_time
from models.enums import ServiceLevel

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "origin": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Origin city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "destination": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Destination city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "carrier_id": {
            "type": "string",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^C\\d{3}$",
            "description": "Specific carrier ID (format: C followed by 3 digits, e.g., C001). Optional.",
        },
        "service_level": {
            "type": "string",
            "minLength": 7,
            "maxLength": 8,
            "enum": ["economy", "standard", "express"],
            "description": "Service level. Affects transit time. Optional.",
        },
    },
    "required": ["origin", "destination"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get estimated transit time between locations.

    Args:
        params: {"origin": str, "destination": str, "carrier_id": str, "service_level": str}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    origin = params.get("origin")
    destination = params.get("destination")

    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

    try:
        data_store = DataStore(data_dir=project_root / "data")

        service_level = None
        if params.get("service_level"):
            service_level = ServiceLevel(params["service_level"])

        result = get_transit_time(
            origin=origin,
            destination=destination,
            data_store=data_store,
            carrier_id=params.get("carrier_id"),
            service_level=service_level,
        )

        return {
            "status": "success",
            "data": {
                "origin": result.origin,
                "destination": result.destination,
                "transit_days": {
                    "min": result.min_days,
                    "max": result.max_days,
                    "average": result.average_days,
                },
                "carrier": result.carrier,
                "service_level": result.service_level.value if result.service_level else None,
                "factors": result.factors,
                "note": "Transit times are estimates and may vary due to weather, traffic, or other conditions.",
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to get transit time: {str(e)}"}


if __name__ == "__main__":
    print(execute({"origin": "Shanghai", "destination": "Beijing"}))