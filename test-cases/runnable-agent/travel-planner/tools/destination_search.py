#!/usr/bin/env python3
"""
destination_search: Search destinations by query, country, or travel theme.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.destination_engine import DestinationEngine

parameters = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Search term (destination name, country, or keyword)"
        },
        "country": {
            "type": "string",
            "description": "Filter by country name"
        },
        "theme": {
            "type": "string",
            "description": "Filter by travel theme (beach, mountain, city, culture, adventure, family, romantic, foodie)"
        }
    }
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Search destinations by query, country, or theme.

    Args:
        params: Search parameters (query, country, theme)

    Returns:
        {"status": "success", "data": {"destinations": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        store = get_data_store(str(project_root / "data"))
        destinations = store.load_destinations()
        attractions = store.load_attractions()

        engine = DestinationEngine(destinations, attractions)
        results = engine.search_destinations(
            query=params.get("query"),
            country=params.get("country"),
            theme=params.get("theme")
        )

        return {
            "status": "success",
            "data": {
                "destinations": [d.model_dump(mode="json") for d in results],
                "count": len(results)
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Destination search failed: {str(e)}"}
