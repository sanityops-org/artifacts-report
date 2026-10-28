#!/usr/bin/env python3
"""
equipment_query_status: Check the status of the device.

Support filtering by device ID, device type and status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import EquipmentType, EquipmentStatus


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform device status query.

    Args:
        params:
            - equip_id: Device ID, exact matching (optional)
            - equip_type: Device type filtering (optional)
            - status: Device status filtering (optional)

    Returns:
        {"status": "success", "count": N, "equipment": [...]} Someone
        {"status": "error", "error": "..."}
    """
    equip_id = params.get("equip_id")
    equip_type = params.get("equip_type")
    status = params.get("status")

    data_store = DataStore(data_dir=project_root / "data")

    try:
        equipment = data_store.load_equipment()

        # Accurate filtering by device ID
        if equip_id:
            equipment = [e for e in equipment if e.equip_id == equip_id]

        # Filter by device type
        if equip_type:
            try:
                # Support strings or enumeration values
                type_enum = EquipmentType(equip_type) if isinstance(equip_type, str) else equip_type
                equipment = [e for e in equipment if e.equip_type == type_enum]
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid device type: {equip_type}, valid value: {[t.value for t in EquipmentType]}"
                }

        # Filter by status
        if status:
            try:
                status_enum = EquipmentStatus(status) if isinstance(status, str) else status
                equipment = [e for e in equipment if e.status == status_enum]
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid device status: {status}, valid value: {[s.value for s in EquipmentStatus]}"
                }

        # Construction return results
        equipment_list = []
        for e in equipment:
            item = {
                "equip_id": e.equip_id,
                "equip_type": e.equip_type.value,
                "equip_name": e.equip_name,
                "status": e.status.value,
                "efficiency_rate": e.efficiency_rate,
            }
            # Add optional fields
            if e.current_task:
                item["current_task"] = e.current_task
            if e.berth_id:
                item["berth_id"] = e.berth_id
            if e.block_id:
                item["block_id"] = e.block_id
            if e.current_location:
                item["current_location"] = e.current_location
            equipment_list.append(item)

        return {
            "status": "success",
            "count": len(equipment_list),
            "equipment": equipment_list
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the device status: {str(e)}"
        }
