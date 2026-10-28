"""Workpiece contract: The module-level parameters of tools/*.py and tools_schema.json must be of the same source and the same value.

Once these two places drift, the local running tool will be declared as another on the platform side (success standard 12）。
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = PROJECT_ROOT / "tools"
SCHEMA_PATH = PROJECT_ROOT / "tools_schema.json"

EXPECTED_TOOL_COUNT = 9


def _load_schema() -> list:
    """The declaration of the neutral format tool used by the reading platform"""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_tool_module(path: Path):
    """Load the tool module by file path (consistent with the scanning method of scripts/run.py)"""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


TOOL_FILES = sorted(p for p in TOOLS_DIR.glob("*.py") if not p.name.startswith("_"))
SCHEMA_BY_NAME = {entry["name"]: entry for entry in _load_schema()}


def test_tools_schema_file_exists():
    """tools_schema.json Must exist - paste directly when creating a new version on the platform"""
    assert SCHEMA_PATH.is_file()


def test_schema_entries_are_well_formed():
    """Each entry name / description / parameters is complete, and the description is specific enough (success standard 9）"""
    entries = _load_schema()

    assert isinstance(entries, list)
    assert len(entries) == EXPECTED_TOOL_COUNT
    assert len({entry["name"] for entry in entries}) == EXPECTED_TOOL_COUNT
    for entry in entries:
        assert set(entry) == {"name", "description", "parameters"}, entry["name"]
        assert len(entry["description"]) >= 40, entry["name"]
        assert entry["parameters"]["type"] == "object"


def test_tool_name_sets_are_equal():
    """The file name set of the tool file is exactly equal to the name set of the schema."""
    assert {path.stem for path in TOOL_FILES} == set(SCHEMA_BY_NAME)


def test_every_tool_file_declares_module_parameters():
    """Each tool file declares the module level. parameters"""
    assert len(TOOL_FILES) == EXPECTED_TOOL_COUNT
    for path in TOOL_FILES:
        assert isinstance(getattr(_load_tool_module(path), "parameters", None), dict), path.name


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda p: p.stem)
def test_module_parameters_match_schema(tool_file):
    """Module-level parameters are verbatim with tools_schema.json (success criteria 12）"""
    module = _load_tool_module(tool_file)

    assert module.parameters == SCHEMA_BY_NAME[tool_file.stem]["parameters"]


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda p: p.stem)
def test_docstring_first_line_names_the_tool(tool_file):
    """docstring The first line begins with `{tool name}: `, and run.py relies on it to take the description."""
    module = _load_tool_module(tool_file)
    first_line = (module.__doc__ or "").strip().split("\n")[0]

    assert first_line.startswith(f"{tool_file.stem}:")


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda p: p.stem)
def test_parameters_are_strict_typed_objects(tool_file):
    """The parameter uses strong type + closed object description, which is convenient for the platform to check the compatibility of provider."""
    params = _load_tool_module(tool_file).parameters

    assert params["type"] == "object"
    assert params["additionalProperties"] is False
    assert isinstance(params["required"], list)
    assert set(params["required"]) <= set(params["properties"])
    for name, prop in params["properties"].items():
        assert prop["type"] in ("string", "integer", "array"), f"{tool_file.stem}.{name}"
        assert prop["description"], f"{tool_file.stem}.{name}"


@pytest.mark.parametrize("tool_file", TOOL_FILES, ids=lambda p: p.stem)
def test_tools_declare_execute(tool_file):
    """Every tool is exposed. execute(params) -> dict"""
    module = _load_tool_module(tool_file)

    assert callable(getattr(module, "execute", None))


FORBIDDEN_NETWORK_MARKERS = (
    "import requests",
    "from requests",
    "import urllib",
    "from urllib",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import socket",
    "from socket",
)

SOURCE_DIRS = ("apis", "models", "skills", "tools", "scripts")


def test_no_network_calls_anywhere_in_the_agent():
    """B4：No network call, no third-party medical interface（spec 2.2 B4 / 11.6）

    The verification method of boundary B4 is code review, which is made into a repeatable assertion.
    """
    for directory in SOURCE_DIRS:
        for path in (PROJECT_ROOT / directory).rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            relative = path.relative_to(PROJECT_ROOT)
            for marker in FORBIDDEN_NETWORK_MARKERS:
                assert marker not in source, f"{relative}: {marker}"
            for scheme in ("http://", "https://", "ws://", "wss://"):
                assert scheme not in source, f"{relative}: {scheme}"
