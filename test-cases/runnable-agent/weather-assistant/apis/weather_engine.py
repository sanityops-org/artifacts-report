"""
weather_engine: Location search and weather lookup.

Pure functions: the caller injects the data, which keeps them directly
unit-testable without touching the filesystem.
"""

from models import CurrentConditions, DailyForecast, Location


def search_locations(query: str, locations: list[Location]) -> list[Location]:
    """
    Search locations by name, region, or country.

    Case-insensitive substring match, capped at 10 results.

    Args:
        query: Search term
        locations: Full location catalog

    Returns:
        Matching locations in catalog order
    """
    query_lower = query.lower().strip()
    matches: list[Location] = []

    for location in locations:
        if (
            query_lower in location.name.lower()
            or query_lower in location.region.lower()
            or query_lower in location.country.lower()
        ):
            matches.append(location)
            if len(matches) >= 10:
                break

    return matches


def get_current_conditions(
    location_id: str,
    conditions: list[CurrentConditions]
) -> CurrentConditions | None:
    """
    Get the most recent current conditions for a location.

    Args:
        location_id: Location ID
        conditions: All current condition observations

    Returns:
        The latest observation for the location, or None if absent
    """
    matching = [c for c in conditions if c.location_id == location_id]

    if not matching:
        return None

    return max(matching, key=lambda c: c.timestamp)


def get_forecast(
    location_id: str,
    days: int,
    forecasts: list[DailyForecast]
) -> list[DailyForecast]:
    """
    Get an ordered forecast for a location, capped at 7 days.

    Args:
        location_id: Location ID
        days: Requested number of days
        forecasts: All forecast rows

    Returns:
        Up to min(days, 7) daily forecasts, earliest first
    """
    days = min(days, 7)

    matching = [f for f in forecasts if f.location_id == location_id]
    matching.sort(key=lambda f: f.date)

    return matching[:days]


__all__ = ["search_locations", "get_current_conditions", "get_forecast"]
