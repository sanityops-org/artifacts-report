#!/usr/bin/env python3
"""
Weather Assistant - Agent startup script

Uses sanityops_agent framework to start weather assistant Agent.
Auto-scans tools/ directory to register tools, loads prompts/system.txt as system prompt.
LLM configuration via .env file (LLM_API_KEY, LLM_PROVIDER, etc.).
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
    ToolRegistry,
    Tool,
    ToolResult,
    ToolContext,
    ProviderConfig,
    SkillManager,
)
from sanityops_agent.llm.factory import ProviderFactory
from sanityops_agent.tools.builtins.skill import SkillTool


def load_system_prompt() -> str:
    """Load system prompt"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are Weather Assistant."


def scan_and_register_tools(registry: ToolRegistry) -> int:
    """
    Scan tools/ directory, auto-register all tools

    Each tool file needs:
    - Filename = tool name (e.g., location_search.py)
    - Module-level docstring first line as tool description
    - execute(params: dict) -> dict function

    Args:
        registry: Tool registry

    Returns:
        Number of registered tools
    """
    tools_dir = project_root / "tools"
    if not tools_dir.exists():
        print(f"Warning: tools/ directory does not exist: {tools_dir}")
        return 0

    count = 0

    for tool_file in tools_dir.glob("*.py"):
        if tool_file.name.startswith("_"):
            continue

        tool_name = tool_file.stem

        # Dynamic module loading
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

        # Get description (from docstring first line)
        docstring = module.__doc__ or ""
        description = docstring.strip().split("\n")[0]
        if not description:
            description = f"Execute {tool_name} operation"

        # Get parameters schema if available
        tool_parameters = getattr(module, "parameters", {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Tool parameters"
                }
            }
        })

        # Create Tool wrapper class
        execute_func = module.execute
        tool_desc = description

        def make_execute(func, tool_name):
            async def execute(self, params: Dict[str, Any] | None = None, **kwargs) -> ToolResult:
                try:
                    full_params = params or {}
                    result = func(full_params)
                    return ToolResult(
                        content=str(result.get("data", result.get("error", ""))),
                        success=result.get("status") == "success",
                        metadata=result
                    )
                except Exception as e:
                    return ToolResult(
                        content=f"Execution error: {str(e)}",
                        success=False,
                        metadata={"error": str(e)}
                    )
            return execute

        # Dynamic Tool subclass creation
        DynamicTool = type(
            f"{tool_name.capitalize()}Tool",
            (Tool,),
            {
                "name": tool_name,
                "description": tool_desc,
                "parameters": tool_parameters,
                "execute": make_execute(execute_func, tool_name),
            }
        )

        registry.register(DynamicTool())
        count += 1
        print(f"  Registered tool: {tool_name}")

    return count


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
        print("Optional configuration:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")
        sys.exit(1)

    return ProviderFactory.create(config)


async def main():
    """Main function"""
    print("=" * 50)
    print("  Weather Assistant v1.0.0")
    print("=" * 50)
    print()

    # 1. Load system prompt
    print("[1] Loading system prompt...")
    system_prompt = load_system_prompt()
    print(f"  Loaded {len(system_prompt)} characters")

    # 2. Create ToolContext and tool registry
    print("\n[2] Creating tool registry...")
    context = ToolContext()

    # 3. Scan and register tools
    print("\n[3] Scanning and registering tools...")
    registry = ToolRegistry(context)
    tool_count = scan_and_register_tools(registry)
    print(f"\n  Total {tool_count} tools registered")

    # 4. Register SkillManager and SkillTool
    print("\n[4] Setting up skills...")
    skill_manager = SkillManager(skills_dir=str(project_root / "skills"))
    context.set("skill_manager", skill_manager)
    registry.register(SkillTool())
    print(f"  SkillManager initialized")

    # 5. Create LLM Provider
    print("\n[5] Creating LLM Provider...")
    provider = create_provider()
    print(f"  Provider: {provider.model}")

    # 6. Create Agent
    print("\n[6] Creating Agent...")
    factory = AgentFactory(
        provider=provider,
        tool_registry=registry,
    )
    agent = factory.create_parent_agent(
        system_prompt=system_prompt,
    )

    print("\nSystem ready. Enter message to start conversation...")
    print("Enter 'quit' or 'exit' to quit")
    print()

    # 7. Interactive loop
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

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
