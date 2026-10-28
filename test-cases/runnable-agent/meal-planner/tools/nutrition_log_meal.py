#!/usr/bin/env python3
"""
nutrition_log_meal: Record a meal you ate, with a serving count.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.recipe_engine import get_recipe_by_id
from models import NutritionLogEntry
from models.enums import MealType

parameters = {
    "type": "object",
    "properties": {
        "date": {
            "type": "string",
            "description": "Date eaten in YYYY-MM-DD form"
        },
        "meal_type": {
            "type": "string",
            "enum": ["breakfast", "lunch", "dinner", "snack"],
            "description": "Meal slot"
        },
        "recipe_id": {
            "type": "string",
            "pattern": "^RECIPE\\d{3}$",
            "description": "Recipe that was eaten"
        },
        "servings": {
            "type": "integer",
            "minimum": 1,
            "maximum": 12,
            "description": "Servings eaten (default 1)"
        }
    },
    "required": ["date", "meal_type", "recipe_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Log a meal.

    Args:
        params:
            - date: YYYY-MM-DD (required)
            - meal_type: breakfast / lunch / dinner / snack (required)
            - recipe_id: Recipe ID (required)
            - servings: Servings eaten (optional, default 1)

    Returns:
        {"status": "success", "data": {"entry": {...}, "log_count": N}} or
        {"status": "error", "error": "..."}
    """
    entry_date = params.get("date")
    meal_type = params.get("meal_type")
    recipe_id = params.get("recipe_id")

    if not entry_date:
        return {"status": "error", "error": "Missing required parameter: date"}
    if not meal_type:
        return {"status": "error", "error": "Missing required parameter: meal_type"}
    if not recipe_id:
        return {"status": "error", "error": "Missing required parameter: recipe_id"}

    try:
        datetime.strptime(str(entry_date), "%Y-%m-%d")
    except ValueError:
        return {"status": "error", "error": f"date must be in YYYY-MM-DD form, got {entry_date!r}"}

    try:
        meal_type_enum = MealType(str(meal_type).lower())
    except ValueError:
        valid = [m.value for m in MealType]
        return {"status": "error", "error": f"Unknown meal_type: {meal_type}. Valid types: {valid}"}

    servings = params.get("servings", 1)
    if not isinstance(servings, int) or isinstance(servings, bool) or not (1 <= servings <= 12):
        return {"status": "error", "error": f"servings must be an integer between 1 and 12, got {servings!r}"}

    try:
        store = get_data_store(str(project_root / "data"))
        recipes = store.load_recipes()
        log = store.load_nutrition_log()

        recipe = get_recipe_by_id(recipe_id, recipes)
        if not recipe:
            return {"status": "error", "error": f"Recipe not found: {recipe_id}"}

        entry = NutritionLogEntry(
            log_id=store.next_log_id(),
            date=str(entry_date),
            meal_type=meal_type_enum,
            recipe_id=recipe_id,
            servings=servings
        )

        log.append(entry)
        store.save_nutrition_log(log)

        return {
            "status": "success",
            "data": {
                "entry": entry.model_dump(mode="json"),
                "recipe_name": recipe.name,
                "log_count": len(log)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to log meal: {str(e)}"}
