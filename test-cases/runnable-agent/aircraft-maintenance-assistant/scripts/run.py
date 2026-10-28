#!/usr/bin/env python3
"""
Agent Start the script

Start the aircraft maintenance airworthiness decision-making assistant Agent and run it using the sanityops_agent framework.
LLM Configuration through .env file settings (LLM_API_KEY, LLM_PROVIDER, etc.).
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sanityops_agent import (
    AgentConfig,
    AgentFactory,
    ProviderConfig,
    ToolRegistry,
    ToolContext,
    HookExecutor,
)
from sanityops_agent.llm.factory import ProviderFactory

# Import custom tools
from skills.airworthiness_advisor.tools.query_airworthiness import QueryAirworthinessTool
from skills.airworthiness_advisor.tools.query_component_status import QueryComponentStatusTool
from skills.airworthiness_advisor.tools.query_maintenance_history import QueryMaintenanceHistoryTool
from skills.airworthiness_advisor.tools.generate_decision import GenerateDecisionTool

from hooks.pretty_output_hook import PrettyOutputHook

def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a professional airworthiness decision-making assistant for aircraft maintenance."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(QueryAirworthinessTool(context))
    registry.register(QueryComponentStatusTool(context))
    registry.register(QueryMaintenanceHistoryTool(context))
    registry.register(GenerateDecisionTool(context))
    return registry


def create_provider():
    """Set up LLM Provider"""
    config = ProviderConfig(_env_file=(project_root / ".env", project_root.parent / ".env"))

    if not config.API_KEY:
        print("Warning: Not configured API Key")
        print()
        print("Please configure it in the .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # Someone openai")

    return ProviderFactory.create(config)


async def run_agent(user_input: str = None):
    """Be in motion Agent"""
    provider = create_provider()
    agent_config = AgentConfig()
    tool_registry = create_tool_registry()
    system_prompt = load_system_prompt()
    hook_executor = HookExecutor()
    hook_executor.register(PrettyOutputHook())
    factory = AgentFactory(
        provider=provider,
        config=agent_config,
        tool_registry=tool_registry,
        hook_executor=hook_executor
    )

    agent = factory.create_parent_agent(system_prompt=system_prompt)

    print(f"Aircraft maintenance airworthiness decision-making assistant launched")
    print(f"Model: {provider.model}")
    print("-" * 60)

    if user_input:
        result = await agent.run(user_input)
        print("\n" + "=" * 60)
        print("Decision-making results:")
        print("=" * 60)
        if hasattr(result, 'text'):
            print(result.text)
        elif hasattr(result, 'content'):
            print(result.content)
        else:
            print(str(result))
        return result
    else:
        print("Please enter the query (enter 'exit' to exit):")
        print("Example: Query the airworthiness status of B-1234 aircraft PN-12345 parts")
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break
                if not user_input:
                    continue

                result = await agent.run(user_input)
                print("\n" + "-" * 40)
                if hasattr(result, 'text'):
                    print(result.text)
                elif hasattr(result, 'content'):
                    print(result.content)
                else:
                    print(str(result))

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


def main():
    """Main entrance"""
    import argparse

    parser = argparse.ArgumentParser(description="Airworthiness decision-making assistant for aircraft maintenance")
    parser.add_argument("--input", "-i", type=str, help="Query content")
    args = parser.parse_args()

    try:
        asyncio.run(run_agent(args.input))
        return 0
    except Exception as e:
        print(f"Failed to run: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
