"""Triage tool test."""

from tools.triage_check_red_flags import execute as check_red_flags
from tools.triage_query_department import execute as query_department
from tools.triage_shortlist_departments import execute as shortlist

FORBIDDEN_KEYS = {"disease", "diagnosis", "diagnose", "medication", "drug", "prescription"}


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


# --- triage_check_red_flags ---

def test_check_red_flags_hits():
    """Hit the red flag to return hit=true and disposal guidelines"""
    result = check_red_flags({"text": "I suddenly had a terrible chest pain and sweated all over."})

    assert result["status"] == "success"
    assert result["data"]["hit"] is True
    assert result["data"]["rule_id"] == "RF001"
    assert result["data"]["action"] == "call_120_or_er"
    assert result["data"]["advice"]


def test_check_red_flags_miss():
    """Failed to return hit=false"""
    result = check_red_flags({"text": "I have a little insomnia recently."})

    assert result["status"] == "success"
    assert result["data"]["hit"] is False
    assert result["data"]["action"] is None


def test_check_red_flags_accepts_symptoms():
    """Can be accompanied by normalized symptom words"""
    result = check_red_flags({"text": "Not feeling well", "symptoms": ["chest pain"]})

    assert result["data"]["hit"] is True


def test_check_red_flags_requires_text():
    """Missing text returns error message"""
    result = check_red_flags({})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: text"


def test_check_red_flags_blank_text_is_not_an_error():
    """Pure blank text does not count as missing parameters and returns unhit"""
    result = check_red_flags({"text": "   "})

    assert result["status"] == "success"
    assert result["data"]["hit"] is False


def test_check_red_flags_never_returns_error_for_long_text():
    """Ultra-long text does not throw exceptions (maxLength of schema is constrained by the platform side)"""
    result = check_red_flags({"text": "Chest pain" + "ah" * 2000})

    assert result["status"] == "success"


# --- triage_shortlist_departments ---

def test_shortlist_returns_candidates():
    """Return to the candidate department for regular symptoms"""
    result = shortlist({"symptoms": ["Have a headache"]})

    assert result["status"] == "success"
    assert result["data"]["candidates"][0]["department_id"] == "dept_neurology"
    assert len(result["data"]["candidates"]) <= 3


def test_shortlist_applies_pediatrics_rule():
    """Compulsory pediatrics under the age of 14 (success criteria 4）"""
    result = shortlist({"symptoms": ["Generate heat"], "age": 8})

    assert [c["department_id"] for c in result["data"]["candidates"]] == ["dept_pediatrics"]
    assert result["data"]["age_rule_applied"] is True


def test_shortlist_fallback_when_nothing_matches():
    """Give the bottom department when there is no hit."""
    result = shortlist({"symptoms": ["I can't tell where it's uncomfortable."]})

    assert result["status"] == "success"
    assert result["data"]["candidates"] == []
    assert result["data"]["fallback_department"] == "dept_general_internal"


def test_shortlist_requires_symptoms():
    """Missing symptoms return error message"""
    result = shortlist({})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: symptoms"


def test_shortlist_rejects_empty_symptoms():
    """The empty array is considered to be missing the required parameters."""
    result = shortlist({"symptoms": []})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: symptoms"


def test_shortlist_rejects_blank_symptoms_list():
    """A blank list of symptoms is considered to be missing the necessary parameters."""
    result = shortlist({"symptoms": ["   ", ""]})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: symptoms"


def test_shortlist_no_diagnosis_keys_in_output():
    """The return structure does not contain any diagnostic / drug phase key (landing verification of B2)"""
    result = shortlist({"symptoms": ["Headache", "Fever"], "age": 30})

    assert _all_keys(result) & FORBIDDEN_KEYS == set()


# --- triage_query_department ---

def test_query_department_returns_info():
    """Return to the business scope, location and pre-treatment preparation of the department"""
    result = query_department({"department_id": "dept_neurology"})

    assert result["status"] == "success"
    assert result["data"]["name"] == "Neurology"
    assert result["data"]["location"] == "Area C, 4th Floor, Outpatient Building"
    assert result["data"]["preparation"]


def test_query_department_unknown_id_is_error():
    """Unknown departments return errors and list available departments."""
    result = query_department({"department_id": "dept_not_exist"})

    assert result["status"] == "error"
    assert "dept_not_exist" in result["error"]
    assert "dept_neurology" in result["error"]


def test_query_department_requires_id():
    """Missing department_id return error message"""
    result = query_department({})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: department_id"


def test_query_department_no_diagnosis_keys_in_output():
    """The return structure does not contain any diagnostic / drug phase key (landing verification of B2)"""
    result = query_department({"department_id": "dept_dermatology"})

    assert _all_keys(result) & FORBIDDEN_KEYS == set()
