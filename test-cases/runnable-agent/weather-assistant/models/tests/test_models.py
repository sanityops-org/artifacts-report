"""
Tests for the Weather Assistant domain models.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def test_location_requires_valid_id_pattern():
    from models import Location

    Location(location_id="LOC001", name="Testville", region="Region", country="Country",
             latitude=10.0, longitude=20.0)

    with pytest.raises(ValidationError):
        Location(location_id="LOC1", name="Testville", region="Region", country="Country",
                 latitude=10.0, longitude=20.0)


def test_location_rejects_out_of_range_coordinates():
    from models import Location

    with pytest.raises(ValidationError):
        Location(location_id="LOC001", name="Testville", region="Region", country="Country",
                 latitude=91.0, longitude=20.0)

    with pytest.raises(ValidationError):
        Location(location_id="LOC001", name="Testville", region="Region", country="Country",
                 latitude=10.0, longitude=-181.0)


def test_current_conditions_rejects_unknown_wind_direction():
    from models import CurrentConditions

    with pytest.raises(ValidationError):
        CurrentConditions(
            location_id="LOC001", timestamp="2026-10-09T14:00:00", temperature_c=20.0,
            feels_like_c=19.0, humidity_percent=50, wind_speed_kmh=10.0,
            wind_direction="SIDEWAYS", conditions="clear", pressure_hpa=1013.0,
            visibility_km=10.0
        )


def test_current_conditions_rejects_humidity_out_of_range():
    from models import CurrentConditions

    with pytest.raises(ValidationError):
        CurrentConditions(
            location_id="LOC001", timestamp="2026-10-09T14:00:00", temperature_c=20.0,
            feels_like_c=19.0, humidity_percent=140, wind_speed_kmh=10.0,
            wind_direction="N", conditions="clear", pressure_hpa=1013.0,
            visibility_km=10.0
        )


def test_alert_defaults_to_active():
    from models import Alert
    from models.enums import AlertStatus

    alert = Alert(
        alert_id="ALT001", event="Tornado Warning", severity="warning",
        headline="A headline long enough", description="A description long enough to pass validation.",
        areas_affected=["Somewhere"], effective_time="2026-10-09T15:30:00",
        expires_time="2026-10-09T16:30:00", location_ids=["LOC001"]
    )
    assert alert.status == AlertStatus.ACTIVE


def test_alert_requires_at_least_one_location():
    from models import Alert

    with pytest.raises(ValidationError):
        Alert(
            alert_id="ALT001", event="Tornado Warning", severity="warning",
            headline="A headline long enough",
            description="A description long enough to pass validation.",
            areas_affected=["Somewhere"], effective_time="2026-10-09T15:30:00",
            expires_time="2026-10-09T16:30:00", location_ids=[]
        )


@pytest.mark.parametrize("filename,key,model_name", [
    ("locations.json", "locations", "Location"),
    ("current_conditions.json", "current_conditions", "CurrentConditions"),
    ("forecasts.json", "forecasts", "DailyForecast"),
    ("alerts.json", "alerts", "Alert"),
])
def test_shipped_data_files_validate_against_models(filename, key, model_name):
    """Every row in data/ must satisfy its model — guards against enum drift."""
    import models

    model = getattr(models, model_name)
    payload = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
    rows = payload[key]

    assert rows, f"{filename} should ship seed data"
    for row in rows:
        model.model_validate(row)


def test_every_location_has_current_conditions():
    from models import CurrentConditions, Location

    locations = [Location.model_validate(r) for r in
                 json.loads((DATA_DIR / "locations.json").read_text(encoding="utf-8"))["locations"]]
    conditions = [CurrentConditions.model_validate(r) for r in
                  json.loads((DATA_DIR / "current_conditions.json").read_text(encoding="utf-8"))["current_conditions"]]

    covered = {c.location_id for c in conditions}
    for location in locations:
        assert location.location_id in covered, f"{location.location_id} has no observation"


def test_every_location_has_a_seven_day_forecast():
    from models import DailyForecast, Location

    locations = [Location.model_validate(r) for r in
                 json.loads((DATA_DIR / "locations.json").read_text(encoding="utf-8"))["locations"]]
    forecasts = [DailyForecast.model_validate(r) for r in
                 json.loads((DATA_DIR / "forecasts.json").read_text(encoding="utf-8"))["forecasts"]]

    for location in locations:
        days = [f for f in forecasts if f.location_id == location.location_id]
        assert len(days) == 7, f"{location.location_id} has {len(days)} forecast days"
