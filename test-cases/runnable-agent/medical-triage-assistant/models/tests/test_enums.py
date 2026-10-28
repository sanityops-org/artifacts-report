"""Enumeration value test."""

import pytest

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


@pytest.mark.parametrize(
    "member,expected",
    [
        (DepartmentCategory.INTERNAL, "internal"),
        (DepartmentCategory.SURGICAL, "surgical"),
        (DepartmentCategory.SPECIALTY, "specialty"),
        (DepartmentCategory.EMERGENCY, "emergency"),
    ],
)
def test_department_category_values(member, expected):
    """Department category take value"""
    assert member.value == expected


@pytest.mark.parametrize(
    "member,expected",
    [
        (DoctorTitle.CHIEF, "chief"),
        (DoctorTitle.ASSOCIATE_CHIEF, "associate_chief"),
        (DoctorTitle.ATTENDING, "attending"),
    ],
)
def test_doctor_title_values(member, expected):
    """Doctor's title value"""
    assert member.value == expected


def test_slot_period_values():
    """Take the value of the period"""
    assert SlotPeriod.MORNING.value == "morning"
    assert SlotPeriod.AFTERNOON.value == "afternoon"


def test_slot_status_values():
    """Number source status take value"""
    assert SlotStatus.AVAILABLE.value == "available"
    assert SlotStatus.FULL.value == "full"
    assert SlotStatus.CLOSED.value == "closed"


def test_appointment_status_values():
    """Register the status to get the value"""
    assert AppointmentStatus.BOOKED.value == "booked"
    assert AppointmentStatus.CANCELLED.value == "cancelled"
    assert AppointmentStatus.COMPLETED.value == "completed"


def test_gender_values():
    """Gender value"""
    assert Gender.MALE.value == "male"
    assert Gender.FEMALE.value == "female"


def test_red_flag_level_values():
    """Red flag severity value"""
    assert RedFlagLevel.EMERGENCY.value == "emergency"
    assert RedFlagLevel.URGENT.value == "urgent"


def test_red_flag_action_values():
    """Red flag disposal action take value"""
    assert RedFlagAction.CALL_120_OR_ER.value == "call_120_or_er"
    assert RedFlagAction.ER_SOON.value == "er_soon"
