"""Registered record model."""

from pydantic import BaseModel, Field, field_validator

from models.enums import AppointmentStatus, SlotPeriod


class Appointment(BaseModel):
    """Registered record. Only change the status and never physically delete it.

    Attributes:
        appointment_id: Registration number, such as AP202609280001
        patient_name: Patient's name
        department_id: Department of consultation
        doctor_id: Outpatient doctor
        slot_id: Occupied number source
        date: Date of consultation（YYYY-MM-DD）
        period: Period of time
        status: Registration status
        created_at: Registration time
        cancelled_at: Cancellation time (uncancelled is None）
    """

    appointment_id: str = Field(
        ...,
        pattern=r"^AP\d{12}$",
        description="Registration number",
        examples=["AP202609280001"],
    )
    patient_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Patient's name",
    )
    department_id: str = Field(
        ...,
        pattern=r"^dept_[a-z_]+$",
        description="Identification of the department of consultation",
    )
    doctor_id: str = Field(
        ...,
        pattern=r"^DR\d{3}$",
        description="Outpatient doctor's logo",
    )
    slot_id: str = Field(
        ...,
        pattern=r"^SLOT-\d{8}-\d{3}$",
        description="Occupied number source identification",
    )
    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Date of consultation",
    )
    period: SlotPeriod = Field(..., description="Period of time")
    status: AppointmentStatus = Field(..., description="Registration status")
    created_at: str = Field(..., min_length=1, description="Registration time")
    cancelled_at: str | None = Field(None, description="Cancel the time")

    @field_validator("appointment_id", mode="before")
    @classmethod
    def _normalize_appointment_id(cls, value: str) -> str:
        value = value.strip().upper()
        if not value.startswith("AP"):
            raise ValueError("appointment_id Must start with AP")
        return value

    @field_validator("patient_name")
    @classmethod
    def _strip_patient_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("The patient's name cannot be empty.")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
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
            ]
        }
    }


__all__ = ["Appointment"]
