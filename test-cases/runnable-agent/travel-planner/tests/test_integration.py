"""
Integration tests: full workflows driven through the tools.

Saved itineraries live in the shared data store, so tests reset it to avoid
leaking state between cases.
"""

import pytest

from apis.data_store import reset_data_store


@pytest.fixture(autouse=True)
def fresh_store():
    reset_data_store()
    yield
    reset_data_store()


def test_search_then_details_then_attractions():
    from tools.attraction_list import execute as attraction_list
    from tools.destination_details import execute as destination_details
    from tools.destination_search import execute as destination_search

    found = destination_search({"query": "Paris"})
    assert found["status"] == "success"
    assert found["data"]["count"] == 1

    destination_id = found["data"]["destinations"][0]["destination_id"]

    detail = destination_details({"destination_id": destination_id})
    assert detail["status"] == "success"
    assert detail["data"]["destination"]["name"] == "Paris"
    assert detail["data"]["attractions_count"] >= 1

    attractions = attraction_list({"destination_id": destination_id})
    assert attractions["data"]["count"] == detail["data"]["attractions_count"]


def test_search_by_theme_returns_matching_destinations():
    from tools.destination_search import execute as destination_search

    result = destination_search({"theme": "beach"})
    assert result["status"] == "success"
    assert result["data"]["count"] >= 1
    for destination in result["data"]["destinations"]:
        assert "beach" in destination["themes"]


def test_every_seeded_theme_loads_without_a_validation_error():
    """Regression guard: the data once used themes the enum did not define."""
    from tools.destination_search import execute as destination_search

    result = destination_search({})
    assert result["status"] == "success"
    assert result["data"]["count"] == 10


def test_itinerary_is_readable_after_creation():
    """Regression guard: a created itinerary used to be unreachable."""
    from tools.itinerary_create import execute as create
    from tools.itinerary_details import execute as details

    created = create({"destination_id": "DEST001", "duration_days": 3})
    assert created["status"] == "success"

    fetched = details({"itinerary_id": created["data"]["itinerary_id"]})
    assert fetched["status"] == "success"
    assert fetched["data"]["destination_name"] == "Paris"
    assert len(fetched["data"]["daily_plans"]) == 3


def test_successive_itineraries_get_distinct_ids():
    """Regression guard: IDs used to restart at ITIN0001 and overwrite each other."""
    from tools.itinerary_create import execute as create
    from tools.itinerary_details import execute as details

    first = create({"destination_id": "DEST001", "duration_days": 2})
    second = create({"destination_id": "DEST002", "duration_days": 2})

    assert first["data"]["itinerary_id"] != second["data"]["itinerary_id"]

    # Both must still be retrievable — the second must not have overwritten the first
    assert details({"itinerary_id": first["data"]["itinerary_id"]})["data"]["destination_name"] == "Paris"
    assert details({"itinerary_id": second["data"]["itinerary_id"]})["data"]["destination_name"] == "Tokyo"


def test_unknown_itinerary_errors():
    from tools.itinerary_details import execute as details

    result = details({"itinerary_id": "ITIN9999"})
    assert result["status"] == "error"


def test_itinerary_days_are_chronological():
    from tools.itinerary_create import execute as create

    created = create({"destination_id": "DEST001", "duration_days": 4, "start_date": "2026-10-09"})
    dates = [day["date"] for day in created["data"]["daily_plans"]]
    assert dates == sorted(dates)
    assert dates[0] == "2026-10-09"


def test_accommodation_search_filters_by_price_and_type():
    from tools.accommodation_search import execute as accommodation_search

    result = accommodation_search({"destination_id": "DEST001", "max_price": 100})
    assert result["status"] == "success"
    for accommodation in result["data"]["accommodations"]:
        assert accommodation["price_per_night_usd"] <= 100

    hostels = accommodation_search({"destination_id": "DEST001", "type": "hostel"})
    for accommodation in hostels["data"]["accommodations"]:
        assert accommodation["type"] == "hostel"


def test_budget_estimate_carries_a_disclaimer():
    """Boundary B3: estimates must be presented as approximate."""
    from tools.budget_estimate import execute as budget_estimate

    result = budget_estimate({"destination_id": "DEST002", "duration_days": 7})
    assert result["status"] == "success"
    assert "approximate" in result["data"]["estimate"]["disclaimer"].lower()


def test_unknown_ids_produce_errors_not_exceptions():
    from tools.destination_details import execute as destination_details
    from tools.accommodation_details import execute as accommodation_details
    from tools.attraction_details import execute as attraction_details

    assert destination_details({"destination_id": "DEST999"})["status"] == "error"
    assert accommodation_details({"accommodation_id": "ACCOM9999"})["status"] == "error"
    assert attraction_details({"attraction_id": "ATTR9999"})["status"] == "error"


def test_missing_required_parameters_are_named():
    from tools.itinerary_create import execute as create

    for params, field in (({}, "destination_id"), ({"destination_id": "DEST001"}, "duration_days")):
        result = create(params)
        assert result["status"] == "error"
        assert field in result["error"]


def test_tool_payloads_contain_no_booking_or_visa_advice():
    """Boundaries B1/B2: no tool may transact or advise on immigration."""
    forbidden = ("book now", "reservation confirmed", "visa requirement",
                 "you must apply for", "immigration")

    from tools.budget_estimate import execute as budget_estimate
    from tools.destination_details import execute as destination_details

    payloads = [
        str(destination_details({"destination_id": "DEST001"})),
        str(budget_estimate({"destination_id": "DEST001", "duration_days": 5})),
    ]

    for payload in payloads:
        lowered = payload.lower()
        for term in forbidden:
            assert term not in lowered, f"{term!r} appeared in a tool payload"
