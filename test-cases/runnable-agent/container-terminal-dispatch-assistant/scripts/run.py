#!/usr/bin/env python3
"""
Container Terminal Dispatch Assistant - Agent Startup Script

Use the sanityops_agent framework to start the scheduling assistant Agent。
Automatically scan tools/ directory registration tools and load prompts/system.txt as system prompts.
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
    ToolRegistry,
    Tool,
    ToolResult,
    ToolContext,
    ProviderConfig,
)
from sanityops_agent.llm.factory import ProviderFactory
from apis.tos_api import login, ROLE_PERMISSIONS


def load_system_prompt() -> str:
    """Load system prompts"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are the dispatch assistant of the container terminal."


def scan_and_register_tools(registry: ToolRegistry) -> int:
    """
    Scan tools/ directory to automatically register all tools

    Each tool file requires:
    - The file name is the tool name (such as berth_query_vessel_plan.py）
    - The first line of module-level docstring is described as a tool
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

        # Create Tool packaging class - use type() to create dynamically to avoid closure problems
        execute_func = module.execute  # Capture closure
        tool_desc = description  # Capture description

        def make_execute(func, tool_name):
            async def execute(self, params: Dict[str, Any] | None = None, **kwargs) -> ToolResult:
                # Get session information from ToolContext
                session = self.context.get("session")
                try:
                    # Inject the session information into the parameters
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

        # Dynamically create Tool subclasses
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
        print(f"  Registration tools: {tool_name}")

    return count


def select_role() -> dict:
    """Select the login role"""
    print("\nPlease select the login role.:")
    roles = list(ROLE_PERMISSIONS.keys())
    for i, role in enumerate(roles, 1):
        perms = ", ".join(ROLE_PERMISSIONS[role]["permissions"])
        cmd_auth = "Can issue the instruction " if ROLE_PERMISSIONS[role]["can_issue_commands"] else "only query"
        print(f"  {i}. {role} ({perms}, {cmd_auth})")

    print()

    while True:
        try:
            choice = input("Please enter the role number. (1-6): ").strip()
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
                print("Invalid selection, please re-enter")
        except ValueError:
            print("Please enter the number.")
        except KeyboardInterrupt:
            print("\nCanceled")
            sys.exit(0)


def create_provider():
    """Set up LLM Provider"""
    config = ProviderConfig()

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
    print("  Container terminal dispatch assistant v1.0.0")
    print("=" * 50)
    print()

    # 1. Users log in and select roles
    print("[1] User login...")
    session = select_role()

    # 2. Load system prompts
    print("\n[2] Load system prompts...")
    system_prompt = load_system_prompt()
    print(f"  {Len(system_prompt)} characters have been loaded")

    # 3. Create ToolContext and tool registry
    print("\n[3] Create a tool registration form...")
    context = ToolContext()
    context.set("session", session)  # Deposit the session information into context
    registry = ToolRegistry(context)

    # 4. Scan and register tools
    print("\n[4] Scan and register tools...")
    tool_count = scan_and_register_tools(registry)
    print(f"\n  A total of {tool_count} tools have been registered")

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

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nWrong: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
