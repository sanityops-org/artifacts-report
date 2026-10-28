#!/usr/bin/env python3
"""
title_by_director: Find movies and TV shows by a given director.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import find_by_director

parameters = {
    "type": "object",
    "properties": {
        "director_name": {
            "type": "string",
            "description": "Director name (case-insensitive substring match)"
        }
    },
    "required": ["director_name"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find titles by a director.

    Args:
        params:
            - director_name: Director name (required)

    Returns:
        {"status": "success", "data": {"titles": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    director_name = params.get("director_name")
    if not director_name:
        return {"status": "error", "error": "Missing required parameter: director_name"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()

        results = find_by_director(director_name, titles)

        return {
            "status": "success",
            "data": {
                "director_name": director_name,
                "titles": [t.model_dump(mode="json") for t in results],
                "count": len(results)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Director search failed: {str(e)}"}
