"""Data storage layer test."""

import json

import pytest

from apis.data_store import DataStore
from models.department import Department
from models.enums import SlotStatus
from models.slot import Slot


def _department(department_id: str = "dept_neurology") -> Department:
    return Department(
        department_id=department_id,
        name="Neurology",
        category="internal",
        description="Diagnosis and treatment of headache, dizziness and other neurological diseases.",
        location="Area C, 4th Floor, Outpatient Building",
    )


def _slot(slot_id: str = "SLOT-20260928-001", remaining: int = 5) -> Slot:
    return Slot(
        slot_id=slot_id,
        department_id="dept_neurology",
        doctor_id="DR001",
        date="2026-09-28",
        period="morning",
        start_time="08:30",
        end_time="09:00",
        capacity=10,
        remaining=remaining,
        status=SlotStatus.AVAILABLE,
    )


def test_missing_file_returns_empty_list(tmp_path):
    """Return an empty list when the file does not exist"""
    store = DataStore(data_dir=tmp_path)

    assert store.load_departments() == []
    assert store.load_slots() == []
    assert store.load_appointments() == []
    assert store.load_red_flag_rules() == []
    assert store.load_symptom_map() == []


def test_missing_key_returns_empty_list(tmp_path):
    """Return an empty list when the file exists but the key is missing."""
    (tmp_path / "departments.json").write_text("{}", encoding="utf-8")

    assert DataStore(data_dir=tmp_path).load_departments() == []


def test_empty_array_returns_empty_list(tmp_path):
    """Return an empty list when the key exists but the array is empty."""
    (tmp_path / "departments.json").write_text('{"departments": []}', encoding="utf-8")

    assert DataStore(data_dir=tmp_path).load_departments() == []


def test_non_dict_top_level_raises(tmp_path):
    """Throw when the top layer is not an object. ValueError"""
    (tmp_path / "departments.json").write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        DataStore(data_dir=tmp_path).load_departments()


def test_non_list_key_raises(tmp_path):
    """Throw when the key is not pointing to the array. ValueError"""
    (tmp_path / "departments.json").write_text('{"departments": {}}', encoding="utf-8")

    with pytest.raises(ValueError):
        DataStore(data_dir=tmp_path).load_departments()


def test_save_then_load_roundtrip(tmp_path):
    """After writing, the reading is consistent, and the fall plate is UTF-8. non-ASCII characters are not escaped."""
    store = DataStore(data_dir=tmp_path)
    store.save_departments([_department()])

    loaded = store.load_departments()
    assert len(loaded) == 1
    assert loaded[0].name == "Neurology"

    raw_text = (tmp_path / "departments.json").read_text(encoding="utf-8")
    assert "Neurology" in raw_text
    assert json.loads(raw_text)["departments"][0]["category"] == "internal"


def test_save_creates_nested_data_dir(tmp_path):
    """Automatically create when the data directory does not exist"""
    target = tmp_path / "nested" / "data"

    DataStore(data_dir=target).save_departments([_department()])

    assert (target / "departments.json").exists()


def test_slot_roundtrip_preserves_remaining(tmp_path):
    """After writing the number source, read to keep the residual number and status."""
    store = DataStore(data_dir=tmp_path)
    store.save_slots([_slot(remaining=0)])

    loaded = store.load_slots()
    assert loaded[0].remaining == 0
    assert loaded[0].capacity == 10


def test_raw_list_roundtrip(tmp_path):
    """Rules and mappings are read back in the form of original dict."""
    payload = {
        "rules": [
            {
                "rule_id": "RF001",
                "name": "Chest pain",
                "level": "emergency",
                "action": "call_120_or_er",
                "advice": "Please call immediately. 120。",
                "keywords": ["Chest pain"],
            }
        ]
    }
    (tmp_path / "red_flag_rules.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )

    rules = DataStore(data_dir=tmp_path).load_red_flag_rules()
    assert rules[0]["rule_id"] == "RF001"
    assert rules[0]["keywords"] == ["Chest pain"]
