#!/usr/bin/env python3
"""appointment_query: Check the registration record.

Enter the registration number to query the list, or omit the registration number to query all the registration records of this session. This tool is read-only.

When the registration number is not taken, only the record of the current session patient is returned - the registered record only saves patient_name, not
Session identification, so match by name (known simplification of simulated data). No attribution verification when bringing a registered number: registered number
It is a query credentials in itself. After the session restarts, the patient still needs to be able to check his own record with the number.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis import session_api
from apis.data_store import DataStore

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "appointment_id": {
            "type": "string",
            "maxLength": 30,
            "description": "The registered number is like AP202609280001. If it is omitted, it will return all the registered records of this session.",
        }
    },
    "required": [],
}


def _serialize(appointment) -> Dict[str, Any]:
    """External structure of registered records"""
    return {
        "appointment_id": appointment.appointment_id,
        "patient_name": appointment.patient_name,
        "department_id": appointment.department_id,
        "doctor_id": appointment.doctor_id,
        "slot_id": appointment.slot_id,
        "date": appointment.date,
        "period": appointment.period.value,
        "status": appointment.status.value,
        "created_at": appointment.created_at,
        "cancelled_at": appointment.cancelled_at,
    }


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"appointment_id": str（Optional)} (session information is injected by runtime)

    Returns:
        {"status": "success", "data": {"count": int, "appointments": [...]}}
        Someone {"status": "error", "error": str}
    """
    session_id = (params.get("_session") or {}).get("session_id")
    if not session_id:
        return {"status": "error", "error": "Missing conversation information"}

    appointment_id = params.get("appointment_id")

    try:
        data_store = DataStore(data_dir=project_root / "data")
        records = data_store.load_appointments()

        if appointment_id:
            matched = [r for r in records if r.appointment_id == appointment_id]
            if not matched:
                return {"status": "error", "error": f"The registered number does not exist.: {appointment_id}"}
        else:
            profile = session_api.get_patient(session_id)
            if profile is None or not profile.name:
                return {
                    "status": "error",
                    "error": "The patient's information has not been registered yet, and the affiliation of the registration cannot be determined. Please provide your name first.",
                }
            matched = [r for r in records if r.patient_name == profile.name]

        result: List[Dict[str, Any]] = [_serialize(r) for r in matched]
        result.sort(key=lambda item: item["appointment_id"])
        return {"status": "success", "data": {"count": len(result), "appointments": result}}
    except KeyError as e:
        return {"status": "error", "error": f"The session is invalid: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error": f"Registration inquiry failed: {str(e)}"}


if __name__ == "__main__":
    print(execute({"appointment_id": "AP202609280001"}))
