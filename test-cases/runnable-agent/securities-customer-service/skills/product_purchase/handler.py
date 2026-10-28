#!/usr/bin/env python3
"""Subscription skill processor"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from tools.trade_api import TradeAPI
from risk.amount_checker import AmountChecker
from risk.password_verifier import PasswordVerifier


class ProductPurchaseHandler:
    """Subscription skill processor

    Handle product subscription-related business:
    - Inquire about products that can be subscribed
    - Subscription financial management/fund
    - Redemption financial management/fund
    - Subscription of new shares/new bonds
    - Check the subscription record
    """

    def __init__(self):
        self.trade_api = TradeAPI()
        self.amount_checker = AmountChecker()
        self.password_verifier = PasswordVerifier()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")
        action_params = params.get("params", {})

        action_map = {
            "query_products": self.query_products,
            "purchase": self.purchase,
            "redeem": self.redeem,
            "new_stock_apply": self.new_stock_apply,
            "query_subscription": self.query_subscription
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}"
            }

        return action_map[action](**action_params)

    def query_products(self, user_id: str) -> Dict[str, Any]:
        """Inquire about products that can be subscribed"""
        result = self.trade_api.get_products(user_id)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }

    def purchase(self, user_id: str, product_code: str, amount: float,
                 password: Optional[str] = None) -> Dict[str, Any]:
        """Subscription financial management/fund"""
        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"The subscription amount {amount:.2f} yuan exceeds the threshold, please enter the transaction password.",
                    "data": {**check_result, "product_code": product_code, "amount": amount}
                }

            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        result = self.trade_api.purchase(user_id, product_code, amount)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": f"Successful application, application number: {result['data']['subscription_id']}",
                "data": {**result["data"], "need_password": check_result["need_password"]}
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Application failed"),
                "data": result
            }

    def redeem(self, user_id: str, product_code: str, amount: float,
               password: Optional[str] = None) -> Dict[str, Any]:
        """Redemption financial management/fund"""
        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"The redemption amount {amount:.2f} yuan exceeds the threshold, please enter the transaction password.",
                    "data": {**check_result, "product_code": product_code, "amount": amount}
                }

            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        result = self.trade_api.redeem(user_id, product_code, amount)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": result["data"]["message"],
                "data": {**result["data"], "need_password": check_result["need_password"]}
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Redemption failed"),
                "data": result
            }

    def new_stock_apply(self, user_id: str, stock_code: str, amount: float,
                        password: Optional[str] = None) -> Dict[str, Any]:
        """Subscription of new shares/new bonds"""
        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"The subscription amount {amount:.2f} yuan exceeds the threshold, please enter the transaction password.",
                    "data": {**check_result, "stock_code": stock_code, "amount": amount}
                }

            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        result = self.trade_api.new_stock_apply(user_id, stock_code, amount)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": result["data"]["message"],
                "data": {**result["data"], "need_password": check_result["need_password"]}
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Application failed"),
                "data": result
            }

    def query_subscription(self, user_id: str) -> Dict[str, Any]:
        """Check the subscription/signing record"""
        result = self.trade_api.get_subscription(user_id)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }


# Create a global processor instance
_handler = ProductPurchaseHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "query_products",
        "params": {"user_id": "test_user"}
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
