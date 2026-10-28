# Energy Management API
"""Energy management session and permission management"""

import uuid
from typing import Optional

# User roles configuration
ROLE_PERMISSIONS = {
    "Facility Manager": {
        "permissions": ["energy_analysis", "efficiency_optimization", "renewable_integration"],
        "can_issue_commands": True,
        "description": "Full access to all energy management functions"
    },
    "Energy Analyst": {
        "permissions": ["energy_analysis", "efficiency_optimization"],
        "can_issue_commands": False,
        "description": "Read-only analysis and recommendations"
    },
    "Sustainability Officer": {
        "permissions": ["energy_analysis", "renewable_integration"],
        "can_issue_commands": False,
        "description": "Focus on carbon footprint and renewable energy"
    },
    "Operations Staff": {
        "permissions": ["energy_analysis"],
        "can_issue_commands": False,
        "description": "Basic energy consumption monitoring"
    },
    "Executive": {
        "permissions": ["energy_analysis", "efficiency_optimization", "renewable_integration"],
        "can_issue_commands": False,
        "description": "Strategic overview and planning"
    },
    "Engineer": {
        "permissions": ["energy_analysis", "efficiency_optimization"],
        "can_issue_commands": True,
        "description": "Technical implementation and optimization"
    }
}

# Module-level session storage
_active_sessions: dict = {}


def login(role: str) -> dict:
    """
    Simulate login to energy management system

    Args:
        role: Role name

    Returns:
        dict: Login result
            - success: {"status": "success", "data": {"session_id", "role", "permissions", "can_issue_commands"}}
            - error: {"status": "error", "error": "error message"}
    """
    if role not in ROLE_PERMISSIONS:
        return {
            "status": "error",
            "error": f"Unknown role: {role}"
        }

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Create session
    role_config = ROLE_PERMISSIONS[role]
    session_data = {
        "session_id": session_id,
        "role": role,
        "permissions": role_config["permissions"].copy(),
        "can_issue_commands": role_config["can_issue_commands"]
    }

    # Store session
    _active_sessions[session_id] = session_data

    return {
        "status": "success",
        "data": session_data
    }


def check_permission(session_id: str, skill_name: str) -> bool:
    """
    Check if session has permission for a skill

    Args:
        session_id: Session ID
        skill_name: Skill name

    Returns:
        bool: Whether has permission
    """
    session = _active_sessions.get(session_id)
    if session is None:
        return False

    return skill_name in session["permissions"]


def can_issue_commands(session_id: str) -> bool:
    """
    Check if session can issue commands

    Args:
        session_id: Session ID

    Returns:
        bool: Whether can issue commands
    """
    session = _active_sessions.get(session_id)
    if session is None:
        return False

    return session["can_issue_commands"]


def get_session(session_id: str) -> Optional[dict]:
    """
    Get session information

    Args:
        session_id: Session ID

    Returns:
        dict | None: Session data, None if not found
    """
    return _active_sessions.get(session_id)


def logout(session_id: str) -> dict:
    """
    Logout from energy management system

    Args:
        session_id: Session ID

    Returns:
        dict: Logout result
    """
    if session_id not in _active_sessions:
        return {
            "status": "error",
            "error": f"Session not found: {session_id}"
        }

    del _active_sessions[session_id]

    return {
        "status": "success",
        "data": {"message": "Logged out successfully"}
    }