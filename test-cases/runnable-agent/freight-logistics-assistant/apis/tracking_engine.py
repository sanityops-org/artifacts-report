"""Shipment tracking engine."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from models import Shipment, TrackingEvent, ShipmentStatus
from apis.data_store import DataStore


class TrackingResult(BaseModel):
    """Result of tracking query."""
    tracking_number: str
    found: bool
    shipment: Optional[Shipment] = None
    error: Optional[str] = None


class ShipmentFilter(BaseModel):
    """Filter for shipment list query."""
    origin: Optional[str] = None
    destination: Optional[str] = None
    status: Optional[ShipmentStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


def get_shipment_status(tracking_number: str, data_store: DataStore) -> TrackingResult:
    """Query shipment status by tracking number."""
    shipment = data_store.get_shipment_by_tracking(tracking_number)
    if not shipment:
        return TrackingResult(
            tracking_number=tracking_number,
            found=False,
            error=f"Shipment not found: {tracking_number}",
        )
    return TrackingResult(
        tracking_number=tracking_number,
        found=True,
        shipment=shipment,
    )


def get_shipment_history(tracking_number: str, data_store: DataStore) -> TrackingResult:
    """Get full tracking history for a shipment."""
    result = get_shipment_status(tracking_number, data_store)
    return result


def list_shipments_by_route(
    filter_params: ShipmentFilter, data_store: DataStore
) -> List[Shipment]:
    """List shipments matching filter criteria."""
    shipments = data_store.load_shipments()
    results = []

    for s in shipments:
        # Filter by origin
        if filter_params.origin and filter_params.origin.lower() not in s.origin.lower():
            continue
        # Filter by destination
        if filter_params.destination and filter_params.destination.lower() not in s.destination.lower():
            continue
        # Filter by status
        if filter_params.status and s.status != filter_params.status:
            continue
        # Filter by date range
        if filter_params.date_from and s.pickup_date:
            if s.pickup_date < filter_params.date_from:
                continue
        if filter_params.date_to and s.pickup_date:
            if s.pickup_date > filter_params.date_to:
                continue
        results.append(s)

    return results