#!/usr/bin/env python3
"""
equipment_dispatch: Assign the task to the device.

Perform equipment status verification, and the equipment must be idle to accept dispatch.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import EquipmentStatus, EquipmentType, TaskStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out equipment dispatch.

    Args:
        params:
            - equip_id: Device ID (required)
            - task_id: Task ID (required)

    Returns:
        {"status": "success", "message": "..."} Someone
        {"status": "error", "error": "...", "alternatives": [...]}
    """

    # Permission verification
    permission_error = check_tool_permission("equipment_dispatch", params)
    if permission_error:
        return permission_error

    equip_id = params.get("equip_id")
    task_id = params.get("task_id")

    # Parameter verification
    if not equip_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: equip_id"
        }

    if not task_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: task_id"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        equipment = data_store.load_equipment()
        tasks = data_store.load_tasks()

        # Find the device
        equip = None
        for e in equipment:
            if e.equip_id == equip_id:
                equip = e
                break

        if not equip:
            return {
                "status": "error",
                "error": f"Device {equip_id} does not exist"
            }

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
                "error": f"Task {task_id} has been completed and cannot be reassigned."
            }

        if task.status == TaskStatus.CANCELLED:
            return {
                "status": "error",
                "error": f"Task {task_id} has been canceled and cannot be assigned."
            }

        # Check whether the task has been assigned to other devices
        if task.equip_id and task.equip_id != equip_id:
            return {
                "status": "error",
                "error": f"Task {task_id} has been assigned to the device {task.equip_id}"
            }

        # The status of the verification device must be idle
        if equip.status != EquipmentStatus.IDLE:
            # Find alternative devices
            alternatives = _find_alternative_equipment(equip, equipment, task)

            status_msg = {
                EquipmentStatus.WORKING: "working",
                EquipmentStatus.MOVING: "It is moving",
                EquipmentStatus.FAULT: "In fault",
                EquipmentStatus.MAINTENANCE: "In maintenance",
                EquipmentStatus.OFFLINE: "Offline"
            }

            return {
                "status": "error",
                "error": f"Device {equip_id} {status_msg.get(equip.status, 'unavailable')}, unable to dispatch equipment",
                "alternatives": alternatives
            }

        # Check whether the equipment has other tasks
        if equip.current_task:
            return {
                "status": "error",
                "error": f"Device {equip_id} already has a task {equip.current_task}, please complete the task or cancel the task first.",
                "alternatives": _find_alternative_equipment(equip, equipment, task)
            }

        # Execution of dispatch
        # Update the device status
        equip.status = EquipmentStatus.WORKING
        equip.current_task = task_id

        # Update the task status
        task.equip_id = equip_id
        task.status = TaskStatus.ASSIGNED

        # Save data
        data_store.save_equipment(equipment)
        data_store.save_tasks(tasks)

        return {
            "status": "success",
            "message": f"Task {task_id} has been successfully assigned to the device {equip_id} ({equip.equip_name})"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Dispatch failed: {str(e)}"
        }


def _find_alternative_equipment(current_equip, equipment: list, task) -> list:
    """
    Find an eligible alternative device.

    Args:
        current_equip: Current device object
        equipment: List of equipment
        task: Task object

    Returns:
        list: List of eligible alternative devices
    """
    alternatives = []

    for equip in equipment:
        # Exclude the current device
        if equip.equip_id == current_equip.equip_id:
            continue

        # Must be free
        if equip.status != EquipmentStatus.IDLE:
            continue

        # There must be no ongoing tasks.
        if equip.current_task:
            continue

        # The device type should match the task type.
        # The loading/unloading task requires a shore bridge.
        if task.task_type.value in ["load", "discharge"]:
            if equip.equip_type != EquipmentType.QUAY_CRANE:
                continue
        # Field bridge is required to move boxes in the field.
        elif task.task_type.value == "yard_move":
            if equip.equip_type not in [EquipmentType.RTG, EquipmentType.RMG]:
                continue
        # Front suspension or top suspension is required for entering and exiting the gate.
        elif task.task_type.value in ["gate_in", "gate_out"]:
            if equip.equip_type not in [EquipmentType.REACH_STACKER, EquipmentType.TOP_LOADER]:
                continue

        alternatives.append({
            "equip_id": equip.equip_id,
            "equip_name": equip.equip_name,
            "equip_type": equip.equip_type.value,
            "status": equip.status.value,
            "efficiency_rate": equip.efficiency_rate
        })

    return alternatives
