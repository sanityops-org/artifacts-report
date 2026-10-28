#!/usr/bin/env python3
"""
Freight Logistics Assistant - Agent Startup Script

Uses sanityops_agent framework to start the freight logistics assistant.
Automatically scans tools/ directory to register tools, loads prompts/system.txt
as system prompt, and connects skills/ via SkillManager for local injection.
LLM configuration is set via .env file (LLM_API_KEY, LLM_PROVIDER, etc.).
"""

import sys
import asyncio
import importlib.util
from pathlib import Path
from typing import Any, Dict

# Add project path
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


# Fallback schema for tools without declared parameters
_FALLBACK_PARAMETERS: Dict[str, Any] = {
    "type": "object",
    "properties": {"params": {"type": "object", "description": "Tool parameters"}},
}


def load_system_prompt() -> str:
    """Load system prompt from prompts/system.txt"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are a Freight Logistics Assistant."


def scan_and_register_tools(registry: ToolRegistry) -> int:
    """
    Scan tools/ directory and register all tools.

    Each tool file must have:
    - Filename is the tool name (e.g., shipment_get_status.py)
    - Module-level docstring first line is the tool description
    - Module-level 'parameters' (JSON Schema) for parameter declaration
    - execute(params: dict) -> dict function as entry point

    Args:
        registry: Tool registry

    Returns:
        Number of registered tools
    """
    tools_dir = project_root / "tools"
    if not tools_dir.exists():
        print(f"Warning: tools/ directory not found: {tools_dir}")
        return 0

    count = 0

    for tool_file in tools_dir.glob("*.py"):
        if tool_file.name.startswith("_"):
            continue

        tool_name = tool_file.stem

        # Dynamically load module
        spec = importlib.util.spec_from_file_location(tool_name, tool_file)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[tool_name] = module
        spec.loader.exec_module(module)

        # Check for execute function
        if not hasattr(module, "execute"):
            print(f"Warning: {tool_file.name} has no execute function, skipping")
            continue

        # Get description from docstring
        docstring = module.__doc__ or ""
        description = docstring.strip().split("\n")[0]
        if not description:
            description = f"Execute {tool_name} operation"

        # Use module-level parameters, fallback if None
        tool_parameters = getattr(module, "parameters", None)
        if tool_parameters is None:
            tool_parameters = _FALLBACK_PARAMETERS

        # Create Tool wrapper using type() to avoid closure issues
        execute_func = module.execute
        tool_desc = description
        tool_schema = tool_parameters

        def make_execute(func, tool_name):
            async def execute(self, params: Dict[str, Any] | None = None, **kwargs) -> ToolResult:
                try:
                    # Merge params and kwargs
                    full_params: Dict[str, Any] = {}
                    if isinstance(params, dict):
                        full_params.update(params)
                    full_params.update(kwargs)

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

        # Dynamically create Tool subclass
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
        print(f"  Registered tool: {tool_name}")

    return count


def register_skill_tool(registry: ToolRegistry) -> bool:
    """
    Connect skills/ to runtime assembly.

    1. Put SkillManager in ToolContext - AgentFactory._inject_skill_prompt()
       reads context.skill_manager and appends '# Available Skills' to system prompt
    2. Register built-in SkillTool - allows model to use skill(operation="load", name="triage")
       to read SKILL.md content

    Args:
        registry: Tool registry

    Returns:
        Whether connection was successful
    """
    skills_dir = project_root / "skills"
    if not skills_dir.exists():
        print(f"Warning: skills/ directory not found: {skills_dir}")
        return False

    manager = SkillManager(skills_dir=str(skills_dir))
    registry.context.set("skill_manager", manager)
    registry.register(SkillTool())

    names = [s.get("name", "") for s in manager.describe_available()]
    print(f"  Connected skills: {', '.join(names) if names else '(none)'}")
    return True


def create_provider():
    """Create LLM Provider"""
    config = ProviderConfig(_env_file=(project_root / ".env", project_root.parent / ".env"))

    if not config.API_KEY:
        print("Warning: API Key not configured")
        print()
        print("Please configure in .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # or openai")
        print()
        print("Optional:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")
        sys.exit(1)

    return ProviderFactory.create(config)


async def main():
    """Main function"""
    print("=" * 50)
    print("  Freight Logistics Assistant v1.0.0")
    print("=" * 50)
    print()

    # 1. Load system prompt
    print("[1] Loading system prompt...")
    system_prompt = load_system_prompt()
    print(f"  Loaded {len(system_prompt)} characters")

    # 2. Create ToolContext and tool registry
    print("\n[2] Creating tool registry...")
    context = ToolContext()
    registry = ToolRegistry(context)

    # 3. Scan and register tools, connect skills
    print("\n[3] Scanning and registering tools...")
    tool_count = scan_and_register_tools(registry)
    print(f"\n  Registered {tool_count} tools")
    register_skill_tool(registry)

    # 4. Create LLM Provider
    print("\n[4] Creating LLM Provider...")
    provider = create_provider()
    print(f"  Provider: {provider.model}")

    # 5. Create Agent
    print("\n[5] Creating Agent...")
    factory = AgentFactory(
        provider=provider,
        tool_registry=registry,
    )
    agent = factory.create_parent_agent(
        system_prompt=system_prompt,
    )

    print("\nSystem ready. Start conversation by entering a message...")
    print("Enter 'quit' or 'exit' to exit")
    print()

    # 6. Interactive loop
    while True:
        try:
            user_input = input("User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            # Run Agent
            print("\nAssistant: ", end="", flush=True)
            result = await agent.run(user_input)
            print(result.text)
            print()

            if result.termination_reason is not TerminationReason.END_TURN:
                print(f"[Abnormal termination] {result.termination_reason.value}")
                if result.error_detail:
                    for detail in result.error_detail:
                        location = f"Iteration {detail.loop_iteration}"
                        if detail.tool_name:
                            location += f" / {detail.tool_name}"
                        print(f"  - {detail.error_type} ({location}): {detail.message}")
                elif result.error:
                    print(f"  {result.error}")
                print()

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {type(e).__name__}: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())