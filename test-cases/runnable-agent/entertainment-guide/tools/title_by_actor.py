#!/usr/bin/env python3
"""
title_by_actor: Find movies and TV shows featuring a given actor.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.search_engine import find_by_actor

parameters = {
    "type": "object",
    "properties": {
        "actor_name": {
            "type": "string",
            "description": "Actor name (case-insensitive substring match)"
        }
    },
    "required": ["actor_name"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find titles featuring an actor.

    Args:
        params:
            - actor_name: Actor name (required)

    Returns:
        {"status": "success", "data": {"titles": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    actor_name = params.get("actor_name")
    if not actor_name:
        return {"status": "error", "error": "Missing required parameter: actor_name"}

    try:
        store = get_data_store(str(project_root / "data"))
        titles = store.load_titles()

        results = find_by_actor(actor_name, titles)

        return {
            "status": "success",
            "data": {
                "actor_name": actor_name,
                "titles": [t.model_dump(mode="json") for t in results],
                "count": len(results)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Actor search failed: {str(e)}"}
