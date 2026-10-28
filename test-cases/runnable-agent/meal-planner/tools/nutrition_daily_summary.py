#!/usr/bin/env python3
"""
nutrition_daily_summary: Total the meals logged on a date and compare them to daily targets.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.disclaimers import DIETITIAN_NOTE, ESTIMATE_DISCLAIMER
from apis.nutrition_engine import compare_to_targets, daily_totals

parameters = {
    "type": "object",
    "properties": {
        "date": {
            "type": "string",
            "description": "Date to summarise in YYYY-MM-DD form"
        }
    },
    "required": ["date"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarise a day's logged nutrition against the daily targets.

    Args:
        params:
            - date: YYYY-MM-DD (required)

    Returns:
        {"status": "success", "data": {"date": ..., "totals": {...}, "comparison": {...}, ...}} or
        {"status": "error", "error": "..."}
    """
    target_date = params.get("date")
    if not target_date:
        return {"status": "error", "error": "Missing required parameter: date"}

    try:
        datetime.strptime(str(target_date), "%Y-%m-%d")
    except ValueError:
        return {"status": "error", "error": f"date must be in YYYY-MM-DD form, got {target_date!r}"}

    try:
        store = get_data_store(str(project_root / "data"))
        recipes = store.load_recipes()
        log = store.load_nutrition_log()
        targets = store.load_targets()

        totals = daily_totals(str(target_date), log, recipes)

        comparison = None
        if targets is not None:
            comparison = compare_to_targets(totals, targets)

        return {
            "status": "success",
            "data": {
                "date": str(target_date),
                "totals": totals,
                "targets": targets.model_dump(mode="json") if targets else None,
                "comparison": comparison,
                "is_estimate": True,
                "disclaimer": ESTIMATE_DISCLAIMER,
                "dietitian_note": DIETITIAN_NOTE,
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to build daily summary: {str(e)}"}
