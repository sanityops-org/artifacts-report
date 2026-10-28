"""
Parking scheduling skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.berth_query_vessel_plan import execute as query_vessel_plan
from tools.berth_query_berth_status import execute as query_berth_status
from tools.berth_query_anchorage import execute as query_anchorage
from tools.berth_assign_berth import execute as assign_berth
from tools.berth_update_plan import execute as update_berth_plan
from tools.berth_confirm_departure import execute as confirm_departure


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "query_vessel_plan": query_vessel_plan,
    "query_berth_status": query_berth_status,
    "query_anchorage": query_anchorage,
    # Command tools
    "assign_berth": assign_berth,
    "update_berth_plan": update_berth_plan,
    "confirm_departure": confirm_departure,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of berth scheduling skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - query_vessel_plan: Inquire about the ship plan
            - query_berth_status: Check the berth status
            - query_anchorage: Query anchorage ships
            - assign_berth: Allocate berths
            - update_berth_plan: Update the mooring plan
            - confirm_departure: Confirm the departure
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
