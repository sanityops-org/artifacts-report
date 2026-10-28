#!/usr/bin/env python3
"""
Permission verification auxiliary module

Provide tool-level permission check functions for each tool to call.
"""

from typing import Any, Dict

from apis.tos_api import check_permission, can_issue_commands


# Mapping of instruction tools and skill fields
COMMAND_SKILL_MAP = {
    # Parking scheduling
    "berth_assign_berth": "berth_scheduling",
    "berth_update_plan": "berth_scheduling",
    "berth_confirm_departure": "berth_scheduling",
    # Field dispatch
    "yard_assign_slot": "yard_scheduling",
    "yard_create_rehandle": "yard_scheduling",
    "yard_update_container": "yard_scheduling",
    # Equipment scheduling
    "equipment_dispatch": "equipment_scheduling",
    "equipment_update_status": "equipment_scheduling",
    "equipment_cancel_task": "equipment_scheduling",
    # Gate dispatch
    "gate_open_channel": "gate_scheduling",
    "gate_close_channel": "gate_scheduling",
    "gate_process_pass": "gate_scheduling",
}


def check_tool_permission(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Check the permission of the tool call.

    Args:
        tool_name: Name of the tool
        params: Tool parameters (need to include _session）

    Returns:
        None: Permission passed
        dict: Permission verification failed and returned an error response.
    """
    session = params.get("_session")

    if not session:
        return {
            "status": "error",
            "error": "Not logged in, please log in to the system first."
        }

    session_id = session.get("session_id")

    # Judge whether it is an instruction tool
    if tool_name in COMMAND_SKILL_MAP:
        skill_name = COMMAND_SKILL_MAP[tool_name]

        # 1. Check the domain permissions
        if not check_permission(session_id, skill_name):
            return {
                "status": "error",
                "error": f"Unauthorized operation {skill_name} domain, current role: {session.get('role')}"
            }

        # 2. Check the instruction permission
        if not can_issue_commands(session_id):
            return {
                "status": "error",
                "error": f"The current role ({session.get('role')}) has no instruction issuance authority, and can only be queried"
            }

    return None  # Permission passed
