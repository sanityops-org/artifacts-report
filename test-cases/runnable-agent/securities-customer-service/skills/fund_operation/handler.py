#!/usr/bin/env python3
"""Capital skill processor"""

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


class FundOperationHandler:
    """Capital skill processor

    Handle fund-related business:
    - Check the balance
    - Bank certificate transfer (deposit/withdrawal)
    - Check the transfer record
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
            "query_balance": self.query_balance,
            "bank_transfer": self.bank_transfer,
            "query_transfer_records": self.query_transfer_records
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}"
            }

        return action_map[action](**action_params)

    def query_balance(self, user_id: str) -> Dict[str, Any]:
        """Check the balance of funds"""
        result = self.trade_api.get_balance(user_id)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }

    def bank_transfer(self, user_id: str, amount: float, direction: str,
                      password: Optional[str] = None) -> Dict[str, Any]:
        """Bank certificate transfer"""
        # Check whether the amount requires a password.
        check_result = self.amount_checker.check(amount)

        if check_result["need_password"]:
            if not password:
                return {
                    "status": "need_password",
                    "message": f"If the single amount exceeds {check_result['threshold']} yuan, please enter the transaction password.",
                    "data": check_result
                }

            # Verify the password
            verify_result = self.password_verifier.verify(user_id, password)
            if not verify_result["success"]:
                return {
                    "status": "error",
                    "message": verify_result["message"],
                    "data": {"error_code": verify_result["error_code"]}
                }

        # Execute the transfer
        result = self.trade_api.bank_transfer(user_id, amount, direction)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": "Successful deposit" if direction == "in" else "successful withdrawal",
                "data": {**result["data"], "need_password": check_result["need_password"]}
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Transfer failed"),
                "data": result
            }

    def query_transfer_records(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Check the transfer record"""
        result = self.trade_api.get_transfer_records(user_id, limit)
        return {
            "status": "success",
            "message": "The query is successful",
            "data": result["data"]
        }


# Create a global processor instance
_handler = FundOperationHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "query_balance",
        "params": {"user_id": "test_user"}
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
