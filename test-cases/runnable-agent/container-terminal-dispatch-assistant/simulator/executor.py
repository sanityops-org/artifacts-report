"""
Execute the simulator module

Provide a simulated execution environment, load all Skill handlers and route execution requests.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from skills.berth_scheduling.handler import run as berth_handler
from skills.yard_scheduling.handler import run as yard_handler
from skills.equipment_scheduling.handler import run as equipment_handler
from skills.gate_scheduling.handler import run as gate_handler


class Simulator:
    """
    Execution simulator

    Load all Skill handlers to provide a unified execution interface.

    Attributes:
        _handlers: Mapping of skill name to handler function
    """

    def __init__(self):
        """Initialize the simulator and load all Skill handler"""
        self._handlers = {
            "berth_scheduling": berth_handler,
            "yard_scheduling": yard_handler,
            "equipment_scheduling": equipment_handler,
            "gate_scheduling": gate_handler,
        }

    def execute(self, command: dict) -> dict:
        """
        Execute the order

        Args:
            command: Command dictionary, including:
                - skill: Skill name (required)
                - action: Operation name (required)
                - params: Parameter dictionary (optional)
                - session_id: Session ID (optional)

        Returns:
            dict: Execution results
                - status: "success" Someone "error"
                - Other fields depend on the operation.
        """
        # Extract parameters
        skill = command.get("skill")
        action = command.get("action")
        params = command.get("params", {})
        # session_id At present, it is only used for logging and does not affect the execution.
        # session_id = command.get("session_id")

        # Verify the required parameters
        if not skill:
            return {
                "status": "error",
                "error": "The required parameters are missing: skill"
            }

        if not action:
            return {
                "status": "error",
                "error": "The required parameters are missing: action"
            }

        # Seek handler
        handler = self._handlers.get(skill)
        if handler is None:
            available_skills = list(self._handlers.keys())
            return {
                "status": "error",
                "error": f"Unknown skills: {skill}, available skills: {available_skills}"
            }

        # Perform the operation
        try:
            result = handler(intent=action, params=params)
            return result
        except Exception as e:
            return {
                "status": "error",
                "error": f"Execution failure: {str(e)}"
            }


__all__ = ["Simulator"]
