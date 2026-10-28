"""Facility data models."""

from typing import Optional
from pydantic import BaseModel, Field
from models.enums import FacilityType


class OperatingHours(BaseModel):
    """Operating hours configuration."""
    weekdays: str = Field(..., description="Weekday operating hours")
    weekends: Optional[str] = Field(None, description="Weekend operating hours")


class Location(BaseModel):
    """Facility location."""
    address: str
    city: str
    state: str
    country: str = "USA"


class Facility(BaseModel):
    """Facility model."""
    facility_id: str = Field(..., description="Unique facility identifier")
    name: str = Field(..., description="Facility name")
    type: FacilityType = Field(..., description="Facility type")
    location: Location
    floor_area_m2: float = Field(..., gt=0, description="Floor area in square meters")
    operating_hours: OperatingHours
    annual_consumption_kwh: Optional[float] = Field(None, ge=0)
    peak_demand_kw: Optional[float] = Field(None, ge=0)
    created_at: Optional[str] = None


class FacilityCreate(BaseModel):
    """Model for creating a new facility."""
    name: str
    type: FacilityType
    location: Location
    floor_area_m2: float = Field(..., gt=0)
    operating_hours: OperatingHours