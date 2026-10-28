"""
Destination model for travel locations.
"""

from pydantic import BaseModel, Field

from models.enums import BudgetLevel, Season, TravelTheme


class Destination(BaseModel):
    """Travel destination model"""
    destination_id: str = Field(..., pattern=r"^DEST\d{3}$", description="Destination ID")
    name: str = Field(..., min_length=2, max_length=100, description="Destination name")
    country: str = Field(..., min_length=2, description="Country name")
    continent: str = Field(..., description="Continent")
    description: str = Field(..., min_length=10, description="Destination description")
    best_seasons: list[Season] = Field(..., min_length=1, description="Best travel seasons")
    budget_level: BudgetLevel = Field(..., description="Typical budget level")
    themes: list[TravelTheme] = Field(..., min_length=1, description="Travel themes")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (ISO 4217)")
    language: str = Field(..., description="Primary language")
    timezone: str = Field(..., description="Timezone identifier")


__all__ = ["Destination"]
