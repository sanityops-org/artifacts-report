"""Built-in simulation data integrity and self-consistency test."""

from datetime import date
from pathlib import Path

import pytest

from apis.data_store import DataStore

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
EXPECTED_DATES = ["2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02"]


@pytest.fixture(scope="module")
def store() -> DataStore:
    return DataStore(data_dir=DATA_DIR)


@pytest.fixture(scope="module")
def departments(store):
    return store.load_departments()


@pytest.fixture(scope="module")
def doctors(store):
    return store.load_doctors()


@pytest.fixture(scope="module")
def slots(store):
    return store.load_slots()


def test_all_data_files_exist():
    """6 Data files are complete"""
    for filename in (
        "departments.json",
        "doctors.json",
        "slots.json",
        "red_flag_rules.json",
        "symptom_department_map.json",
        "appointments.json",
    ):
        assert (DATA_DIR / filename).exists(), f"Missing data files {filename}"


def test_twelve_departments_with_unique_ids(departments):
    """12 Department, the identification is unique"""
    assert len(departments) == 12
    ids = [d.department_id for d in departments]
    assert len(set(ids)) == 12
    assert "dept_general_internal" in ids
    assert "dept_pediatrics" in ids
    assert "dept_emergency" in ids


def test_every_department_has_preparation(departments):
    """Each department has pre-treatment preparation tips."""
    for dept in departments:
        assert dept.preparation, f"{dept.department_id} Lack preparation"


def test_twenty_four_doctors_two_per_department(doctors, departments):
    """24 Famous doctors, 2 in each department, the department's quotation is valid"""
    assert len(doctors) == 24
    dept_ids = {d.department_id for d in departments}
    for doctor in doctors:
        assert doctor.department_id in dept_ids
    per_dept = {}
    for doctor in doctors:
        per_dept[doctor.department_id] = per_dept.get(doctor.department_id, 0) + 1
    assert set(per_dept) == dept_ids
    assert set(per_dept.values()) == {2}


def test_slot_count_and_doctor_pairing(slots, doctors):
    """240 Number source = 5 working days × 2 periods × 24 doctors"""
    assert len(slots) == 240
    doctor_ids = {d.doctor_id for d in doctors}
    slot_ids = [s.slot_id for s in slots]
    assert len(set(slot_ids)) == 240
    per_doctor = {}
    for slot in slots:
        assert slot.doctor_id in doctor_ids
        per_doctor[slot.doctor_id] = per_doctor.get(slot.doctor_id, 0) + 1
    assert set(per_doctor) == doctor_ids
    assert set(per_doctor.values()) == {10}


def test_slot_dates_are_exactly_the_five_weekdays(slots):
    """The source date is exactly 5 working days."""
    assert sorted({s.date for s in slots}) == EXPECTED_DATES
    for value in EXPECTED_DATES:
        assert date.fromisoformat(value).weekday() < 5


def test_slot_department_matches_doctor_department(slots, doctors):
    """The department of the number source is the same as the department of the visiting doctor."""
    dept_of = {d.doctor_id: d.department_id for d in doctors}
    for slot in slots:
        assert slot.department_id == dept_of[slot.doctor_id], slot.slot_id


def test_slot_date_falls_on_doctor_clinic_day(slots, doctors):
    """The source date falls on the doctor's appointment date."""
    clinic_days = {d.doctor_id: set(d.clinic_days) for d in doctors}
    for slot in slots:
        weekday = WEEKDAY_NAMES[date.fromisoformat(slot.date).weekday()]
        assert weekday in clinic_days[slot.doctor_id], f"{slot.slot_id} Not on the day of consultation"


def test_slots_start_available_with_full_remaining(slots):
    """The initial state of the number source is available, the remaining number is equal to the total number, and the total number is 8~20"""
    for slot in slots:
        assert slot.status.value == "available"
        assert slot.remaining == slot.capacity
        assert 8 <= slot.capacity <= 20


def test_ten_red_flag_rules_are_well_formed(store):
    """10 Red flag rules, complete fields and severity match the disposal action"""
    rules = store.load_red_flag_rules()
    assert len(rules) == 10
    expected_actions = {"emergency": "call_120_or_er", "urgent": "er_soon"}
    assert len({r["rule_id"] for r in rules}) == 10
    for rule in rules:
        for key in ("rule_id", "name", "level", "action", "advice", "keywords"):
            assert key in rule, f"{rule.get('rule_id')} Lack {key}"
        assert rule["level"] in expected_actions
        assert rule["action"] == expected_actions[rule["level"]]
        assert rule["keywords"], f"{rule['rule_id']} The keyword is empty."
        assert all(isinstance(kw, str) and kw for kw in rule["keywords"])


def test_sixteen_symptom_mappings_are_well_formed(store, departments):
    """16 The symptom mapping, the department's reference is valid, and the weight is 1~3"""
    mappings = store.load_symptom_map()
    assert len(mappings) == 16
    dept_ids = {d.department_id for d in departments}
    for mapping in mappings:
        assert mapping["symptom"]
        assert mapping["aliases"]
        assert mapping["departments"], f"{mapping['symptom']} Departments not mapped"
        assert 1 <= mapping["weight"] <= 3
        for dept_id in mapping["departments"]:
            assert dept_id in dept_ids, f"{mapping['symptom']} Point to the unknown department {dept_id}"


def test_appointments_start_empty(store):
    """The registration record is initially empty."""
    assert store.load_appointments() == []
