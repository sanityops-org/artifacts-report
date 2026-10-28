"""
Location model for geographic coordinates and metadata.
"""

from pydantic import BaseModel, Field


class Location(BaseModel):
    """Geographic location model"""
    location_id: str = Field(..., pattern=r"^LOC\d{3}$", description="Location ID")
    name: str = Field(..., min_length=2, max_length=100, description="Location name")
    region: str = Field(..., description="Region / State / Province")
    country: str = Field(..., description="Country")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    elevation_m: float | None = Field(None, ge=0, description="Elevation in meters")


__all__ = ["Location"]
