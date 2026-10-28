"""Domain enumeration definition."""

from enum import Enum


class DepartmentCategory(str, Enum):
    """Department category"""

    INTERNAL = "internal"      # Internal medicine system
    SURGICAL = "surgical"      # Surgical system
    SPECIALTY = "specialty"    # Specialized subject
    EMERGENCY = "emergency"    # Emergency treatment


class DoctorTitle(str, Enum):
    """Doctor's job title"""

    CHIEF = "chief"                    # Chief physician
    ASSOCIATE_CHIEF = "associate_chief"  # Deputy Chief Physician
    ATTENDING = "attending"            # Physician-in-charge


class SlotPeriod(str, Enum):
    """Number source time period"""

    MORNING = "morning"        # Morning
    AFTERNOON = "afternoon"    # Afternoon


class SlotStatus(str, Enum):
    """Number source status"""

    AVAILABLE = "available"    # Can be registered
    FULL = "full"              # It is full
    CLOSED = "closed"          # Stop receiving outpatients


class AppointmentStatus(str, Enum):
    """Registration status"""

    BOOKED = "booked"          # Registered
    CANCELLED = "cancelled"    # Canceled
    COMPLETED = "completed"    # Completed the medical treatment


class Gender(str, Enum):
    """Sex"""

    MALE = "male"              # Man
    FEMALE = "female"          # Woman


class RedFlagLevel(str, Enum):
    """The severity of red flag symptoms"""

    EMERGENCY = "emergency"    # Immediately 120 / Emergency
    URGENT = "urgent"          # As soon as possible to the emergency room for evaluation.


class RedFlagAction(str, Enum):
    """Red flag symptom disposal action"""

    CALL_120_OR_ER = "call_120_or_er"  # Call 120 immediately or go to the emergency room.
    ER_SOON = "er_soon"                # As soon as possible to the emergency room for evaluation.


__all__ = [
    "AppointmentStatus",
    "DepartmentCategory",
    "DoctorTitle",
    "Gender",
    "RedFlagAction",
    "RedFlagLevel",
    "SlotPeriod",
    "SlotStatus",
]
