"""Enumerations for energy management domain."""

from enum import Enum


class FacilityType(str, Enum):
    """Facility type classification."""
    MANUFACTURING = "manufacturing"
    OFFICE = "office"
    WAREHOUSE = "warehouse"
    DATA_CENTER = "data_center"
    LABORATORY = "laboratory"
    RETAIL = "retail"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"


class EquipmentType(str, Enum):
    """Equipment type classification."""
    HVAC = "hvac"
    LIGHTING = "lighting"
    MACHINERY = "machinery"
    COMPUTING = "computing"
    PROCESS = "process"
    OTHER = "other"


class EnergySource(str, Enum):
    """Energy source types."""
    ELECTRICITY_GRID = "electricity_grid"
    NATURAL_GAS = "natural_gas"
    DIESEL = "diesel"
    SOLAR = "solar"
    WIND = "wind"
    OTHER = "other"


class Priority(str, Enum):
    """Recommendation priority levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Confidence(str, Enum):
    """Confidence levels for estimates."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RenewableType(str, Enum):
    """Renewable energy types."""
    SOLAR = "solar"
    WIND = "wind"
    STORAGE = "storage"


class AnomalySeverity(str, Enum):
    """Anomaly severity levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"