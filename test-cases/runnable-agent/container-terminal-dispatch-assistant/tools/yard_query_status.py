#!/usr/bin/env python3
"""
yard_query_status: Check the status and capacity information of the storage box area.

Support querying a single box area by block_id, or filtering the list of box areas by container type.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import ContainerType


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the status query of the warehouse box area.

    Args:
        params:
            - block_id: Box area ID, specify to query a single box area (optional)
            - type: Container type filtration (import, export, transshipment, empty, dangerous, reefer) (optional)

    Returns:
        {"status": "success", "data": {"blocks": [...], "summary": {...}}} Someone
        {"status": "success", "data": {"block": {...}, "available_slots": N, "utilization_rate": X}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    block_id = params.get("block_id")
    type_filter = params.get("type")

    try:
        blocks = data_store.load_yard_blocks()

        if block_id:
            # Query a single box area
            for block in blocks:
                if block.block_id == block_id:
                    # Calculate the available capacity
                    available = block.capacity - block.occupied
                    utilization_rate = (block.occupied / block.capacity) * 100 if block.capacity > 0 else 0

                    return {
                        "status": "success",
                        "data": {
                            "block": block.model_dump(mode="json"),
                            "available_slots": available,
                            "utilization_rate": round(utilization_rate, 2)
                        }
                    }
            # The box area was not found.
            return {
                "status": "error",
                "error": f"Box area {block_id} does not exist"
            }

        # Filter by type
        if type_filter:
            try:
                # Verify whether the type is valid
                type_enum = ContainerType(type_filter)
                filtered_blocks = [
                    b for b in blocks if b.type == type_enum
                ]
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid container type: {type_filter}, the valid value is: {[t.value for t in ContainerType]}"
                }
        else:
            filtered_blocks = blocks

        # Build return data and add statistical information
        blocks_data = []
        for block in filtered_blocks:
            available = block.capacity - block.occupied
            utilization_rate = (block.occupied / block.capacity) * 100 if block.capacity > 0 else 0

            block_info = block.model_dump(mode="json")
            block_info["available_slots"] = available
            block_info["utilization_rate"] = round(utilization_rate, 2)
            blocks_data.append(block_info)

        # Calculate summary statistics
        total_capacity = sum(b.capacity for b in filtered_blocks)
        total_occupied = sum(b.occupied for b in filtered_blocks)
        total_available = total_capacity - total_occupied
        overall_utilization = (total_occupied / total_capacity) * 100 if total_capacity > 0 else 0

        return {
            "status": "success",
            "data": {
                "blocks": blocks_data,
                "summary": {
                    "total_blocks": len(filtered_blocks),
                    "total_capacity": total_capacity,
                    "total_occupied": total_occupied,
                    "total_available": total_available,
                    "overall_utilization": round(overall_utilization, 2)
                }
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the status of the warehouse: {str(e)}"
        }
