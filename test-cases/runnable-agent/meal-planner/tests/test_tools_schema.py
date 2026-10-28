"""
Artifact contract tests.

Every tool must be self-describing in the way the platform's LLM-based extractor
expects: a module docstring whose first line is "{tool_name}: ...", and a
module-level `parameters` JSON Schema. These tests fail if a tool drifts.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).parent.parent / "tools"

TOOL_FILES = sorted(f for f in TOOLS_DIR.glob("*.py") if not f.name.startswith("_"))

SKILLS = ("recipe_search", "meal_planning", "nutrition_tracking")

CLINICAL_KEYS = {
    "condition", "diagnosis", "treatment", "supplement_dose",
    "prescription", "medication_dose", "dosage",
}


def _load(tool_file: Path):
    spec = importlib.util.spec_from_file_location(tool_file.stem, tool_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[tool_file.stem] = module
    spec.loader.exec_module(module)
    return module


def test_expected_tool_count():
    assert len(TOOL_FILES) == 10


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda f: f.stem)
def test_tool_declares_a_valid_object_schema(tool_file):
    module = _load(tool_file)
    schema = getattr(module, "parameters", None)

    assert schema is not None, f"{tool_file.name} has no module-level parameters"
    assert schema.get("type") == "object"
    json.dumps(schema)  # must be JSON-serializable for platform extraction


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda f: f.stem)
def test_tool_docstring_follows_the_naming_convention(tool_file):
    module = _load(tool_file)
    first_line = (module.__doc__ or "").strip().split("\n")[0]
    assert first_line.startswith(f"{tool_file.stem}:"), (
        f"{tool_file.name} docstring starts with {first_line!r}"
    )


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda f: f.stem)
def test_tool_exposes_execute(tool_file):
    module = _load(tool_file)
    assert callable(getattr(module, "execute", None))


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda f: f.stem)
def test_declared_required_fields_exist_in_properties(tool_file):
    module = _load(tool_file)
    schema = module.parameters
    properties = set(schema.get("properties", {}))
    for required in schema.get("required", []):
        assert required in properties, (
            f"{tool_file.name} requires {required!r} but does not declare it"
        )


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda f: f.stem)
def test_tool_schema_declares_no_clinical_parameters(tool_file):
    """Boundary B1: no tool may accept a condition, treatment, or supplement dose."""
    module = _load(tool_file)
    properties = set(module.parameters.get("properties", {}))
    assert not (CLINICAL_KEYS & properties), (
        f"{tool_file.name} declares clinical parameters: {CLINICAL_KEYS & properties}"
    )


def test_no_network_imports_in_any_tool():
    banned = ("requests", "httpx", "urllib", "socket", "aiohttp")
    for tool_file in TOOL_FILES:
        source = tool_file.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in source, f"{tool_file.name} imports {name}"


def test_tools_share_the_data_store_singleton():
    """Guards against per-call stores, which silently drop plan and log writes."""
    for tool_file in TOOL_FILES:
        source = tool_file.read_text(encoding="utf-8")
        assert "get_data_store" in source, f"{tool_file.name} does not use the shared store"
        assert "DataStore(" not in source, (
            f"{tool_file.name} constructs its own DataStore and would lose shared state"
        )


def test_skill_handlers_expose_run():
    for skill in SKILLS:
        handler = Path(__file__).parent.parent / "skills" / skill / "handler.py"
        assert handler.exists(), f"missing handler for {skill}"
        assert "def run(intent" in handler.read_text(encoding="utf-8")


def test_every_skill_has_a_skill_md():
    for skill in SKILLS:
        skill_md = Path(__file__).parent.parent / "skills" / skill / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{skill}/SKILL.md is missing frontmatter"
        assert "name:" in text and "description:" in text


def test_skill_handlers_route_known_intents():
    from skills.meal_planning.handler import run as meal_planning
    from skills.nutrition_tracking.handler import run as nutrition
    from skills.recipe_search.handler import run as recipes

    assert recipes("recipe_search", {"cuisine": "italian"})["status"] == "success"
    assert meal_planning("meal_plan_get", {"plan_id": "PLAN0001"})["status"] == "success"
    assert nutrition("nutrition_targets_get", {})["status"] == "success"


def test_skill_handlers_reject_unknown_intents():
    from skills.meal_planning.handler import run as meal_planning
    from skills.nutrition_tracking.handler import run as nutrition
    from skills.recipe_search.handler import run as recipes

    for handler in (recipes, meal_planning, nutrition):
        result = handler("not_a_real_intent", {})
        assert result["status"] == "error"
        assert "Unknown operation" in result["error"]
