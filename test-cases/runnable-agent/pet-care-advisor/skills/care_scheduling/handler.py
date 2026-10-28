"""
Care scheduling skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.care_task_list import execute as care_task_list
from tools.care_task_create import execute as care_task_create
from tools.care_task_complete import execute as care_task_complete
from tools.care_schedule_today import execute as care_schedule_today

_TOOLS = {
    "care_task_list": care_task_list,
    "care_task_create": care_task_create,
    "care_task_complete": care_task_complete,
    "care_schedule_today": care_schedule_today,
}


def run(intent: str, params: dict) -> dict:
    """
    Care scheduling skill unified entry point.

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
