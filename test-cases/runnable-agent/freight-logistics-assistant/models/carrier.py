"""Carrier model for freight logistics."""

from typing import List, Optional
from pydantic import BaseModel, Field

from models.enums import CarrierType, ServiceLevel


class Carrier(BaseModel):
    """Carrier model."""
    carrier_id: str = Field(..., description="Carrier identifier")
    name: str = Field(..., description="Carrier name")
    type: CarrierType = Field(..., description="Carrier service type")
    coverage_regions: List[str] = Field(default_factory=list, description="Coverage regions")
    service_levels: List[ServiceLevel] = Field(default_factory=list, description="Available service levels")
    rating: float = Field(3.0, ge=1, le=5, description="Carrier rating (1-5)")
    contact: Optional[str] = Field(None, description="Contact information")
    website: Optional[str] = Field(None, description="Carrier website")
    base_rate_per_km: float = Field(..., ge=0, description="Base rate per km")
    fuel_surcharge_pct: float = Field(0.15, ge=0, description="Fuel surcharge percentage")
    min_charge: float = Field(100, ge=0, description="Minimum charge")