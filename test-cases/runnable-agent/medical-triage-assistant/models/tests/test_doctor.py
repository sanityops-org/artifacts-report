"""Doctor model test."""

import pytest
from pydantic import ValidationError

from models.doctor import Doctor
from models.enums import DoctorTitle


def _doctor(**overrides) -> dict:
    data = {
        "doctor_id": "DR001",
        "name": "Zhang Ming",
        "title": "chief",
        "department_id": "dept_neurology",
        "specialties": ["Headache", "Dizziness"],
        "clinic_days": ["Monday", "Thursday"],
    }
    data.update(overrides)
    return data


def test_valid_doctor():
    """Legal doctors can construct"""
    doctor = Doctor.model_validate(_doctor())

    assert doctor.doctor_id == "DR001"
    assert doctor.title == DoctorTitle.CHIEF
    assert doctor.specialties == ["Headache", "Dizziness"]


def test_doctor_id_is_uppercased_and_trimmed():
    """doctor_id Unify the blank space and capitalization"""
    assert Doctor.model_validate(_doctor(doctor_id=" dr001 ")).doctor_id == "DR001"


@pytest.mark.parametrize("bad_id", ["DR1", "DR0001", "X001", "doctor001"])
def test_invalid_doctor_id_rejected(bad_id):
    """Illegal doctor_id was rejected"""
    with pytest.raises(ValidationError):
        Doctor.model_validate(_doctor(doctor_id=bad_id))


def test_invalid_title_rejected():
    """Illegal titles are rejected"""
    with pytest.raises(ValidationError):
        Doctor.model_validate(_doctor(title="Professor"))


@pytest.mark.parametrize("bad_day", ["Funday", "Monday0", "Tuesday0"])
def test_invalid_clinic_day_rejected(bad_day):
    """Illegal medical appointment day was rejected."""
    with pytest.raises(ValidationError):
        Doctor.model_validate(_doctor(clinic_days=[bad_day]))


def test_empty_specialties_rejected():
    """specialties Can't be empty"""
    with pytest.raises(ValidationError):
        Doctor.model_validate(_doctor(specialties=[]))
