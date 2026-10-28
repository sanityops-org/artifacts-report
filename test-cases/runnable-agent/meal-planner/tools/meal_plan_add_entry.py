#!/usr/bin/env python3
"""
meal_plan_add_entry: Assign a recipe to a day and meal slot in a meal plan.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.recipe_engine import get_recipe_by_id
from models import PlanEntry
from models.enums import MealType

parameters = {
    "type": "object",
    "properties": {
        "plan_id": {
            "type": "string",
            "pattern": "^PLAN\\d{4}$",
            "description": "Plan ID to add the entry to"
        },
        "day_index": {
            "type": "integer",
            "minimum": 1,
            "maximum": 14,
            "description": "Day number within the plan, 1-based"
        },
        "meal_type": {
            "type": "string",
            "enum": ["breakfast", "lunch", "dinner", "snack"],
            "description": "Meal slot"
        },
        "recipe_id": {
            "type": "string",
            "pattern": "^RECIPE\\d{3}$",
            "description": "Recipe to plan"
        },
        "servings": {
            "type": "integer",
            "minimum": 1,
            "maximum": 12,
            "description": "Servings for this slot (default: the recipe's own serving count)"
        }
    },
    "required": ["plan_id", "day_index", "meal_type", "recipe_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a recipe to a meal plan slot.

    Args:
        params:
            - plan_id: Plan ID (required)
            - day_index: 1-based day number (required)
            - meal_type: breakfast / lunch / dinner / snack (required)
            - recipe_id: Recipe ID (required)
            - servings: Servings for this slot (optional)

    Returns:
        {"status": "success", "data": {"entry": {...}, "entry_count": N}} or
        {"status": "error", "error": "..."}
    """
    plan_id = params.get("plan_id")
    day_index = params.get("day_index")
    meal_type = params.get("meal_type")
    recipe_id = params.get("recipe_id")

    if not plan_id:
        return {"status": "error", "error": "Missing required parameter: plan_id"}
    if day_index is None:
        return {"status": "error", "error": "Missing required parameter: day_index"}
    if not meal_type:
        return {"status": "error", "error": "Missing required parameter: meal_type"}
    if not recipe_id:
        return {"status": "error", "error": "Missing required parameter: recipe_id"}

    if not isinstance(day_index, int) or isinstance(day_index, bool) or not (1 <= day_index <= 14):
        return {"status": "error", "error": f"day_index must be an integer between 1 and 14, got {day_index!r}"}

    try:
        meal_type_enum = MealType(str(meal_type).lower())
    except ValueError:
        valid = [m.value for m in MealType]
        return {"status": "error", "error": f"Unknown meal_type: {meal_type}. Valid types: {valid}"}

    try:
        store = get_data_store(str(project_root / "data"))
        plans = store.load_meal_plans()
        recipes = store.load_recipes()

        plan = next((p for p in plans if p.plan_id == plan_id), None)
        if not plan:
            return {"status": "error", "error": f"Meal plan not found: {plan_id}"}

        if day_index > plan.days:
            return {
                "status": "error",
                "error": f"day_index {day_index} is outside plan {plan_id}, which covers {plan.days} day(s)"
            }

        recipe = get_recipe_by_id(recipe_id, recipes)
        if not recipe:
            return {"status": "error", "error": f"Recipe not found: {recipe_id}"}

        servings = params.get("servings", recipe.servings)
        if not isinstance(servings, int) or isinstance(servings, bool) or not (1 <= servings <= 12):
            return {"status": "error", "error": f"servings must be an integer between 1 and 12, got {servings!r}"}

        entry = PlanEntry(
            entry_id=store.next_entry_id(),
            day_index=day_index,
            meal_type=meal_type_enum,
            recipe_id=recipe_id,
            servings=servings
        )

        plan.entries.append(entry)
        store.save_meal_plans(plans)

        return {
            "status": "success",
            "data": {
                "entry": entry.model_dump(mode="json"),
                "recipe_name": recipe.name,
                "entry_count": len(plan.entries)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to add plan entry: {str(e)}"}
