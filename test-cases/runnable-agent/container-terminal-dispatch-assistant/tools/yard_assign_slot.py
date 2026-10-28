#!/usr/bin/env python3
"""
yard_assign_slot: Assign the drop-in location of the container.

Perform capacity, status and type checks, and return to the alternative box recommendation in case of failure.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import BlockStatus, ContainerType
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the location allocation of the box.

    Args:
        params:
            - container_id: Container ID (required)
            - block_id: Target box area ID (required)
            - bay: Shell number, automatic allocation if not specified (optional)
            - row: Number, automatically assigned if not specified (optional)
            - tier: Floor number, automatically assigned if not specified (optional)

    Returns:
        {"status": "success", "message": "...", "data": {...}} Someone
        {"status": "error", "error": "...", "alternatives": [...]}
    """

    # Permission verification
    permission_error = check_tool_permission("yard_assign_slot", params)
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

        # Find the box area
        block = None
        for b in blocks:
            if b.block_id == block_id:
                block = b
                break

        if not block:
            return {
                "status": "error",
                "error": f"Box area {block_id} does not exist"
            }

        # Check the status of the box area
        if block.status != BlockStatus.OPERATIONAL:
            alternatives = _find_alternative_blocks(container, blocks, block_id)

            status_msg = {
                BlockStatus.FULL: "It is full",
                BlockStatus.CLOSED: "Closed",
                BlockStatus.MAINTENANCE: "Under maintenance"
            }

            return {
                "status": "error",
                "error": f"Box area {block_id} {status_msg.get(block.status, 'not available')}",
                "alternatives": alternatives
            }

        # Check the capacity of the box area
        if block.occupied >= block.capacity:
            alternatives = _find_alternative_blocks(container, blocks, block_id)

            return {
                "status": "error",
                "error": f"Box area {block_id} capacity is full ({block.occupied}/{block.capacity})",
                "alternatives": alternatives
            }

        # Check the match between the container type and the box area type
        if container.type != block.type:
            # For dangerous goods boxes and refrigerators, the types must be exactly the match.
            if container.type in [ContainerType.DANGEROUS, ContainerType.REEFER]:
                alternatives = _find_alternative_blocks(container, blocks, block_id)

                return {
                    "status": "error",
                    "error": f"The container type {container.type.value} does not match the box type {block.type.value}",
                    "alternatives": alternatives
                }

            # Other types can have some flexibility, but give a warning.
            # The import box can be placed in the export box area, and vice versa.
            pass

        # Check layer height limit
        if tier is not None:
            if tier < 1 or tier > block.tiers_max:
                return {
                    "status": "error",
                    "error": f"The floor number {tier} exceeds the maximum floor limit of the box area (1-{block.tiers_max})"
                }

        # Automatically assign location parameters
        if bay is None:
            bay = _find_available_bay(block, containers)
        if row is None:
            row = _find_available_row(block, containers, bay)
        if tier is None:
            tier = _find_available_tier(block, containers, bay, row)

        # Update the container location
        container.block_id = block_id
        container.bay = bay
        container.row = row
        container.tier = tier

        # Update the occupancy of the box area
        # If the container is not in any box area before, increase the occupancy.
        old_block_id = None
        for c in containers:
            if c.container_id == container_id and c.block_id:
                old_block_id = c.block_id
                break

        # Increase the occupancy of the new box area
        block.occupied += 1

        # If you move from other box areas, reduce the occupancy of the original box area.
        if old_block_id and old_block_id != block_id:
            for b in blocks:
                if b.block_id == old_block_id:
                    b.occupied = max(0, b.occupied - 1)
                    break

        # Save data
        data_store.save_containers(containers)
        data_store.save_yard_blocks(blocks)

        location_desc = f"Box area {block_id}, shell {bay}, row {row}, layer {tier}"

        return {
            "status": "success",
            "message": f"The container {container_id} has been successfully assigned to {location_desc}",
            "data": {
                "container_id": container_id,
                "block_id": block_id,
                "bay": bay,
                "row": row,
                "tier": tier,
                "location_description": location_desc
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to assign the location of the box: {str(e)}"
        }


def _find_alternative_blocks(container, blocks: list, excluded_block_id: str = None) -> list:
    """
    Find eligible alternative box areas.

    Args:
        container: Container object
        blocks: List of box areas
        excluded_block_id: Excluded box areaID

    Returns:
        list: List of eligible alternative boxes
    """
    alternatives = []

    for block in blocks:
        # Exclude the designated box area
        if block.block_id == excluded_block_id:
            continue

        # Must be able to do homework
        if block.status != BlockStatus.OPERATIONAL:
            continue

        # There must be an empty seat.
        if block.occupied >= block.capacity:
            continue

        # Type matching
        if container.type != block.type:
            # Dangerous goods and refrigerators must be accurately matched.
            if container.type in [ContainerType.DANGEROUS, ContainerType.REEFER]:
                continue

        alternatives.append({
            "block_id": block.block_id,
            "block_name": block.block_name,
            "type": block.type.value,
            "available_slots": block.capacity - block.occupied,
            "capacity": block.capacity,
            "tiers_max": block.tiers_max
        })

    # Sort by available capacity
    alternatives.sort(key=lambda x: x["available_slots"], reverse=True)

    return alternatives[:5]  # Return to the first 5


def _find_available_bay(block, containers: list) -> int:
    """Find available shells"""
    # Simple implementation: return1
    # The actual realization should consider the layout of the warehouse and the existing containers.
    return 1


def _find_available_row(block, containers: list, bay: int) -> int:
    """Find the available row"""
    # Simple implementation: return1
    return 1


def _find_available_tier(block, containers: list, bay: int, row: int) -> int:
    """Find the available layers"""
    # Simple implementation: return1
    return 1
