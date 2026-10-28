#!/usr/bin/env python3
"""
breed_details: Get full characteristics for a single breed.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import get_breed_by_id

parameters = {
    "type": "object",
    "properties": {
        "breed_id": {
            "type": "string",
            "pattern": "^BREED\\d{3}$",
            "description": "Breed ID, e.g. BREED001"
        }
    },
    "required": ["breed_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed characteristics for one breed.

    Args:
        params:
            - breed_id: Breed ID (required)

    Returns:
        {"status": "success", "data": {...breed...}} or
        {"status": "error", "error": "..."}
    """
    breed_id = params.get("breed_id")
    if not breed_id:
        return {"status": "error", "error": "Missing required parameter: breed_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        breeds = store.load_breeds()

        breed = get_breed_by_id(breed_id, breeds)

        if not breed:
            return {"status": "error", "error": f"Breed not found: {breed_id}"}

        return {"status": "success", "data": breed.model_dump(mode="json")}

    except Exception as e:
        return {"status": "error", "error": f"Failed to get breed details: {str(e)}"}
