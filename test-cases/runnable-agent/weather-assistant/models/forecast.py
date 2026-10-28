"""
Daily forecast model.
"""

from pydantic import BaseModel, Field

from models.enums import WeatherCondition


class DailyForecast(BaseModel):
    """Daily weather forecast"""
    location_id: str = Field(..., pattern=r"^LOC\d{3}$", description="Location ID")
    date: str = Field(..., description="Forecast date (YYYY-MM-DD)")
    high_c: float = Field(..., ge=-50, le=60, description="Daily high temperature")
    low_c: float = Field(..., ge=-50, le=60, description="Daily low temperature")
    conditions: WeatherCondition = Field(..., description="Expected conditions")
    precipitation_probability: int = Field(..., ge=0, le=100, description="Precipitation probability %")
    wind_speed_kmh: float = Field(..., ge=0, le=200, description="Expected wind speed")
    humidity_percent: int = Field(..., ge=0, le=100, description="Expected humidity %")


__all__ = ["DailyForecast"]
