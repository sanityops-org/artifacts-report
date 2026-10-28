"""
Pet model describing an adoptable animal.
"""

from pydantic import BaseModel, Field

from models.enums import AdoptionStatus, PetSex, Species


class Pet(BaseModel):
    """Adoptable pet model"""
    pet_id: str = Field(..., pattern=r"^PET\d{3}$", description="Pet ID")
    name: str = Field(..., min_length=1, max_length=50, description="Pet name")
    breed_id: str = Field(..., pattern=r"^BREED\d{3}$", description="Breed ID")
    species: Species = Field(..., description="Species")
    age_months: int = Field(..., ge=0, le=400, description="Age in months")
    sex: PetSex = Field(..., description="Sex")
    adoption_status: AdoptionStatus = Field(
        default=AdoptionStatus.AVAILABLE, description="Adoption listing status"
    )
    description: str = Field(..., min_length=10, description="Pet description")


__all__ = ["Pet"]
