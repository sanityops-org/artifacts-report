#!/usr/bin/env python3
"""
pet_list: List adoptable pets, filtered by species, size, temperament, or age.

Only pets whose listing status is "available" are returned.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import filter_pets

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
            "description": "Restrict results by the breed's adult size class"
        },
        "temperament": {
            "type": "string",
            "enum": [
                "friendly", "energetic", "calm", "playful",
                "independent", "affectionate", "protective", "shy"
            ],
            "description": "Restrict results by a temperament trait of the pet's breed"
        },
        "max_age_months": {
            "type": "integer",
            "minimum": 0,
            "description": "Only include pets at or below this age in months"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List adoptable pets.

    Args:
        params:
            - species: "dog" or "cat" (optional)
            - size: Adult size class (optional)
            - temperament: Temperament trait (optional)
            - max_age_months: Age ceiling in months (optional)

    Returns:
        {"status": "success", "data": {"pets": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    try:
        store = get_data_store(str(project_root / "data"))
        pets = store.load_pets()
        breeds = store.load_breeds()

        results = filter_pets(
            pets=pets,
            breeds=breeds,
            species=params.get("species"),
            size=params.get("size"),
            temperament=params.get("temperament"),
            max_age_months=params.get("max_age_months")
        )

        breed_by_id = {b.breed_id: b for b in breeds}
        enriched = []
        for pet in results:
            entry = pet.model_dump(mode="json")
            breed = breed_by_id.get(pet.breed_id)
            entry["breed_name"] = breed.name if breed else None
            entry["breed_size"] = breed.size.value if breed else None
            enriched.append(entry)

        return {
            "status": "success",
            "data": {
                "pets": enriched,
                "count": len(enriched)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Pet listing failed: {str(e)}"}
