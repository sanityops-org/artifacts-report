#!/usr/bin/env python3
"""
equipment_update_status: Update the status of the device.

Support updating the device status and current location (for card collection only).
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import EquipmentStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the device status update.

    Args:
        params:
            - equip_id: Device ID (required)
            - status: New status (required)
            - current_location: Current location (optional, dedicated to collecting cards)

    Returns:
        {"status": "success", "message": "..."} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("equipment_update_status", params)
    if permission_error:
        return permission_error

    equip_id = params.get("equip_id")
    new_status = params.get("status")
    current_location = params.get("current_location")

    # Parameter verification
    if not equip_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: equip_id"
        }

    if not new_status:
        return {
            "status": "error",
            "error": "The required parameters are missing: status"
        }

    # Verify the status value
    try:
        status_enum = EquipmentStatus(new_status) if isinstance(new_status, str) else new_status
    except ValueError:
        return {
            "status": "error",
            "error": f"Invalid device status: {new_status}, valid value: {[s.value for s in EquipmentStatus]}"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        equipment = data_store.load_equipment()

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

        old_status = equip.status

        # Perform status update
        equip.status = status_enum

        # Update the current location (for collecting cards only)
        if current_location is not None:
            equip.current_location = current_location

        # If the status becomes idle or fault/maintenance/offline, clear the current task.
        if status_enum in [EquipmentStatus.IDLE, EquipmentStatus.FAULT,
                          EquipmentStatus.MAINTENANCE, EquipmentStatus.OFFLINE]:
            equip.current_task = None

        # Save data
        data_store.save_equipment(equipment)

        return {
            "status": "success",
            "message": f"The status of the device {equip_id} ({equip.equip_name}) has been updated from {old_status.value} to {status_enum.value}"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to update the device status: {str(e)}"
        }
