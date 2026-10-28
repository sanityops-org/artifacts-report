#!/usr/bin/env python3
"""
Energy Management Assistant - Agent Startup Script

Uses sanityops_agent framework to start the Energy Management Assistant Agent.
Automatically scans tools/ directory to register tools, loads prompts/system.txt as system prompt.
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
    ToolRegistry,
    Tool,
    ToolResult,
    ToolContext,
    ProviderConfig,
)
from sanityops_agent.llm.factory import ProviderFactory
from apis.energy_api import login, ROLE_PERMISSIONS


def load_system_prompt() -> str:
    """Load system prompt"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are the Energy Management Assistant."


def scan_and_register_tools(registry: ToolRegistry) -> int:
    """
    Scan tools/ directory and automatically register all tools

    Each tool file requires:
    - File name is the tool name (e.g., energy_analyze_consumption.py)
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

        tool_name = tool_file.stem  # File name without extension

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

        # Get description (from docstring first line)
        docstring = module.__doc__ or ""
        description = docstring.strip().split("\n")[0]
        if not description:
            description = f"Execute {tool_name} operation"

        # Create Tool wrapper - use type() to dynamically create to avoid closure issues
        execute_func = module.execute
        tool_desc = description

        def make_execute(func, tool_name):
            async def execute(self, params: Dict[str, Any] | None = None, **kwargs) -> ToolResult:
                # Get session from ToolContext
                session = self.context.get("session")
                try:
                    # Inject session info into params
                    full_params = params or {}
                    if session:
                        full_params["_session"] = session

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

        # Dynamically create Tool subclass
        DynamicTool = type(
            f"{tool_name.capitalize()}Tool",
            (Tool,),
            {
                "name": tool_name,
                "description": tool_desc,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "params": {
                            "type": "object",
                            "description": "Tool parameters"
                        }
                    }
                },
                "execute": make_execute(execute_func, tool_name),
            }
        )

        registry.register(DynamicTool())
        count += 1
        print(f"  Registered tool: {tool_name}")

    return count


def select_role() -> dict:
    """Select login role"""
    print("\nPlease select a login role:")
    roles = list(ROLE_PERMISSIONS.keys())
    for i, role in enumerate(roles, 1):
        config = ROLE_PERMISSIONS[role]
        perms = ", ".join(config["permissions"])
        cmd_auth = "Can issue commands" if config["can_issue_commands"] else "Read-only"
        print(f"  {i}. {role} ({perms}, {cmd_auth})")

    print()

    while True:
        try:
            choice = input("Enter role number (1-6): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(roles):
                role = roles[idx]
                result = login(role)
                if result["status"] == "success":
                    print(f"\nLogin successful! Current role: {role}")
                    return result["data"]
                else:
                    print(f"Login failed: {result['error']}")
            else:
                print("Invalid selection, please try again")
        except ValueError:
            print("Please enter a number")
        except KeyboardInterrupt:
            print("\nCancelled")
            sys.exit(0)


def create_provider():
    """Create LLM Provider"""
    config = ProviderConfig()

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
    print("  Energy Management Assistant v1.0.0")
    print("=" * 50)
    print()

    # 1. User login and role selection
    print("[1] User login...")
    session = select_role()

    # 2. Load system prompt
    print("\n[2] Loading system prompt...")
    system_prompt = load_system_prompt()
    print(f"  Loaded {len(system_prompt)} characters")

    # 3. Create ToolContext and tool registry
    print("\n[3] Creating tool registry...")
    context = ToolContext()
    context.set("session", session)  # Store session info in context
    registry = ToolRegistry(context)

    # 4. Scan and register tools
    print("\n[4] Scanning and registering tools...")
    tool_count = scan_and_register_tools(registry)
    print(f"\n  Total {tool_count} tools registered")

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

    print("\nSystem ready. Enter a message to start the conversation...")
    print("Enter 'quit' or 'exit' to exit")
    print()

    # 7. Interaction loop
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