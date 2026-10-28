"""
Efficiency optimization skills Handler

Provide a unified skill entrance and route it to the corresponding tool function.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.energy_recommend_optimizations import execute as recommend_optimizations
from tools.energy_estimate_savings import execute as estimate_savings


# Tool mapping dictionary
_TOOLS = {
    # Query tools
    "recommend_optimizations": recommend_optimizations,
    "estimate_savings": estimate_savings,
}


def run(intent: str, params: dict) -> dict:
    """
    Unified entrance of efficiency optimization skills

    Route to the corresponding tool function according to the intention to execute.

    Args:
        intent: Operation intention
            - recommend_optimizations: Generate efficiency optimization suggestions
            - estimate_savings: Estimate the energy-saving effect
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
