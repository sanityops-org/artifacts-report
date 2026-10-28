"""
Breed model describing a dog or cat breed's characteristics.
"""

from pydantic import BaseModel, Field

from models.enums import GroomingLevel, PetSize, Species, Temperament


class Breed(BaseModel):
    """Breed model"""
    breed_id: str = Field(..., pattern=r"^BREED\d{3}$", description="Breed ID")
    name: str = Field(..., min_length=2, max_length=100, description="Breed name")
    species: Species = Field(..., description="Species")
    size: PetSize = Field(..., description="Adult size class")
    temperaments: list[Temperament] = Field(..., min_length=1, description="Temperament traits")
    exercise_minutes_per_day: int = Field(..., ge=0, le=300, description="Typical daily exercise (minutes)")
    grooming_level: GroomingLevel = Field(..., description="Grooming intensity")
    apartment_friendly: bool = Field(..., description="Suitable for apartment living")
    good_with_kids: bool = Field(..., description="Generally good with children")
    lifespan_years: str = Field(..., description="Typical lifespan range")
    description: str = Field(..., min_length=10, description="Breed description")


__all__ = ["Breed"]
