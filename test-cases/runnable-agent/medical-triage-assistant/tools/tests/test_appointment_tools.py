"""Registration tool test.

The test points the project_root of the tool module to the temporary directory (sandbox) to avoid pollution. data/。
"""

import json
import shutil
from pathlib import Path

import pytest

from apis import session_api
from apis.data_store import DataStore
from tools.appointment_cancel import execute as cancel
from tools.appointment_create import execute as create
from tools.appointment_query import execute as query
from tools.appointment_query_slots import execute as query_slots

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILES = (
    "departments.json",
    "doctors.json",
    "slots.json",
    "red_flag_rules.json",
    "symptom_department_map.json",
    "appointments.json",
)


def _read(data_dir: Path, filename: str, key: str) -> list:
    payload = json.loads((data_dir / filename).read_text(encoding="utf-8"))
    return payload[key]


def _write(data_dir: Path, filename: str, key: str, items: list) -> None:
    (data_dir / filename).write_text(
        json.dumps({key: items}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@pytest.fixture(autouse=True)
def _clean_sessions():
    session_api.reset_all()
    yield
    session_api.reset_all()


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Point the data directory of the tool module to a temporary copy and return to the copy directory."""
    import tools.appointment_cancel as cancel_module
    import tools.appointment_create as create_module
    import tools.appointment_query as query_module
    import tools.appointment_query_slots as query_slots_module

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for name in DATA_FILES:
        shutil.copy(DATA_DIR / name, data_dir / name)

    for module in (
        cancel_module,
        create_module,
        query_module,
        query_slots_module,
    ):
        monkeypatch.setattr(module, "project_root", tmp_path)
    return data_dir


@pytest.fixture
def bookable(sandbox):
    """Choose a real registered number source from the sandbox data."""
    slots = _read(sandbox, "slots.json", "slots")
    return next(s for s in slots if s["status"] == "available" and s["remaining"] > 0)


def _session_with(patient_name: str | None, **fields) -> dict:
    """Build a session; do not register patients when patient_name is None"""
    session_id = session_api.create_session()["session_id"]
    if patient_name is not None:
        session_api.update_patient(session_id, name=patient_name, **fields)
    return {"_session": {"session_id": session_id}}


@pytest.fixture
def params():
    """Patient conversation parameters with complete information"""
    return _session_with("Li Wei", gender="male", age=32, phone="13800138000")


# --- appointment_query_slots ---

def test_query_slots_returns_only_bookable_slots(sandbox, bookable):
    """Only return the registered number source, and all of them belong to the department."""
    result = query_slots({"department_id": bookable["department_id"]})

    assert result["status"] == "success"
    slots = result["data"]["slots"]
    assert slots
    assert all(s["status"] == "available" and s["remaining"] > 0 for s in slots)
    assert all(s["department_id"] == bookable["department_id"] for s in slots)


def test_query_slots_includes_doctor_name(sandbox, bookable):
    """Each number source has the doctor's name and title, so that the patient can understand it."""
    result = query_slots({"department_id": bookable["department_id"]})

    first = result["data"]["slots"][0]
    assert first["doctor_name"]
    assert first["doctor_title"] in ("Chief Physician", "Deputy Chief Physician", "Attending Physician")


def test_query_slots_returns_department_name(sandbox, bookable):
    """The English display name of the department on the top floor"""
    result = query_slots({"department_id": bookable["department_id"]})

    assert result["data"]["department_name"]
    assert result["data"]["count"] == len(result["data"]["slots"])


def test_query_slots_filters_by_date(sandbox, bookable):
    """Filter by date"""
    result = query_slots(
        {"department_id": bookable["department_id"], "date": bookable["date"]}
    )

    assert result["data"]["slots"]
    assert all(s["date"] == bookable["date"] for s in result["data"]["slots"])


def test_query_slots_filters_by_period(sandbox, bookable):
    """Filter by time period"""
    result = query_slots(
        {"department_id": bookable["department_id"], "period": bookable["period"]}
    )

    assert result["data"]["slots"]
    assert all(s["period"] == bookable["period"] for s in result["data"]["slots"])


def test_query_slots_filters_by_doctor(sandbox, bookable):
    """Filter by doctor"""
    result = query_slots(
        {"department_id": bookable["department_id"], "doctor_id": bookable["doctor_id"]}
    )

    assert result["data"]["slots"]
    assert all(s["doctor_id"] == bookable["doctor_id"] for s in result["data"]["slots"])


def test_query_slots_unknown_date_returns_empty(sandbox, bookable):
    """Return an empty list when the date is outside the source table, instead of making up the source."""
    result = query_slots(
        {"department_id": bookable["department_id"], "date": "2027-01-01"}
    )

    assert result["status"] == "success"
    assert result["data"]["slots"] == []
    assert result["data"]["count"] == 0


def test_query_slots_excludes_full_slots(sandbox, bookable):
    """The number source with the remaining number of 0 does not appear in the registered list."""
    slots = _read(sandbox, "slots.json", "slots")
    for slot in slots:
        if slot["slot_id"] == bookable["slot_id"]:
            slot["remaining"] = 0
            slot["status"] = "full"
    _write(sandbox, "slots.json", "slots", slots)

    result = query_slots(
        {"department_id": bookable["department_id"], "date": bookable["date"]}
    )

    assert bookable["slot_id"] not in [s["slot_id"] for s in result["data"]["slots"]]


def test_query_slots_unknown_department_is_error(sandbox):
    """Unknown department returns an error"""
    result = query_slots({"department_id": "dept_not_exist"})

    assert result["status"] == "error"
    assert "dept_not_exist" in result["error"]


def test_query_slots_requires_department_id(sandbox):
    """Missing department_id return error message"""
    result = query_slots({})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: department_id"


def test_query_slots_is_read_only(sandbox, bookable):
    """Query does not occupy the number source, nor does it write documents."""
    before = (sandbox / "slots.json").read_text(encoding="utf-8")

    query_slots({"department_id": bookable["department_id"]})

    assert (sandbox / "slots.json").read_text(encoding="utf-8") == before


# --- appointment_create ---

def test_create_succeeds(sandbox, bookable, params):
    """Successful registration return registration number and consultation prompts"""
    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "success"
    assert result["data"]["appointment_id"].startswith("AP" + bookable["date"].replace("-", ""))
    assert result["data"]["patient_name"] == "Li Wei"
    assert result["data"]["slot_id"] == bookable["slot_id"]
    assert result["data"]["status"] == "booked"
    assert result["data"]["hint"]


def test_create_decrements_remaining(sandbox, bookable, params):
    """The remaining number after registration -1"""
    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["data"]["remaining_after"] == bookable["remaining"] - 1
    after = _read(sandbox, "slots.json", "slots")
    stored = next(s for s in after if s["slot_id"] == bookable["slot_id"])
    assert stored["remaining"] == bookable["remaining"] - 1


def test_create_marks_slot_full_when_last_seat_taken(sandbox, bookable, params):
    """When the remaining number is deducted to 0, the status is changed. full"""
    slots = _read(sandbox, "slots.json", "slots")
    for slot in slots:
        if slot["slot_id"] == bookable["slot_id"]:
            slot["remaining"] = 1
    _write(sandbox, "slots.json", "slots", slots)

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["data"]["remaining_after"] == 0
    after = _read(sandbox, "slots.json", "slots")
    stored = next(s for s in after if s["slot_id"] == bookable["slot_id"])
    assert stored["remaining"] == 0
    assert stored["status"] == "full"


def test_create_writes_appointment_record(sandbox, bookable, params):
    """Registered record landing"""
    result = create({**params, "slot_id": bookable["slot_id"]})

    records = _read(sandbox, "appointments.json", "appointments")
    assert len(records) == 1
    assert records[0]["appointment_id"] == result["data"]["appointment_id"]
    assert records[0]["status"] == "booked"
    assert records[0]["created_at"]
    assert records[0]["cancelled_at"] is None


def test_create_rejects_full_slot(sandbox, bookable, params):
    """Reject when the remaining number is 0 (success standard 5）"""
    slots = _read(sandbox, "slots.json", "slots")
    for slot in slots:
        if slot["slot_id"] == bookable["slot_id"]:
            slot["remaining"] = 0
            slot["status"] = "full"
    _write(sandbox, "slots.json", "slots", slots)

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert "full" in result["error"].lower()


def test_create_rejects_closed_slot(sandbox, bookable, params):
    """The source of the suspension number cannot be hung up."""
    slots = _read(sandbox, "slots.json", "slots")
    for slot in slots:
        if slot["slot_id"] == bookable["slot_id"]:
            slot["status"] = "closed"
    _write(sandbox, "slots.json", "slots", slots)

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert "closed" in result["error"]


def test_create_rejects_invented_slot_id(sandbox, params):
    """The fabricated slot_id was rejected and prompted to re-query."""
    result = create({**params, "slot_id": "SLOT-20260928-999"})

    assert result["status"] == "error"
    assert "SLOT-20260928-999" in result["error"]
    assert "number source does not exist" in result["error"].lower()


def test_create_rejects_incomplete_profile(sandbox, bookable):
    """When the patient's information is incomplete, which fields are rejected and returned?"""
    params = _session_with("Li Wei")

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert result["data"]["missing_fields"] == ["Gender", "Age"]


def test_create_rejects_missing_profile(sandbox, bookable):
    """Refuse to hang up when the patient is not registered"""
    params = _session_with(None)

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert result["data"]["missing_fields"] == ["Name", "Gender", "Age"]


def test_create_rejects_duplicate_booking(sandbox, bookable, params):
    """The same patient + the same department + repeated registration on the same date was rejected (success criteria 5）"""
    first = create({**params, "slot_id": bookable["slot_id"]})
    assert first["status"] == "success"

    second = create({**params, "slot_id": bookable["slot_id"]})

    assert second["status"] == "error"
    assert "Repeated registration" in second["error"]


def test_duplicate_rejection_has_no_side_effect(sandbox, bookable, params):
    """When repeated registration is rejected, the remaining number does not move and the record does not increase."""
    before = (sandbox / "slots.json").read_text(encoding="utf-8")
    create({**params, "slot_id": bookable["slot_id"]})
    after_first = (sandbox / "slots.json").read_text(encoding="utf-8")

    create({**params, "slot_id": bookable["slot_id"]})

    assert (sandbox / "slots.json").read_text(encoding="utf-8") == after_first
    assert (sandbox / "slots.json").read_text(encoding="utf-8") != before
    assert len(_read(sandbox, "appointments.json", "appointments")) == 1


def test_create_allows_same_day_other_department(sandbox, params):
    """It is not a duplication to hang in another department on the same day."""
    slots = _read(sandbox, "slots.json", "slots")
    by_date: dict = {}
    for slot in slots:
        if slot["status"] == "available" and slot["remaining"] > 0:
            by_date.setdefault(slot["date"], {})[slot["department_id"]] = slot
    pair = next(depts for depts in by_date.values() if len(depts) >= 2)
    two = list(pair.values())[:2]

    assert create({**params, "slot_id": two[0]["slot_id"]})["status"] == "success"
    assert create({**params, "slot_id": two[1]["slot_id"]})["status"] == "success"


def test_appointment_id_sequence_increments_per_date(sandbox, params):
    """The serial number of the second order increases on the same day"""
    slots = _read(sandbox, "slots.json", "slots")
    by_date: dict = {}
    for slot in slots:
        if slot["status"] == "available" and slot["remaining"] > 0:
            by_date.setdefault(slot["date"], {})[slot["department_id"]] = slot
    pair = next(depts for depts in by_date.values() if len(depts) >= 2)
    two = list(pair.values())[:2]

    first = create({**params, "slot_id": two[0]["slot_id"]})["data"]["appointment_id"]
    second = create({**params, "slot_id": two[1]["slot_id"]})["data"]["appointment_id"]

    prefix = "AP" + two[0]["date"].replace("-", "")
    assert first == f"{prefix}0001"
    assert second == f"{prefix}0002"


def test_appointment_id_sequence_does_not_reset_per_department(sandbox, params):
    """The serial number increases by date and has nothing to do with the department."""
    slots = _read(sandbox, "slots.json", "slots")
    by_date: dict = {}
    for slot in slots:
        if slot["status"] == "available" and slot["remaining"] > 0:
            by_date.setdefault(slot["date"], {})[slot["department_id"]] = slot
    pair = next(depts for depts in by_date.values() if len(depts) >= 2)
    two = list(pair.values())[:2]

    create({**params, "slot_id": two[0]["slot_id"]})
    second = create({**params, "slot_id": two[1]["slot_id"]})["data"]["appointment_id"]

    assert second.endswith("0002")
    assert second.startswith("AP" + two[0]["date"].replace("-", ""))


def test_create_rejects_invented_slot_has_no_side_effect(sandbox, params):
    """Do not move any file when the number source does not exist."""
    before = (sandbox / "slots.json").read_text(encoding="utf-8")

    create({**params, "slot_id": "SLOT-20260928-999"})

    assert (sandbox / "slots.json").read_text(encoding="utf-8") == before
    assert _read(sandbox, "appointments.json", "appointments") == []


def test_create_rolls_back_slot_when_appointment_write_fails(sandbox, bookable, params, monkeypatch):
    """Rollback number source when writing registered record failure: do not leave the occupied but unrecorded residual number (check first and write the atomicity)"""
    before = _read(sandbox, "slots.json", "slots")
    original = next(s for s in before if s["slot_id"] == bookable["slot_id"])

    def boom(self, items):
        raise OSError("Failed to simulate writing disk")

    # The second write (registered record) failed; the first write (number source) must be compensated and rolled back.
    monkeypatch.setattr(DataStore, "save_appointments", boom)

    result = create({**params, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    after = _read(sandbox, "slots.json", "slots")
    stored = next(s for s in after if s["slot_id"] == bookable["slot_id"])
    assert stored["remaining"] == original["remaining"]
    assert stored["status"] == original["status"]
    assert _read(sandbox, "appointments.json", "appointments") == []


def test_create_requires_slot_id(sandbox, params):
    """Missing slot_id returns error message"""
    result = create(dict(params))

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: slot_id"


def test_create_requires_session(sandbox, bookable):
    """Missing session message return error"""
    result = create({"slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert result["error"] == "Missing conversation information"


def test_create_unknown_session_is_an_error(sandbox, bookable):
    """Unknown session_id is converted into an error structure and does not throw an exception."""
    result = create({"_session": {"session_id": "SESS-NOTEXIST"}, "slot_id": bookable["slot_id"]})

    assert result["status"] == "error"
    assert "session" in result["error"].lower()


# --- appointment_query ---

def test_query_without_id_lists_session_appointments(sandbox, bookable, params):
    """List the registration record of this session when the registration number is not transmitted."""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = query(dict(params))

    assert result["status"] == "success"
    assert result["data"]["count"] == 1
    assert result["data"]["appointments"][0]["appointment_id"] == created["appointment_id"]


def test_query_without_records_returns_empty_list(sandbox, params):
    """No error will be reported when there is no registration, and an empty list will be returned."""
    result = query(dict(params))

    assert result["status"] == "success"
    assert result["data"]["appointments"] == []
    assert result["data"]["count"] == 0


def test_query_without_id_requires_profile(sandbox):
    """When the patient is not registered, the attribution cannot be determined, and the error is returned."""
    result = query(_session_with(None))

    assert result["status"] == "error"
    assert "patient" in result["error"].lower()


def test_query_is_scoped_to_current_patient(sandbox, bookable, params):
    """Other sessions cannot see the registration of the patient in this session (registration attribution)"""
    create({**params, "slot_id": bookable["slot_id"]})

    other = query(_session_with("Wang Fang", gender="female", age=30))

    assert other["status"] == "success"
    assert other["data"]["appointments"] == []


def test_query_by_id_returns_record(sandbox, bookable, params):
    """Check the order with the registration number"""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = query({**params, "appointment_id": created["appointment_id"]})

    assert result["data"]["count"] == 1
    record = result["data"]["appointments"][0]
    assert record["appointment_id"] == created["appointment_id"]
    assert record["patient_name"] == "Li Wei"
    assert record["department_id"] == bookable["department_id"]
    assert record["slot_id"] == bookable["slot_id"]
    assert record["status"] == "booked"


def test_query_by_id_works_from_another_session(sandbox, bookable, params):
    """The registration number itself is the query credentials, and you can still query the number when you change the session."""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = query({**_session_with(None), "appointment_id": created["appointment_id"]})

    assert result["status"] == "success"
    assert result["data"]["count"] == 1


def test_query_unknown_id_is_error(sandbox, params):
    """The registration number does not exist. Return error."""
    result = query({**params, "appointment_id": "AP202609280099"})

    assert result["status"] == "error"
    assert "AP202609280099" in result["error"]


def test_query_requires_session(sandbox):
    """Missing session message return error"""
    result = query({})

    assert result["status"] == "error"
    assert result["error"] == "Missing conversation information"


def test_query_is_read_only(sandbox, bookable, params):
    """Query without writing documents"""
    create({**params, "slot_id": bookable["slot_id"]})
    before = (sandbox / "appointments.json").read_text(encoding="utf-8")

    query(dict(params))

    assert (sandbox / "appointments.json").read_text(encoding="utf-8") == before


# --- appointment_cancel ---

def test_cancel_marks_record_cancelled(sandbox, bookable, params):
    """After cancellation, record to cancelled and record the cancellation time."""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = cancel({**params, "appointment_id": created["appointment_id"]})

    assert result["status"] == "success"
    assert result["data"]["status"] == "cancelled"
    assert result["data"]["cancelled_at"]
    records = _read(sandbox, "appointments.json", "appointments")
    assert records[0]["status"] == "cancelled"
    assert records[0]["cancelled_at"]


def test_cancel_restores_remaining(sandbox, bookable, params):
    """The remaining number after cancellation +1"""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = cancel({**params, "appointment_id": created["appointment_id"]})

    assert result["data"]["remaining_after"] == bookable["remaining"]
    stored = next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )
    assert stored["remaining"] == bookable["remaining"]


def test_cancel_returns_slot_to_initial_remaining(sandbox, bookable, params):
    """Register → Cancel the remaining number to return to the initial value (success standard 5）"""
    create({**params, "slot_id": bookable["slot_id"]})
    after_book = next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )
    assert after_book["remaining"] == bookable["remaining"] - 1

    cancel({**params, "appointment_id": _read(sandbox, "appointments.json", "appointments")[0]["appointment_id"]})

    final = next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )
    assert final["remaining"] == bookable["remaining"]


def test_cancel_reopens_full_slot(sandbox, bookable, params):
    """The whole account is canceled after it is full, and the number source returns to available"""
    slots = _read(sandbox, "slots.json", "slots")
    for slot in slots:
        if slot["slot_id"] == bookable["slot_id"]:
            slot["remaining"] = 1
    _write(sandbox, "slots.json", "slots", slots)

    created = create({**params, "slot_id": bookable["slot_id"]})["data"]
    assert next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )["status"] == "full"

    cancel({**params, "appointment_id": created["appointment_id"]})

    restored = next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )
    assert restored["status"] == "available"
    assert restored["remaining"] == 1


def test_cancelled_slot_is_bookable_again(sandbox, bookable, params):
    """After cancellation, the account source can be hung up again."""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]
    cancel({**params, "appointment_id": created["appointment_id"]})

    again = create({**params, "slot_id": bookable["slot_id"]})

    assert again["status"] == "success"
    assert again["data"]["appointment_id"] != created["appointment_id"]


def test_cancel_twice_is_error(sandbox, bookable, params):
    """Repeated cancellation returns an error, and no longer return the residual number (the canceled power fails)"""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]
    cancel({**params, "appointment_id": created["appointment_id"]})
    snapshot = (sandbox / "slots.json").read_text(encoding="utf-8")

    second = cancel({**params, "appointment_id": created["appointment_id"]})

    assert second["status"] == "error"
    assert "cancelled" in second["error"]
    assert (sandbox / "slots.json").read_text(encoding="utf-8") == snapshot


def test_cancel_unknown_id_is_error(sandbox, params):
    """The registration number does not exist. Return error."""
    result = cancel({**params, "appointment_id": "AP202609280099"})

    assert result["status"] == "error"
    assert "AP202609280099" in result["error"]


def test_cancel_other_patients_appointment_rejected(sandbox, bookable, params):
    """Can't cancel other people's registration (registration belongs)"""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]
    snapshot = (sandbox / "slots.json").read_text(encoding="utf-8")

    result = cancel(
        {**_session_with("Wang Fang", gender="female", age=30),
         "appointment_id": created["appointment_id"]}
    )

    assert result["status"] == "error"
    assert "patient" in result["error"].lower()
    assert (sandbox / "slots.json").read_text(encoding="utf-8") == snapshot


def test_cancel_requires_profile(sandbox, bookable, params):
    """When the session does not register the patient, the attribution cannot be verified, and the cancellation is refused."""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    result = cancel({**_session_with(None), "appointment_id": created["appointment_id"]})

    assert result["status"] == "error"
    assert "patient" in result["error"].lower()


def test_cancel_requires_appointment_id(sandbox, params):
    """Missing appointment_id returns a error message"""
    result = cancel(dict(params))

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: appointment_id"


def test_cancel_requires_session(sandbox):
    """Missing session message return error"""
    result = cancel({"appointment_id": "AP202609280001"})

    assert result["status"] == "error"
    assert result["error"] == "Missing conversation information"


def test_cancel_does_not_recycle_sequence_number(sandbox, params):
    """Cancellation does not recover the serial number: the second order on the same day is still 0002"""
    slots = _read(sandbox, "slots.json", "slots")
    by_date: dict = {}
    for slot in slots:
        if slot["status"] == "available" and slot["remaining"] > 0:
            by_date.setdefault(slot["date"], {})[slot["department_id"]] = slot
    pair = next(depts for depts in by_date.values() if len(depts) >= 2)
    two = list(pair.values())[:2]

    first = create({**params, "slot_id": two[0]["slot_id"]})["data"]
    cancel({**params, "appointment_id": first["appointment_id"]})
    second = create({**params, "slot_id": two[1]["slot_id"]})["data"]["appointment_id"]

    assert second == "AP" + two[0]["date"].replace("-", "") + "0002"


def test_cancel_leaves_other_slots_untouched(sandbox, bookable, params):
    """Only reply to the corresponding number source, and other number sources remain unchanged."""
    before = _read(sandbox, "slots.json", "slots")
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]
    cancel({**params, "appointment_id": created["appointment_id"]})

    after = _read(sandbox, "slots.json", "slots")

    assert after == before


def test_cancel_rolls_back_record_when_slot_write_fails(sandbox, bookable, params, monkeypatch):
    """Roll back the registration record when the replenishment number source fails: do not leave the intermediate state of the canceled but not replenished residual number (check first and then write the atomicity)"""
    created = create({**params, "slot_id": bookable["slot_id"]})["data"]

    def boom(self, items):
        raise OSError("Failed to simulate writing disk")

    # The second write (number source) failed; the first write (record transfer cancelled) must be compensated and rolled back.
    monkeypatch.setattr(DataStore, "save_slots", boom)

    result = cancel({**params, "appointment_id": created["appointment_id"]})

    assert result["status"] == "error"
    records = _read(sandbox, "appointments.json", "appointments")
    assert len(records) == 1
    assert records[0]["status"] == "booked"
    assert records[0]["cancelled_at"] is None
    stored = next(
        s for s in _read(sandbox, "slots.json", "slots") if s["slot_id"] == bookable["slot_id"]
    )
    assert stored["remaining"] == bookable["remaining"] - 1
