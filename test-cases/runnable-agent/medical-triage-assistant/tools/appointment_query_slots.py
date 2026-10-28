#!/usr/bin/env python3
"""appointment_query_slots: Query the source and residual number of the registered number of a department.

After the patient determines the department and is ready to register, return to the list of optional time slots (including slot_id, doctor,
Date, period, residual number). This tool is read-only and does not occupy the number source. Full (remaining number 0) and the source of the suspended number will not
Appear in the result.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import SlotStatus
from tools._labels import DOCTOR_TITLE_LABELS

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "department_id": {
            "type": "string",
            "enum": [
                "dept_general_internal",
                "dept_surgery",
                "dept_orthopedics",
                "dept_obgyn",
                "dept_pediatrics",
                "dept_ophthalmology",
                "dept_ent",
                "dept_dentistry",
                "dept_dermatology",
                "dept_neurology",
                "dept_cardiology",
                "dept_emergency",
            ],
            "description": "Department identification, must use candidate return or confirmed department_id。",
        },
        "date": {
            "type": "string",
            "enum": [
                "2026-09-28",
                "2026-09-29",
                "2026-09-30",
                "2026-10-01",
                "2026-10-02",
            ],
            "description": "Date of consultation, format YYYY-MM-DD. If it is omitted, it will return to all the appointments available dates.",
        },
        "doctor_id": {
            "type": "string",
            "maxLength": 40,
            "description": "Doctor's logo. It is transmitted when the patient names a doctor; if it is omitted, it will return to the number source of all doctors in the department.",
        },
        "period": {
            "type": "string",
            "enum": ["morning", "afternoon"],
            "description": "Time: morning = morning, afternoon = afternoon. There is no limit to omission.",
        },
    },
    "required": ["department_id"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"department_id": str, "date": str（Optional), "doctor_id": str (optional),
                 "period": "morning"|"afternoon"（Optional)}

    Returns:
        {"status": "success", "data": {"department_id", "department_name", "count",
         "slots": [{"slot_id", "department_id", "doctor_id", "doctor_name",
         "doctor_title", "date", "period", "start_time", "end_time", "status",
         "remaining"}]}}
        Someone {"status": "error", "error": str}
    """
    department_id = params.get("department_id")
    if not department_id:
        return {"status": "error", "error": "The required parameters are missing: department_id"}

    date_filter = params.get("date")
    doctor_filter = params.get("doctor_id")
    period_filter = params.get("period")

    try:
        data_store = DataStore(data_dir=project_root / "data")
        departments = data_store.load_departments()
        department = next(
            (d for d in departments if d.department_id == department_id), None
        )
        if department is None:
            available = ", ".join(d.department_id for d in departments)
            return {
                "status": "error",
                "error": f"The department does not exist: {department_id}, the available department: {available}",
            }

        doctors = {d.doctor_id: d for d in data_store.load_doctors()}

        slots: List[Dict[str, Any]] = []
        for slot in data_store.load_slots():
            if slot.department_id != department_id:
                continue
            if slot.status != SlotStatus.AVAILABLE or slot.remaining <= 0:
                continue
            if date_filter and slot.date != date_filter:
                continue
            if doctor_filter and slot.doctor_id != doctor_filter:
                continue
            if period_filter and slot.period.value != period_filter:
                continue
            doctor = doctors.get(slot.doctor_id)
            slots.append(
                {
                    "slot_id": slot.slot_id,
                    "department_id": slot.department_id,
                    "doctor_id": slot.doctor_id,
                    "doctor_name": doctor.name if doctor else "",
                    "doctor_title": DOCTOR_TITLE_LABELS[doctor.title] if doctor else "",
                    "date": slot.date,
                    "period": slot.period.value,
                    "start_time": slot.start_time,
                    "end_time": slot.end_time,
                    "status": slot.status.value,
                    "remaining": slot.remaining,
                }
            )

        slots.sort(key=lambda item: (item["date"], item["start_time"], item["doctor_id"]))
        return {
            "status": "success",
            "data": {
                "department_id": department_id,
                "department_name": department.name,
                "count": len(slots),
                "slots": slots,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to query the number source: {str(e)}"}


if __name__ == "__main__":
    print(execute({"department_id": "dept_neurology"}))
