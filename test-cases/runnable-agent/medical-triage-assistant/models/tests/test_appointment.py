"""Register to record the model test."""

import pytest
from pydantic import ValidationError

from models.appointment import Appointment
from models.enums import AppointmentStatus, SlotPeriod


def _appointment(**overrides) -> dict:
    data = {
        "appointment_id": "AP202609280001",
        "patient_name": "Li Wei",
        "department_id": "dept_neurology",
        "doctor_id": "DR001",
        "slot_id": "SLOT-20260928-001",
        "date": "2026-09-28",
        "period": "morning",
        "status": "booked",
        "created_at": "2026-09-26T10:00:00",
        "cancelled_at": None,
    }
    data.update(overrides)
    return data


def test_valid_appointment():
    """Legal registered records can be constructed"""
    appt = Appointment.model_validate(_appointment())

    assert appt.appointment_id == "AP202609280001"
    assert appt.status == AppointmentStatus.BOOKED
    assert appt.period == SlotPeriod.MORNING
    assert appt.cancelled_at is None


@pytest.mark.parametrize(
    "bad_id",
    ["AP20260928001", "AP2026092800001", "AP-20260928-0001", "A202609280001"],
)
def test_invalid_appointment_id_rejected(bad_id):
    """The illegal registration number was rejected."""
    with pytest.raises(ValidationError):
        Appointment.model_validate(_appointment(appointment_id=bad_id))


def test_invalid_status_rejected():
    """The illegal status is rejected."""
    with pytest.raises(ValidationError):
        Appointment.model_validate(_appointment(status="pending"))


def test_empty_patient_name_rejected():
    """The patient's name cannot be empty."""
    with pytest.raises(ValidationError):
        Appointment.model_validate(_appointment(patient_name=""))
