#!/usr/bin/env python3
"""
shopping_list_generate: Roll a meal plan's ingredients up into one shopping list.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.plan_engine import build_shopping_list

parameters = {
    "type": "object",
    "properties": {
        "plan_id": {
            "type": "string",
            "pattern": "^PLAN\\d{4}$",
            "description": "Plan ID to shop for"
        }
    },
    "required": ["plan_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a shopping list for a meal plan.

    Quantities are scaled to each entry's serving count, and the same ingredient
    in the same unit is summed into a single line.

    Args:
        params:
            - plan_id: Plan ID (required)

    Returns:
        {"status": "success", "data": {"items": [...], "item_count": N, "unresolved": [...]}} or
        {"status": "error", "error": "..."}
    """
    plan_id = params.get("plan_id")
    if not plan_id:
        return {"status": "error", "error": "Missing required parameter: plan_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        plans = store.load_meal_plans()
        recipes = store.load_recipes()

        plan = next((p for p in plans if p.plan_id == plan_id), None)
        if not plan:
            return {"status": "error", "error": f"Meal plan not found: {plan_id}"}

        result = build_shopping_list(plan, recipes)

        return {"status": "success", "data": result}

    except Exception as e:
        return {"status": "error", "error": f"Failed to generate shopping list: {str(e)}"}
