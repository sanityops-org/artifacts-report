# tests/test_prompt_contract.py
"""Prompt contract: system.txt must write three red lines and all the tools clearly.

The platform does not inject SKILL.md, so system.txt is the only behavior basis for the model on the platform.
"""

import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PROMPT = (PROJECT_ROOT / "prompts" / "system.txt").read_text(encoding="utf-8")

# Red line 1: The red flag is given priority, and if it hits, it will be interrupted (the hint of B1 will land on the side)
RED_LINE_1_PHRASES = (
    "Red line 1: Dangerous symptoms must be interrupted immediately",
    "the first step is to call `triage_check_red_flags`",
    "immediately stop",
    "Don't ask questions when you hit the red flag",
    "No exception",
)

# Red line 2: No diagnosis, no medication (the hint of B2 is on the side)
RED_LINE_2_PHRASES = (
    "Red line 2: No diagnosis, no medicine",
    "Any disease name as a judgment",
    "Any drug name, dosage, usage or drug comparison",
    "I only do guidance, can't judge specific diseases, and don't provide medication advice",
)

# Red line 3: Sections can only be selected in the candidate set (B3's prompts land on the side)
RED_LINE_3_PHRASES = (
    "Red Line 3: Sections can only be selected in the candidate set.",
    "The recommended department must come from the `candidates` returned by `triage_shortlist_departments`",
    "Do not assign departments other than candidates based on your own experience",
    "If `candidates` is empty, recommend the department pointed to by `fallback_department`",
)

EXPECTED_TOOL_NAMES = (
    "triage_check_red_flags",
    "triage_shortlist_departments",
    "triage_query_department",
    "patient_update_profile",
    "patient_get_profile",
    "appointment_query_slots",
    "appointment_create",
    "appointment_query",
    "appointment_cancel",
)


@pytest.mark.parametrize("phrase", RED_LINE_1_PHRASES)
def test_red_line_1_is_stated(phrase):
    assert phrase in SYSTEM_PROMPT


@pytest.mark.parametrize("phrase", RED_LINE_2_PHRASES)
def test_red_line_2_is_stated(phrase):
    assert phrase in SYSTEM_PROMPT


@pytest.mark.parametrize("phrase", RED_LINE_3_PHRASES)
def test_red_line_3_is_stated(phrase):
    assert phrase in SYSTEM_PROMPT


def test_red_lines_are_declared_highest_priority():
    """The priority of the three red lines is explicitly written."""
    assert "higher priority than all other contents of this document" in SYSTEM_PROMPT


@pytest.mark.parametrize("tool_name", EXPECTED_TOOL_NAMES)
def test_every_tool_is_named_in_the_prompt(tool_name):
    """9 Tools can be found in system.txt (success criteria 10）"""
    assert tool_name in SYSTEM_PROMPT


def test_tool_usage_table_covers_every_declared_tool():
    """The tool usage guideline table is consistent with the tool set of tools_schema.json"""
    entries = json.loads((PROJECT_ROOT / "tools_schema.json").read_text(encoding="utf-8"))
    declared = {entry["name"] for entry in entries}

    for name in declared:
        assert name in SYSTEM_PROMPT, name


def test_conversation_flow_has_four_steps():
    """The dialogue process is complete in four steps, and the registration is after the triage."""
    assert "Step 1: Red Flag Screening" in SYSTEM_PROMPT
    assert "Step 2: Structured questioning (up to 3 rounds)" in SYSTEM_PROMPT
    assert "Step 3: Department recommendation" in SYSTEM_PROMPT
    assert "Step 4: Number source and registration" in SYSTEM_PROMPT
    assert SYSTEM_PROMPT.index("Step 1: Red Flag Screening") < SYSTEM_PROMPT.index("Step 3: Department recommendation")
    assert SYSTEM_PROMPT.index("Step 3: Department recommendation") < SYSTEM_PROMPT.index("Step 4: Number source and registration")


def test_output_norms_forbid_overpromising():
    """The output specification does not promise accurate diagnosis / it must be able to be numbered."""
    assert "do not promise" in SYSTEM_PROMPT.lower()


def test_prompt_states_the_data_is_simulated():
    """The boundary description indicates that the data is built-in simulation data (readable side evidence of B4)"""
    assert "built-in simulation data" in SYSTEM_PROMPT
    assert "does not involve any real patient information" in SYSTEM_PROMPT


def test_prompt_does_not_depend_on_skill_injection():
    """system.txt Do not refer to SKILL.md - it is self-contained (success criteria 10）"""
    assert "SKILL.md" not in SYSTEM_PROMPT
    assert "skills/" not in SYSTEM_PROMPT


def test_prompt_mentions_the_fallback_department_rule():
    """The bottom rule is consistent with the engine realization: the candidate is to go when it is empty. fallback_department"""
    assert "fallback_department" in SYSTEM_PROMPT
