"""
Recipe search skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.recipe_search import execute as recipe_search
from tools.recipe_details import execute as recipe_details
from tools.recipe_by_ingredient import execute as recipe_by_ingredient

_TOOLS = {
    "recipe_search": recipe_search,
    "recipe_details": recipe_details,
    "recipe_by_ingredient": recipe_by_ingredient,
}


def run(intent: str, params: dict) -> dict:
    """
    Recipe search skill unified entry point.

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
