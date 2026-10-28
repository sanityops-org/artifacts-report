"""
Prompt contract tests.

The platform never injects SKILL.md, so prompts/system.txt has to carry the red
lines and the tool map on its own. These tests fail if that content is dropped.
"""

from pathlib import Path

import pytest

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system.txt").read_text(encoding="utf-8")

TOOL_NAMES = [
    "breed_search",
    "breed_details",
    "pet_list",
    "pet_details",
    "care_task_list",
    "care_task_create",
    "care_task_complete",
    "care_schedule_today",
    "health_record_list",
    "health_record_add",
]


@pytest.mark.parametrize("tool_name", TOOL_NAMES)
def test_prompt_names_every_tool(tool_name):
    assert tool_name in SYSTEM_PROMPT


def test_prompt_states_the_vet_referral_rule():
    assert "No Veterinary Diagnosis or Medical Advice" in SYSTEM_PROMPT
    assert "consult a licensed veterinarian" in SYSTEM_PROMPT


def test_prompt_states_the_no_real_adoption_rule():
    assert "No Real Adoption Transactions" in SYSTEM_PROMPT


def test_prompt_states_care_schedules_are_not_prescriptions():
    assert "Recommendations, Not Prescriptions" in SYSTEM_PROMPT
    assert "never invent a feeding amount" in SYSTEM_PROMPT


def test_prompt_does_not_promise_diagnosis():
    """No clause should offer diagnostic capability."""
    lowered = SYSTEM_PROMPT.lower()
    for forbidden in ("you can diagnose", "provide a diagnosis", "prescribe"):
        assert forbidden not in lowered


def test_prompt_inlines_enum_values():
    for value in ("dog", "cat", "small", "medium", "large", "feeding", "walk",
                  "vaccination", "vet_visit", "weekly", "energetic", "shy"):
        assert value in SYSTEM_PROMPT, f"enum value {value!r} missing from the prompt"


def test_prompt_is_self_contained():
    """It must not point the model at SKILL.md files for the essentials."""
    assert "skills/" not in SYSTEM_PROMPT
    assert "SKILL.md" not in SYSTEM_PROMPT
