"""Pydantic enumerations for freight logistics domain."""

from enum import Enum


class ShipmentStatus(str, Enum):
    """Shipment status values."""
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    EXCEPTION = "exception"


class CargoCategory(str, Enum):
    """Cargo category types."""
    GENERAL = "general"
    REFRIGERATED = "refrigerated"
    HAZARDOUS = "hazardous"
    OVERSIZED = "oversized"
    FRAGILE = "fragile"
    HIGH_VALUE = "high_value"


class ServiceLevel(str, Enum):
    """Freight service levels."""
    ECONOMY = "economy"
    STANDARD = "standard"
    EXPRESS = "express"


class CarrierType(str, Enum):
    """Carrier service types."""
    FTL = "ftl"  # Full Truckload
    LTL = "ltl"  # Less Than Truckload
    INTERMODAL = "intermodal"
    AIR = "air"
    OCEAN = "ocean"


class RoutePriority(str, Enum):
    """Route optimization priorities."""
    COST = "cost"
    TIME = "time"
    BALANCED = "balanced"


class QuotationStatus(str, Enum):
    """Quotation status."""
    DRAFT = "draft"
    VALID = "valid"
    EXPIRED = "expired"
    ACCEPTED = "accepted"