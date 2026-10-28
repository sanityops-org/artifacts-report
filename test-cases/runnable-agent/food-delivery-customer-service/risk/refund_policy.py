#!/usr/bin/env python3
"""Refund strategy judgment"""

from typing import Dict, Any
from .order_state import OrderStatus


class RefundPolicy:
    """Refund strategy judgment

    Decide how to process the refund according to the order status:
    - auto: Automatic refund is available (not served)
    - manual: Need to transfer to manual processing (meal has been served)
    - not_refundable: Non-refundable (cancelled/refunded)
    """

    @staticmethod
    def decide(order_status: str) -> Dict[str, Any]:
        """Determine how to handle the refund

        Args:
            order_status: Order status

        Returns:
            {
                "decision": "auto" | "manual" | "not_refundable",
                "reason": str
            }
        """
        # Unsuppled → Automatic refund
        if OrderStatus.is_refundable(order_status):
            return {
                "decision": "auto",
                "reason": "The meal has not been served. The order can be refunded automatically."
            }

        # Meals have been served → Transfer labor
        if OrderStatus.is_manual(order_status):
            return {
                "decision": "manual",
                "reason": "The meal has been served. The order requires manual review."
            }

        # Canceled/Refunded → Non-refundable
        if order_status == OrderStatus.CANCELLED:
            return {
                "decision": "not_refundable",
                "reason": "Canceled orders cannot be refunded."
            }

        if order_status == OrderStatus.REFUNDED:
            return {
                "decision": "not_refundable",
                "reason": "Refunded orders cannot be refunded again."
            }

        # Unknown status
        return {
            "decision": "not_refundable",
            "reason": "Unable to identify the order status; manual review is required."
        }


if __name__ == "__main__":
    # Local test
    from risk.order_state import OrderStatus

    for status in ["pending", "paid", "preparing", "delivering", "completed", "cancelled", "refunded"]:
        result = RefundPolicy.decide(status)
        print(f"{status}: {result}")
