#!/usr/bin/env python3
"""
meal_plan_get: Read a meal plan with its entries enriched with recipe names.
"""

import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.plan_engine import plan_entries_with_recipes
from apis.disclaimers import ESTIMATE_DISCLAIMER

parameters = {
    "type": "object",
    "properties": {
        "plan_id": {
            "type": "string",
            "pattern": "^PLAN\\d{4}$",
            "description": "Plan ID, e.g. PLAN0001"
        }
    },
    "required": ["plan_id"]
}


def _dated_entries(plan: Any, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach the calendar date each entry falls on"""
    try:
        start = date.fromisoformat(plan.start_date)
    except ValueError:
        return entries

    for entry in entries:
        entry["date"] = (start + timedelta(days=entry["day_index"] - 1)).isoformat()

    return entries


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read a meal plan.

    Args:
        params:
            - plan_id: Plan ID (required)

    Returns:
        {"status": "success", "data": {"plan": {...}, "entries": [...], "entry_count": N}} or
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

        entries = _dated_entries(plan, plan_entries_with_recipes(plan, recipes))

        return {
            "status": "success",
            "data": {
                "plan": plan.model_dump(mode="json"),
                "entries": entries,
                "entry_count": len(entries),
                "nutrition_is_estimate": True,
                "disclaimer": ESTIMATE_DISCLAIMER,
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to read meal plan: {str(e)}"}
