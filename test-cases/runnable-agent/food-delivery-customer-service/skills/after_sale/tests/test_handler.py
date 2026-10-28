#!/usr/bin/env python3
"""After-sales service skills test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.after_sale.handler import main
from tools.order_api import OrderAPI


class TestAfterSaleHandler:
    """After-sales service skill test category"""

    def setup_method(self):
        self.user_id = "test_user_001"
        self.order_api = OrderAPI()

    def test_apply_refund_auto(self):
        """Test application for automatic refund (unsupply ordered)"""
        # Create an order first
        create_result = self.order_api.create_order(
            user_id=self.user_id,
            items=[{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": order_id,
                "amount": 38.0,
                "reason": "I don't want it anymore"
            }
        })
        assert result["status"] == "success"
        assert "refund_id" in result["data"]
        assert result["data"]["decision"] == "auto"

    def test_apply_refund_manual(self):
        """Test application for refund transfer to labor (meal order has been delivered)"""
        result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD_DELIVERING_001",
                "amount": 50.0,
                "reason": "Commodity quality problems"
            }
        })
        assert result["status"] == "success"
        assert "ticket_id" in result["data"]
        assert result["data"]["decision"] == "manual"

    def test_apply_refund_completed_manual(self):
        """The test application for refund has been completed. The order has been transferred to labor."""
        result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD_COMPLETED_001",
                "amount": 60.0,
                "reason": "I don't want it anymore"
            }
        })
        # Completed orders also need to be transferred manually.
        assert result["status"] == "success"
        assert result["data"]["decision"] == "manual"

    def test_apply_refund_not_refundable(self):
        """The test application refund is non-refundable (refunded order)"""
        result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD_REFUNDED_001",
                "amount": 50.0,
                "reason": "I don't want it anymore"
            }
        })
        assert result["status"] == "error"
        assert result["data"]["decision"] == "not_refundable"

    def test_apply_refund_invalid_amount(self):
        """The refund amount of the test application is invalid."""
        result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD_PENDING_001",
                "amount": 0,
                "reason": "Test"
            }
        })
        assert result["status"] == "error"

    def test_query_refund(self):
        """Test inquiry refund"""
        # Apply for a refund first
        apply_result = main({
            "action": "apply_refund",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD_PENDING_001",
                "amount": 50.0,
                "reason": "Test refund"
            }
        })
        refund_id = apply_result["data"]["refund_id"]

        # Inquire about refund
        result = main({
            "action": "query_refund",
            "params": {"user_id": self.user_id, "refund_id": refund_id}
        })
        assert result["status"] == "success"
        assert result["data"]["refund_id"] == refund_id

    def test_query_refund_not_found(self):
        """Test query for non-existent refunds"""
        result = main({
            "action": "query_refund",
            "params": {"user_id": self.user_id, "refund_id": "NON_EXISTENT"}
        })
        assert result["status"] == "error"

    def test_create_ticket(self):
        """Test to create a work order"""
        result = main({
            "action": "create_ticket",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD001",
                "reason": "Abnormal distribution",
                "detail": "The rider was not delivered to the designated location."
            }
        })
        assert result["status"] == "success"
        assert "ticket_id" in result["data"]

    def test_create_ticket_empty_reason(self):
        """The reason for testing and creating a work order is empty."""
        result = main({
            "action": "create_ticket",
            "params": {
                "user_id": self.user_id,
                "order_id": "FD001",
                "reason": "",
                "detail": "Test"
            }
        })
        assert result["status"] == "error"

    def test_unknown_action(self):
        """Test unknown operations"""
        result = main({
            "action": "unknown_action",
            "params": {}
        })
        assert result["status"] == "error"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
