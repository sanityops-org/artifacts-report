# TOSAnalog interface
"""Simulate the login and permission management functions of the terminal operating system (TOS)"""

import uuid
from typing import Optional

# Role permission configuration
ROLE_PERMISSIONS = {
    "Parking dispatcher": {
        "permissions": ["berth_scheduling"],
        "can_issue_commands": True
    },
    "Stacking dispatcher": {
        "permissions": ["yard_scheduling"],
        "can_issue_commands": True
    },
    "Equipment dispatcher": {
        "permissions": ["equipment_scheduling"],
        "can_issue_commands": True
    },
    "Gate dispatcher": {
        "permissions": ["gate_scheduling"],
        "can_issue_commands": True
    },
    "Operation supervisor": {
        "permissions": [
            "berth_scheduling",
            "yard_scheduling",
            "equipment_scheduling",
            "gate_scheduling"
        ],
        "can_issue_commands": True
    },
    "Dock manager": {
        "permissions": [
            "berth_scheduling",
            "yard_scheduling",
            "equipment_scheduling",
            "gate_scheduling"
        ],
        "can_issue_commands": False
    }
}

# Module-level session storage
_active_sessions: dict = {}


def login(role: str) -> dict:
    """
    Simulate login to TOS system

    Args:
        role: Character name

    Returns:
        dict: Login results
            - success: {"status": "success", "data": {"session_id", "role", "permissions", "can_issue_commands"}}
            - error: {"status": "error", "error": "Error message"}
    """
    if role not in ROLE_PERMISSIONS:
        return {
            "status": "error",
            "error": f"Unknown role: {role}"
        }

    # Generate a sessionID
    session_id = str(uuid.uuid4())

    # Create a session
    role_config = ROLE_PERMISSIONS[role]
    session_data = {
        "session_id": session_id,
        "role": role,
        "permissions": role_config["permissions"].copy(),
        "can_issue_commands": role_config["can_issue_commands"]
    }

    # Storage session
    _active_sessions[session_id] = session_data

    return {
        "status": "success",
        "data": session_data
    }


def check_permission(session_id: str, skill_name: str) -> bool:
    """
    Verify domain permissions

    Args:
        session_id: ConverseID
        skill_name: Skill name (field name)

    Returns:
        bool: Do you have the authority?
    """
    session = _active_sessions.get(session_id)
    if session is None:
        return False

    return skill_name in session["permissions"]


def can_issue_commands(session_id: str) -> bool:
    """
    Check the command permission

    Args:
        session_id: ConverseID

    Returns:
        bool: Can instructions be issued?
    """
    session = _active_sessions.get(session_id)
    if session is None:
        return False

    return session["can_issue_commands"]


def get_session(session_id: str) -> Optional[dict]:
    """
    Get the conversation information

    Args:
        session_id: ConverseID

    Returns:
        dict | None: Session data, there is no returnNone
    """
    return _active_sessions.get(session_id)


def logout(session_id: str) -> dict:
    """
    Log out of the TOS system

    Args:
        session_id: ConverseID

    Returns:
        dict: The result of cancellation
    """
    if session_id not in _active_sessions:
        return {
            "status": "error",
            "error": f"The session does not exist.: {session_id}"
        }

    del _active_sessions[session_id]

    return {
        "status": "success",
        "data": {"message": "Successful cancellation"}
    }
