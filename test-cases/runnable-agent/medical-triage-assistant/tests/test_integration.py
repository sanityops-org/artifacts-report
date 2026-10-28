# tests/test_integration.py
"""End-to-end integration: from symptom description to registered closed loop (not dependent on LLM）。

String the process with two skill entrances, covering the integrated use cases and success standards in Section 12 of spec. 5。
"""

import shutil
from pathlib import Path

import pytest

from apis import session_api
from skills.registration.handler import run as registration
from skills.triage.handler import run as triage

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILES = (
    "departments.json",
    "doctors.json",
    "slots.json",
    "red_flag_rules.json",
    "symptom_department_map.json",
    "appointments.json",
)


def _all_keys(node) -> set:
    """Collect all key names recursively"""
    keys = set()
    if isinstance(node, dict):
        for key, value in node.items():
            keys.add(key)
            keys |= _all_keys(value)
    elif isinstance(node, list):
        for item in node:
            keys |= _all_keys(item)
    return keys


@pytest.fixture(autouse=True)
def _clean_sessions():
    session_api.reset_all()
    yield
    session_api.reset_all()


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Point the data directory of the four disk writing tools to the temporary copy to ensure that the integration test can be repeated."""
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


def _session() -> dict:
    """Open a new session"""
    return {"_session": {"session_id": session_api.create_session()["session_id"]}}


def _intake(session: dict, name: str, gender: str, age: int) -> None:
    """Register the complete patient information"""
    result = registration(
        "update_profile", {**session, "name": name, "gender": gender, "age": age}
    )
    assert result["status"] == "success"
    assert result["data"]["is_complete"] is True


def _slot_for(department_id: str, session: dict) -> dict:
    """Take the first registered source of this department"""
    result = registration("query_slots", {"department_id": department_id})
    assert result["status"] == "success"
    assert result["data"]["count"] > 0, f"{department_id} There is no source to register."
    return result["data"]["slots"][0]


def _query_slot(session: dict, slot: dict) -> dict:
    """Check the current balance of a source by date"""
    result = registration(
        "query_slots", {"department_id": slot["department_id"], "date": slot["date"]}
    )
    return next(s for s in result["data"]["slots"] if s["slot_id"] == slot["slot_id"])


# --- Red flag priority（B1）---

def test_red_flag_interrupts_the_whole_flow(sandbox):
    """When the red flag is hit, only the emergency guidance will be returned, and no department/number source/registration information will be generated."""
    result = triage("check_red_flags", {"text": "I suddenly had a terrible chest pain and sweated all over."})

    assert result["status"] == "success"
    assert result["data"]["hit"] is True
    assert result["data"]["action"] == "call_120_or_er"
    assert result["data"]["advice"]
    assert _all_keys(result) & {"department_id", "slot_id", "appointment_id"} == set()


def test_urgent_red_flag_also_interrupts(sandbox):
    """urgent The level red flag also interrupted the general triage."""
    result = triage("check_red_flags", {"text": "The child vomited twice after falling on the head."})

    assert result["data"]["hit"] is True
    assert result["data"]["action"] == "er_soon"


# --- Conventional triage link ---

def test_normal_flow_reaches_candidate_then_slots(sandbox):
    """Failed to hit the red flag → Candidate department → Department details → Number source"""
    shortlist = triage("shortlist_departments", {"symptoms": ["Fever", "Cough"]})

    assert shortlist["status"] == "success"
    assert shortlist["data"]["age_rule_applied"] is False
    department_id = shortlist["data"]["candidates"][0]["department_id"]
    assert department_id == "dept_general_internal"

    detail = triage("query_department", {"department_id": department_id})
    assert detail["status"] == "success"
    assert detail["data"]["location"]
    assert detail["data"]["preparation"]

    assert registration("query_slots", {"department_id": department_id})["data"]["count"] > 0


def test_fallback_department_is_actually_bookable(sandbox):
    """The bottom department is not a short promise: the fallback pointed to by the red line 3 must really be able to register."""
    shortlist = triage("shortlist_departments", {"symptoms": ["I feel weak all over."]})

    assert shortlist["data"]["candidates"] == []
    fallback = shortlist["data"]["fallback_department"]
    assert fallback == "dept_general_internal"

    detail = triage("query_department", {"department_id": fallback})
    assert detail["status"] == "success"
    assert registration("query_slots", {"department_id": fallback})["data"]["count"] > 0


def test_pediatric_patient_is_routed_then_books(sandbox):
    """After the pediatric rules take effect, you can still go through the full registration (end-to-end version of Success Standard 4)"""
    shortlist = triage("shortlist_departments", {"symptoms": ["Fever", "Cough"], "age": 8})
    assert [c["department_id"] for c in shortlist["data"]["candidates"]] == ["dept_pediatrics"]
    assert shortlist["data"]["age_rule_applied"] is True

    session = _session()
    _intake(session, "Li Xiaoming", "male", 8)
    slot = _slot_for("dept_pediatrics", session)

    booked = registration("create_appointment", {**session, "slot_id": slot["slot_id"]})

    assert booked["status"] == "success"
    assert booked["data"]["patient_name"] == "Li Xiaoming"
    assert booked["data"]["hint"]


# --- Registered closed-loop (success standard 5）---

def test_full_appointment_loop(sandbox):
    """Check the number source → register → balance -1 → repeated rejection → query → cancel → balance rollback"""
    session = _session()
    _intake(session, "Li Wei", "male", 32)

    # 1. Check the source of the number
    slot = _slot_for("dept_general_internal", session)
    initial_remaining = slot["remaining"]
    assert initial_remaining >= 2, "The initial margin is too small to verify the deduction and rollback."

    # 2. Register
    created = registration("create_appointment", {**session, "slot_id": slot["slot_id"]})
    assert created["status"] == "success"
    appointment_id = created["data"]["appointment_id"]
    assert created["data"]["remaining_after"] == initial_remaining - 1

    # 3. Surplus -1
    assert _query_slot(session, slot)["remaining"] == initial_remaining - 1

    # 4. Repeated registration is rejected
    duplicate = registration("create_appointment", {**session, "slot_id": slot["slot_id"]})
    assert duplicate["status"] == "error"
    assert "Repeated registration" in duplicate["error"]
    assert _query_slot(session, slot)["remaining"] == initial_remaining - 1

    # 5. Inquire about the registration
    listed = registration("query_appointment", dict(session))
    assert [a["appointment_id"] for a in listed["data"]["appointments"]] == [appointment_id]
    assert listed["data"]["appointments"][0]["status"] == "booked"

    # 6. Cancel
    cancelled = registration(
        "cancel_appointment", {**session, "appointment_id": appointment_id}
    )
    assert cancelled["status"] == "success"
    assert cancelled["data"]["status"] == "cancelled"
    assert cancelled["data"]["remaining_after"] == initial_remaining

    # 7. The margin rolls back
    assert _query_slot(session, slot)["remaining"] == initial_remaining

    # 8. The record is transferred to cancelled, and it is not physically deleted.
    final = registration("query_appointment", {**session, "appointment_id": appointment_id})
    assert final["data"]["count"] == 1
    assert final["data"]["appointments"][0]["status"] == "cancelled"
    assert final["data"]["appointments"][0]["cancelled_at"]


def test_loop_is_repeatable_on_a_fresh_data_copy(sandbox):
    """The complete process can be repeated in the same sandbox (the number source can be hung up again after cancellation)"""
    session = _session()
    _intake(session, "Li Wei", "male", 32)
    slot = _slot_for("dept_general_internal", session)

    first = registration("create_appointment", {**session, "slot_id": slot["slot_id"]})
    registration("cancel_appointment", {**session, "appointment_id": first["data"]["appointment_id"]})
    second = registration("create_appointment", {**session, "slot_id": slot["slot_id"]})

    assert second["status"] == "success"
    assert second["data"]["appointment_id"] != first["data"]["appointment_id"]
    assert _query_slot(session, slot)["remaining"] == slot["remaining"] - 1


def test_two_patients_share_a_slot_without_shadowing_each_other(sandbox):
    """Two sessions hang on the same source: each can only see their own records (registered attribution)"""
    slot_owner = _session()
    _intake(slot_owner, "Li Wei", "male", 32)
    slot = _slot_for("dept_general_internal", slot_owner)

    other = _session()
    _intake(other, "Wang Fang", "female", 30)

    first = registration("create_appointment", {**slot_owner, "slot_id": slot["slot_id"]})
    second = registration("create_appointment", {**other, "slot_id": slot["slot_id"]})

    assert first["status"] == "success"
    assert second["status"] == "success"
    assert first["data"]["appointment_id"] != second["data"]["appointment_id"]
    assert _query_slot(slot_owner, slot)["remaining"] == slot["remaining"] - 2

    assert [
        a["appointment_id"]
        for a in registration("query_appointment", dict(slot_owner))["data"]["appointments"]
    ] == [first["data"]["appointment_id"]]
    assert [
        a["appointment_id"]
        for a in registration("query_appointment", dict(other))["data"]["appointments"]
    ] == [second["data"]["appointment_id"]]
