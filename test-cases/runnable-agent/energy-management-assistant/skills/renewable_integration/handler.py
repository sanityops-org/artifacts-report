"""
Renewable energy integration skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.energy_suggest_renewables import execute as suggest_renewables


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "assess_potential": suggest_renewables,
    "suggest_renewables": suggest_renewables,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of renewable energy integration skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - assess_potential: Assess the potential of renewable energy
            - suggest_renewables: Suggest renewable energy options
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
            "error": f"Unknown operation: {intent}. Available operations: {available_intents}"
        }

    # Execution tools
    return tool_func(params)
