# skills/registration/tests/test_handler.py
"""Register to make an appointment for the Handler test of skills."""

import json
import shutil
from pathlib import Path

import pytest

from apis import session_api
from skills.registration.handler import run

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
DATA_FILES = (
    "departments.json",
    "doctors.json",
    "slots.json",
    "red_flag_rules.json",
    "symptom_department_map.json",
    "appointments.json",
)


@pytest.fixture(autouse=True)
def _clean_sessions():
    session_api.reset_all()
    yield
    session_api.reset_all()


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Point the data directory of the four disk writing tools to the temporary copy"""
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
def session_params():
    """Conversation parameters of the patient who has not been registered"""
    session_id = session_api.create_session()["session_id"]
    return {"_session": {"session_id": session_id}}


def _bookable(data_dir: Path) -> dict:
    slots = json.loads((data_dir / "slots.json").read_text(encoding="utf-8"))["slots"]
    return next(s for s in slots if s["status"] == "available" and s["remaining"] > 0)


def test_unknown_intent_lists_available_intents(sandbox):
    """Unknown intent returns a list of available intentions"""
    result = run("no_such_intent", {})

    assert result["status"] == "error"
    assert "Unknown operation: no_such_intent" in result["error"]
    for intent in (
        "update_profile",
        "get_profile",
        "query_slots",
        "create_appointment",
        "query_appointment",
        "cancel_appointment",
    ):
        assert intent in result["error"]


def test_empty_intent_is_error(sandbox):
    """Empty intent returns an error"""
    result = run("", {})

    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]


def test_update_profile_intent_routes(sandbox):
    """update_profile The intention is to route to the patient to write"""
    session_id = session_api.create_session()["session_id"]

    result = run("update_profile", {"_session": {"session_id": session_id}, "name": "Li Wei"})

    assert result["status"] == "success"
    assert result["data"]["name"] == "Li Wei"
    assert result["data"]["missing_fields"] == ["Gender", "Age"]


def test_get_profile_intent_routes(sandbox):
    """get_profile The intention is to route to the patient to read."""
    session_id = session_api.create_session()["session_id"]

    result = run("get_profile", {"_session": {"session_id": session_id}})

    assert result["status"] == "success"
    assert result["data"]["is_complete"] is False


def test_query_slots_intent_routes(sandbox):
    """query_slots Intention route to the number source query"""
    slot = _bookable(sandbox)

    result = run("query_slots", {"department_id": slot["department_id"]})

    assert result["status"] == "success"
    assert result["data"]["slots"]


def test_full_appointment_lifecycle_through_the_skill(sandbox):
    """Go to the skill entrance to complete registration → query → cancel closed loop"""
    slot = _bookable(sandbox)
    session_id = session_api.create_session()["session_id"]
    session = {"_session": {"session_id": session_id}}

    assert run("update_profile", {**session, "name": "Li Wei", "gender": "male", "age": 32})[
        "status"
    ] == "success"
    created = run("create_appointment", {**session, "slot_id": slot["slot_id"]})
    assert created["status"] == "success"
    appointment_id = created["data"]["appointment_id"]

    listed = run("query_appointment", dict(session))
    assert listed["data"]["count"] == 1

    cancelled = run("cancel_appointment", {**session, "appointment_id": appointment_id})
    assert cancelled["status"] == "success"
    assert cancelled["data"]["remaining_after"] == slot["remaining"]


def test_create_appointment_requires_profile(sandbox, session_params):
    """Registration fails when the information is incomplete, and the error points to the missing field."""
    slot = _bookable(sandbox)

    result = run("create_appointment", {**session_params, "slot_id": slot["slot_id"]})

    assert result["status"] == "error"
    assert result["data"]["missing_fields"] == ["Name", "Gender", "Age"]


def test_skill_directory_is_colocated_with_its_skill_md():
    """SKILL.md The same directory as handler.py for SkillManager to scan"""
    skill_dir = Path(__file__).resolve().parents[1]

    assert (skill_dir / "SKILL.md").is_file()
    assert (skill_dir / "handler.py").is_file()
    assert skill_dir.name == "registration"
