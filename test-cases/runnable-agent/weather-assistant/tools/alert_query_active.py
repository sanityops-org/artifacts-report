#!/usr/bin/env python3
"""
alert_query_active: Query all active severe weather alerts.
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
    "properties": {}
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query all active alerts.

    Args:
        params: No parameters required

    Returns:
        {"status": "success", "data": {"alerts": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        alerts = data_store.load_alerts()

        active = get_active_alerts(None, alerts)

        return {
            "status": "success",
            "data": {
                "alerts": [a.model_dump(mode="json") for a in active],
                "count": len(active)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to query alerts: {str(e)}"}
