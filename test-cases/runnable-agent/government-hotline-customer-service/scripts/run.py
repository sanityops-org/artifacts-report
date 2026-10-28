#!/usr/bin/env python3
"""
Agent Start the script

Launch the government hotline intelligent customer service Agent and run it using the sanityops_agent framework.
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
)
from sanityops_agent.llm.factory import ProviderFactory

# Import custom tools
from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool
from skills.government_ticket.tools.ticket_store import TicketStoreTool


def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are the intelligent customer service assistant of the government hotline, specializing in receiving complaints, suggestions and consultations from citizens."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(DispatchEngineTool(context))
    registry.register(TicketStoreTool(context))
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

    factory = AgentFactory(
        provider=provider,
        config=agent_config,
        tool_registry=tool_registry,
    )

    agent = factory.create_parent_agent(system_prompt=system_prompt)

    print("Government hotline intelligent customer service launched")
    print(f"Model: {provider.model}")
    print("-" * 60)

    if user_input:
        result = await agent.run(user_input)
        print("\n" + "=" * 60)
        print("Processing results:")
        print("=" * 60)
        if hasattr(result, 'text'):
            print(result.text)
        elif hasattr(result, 'content'):
            print(result.content)
        else:
            print(str(result))
        return result
    else:
        print("Please enter your request (enter 'exit' to exit):")
        print("Example: I want to complain about the noise of construction at night in the community.")
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() == "exit":
                    print("Thank you for using it. Goodbye.!")
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
                print("\nThank you for using it. Goodbye.!")
                break


def main():
    """Main entrance"""
    import argparse

    parser = argparse.ArgumentParser(description="Government Hotline Intelligent Customer Service")
    parser.add_argument("--input", "-i", type=str, help="Directly enter the content of the appeal")
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
