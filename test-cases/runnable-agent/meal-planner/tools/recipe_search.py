#!/usr/bin/env python3
"""
recipe_search: Search recipes by cuisine, diet tag, total time, name, or ingredient.

With no filters, returns the whole catalog ordered by total time.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.disclaimers import ALLERGEN_NOTE, ESTIMATE_DISCLAIMER
from apis.recipe_engine import search_recipes, total_minutes

parameters = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Matched against the recipe name and its ingredient names"
        },
        "cuisine": {
            "type": "string",
            "enum": ["italian", "japanese", "mexican", "indian", "asian",
                     "mediterranean", "american", "thai"],
            "description": "Restrict results to a cuisine"
        },
        "diet": {
            "type": "string",
            "enum": ["vegetarian", "vegan", "gluten_free", "dairy_free",
                     "low_carb", "high_protein", "pescatarian", "nut_free"],
            "description": "Restrict results to recipes carrying this diet label"
        },
        "max_total_minutes": {
            "type": "integer",
            "minimum": 1,
            "description": "Upper bound on prep plus cook time, in minutes"
        },
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50,
            "description": "Maximum number of results (default 20)"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search recipes.

    Args:
        params:
            - query: Free-text search term (optional)
            - cuisine: Cuisine filter (optional)
            - diet: Diet tag filter (optional)
            - max_total_minutes: Time ceiling (optional)
            - limit: Maximum results (optional, default 20)

    Returns:
        {"status": "success", "data": {"recipes": [...], "count": N, ...}} or
        {"status": "error", "error": "..."}
    """
    try:
        store = get_data_store(str(project_root / "data"))
        recipes = store.load_recipes()

        results = search_recipes(
            recipes=recipes,
            query=params.get("query"),
            cuisine=params.get("cuisine"),
            diet=params.get("diet"),
            max_total_minutes=params.get("max_total_minutes"),
            limit=params.get("limit", 20)
        )

        summaries = []
        for recipe in results:
            summaries.append({
                "recipe_id": recipe.recipe_id,
                "name": recipe.name,
                "cuisine": recipe.cuisine.value,
                "diet_tags": [t.value for t in recipe.diet_tags],
                "total_minutes": total_minutes(recipe),
                "servings": recipe.servings,
                "calories_per_serving": recipe.nutrition_per_serving.calories,
            })

        return {
            "status": "success",
            "data": {
                "recipes": summaries,
                "count": len(summaries),
                "nutrition_is_estimate": True,
                "disclaimer": ESTIMATE_DISCLAIMER,
                "allergen_note": ALLERGEN_NOTE,
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Recipe search failed: {str(e)}"}
