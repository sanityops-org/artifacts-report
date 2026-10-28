#!/usr/bin/env python3
"""
pet_details: Get one adoptable pet's profile together with its breed characteristics.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import get_breed_by_id, get_pet_by_id

parameters = {
    "type": "object",
    "properties": {
        "pet_id": {
            "type": "string",
            "pattern": "^PET\\d{3}$",
            "description": "Pet ID, e.g. PET001"
        }
    },
    "required": ["pet_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a pet's profile plus its resolved breed.

    Args:
        params:
            - pet_id: Pet ID (required)

    Returns:
        {"status": "success", "data": {"pet": {...}, "breed": {...}}} or
        {"status": "error", "error": "..."}
    """
    pet_id = params.get("pet_id")
    if not pet_id:
        return {"status": "error", "error": "Missing required parameter: pet_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        pets = store.load_pets()
        breeds = store.load_breeds()

        pet = get_pet_by_id(pet_id, pets)
        if not pet:
            return {"status": "error", "error": f"Pet not found: {pet_id}"}

        breed = get_breed_by_id(pet.breed_id, breeds)

        return {
            "status": "success",
            "data": {
                "pet": pet.model_dump(mode="json"),
                "breed": breed.model_dump(mode="json") if breed else None
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to get pet details: {str(e)}"}
