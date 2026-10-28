#!/usr/bin/env python3
"""
recipe_details: Get the full ingredient list, steps, and per-serving nutrition for a recipe.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.disclaimers import ALLERGEN_NOTE, ESTIMATE_DISCLAIMER
from apis.recipe_engine import get_recipe_by_id, total_minutes

parameters = {
    "type": "object",
    "properties": {
        "recipe_id": {
            "type": "string",
            "pattern": "^RECIPE\\d{3}$",
            "description": "Recipe ID, e.g. RECIPE001"
        }
    },
    "required": ["recipe_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get full details for one recipe.

    Args:
        params:
            - recipe_id: Recipe ID (required)

    Returns:
        {"status": "success", "data": {...recipe..., "nutrition_is_estimate": True, ...}} or
        {"status": "error", "error": "..."}
    """
    recipe_id = params.get("recipe_id")
    if not recipe_id:
        return {"status": "error", "error": "Missing required parameter: recipe_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        recipes = store.load_recipes()

        recipe = get_recipe_by_id(recipe_id, recipes)
        if not recipe:
            return {"status": "error", "error": f"Recipe not found: {recipe_id}"}

        payload = recipe.model_dump(mode="json")
        payload["total_minutes"] = total_minutes(recipe)
        payload["nutrition_is_estimate"] = True
        payload["disclaimer"] = ESTIMATE_DISCLAIMER
        payload["allergen_note"] = ALLERGEN_NOTE

        return {"status": "success", "data": payload}

    except Exception as e:
        return {"status": "error", "error": f"Failed to get recipe details: {str(e)}"}
