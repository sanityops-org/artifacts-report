"""Handler test of guidance and triage skills."""

from pathlib import Path

from skills.triage.handler import run

DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def test_check_red_flags_intent_routes():
    """check_red_flags Intention to route to red flag screening"""
    result = run("check_red_flags", {"text": "I suddenly had a terrible chest pain."})

    assert result["status"] == "success"
    assert result["data"]["hit"] is True


def test_shortlist_departments_intent_routes():
    """shortlist_departments Intention route to candidate convergence"""
    result = run("shortlist_departments", {"symptoms": ["Have a headache"]})

    assert result["status"] == "success"
    assert result["data"]["candidates"][0]["department_id"] == "dept_neurology"


def test_query_department_intent_routes():
    """query_department Intention to route to the details of the department"""
    result = run("query_department", {"department_id": "dept_neurology"})

    assert result["status"] == "success"
    assert result["data"]["location"]


def test_intents_share_the_tools_parameter_contract():
    """Routing does not swallow parameters: when the parameter is missing, the error of the tool is transparent as it is"""
    result = run("query_department", {})

    assert result["status"] == "error"
    assert result["error"] == "The required parameters are missing: department_id"


def test_unknown_intent_lists_available_intents():
    """Unknown intent returns a list of available intentions"""
    result = run("no_such_intent", {})

    assert result["status"] == "error"
    assert "Unknown operation: no_such_intent" in result["error"]
    assert "check_red_flags" in result["error"]
    assert "shortlist_departments" in result["error"]
    assert "query_department" in result["error"]


def test_empty_intent_is_error():
    """Empty intent returns an error"""
    result = run("", {})

    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]


def test_skill_directory_is_colocated_with_its_skill_md():
    """SKILL.md The same directory as handler.py for SkillManager to scan"""
    skill_dir = Path(__file__).resolve().parents[1]

    assert (skill_dir / "SKILL.md").is_file()
    assert (skill_dir / "handler.py").is_file()
    assert skill_dir.name == "triage"
