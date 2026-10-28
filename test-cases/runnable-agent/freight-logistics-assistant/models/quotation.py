"""Quotation model for freight pricing."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from models.enums import ServiceLevel, QuotationStatus


class AccessorialCharge(BaseModel):
    """Accessorial charge item."""
    name: str = Field(..., description="Charge name")
    description: Optional[str] = Field(None, description="Charge description")
    amount: float = Field(..., ge=0, description="Charge amount")


class Quotation(BaseModel):
    """Freight quotation model."""
    quote_id: str = Field(..., description="Quotation identifier")
    carrier_id: str = Field(..., description="Carrier identifier")
    carrier_name: Optional[str] = Field(None, description="Carrier display name")
    route_id: Optional[str] = Field(None, description="Route identifier")
    origin: str = Field(..., description="Origin")
    destination: str = Field(..., description="Destination")
    distance_km: float = Field(..., ge=0, description="Distance")
    weight_kg: float = Field(..., gt=0, description="Weight")
    volume_cbm: Optional[float] = Field(None, description="Volume")
    service_level: ServiceLevel = Field(ServiceLevel.STANDARD, description="Service level")
    base_rate: float = Field(..., ge=0, description="Base freight rate")
    fuel_surcharge: float = Field(..., ge=0, description="Fuel surcharge")
    accessorial_charges: List[AccessorialCharge] = Field(default_factory=list, description="Additional charges")
    total_estimate: float = Field(..., ge=0, description="Total estimated cost")
    transit_days_min: int = Field(1, ge=1, description="Minimum transit days")
    transit_days_max: int = Field(5, ge=1, description="Maximum transit days")
    valid_from: datetime = Field(default_factory=datetime.now, description="Quote validity start")
    valid_until: datetime = Field(..., description="Quote expiry")
    status: QuotationStatus = Field(QuotationStatus.VALID, description="Quote status")
    notes: Optional[str] = Field(None, description="Additional notes")


class QuotationComparison(BaseModel):
    """Multi-carrier quotation comparison."""
    origin: str = Field(..., description="Origin")
    destination: str = Field(..., description="Destination")
    weight_kg: float = Field(..., description="Weight")
    quotes: List[Quotation] = Field(..., description="Carrier quotations")
    best_price: Optional[str] = Field(None, description="Quote ID with best price")
    fastest: Optional[str] = Field(None, description="Quote ID with fastest transit")
    generated_at: datetime = Field(default_factory=datetime.now, description="Comparison timestamp")