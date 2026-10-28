#!/usr/bin/env python3
"""
care_schedule_today: Show today's outstanding care tasks across all pets.
"""

import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.care_engine import tasks_due_on
from apis.data_store import get_data_store
from apis.matching_engine import get_pet_by_id

parameters = {
    "type": "object",
    "properties": {
        "include_done": {
            "type": "boolean",
            "description": "Include tasks already marked done (default false)"
        },
        "date": {
            "type": "string",
            "description": "Date to report on in YYYY-MM-DD form (default today)"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List the care tasks scheduled for a given day.

    Args:
        params:
            - include_done: Keep completed tasks in the result (optional)
            - date: Target date, YYYY-MM-DD (optional, defaults to today)

    Returns:
        {"status": "success", "data": {"date": ..., "tasks": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    target_date = params.get("date") or date.today().isoformat()
    include_done = bool(params.get("include_done", False))

    try:
        store = get_data_store(str(project_root / "data"))
        tasks = store.load_care_tasks()
        pets = store.load_pets()

        due = tasks_due_on(target_date, tasks, include_done=include_done)

        enriched = []
        for task in due:
            entry = task.model_dump(mode="json")
            pet = get_pet_by_id(task.pet_id, pets)
            entry["pet_name"] = pet.name if pet else None
            enriched.append(entry)

        return {
            "status": "success",
            "data": {
                "date": target_date,
                "tasks": enriched,
                "count": len(enriched)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to build today's schedule: {str(e)}"}
