#!/usr/bin/env python3
"""
get_recommendations: Recommend movies and TV shows by genre and/or viewing mood.

With no filters, returns the highest-rated titles across the whole catalog.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.recommendation_engine import get_recommendations

parameters = {
    "type": "object",
    "properties": {
        "genre": {
            "type": "string",
            "enum": [
                "action", "comedy", "drama", "horror", "romance",
                "sci_fi", "thriller", "documentary", "animation", "fantasy"
            ],
            "description": "Restrict recommendations to a genre"
        },
        "mood": {
            "type": "string",
            "enum": ["happy", "sad", "excited", "relaxed", "thrilled", "thoughtful"],
            "description": "Restrict recommendations to a viewing mood"
        },
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 30,
            "description": "Maximum number of recommendations (default 10)"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get recommendations filtered by genre and/or mood.

    Args:
        params:
            - genre: Genre filter (optional)
            - mood: Mood filter (optional)
            - limit: Maximum results (optional, default 10)

    Returns:
        {"status": "success", "data": {"titles": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        limit = params.get("limit", 10)

        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()

        results = get_recommendations(
            titles=titles,
            genre=params.get("genre"),
            mood=params.get("mood"),
            limit=limit
        )

        return {
            "status": "success",
            "data": {
                "titles": [t.model_dump(mode="json") for t in results],
                "count": len(results),
                "note": "Recommendations are suggestions based on simulated data, not real-time trends."
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Recommendation failed: {str(e)}"}
