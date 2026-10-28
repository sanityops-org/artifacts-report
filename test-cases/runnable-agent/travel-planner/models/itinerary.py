"""
Itinerary model for travel plans.
"""

from pydantic import BaseModel, Field

from models.enums import AttractionCategory


class Activity(BaseModel):
    """Single activity in an itinerary"""
    activity_id: str = Field(..., description="Activity ID")
    attraction_id: str = Field(..., pattern=r"^ATTR\d{4}$", description="Attraction ID")
    attraction_name: str = Field(..., description="Attraction name")
    start_time: str = Field(..., description="Start time (HH:MM format)")
    duration_hours: float = Field(..., gt=0, description="Duration in hours")
    notes: str | None = Field(None, description="Additional notes")


class DailyPlan(BaseModel):
    """Daily plan in an itinerary"""
    day_number: int = Field(..., ge=1, description="Day number")
    date: str = Field(..., description="Date (YYYY-MM-DD format)")
    activities: list[Activity] = Field(default_factory=list, description="List of activities")
    estimated_cost_usd: float = Field(default=0, ge=0, description="Estimated cost for the day")


class Itinerary(BaseModel):
    """Travel itinerary model"""
    itinerary_id: str = Field(..., pattern=r"^ITIN\d{4}$", description="Itinerary ID")
    destination_id: str = Field(..., pattern=r"^DEST\d{3}$", description="Destination ID")
    destination_name: str = Field(..., description="Destination name")
    duration_days: int = Field(..., ge=1, le=14, description="Duration in days")
    theme: str | None = Field(None, description="Travel theme")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD format)")
    daily_plans: list[DailyPlan] = Field(default_factory=list, description="List of daily plans")
    total_estimated_cost_usd: float = Field(default=0, ge=0, description="Total estimated cost")


__all__ = ["Activity", "DailyPlan", "Itinerary"]
