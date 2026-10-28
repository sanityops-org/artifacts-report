#!/usr/bin/env python3
"""patient_update_profile: Record or update the basic information of the patient in this session.

Call when the patient provides the name, gender, age or mobile phone number. Name, gender and age must be guaranteed before registration.
Complete. This tool only writes to the current session and does not involve any real patient data.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis import session_api

_PROFILE_FIELDS = ("name", "gender", "age", "phone")
_RUNTIME_KEYS = ("_session",)  # Injected by run.py, not a business field

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string", "maxLength": 30, "description": "Patient's name."},
        "gender": {
            "type": "string",
            "enum": ["male", "female"],
            "description": "Gender: male = male, female = female.",
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 120,
            "description": "Age (years).",
        },
        "phone": {
            "type": "string",
            "pattern": "^1[3-9][0-9]{9}$",
            "description": "Mainland China mobile phone number, 11 digits. Fill in the optional.",
        },
    },
    "required": [],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"name": str, "gender": "male"|"female", "age": int, "phone": str}（All are optional)

    Returns:
        {"status": "success", "data": {"name", "gender", "age", "phone",
         "is_complete", "missing_fields"}} Someone {"status": "error", "error": str}
    """
    session_id = (params.get("_session") or {}).get("session_id")
    if not session_id:
        return {"status": "error", "error": "Missing conversation information"}

    unknown = [key for key in params if key not in _PROFILE_FIELDS and key not in _RUNTIME_KEYS]
    if unknown:
        return {"status": "error", "error": "Unsupported fields: " + ", ".join(unknown)}

    provided = {key: params[key] for key in _PROFILE_FIELDS if key in params and params[key] is not None}
    if not provided:
        return {"status": "error", "error": "At least one of the following fields needs to be provided: " + ", ".join(_PROFILE_FIELDS)}

    try:
        profile = session_api.update_patient(session_id, **provided)
        data = profile.model_dump(mode="json")
        data["is_complete"] = profile.is_complete
        data["missing_fields"] = profile.missing_fields
        return {"status": "success", "data": data}
    except KeyError as e:
        return {"status": "error", "error": f"The session is invalid: {str(e)}"}
    except ValueError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to record the patient's information: {str(e)}"}


if __name__ == "__main__":
    print(execute({"name": "Li Wei", "gender": "male", "age": 32}))
