"""
Accommodation search skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.accommodation_search import execute as accommodation_search
from tools.accommodation_details import execute as accommodation_details

_TOOLS = {
    "accommodation_search": accommodation_search,
    "accommodation_details": accommodation_details,
}


def run(intent: str, params: dict) -> dict:
    """
    Accommodation search skill unified entry point.

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
