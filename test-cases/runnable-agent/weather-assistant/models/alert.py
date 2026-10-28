"""
Severe weather alert model.
"""

from pydantic import BaseModel, Field

from models.enums import AlertSeverity, AlertStatus


class Alert(BaseModel):
    """Severe weather alert"""
    alert_id: str = Field(..., pattern=r"^ALT\d{3}$", description="Alert ID")
    event: str = Field(..., min_length=5, description="Event type, e.g. Tornado Warning")
    severity: AlertSeverity = Field(..., description="Severity level")
    headline: str = Field(..., min_length=10, description="Alert headline")
    description: str = Field(..., min_length=20, description="Full alert description")
    areas_affected: list[str] = Field(..., min_length=1, description="Affected areas")
    effective_time: str = Field(..., description="Alert effective time (ISO 8601)")
    expires_time: str = Field(..., description="Alert expiration time (ISO 8601)")
    location_ids: list[str] = Field(..., min_length=1, description="Affected location IDs")
    status: AlertStatus = Field(default=AlertStatus.ACTIVE, description="Alert status")


__all__ = ["Alert"]
