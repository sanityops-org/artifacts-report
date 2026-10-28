#!/usr/bin/env python3
"""Transaction skill processor"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from tools.trade_api import TradeAPI
from tools.market_data import MarketData
from risk.amount_checker import AmountChecker
from risk.password_verifier import PasswordVerifier


class StockTradingHandler:
    """Transaction skill processor

    Handle the business related to stock trading:
    - Inquire about the position
    - Query and entrust
    - Inquire about the transaction
    - Buy stocks
    - Sell stocks
    - Withdraw the order
    """

    def __init__(self):
        self.trade_api = TradeAPI()
        self.market_data = MarketData()
        self.amount_checker = AmountChecker()
        self.password_verifier = PasswordVerifier()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")
        action_params = params.get("params", {})

        action_map = {
            "query_position": self.query_position,
            "query_orders": self.query_orders,
            "query_deals": self.query_deals,
            "buy_stock": self.buy_stock,
            "sell_stock": self.sell_stock,
            "cancel_order": self.cancel_order
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}"
            }

        return action_map[action](**action_params)

    def query_position(self, user_id: str) -> Dict[str, Any]:
        """Inquire about the position"""
        result = self.trade_api.get_position(user_id)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }

    def query_orders(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Inquire about the power of attorney"""
        result = self.trade_api.get_orders(user_id, status)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }

    def query_deals(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Check the transaction record"""
        result = self.trade_api.get_deals(user_id, limit)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }

    def buy_stock(self, user_id: str, stock_code: str, quantity: int,
                  price: Optional[float] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Buy stocks"""
        # Get the price
        if price is None:
            quote_result = self.market_data.get_quote(stock_code)
            if quote_result["status"] != "success":
                return {
                    "status": "error",
                    "message": f"Unable to get the market price of stock {stock_code}"
                }
            price = quote_result["data"]["price"]

        amount = price * quantity

        # Check the balance
        balance = self.trade_api.get_balance(user_id)
        if balance["data"]["available"] < amount:
            return {
                "status": "error",
                "message": f"Insufficient available funds, currently available: {balance['data']['available']:.2f} yuan, needed: {amount:.2f} yuan"
            }

        # Check whether you need a password.
        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"The single amount {amount:.2f} exceeds the threshold, please enter the transaction password.",
                    "data": {
                        **check_result,
                        "stock_code": stock_code,
                        "quantity": quantity,
                        "price": price,
                        "amount": amount
                    }
                }

            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        # Execute the order
        result = self.trade_api.place_order(user_id, stock_code, "buy", price, quantity)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": f"The entrustment is successful, the entrustment number: {result['data']['order_id']}",
                "data": {
                    **result["data"],
                    "need_password": check_result["need_password"]
                }
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Entrustment failed"),
                "data": result
            }

    def sell_stock(self, user_id: str, stock_code: str, quantity: int,
                   price: Optional[float] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Sell stocks"""
        # Get the price
        if price is None:
            quote_result = self.market_data.get_quote(stock_code)
            if quote_result["status"] != "success":
                return {
                    "status": "error",
                    "message": f"Unable to get the market price of stock {stock_code}"
                }
            price = quote_result["data"]["price"]

        amount = price * quantity

        # Check the position
        position = self.trade_api.get_position(user_id)
        stock_holdings = next(
            (p for p in position["data"]["positions"] if p["stock_code"] == stock_code),
            None
        )
        if not stock_holdings:
            return {
                "status": "error",
                "message": f"Not held: you do not hold stock {stock_code} and cannot sell it."
            }
        if stock_holdings["available"] < quantity:
            return {
                "status": "error",
                "message": f"The quantity available for sale is insufficient. Currently available for sale: {stock_holdings['available']} shares, needed: {quantity} shares"
            }

        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"The single amount {amount:.2f} exceeds the threshold, please enter the transaction password.",
                    "data": {**check_result, "stock_code": stock_code, "quantity": quantity, "price": price}
                }

            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        result = self.trade_api.place_order(user_id, stock_code, "sell", price, quantity)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": f"The entrustment is successful, the entrustment number: {result['data']['order_id']}",
                "data": {**result["data"], "need_password": check_result["need_password"]}
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Entrustment failed"),
                "data": result
            }

    def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Withdraw the order"""
        result = self.trade_api.cancel_order(user_id, order_id)
        return {
            "status": "success",
            "message": "Successful withdrawal of the order",
            "data": result["data"]
        }


# Create a global processor instance
_handler = StockTradingHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "query_position",
        "params": {"user_id": "test_user"}
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
