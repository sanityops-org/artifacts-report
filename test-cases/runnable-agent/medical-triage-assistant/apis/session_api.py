"""Patient session: in-process memory session table.

If the session does not fall, the process will be emptied when restarted; the simulated data itself will be emptied. The session is only saved this time.
The basic information of the conversational patient does not involve any real patient data.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from models.patient import PatientProfile

_ALLOWED_FIELDS = ("name", "gender", "age", "phone")

_sessions: Dict[str, Dict[str, Any]] = {}


def create_session() -> Dict[str, Any]:
    """Create a new session.

    Returns:
        Conversation dictionary {"session_id", "patient", "created_at"}
    """
    session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"
    session: Dict[str, Any] = {
        "session_id": session_id,
        "patient": None,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Dict[str, Any]:
    """Take the session by id.

    Raises:
        KeyError: The session does not exist.
    """
    if session_id not in _sessions:
        raise KeyError(f"The session does not exist.: {session_id}")
    return _sessions[session_id]


def get_patient(session_id: str) -> Optional[PatientProfile]:
    """Read the session patient's file and return it when it is not filled in. None"""
    raw = get_session(session_id)["patient"]
    if raw is None:
        return None
    return PatientProfile.model_validate(raw)


def update_patient(session_id: str, **fields: Any) -> PatientProfile:
    """Record or update the session patient information (field accumulation, fields with the value None are not overwritten).

    Raises:
        KeyError: The session does not exist.
        ValueError: The field name is not supported, or the field value is illegal.
    """
    unknown: List[str] = [key for key in fields if key not in _ALLOWED_FIELDS]
    if unknown:
        raise ValueError(f"Unsupported fields: {', '.join(unknown)}")

    session = get_session(session_id)
    current = session["patient"] or {}
    merged = {**current, **{k: v for k, v in fields.items() if v is not None}}
    try:
        profile = PatientProfile.model_validate(merged)
    except Exception as e:
        raise ValueError(f"The patient's information is not legal.: {e}") from e

    session["patient"] = profile.model_dump(mode="json")
    return profile


def reset_all() -> None:
    """Clear all sessions (for test isolation)"""
    _sessions.clear()


__all__ = [
    "create_session",
    "get_patient",
    "get_session",
    "reset_all",
    "update_patient",
]
