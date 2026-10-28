#!/usr/bin/env python3
"""
breed_search: Search dog and cat breeds by species, size, temperament, or name.

With no parameters, returns the full breed catalog.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import search_breeds

parameters = {
    "type": "object",
    "properties": {
        "species": {
            "type": "string",
            "enum": ["dog", "cat"],
            "description": "Restrict results to a species"
        },
        "size": {
            "type": "string",
            "enum": ["small", "medium", "large"],
            "description": "Restrict results to an adult size class"
        },
        "temperament": {
            "type": "string",
            "enum": [
                "friendly", "energetic", "calm", "playful",
                "independent", "affectionate", "protective", "shy"
            ],
            "description": "Restrict results to breeds carrying this temperament trait"
        },
        "query": {
            "type": "string",
            "description": "Free-text query matched against breed name and description"
        },
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50,
            "description": "Maximum number of results (default 20, which covers the whole catalog)"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search breeds by species, size, temperament, or name.

    Args:
        params:
            - species: "dog" or "cat" (optional)
            - size: "small", "medium" or "large" (optional)
            - temperament: Temperament trait (optional)
            - query: Free-text search term (optional)
            - limit: Maximum results (optional, default 20)

    Returns:
        {"status": "success", "data": {"breeds": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        store = get_data_store(str(project_root / "data"))
        breeds = store.load_breeds()

        results = search_breeds(
            breeds=breeds,
            species=params.get("species"),
            size=params.get("size"),
            temperament=params.get("temperament"),
            query=params.get("query"),
            limit=params.get("limit", 20)
        )

        return {
            "status": "success",
            "data": {
                "breeds": [b.model_dump(mode="json") for b in results],
                "count": len(results)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Breed search failed: {str(e)}"}
