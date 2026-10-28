#!/usr/bin/env python3
"""
Agent Start the script

Start the securities investment customer service Agent and use the sanityops_agent framework to run.
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
    Tool,
    ToolResult,
)
from sanityops_agent.llm.factory import ProviderFactory


# ============== Definition of tools ==============

class QueryBalanceTool(Tool):
    """Check the fund balance tool"""
    name = "query_balance"
    description = "Check the balance and available funds of the user's securities account"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "ConsumerID"
            }
        },
        "required": ["user_id"]
    }

    async def execute(self, user_id: str, **kwargs) -> ToolResult:
        from tools.trade_api import TradeAPI
        api = TradeAPI()
        result = api.get_balance(user_id)
        return ToolResult(
            content=result.get("message", "The query is successful"),
            success=result["status"] == "success",
            metadata=result["data"]
        )


class BankTransferTool(Tool):
    """Bank certificate transfer tool"""
    name = "bank_transfer"
    description = "Execute bank certificate transfer (deposit or withdrawal), and password verification is required for large-amount transfers."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "amount": {"type": "number", "description": "Transfer amount"},
            "direction": {"type": "string", "enum": ["in", "out"], "description": "Transfer direction: in = deposit, out = withdrawal"},
            "password": {"type": "string", "description": "Transaction password (reequired for large amounts)"}
        },
        "required": ["user_id", "amount", "direction"]
    }

    async def execute(self, user_id: str, amount: float, direction: str, password: str = None, **kwargs) -> ToolResult:
        from skills.fund_operation.handler import main
        result = main({
            "action": "bank_transfer",
            "params": {"user_id": user_id, "amount": amount, "direction": direction, "password": password}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class QueryPositionTool(Tool):
    """Query position tool"""
    name = "query_position"
    description = "Inquire about the user's stock position"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"}
        },
        "required": ["user_id"]
    }

    async def execute(self, user_id: str, **kwargs) -> ToolResult:
        from tools.trade_api import TradeAPI
        api = TradeAPI()
        result = api.get_position(user_id)
        return ToolResult(
            content="Position inquiry is successful",
            success=True,
            metadata=result["data"]
        )


class BuyStockTool(Tool):
    """Buy stock tools"""
    name = "buy_stock"
    description = "Buy designated stocks, and password verification is required for large transactions."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "stock_code": {"type": "string", "description": "Stock code"},
            "quantity": {"type": "integer", "description": "Purchase quantity (shares)"},
            "price": {"type": "number", "description": "Entrusted price (optional, use the current price if not passed)"},
            "password": {"type": "string", "description": "Transaction password (reequired for large amounts)"}
        },
        "required": ["user_id", "stock_code", "quantity"]
    }

    async def execute(self, user_id: str, stock_code: str, quantity: int, price: float = None, password: str = None, **kwargs) -> ToolResult:
        from skills.stock_trading.handler import main
        result = main({
            "action": "buy_stock",
            "params": {"user_id": user_id, "stock_code": stock_code, "quantity": quantity, "price": price, "password": password}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class SellStockTool(Tool):
    """Sell stock tools"""
    name = "sell_stock"
    description = "Sell designated stocks, and password verification is required for large transactions."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "stock_code": {"type": "string", "description": "Stock code"},
            "quantity": {"type": "integer", "description": "Selling quantity (shares)"},
            "price": {"type": "number", "description": "Entrusted price (optional)"},
            "password": {"type": "string", "description": "Transaction password (reequired for large amounts)"}
        },
        "required": ["user_id", "stock_code", "quantity"]
    }

    async def execute(self, user_id: str, stock_code: str, quantity: int, price: float = None, password: str = None, **kwargs) -> ToolResult:
        from skills.stock_trading.handler import main
        result = main({
            "action": "sell_stock",
            "params": {"user_id": user_id, "stock_code": stock_code, "quantity": quantity, "price": price, "password": password}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class QueryQuoteTool(Tool):
    """Query the market tool"""
    name = "query_quote"
    description = "Check the real-time stock market"
    parameters = {
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code"}
        },
        "required": ["stock_code"]
    }

    async def execute(self, stock_code: str, **kwargs) -> ToolResult:
        from skills.inquiry.handler import main
        result = main({
            "action": "query_quote",
            "params": {"stock_code": stock_code}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result.get("data", {})
        )


class BusinessGuideTool(Tool):
    """Business guidance tool"""
    name = "business_guide"
    description = "Provide business handling guidelines and help"
    parameters = {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Consulting topics, such as: how to transfer money, how to buy stocks"}
        },
        "required": ["topic"]
    }

    async def execute(self, topic: str, **kwargs) -> ToolResult:
        from skills.inquiry.handler import main
        result = main({
            "action": "business_guide",
            "params": {"topic": topic}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=True,
            metadata=result.get("data", {})
        )


# ============== Startup logic ==============

def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a securities investment customer service assistant, helping customers handle fund transfer, stock trading, product subscription and other business."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)

    # Financial tools
    registry.register(QueryBalanceTool(context))
    registry.register(BankTransferTool(context))

    # Trading tools
    registry.register(QueryPositionTool(context))
    registry.register(BuyStockTool(context))
    registry.register(SellStockTool(context))

    # Consulting tools
    registry.register(QueryQuoteTool(context))
    registry.register(BusinessGuideTool(context))

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
        print()
        print("Optional configuration:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")

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

    print("Securities Investment Customer Service Agent Launch")
    print(f"Model: {provider.model}")
    print("-" * 60)
    print("I can help you.:")
    print("  - Check the balance and transfer the bank certificate")
    print("  - Stock trading and position inquiry")
    print("  - Market inquiry, business guidelines")
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
        print("Please enter your needs (enter 'exit' to exit):")
        print("Example: Check my balance, how much is China Merchants Bank now, buy 100 shares of China Merchants Bank")
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

    parser = argparse.ArgumentParser(description="Securities investment customer service Agent")
    parser.add_argument("--input", "-i", type=str, help="Enter the query content directly")
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
