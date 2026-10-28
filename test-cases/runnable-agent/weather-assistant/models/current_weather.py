"""
Current weather conditions model.
"""

from pydantic import BaseModel, Field

from models.enums import WeatherCondition, WindDirection


class CurrentConditions(BaseModel):
    """Current weather observations"""
    location_id: str = Field(..., pattern=r"^LOC\d{3}$", description="Location ID")
    timestamp: str = Field(..., description="Observation timestamp (ISO 8601)")
    temperature_c: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    feels_like_c: float = Field(..., ge=-50, le=60, description="Feels-like temperature")
    humidity_percent: int = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed_kmh: float = Field(..., ge=0, le=200, description="Wind speed in km/h")
    wind_direction: WindDirection = Field(..., description="Wind direction")
    conditions: WeatherCondition = Field(..., description="Weather condition")
    pressure_hpa: float = Field(..., ge=900, le=1100, description="Atmospheric pressure in hPa")
    visibility_km: float = Field(..., ge=0, le=50, description="Visibility in kilometers")


__all__ = ["CurrentConditions"]
