"""
Tests for the travel destination engine.
"""

import pytest

from apis.destination_engine import DestinationEngine
from models import Attraction, Destination


@pytest.fixture
def destinations():
    return [
        Destination(
            destination_id="DEST001", name="Paris", country="France", continent="Europe",
            description="A romantic European capital for testing.", best_seasons=["spring"],
            budget_level="moderate", themes=["culture", "romantic"], currency="EUR",
            language="French", timezone="CET"
        ),
        Destination(
            destination_id="DEST002", name="Bali", country="Indonesia", continent="Asia",
            description="A tropical island for testing.", best_seasons=["summer"],
            budget_level="budget", themes=["beach", "relaxation"], currency="IDR",
            language="Indonesian", timezone="WITA"
        ),
        Destination(
            destination_id="DEST003", name="Vancouver", country="Canada", continent="North America",
            description="A coastal city for testing.", best_seasons=["summer"],
            budget_level="moderate", themes=["nature", "city"], currency="CAD",
            language="English", timezone="PST"
        ),
    ]


@pytest.fixture
def attractions():
    return [
        Attraction(attraction_id="ATTR0001", destination_id="DEST001", name="Tower",
                   category="culture", description="A tower used only in tests.",
                   visit_duration_hours=2.0, entrance_fee_usd=25, rating=4.7,
                   recommended_time="afternoon"),
        Attraction(attraction_id="ATTR0002", destination_id="DEST001", name="Quiet Museum",
                   category="culture", description="A museum used only in tests.",
                   visit_duration_hours=3.0, entrance_fee_usd=20, rating=4.2,
                   recommended_time="morning"),
        Attraction(attraction_id="ATTR0003", destination_id="DEST002", name="Beach",
                   category="beach", description="A beach used only in tests.",
                   visit_duration_hours=4.0, entrance_fee_usd=0, rating=4.5,
                   recommended_time="afternoon"),
    ]


@pytest.fixture
def engine(destinations, attractions):
    return DestinationEngine(destinations, attractions)


def test_search_with_no_filters_returns_all(engine):
    assert len(engine.search_destinations()) == 3


def test_search_by_country_is_case_insensitive(engine):
    assert [d.destination_id for d in engine.search_destinations(country="france")] == ["DEST001"]


def test_search_by_theme(engine):
    assert [d.destination_id for d in engine.search_destinations(theme="relaxation")] == ["DEST002"]


def test_search_by_query_matches_description(engine):
    assert [d.destination_id for d in engine.search_destinations(query="tropical")] == ["DEST002"]


def test_search_combines_filters(engine):
    """A theme and a country that do not overlap yields nothing."""
    assert engine.search_destinations(country="France", theme="beach") == []


def test_search_with_unknown_theme_is_ignored(engine):
    """An unparseable enum value must not silently empty the result set."""
    assert len(engine.search_destinations(theme="teleportation")) == 3


def test_get_destination(engine):
    assert engine.get_destination("DEST002").name == "Bali"
    assert engine.get_destination("DEST999") is None


def test_attractions_for_destination(engine):
    assert len(engine.get_attractions_for_destination("DEST001")) == 2


def test_attractions_are_ordered_by_rating_descending(engine):
    result = engine.get_attractions_for_destination("DEST001")
    assert [a.rating for a in result] == sorted([a.rating for a in result], reverse=True)


def test_attractions_filter_by_category(engine):
    result = engine.get_attractions_for_destination("DEST002", category="beach")
    assert [a.attraction_id for a in result] == ["ATTR0003"]


def test_attractions_filter_by_min_rating(engine):
    result = engine.get_attractions_for_destination("DEST001", min_rating=4.5)
    assert [a.attraction_id for a in result] == ["ATTR0001"]


def test_attractions_for_unknown_destination_returns_empty(engine):
    assert engine.get_attractions_for_destination("DEST999") == []
