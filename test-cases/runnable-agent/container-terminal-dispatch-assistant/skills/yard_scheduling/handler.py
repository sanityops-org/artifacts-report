"""
Stacking field scheduling skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.yard_query_status import execute as query_yard_status
from tools.yard_query_container import execute as query_container_location
from tools.yard_query_rehandle import execute as query_rehandle_list
from tools.yard_assign_slot import execute as assign_yard_slot
from tools.yard_create_rehandle import execute as create_rehandle_task
from tools.yard_update_container import execute as update_container_location


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "query_yard_status": query_yard_status,
    "query_container_location": query_container_location,
    "query_rehandle_list": query_rehandle_list,
    # Command tools
    "assign_yard_slot": assign_yard_slot,
    "create_rehandle_task": create_rehandle_task,
    "update_container_location": update_container_location,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of warehouse scheduling skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - query_yard_status: Query the status of the storage box area
            - query_container_location: Check the location of the container
            - query_rehandle_list: Query the list of box-turning tasks
            - assign_yard_slot: Assign the location of the box
            - create_rehandle_task: Create a box-turning task
            - update_container_location: Update the container location
        params: Tool parameter dictionary

    Returns:
        dict: Tool execution results
            - status: "success" Someone "error"
            - Other fields depend on the tool.
    """
    # Find the corresponding tools
    tool_func = _TOOLS.get(intent)

    if tool_func is None:
        # Return an unknown operation error
        available_intents = list(_TOOLS.keys())
        return {
            "status": "error",
            "error": f"Unknown operation: {intent}, available operation: {available_intents}"
        }

    # Execution tools
    return tool_func(params)
