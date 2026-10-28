"""
Guidance and triage skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.triage_check_red_flags import execute as check_red_flags
from tools.triage_query_department import execute as query_department
from tools.triage_shortlist_departments import execute as shortlist_departments


# Tool mapping dictionary
_TOOLS = {
    # Regular gate
    "check_red_flags": check_red_flags,
    # Query tools
    "shortlist_departments": shortlist_departments,
    "query_department": query_department,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of guidance and triage skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - check_red_flags: Red flag symptom screening (compulsory gate)
            - shortlist_departments: Convergence candidate department
            - query_department: Check the department information
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
