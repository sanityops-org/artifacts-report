"""
Tests for the weather engine.
"""

import pytest

from apis.weather_engine import get_current_conditions, get_forecast, search_locations
from models import CurrentConditions, DailyForecast, Location


@pytest.fixture
def locations():
    return [
        Location(location_id="LOC001", name="New York", region="New York", country="USA",
                 latitude=40.7, longitude=-74.0),
        Location(location_id="LOC002", name="New Orleans", region="Louisiana", country="USA",
                 latitude=30.0, longitude=-90.0),
        Location(location_id="LOC003", name="Paris", region="Ile-de-France", country="France",
                 latitude=48.9, longitude=2.4),
    ]


def test_search_matches_name(locations):
    assert [l.location_id for l in search_locations("Paris", locations)] == ["LOC003"]


def test_search_is_case_insensitive(locations):
    assert [l.location_id for l in search_locations("pArIs", locations)] == ["LOC003"]


def test_search_matches_region_and_country(locations):
    assert len(search_locations("Louisiana", locations)) == 1
    assert len(search_locations("USA", locations)) == 2


def test_search_returns_all_substring_matches(locations):
    """'New' matches both New York and New Orleans."""
    ids = {l.location_id for l in search_locations("New", locations)}
    assert ids == {"LOC001", "LOC002"}


def test_search_with_no_matches_returns_empty(locations):
    assert search_locations("Atlantis", locations) == []


def test_search_is_capped_at_ten():
    many = [
        Location(location_id=f"LOC{i:03d}", name=f"Place {i}", region="R", country="C",
                 latitude=0.0, longitude=0.0)
        for i in range(1, 16)
    ]
    assert len(search_locations("Place", many)) == 10


def _observation(location_id, timestamp, temperature):
    return CurrentConditions(
        location_id=location_id, timestamp=timestamp, temperature_c=temperature,
        feels_like_c=temperature, humidity_percent=50, wind_speed_kmh=10.0,
        wind_direction="N", conditions="clear", pressure_hpa=1013.0, visibility_km=10.0
    )


def test_get_current_conditions_returns_latest():
    observations = [
        _observation("LOC001", "2026-10-09T08:00:00", 12.0),
        _observation("LOC001", "2026-10-09T14:00:00", 18.5),
        _observation("LOC001", "2026-10-09T11:00:00", 15.0),
    ]
    assert get_current_conditions("LOC001", observations).temperature_c == 18.5


def test_get_current_conditions_returns_none_when_absent():
    assert get_current_conditions("LOC999", []) is None


def _forecast(location_id, date):
    return DailyForecast(
        location_id=location_id, date=date, high_c=20.0, low_c=10.0, conditions="clear",
        precipitation_probability=10, wind_speed_kmh=10.0, humidity_percent=50
    )


def test_get_forecast_returns_requested_days_earliest_first():
    forecasts = [
        _forecast("LOC001", "2026-10-12"),
        _forecast("LOC001", "2026-10-10"),
        _forecast("LOC001", "2026-10-11"),
    ]
    result = get_forecast("LOC001", 2, forecasts)
    assert [f.date for f in result] == ["2026-10-10", "2026-10-11"]


def test_get_forecast_caps_at_seven_days():
    forecasts = [_forecast("LOC001", f"2026-10-{d:02d}") for d in range(1, 11)]
    assert len(get_forecast("LOC001", 30, forecasts)) == 7


def test_get_forecast_filters_by_location():
    forecasts = [_forecast("LOC001", "2026-10-10"), _forecast("LOC002", "2026-10-10")]
    assert len(get_forecast("LOC001", 7, forecasts)) == 1


def test_get_forecast_with_no_data_returns_empty():
    assert get_forecast("LOC999", 5, []) == []
