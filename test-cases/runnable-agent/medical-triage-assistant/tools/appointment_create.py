#!/usr/bin/env python3
"""appointment_create: Register for the current conversation patient and occupy a number source.

Before calling, it must be confirmed that the patient's name, gender and age are complete, and slot_id comes from the number source query results.
The same patient cannot be registered repeatedly in the same department on the same day. Successfully return the registration number and the consultation prompt; the remaining number is insufficient or
When the information is incomplete, it returns an error without any side effects. This tool will be written into the registered record and the remaining number will be deducted.

The registration number format is AP{YYYYMMDD}{4-digit serial number}, and the serial number is increased globally according to the date of consultation; cancel the serial number without recycling.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis import session_api
from apis.data_store import DataStore
from models.appointment import Appointment
from models.enums import AppointmentStatus, SlotPeriod, SlotStatus
from tools._labels import DOCTOR_TITLE_LABELS

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "slot_id": {
            "type": "string",
            "maxLength": 60,
            "description": "The source identification of the account to be hung must come from the return result of appointment_query_slots. Do not make it up by yourself.",
        }
    },
    "required": ["slot_id"],
}


def _next_appointment_id(existing: list, date_part: str) -> str:
    """Generate the next registration number on the same day: the number of records on the same date + 1, and fill in the left from zero to 4 digits"""
    prefix = f"AP{date_part}"
    used = sum(1 for item in existing if item.appointment_id.startswith(prefix))
    return f"{prefix}{used + 1:04d}"


def _build_hint(appointment: Appointment, department, doctor) -> str:
    """Tips for patients to go to the doctor"""
    period_cn = "Morning " if appointment.period == SlotPeriod.MORNING else " Afternoon"
    parts = [
        f"Please go to {department.location} to pick up the number and wait for treatment at {appointment.date} {period_cn} according to the registration time.",
        f"Department:{department.name}",
        f"Doctor:{doctor.name}（{DOCTOR_TITLE_LABELS[doctor.title]}）",
        f"Registration number:{appointment.appointment_id}",
    ]
    if department.preparation:
        parts.append("Preparation before going to the doctor:" + "；".join(department.preparation))
    parts.append("Please bring a valid ID. It is recommended to arrive 15 minutes in advance.")
    return "。".join(parts[:-1]) + "。" + parts[-1]


def _prepare(
    params: Dict[str, Any]
) -> Tuple[Dict[str, Any] | None, Dict[str, Any] | None]:
    """Check and return (error result, context); when an error occurs, the second item is None"""
    session_id = (params.get("_session") or {}).get("session_id")
    if not session_id:
        return {"status": "error", "error": "Missing conversation information"}, None

    slot_id = params.get("slot_id")
    if not slot_id:
        return {"status": "error", "error": "The required parameters are missing: slot_id"}, None

    try:
        data_store = DataStore(data_dir=project_root / "data")

        profile = session_api.get_patient(session_id)
        if profile is None or not profile.is_complete:
            missing = profile.missing_fields if profile else ["Name", "Gender", "Age"]
            return (
                {
                    "status": "error",
                    "error": "The patient's information is incomplete and missing: " + "、".join(missing),
                    "data": {"missing_fields": missing},
                },
                None,
            )

        slots = data_store.load_slots()
        slot = next((s for s in slots if s.slot_id == slot_id), None)
        if slot is None:
            return (
                {"status": "error", "error": f"The number source does not exist: {slot_id}, please call the number source to query first to get valid slot_id"},
                None,
            )
        if slot.status == SlotStatus.FULL or slot.remaining <= 0:
            return ({"status": "error", "error": f"The account source is full.: {slot_id}"}, None)
        if slot.status != SlotStatus.AVAILABLE:
            return (
                {"status": "error", "error": f"The number source cannot be registered: {slot_id}, current status {slot.status.value}"},
                None,
            )

        appointments = data_store.load_appointments()
        for item in appointments:
            if (
                item.patient_name == profile.name
                and item.department_id == slot.department_id
                and item.date == slot.date
                and item.status == AppointmentStatus.BOOKED
            ):
                return (
                    {
                        "status": "error",
                        "error": (
                            f"Repeated registration: {profile.name} already in {slot.date}"
                            f" {slot.department_id} The registration of {item.appointment_id}"
                        ),
                    },
                    None,
                )

        return (
            None,
            {
                "data_store": data_store,
                "profile": profile,
                "slots": slots,
                "slot": slot,
                "appointments": appointments,
            },
        )
    except Exception as e:
        return {"status": "error", "error": f"Registration failed: {str(e)}"}, None


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"slot_id": str}（Session information is injected by runtime)

    Returns:
        {"status": "success", "data": {"appointment_id", "patient_name",
         "department_id", "department_name", "location", "doctor_id", "doctor_name",
         "slot_id", "date", "period", "start_time", "end_time", "status",
         "remaining_after", "hint"}} Someone {"status": "error", "error": str}
    """
    error, ctx = _prepare(params)
    if error is not None:
        return error

    try:
        data_store = ctx["data_store"]
        profile = ctx["profile"]
        slots = ctx["slots"]
        slot = ctx["slot"]
        appointments = ctx["appointments"]

        departments = {d.department_id: d for d in data_store.load_departments()}
        doctors = {d.doctor_id: d for d in data_store.load_doctors()}
        department = departments[slot.department_id]
        doctor = doctors[slot.doctor_id]

        appointment_id = _next_appointment_id(appointments, slot.date.replace("-", ""))
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_name=profile.name,
            department_id=slot.department_id,
            doctor_id=slot.doctor_id,
            slot_id=slot.slot_id,
            date=slot.date,
            period=slot.period,
            status=AppointmentStatus.BOOKED,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )

        remaining_after = slot.remaining - 1
        updated_slot = slot.model_copy(
            update={
                "remaining": remaining_after,
                "status": SlotStatus.FULL if remaining_after == 0 else slot.status,
            }
        )
        refreshed = [updated_slot if s.slot_id == slot.slot_id else s for s in slots]
        updated_appointments = appointments + [appointment]

        data_store.save_slots(refreshed)
        try:
            data_store.save_appointments(updated_appointments)
        except Exception:
            # Write first and then write two steps to atom: roll back the deducted number source when the registered record fails to write,
            # Otherwise, the remaining number is occupied but there is no record, resulting in permanent omission.
            data_store.save_slots(slots)
            raise

        return {
            "status": "success",
            "data": {
                "appointment_id": appointment.appointment_id,
                "patient_name": appointment.patient_name,
                "department_id": slot.department_id,
                "department_name": department.name,
                "location": department.location,
                "doctor_id": slot.doctor_id,
                "doctor_name": doctor.name,
                "slot_id": slot.slot_id,
                "date": slot.date,
                "period": slot.period.value,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "status": appointment.status.value,
                "remaining_after": remaining_after,
                "hint": _build_hint(appointment, department, doctor),
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Registration failed: {str(e)}"}


if __name__ == "__main__":
    print(execute({"slot_id": "SLOT-20260928-001"}))
