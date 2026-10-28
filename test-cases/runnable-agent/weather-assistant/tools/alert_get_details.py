#!/usr/bin/env python3
"""
alert_get_details: Get full details of a specific alert.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.alert_engine import get_alert_by_id

parameters = {
    "type": "object",
    "properties": {
        "alert_id": {
            "type": "string",
            "pattern": "^ALT\\d{3}$",
            "description": "Alert ID"
        }
    },
    "required": ["alert_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get alert details.

    Args:
        params:
            - alert_id: Alert ID (required)

    Returns:
        {"status": "success", "data": {...alert details...}} or
        {"status": "error", "error": "..."}
    """
    alert_id = params.get("alert_id")
    if not alert_id:
        return {"status": "error", "error": "Missing required parameter: alert_id"}

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        alerts = data_store.load_alerts()

        alert = get_alert_by_id(alert_id, alerts)

        if not alert:
            return {"status": "error", "error": f"Alert {alert_id} not found"}

        return {"status": "success", "data": alert.model_dump(mode="json")}

    except Exception as e:
        return {"status": "error", "error": f"Failed to get alert details: {str(e)}"}
