"""
Prompt contract tests.

The platform never injects SKILL.md, so prompts/system.txt has to carry the red
lines and the tool map on its own. These tests fail if that content is dropped.
"""

from pathlib import Path

import pytest

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system.txt").read_text(encoding="utf-8")

TOOL_NAMES = [
    "location_search",
    "weather_current",
    "weather_forecast",
    "alert_query_active",
    "alert_query_by_location",
    "alert_get_details",
    "alert_subscribe",
]


@pytest.mark.parametrize("tool_name", TOOL_NAMES)
def test_prompt_names_every_tool(tool_name):
    assert tool_name in SYSTEM_PROMPT


def test_prompt_states_the_no_real_api_rule():
    assert "B1: No Real API Calls" in SYSTEM_PROMPT
    assert "simulated" in SYSTEM_PROMPT.lower()


def test_prompt_states_the_no_health_advice_rule():
    assert "B2: No Health Advice" in SYSTEM_PROMPT
    assert "medical or health recommendations" in SYSTEM_PROMPT


def test_prompt_states_the_severity_hierarchy():
    assert "B3: Alert Severity Hierarchy" in SYSTEM_PROMPT
    assert "Warning > Watch > Advisory" in SYSTEM_PROMPT


def test_prompt_does_not_offer_medical_guidance():
    lowered = SYSTEM_PROMPT.lower()
    for forbidden in ("you can advise", "stay indoors if", "medical advice for"):
        assert forbidden not in lowered


def test_prompt_is_self_contained():
    """It must not point the model at SKILL.md files for the essentials."""
    assert "SKILL.md" not in SYSTEM_PROMPT
    assert "skills/" not in SYSTEM_PROMPT
