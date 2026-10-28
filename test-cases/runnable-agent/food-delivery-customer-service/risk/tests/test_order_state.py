#!/usr/bin/env python3
"""Order status test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from risk.order_state import OrderStatus


class TestOrderStatus:
    """Order status test class"""

    def test_status_constants_exist(self):
        """The test state constant exists"""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.PAID == "paid"
        assert OrderStatus.PREPARING == "preparing"
        assert OrderStatus.DELIVERING == "delivering"
        assert OrderStatus.COMPLETED == "completed"
        assert OrderStatus.CANCELLED == "cancelled"
        assert OrderStatus.REFUNDED == "refunded"

    def test_is_refundable_for_pending(self):
        """Test the status of pending payment can be refunded"""
        assert OrderStatus.is_refundable(OrderStatus.PENDING) is True

    def test_is_refundable_for_paid(self):
        """Test the paid status can be refunded"""
        assert OrderStatus.is_refundable(OrderStatus.PAID) is True

    def test_is_refundable_for_preparing(self):
        """The status of test preparation can be refunded."""
        assert OrderStatus.is_refundable(OrderStatus.PREPARING) is True

    def test_is_refundable_for_delivering(self):
        """The status of test delivery cannot be automatically refunded."""
        assert OrderStatus.is_refundable(OrderStatus.DELIVERING) is False

    def test_is_refundable_for_completed(self):
        """The test has been completed and cannot be automatically refunded."""
        assert OrderStatus.is_refundable(OrderStatus.COMPLETED) is False

    def test_is_refundable_for_cancelled(self):
        """The test has been canceled and cannot be refunded."""
        assert OrderStatus.is_refundable(OrderStatus.CANCELLED) is False

    def test_is_refundable_for_refunded(self):
        """The test has been refunded and cannot be refunded again."""
        assert OrderStatus.is_refundable(OrderStatus.REFUNDED) is False

    def test_is_manual_for_delivering(self):
        """The status of test distribution needs to be handled manually."""
        assert OrderStatus.is_manual(OrderStatus.DELIVERING) is True

    def test_is_manual_for_completed(self):
        """The test is completed and needs to be handled manually."""
        assert OrderStatus.is_manual(OrderStatus.COMPLETED) is True

    def test_is_manual_for_pending(self):
        """The test pending payment status does not need manual processing."""
        assert OrderStatus.is_manual(OrderStatus.PENDING) is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
