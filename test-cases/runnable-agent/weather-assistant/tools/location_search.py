#!/usr/bin/env python3
"""
location_search: Search for locations by name.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.weather_engine import search_locations

# Tool parameter schema for platform extraction
parameters = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Location name to search for (case-insensitive substring match)"
        }
    },
    "required": ["query"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search for locations by name.

    Args:
        params:
            - query: Search query (required)

    Returns:
        {"status": "success", "data": {"locations": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    # Parameter validation
    query = params.get("query")
    if not query:
        return {"status": "error", "error": "Missing required parameter: query"}

    try:
        data_store = DataStore(data_dir=str(project_root / "data"))
        locations = data_store.load_locations()

        matches = search_locations(query, locations)

        return {
            "status": "success",
            "data": {
                "locations": [loc.model_dump(mode="json") for loc in matches],
                "count": len(matches)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Location search failed: {str(e)}"}
