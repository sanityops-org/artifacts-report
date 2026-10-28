"""Route model for freight logistics."""

from typing import List, Optional
from pydantic import BaseModel, Field

from models.enums import CargoCategory


class Waypoint(BaseModel):
    """Waypoint on a route."""
    sequence: int = Field(..., description="Order in route")
    location: str = Field(..., description="Waypoint location")
    facility: Optional[str] = Field(None, description="Facility name")
    estimated_arrival: Optional[str] = Field(None, description="ETA at waypoint")
    estimated_departure: Optional[str] = Field(None, description="ETD from waypoint")


class RouteRestriction(BaseModel):
    """Route restriction for specific cargo types."""
    cargo_category: CargoCategory = Field(..., description="Restricted cargo category")
    allowed: bool = Field(True, description="Whether cargo is allowed")
    requirements: List[str] = Field(default_factory=list, description="Requirements if allowed")
    notes: Optional[str] = Field(None, description="Additional notes")


class Route(BaseModel):
    """Route model for freight planning."""
    route_id: str = Field(..., description="Route identifier")
    name: str = Field(..., description="Route name")
    origin: str = Field(..., description="Origin city/facility")
    destination: str = Field(..., description="Destination city/facility")
    distance_km: float = Field(..., ge=0, description="Total distance in km")
    estimated_hours: float = Field(..., ge=0, description="Estimated transit time in hours")
    waypoints: List[Waypoint] = Field(default_factory=list, description="Route waypoints")
    road_types: List[str] = Field(default_factory=list, description="Highway/road types")
    service_stations: List[str] = Field(default_factory=list, description="Available service stations")
    restrictions: List[RouteRestriction] = Field(default_factory=list, description="Cargo restrictions")
    toll_cost: float = Field(0, ge=0, description="Estimated toll costs")
    average_speed_kmh: float = Field(60, description="Average speed estimate")


class RouteOption(BaseModel):
    """Route option for recommendation."""
    route_id: str = Field(..., description="Route identifier")
    name: str = Field(..., description="Route name")
    origin: str = Field(..., description="Origin")
    destination: str = Field(..., description="Destination")
    distance_km: float = Field(..., description="Distance in km")
    estimated_hours: float = Field(..., description="Transit time in hours")
    estimated_cost: float = Field(..., description="Estimated cost")
    waypoints_count: int = Field(0, description="Number of waypoints")
    restrictions: List[str] = Field(default_factory=list, description="Restriction summary")