#!/usr/bin/env python3
"""
care_task_complete: Mark a care task as done.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from models.enums import CareTaskStatus

parameters = {
    "type": "object",
    "properties": {
        "task_id": {
            "type": "string",
            "pattern": "^TASK\\d{4}$",
            "description": "Task ID to complete, e.g. TASK0001"
        },
        "skipped": {
            "type": "boolean",
            "description": "Mark the task as skipped instead of done (default false)"
        }
    },
    "required": ["task_id"]
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a care task as done, or skipped when requested.

    Args:
        params:
            - task_id: Task ID (required)
            - skipped: Mark as skipped rather than done (optional)

    Returns:
        {"status": "success", "data": {"task": {...}}} or
        {"status": "error", "error": "..."}
    """
    task_id = params.get("task_id")
    if not task_id:
        return {"status": "error", "error": "Missing required parameter: task_id"}

    skipped = bool(params.get("skipped", False))

    try:
        store = get_data_store(str(project_root / "data"))
        tasks = store.load_care_tasks()

        task = next((t for t in tasks if t.task_id == task_id), None)
        if not task:
            return {"status": "error", "error": f"Task not found: {task_id}"}

        if task.status != CareTaskStatus.PENDING:
            return {
                "status": "error",
                "error": f"Task {task_id} is already marked {task.status.value}"
            }

        task.status = CareTaskStatus.SKIPPED if skipped else CareTaskStatus.DONE
        store.save_care_tasks(tasks)

        return {
            "status": "success",
            "data": {"task": task.model_dump(mode="json")}
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to complete care task: {str(e)}"}
