"""Department data model."""

from pydantic import BaseModel, Field, field_validator

from models.enums import DepartmentCategory


class Department(BaseModel):
    """Department.

    Attributes:
        department_id: Department identification, like dept_general_internal
        name: English display name of the department
        category: Department category
        description: Scope of business
        location: Location of the outpatient clinic
        preparation: Tips to prepare before going to the doctor
    """

    department_id: str = Field(
        ...,
        pattern=r"^dept_[a-z_]+$",
        description="Department identification",
        examples=["dept_general_internal"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="English name of the department",
        examples=["General medicine"],
    )
    category: DepartmentCategory = Field(..., description="Department category")
    description: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Scope of business",
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Location of the outpatient clinic",
        examples=["Area A, 3rd Floor, Outpatient Building"],
    )
    preparation: list[str] = Field(
        default_factory=list,
        description="Tips to prepare before going to the doctor",
    )

    @field_validator("department_id", mode="before")
    @classmethod
    def _normalize_department_id(cls, value: str) -> str:
        value = value.strip().lower()
        if not value.startswith("dept_"):
            raise ValueError("department_id Must start with dept_")
        return value

    @field_validator("preparation")
    @classmethod
    def _strip_preparation(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item.strip()]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "department_id": "dept_general_internal",
                    "name": "General medicine",
                    "category": "internal",
                    "description": "Diagnosis and treatment of fever, cough, abdominal pain, diarrhea and other common internal diseases.",
                    "location": "Area A, 3rd Floor, Outpatient Building",
                    "preparation": ["If you need an empty stomach examination, please go to the doctor in the morning and do not eat on the day."],
                }
            ]
        }
    }


__all__ = ["Department"]
