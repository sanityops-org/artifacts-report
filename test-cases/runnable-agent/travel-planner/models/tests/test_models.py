"""
Tests for the Travel Planner domain models.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def test_destination_requires_three_letter_currency():
    from models import Destination

    Destination(
        destination_id="DEST001", name="Testville", country="Testland", continent="Europe",
        description="A destination used only in tests.", best_seasons=["spring"],
        budget_level="moderate", themes=["culture"], currency="EUR",
        language="Testish", timezone="CET"
    )

    with pytest.raises(ValidationError):
        Destination(
            destination_id="DEST001", name="Testville", country="Testland", continent="Europe",
            description="A destination used only in tests.", best_seasons=["spring"],
            budget_level="moderate", themes=["culture"], currency="EURO",
            language="Testish", timezone="CET"
        )


def test_destination_requires_at_least_one_theme():
    from models import Destination

    with pytest.raises(ValidationError):
        Destination(
            destination_id="DEST001", name="Testville", country="Testland", continent="Europe",
            description="A destination used only in tests.", best_seasons=["spring"],
            budget_level="moderate", themes=[], currency="EUR",
            language="Testish", timezone="CET"
        )


def test_attraction_rating_bounds():
    from models import Attraction

    with pytest.raises(ValidationError):
        Attraction(
            attraction_id="ATTR0001", destination_id="DEST001", name="Test",
            category="culture", description="An attraction used only in tests.",
            visit_duration_hours=2.0, entrance_fee_usd=0, rating=6.0,
            recommended_time="morning"
        )


def test_attraction_rejects_negative_fee():
    from models import Attraction

    with pytest.raises(ValidationError):
        Attraction(
            attraction_id="ATTR0001", destination_id="DEST001", name="Test",
            category="culture", description="An attraction used only in tests.",
            visit_duration_hours=2.0, entrance_fee_usd=-1, rating=4.0,
            recommended_time="morning"
        )


def test_itinerary_duration_bounds():
    from models import Itinerary

    with pytest.raises(ValidationError):
        Itinerary(
            itinerary_id="ITIN0001", destination_id="DEST001", destination_name="Testville",
            duration_days=30, start_date="2026-10-09"
        )


def test_accommodation_defaults_to_empty_amenities():
    from models import Accommodation

    acc = Accommodation(
        accommodation_id="ACCOM0001", destination_id="DEST001", name="Test Hotel",
        type="hotel", price_per_night_usd=100.0, rating=4.0,
        location_description="Somewhere central"
    )
    assert acc.amenities == []


@pytest.mark.parametrize("filename,key,model_name", [
    ("destinations.json", "destinations", "Destination"),
    ("attractions.json", "attractions", "Attraction"),
    ("accommodations.json", "accommodations", "Accommodation"),
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


def test_every_destination_theme_is_a_declared_enum_member():
    """Regression guard: data once used themes the enum did not define."""
    from models.enums import TravelTheme

    declared = {m.value for m in TravelTheme}
    destinations = json.loads((DATA_DIR / "destinations.json").read_text(encoding="utf-8"))["destinations"]

    for destination in destinations:
        for theme in destination["themes"]:
            assert theme in declared, f"{destination['name']} uses undeclared theme {theme!r}"


def test_every_attraction_category_is_a_declared_enum_member():
    """Regression guard: data once used categories the enum did not define."""
    from models.enums import AttractionCategory

    declared = {m.value for m in AttractionCategory}
    attractions = json.loads((DATA_DIR / "attractions.json").read_text(encoding="utf-8"))["attractions"]

    for attraction in attractions:
        assert attraction["category"] in declared, (
            f"{attraction['name']} uses undeclared category {attraction['category']!r}"
        )


def test_every_attraction_references_a_known_destination():
    destinations = json.loads((DATA_DIR / "destinations.json").read_text(encoding="utf-8"))["destinations"]
    attractions = json.loads((DATA_DIR / "attractions.json").read_text(encoding="utf-8"))["attractions"]
    accommodations = json.loads((DATA_DIR / "accommodations.json").read_text(encoding="utf-8"))["accommodations"]

    known = {d["destination_id"] for d in destinations}
    for row in attractions + accommodations:
        assert row["destination_id"] in known, f"{row.get('name')} references an unknown destination"
