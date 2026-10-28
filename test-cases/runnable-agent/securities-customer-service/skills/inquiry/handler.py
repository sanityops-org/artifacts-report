#!/usr/bin/env python3
"""Consulting skill processor"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from tools.market_data import MarketData


class InquiryHandler:
    """Consulting skill processor

    Handle consulting-related business:
    - Check the stock market
    - Check the net value of the fund
    - Business handling guidelines
    """

    def __init__(self):
        self.market_data = MarketData()

    # Business Guidelines Knowledge Base
    GUIDES = {
        "How to transfer money": """Operation guidelines for bank-securities transfers:
1. Make sure the bank card is linked.
2. Enter "deposit 10,000 yuan" or "withdraw 5,000 yuan" in the conversation.
3. Large transfers over CNY 50,000 require the transaction password.""",
        "How to buy stocks": """Guidelines for buying stocks:
1. Check the stock price first, for example, "What is the current price of China Merchants Bank?"
2. Enter a purchase instruction, for example, "Buy 1,000 shares of China Merchants Bank."
3. The system confirms the stock code, quantity, and price.
4. Large transactions over CNY 50,000 require the transaction password.""",
        "How to sell stocks": """Guidelines for selling stocks:
1. Check the position first by selecting "Check position."
2. Enter a sell instruction, for example, "Sell 500 shares of China Merchants Bank."
3. Confirm the selling price.
4. Large transactions require password confirmation.""",
        "How to subscribe to funds": """Guidelines for fund subscriptions:
1. To view available products, select "Check available products."
2. Enter a subscription instruction, for example, "Subscribe CNY 10,000 to the Stable Growth Fund."
3. Confirm the purchase amount.
4. Large subscriptions require password confirmation.""",
        "Password error": """Transaction-password issues:
- Entering the wrong password three times locks the account.
- To reset a forgotten password, visit a sales department with identification.
- You can also reset the password through the app's "Forgot Transaction Password" function."""
    }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")
        action_params = params.get("params", {})

        action_map = {
            "query_quote": self.query_quote,
            "query_fund_nav": self.query_fund_nav,
            "business_guide": self.business_guide
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}"
            }

        return action_map[action](**action_params)

    def query_quote(self, stock_code: str) -> Dict[str, Any]:
        """Check the real-time stock market"""
        result = self.market_data.get_quote(stock_code)

        if result["status"] == "success":
            data = result["data"]
            return {
                "status": "success",
                "message": f"{data['name']}({data['code']}) Current price: {data['price']} yuan, up and down: {data['change_pct']:+.2f}%",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Query failed"),
                "data": {}
            }

    def query_fund_nav(self, fund_code: str) -> Dict[str, Any]:
        """Check the net value of the fund"""
        result = self.market_data.get_fund_nav(fund_code)

        if result["status"] == "success":
            data = result["data"]
            return {
                "status": "success",
                "message": f"{data['name']}({data['code']}) Net unit value: {data['nav']} yuan（{data['nav_date']}）",
                "data": data
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Query failed"),
                "data": {}
            }

    def business_guide(self, topic: str) -> Dict[str, Any]:
        """Business handling guidelines"""
        # Keyword matching
        for key, guide in self.GUIDES.items():
            if key in topic:
                return {
                    "status": "success",
                    "message": guide,
                    "data": {"topic": key, "guide": guide}
                }

        # Default reply
        default_guide = "I can help you deal with the following business:\n" + \
                       "- Bank certificate transfer (deposit/withdrawal)\n" + \
                       "- Stock trading and withdrawal of orders\n" + \
                       "- Subscription and redemption of funds/financial products\n" + \
                       "- Subscription of new shares\n" + \
                       "- Market inquiry\n\n" + \
                       "Excuse me, which business do you need?"

        return {
            "status": "success",
            "message": default_guide,
            "data": {"topic": "default", "guide": default_guide}
        }


# Create a global processor instance
_handler = InquiryHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "query_quote",
        "params": {"stock_code": "600036"}
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
