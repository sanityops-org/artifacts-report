"""Carbon footprint models."""

from typing import Optional
from pydantic import BaseModel, Field


class CarbonBreakdown(BaseModel):
    """Carbon emissions breakdown by source."""
    electricity_kgco2: float = Field(..., ge=0)
    natural_gas_kgco2: float = Field(..., ge=0)
    other_kgco2: Optional[float] = Field(0, ge=0)
    electricity_percent: float = Field(..., ge=0, le=100)
    natural_gas_percent: float = Field(..., ge=0, le=100)


class EmissionIntensity(BaseModel):
    """Emission intensity metrics."""
    per_sqm: float = Field(..., description="kg CO2 per square meter")
    per_kwh: float = Field(..., description="kg CO2 per kWh")


class CarbonFootprint(BaseModel):
    """Carbon footprint calculation result."""
    facility_id: str
    period_start: str
    period_end: str
    total_emissions_kgco2: float = Field(..., ge=0)
    emission_intensity: EmissionIntensity
    breakdown: Optional[CarbonBreakdown] = None
    previous_period_kgco2: Optional[float] = None
    change_percent: Optional[float] = None


class EmissionFactors(BaseModel):
    """Emission factors by energy source."""
    electricity_grid: float = Field(0.42, description="kg CO2/kWh")
    natural_gas: float = Field(2.0, description="kg CO2/m³")
    diesel: float = Field(2.68, description="kg CO2/liter")
    solar: float = Field(0, description="kg CO2/kWh (Scope 2 only)")
    wind: float = Field(0, description="kg CO2/kWh (Scope 2 only)")