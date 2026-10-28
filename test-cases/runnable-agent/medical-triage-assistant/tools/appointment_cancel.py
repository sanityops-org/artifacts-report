#!/usr/bin/env python3
"""appointment_cancel: Cancel a registered record and roll back the source residual number of the corresponding number.

Only call after the patient clearly indicates that he wants to cancel and the registration number has been confirmed. Only records with booked status can be canceled,
And the record must belong to the patient of the current session. This tool will write the status change and make up for the remaining number.

Cancel the serial number of the non-recoverable registration number - the record only changes the status and never physically deletes.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis import session_api
from apis.data_store import DataStore
from models.enums import AppointmentStatus, SlotStatus

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "appointment_id": {
            "type": "string",
            "maxLength": 30,
            "description": "The registration number to be canceled, such as AP202609280001, comes from the registration results or query results.",
        }
    },
    "required": ["appointment_id"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"appointment_id": str}（Session information is injected by runtime)

    Returns:
        {"status": "success", "data": {"appointment_id", "patient_name", "slot_id",
         "date", "period", "status", "cancelled_at", "remaining_after"}}
        Someone {"status": "error", "error": str}
    """
    session_id = (params.get("_session") or {}).get("session_id")
    if not session_id:
        return {"status": "error", "error": "Missing conversation information"}

    appointment_id = params.get("appointment_id")
    if not appointment_id:
        return {"status": "error", "error": "The required parameters are missing: appointment_id"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        records = data_store.load_appointments()

        target = next((r for r in records if r.appointment_id == appointment_id), None)
        if target is None:
            return {"status": "error", "error": f"The registered number does not exist.: {appointment_id}"}

        profile = session_api.get_patient(session_id)
        if profile is None or not profile.name:
            return {
                "status": "error",
                "error": "The patient's information has not been registered yet, and the registration attribution cannot be verified. Please provide your name first.",
            }
        if target.patient_name != profile.name:
            return {
                "status": "error",
                "error": f"No right to cancel: The registered {appointment_id} patient is {target.patient_name}, not the patient of this session.",
            }
        if target.status != AppointmentStatus.BOOKED:
            return {
                "status": "error",
                "error": f"Registration cannot be canceled: {appointment_id}, current status {target.status.value}",
            }

        slots = data_store.load_slots()
        slot = next((s for s in slots if s.slot_id == target.slot_id), None)
        if slot is None:
            return {
                "status": "error",
                "error": f"The number source does not exist: {target.slot_id}, and the remaining number cannot be replenished.",
            }

        cancelled_at = datetime.now().isoformat(timespec="seconds")
        updated_record = target.model_copy(
            update={"status": AppointmentStatus.CANCELLED, "cancelled_at": cancelled_at}
        )
        remaining_after = min(slot.remaining + 1, slot.capacity)
        updated_slot = slot.model_copy(
            update={
                "remaining": remaining_after,
                "status": SlotStatus.AVAILABLE if slot.status == SlotStatus.FULL else slot.status,
            }
        )

        updated_records = [
            updated_record if r.appointment_id == appointment_id else r for r in records
        ]
        updated_slots = [
            updated_slot if s.slot_id == slot.slot_id else s for s in slots
        ]

        data_store.save_appointments(updated_records)
        try:
            data_store.save_slots(updated_slots)
        except Exception:
            # Two-step writing to the must atom: roll back the registered record status when the source of the supplementary number fails,
            # Otherwise, the record has been cancelled and the remaining number has not been replenished, and the number source will be permanently missing.
            data_store.save_appointments(records)
            raise

        return {
            "status": "success",
            "data": {
                "appointment_id": updated_record.appointment_id,
                "patient_name": updated_record.patient_name,
                "slot_id": updated_record.slot_id,
                "date": updated_record.date,
                "period": updated_record.period.value,
                "status": updated_record.status.value,
                "cancelled_at": cancelled_at,
                "remaining_after": remaining_after,
            },
        }
    except KeyError as e:
        return {"status": "error", "error": f"The session is invalid: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error": f"Failed to cancel the registration: {str(e)}"}


if __name__ == "__main__":
    print(execute({"appointment_id": "AP202609280001"}))
