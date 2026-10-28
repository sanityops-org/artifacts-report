#!/usr/bin/env python3
"""
title_details: Get full details for a single movie or TV show.
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
    Get detailed information for one title.

    Args:
        params:
            - title_id: Title ID (required)

    Returns:
        {"status": "success", "data": {...title...}} or
        {"status": "error", "error": "..."}
    """
    title_id = params.get("title_id")
    if not title_id:
        return {"status": "error", "error": "Missing required parameter: title_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()

        title = get_title_by_id(title_id, titles)

        if not title:
            return {"status": "error", "error": f"Title not found: {title_id}"}

        return {"status": "success", "data": title.model_dump(mode="json")}

    except Exception as e:
        return {"status": "error", "error": f"Failed to get title details: {str(e)}"}
