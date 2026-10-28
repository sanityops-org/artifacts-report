"""
Meal planning skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.meal_plan_create import execute as meal_plan_create
from tools.meal_plan_get import execute as meal_plan_get
from tools.meal_plan_add_entry import execute as meal_plan_add_entry
from tools.shopping_list_generate import execute as shopping_list_generate

_TOOLS = {
    "meal_plan_create": meal_plan_create,
    "meal_plan_get": meal_plan_get,
    "meal_plan_add_entry": meal_plan_add_entry,
    "shopping_list_generate": shopping_list_generate,
}


def run(intent: str, params: dict) -> dict:
    """
    Meal planning skill unified entry point.

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
