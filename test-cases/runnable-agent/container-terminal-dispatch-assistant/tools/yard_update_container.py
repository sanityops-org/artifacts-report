#!/usr/bin/env python3
"""
yard_update_container: Update the location information of the container.

Update the box area, shell space, row and floor information of the container, and update the occupancy of the box area at the same time.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import BlockStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the container location update.

    Args:
        params:
            - container_id: Container ID (required)
            - block_id: New box area ID (required)
            - bay: New Beibit number (required)
            - row: New queue number (required)
            - tier: New floor number (required)

    Returns:
        {"status": "success", "message": "...", "data": {...}} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("yard_update_container", params)
    if permission_error:
        return permission_error

    container_id = params.get("container_id")
    block_id = params.get("block_id")
    bay = params.get("bay")
    row = params.get("row")
    tier = params.get("tier")

    # Parameter verification
    if not container_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: container_id"
        }

    if not block_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: block_id"
        }

    if bay is None:
        return {
            "status": "error",
            "error": "The required parameters are missing: bay"
        }

    if row is None:
        return {
            "status": "error",
            "error": "The required parameters are missing: row"
        }

    if tier is None:
        return {
            "status": "error",
            "error": "The required parameters are missing: tier"
        }

    # Numerical verification
    try:
        bay = int(bay)
        row = int(row)
        tier = int(tier)
    except (ValueError, TypeError):
        return {
            "status": "error",
            "error": "bay, row, tier It must be an integer."
        }

    if bay < 1:
        return {
            "status": "error",
            "error": f"The shell sign must be greater than or equal to 1, and the current value: {bay}"
        }

    if row < 1:
        return {
            "status": "error",
            "error": f"The queue number must be greater than or equal to 1, and the current value: {row}"
        }

    if tier < 1:
        return {
            "status": "error",
            "error": f"The layer number must be greater than or equal to 1, the current value: {tier}"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        containers = data_store.load_containers()
        blocks = data_store.load_yard_blocks()

        # Find the container
        container = None
        for c in containers:
            if c.container_id == container_id:
                container = c
                break

        if not container:
            return {
                "status": "error",
                "error": f"Container {container_id} does not exist"
            }

        # Find the target box area
        target_block = None
        for b in blocks:
            if b.block_id == block_id:
                target_block = b
                break

        if not target_block:
            return {
                "status": "error",
                "error": f"The target box area {block_id} does not exist"
            }

        # Check the status of the target box area
        if target_block.status != BlockStatus.OPERATIONAL:
            status_msg = {
                BlockStatus.FULL: "It is full",
                BlockStatus.CLOSED: "Closed",
                BlockStatus.MAINTENANCE: "Under maintenance"
            }
            return {
                "status": "error",
                "error": f"Target box area {block_id} {status_msg.get(target_block.status, 'not available')}"
            }

        # Check the capacity of the target box area
        if target_block.occupied >= target_block.capacity:
            return {
                "status": "error",
                "error": f"The capacity of the target box area {block_id} is full ({target_block.occupied}/{target_block.capacity})"
            }

        # Check layer height limit
        if tier > target_block.tiers_max:
            return {
                "status": "error",
                "error": f"The floor number {tier} exceeds the maximum number of layers in the target box area. (1-{target_block.tiers_max})"
            }

        # Record the original location
        old_block_id = container.block_id
        old_bay = container.bay
        old_row = container.row
        old_tier = container.tier

        # Update the container location
        container.block_id = block_id
        container.bay = bay
        container.row = row
        container.tier = tier

        # Update the occupancy of the box area
        # If the container moves from other boxes
        if old_block_id and old_block_id != block_id:
            # Reduce the occupancy of the original box area
            for b in blocks:
                if b.block_id == old_block_id:
                    b.occupied = max(0, b.occupied - 1)
                    break

            # Increase the occupancy of the new box area
            target_block.occupied += 1
        elif not old_block_id:
            # There is no space in the container before, and the new container area will be occupied.
            target_block.occupied += 1

        # Save data
        data_store.save_containers(containers)
        data_store.save_yard_blocks(blocks)

        old_location = f"Box area {old_block_id}, shell {old_bay}, row {old_row}, layer {old_tier}" if old_block_id else "no location"
        new_location = f"Box area {block_id}, shell {bay}, row {row}, layer {tier}"

        return {
            "status": "success",
            "message": f"Container {container_id} location has been updated",
            "data": {
                "container_id": container_id,
                "old_location": old_location if old_block_id else None,
                "new_location": new_location,
                "from": {
                    "block_id": old_block_id,
                    "bay": old_bay,
                    "row": old_row,
                    "tier": old_tier
                } if old_block_id else None,
                "to": {
                    "block_id": block_id,
                    "bay": bay,
                    "row": row,
                    "tier": tier
                }
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to update the container location: {str(e)}"
        }
