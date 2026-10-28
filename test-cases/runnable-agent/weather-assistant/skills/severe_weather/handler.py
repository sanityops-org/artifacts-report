"""
severe_weather skill handler
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.alert_query_active import execute as alert_query_active
from tools.alert_query_by_location import execute as alert_query_by_location
from tools.alert_get_details import execute as alert_get_details
from tools.alert_subscribe import execute as alert_subscribe

_TOOLS = {
    "alert_query_active": alert_query_active,
    "alert_query_by_location": alert_query_by_location,
    "alert_get_details": alert_get_details,
    "alert_subscribe": alert_subscribe,
}


def run(intent: str, params: dict) -> dict:
    """
    Severe weather skill unified entry point.

    Args:
        intent: Operation name
        params: Tool parameters

    Returns:
        Tool execution result
    """
    tool_func = _TOOLS.get(intent)

    if tool_func is None:
        available_intents = list(_TOOLS.keys())
        return {
            "status": "error",
            "error": f"Unknown operation: {intent}, available operations: {available_intents}"
        }

    return tool_func(params)
