#!/usr/bin/env python3
"""
Medical Guidance Assistant - Agent Startup Script

Use the sanityops_agent framework to start the guidance assistant Agent。
Automatically scan tools/ directory registration tools, load prompts/system.txt as system prompts,
And give skills/ to SkillManager and let SKILL.md inject system prompts locally.
LLM Configuration through .env file settings (LLM_API_KEY, LLM_PROVIDER, etc.).
"""

import sys
import asyncio
import importlib.util
from pathlib import Path
from typing import Any, Dict

# Add the project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sanityops_agent import (
    AgentFactory,
    SkillManager,
    TerminationReason,
    ToolRegistry,
    Tool,
    ToolResult,
    ToolContext,
    ProviderConfig,
)
from sanityops_agent.llm.factory import ProviderFactory
from sanityops_agent.tools.builtins.skill import SkillTool
from apis.session_api import create_session


# When the tool file does not declare module-level parameters schema
_FALLBACK_PARAMETERS: Dict[str, Any] = {
    "type": "object",
    "properties": {"params": {"type": "object", "description": "Tool parameters"}},
}


def load_system_prompt() -> str:
    """Load system prompts"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are a medical guidance assistant."


def scan_and_register_tools(registry: ToolRegistry) -> int:
    """
    Scan tools/ directory to automatically register all tools

    Each tool file requires:
    - The file name is the tool name (such as triage_check_red_flags.py）
    - The first line of module-level docstring is described as a tool
    - Module-level parameters (JSON Schema) are declared as tool parameters, and the default is universal. schema
    - execute(params: dict) -> dict Function

    Args:
        registry: Tool registration form

    Returns:
        The number of registered tools
    """
    tools_dir = project_root / "tools"
    if not tools_dir.exists():
        print(f"Warning: Tools/ directory does not exist: {tools_dir}")
        return 0

    count = 0

    for tool_file in tools_dir.glob("*.py"):
        if tool_file.name.startswith("_"):
            continue

        tool_name = tool_file.stem  # File name (without extension)

        # Dynamic loading module
        spec = importlib.util.spec_from_file_location(tool_name, tool_file)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[tool_name] = module
        spec.loader.exec_module(module)

        # Check whether there is an execute function
        if not hasattr(module, "execute"):
            print(f"Warning: {tool_file.name} does not have an execute function, skip")
            continue

        # Get the description (from the first line of docstring)
        docstring = module.__doc__ or ""
        description = docstring.strip().split("\n")[0]
        if not description:
            description = f"Perform the {tool_name} operation"

        # Use module-level parameters first, and share the same copy with the platform extraction. schema；
        # Only when the module does not declare parameters (None) can it be returned to the bottom. The explicit empty {} is considered as an intentional declaration.
        tool_parameters = getattr(module, "parameters", None)
        if tool_parameters is None:
            tool_parameters = _FALLBACK_PARAMETERS

        # Create Tool packaging class - use type() to create dynamically to avoid closure problems
        execute_func = module.execute  # Capture closure
        tool_desc = description  # Capture description
        tool_schema = tool_parameters  # Catch schema

        def make_execute(func, tool_name):
            async def execute(self, params: Dict[str, Any] | None = None, **kwargs) -> ToolResult:
                # Get session information from ToolContext
                session = self.context.get("session")
                try:
                    # Combine two call forms: the model passes the top-level parameters according to the declaration schema (falling in kwargs），
                    # The old call wraps the parameters in params.
                    full_params: Dict[str, Any] = {}
                    if isinstance(params, dict):
                        full_params.update(params)
                    full_params.update(kwargs)

                    # Inject the session information into the parameters
                    if session:
                        full_params["_session"] = session

                    result = func(full_params)
                    return ToolResult(
                        content=str(result.get("data", result.get("error", ""))),
                        success=result.get("status") == "success",
                        metadata=result,
                    )
                except Exception as e:
                    return ToolResult(
                        content=f"Execution error: {str(e)}",
                        success=False,
                        metadata={"error": str(e)},
                    )
            return execute

        # Dynamically create Tool subclasses
        DynamicTool = type(
            f"{tool_name.capitalize()}Tool",
            (Tool,),
            {
                "name": tool_name,
                "description": tool_desc,
                "parameters": tool_schema,
                "execute": make_execute(execute_func, tool_name),
            },
        )

        registry.register(DynamicTool())
        count += 1
        print(f"  Registration tools: {tool_name}")

    return count


def register_skill_tool(registry: ToolRegistry) -> bool:
    """
    Link skills/ into the assembly chain at runtime

    1. Put SkillManager into ToolContext —— AgentFactory._inject_skill_prompt()
       It will read context.skill_manager and add the `# Available Skills` paragraph to the system prompt.
    2. Register the built-in SkillTool - the model can only be used skill(operation="load", name="triage")
       Read the text of SKILL.md

    Args:
        registry: Tool registration form

    Returns:
        Whether the access is successful
    """
    skills_dir = project_root / "skills"
    if not skills_dir.exists():
        print(f"Warning: skills/ directory does not exist: {skills_dir}")
        return False

    manager = SkillManager(skills_dir=str(skills_dir))
    registry.context.set("skill_manager", manager)
    registry.register(SkillTool())

    names = [s.get("name", "") for s in manager.describe_available()]
    print(f"  Accessed skills: {', '.join(names) if names else '(none)'}")
    return True


def create_provider():
    """Set up LLM Provider"""
    config = ProviderConfig(_env_file=(project_root / ".env", project_root.parent / ".env"))

    if not config.API_KEY:
        print("Warning: Not configured API Key")
        print()
        print("Please configure it in the .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # Someone openai")
        print()
        print("Optional configuration:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")
        sys.exit(1)

    return ProviderFactory.create(config)


async def main():
    """Main function"""
    print("=" * 50)
    print("  Medical guidance assistant v1.0.0")
    print("=" * 50)
    print()

    # 1. Create a patient session (this Agent does not log in and select roles)
    print("[1] Create a patient session...")
    session = create_session()
    print(f"  Conversation number: {session['session_id']}")

    # 2. Load system prompts
    print("\n[2] Load system prompts...")
    system_prompt = load_system_prompt()
    print(f"  {len(system_prompt)} characters have been loaded")

    # 3. Create ToolContext and tool registry
    print("\n[3] Create a tool registration form...")
    context = ToolContext()
    context.set("session", session)  # Deposit the session information into context
    registry = ToolRegistry(context)

    # 4. Scan and register tools to access skills
    print("\n[4] Scan and register tools...")
    tool_count = scan_and_register_tools(registry)
    print(f"\n  A total of {tool_count} tools have been registered")
    register_skill_tool(registry)

    # 5. Set up LLM Provider
    print("\n[5] Set up LLM Provider...")
    provider = create_provider()
    print(f"  Provider: {provider.model}")

    # 6. Set up Agent
    print("\n[6] Set up Agent...")
    factory = AgentFactory(
        provider=provider,
        tool_registry=registry,
    )
    agent = factory.create_parent_agent(
        system_prompt=system_prompt,
    )

    print("\nThe system is ready. Enter the message to start the conversation...")
    print("Enter 'quit' or 'exit' to exit")
    print()

    # 7. Interactive loop
    while True:
        try:
            user_input = input("Consumer: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            # Be in motion Agent
            print("\nAssistant: ", end="", flush=True)
            result = await agent.run(user_input)
            print(result.text)
            print()

            if result.termination_reason is not TerminationReason.END_TURN:
                print(f"[Abnormal termination] {result.termination_reason.value}")
                if result.error_detail:
                    for detail in result.error_detail:
                        location = f"The {detail.loop_iteration} round"
                        if detail.tool_name:
                            location += f" / {detail.tool_name}"
                        print(f"  - {detail.error_type}（{location}）: {detail.message}")
                elif result.error:
                    print(f"  {result.error}")
                print()

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nWrong: {type(e).__name__}: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
