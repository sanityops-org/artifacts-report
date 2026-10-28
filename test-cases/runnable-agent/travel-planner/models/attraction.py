"""
Attraction model for tourist attractions.
"""

from pydantic import BaseModel, Field

from models.enums import AttractionCategory


class Attraction(BaseModel):
    """Tourist attraction model"""
    attraction_id: str = Field(..., pattern=r"^ATTR\d{4}$", description="Attraction ID")
    destination_id: str = Field(..., pattern=r"^DEST\d{3}$", description="Destination ID")
    name: str = Field(..., min_length=2, description="Attraction name")
    category: AttractionCategory = Field(..., description="Attraction category")
    description: str = Field(..., min_length=10, description="Attraction description")
    visit_duration_hours: float = Field(..., gt=0, le=24, description="Recommended visit duration in hours")
    entrance_fee_usd: float = Field(..., ge=0, description="Entrance fee in USD")
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1.0 to 5.0")
    recommended_time: str = Field(..., description="Recommended visit time (morning, afternoon, evening, full_day)")


__all__ = ["Attraction"]
