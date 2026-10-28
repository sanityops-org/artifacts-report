#!/usr/bin/env python3
"""
watchlist_add: Add a movie or TV show to the watchlist.

Rejects unknown title IDs and titles already on the watchlist.
"""

import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import get_title_by_id
from models import WatchlistItem
from models.enums import WatchlistStatus

parameters = {
    "type": "object",
    "properties": {
        "title_id": {
            "type": "string",
            "pattern": "^TITLE\\d{4}$",
            "description": "Title ID to add, e.g. TITLE0003"
        }
    },
    "required": ["title_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a title to the watchlist.

    Args:
        params:
            - title_id: Title ID (required)

    Returns:
        {"status": "success", "data": {"item": {...}, "title": {...}}} or
        {"status": "error", "error": "..."}
    """
    title_id = params.get("title_id")
    if not title_id:
        return {"status": "error", "error": "Missing required parameter: title_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()
        watchlist = store.load_watchlist()

        title = get_title_by_id(title_id, titles)
        if not title:
            return {"status": "error", "error": f"Title not found: {title_id}"}

        if any(item.title_id == title_id for item in watchlist):
            return {
                "status": "error",
                "error": f"{title.title} is already on the watchlist"
            }

        item = WatchlistItem(
            item_id=store.next_watchlist_id(),
            title_id=title_id,
            status=WatchlistStatus.TO_WATCH,
            added_date=date.today().isoformat()
        )

        watchlist.append(item)
        store.save_watchlist(watchlist)

        return {
            "status": "success",
            "data": {
                "item": item.model_dump(mode="json"),
                "title": title.model_dump(mode="json"),
                "watchlist_count": len(watchlist)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to add to watchlist: {str(e)}"}
