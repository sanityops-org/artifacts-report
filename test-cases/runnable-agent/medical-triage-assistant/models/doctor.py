"""Doctor's data model."""

from pydantic import BaseModel, Field, field_validator

from models.enums import DoctorTitle

_CLINIC_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


class Doctor(BaseModel):
    """Visiting doctor.

    Attributes:
        doctor_id: The doctor's logo, shaped like DR001
        name: Doctor's name
        title: Professional title
        department_id: Department
        specialties: Good at direction
        clinic_days: Out-patient day
    """

    doctor_id: str = Field(
        ...,
        pattern=r"^DR\d{3}$",
        description="Doctor's logo",
        examples=["DR001"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Doctor's name",
        examples=["Zhang Ming"],
    )
    title: DoctorTitle = Field(..., description="Professional title")
    department_id: str = Field(
        ...,
        pattern=r"^dept_[a-z_]+$",
        description="Identification of the department",
    )
    specialties: list[str] = Field(
        ...,
        min_length=1,
        description="Good at direction",
        examples=[["Headache", "Dizziness"]],
    )
    clinic_days: list[str] = Field(
        default_factory=list,
        description="Out-patient day",
        examples=[["Monday", "Thursday"]],
    )

    @field_validator("doctor_id", mode="before")
    @classmethod
    def _normalize_doctor_id(cls, value: str) -> str:
        value = value.strip().upper()
        if not value.startswith("DR"):
            raise ValueError("doctor_id Must start with DR")
        return value

    @field_validator("clinic_days")
    @classmethod
    def _validate_clinic_days(cls, value: list[str]) -> list[str]:
        for day in value:
            if day not in _CLINIC_DAYS:
                raise ValueError(f"It is illegal to take the value on the day of consultation.: {day}")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "doctor_id": "DR001",
                    "name": "Zhang Ming",
                    "title": "chief",
                    "department_id": "dept_neurology",
                    "specialties": ["Headache", "Dizziness"],
                    "clinic_days": ["Monday", "Thursday"],
                }
            ]
        }
    }


__all__ = ["Doctor"]
