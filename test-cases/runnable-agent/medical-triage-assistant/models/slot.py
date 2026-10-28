"""Number source data model."""

from pydantic import BaseModel, Field, field_validator, model_validator

from models.enums import SlotPeriod, SlotStatus


class Slot(BaseModel):
    """Number source: take "department + doctor + date + period + start time" as one unit.

    Attributes:
        slot_id: The number source logo, in the form of SLOT-20260928-001
        department_id: Department
        doctor_id: Outpatient doctor
        date: Date of consultation（YYYY-MM-DD）
        period: Period of time
        start_time: Start time（HH:MM）
        end_time: End time（HH:MM）
        capacity: Total number
        remaining: Remaining number
        status: Number source status
    """

    slot_id: str = Field(
        ...,
        pattern=r"^SLOT-\d{8}-\d{3}$",
        description="Number source identification",
        examples=["SLOT-20260928-001"],
    )
    department_id: str = Field(
        ...,
        pattern=r"^dept_[a-z_]+$",
        description="Identification of the department",
    )
    doctor_id: str = Field(
        ...,
        pattern=r"^DR\d{3}$",
        description="Outpatient doctor's logo",
    )
    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Date of consultation",
        examples=["2026-09-28"],
    )
    period: SlotPeriod = Field(..., description="Period of time")
    start_time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}$",
        description="Start time",
        examples=["08:30"],
    )
    end_time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}$",
        description="End time",
        examples=["09:00"],
    )
    capacity: int = Field(..., ge=1, le=200, description="Total number")
    remaining: int = Field(..., ge=0, description="Remaining number")
    status: SlotStatus = Field(..., description="Number source status")

    @field_validator("slot_id", mode="before")
    @classmethod
    def _normalize_slot_id(cls, value: str) -> str:
        value = value.strip()
        if not value.startswith("SLOT-"):
            raise ValueError("slot_id Must start with SLOT-")
        return value

    @model_validator(mode="after")
    def _check_remaining(self) -> "Slot":
        if self.remaining > self.capacity:
            raise ValueError("remaining Can't be greater than capacity")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "slot_id": "SLOT-20260928-001",
                    "department_id": "dept_neurology",
                    "doctor_id": "DR001",
                    "date": "2026-09-28",
                    "period": "morning",
                    "start_time": "08:30",
                    "end_time": "09:00",
                    "capacity": 10,
                    "remaining": 10,
                    "status": "available",
                }
            ]
        }
    }


__all__ = ["Slot"]
