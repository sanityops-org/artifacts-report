"""The domain model is exported uniformly."""

from models.appointment import Appointment
from models.department import Department
from models.doctor import Doctor
from models.enums import (
    AppointmentStatus,
    DepartmentCategory,
    DoctorTitle,
    Gender,
    RedFlagAction,
    RedFlagLevel,
    SlotPeriod,
    SlotStatus,
)
from models.patient import PatientProfile
from models.slot import Slot

__all__ = [
    # Enumeration type
    "AppointmentStatus",
    "DepartmentCategory",
    "DoctorTitle",
    "Gender",
    "RedFlagAction",
    "RedFlagLevel",
    "SlotPeriod",
    "SlotStatus",
    # Data model
    "Appointment",
    "Department",
    "Doctor",
    "PatientProfile",
    "Slot",
]
