#!/usr/bin/env python3
"""
yard_query_container: Check the location information of the container.

Support querying a single container by container_id, or querying all containers in the box area by block_id.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the container location inquiry.

    Args:
        params:
            - container_id: Container ID, specify to query the location of a single container (optional)
            - block_id: Box area ID, query all containers in the designated box area (optional)

    Returns:
        {"status": "success", "data": {"container": {...}, "location_description": "..."}} Someone
        {"status": "success", "data": {"containers": [...], "block_id": "...", "count": N}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    container_id = params.get("container_id")
    block_id = params.get("block_id")

    try:
        containers = data_store.load_containers()

        if container_id:
            # Query a single container
            for container in containers:
                if container.container_id == container_id:
                    container_data = container.model_dump(mode="json")

                    # Build a location description
                    location_parts = []
                    if container.block_id:
                        location_parts.append(f"Box area {container.block_id}")
                    if container.bay:
                        location_parts.append(f"Shellfish {container.bay}")
                    if container.row:
                        location_parts.append(f"Put in order {container.row}")
                    if container.tier:
                        location_parts.append(f"Tier {container.tier}")

                    location_desc = " ".join(location_parts) if location_parts else "The position has not been assigned"

                    return {
                        "status": "success",
                        "data": {
                            "container": container_data,
                            "location_description": location_desc
                        }
                    }
            # The container was not found.
            return {
                "status": "error",
                "error": f"Container {container_id} does not exist"
            }

        if block_id:
            # Query all containers in the designated container area
            filtered_containers = [
                c for c in containers if c.block_id == block_id
            ]

            if not filtered_containers:
                return {
                    "status": "success",
                    "data": {
                        "containers": [],
                        "message": f"There is no container in the box area {block_id}"
                    }
                }

            # Sort by location
            filtered_containers.sort(key=lambda c: (
                c.bay or 0, c.row or 0, c.tier or 0
            ))

            return {
                "status": "success",
                "data": {
                    "containers": [c.model_dump(mode="json") for c in filtered_containers],
                    "block_id": block_id,
                    "count": len(filtered_containers)
                }
            }

        # Return to all containers
        return {
            "status": "success",
            "data": {
                "containers": [c.model_dump(mode="json") for c in containers],
                "count": len(containers)
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the location of the container: {str(e)}"
        }
