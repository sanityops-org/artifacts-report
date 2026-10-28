"""
Accommodation model for places to stay.
"""

from pydantic import BaseModel, Field

from models.enums import AccommodationType


class Accommodation(BaseModel):
    """Accommodation model"""
    accommodation_id: str = Field(..., pattern=r"^ACCOM\d{4}$", description="Accommodation ID")
    destination_id: str = Field(..., pattern=r"^DEST\d{3}$", description="Destination ID")
    name: str = Field(..., min_length=2, description="Accommodation name")
    type: AccommodationType = Field(..., description="Accommodation type")
    price_per_night_usd: float = Field(..., gt=0, description="Price per night in USD")
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1.0 to 5.0")
    amenities: list[str] = Field(default_factory=list, description="List of amenities")
    location_description: str = Field(..., min_length=5, description="Location description")


__all__ = ["Accommodation"]
