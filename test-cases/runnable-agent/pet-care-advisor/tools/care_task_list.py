#!/usr/bin/env python3
"""
care_task_list: List care tasks, optionally filtered by pet or status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import get_pet_by_id

parameters = {
    "type": "object",
    "properties": {
        "pet_id": {
            "type": "string",
            "pattern": "^PET\\d{3}$",
            "description": "Restrict to one pet"
        },
        "status": {
            "type": "string",
            "enum": ["pending", "done", "skipped"],
            "description": "Restrict to one task status"
        }
    }
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List care tasks.

    Args:
        params:
            - pet_id: Pet ID filter (optional)
            - status: Task status filter (optional)

    Returns:
        {"status": "success", "data": {"tasks": [...], "count": N}} or
        {"status": "error", "error": "..."}
    """
    pet_id = params.get("pet_id")
    status_filter = params.get("status")

    try:
        store = get_data_store(str(project_root / "data"))
        tasks = store.load_care_tasks()
        pets = store.load_pets()

        if pet_id and not get_pet_by_id(pet_id, pets):
            return {"status": "error", "error": f"Pet not found: {pet_id}"}

        results = tasks
        if pet_id:
            results = [t for t in results if t.pet_id == pet_id]
        if status_filter:
            results = [t for t in results if t.status.value == status_filter]

        results = sorted(results, key=lambda t: (t.scheduled_time, t.task_id))

        enriched = []
        for task in results:
            entry = task.model_dump(mode="json")
            pet = get_pet_by_id(task.pet_id, pets)
            entry["pet_name"] = pet.name if pet else None
            enriched.append(entry)

        return {
            "status": "success",
            "data": {
                "tasks": enriched,
                "count": len(enriched)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to list care tasks: {str(e)}"}
