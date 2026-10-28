"""Patient information tool test."""

import pytest

from apis import session_api
from tools.patient_get_profile import execute as get_profile
from tools.patient_update_profile import execute as update_profile


@pytest.fixture(autouse=True)
def _clean_sessions():
    session_api.reset_all()
    yield
    session_api.reset_all()


@pytest.fixture
def session_id() -> str:
    return session_api.create_session()["session_id"]


def _params(session_id: str, **fields) -> dict:
    return {"_session": {"session_id": session_id}, **fields}


def test_update_profile_records_fields(session_id):
    """Write in the name, gender and age"""
    result = update_profile(_params(session_id, name="Li Wei", gender="male", age=32))

    assert result["status"] == "success"
    assert result["data"]["name"] == "Li Wei"
    assert result["data"]["is_complete"] is True
    assert result["data"]["missing_fields"] == []


def test_update_profile_reports_missing_fields(session_id):
    """When only filling in the name, the gender and age are still missing."""
    result = update_profile(_params(session_id, name="Li Wei"))

    assert result["status"] == "success"
    assert result["data"]["is_complete"] is False
    assert result["data"]["missing_fields"] == ["Gender", "Age"]


def test_update_profile_merges_across_calls(session_id):
    """Multiple call field accumulation"""
    update_profile(_params(session_id, name="Li Wei"))
    update_profile(_params(session_id, age=32))
    result = update_profile(_params(session_id, gender="male"))

    assert result["data"]["is_complete"] is True


def test_update_profile_requires_at_least_one_field(session_id):
    """Not a single field returns an error."""
    result = update_profile(_params(session_id))

    assert result["status"] == "error"
    assert "At least" in result["error"]


def test_update_profile_rejects_unknown_field(session_id):
    """Unknown fields return errors and are not written"""
    result = update_profile(_params(session_id, nickname="XiaoLi"))

    assert result["status"] == "error"
    assert "nickname" in result["error"]


def test_update_profile_rejects_invalid_phone(session_id):
    """Illegal mobile phone number return error"""
    result = update_profile(_params(session_id, phone="123"))

    assert result["status"] == "error"
    assert result["error"]


def test_update_profile_rejects_out_of_range_age(session_id):
    """Age cross-border return error"""
    result = update_profile(_params(session_id, age=200))

    assert result["status"] == "error"


def test_update_profile_requires_session():
    """Missing session message return error"""
    result = update_profile({"name": "Li Wei"})

    assert result["status"] == "error"
    assert result["error"] == "Missing conversation information"


def test_get_profile_before_update(session_id):
    """Return empty files and all missing items when not filled in."""
    result = get_profile(_params(session_id))

    assert result["status"] == "success"
    assert result["data"]["is_complete"] is False
    assert result["data"]["missing_fields"] == ["Name", "Gender", "Age"]


def test_get_profile_after_update(session_id):
    """After filling in, you can read it back."""
    update_profile(_params(session_id, name="Li Wei", gender="female", age=28))

    result = get_profile(_params(session_id))

    assert result["data"]["name"] == "Li Wei"
    assert result["data"]["gender"] == "female"
    assert result["data"]["age"] == 28
    assert result["data"]["is_complete"] is True


def test_get_profile_requires_session():
    """Missing session message return error"""
    result = get_profile({})

    assert result["status"] == "error"
    assert result["error"] == "Missing conversation information"


def test_unknown_session_is_an_error_not_an_exception():
    """Unknown session_id is converted into an error structure and does not throw an exception."""
    result = get_profile({"_session": {"session_id": "SESS-NOTEXIST"}})

    assert result["status"] == "error"
    assert "session" in result["error"].lower()
