"""
Watchlist management skill handler.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.watchlist_add import execute as watchlist_add
from tools.watchlist_remove import execute as watchlist_remove
from tools.watchlist_list import execute as watchlist_list
from tools.watchlist_mark_watched import execute as watchlist_mark_watched
from tools.review_list import execute as review_list

_TOOLS = {
    "watchlist_add": watchlist_add,
    "watchlist_remove": watchlist_remove,
    "watchlist_list": watchlist_list,
    "watchlist_mark_watched": watchlist_mark_watched,
    "review_list": review_list,
}


def run(intent: str, params: dict) -> dict:
    """
    Watchlist management skill unified entry point.

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
