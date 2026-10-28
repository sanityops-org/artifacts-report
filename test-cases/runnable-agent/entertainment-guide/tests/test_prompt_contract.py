"""
Prompt contract tests.

The platform never injects SKILL.md, so prompts/system.txt has to carry the red
lines and the tool map on its own. These tests fail if that content is dropped.
"""

from pathlib import Path

import pytest

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system.txt").read_text(encoding="utf-8")

TOOL_NAMES = [
    "title_search",
    "title_details",
    "title_by_actor",
    "title_by_director",
    "get_recommendations",
    "watchlist_add",
    "watchlist_remove",
    "watchlist_list",
    "watchlist_mark_watched",
    "review_list",
]


@pytest.mark.parametrize("tool_name", TOOL_NAMES)
def test_prompt_names_every_tool(tool_name):
    assert tool_name in SYSTEM_PROMPT


def test_prompt_states_the_no_streaming_rule():
    assert "B1: No Streaming or Playback" in SYSTEM_PROMPT
    assert "simulated" in SYSTEM_PROMPT.lower()


def test_prompt_states_the_no_piracy_rule():
    assert "B2: No Piracy or Illegal Content" in SYSTEM_PROMPT
    assert "pirated" in SYSTEM_PROMPT


def test_prompt_states_that_recommendations_are_suggestions():
    assert "B3: Recommendations Are Suggestions" in SYSTEM_PROMPT


def test_prompt_inlines_enum_values():
    for value in ("sci_fi", "thriller", "documentary", "thoughtful", "to_watch", "watched"):
        assert value in SYSTEM_PROMPT, f"{value!r} missing from the prompt"


def test_prompt_is_self_contained():
    """It must not point the model at SKILL.md files for the essentials."""
    assert "SKILL.md" not in SYSTEM_PROMPT
    assert "skills/" not in SYSTEM_PROMPT
