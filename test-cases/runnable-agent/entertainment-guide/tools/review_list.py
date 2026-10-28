#!/usr/bin/env python3
"""
review_list: List user reviews for a title, with the average review rating.
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
            "description": "Title ID, e.g. TITLE0001"
        }
    },
    "required": ["title_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List reviews for a title.

    Args:
        params:
            - title_id: Title ID (required)

    Returns:
        {"status": "success", "data": {"title_name": ..., "reviews": [...], "count": N, "average_rating": x}} or
        {"status": "error", "error": "..."}
    """
    title_id = params.get("title_id")
    if not title_id:
        return {"status": "error", "error": "Missing required parameter: title_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()
        reviews = store.load_reviews()

        title = get_title_by_id(title_id, titles)
        if not title:
            return {"status": "error", "error": f"Title not found: {title_id}"}

        matching = [r for r in reviews if r.title_id == title_id]
        matching.sort(key=lambda r: r.review_id)

        average = round(sum(r.rating for r in matching) / len(matching), 2) if matching else None

        return {
            "status": "success",
            "data": {
                "title_id": title_id,
                "title_name": title.title,
                "reviews": [r.model_dump(mode="json") for r in matching],
                "count": len(matching),
                "average_rating": average
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to list reviews: {str(e)}"}
