"""
Energy analysis skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.energy_analyze_consumption import execute as analyze_consumption
from tools.energy_identify_efficiency_opportunities import execute as identify_opportunities
from tools.energy_calculate_carbon_footprint import execute as calculate_carbon


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "analyze_consumption": analyze_consumption,
    "identify_opportunities": identify_opportunities,
    "calculate_carbon": calculate_carbon,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of energy analysis skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - analyze_consumption: Analyze the energy consumption pattern
            - identify_opportunities: Identify opportunities for efficiency improvement
            - calculate_carbon: Calculate the carbon footprint
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
