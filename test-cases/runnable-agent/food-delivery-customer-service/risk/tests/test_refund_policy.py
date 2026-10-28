#!/usr/bin/env python3
"""Refund strategy test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from risk.refund_policy import RefundPolicy
from risk.order_state import OrderStatus


class TestRefundPolicy:
    """Refund strategy test class"""

    def test_decide_pending_auto(self):
        """Test the automatic refund of pending orders"""
        result = RefundPolicy.decide(OrderStatus.PENDING)
        assert result["decision"] == "auto"
        assert "The meal has not been served" in result["reason"]

    def test_decide_paid_auto(self):
        """Test the automatic refund of paid orders"""
        result = RefundPolicy.decide(OrderStatus.PAID)
        assert result["decision"] == "auto"
        assert "The meal has not been served" in result["reason"]

    def test_decide_preparing_auto(self):
        """Automatic refund of orders in the test meal preparation"""
        result = RefundPolicy.decide(OrderStatus.PREPARING)
        assert result["decision"] == "auto"
        assert "The meal has not been served" in result["reason"]

    def test_decide_delivering_manual(self):
        """Transfer orders to manual during testing and distribution"""
        result = RefundPolicy.decide(OrderStatus.DELIVERING)
        assert result["decision"] == "manual"
        assert "The meal has been served." in result["reason"]

    def test_decide_completed_manual(self):
        """The test has been completed and the order has been transferred to manual."""
        result = RefundPolicy.decide(OrderStatus.COMPLETED)
        assert result["decision"] == "manual"
        assert "The meal has been served." in result["reason"]

    def test_decide_cancelled_not_refundable(self):
        """The test has been canceled and the order is non-refundable."""
        result = RefundPolicy.decide(OrderStatus.CANCELLED)
        assert result["decision"] == "not_refundable"
        assert "Canceled" in result["reason"]

    def test_decide_refunded_not_refundable(self):
        """The test has been refunded and the order can no longer be refunded."""
        result = RefundPolicy.decide(OrderStatus.REFUNDED)
        assert result["decision"] == "not_refundable"
        assert "Refunded" in result["reason"]

    def test_decide_unknown_status(self):
        """The test unknown status is non-refundable."""
        result = RefundPolicy.decide("unknown_status")
        assert result["decision"] == "not_refundable"
        assert "Unable to identify" in result["reason"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
