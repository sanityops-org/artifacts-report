#!/usr/bin/env python3
"""
equipment_query_task: Query the task of the device.

Support filtering by device ID, task ID and task status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import TaskStatus


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform device task query.

    Args:
        params:
            - equip_id: Device ID filtering (optional)
            - task_id: Task ID, exact matching (optional)
            - status: Task status filtering (optional)

    Returns:
        {"status": "success", "count": N, "tasks": [...]} Someone
        {"status": "error", "error": "..."}
    """
    equip_id = params.get("equip_id")
    task_id = params.get("task_id")
    status = params.get("status")

    data_store = DataStore(data_dir=project_root / "data")

    try:
        tasks = data_store.load_tasks()

        # Filter accurately by task ID
        if task_id:
            tasks = [t for t in tasks if t.task_id == task_id]

        # Filter by device ID
        if equip_id:
            tasks = [t for t in tasks if t.equip_id == equip_id]

        # Filter by status
        if status:
            try:
                status_enum = TaskStatus(status) if isinstance(status, str) else status
                tasks = [t for t in tasks if t.status == status_enum]
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid task status: {status}, valid value: {[s.value for s in TaskStatus]}"
                }

        # Construction return results
        task_list = []
        for t in tasks:
            item = {
                "task_id": t.task_id,
                "task_type": t.task_type.value,
                "status": t.status.value,
                "estimated_duration": t.estimated_duration,
            }
            # Add optional fields
            if t.equip_id:
                item["equip_id"] = t.equip_id
            if t.container_id:
                item["container_id"] = t.container_id
            if t.vessel_id:
                item["vessel_id"] = t.vessel_id
            if t.source_location:
                item["source_location"] = t.source_location
            if t.target_location:
                item["target_location"] = t.target_location
            if t.created_at:
                item["created_at"] = t.created_at
            task_list.append(item)

        return {
            "status": "success",
            "count": len(task_list),
            "tasks": task_list
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the device task: {str(e)}"
        }
