"""
Nutrition tracking skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.nutrition_log_meal import execute as nutrition_log_meal
from tools.nutrition_daily_summary import execute as nutrition_daily_summary
from tools.nutrition_targets_get import execute as nutrition_targets_get

_TOOLS = {
    "nutrition_log_meal": nutrition_log_meal,
    "nutrition_daily_summary": nutrition_daily_summary,
    "nutrition_targets_get": nutrition_targets_get,
}


def run(intent: str, params: dict) -> dict:
    """
    Nutrition tracking skill unified entry point.

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
