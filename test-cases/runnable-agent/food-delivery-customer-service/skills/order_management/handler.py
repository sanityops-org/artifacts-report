#!/usr/bin/env python3
"""Order management skill processor"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from tools.order_api import OrderAPI
from tools.refund_api import RefundAPI
from risk.refund_policy import RefundPolicy


class OrderManagementHandler:
    """Order management skill processor

    Handle order-related business:
    - Create an order (place an order)
    - Check the order
    - Follow up on the order
    - Modify the order
    - Cancel the order
    """

    def __init__(self):
        self.order_api = OrderAPI()
        self.refund_api = RefundAPI()
        self.refund_policy = RefundPolicy()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")
        action_params = params.get("params", {})

        action_map = {
            "create_order": self.create_order,
            "query_order": self.query_order,
            "remind_order": self.remind_order,
            "modify_order": self.modify_order,
            "cancel_order": self.cancel_order
        }

        if action not in action_map:
            return {
                "status": "error",
                "message": f"Unknown operation type: {action}",
                "data": {}
            }

        return action_map[action](**action_params)

    def create_order(
        self,
        user_id: str,
        items: List[Dict[str, Any]],
        address: str,
        remark: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an order

        Args:
            user_id: ConsumerID
            items: List of goods
            address: Delivery address
            remark: Remarks (optional)

        Returns:
            Create results
        """
        result = self.order_api.create_order(user_id, items, address, remark)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": f"The order was created successfully, and the order number: {result['data']['order_id']}",
                "data": result["data"]
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to create the order"),
                "data": result
            }

    def query_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Check the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            Order details
        """
        result = self.order_api.get_order(user_id, order_id)

        if result["status"] == "success":
            order = result["data"]
            return {
                "status": "success",
                "message": f"Order {order_id} Current status: {order['status']}",
                "data": order
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to query the order"),
                "data": result
            }

    def remind_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Follow up on the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            The result of the order reminder
        """
        result = self.order_api.remind_order(user_id, order_id)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": "The merchant has been notified to deal with it as soon as possible. Please wait patiently.",
                "data": result["data"]
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to urge the order"),
                "data": result
            }

    def modify_order(
        self,
        user_id: str,
        order_id: str,
        address: Optional[str] = None,
        remark: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Modify the order

        Args:
            user_id: ConsumerID
            order_id: Order number
            address: New address (optional)
            remark: New remarks (optional)
            items: List of new products (optional)

        Returns:
            Modified results
        """
        result = self.order_api.modify_order(user_id, order_id, address, remark, items)

        if result["status"] == "success":
            return {
                "status": "success",
                "message": "The order has been modified successfully",
                "data": result["data"]
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Order modification failed"),
                "data": result
            }

    def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Cancel the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            Cancellation results, including refund prompts
        """
        # Check the order status first.
        order_result = self.order_api.get_order(user_id, order_id)

        if order_result["status"] != "success":
            return {
                "status": "error",
                "message": order_result.get("error", "Failed to query the order"),
                "data": order_result
            }

        order_status = order_result["data"]["status"]

        # Execute and cancel
        result = self.order_api.cancel_order(user_id, order_id)

        if result["status"] == "success":
            # Judge the refund strategy
            policy = self.refund_policy.decide(order_status)

            if policy["decision"] == "auto":
                refund_amount = order_result["data"].get("total", 0)
                refund_result = self.refund_api.apply_refund(
                    user_id, order_id, refund_amount, "Automatic refund for canceling the order"
                )
                refund_status = refund_result["status"]
                refund_mark = {
                    "refund_created": refund_status == "success",
                    "refund_info": refund_result.get("data", {}),
                }
                return {
                    "status": "success",
                    "message": "The order has been canceled, and the refund will be processed automatically. It is expected to arrive in 1-3 working days" if refund_status == "success" else "The order has been canceled, and the refund is being processed. Please check later.",
                    "data": {
                        **result["data"],
                        "refund_decision": policy["decision"],
                        "refund_reason": policy["reason"],
                        **refund_mark,
                    }
                }
            else:
                # Defensive branch: It is impossible for the normal cancellation process to come this far (cancel the pre-check has been intercepted and served/delivered).
                # If you come here, it means that the status is abnormal, and you will be guided to change the manual.
                return {
                    "status": "error",
                    "message": "The order status is abnormal and cannot be refunded automatically. Please transfer to manual processing.",
                    "data": result["data"],
                }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Failed to cancel the order"),
                "data": result
            }


# Create a global processor instance
_handler = OrderManagementHandler()


def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """The main entrance of skills"""
    return _handler.execute(params)


if __name__ == "__main__":
    """Local test"""
    import json

    test_params = {
        "action": "create_order",
        "params": {
            "user_id": "test_user",
            "items": [{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
            "address": "Xxx Street, Chaoyang District, Beijing"
        }
    }
    result = main(test_params)
    print(json.dumps(result, indent=2, ensure_ascii=False))
