"""
Health tracking skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.health_record_list import execute as health_record_list
from tools.health_record_add import execute as health_record_add

_TOOLS = {
    "health_record_list": health_record_list,
    "health_record_add": health_record_add,
}


def run(intent: str, params: dict) -> dict:
    """
    Health tracking skill unified entry point.

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
