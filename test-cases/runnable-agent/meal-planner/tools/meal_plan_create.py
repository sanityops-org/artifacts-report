#!/usr/bin/env python3
"""
meal_plan_create: Create an empty multi-day meal plan.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from models import MealPlan

parameters = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "A name for the plan, e.g. 'Weeknight Basics'"
        },
        "start_date": {
            "type": "string",
            "description": "Start date in YYYY-MM-DD form"
        },
        "days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 14,
            "description": "Number of days the plan covers"
        }
    },
    "required": ["name", "start_date", "days"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a meal plan.

    Args:
        params:
            - name: Plan name (required)
            - start_date: YYYY-MM-DD (required)
            - days: Number of days, 1-14 (required)

    Returns:
        {"status": "success", "data": {"plan": {...}}} or
        {"status": "error", "error": "..."}
    """
    name = params.get("name")
    start_date = params.get("start_date")
    days = params.get("days")

    if not name:
        return {"status": "error", "error": "Missing required parameter: name"}
    if not start_date:
        return {"status": "error", "error": "Missing required parameter: start_date"}
    if days is None:
        return {"status": "error", "error": "Missing required parameter: days"}

    try:
        datetime.strptime(str(start_date), "%Y-%m-%d")
    except ValueError:
        return {"status": "error", "error": f"start_date must be in YYYY-MM-DD form, got {start_date!r}"}

    if not isinstance(days, int) or isinstance(days, bool) or not (1 <= days <= 14):
        return {"status": "error", "error": f"days must be an integer between 1 and 14, got {days!r}"}

    try:
        store = get_data_store(str(project_root / "data"))
        plans = store.load_meal_plans()

        plan = MealPlan(
            plan_id=store.next_plan_id(),
            name=str(name),
            start_date=str(start_date),
            days=days,
            entries=[]
        )

        plans.append(plan)
        store.save_meal_plans(plans)

        return {
            "status": "success",
            "data": {
                "plan": plan.model_dump(mode="json"),
                "plan_count": len(plans)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to create meal plan: {str(e)}"}
