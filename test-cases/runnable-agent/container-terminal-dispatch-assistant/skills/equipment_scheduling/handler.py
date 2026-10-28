"""
Equipment scheduling skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.equipment_query_status import execute as query_equipment_status
from tools.equipment_query_task import execute as query_equipment_task
from tools.equipment_dispatch import execute as dispatch_equipment
from tools.equipment_update_status import execute as update_equipment_status
from tools.equipment_cancel_task import execute as cancel_task


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "query_equipment_status": query_equipment_status,
    "query_equipment_task": query_equipment_task,
    # Command tools
    "dispatch_equipment": dispatch_equipment,
    "update_equipment_status": update_equipment_status,
    "cancel_task": cancel_task,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of equipment scheduling skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - query_equipment_status: Check the status of the device
            - query_equipment_task: Query device tasks
            - dispatch_equipment: Dispatch
            - update_equipment_status: Update the device status
            - cancel_task: Cancel the task
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
