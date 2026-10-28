#!/usr/bin/env python3
"""
recipe_by_ingredient: Find recipes that use a given ingredient.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.disclaimers import ALLERGEN_NOTE
from apis.recipe_engine import find_by_ingredient, total_minutes

parameters = {
    "type": "object",
    "properties": {
        "ingredient": {
            "type": "string",
            "description": "Ingredient name to look for (case-insensitive substring match)"
        }
    },
    "required": ["ingredient"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find recipes using an ingredient.

    Args:
        params:
            - ingredient: Ingredient name (required)

    Returns:
        {"status": "success", "data": {"recipes": [...], "count": N, "allergen_note": ...}} or
        {"status": "error", "error": "..."}
    """
    ingredient = params.get("ingredient")
    if not ingredient:
        return {"status": "error", "error": "Missing required parameter: ingredient"}

    try:
        store = get_data_store(str(project_root / "data"))
        recipes = store.load_recipes()

        results = find_by_ingredient(ingredient, recipes)

        summaries = []
        for recipe in results:
            summaries.append({
                "recipe_id": recipe.recipe_id,
                "name": recipe.name,
                "cuisine": recipe.cuisine.value,
                "total_minutes": total_minutes(recipe),
            })

        return {
            "status": "success",
            "data": {
                "ingredient": ingredient,
                "recipes": summaries,
                "count": len(summaries),
                "allergen_note": ALLERGEN_NOTE,
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Ingredient lookup failed: {str(e)}"}
