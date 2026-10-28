#!/usr/bin/env python3
"""
alert_query_by_location: Query active alerts for a specific location.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.alert_engine import get_active_alerts

parameters = {
    "type": "object",
    "properties": {
        "location_id": {
            "type": "string",
            "pattern": "^LOC\\d{3}$",
            "description": "Location ID"
        }
    },
    "required": ["location_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query alerts for a location.

    Args:
        params:
            - location_id: Location ID (required)

    Returns:
        {"status": "success", "data": {"alerts": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    location_id = params.get("location_id")
    if not location_id:
        return {"status": "error", "error": "Missing required parameter: location_id"}

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        alerts = data_store.load_alerts()

        active = get_active_alerts(location_id, alerts)

        return {
            "status": "success",
            "data": {
                "alerts": [a.model_dump(mode="json") for a in active],
                "count": len(active)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to query alerts: {str(e)}"}
