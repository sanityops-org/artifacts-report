"""
Gate dispatching skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.gate_query_status import execute as query_gate_status
from tools.gate_query_appointment import execute as query_gate_appointment
from tools.gate_query_queue import execute as query_gate_queue
from tools.gate_open_channel import execute as open_gate_channel
from tools.gate_close_channel import execute as close_gate_channel
from tools.gate_process_pass import execute as process_gate_pass


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "query_gate_status": query_gate_status,
    "query_gate_appointment": query_gate_appointment,
    "query_gate_queue": query_gate_queue,
    # Command tools
    "open_gate_channel": open_gate_channel,
    "close_gate_channel": close_gate_channel,
    "process_gate_pass": process_gate_pass,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of gate dispatching skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - query_gate_status: Check the status of the gate channel
            - query_gate_appointment: Check the appointment record
            - query_gate_queue: Check the queue
            - open_gate_channel: Open the gate passage
            - close_gate_channel: Close the gate passage
            - process_gate_pass: Handle the collection card to enter and exit the port
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
