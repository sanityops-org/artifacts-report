#!/usr/bin/env python3
"""
yard_create_rehandle: Create a new box-turning task.

The box-turning task is used to move the container from one position to another.
"""

import sys
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.equipment import Task
from models.enums import TaskType, TaskStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the box-turning task to create.

    Args:
        params:
            - container_id: Container ID that needs to be turned over (required)
            - from_block_id: Original box area ID (required)
            - to_block_id: Target box area ID, if not specified, the appropriate box area will be automatically selected (optional)
            - reason: The reason for turning over the box (optional)

    Returns:
        {"status": "success", "message": "...", "data": {...}} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("yard_create_rehandle", params)
    if permission_error:
        return permission_error

    container_id = params.get("container_id")
    from_block_id = params.get("from_block_id")
    to_block_id = params.get("to_block_id")
    reason = params.get("reason", "Dispatching needs")

    # Parameter verification
    if not container_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: container_id"
        }

    if not from_block_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: from_block_id"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        containers = data_store.load_containers()
        blocks = data_store.load_yard_blocks()
        tasks = data_store.load_tasks()

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

        # Check the current location of the container
        if container.block_id != from_block_id:
            return {
                "status": "error",
                "error": f"The container {container_id} is not in the box area at present. {from_block_id}"
            }

        # Find the original box area
        from_block = None
        for b in blocks:
            if b.block_id == from_block_id:
                from_block = b
                break

        if not from_block:
            return {
                "status": "error",
                "error": f"The original box area {from_block_id} does not exist"
            }

        # Automatically select the target box area
        if not to_block_id:
            # Looking for similar box areas
            for block in blocks:
                if (block.block_id != from_block_id and
                    block.type == container.type and
                    block.status.value == "operational" and
                    block.occupied < block.capacity):
                    to_block_id = block.block_id
                    break

            if not to_block_id:
                return {
                    "status": "error",
                    "error": "No suitable target box area was found. Please specify the target box area manually."
                }

        # Find the target box area
        to_block = None
        for b in blocks:
            if b.block_id == to_block_id:
                to_block = b
                break

        if not to_block:
            return {
                "status": "error",
                "error": f"The target box area {to_block_id} does not exist"
            }

        # Check the capacity of the target box area
        if to_block.occupied >= to_block.capacity:
            return {
                "status": "error",
                "error": f"The capacity of the target box area {to_block_id} is full"
            }

        # Check whether there is a pending overturning task of the same container
        for t in tasks:
            if (t.container_id == container_id and
                t.task_type == TaskType.YARD_MOVE and
                t.status in [TaskStatus.PENDING, TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]):
                return {
                    "status": "error",
                    "error": f"Container {container_id} already has a pending box turning task (taskID: {t.task_id})",
                    "existing_task": t.model_dump(mode="json")
                }

        # Create a task ID (format: T followed by a 4-digit number)
        # Find the largest number in the existing task
        max_num = 0
        for t in tasks:
            if t.task_id.startswith("T"):
                try:
                    num = int(t.task_id[1:])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        new_num = max_num + 1
        task_id = f"T{new_num:04d}"

        # Build a position string
        source_location = f"{from_block_id}-{container.bay or 0}-{container.row or 0}-{container.tier or 0}"
        target_location = f"{to_block_id}"

        now = datetime.now().isoformat()

        new_task = Task(
            task_id=task_id,
            task_type=TaskType.YARD_MOVE,
            container_id=container_id,
            source_location=source_location,
            target_location=target_location,
            status=TaskStatus.PENDING,
            created_at=now,
            estimated_duration=15  # It is estimated that it will take 15 minutes to turn over the box.
        )

        tasks.append(new_task)
        data_store.save_tasks(tasks)

        return {
            "status": "success",
            "message": f"The box-turning task {task_id} was created successfully",
            "data": {
                "task": new_task.model_dump(mode="json"),
                "container_id": container_id,
                "from_block_id": from_block_id,
                "to_block_id": to_block_id,
                "reason": reason
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to create a box-turning task: {str(e)}"
        }
