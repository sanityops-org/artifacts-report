#!/usr/bin/env python3
"""
equipment_cancel_task: Cancel the task and release the device.

Set the task status to cancelled and release the associated device.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import TaskStatus, EquipmentStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cancel the execution task.

    Args:
        params:
            - task_id: Task ID (required)

    Returns:
        {"status": "success", "message": "...", "released_equipment": {...}} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("equipment_cancel_task", params)
    if permission_error:
        return permission_error

    task_id = params.get("task_id")

    # Parameter verification
    if not task_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: task_id"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        tasks = data_store.load_tasks()
        equipment = data_store.load_equipment()

        # Find the task
        task = None
        for t in tasks:
            if t.task_id == task_id:
                task = t
                break

        if not task:
            return {
                "status": "error",
                "error": f"Task {task_id} does not exist"
            }

        # Check the task status
        if task.status == TaskStatus.COMPLETED:
            return {
                "status": "error",
                "error": f"Task {task_id} has been completed and cannot be canceled."
            }

        if task.status == TaskStatus.CANCELLED:
            return {
                "status": "error",
                "error": f"Task {task_id} has been canceled"
            }

        # Record the original device information
        released_equipment = None
        old_status = task.status
        old_equip_id = task.equip_id

        # If the task has assigned the device, release the device.
        if task.equip_id:
            equip = None
            for e in equipment:
                if e.equip_id == task.equip_id:
                    equip = e
                    break

            if equip:
                # Release the equipment
                equip.status = EquipmentStatus.IDLE
                equip.current_task = None
                released_equipment = {
                    "equip_id": equip.equip_id,
                    "equip_name": equip.equip_name,
                    "new_status": EquipmentStatus.IDLE.value
                }

        # Cancel the task
        task.status = TaskStatus.CANCELLED

        # Save data
        data_store.save_tasks(tasks)
        data_store.save_equipment(equipment)

        result = {
            "status": "success",
            "message": f"Task {task_id} has been canceled (original status: {old_status.value})"
        }

        if released_equipment:
            result["released_equipment"] = released_equipment
            result["message"] += f"; device {released_equipment['equip_id']} has been released"

        return result

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to cancel the task: {str(e)}"
        }
