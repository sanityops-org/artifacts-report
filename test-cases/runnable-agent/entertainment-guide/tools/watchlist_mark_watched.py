#!/usr/bin/env python3
"""
watchlist_mark_watched: Mark a watchlist entry as watched, with an optional rating.
"""

import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import get_title_by_id
from models.enums import WatchlistStatus

parameters = {
    "type": "object",
    "properties": {
        "title_id": {
            "type": "string",
            "pattern": "^TITLE\\d{4}$",
            "description": "Title ID to mark as watched"
        },
        "rating": {
            "type": "number",
            "minimum": 1.0,
            "maximum": 10.0,
            "description": "Your rating from 1.0 to 10.0 (optional)"
        }
    },
    "required": ["title_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a watchlist entry as watched.

    Args:
        params:
            - title_id: Title ID (required)
            - rating: User rating 1.0-10.0 (optional)

    Returns:
        {"status": "success", "data": {"item": {...}, "title_name": ...}} or
        {"status": "error", "error": "..."}
    """
    title_id = params.get("title_id")
    if not title_id:
        return {"status": "error", "error": "Missing required parameter: title_id"}

    rating = params.get("rating")
    if rating is not None:
        if not isinstance(rating, (int, float)) or isinstance(rating, bool):
            return {"status": "error", "error": "rating must be a number between 1.0 and 10.0"}
        if rating < 1.0 or rating > 10.0:
            return {"status": "error", "error": f"rating must be between 1.0 and 10.0, got {rating}"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()
        watchlist = store.load_watchlist()

        item = next((i for i in watchlist if i.title_id == title_id), None)
        if not item:
            return {
                "status": "error",
                "error": f"Title {title_id} is not on the watchlist"
            }

        item.status = WatchlistStatus.WATCHED
        item.watched_date = date.today().isoformat()
        if rating is not None:
            item.user_rating = float(rating)

        store.save_watchlist(watchlist)

        title = get_title_by_id(title_id, titles)

        return {
            "status": "success",
            "data": {
                "item": item.model_dump(mode="json"),
                "title_name": title.title if title else None
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to mark as watched: {str(e)}"}
