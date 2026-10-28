#!/usr/bin/env python3
"""After-sales service skill processor"""

import sys
from pathlib import Path
from typing import Dict, Any

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from tools.order_api import OrderAPI
from tools.refund_api import RefundAPI
from tools.ticket_api import TicketAPI
from risk.refund_policy import RefundPolicy


class AfterSaleHandler:
    """After-sales service skill processor

    Handle refund and after-sales related business:
    - Apply for a refund (automatic refund or transfer according to the order status)
    - Check the progress of the refund
    - Create a manual work order
    """

    def __init__(self):
        self.order_api = OrderAPI()
        self.refund_api = RefundAPI()
        self.ticket_api = TicketAPI()
        self.refund_policy = RefundPolicy()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")
        action_params = params.get("params", {})

        action_map = {
            "apply_refund": self.apply_refund,
            "query_refund": self.query_refund,
            "create_ticket": self.create_ticket
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}",
                "data": {}
            }

        return action_map[action](**action_params)

    def apply_refund(
        self,
        user_id: str,
        order_id: str,
        amount: float,
        reason: str
    ) -> Dict[str, Any]:
        """Apply for a refund

        Judge according to the order status:
        - Unsuppled → Automatic refund
        - Meals have been served → Transfer manual work order

        Args:
            user_id: ConsumerID
            order_id: Order number
            amount: Refund amount
            reason: Reason for refund

        Returns:
            Refund result
        """
        # Check the order
        order_result = self.order_api.get_order(user_id, order_id)

        if order_result["status"] != "success":
            return {
                "status": "error",
                "message": order_result.get("error", "Failed to query the order"),
                "data": order_result
            }

        order = order_result["data"]
        order_status = order["status"]

        # Verification of refund amount
        if amount <= 0:
            return {"status": "error", "message": "The refund amount must be greater than0", "data": {"order_id": order_id}}
        if amount > order["total"]:
            return {"status": "error", "message": f"The refund amount cannot exceed the order amount {order['total']} yuan", "data": {"order_id": order_id, "order_total": order["total"]}}

        # Determine the refund strategy
        policy = self.refund_policy.decide(order_status)

        if policy["decision"] == "not_refundable":
            return {
                "status": "error",
                "message": f"Unable to apply for a refund: {policy['reason']}",
                "data": {"order_id": order_id, "decision": "not_refundable"}
            }

        if policy["decision"] == "auto":
            # Unsuppled → Automatic refund
            refund_result = self.refund_api.apply_refund(user_id, order_id, amount, reason)

            if refund_result["status"] == "success":
                return {
                    "status": "success",
                    "message": f"The refund application has been submitted, and the refund amount is {amount} yuan, which is expected to arrive in 1-3 working days.",
                    "data": {
                        **refund_result["data"],
                        "decision": "auto",
                        "order_id": order_id
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": refund_result.get("error", "The refund application failed."),
                    "data": refund_result
                }

        else:
            # Meals have been served → Transfer labor
            ticket_result = self.ticket_api.create_ticket(
                user_id,
                order_id,
                f"Refund application: {reason}",
                f"Order status: {order_status}, refund amount applied for: {amount} yuan, reason: {reason}"
            )

            if ticket_result["status"] == "success":
                return {
                    "status": "success",
                    "message": f"The order has been served and has been processed manually for you. Work order number: {ticket_result['data']['ticket_id']}, the exclusive customer service will contact you within 30 minutes.",
                    "data": {
                        **ticket_result["data"],
                        "decision": "manual",
                        "order_id": order_id
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": ticket_result.get("error", "Failed to create a work order"),
                    "data": ticket_result
                }

    def query_refund(self, user_id: str, refund_id: str) -> Dict[str, Any]:
        """Check the progress of the refund

        Args:
            user_id: ConsumerID
            refund_id: Refund order number

        Returns:
            Refund details
        """
        result = self.refund_api.get_refund(user_id, refund_id)

        if result["status"] == "success":
            refund = result["data"]
            return {
                "status": "success",
                "message": f"Refund order {refund_id} Status: {refund['status']}, expected {refund['estimated_arrival']} to the account",
                "data": refund
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to inquire about refund"),
                "data": result
            }

    def create_ticket(
        self,
        user_id: str,
        order_id: str,
        reason: str,
        detail: str
    ) -> Dict[str, Any]:
        """Create a manual work order

        Args:
            user_id: ConsumerID
            order_id: Order number
            reason: The reason for the work order
            detail: Detailed description

        Returns:
            The result of work order creation
        """
        result = self.ticket_api.create_ticket(user_id, order_id, reason, detail)

        if result["status"] == "success":
            ticket = result["data"]
            return {
                "status": "success",
                "message": f"A manual work order has been created for you, work order number: {ticket['ticket_id']}, and the exclusive customer service will contact you at {ticket['estimated_response']}",
                "data": ticket
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to create a work order"),
                "data": result
            }


# Create a global processor instance
_handler = AfterSaleHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "apply_refund",
        "params": {
            "user_id": "test_user",
            "order_id": "FD_PENDING_001",
            "amount": 50.0,
            "reason": "I don't want it anymore"
        }
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
