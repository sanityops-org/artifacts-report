"""Patient conversation layer test."""

import re

import pytest

from apis import session_api
from models.enums import Gender


@pytest.fixture(autouse=True)
def _clean_sessions():
    """Empty the conversation table before and after each use case to ensure isolation."""
    session_api.reset_all()
    yield
    session_api.reset_all()


def test_create_session_has_expected_shape():
    """The new session structure is complete, and the id conforms to the agreed format.（^SESS-[0-9A-F]{8}$）"""
    session = session_api.create_session()

    assert re.fullmatch(r"SESS-[0-9A-F]{8}", session["session_id"])
    assert len(session["session_id"]) == len("SESS-") + 8
    assert session["patient"] is None
    assert session["created_at"]


def test_session_ids_are_unique():
    """Create it many times to get different id"""
    ids = {session_api.create_session()["session_id"] for _ in range(20)}

    assert len(ids) == 20


def test_get_session_returns_created_session():
    """Retrie the session by id"""
    created = session_api.create_session()

    assert session_api.get_session(created["session_id"])["session_id"] == created["session_id"]


def test_get_unknown_session_raises_key_error():
    """Unknown session_id throw KeyError"""
    with pytest.raises(KeyError):
        session_api.get_session("SESS-NOTEXIST")


def test_get_patient_is_none_before_update():
    """When the information is not filled in, it is read as None"""
    session = session_api.create_session()

    assert session_api.get_patient(session["session_id"]) is None


def test_update_patient_creates_profile():
    """Read the complete file after writing"""
    session = session_api.create_session()

    profile = session_api.update_patient(
        session["session_id"], name="Li Wei", gender="male", age=32
    )

    assert profile.name == "Li Wei"
    assert profile.gender == Gender.MALE
    assert profile.age == 32
    assert profile.is_complete is True


def test_update_patient_merges_partial_fields():
    """Fields are cumulative when supplemented multiple times and do not overwrite each other."""
    session = session_api.create_session()
    sid = session["session_id"]

    session_api.update_patient(sid, name="Li Wei")
    session_api.update_patient(sid, age=32)
    profile = session_api.update_patient(sid, gender="male")

    assert (profile.name, profile.age, profile.gender) == ("Li Wei", 32, Gender.MALE)
    assert profile.is_complete is True


def test_update_patient_overwrites_existing_field():
    """When providing the same field repeatedly, the last one shall prevail."""
    session = session_api.create_session()
    sid = session["session_id"]
    session_api.update_patient(sid, name="Li Wei")

    profile = session_api.update_patient(sid, name="Li Xiaoming")

    assert profile.name == "Li Xiaoming"


def test_update_patient_ignores_none_values():
    """Fields with the value None do not overwrite existing values."""
    session = session_api.create_session()
    sid = session["session_id"]
    session_api.update_patient(sid, name="Li Wei")

    profile = session_api.update_patient(sid, name=None, age=32)

    assert profile.name == "Li Wei"
    assert profile.age == 32


def test_update_patient_rejects_unknown_field():
    """Unknown field throw ValueError"""
    session = session_api.create_session()

    with pytest.raises(ValueError):
        session_api.update_patient(session["session_id"], nickname="XiaoLi")


def test_update_patient_rejects_invalid_phone():
    """Illegal mobile phone numbers are rejected when writing."""
    session = session_api.create_session()

    with pytest.raises(ValueError):
        session_api.update_patient(session["session_id"], phone="123")


def test_update_unknown_session_raises_key_error():
    """Write and throw to the unknown session KeyError"""
    with pytest.raises(KeyError):
        session_api.update_patient("SESS-NOTEXIST", name="Li Wei")


def test_patient_is_visible_through_session_dict():
    """Patient snapshots in the session dict are updated synchronously for tool layer reading"""
    session = session_api.create_session()
    session_api.update_patient(session["session_id"], name="Li Wei")

    assert session["patient"]["name"] == "Li Wei"


def test_reset_all_clears_sessions():
    """reset_all Empty the session table"""
    created = session_api.create_session()

    session_api.reset_all()

    with pytest.raises(KeyError):
        session_api.get_session(created["session_id"])
