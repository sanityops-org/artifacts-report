"""
Title search skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.title_search import execute as title_search
from tools.title_details import execute as title_details
from tools.title_by_actor import execute as title_by_actor
from tools.title_by_director import execute as title_by_director

_TOOLS = {
    "title_search": title_search,
    "title_details": title_details,
    "title_by_actor": title_by_actor,
    "title_by_director": title_by_director,
}


def run(intent: str, params: dict) -> dict:
    """
    Title search skill unified entry point.

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
