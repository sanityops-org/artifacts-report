#!/usr/bin/env python3
"""
title_search: Search movies and TV shows by title, director, cast, or genre.

With no parameters, returns the full catalog ranked by rating.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import search_titles

parameters = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Free-text query matched against title, director, cast, and synopsis"
        },
        "type": {
            "type": "string",
            "enum": ["movie", "tv_show"],
            "description": "Restrict results to movies or TV shows"
        },
        "genre": {
            "type": "string",
            "enum": [
                "action", "comedy", "drama", "horror", "romance",
                "sci_fi", "thriller", "documentary", "animation", "fantasy"
            ],
            "description": "Restrict results to a single genre"
        },
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50,
            "description": "Maximum number of results (default 20)"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search titles by query, type, or genre.

    Args:
        params:
            - query: Free-text search term (optional)
            - type: "movie" or "tv_show" (optional)
            - genre: Genre filter (optional)
            - limit: Maximum results (optional, default 20)

    Returns:
        {"status": "success", "data": {"titles": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        limit = params.get("limit", 20)

        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()

        results = search_titles(
            query=params.get("query"),
            title_type=params.get("type"),
            genre=params.get("genre"),
            titles=titles,
            limit=limit
        )

        return {
            "status": "success",
            "data": {
                "titles": [t.model_dump(mode="json") for t in results],
                "count": len(results)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Title search failed: {str(e)}"}
