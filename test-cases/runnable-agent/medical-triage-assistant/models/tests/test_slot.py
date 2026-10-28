"""Number source model test."""

import pytest
from pydantic import ValidationError

from models.enums import SlotPeriod, SlotStatus
from models.slot import Slot


def _slot(**overrides) -> dict:
    data = {
        "slot_id": "SLOT-20260928-001",
        "department_id": "dept_neurology",
        "doctor_id": "DR001",
        "date": "2026-09-28",
        "period": "morning",
        "start_time": "08:30",
        "end_time": "09:00",
        "capacity": 10,
        "remaining": 10,
        "status": "available",
    }
    data.update(overrides)
    return data


def test_valid_slot():
    """The legal number source can be constructed"""
    slot = Slot.model_validate(_slot())

    assert slot.slot_id == "SLOT-20260928-001"
    assert slot.period == SlotPeriod.MORNING
    assert slot.status == SlotStatus.AVAILABLE
    assert slot.remaining == 10


@pytest.mark.parametrize(
    "bad_id",
    ["SLOT-2026092-001", "SLOT-20260928-1", "20260928-001", "slot-20260928-001"],
)
def test_invalid_slot_id_rejected(bad_id):
    """Illegal slot_id was rejected"""
    with pytest.raises(ValidationError):
        Slot.model_validate(_slot(slot_id=bad_id))


@pytest.mark.parametrize("bad_date", ["2026/09/28", "20260928", "2026-9-28", "26-09-28"])
def test_invalid_date_rejected(bad_date):
    """Illegal dates are rejected"""
    with pytest.raises(ValidationError):
        Slot.model_validate(_slot(date=bad_date))


def test_remaining_greater_than_capacity_rejected():
    """remaining Can't be greater than capacity"""
    with pytest.raises(ValidationError):
        Slot.model_validate(_slot(capacity=5, remaining=6))


def test_negative_remaining_rejected():
    """remaining Can't be negative"""
    with pytest.raises(ValidationError):
        Slot.model_validate(_slot(remaining=-1))


def test_zero_remaining_is_allowed():
    """remaining It can be 0 (full)"""
    slot = Slot.model_validate(_slot(remaining=0, status="full"))

    assert slot.remaining == 0
    assert slot.status == SlotStatus.FULL


def test_invalid_period_rejected():
    """Illegal time period is rejected"""
    with pytest.raises(ValidationError):
        Slot.model_validate(_slot(period="evening"))
