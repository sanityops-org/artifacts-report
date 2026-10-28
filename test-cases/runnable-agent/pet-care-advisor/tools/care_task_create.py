#!/usr/bin/env python3
"""
care_task_create: Add a care task for a pet.

Only values supplied by the user are stored — the tool never invents a feeding
amount, medication name, or dose.
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import get_pet_by_id
from models import CareTask
from models.enums import CareTaskStatus, CareTaskType, TaskFrequency

parameters = {
    "type": "object",
    "properties": {
        "pet_id": {
            "type": "string",
            "pattern": "^PET\\d{3}$",
            "description": "Pet ID the task belongs to"
        },
        "type": {
            "type": "string",
            "enum": ["feeding", "walk", "grooming", "medication", "vet_visit", "play", "training"],
            "description": "Care task type"
        },
        "scheduled_time": {
            "type": "string",
            "pattern": "^\\d{2}:\\d{2}$",
            "description": "Time of day in HH:MM form"
        },
        "frequency": {
            "type": "string",
            "enum": ["once", "daily", "weekly"],
            "description": "Recurrence (default daily)"
        },
        "scheduled_date": {
            "type": "string",
            "description": "Date in YYYY-MM-DD form; required for once and weekly tasks"
        },
        "notes": {
            "type": "string",
            "description": "Notes supplied by the user, stored verbatim"
        }
    },
    "required": ["pet_id", "type", "scheduled_time"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a care task.

    Args:
        params:
            - pet_id: Pet ID (required)
            - type: Care task type (required)
            - scheduled_time: HH:MM (required)
            - frequency: once / daily / weekly (optional, default daily)
            - scheduled_date: YYYY-MM-DD, required for once and weekly (optional)
            - notes: User-supplied notes (optional)

    Returns:
        {"status": "success", "data": {"task": {...}}} or
        {"status": "error", "error": "..."}
    """
    pet_id = params.get("pet_id")
    task_type = params.get("type")
    scheduled_time = params.get("scheduled_time")

    if not pet_id:
        return {"status": "error", "error": "Missing required parameter: pet_id"}
    if not task_type:
        return {"status": "error", "error": "Missing required parameter: type"}
    if not scheduled_time:
        return {"status": "error", "error": "Missing required parameter: scheduled_time"}

    if not re.fullmatch(r"\d{2}:\d{2}", str(scheduled_time)):
        return {
            "status": "error",
            "error": f"scheduled_time must be in HH:MM form, got {scheduled_time!r}"
        }

    hours, minutes = (int(part) for part in str(scheduled_time).split(":"))
    if hours > 23 or minutes > 59:
        return {
            "status": "error",
            "error": f"scheduled_time must be a valid time of day, got {scheduled_time!r}"
        }

    try:
        task_type_enum = CareTaskType(str(task_type).lower())
    except ValueError:
        valid = [t.value for t in CareTaskType]
        return {
            "status": "error",
            "error": f"Unknown task type: {task_type}. Valid types: {valid}"
        }

    frequency_raw = params.get("frequency", "daily")
    try:
        frequency_enum = TaskFrequency(str(frequency_raw).lower())
    except ValueError:
        valid = [f.value for f in TaskFrequency]
        return {
            "status": "error",
            "error": f"Unknown frequency: {frequency_raw}. Valid frequencies: {valid}"
        }

    scheduled_date = params.get("scheduled_date")
    if frequency_enum in (TaskFrequency.ONCE, TaskFrequency.WEEKLY) and not scheduled_date:
        return {
            "status": "error",
            "error": f"scheduled_date is required for {frequency_enum.value} tasks"
        }

    if scheduled_date:
        try:
            datetime.strptime(str(scheduled_date), "%Y-%m-%d")
        except ValueError:
            return {
                "status": "error",
                "error": f"scheduled_date must be in YYYY-MM-DD form, got {scheduled_date!r}"
            }

    try:
        store = get_data_store(str(project_root / "data"))
        pets = store.load_pets()
        tasks = store.load_care_tasks()

        pet = get_pet_by_id(pet_id, pets)
        if not pet:
            return {"status": "error", "error": f"Pet not found: {pet_id}"}

        task = CareTask(
            task_id=store.next_task_id(),
            pet_id=pet_id,
            type=task_type_enum,
            scheduled_time=str(scheduled_time),
            frequency=frequency_enum,
            scheduled_date=scheduled_date,
            status=CareTaskStatus.PENDING,
            notes=params.get("notes"),
            created_at=datetime.now().isoformat(timespec="seconds")
        )

        tasks.append(task)
        store.save_care_tasks(tasks)

        return {
            "status": "success",
            "data": {
                "task": task.model_dump(mode="json"),
                "pet_name": pet.name,
                "task_count": len(tasks)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to create care task: {str(e)}"}
