"""
Tests for the alert engine's filtering and severity ranking.
"""

from apis.alert_engine import get_active_alerts, get_alert_by_id
from models import Alert


def _alert(alert_id, severity, effective_time, location_ids, status="active"):
    return Alert(
        alert_id=alert_id, event=f"{severity.title()} Event", severity=severity,
        headline=f"A {severity} headline", description="A description long enough to validate.",
        areas_affected=["Somewhere"], effective_time=effective_time,
        expires_time="2026-10-10T00:00:00", location_ids=location_ids, status=status
    )


def test_orders_warning_before_watch_before_advisory():
    alerts = [
        _alert("ALT003", "advisory", "2026-10-09T12:00:00", ["LOC001"]),
        _alert("ALT002", "watch", "2026-10-09T14:00:00", ["LOC001"]),
        _alert("ALT001", "warning", "2026-10-09T15:30:00", ["LOC001"]),
    ]
    assert [a.alert_id for a in get_active_alerts(None, alerts)] == ["ALT001", "ALT002", "ALT003"]


def test_same_severity_is_ordered_by_effective_time():
    alerts = [
        _alert("ALT002", "warning", "2026-10-09T15:30:00", ["LOC001"]),
        _alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC001"]),
    ]
    assert [a.alert_id for a in get_active_alerts(None, alerts)] == ["ALT001", "ALT002"]


def test_excludes_non_active_alerts():
    alerts = [
        _alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC001"]),
        _alert("ALT002", "warning", "2026-10-09T13:00:00", ["LOC001"], status="expired"),
        _alert("ALT003", "warning", "2026-10-09T13:00:00", ["LOC001"], status="cancelled"),
    ]
    assert [a.alert_id for a in get_active_alerts(None, alerts)] == ["ALT001"]


def test_filters_by_location():
    alerts = [
        _alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC005"]),
        _alert("ALT002", "watch", "2026-10-09T13:00:00", ["LOC004"]),
    ]
    assert [a.alert_id for a in get_active_alerts("LOC005", alerts)] == ["ALT001"]


def test_location_filter_matches_any_affected_location():
    alerts = [_alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC001", "LOC002"])]
    assert len(get_active_alerts("LOC002", alerts)) == 1


def test_location_filter_with_no_match_returns_empty():
    alerts = [_alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC001"])]
    assert get_active_alerts("LOC999", alerts) == []


def test_no_alerts_returns_empty():
    assert get_active_alerts(None, []) == []


def test_get_alert_by_id():
    alerts = [_alert("ALT001", "warning", "2026-10-09T13:00:00", ["LOC001"])]
    assert get_alert_by_id("ALT001", alerts).alert_id == "ALT001"
    assert get_alert_by_id("ALT999", alerts) is None
