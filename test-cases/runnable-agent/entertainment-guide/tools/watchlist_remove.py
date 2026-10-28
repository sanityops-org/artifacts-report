#!/usr/bin/env python3
"""
watchlist_remove: Remove a movie or TV show from the watchlist.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import get_title_by_id

parameters = {
    "type": "object",
    "properties": {
        "title_id": {
            "type": "string",
            "pattern": "^TITLE\\d{4}$",
            "description": "Title ID to remove, e.g. TITLE0003"
        }
    },
    "required": ["title_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove a title from the watchlist.

    Args:
        params:
            - title_id: Title ID (required)

    Returns:
        {"status": "success", "data": {"removed": {...}, "watchlist_count": N}} or
        {"status": "error", "error": "..."}
    """
    title_id = params.get("title_id")
    if not title_id:
        return {"status": "error", "error": "Missing required parameter: title_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()
        watchlist = store.load_watchlist()

        removed = next((item for item in watchlist if item.title_id == title_id), None)
        if not removed:
            return {
                "status": "error",
                "error": f"Title {title_id} is not on the watchlist"
            }

        remaining = [item for item in watchlist if item.title_id != title_id]
        store.save_watchlist(remaining)

        title = get_title_by_id(title_id, titles)

        return {
            "status": "success",
            "data": {
                "removed": removed.model_dump(mode="json"),
                "title_name": title.title if title else None,
                "watchlist_count": len(remaining)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to remove from watchlist: {str(e)}"}
