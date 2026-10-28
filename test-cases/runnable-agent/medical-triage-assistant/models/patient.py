"""Patient model."""

from pydantic import BaseModel, Field, field_validator

from models.enums import Gender


class PatientProfile(BaseModel):
    """The basic information of the patient in this conversation.

    Name/gender/age are all three prerequisites for registration, and the mobile phone number is optional.

    Attributes:
        name: Full name
        gender: Sex
        age: Age (years old)
        phone: Mobile phone number
    """

    name: str | None = Field(None, min_length=1, max_length=30, description="Name")
    gender: Gender | None = Field(None, description="Gender")
    age: int | None = Field(None, ge=0, le=120, description="Age (years old)")
    phone: str | None = Field(
        None,
        pattern=r"^1[3-9][0-9]{9}$",
        description="Mainland China mobile phone number",
    )

    @field_validator("name")
    @classmethod
    def _normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @property
    def is_complete(self) -> bool:
        """Are the three items of name, gender and age complete?"""
        return self.name is not None and self.gender is not None and self.age is not None

    @property
    def missing_fields(self) -> list[str]:
        """Missing required name fields"""
        missing = []
        if self.name is None:
            missing.append("Name")
        if self.gender is None:
            missing.append("Gender")
        if self.age is None:
            missing.append("Age")
        return missing

    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "Li Wei", "gender": "male", "age": 32, "phone": "13800138000"}]
        }
    }


__all__ = ["PatientProfile"]
