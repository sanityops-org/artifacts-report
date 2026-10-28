"""
Itinerary planning skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.itinerary_create import execute as itinerary_create
from tools.itinerary_details import execute as itinerary_details
from tools.budget_estimate import execute as budget_estimate

_TOOLS = {
    "itinerary_create": itinerary_create,
    "itinerary_details": itinerary_details,
    "budget_estimate": budget_estimate,
}


def run(intent: str, params: dict) -> dict:
    """
    Itinerary planning skill unified entry point.

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
