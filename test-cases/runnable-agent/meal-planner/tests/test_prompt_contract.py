"""
Prompt contract tests.

The platform never injects SKILL.md, so prompts/system.txt has to carry the red
lines and the tool map on its own. These tests fail if that content is dropped.
"""

from pathlib import Path

import pytest

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system.txt").read_text(encoding="utf-8")

TOOL_NAMES = [
    "recipe_search",
    "recipe_details",
    "recipe_by_ingredient",
    "meal_plan_create",
    "meal_plan_get",
    "meal_plan_add_entry",
    "shopping_list_generate",
    "nutrition_log_meal",
    "nutrition_daily_summary",
    "nutrition_targets_get",
]


@pytest.mark.parametrize("tool_name", TOOL_NAMES)
def test_prompt_names_every_tool(tool_name):
    assert tool_name in SYSTEM_PROMPT


def test_prompt_states_the_no_clinical_advice_rule():
    assert "B1: No Clinical Nutrition Advice" in SYSTEM_PROMPT
    assert "registered dietitian" in SYSTEM_PROMPT
    assert "supplement" in SYSTEM_PROMPT


def test_prompt_states_the_no_allergen_guarantee_rule():
    assert "B2: No Allergen Guarantees" in SYSTEM_PROMPT
    assert "not an allergen analysis" in SYSTEM_PROMPT


def test_prompt_states_that_nutrition_is_estimated():
    assert "B3: Nutrition Values Are Estimates" in SYSTEM_PROMPT
    assert "estimate" in SYSTEM_PROMPT.lower()


def test_prompt_forbids_clinical_capability_rather_than_offering_it():
    """
    The prompt is expected to *mention* clinical topics — in order to forbid them.
    So this checks the framing: the prohibition must be present, and no affirmative
    offer of clinical capability may appear alongside it.
    """
    lowered = SYSTEM_PROMPT.lower()

    # The prohibition is what the red line is made of
    assert "never diagnose" in lowered or "never tell" in lowered

    # Affirmative offers would look like these
    for offering in (
        "you can diagnose",
        "you may prescribe",
        "we can treat",
        "will cure your",
        "i will treat",
        "helps manage your condition",
    ):
        assert offering not in lowered, f"prompt offers clinical capability: {offering!r}"


def test_prompt_inlines_enum_values():
    for value in ("breakfast", "lunch", "dinner", "snack", "gluten_free",
                  "high_protein", "mediterranean", "thai"):
        assert value in SYSTEM_PROMPT, f"enum value {value!r} missing from the prompt"


def test_prompt_is_self_contained():
    """It must not point the model at SKILL.md files for the essentials."""
    assert "SKILL.md" not in SYSTEM_PROMPT
    assert "skills/" not in SYSTEM_PROMPT
