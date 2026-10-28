"""
Integration tests: full workflows driven through the tools.
"""

from tools.alert_get_details import execute as alert_details
from tools.alert_query_active import execute as alert_active
from tools.alert_query_by_location import execute as alert_by_location
from tools.alert_subscribe import execute as alert_subscribe
from tools.location_search import execute as location_search
from tools.weather_current import execute as weather_current
from tools.weather_forecast import execute as weather_forecast


def test_location_search_then_current_conditions():
    """The documented two-step flow must resolve end to end."""
    found = location_search({"query": "Chicago"})
    assert found["status"] == "success"
    assert found["data"]["count"] == 1

    location_id = found["data"]["locations"][0]["location_id"]
    current = weather_current({"location_id": location_id})
    assert current["status"] == "success"
    assert current["data"]["location_name"] == "Chicago"
    assert current["data"]["location_id"] == location_id


def test_location_search_then_forecast():
    found = location_search({"query": "Denver"})
    assert found["data"]["count"] == 1
    location_id = found["data"]["locations"][0]["location_id"]

    forecast = weather_forecast({"location_id": location_id, "days": 3})
    assert forecast["status"] == "success"
    assert forecast["data"]["forecast_days"] == 3


def test_forecast_days_are_capped_at_seven():
    result = weather_forecast({"location_id": "LOC001", "days": 14})
    assert result["data"]["forecast_days"] == 7


def test_forecast_days_are_chronological():
    result = weather_forecast({"location_id": "LOC001", "days": 7})
    dates = [d["date"] for d in result["data"]["daily_forecasts"]]
    assert dates == sorted(dates)


def test_forecast_defaults_to_five_days():
    result = weather_forecast({"location_id": "LOC001"})
    assert result["data"]["forecast_days"] == 5


def test_search_for_unsupported_location_returns_empty_not_error():
    result = location_search({"query": "Atlantis"})
    assert result["status"] == "success"
    assert result["data"]["count"] == 0


def test_current_conditions_for_unknown_location_errors():
    result = weather_current({"location_id": "LOC999"})
    assert result["status"] == "error"
    assert "LOC999" in result["error"]


def test_active_alerts_are_returned_severity_ordered():
    result = alert_active({})
    assert result["status"] == "success"

    order = {"warning": 1, "watch": 2, "advisory": 3}
    ranks = [order[a["severity"]] for a in result["data"]["alerts"]]
    assert ranks == sorted(ranks)


def test_alerts_by_location_returns_only_that_location():
    result = alert_by_location({"location_id": "LOC005"})
    assert result["status"] == "success"
    assert result["data"]["count"] >= 1
    for alert in result["data"]["alerts"]:
        assert "LOC005" in alert["location_ids"]


def test_alert_details_round_trip():
    listed = alert_active({})["data"]["alerts"]
    assert listed

    alert_id = listed[0]["alert_id"]
    detail = alert_details({"alert_id": alert_id})
    assert detail["status"] == "success"
    assert detail["data"]["alert_id"] == alert_id


def test_unknown_alert_id_errors():
    result = alert_details({"alert_id": "ALT999"})
    assert result["status"] == "error"
    assert "ALT999" in result["error"]


def test_missing_required_parameters_are_named():
    for tool, field in (
        (weather_current, "location_id"),
        (weather_forecast, "location_id"),
        (alert_details, "alert_id"),
        (alert_by_location, "location_id"),
        (location_search, "query"),
    ):
        result = tool({})
        assert result["status"] == "error"
        assert field in result["error"], f"{tool.__module__} did not name {field}"


def test_subscription_returns_an_id_for_a_known_location():
    result = alert_subscribe({"location_id": "LOC001"})
    assert result["status"] == "success"
    assert result["data"]["subscription_id"].startswith("SUB")


def test_subscription_rejects_unknown_location():
    result = alert_subscribe({"location_id": "LOC999"})
    assert result["status"] == "error"


def test_tool_payloads_contain_no_health_guidance():
    """Boundary B2: no tool may return medical or health advice."""
    forbidden = ("medication", "diagnosis", "symptom", "asthma", "respiratory",
                 "health advice", "consult a doctor")

    payloads = [
        str(weather_current({"location_id": "LOC001"})),
        str(weather_forecast({"location_id": "LOC001"})),
        str(alert_active({})),
        str(alert_by_location({"location_id": "LOC005"})),
    ]

    for payload in payloads:
        lowered = payload.lower()
        for term in forbidden:
            assert term not in lowered, f"health term {term!r} appeared in a tool payload"
