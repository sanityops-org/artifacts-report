"""
Pet matching skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.breed_search import execute as breed_search
from tools.breed_details import execute as breed_details
from tools.pet_list import execute as pet_list
from tools.pet_details import execute as pet_details

_TOOLS = {
    "breed_search": breed_search,
    "breed_details": breed_details,
    "pet_list": pet_list,
    "pet_details": pet_details,
}


def run(intent: str, params: dict) -> dict:
    """
    Pet matching skill unified entry point.

    Args:
        intent: Operation name
        params: Tool parameters

    Returns:
        Tool execution result
    """
    tool_func = _TOOLS.get(intent)

    if tool_func is None:
        return {
            "status": "error",
            "error": f"Unknown operation: {intent}, available operations: {list(_TOOLS.keys())}"
        }

    return tool_func(params)
