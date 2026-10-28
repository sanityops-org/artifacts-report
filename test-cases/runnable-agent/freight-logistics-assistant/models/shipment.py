"""Shipment model for freight tracking."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from models.enums import ShipmentStatus, CargoCategory


class TrackingEvent(BaseModel):
    """Single tracking event."""
    timestamp: datetime = Field(..., description="Event timestamp")
    location: str = Field(..., description="Event location")
    status: ShipmentStatus = Field(..., description="Status at this event")
    description: str = Field(..., description="Event description")


class Shipment(BaseModel):
    """Shipment model for tracking."""
    tracking_number: str = Field(..., description="Unique tracking number")
    origin: str = Field(..., description="Origin city/facility")
    destination: str = Field(..., description="Destination city/facility")
    status: ShipmentStatus = Field(..., description="Current status")
    carrier_id: str = Field(..., description="Carrier identifier")
    carrier_name: Optional[str] = Field(None, description="Carrier display name")
    cargo_type: CargoCategory = Field(CargoCategory.GENERAL, description="Cargo category")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    volume_cbm: Optional[float] = Field(None, ge=0, description="Volume in cubic meters")
    pickup_date: Optional[datetime] = Field(None, description="Scheduled pickup date")
    eta: Optional[datetime] = Field(None, description="Estimated arrival")
    actual_delivery: Optional[datetime] = Field(None, description="Actual delivery time")
    current_location: Optional[str] = Field(None, description="Current location")
    last_update: datetime = Field(default_factory=datetime.now, description="Last status update")
    tracking_history: List[TrackingEvent] = Field(default_factory=list, description="Tracking events")
    notes: Optional[str] = Field(None, description="Additional notes")