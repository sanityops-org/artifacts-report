#!/usr/bin/env python3
"""
yard_query_rehandle: Query the pending box-turning task.

The task of turning over the box refers to the task of moving the container for various reasons.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import TaskType, TaskStatus


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the task list query of box-turning.

    Args:
        params:
            - status: Task status filtering (pending, assigned, in_progress, completed, failed, cancelled) (optional)

    Returns:
        {"status": "success", "data": {"tasks": [...], "count": N, "status_summary": {...}}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    status_filter = params.get("status")

    try:
        tasks = data_store.load_tasks()

        # Screening box-turning tasks (in-field box transfer)
        rehandle_tasks = [
            t for t in tasks if t.task_type == TaskType.YARD_MOVE
        ]

        # Filter by status
        if status_filter:
            try:
                status_enum = TaskStatus(status_filter)
                rehandle_tasks = [
                    t for t in rehandle_tasks if t.status == status_enum
                ]
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid task status: {status_filter}, the valid value is: {[s.value for s in TaskStatus]}"
                }

        # Sort by priority:pending > assigned > in_progress
        status_order = {
            TaskStatus.PENDING: 0,
            TaskStatus.ASSIGNED: 1,
            TaskStatus.IN_PROGRESS: 2,
            TaskStatus.COMPLETED: 3,
            TaskStatus.FAILED: 4,
            TaskStatus.CANCELLED: 5
        }
        rehandle_tasks.sort(key=lambda t: status_order.get(t.status, 99))

        # Count the number of tasks in each state
        status_counts = {}
        for status in TaskStatus:
            count = sum(1 for t in rehandle_tasks if t.status == status)
            if count > 0:
                status_counts[status.value] = count

        return {
            "status": "success",
            "data": {
                "tasks": [t.model_dump(mode="json") for t in rehandle_tasks],
                "count": len(rehandle_tasks),
                "status_summary": status_counts
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"The query box-turning task failed: {str(e)}"
        }
