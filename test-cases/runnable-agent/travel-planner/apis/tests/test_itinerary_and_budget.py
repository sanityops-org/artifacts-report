"""
Tests for the itinerary planner and budget calculator.
"""

import pytest

from apis.budget_calculator import BudgetCalculator
from apis.itinerary_planner import ItineraryPlanner
from models import Attraction, Destination
from models.enums import BudgetLevel


@pytest.fixture
def destination():
    return Destination(
        destination_id="DEST001", name="Paris", country="France", continent="Europe",
        description="A romantic European capital for testing.", best_seasons=["spring"],
        budget_level="moderate", themes=["culture"], currency="EUR",
        language="French", timezone="CET"
    )


@pytest.fixture
def attractions():
    return [
        Attraction(attraction_id="ATTR0001", destination_id="DEST001", name="Tower",
                   category="culture", description="A tower used only in tests.",
                   visit_duration_hours=2.0, entrance_fee_usd=25, rating=4.7,
                   recommended_time="afternoon"),
        Attraction(attraction_id="ATTR0002", destination_id="DEST001", name="Museum",
                   category="culture", description="A museum used only in tests.",
                   visit_duration_hours=3.0, entrance_fee_usd=20, rating=4.5,
                   recommended_time="morning"),
        Attraction(attraction_id="ATTR0003", destination_id="DEST001", name="Park",
                   category="nature", description="A park used only in tests.",
                   visit_duration_hours=1.5, entrance_fee_usd=0, rating=4.1,
                   recommended_time="afternoon"),
    ]


def test_itinerary_has_one_plan_per_day(destination, attractions):
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=3)
    assert len(itinerary.daily_plans) == 3
    assert [p.day_number for p in itinerary.daily_plans] == [1, 2, 3]


def test_daily_plans_advance_one_day_at_a_time(destination, attractions):
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=2, start_date="2026-10-09")
    assert [p.date for p in itinerary.daily_plans] == ["2026-10-09", "2026-10-10"]


def test_itinerary_uses_the_caller_supplied_id(destination, attractions):
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=1, itinerary_id="ITIN0042")
    assert itinerary.itinerary_id == "ITIN0042"


def test_itinerary_falls_back_to_an_internal_counter(destination, attractions):
    planner = ItineraryPlanner(attractions)
    first = planner.create_itinerary(destination, duration_days=1)
    second = planner.create_itinerary(destination, duration_days=1)
    assert (first.itinerary_id, second.itinerary_id) == ("ITIN0001", "ITIN0002")


def test_total_cost_is_the_sum_of_daily_costs(destination, attractions):
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=3)
    expected = sum(p.estimated_cost_usd for p in itinerary.daily_plans)
    assert itinerary.total_estimated_cost_usd == pytest.approx(expected)


def test_theme_filter_narrows_the_attraction_pool(destination, attractions):
    """A culture-only theme should exclude the nature attraction."""
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=1, theme="culture")
    chosen = {a.attraction_id for day in itinerary.daily_plans for a in day.activities}
    assert "ATTR0003" not in chosen


def test_itinerary_with_no_matching_attractions_still_produces_plans(destination, attractions):
    planner = ItineraryPlanner(attractions)
    itinerary = planner.create_itinerary(destination, duration_days=2, theme="foodie")
    assert len(itinerary.daily_plans) == 2
    assert all(day.activities == [] for day in itinerary.daily_plans)


def test_no_day_exceeds_four_activities(destination):
    many = [
        Attraction(attraction_id=f"ATTR{i:04d}", destination_id="DEST001", name=f"Spot {i}",
                   category="culture", description="An attraction used only in tests.",
                   visit_duration_hours=1.0, entrance_fee_usd=0, rating=4.0,
                   recommended_time="morning")
        for i in range(1, 13)
    ]
    planner = ItineraryPlanner(many)
    itinerary = planner.create_itinerary(destination, duration_days=1)
    assert len(itinerary.daily_plans[0].activities) == 4


def test_budget_scales_with_duration(destination):
    calculator = BudgetCalculator()
    short = calculator.estimate_budget(destination, duration_days=2)
    long = calculator.estimate_budget(destination, duration_days=8)
    assert long["total_usd"] > short["total_usd"]


def test_budget_scales_with_travelers(destination):
    calculator = BudgetCalculator()
    solo = calculator.estimate_budget(destination, duration_days=5, travelers_count=1)
    pair = calculator.estimate_budget(destination, duration_days=5, travelers_count=2)

    assert pair["accommodation_usd"] == pytest.approx(solo["accommodation_usd"] * 2)
    assert pair["food_usd"] == pytest.approx(solo["food_usd"] * 2)


def test_luxury_exceeds_budget_level(destination):
    calculator = BudgetCalculator()
    cheap = calculator.estimate_budget(destination, duration_days=5, budget_level=BudgetLevel.BUDGET)
    pricey = calculator.estimate_budget(destination, duration_days=5, budget_level=BudgetLevel.LUXURY)
    assert pricey["total_usd"] > cheap["total_usd"]


def test_total_equals_the_sum_of_the_components(destination):
    calculator = BudgetCalculator()
    result = calculator.estimate_budget(destination, duration_days=4)
    components = sum(
        result[key] for key in
        ("accommodation_usd", "food_usd", "activities_usd", "transport_usd",
         "visa_fees_usd", "insurance_usd")
    )
    assert result["total_usd"] == pytest.approx(components)


def test_budget_always_carries_the_disclaimer(destination):
    """Boundary B3: estimates must be presented as approximate."""
    calculator = BudgetCalculator()
    result = calculator.estimate_budget(destination, duration_days=3)
    assert "approximate" in result["disclaimer"].lower()
