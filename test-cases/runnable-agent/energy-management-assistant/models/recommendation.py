"""Recommendation models."""

from typing import List, Optional
from pydantic import BaseModel, Field
from models.enums import Priority, Confidence


class Recommendation(BaseModel):
    """Energy efficiency recommendation."""
    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    category: str = Field(..., description="Category: HVAC, Lighting, Equipment, Operations, Maintenance")
    description: str = Field(..., description="Detailed recommendation description")
    estimated_annual_savings_kwh: float = Field(..., ge=0)
    estimated_annual_cost_savings: float = Field(..., ge=0)
    implementation_cost_min: float = Field(..., ge=0)
    implementation_cost_max: float = Field(..., ge=0)
    payback_period_months: float = Field(..., ge=0)
    priority: Priority
    implementation_notes: Optional[List[str]] = None


class Opportunity(BaseModel):
    """Identified efficiency opportunity."""
    opportunity_type: str
    category: str
    description: str
    estimated_savings_potential_percent: float = Field(..., ge=0, le=100)
    confidence: Confidence
    indicators: List[str] = []


class SavingsEstimate(BaseModel):
    """Savings estimate for a measure."""
    measure_type: str
    scope: Optional[str] = None
    baseline_consumption_kwh: float
    projected_consumption_kwh: float
    annual_savings_kwh: float
    annual_cost_savings: float
    confidence_interval: dict  # {"low": float, "high": float}