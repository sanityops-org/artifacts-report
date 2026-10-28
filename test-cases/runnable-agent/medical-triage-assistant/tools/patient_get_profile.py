#!/usr/bin/env python3
"""patient_get_profile: Read the patient information recorded in this session.

It is used to confirm whether the name, gender and age are complete before registration. This tool is read-only and has no parameters.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis import session_api
from models.patient import PatientProfile

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {},
    "required": [],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: No business parameters are required (session information is injected by runtime)

    Returns:
        {"status": "success", "data": {"name", "gender", "age", "phone",
         "is_complete", "missing_fields"}} Someone {"status": "error", "error": str}
    """
    session_id = (params.get("_session") or {}).get("session_id")
    if not session_id:
        return {"status": "error", "error": "Missing conversation information"}

    try:
        profile = session_api.get_patient(session_id) or PatientProfile()
        data = profile.model_dump(mode="json")
        data["is_complete"] = profile.is_complete
        data["missing_fields"] = profile.missing_fields
        return {"status": "success", "data": data}
    except KeyError as e:
        return {"status": "error", "error": f"The session is invalid: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error": f"Failed to read the patient's information: {str(e)}"}


if __name__ == "__main__":
    print(execute({}))
