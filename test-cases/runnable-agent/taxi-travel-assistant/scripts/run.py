#!/usr/bin/env python3
"""
Agent Start the script

Start the taxi travel assistant Agent and run it using the sanityops_agent framework.
"""

import sys
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

# Import tools
from skills.route_planning.tools.plan_route import PlanRouteTool
from skills.fare_estimation.tools.estimate_fare import EstimateFareTool
from skills.vehicle_query.tools.query_vehicle import QueryVehicleTool
from skills.order_booking.tools.place_order import PlaceOrderTool
from skills.order_booking.tools.cancel_order import CancelOrderTool


def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a taxi travel assistant."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(PlanRouteTool(context))
    registry.register(EstimateFareTool(context))
    registry.register(QueryVehicleTool(context))
    registry.register(PlaceOrderTool(context))
    registry.register(CancelOrderTool(context))
    return registry


def create_provider():
    """Set up LLM Provider"""
    config = ProviderConfig()

    if not config.API_KEY:
        print("Warning: Not configured API Key")
        print()
        print("Please configure it in the .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # Someone openai")

    from sanityops_agent.llm.factory import ProviderFactory
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

    print("Taxi travel assistant starts")
    print(f"Model: {provider.model}")
    print("-" * 60)

    if user_input:
        result = await agent.run(user_input)
        print("\n" + "=" * 60)
        if hasattr(result, 'text'):
            print(result.text)
        elif hasattr(result, 'content'):
            print(result.content)
        else:
            print(str(result))
        return result
    else:
        print("Please enter the query (enter 'exit' to exit):")
        print("Example: How much does it cost from Beijing West Railway Station to Capital Airport T3?")
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

    parser = argparse.ArgumentParser(description="Taxi travel assistant")
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
