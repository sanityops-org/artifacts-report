#!/usr/bin/env python3
"""Refund system interface packaging (simulated data)"""

from typing import Dict, Any, Optional
from datetime import datetime
import random


class RefundAPI:
    """Refund system interface packaging

    Simulate the takeaway refund system interface, including functions such as applying for refunds and checking refund progress.
    All data are analog data for development and testing.
    """

    # Class-level refund storage to ensure that all instances share the same mock data
    _refunds: Dict[str, Dict[str, Any]] = {}
    _refund_counter = 1000
    _initialized = False

    def __init__(self):
        """Initialize the refund interface"""
        if not RefundAPI._initialized:
            self._init_mock_refunds()
            RefundAPI._initialized = True

    def _init_mock_refunds(self):
        """Initialize simulated refund data"""
        pass

    def _generate_refund_id(self) -> str:
        """Generate the refund order number"""
        RefundAPI._refund_counter += 1
        return f"RF{datetime.now().strftime('%Y%m%d')}{RefundAPI._refund_counter:04d}"

    def _success_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build a successful response"""
        return {
            "status": "success",
            "data": data,
            "error": "",
            "error_code": ""
        }

    def _error_response(self, error: str, code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
        """Build an error response"""
        return {
            "status": "error",
            "data": {},
            "error": error,
            "error_code": code
        }

    def apply_refund(
        self,
        user_id: str,
        order_id: str,
        amount: float,
        reason: str
    ) -> Dict[str, Any]:
        """Apply for a refund

        Args:
            user_id: ConsumerID
            order_id: Order number
            amount: Refund amount
            reason: Reason for refund

        Returns:
            The result of the refund application
        """
        # Parameter verification
        if amount <= 0:
            return self._error_response("Refund amount must be greater than 0.", "INVALID_AMOUNT")

        if not reason or not reason.strip():
            return self._error_response("The reason for the refund cannot be empty.", "EMPTY_REASON")

        # Generate a refund slip
        refund_id = self._generate_refund_id()
        refund = {
            "refund_id": refund_id,
            "user_id": user_id,
            "order_id": order_id,
            "amount": amount,
            "reason": reason,
            "status": "processing",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_arrival": "1-3Working day"
        }

        # Save the refund
        RefundAPI._refunds[refund_id] = refund

        return self._success_response(refund)

    def get_refund(self, user_id: str, refund_id: str) -> Dict[str, Any]:
        """Check the progress of the refund

        Args:
            user_id: ConsumerID
            refund_id: Refund order number

        Returns:
            Refund details
        """
        if refund_id not in RefundAPI._refunds:
            return self._error_response(f"The refund order {refund_id} does not exist", "REFUND_NOT_FOUND")

        refund = RefundAPI._refunds[refund_id]

        # Permission check
        if refund["user_id"] != user_id:
            return self._error_response("I don't have the right to view the refund slip.", "PERMISSION_DENIED")

        return self._success_response(refund)


if __name__ == "__main__":
    # Local test
    api = RefundAPI()
    print("Test and apply for a refund:")
    result = api.apply_refund(
        user_id="test_user",
        order_id="FD001",
        amount=50.0,
        reason="I don't want it anymore"
    )
    print(result)
