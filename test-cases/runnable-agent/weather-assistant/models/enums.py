"""
Enumerations for Weather Assistant domain models.
"""

from enum import Enum


class WeatherCondition(str, Enum):
    """Weather condition types"""
    CLEAR = "clear"                      # Fine
    PARTLY_CLOUDY = "partly_cloudy"      # Cloud
    CLOUDY = "cloudy"                    # Cloudy day
    RAIN = "rain"                        # Rain
    HEAVY_RAIN = "heavy_rain"            # Heavy rain
    THUNDERSTORM = "thunderstorm"        # Thunderstorm
    SNOW = "snow"                        # Snow
    SLEET = "sleet"                      # Sleet
    FOG = "fog"                          # Fog
    WINDY = "windy"                      # Gale


class WindDirection(str, Enum):
    """Wind direction"""
    N = "N"      # North
    NE = "NE"    # North-east
    E = "E"      # East
    SE = "SE"    # South-east
    S = "S"      # South
    SW = "SW"    # Southwest
    W = "W"      # West
    NW = "NW"    # North-west


class AlertSeverity(str, Enum):
    """Alert severity levels, ordered by urgency"""
    WARNING = "warning"      # Warning: Threat to life/property immediately
    WATCH = "watch"          # Surveillance: conditions conducive to bad weather
    ADVISORY = "advisory"    # Consultation: Less serious but noteworthy conditions


class AlertStatus(str, Enum):
    """Alert status"""
    ACTIVE = "active"        # Dynamic
    EXPIRED = "expired"      # Expired
    CANCELLED = "cancelled"  # Canceled


__all__ = [
    "WeatherCondition",
    "WindDirection",
    "AlertSeverity",
    "AlertStatus",
]
