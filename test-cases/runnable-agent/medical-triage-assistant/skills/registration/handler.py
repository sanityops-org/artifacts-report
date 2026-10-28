"""
Registration appointment skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.appointment_cancel import execute as cancel_appointment
from tools.appointment_create import execute as create_appointment
from tools.appointment_query import execute as query_appointment
from tools.appointment_query_slots import execute as query_slots
from tools.patient_get_profile import execute as get_profile
from tools.patient_update_profile import execute as update_profile


# Tool mapping dictionary
_TOOLS = {
    # Patient information
    "update_profile": update_profile,
    "get_profile": get_profile,
    # Number source and registration
    "query_slots": query_slots,
    "create_appointment": create_appointment,
    "query_appointment": query_appointment,
    "cancel_appointment": cancel_appointment,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of registration and appointment skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - update_profile: Record or update patient information
            - get_profile: Read the patient's information
            - query_slots: Query number source and residual number
            - create_appointment: Register
            - query_appointment: Check the registration record
            - cancel_appointment: Cancel the registration
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
            "error": f"Unknown operation: {intent}, available operation: {available_intents}",
        }

    # Execution tools
    return tool_func(params)
