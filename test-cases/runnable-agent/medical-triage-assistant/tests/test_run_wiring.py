# tests/test_run_wiring.py
"""Start the script assembly self-test. No need for LLM_API_KEY, only verify that the assembly chain is correct."""

import asyncio
from pathlib import Path

import pytest

from sanityops_agent import AgentFactory, SkillManager, ToolContext, ToolRegistry
from apis import session_api
from scripts.run import (
    load_system_prompt,
    register_skill_tool,
    scan_and_register_tools,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TOOLS = {
    "triage_check_red_flags",
    "triage_shortlist_departments",
    "triage_query_department",
    "patient_update_profile",
    "patient_get_profile",
    "appointment_query_slots",
    "appointment_create",
    "appointment_query",
    "appointment_cancel",
}


@pytest.fixture
def registry():
    """Assemble a complete registry: real session + 9 tools + SkillManager + SkillTool"""
    session_api.reset_all()
    context = ToolContext()
    context.set("session", session_api.create_session())
    reg = ToolRegistry(context)
    scan_and_register_tools(reg)
    register_skill_tool(reg)
    return reg


def test_system_prompt_is_loaded_verbatim():
    """The system prompts are loaded according to the original text, and no processing is done."""
    prompt = load_system_prompt()

    assert prompt == (PROJECT_ROOT / "prompts" / "system.txt").read_text(encoding="utf-8")
    assert len(prompt) > 500


def test_scan_registers_all_nine_tools(registry):
    """9 Register all business tools"""
    registered = {tool.name for tool in registry.list_all()}

    assert EXPECTED_TOOLS <= registered
    assert len(EXPECTED_TOOLS) == 9


def test_tool_description_comes_from_docstring_first_line(registry):
    """The tool description is taken from the first line of the module docstring"""
    tool = registry.get("triage_check_red_flags")

    assert tool.description.startswith("triage_check_red_flags: Red flag symptom screening")


def test_registered_tools_use_module_level_parameters(registry):
    """Module-level parameters are used for registration, instead of the general-purpose parameters of 09-14."""
    tool = registry.get("triage_check_red_flags")

    assert set(tool.parameters["properties"]) == {"text", "symptoms"}
    assert tool.parameters["required"] == ["text"]
    assert "params" not in tool.parameters["properties"]


def test_kwargs_are_merged_and_session_is_injected(registry):
    """The model transmits top-level parameters according to the declaration schema: parameters and session information can be in place."""
    tool = registry.get("patient_update_profile")

    result = asyncio.run(tool.execute(name="Li Wei", gender="male", age=32))

    assert result.success is True
    assert result.metadata["data"]["name"] == "Li Wei"
    assert result.metadata["data"]["is_complete"] is True


def test_failed_tool_call_is_reported_as_unsuccessful(registry):
    """ToolResult.success is False when the tool returns error, and does not throw an exception."""
    tool = registry.get("triage_query_department")

    result = asyncio.run(tool.execute(department_id="dept_not_exist"))

    assert result.success is False
    assert "dept_not_exist" in result.metadata["error"]


def test_read_only_tool_runs_through_the_adapter(registry):
    """Red flag screening is called by the adapter and returns to structured metadata"""
    tool = registry.get("triage_check_red_flags")

    result = asyncio.run(tool.execute(text="I suddenly had a terrible chest pain."))

    assert result.success is True
    assert result.metadata["data"]["hit"] is True
    assert result.metadata["data"]["action"] == "call_120_or_er"


def test_skill_manager_is_wired_into_context(registry):
    """SkillManager It has been put into ToolContext (success standard 11）"""
    manager = registry.context.skill_manager

    assert isinstance(manager, SkillManager)
    assert {s["name"] for s in manager.describe_available()} == {"triage", "registration"}


def test_available_skills_section_is_appended_to_prompt(registry):
    """After assembly, the system prompt will have more `# Available Skills` paragraph (success criteria 11）"""
    section = AgentFactory._build_skill_prompt(registry.context.skill_manager)

    assert section.startswith("\n# Available Skills")
    assert "triage" in section
    assert "registration" in section


def test_skill_tool_can_load_skill_markdown(registry):
    """skill(operation="load") Be able to read the body of SKILL.md (success standard 11）"""
    tool = registry.get("skill")

    assert tool is not None
    result = asyncio.run(tool.execute(operation="load", name="triage"))

    assert result.success is True
    assert "Guidance and triage skills" in result.content


def test_register_skill_tool_reports_missing_skills_dir(monkeypatch, tmp_path):
    """skills/ Give a warning when it does not exist and return False, without throwing an exception."""
    import scripts.run as run_module

    monkeypatch.setattr(run_module, "project_root", tmp_path)
    reg = ToolRegistry(ToolContext())

    assert run_module.register_skill_tool(reg) is False
    assert reg.get("skill") is None


def test_tools_without_module_parameters_fall_back(monkeypatch, tmp_path):
    """Tools that have not declared parameters go back to the bottom of the general pocket. schema"""
    import scripts.run as run_module

    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    (tools_dir / "__init__.py").write_text("", encoding="utf-8")
    (tools_dir / "legacy_echo.py").write_text(
        '"""legacy_echo: Display parameters."""\n'
        "\n"
        "\n"
        "def execute(params):\n"
        '    return {"status": "success", "data": params}\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(run_module, "project_root", tmp_path)
    reg = ToolRegistry(ToolContext())

    count = run_module.scan_and_register_tools(reg)

    assert count == 1
    tool = reg.get("legacy_echo")
    assert "params" in tool.parameters["properties"]
    result = asyncio.run(tool.execute(params={"x": 1}))
    assert result.metadata["data"] == {"x": 1}
