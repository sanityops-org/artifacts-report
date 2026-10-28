"""
weather_query skill handler
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.location_search import execute as location_search
from tools.weather_current import execute as weather_current
from tools.weather_forecast import execute as weather_forecast

_TOOLS = {
    "location_search": location_search,
    "weather_current": weather_current,
    "weather_forecast": weather_forecast,
}


def run(intent: str, params: dict) -> dict:
    """
    Weather query skill unified entry point.

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
