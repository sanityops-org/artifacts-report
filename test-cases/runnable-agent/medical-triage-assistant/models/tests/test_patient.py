"""Patient model test."""

import pytest
from pydantic import ValidationError

from models.enums import Gender
from models.patient import PatientProfile


def test_empty_profile_is_incomplete():
    """The empty file is incomplete and three items are missing."""
    profile = PatientProfile()

    assert profile.is_complete is False
    assert profile.missing_fields == ["Name", "Gender", "Age"]


def test_full_profile_is_complete():
    """Name + gender + age is complete"""
    profile = PatientProfile(name="Li Wei", gender="male", age=32)

    assert profile.is_complete is True
    assert profile.missing_fields == []
    assert profile.gender == Gender.MALE


def test_phone_is_optional():
    """The mobile phone number is optional, which does not affect the integrity."""
    profile = PatientProfile(name="Li Wei", gender="male", age=32, phone="13800138000")

    assert profile.is_complete is True
    assert profile.phone == "13800138000"


def test_partial_profile_reports_exact_missing_fields():
    """Only report age when there is a lack of age."""
    profile = PatientProfile(name="Li Wei", gender="male")

    assert profile.is_complete is False
    assert profile.missing_fields == ["Age"]


def test_name_is_stripped():
    """The name is blank before and after"""
    assert PatientProfile(name="  Li Wei ").name == "Li Wei"


def test_empty_name_is_treated_as_absent():
    """Pure blank names are considered to be unfilled."""
    profile = PatientProfile(name="   ")

    assert profile.name is None
    assert "Name" in profile.missing_fields


@pytest.mark.parametrize("bad_phone", ["1380013800", "23800138000", "138-0013-8000", "abcdefghijk"])
def test_invalid_phone_rejected(bad_phone):
    """Illegal mobile phone numbers are rejected"""
    with pytest.raises(ValidationError):
        PatientProfile(phone=bad_phone)


@pytest.mark.parametrize("bad_age", [-1, 121])
def test_age_out_of_range_rejected(bad_age):
    """Rejected if the age exceeds 0~120"""
    with pytest.raises(ValidationError):
        PatientProfile(age=bad_age)


def test_zero_age_is_allowed():
    """0 Age (babies under one year old) legal"""
    assert PatientProfile(name="Baby", gender="female", age=0).is_complete is True


def test_models_package_reexports_everything():
    """models Package unified and then export all enumerations and models"""
    import models

    for name in (
        "Appointment",
        "AppointmentStatus",
        "Department",
        "DepartmentCategory",
        "Doctor",
        "DoctorTitle",
        "Gender",
        "PatientProfile",
        "RedFlagAction",
        "RedFlagLevel",
        "Slot",
        "SlotPeriod",
        "SlotStatus",
    ):
        assert hasattr(models, name), f"models Not exported {name}"
