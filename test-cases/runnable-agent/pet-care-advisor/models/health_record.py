"""
Health record model for vaccinations, vet visits, and measurements.
"""

from pydantic import BaseModel, Field

from models.enums import HealthRecordType


class HealthRecord(BaseModel):
    """Health record model"""
    record_id: str = Field(..., pattern=r"^REC\d{4}$", description="Record ID")
    pet_id: str = Field(..., pattern=r"^PET\d{3}$", description="Pet ID")
    type: HealthRecordType = Field(..., description="Record type")
    date: str = Field(..., description="Record date (YYYY-MM-DD)")
    description: str = Field(..., min_length=5, description="Record description")
    next_due: str | None = Field(None, description="Next due date (YYYY-MM-DD), if recurring")


__all__ = ["HealthRecord"]
