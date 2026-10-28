"""
alert_engine: Alert filtering and severity ranking.
"""

from models import Alert
from models.enums import AlertSeverity, AlertStatus

# Severity ranking: lower number is more urgent
_SEVERITY_RANK = {
    AlertSeverity.WARNING: 1,
    AlertSeverity.WATCH: 2,
    AlertSeverity.ADVISORY: 3,
}


def get_active_alerts(
    location_id: str | None,
    alerts: list[Alert]
) -> list[Alert]:
    """
    Get active alerts, optionally filtered to one location.

    Args:
        location_id: Optional location filter
        alerts: All alerts

    Returns:
        Active alerts ordered by severity (warning, watch, advisory), then by
        effective_time ascending within the same severity
    """
    active = [a for a in alerts if a.status == AlertStatus.ACTIVE]

    if location_id:
        active = [a for a in active if location_id in a.location_ids]

    active.sort(key=lambda a: (_SEVERITY_RANK[a.severity], a.effective_time))

    return active


def get_alert_by_id(alert_id: str, alerts: list[Alert]) -> Alert | None:
    """Get an alert by its ID"""
    for alert in alerts:
        if alert.alert_id == alert_id:
            return alert
    return None


__all__ = ["get_active_alerts", "get_alert_by_id"]
