"""
Prompt contract tests.

The platform never injects SKILL.md, so prompts/system.txt has to carry the red
lines and the tool map on its own. These tests fail if that content is dropped.
"""

from pathlib import Path

import pytest

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system.txt").read_text(encoding="utf-8")

TOOL_NAMES = [
    "destination_search",
    "destination_details",
    "attraction_list",
    "attraction_details",
    "accommodation_search",
    "accommodation_details",
    "itinerary_create",
    "itinerary_details",
    "budget_estimate",
]


@pytest.mark.parametrize("tool_name", TOOL_NAMES)
def test_prompt_names_every_tool(tool_name):
    assert tool_name in SYSTEM_PROMPT


def test_prompt_states_the_no_real_bookings_rule():
    assert "B1: No Real Bookings" in SYSTEM_PROMPT
    assert "simulated" in SYSTEM_PROMPT.lower()


def test_prompt_states_the_no_legal_advice_rule():
    assert "B2: No Legal/Visa Advice" in SYSTEM_PROMPT


def test_prompt_states_estimates_are_approximate():
    assert "B3: Budget Estimates Are Approximate" in SYSTEM_PROMPT
    assert "Estimates are approximate" in SYSTEM_PROMPT


def test_prompt_is_self_contained():
    """It must not point the model at SKILL.md files for the essentials."""
    assert "SKILL.md" not in SYSTEM_PROMPT
    assert "skills/" not in SYSTEM_PROMPT
