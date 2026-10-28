#!/usr/bin/env python3
"""
watchlist_list: List watchlist entries, optionally filtered by status.

Each entry is enriched with the title's name, type, and year.
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
        "status": {
            "type": "string",
            "enum": ["to_watch", "watched"],
            "description": "Filter by watch status"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List watchlist entries.

    Args:
        params:
            - status: "to_watch" or "watched" (optional)

    Returns:
        {"status": "success", "data": {"items": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    status_filter = params.get("status")

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()
        watchlist = store.load_watchlist()

        items = watchlist
        if status_filter:
            items = [i for i in watchlist if i.status.value == status_filter]

        enriched = []
        for item in items:
            title = get_title_by_id(item.title_id, titles)
            entry = item.model_dump(mode="json")
            entry["title_name"] = title.title if title else None
            entry["title_type"] = title.type.value if title else None
            entry["title_year"] = title.year if title else None
            enriched.append(entry)

        return {
            "status": "success",
            "data": {
                "items": enriched,
                "count": len(enriched),
                "total_watchlist_size": len(watchlist)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to list watchlist: {str(e)}"}
