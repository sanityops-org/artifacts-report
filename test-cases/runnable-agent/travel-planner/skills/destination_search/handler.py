"""
Destination search skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.destination_search import execute as destination_search
from tools.destination_details import execute as destination_details
from tools.attraction_list import execute as attraction_list
from tools.attraction_details import execute as attraction_details

_TOOLS = {
    "destination_search": destination_search,
    "destination_details": destination_details,
    "attraction_list": attraction_list,
    "attraction_details": attraction_details,
}


def run(intent: str, params: dict) -> dict:
    """
    Destination search skill unified entry point.

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
