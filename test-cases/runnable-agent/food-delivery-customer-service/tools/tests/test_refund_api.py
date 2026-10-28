#!/usr/bin/env python3
"""Refund API test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.refund_api import RefundAPI


class TestRefundAPI:
    """Refund API test class"""

    def setup_method(self):
        self.api = RefundAPI()
        self.user_id = "test_user_001"

    def test_apply_refund_success(self):
        """The test application for refund is successful"""
        result = self.api.apply_refund(
            user_id=self.user_id,
            order_id="FD_PENDING_001",
            amount=50.0,
            reason="I don't want it anymore"
        )
        assert result["status"] == "success"
        assert "refund_id" in result["data"]
        assert result["data"]["amount"] == 50.0

    def test_apply_refund_zero_amount(self):
        """The test refund amount is zero."""
        result = self.api.apply_refund(
            user_id=self.user_id,
            order_id="FD_PENDING_001",
            amount=0,
            reason="Test"
        )
        assert result["status"] == "error"
        assert "Refund amount" in result["error"]

    def test_apply_refund_negative_amount(self):
        """The test refund amount is negative."""
        result = self.api.apply_refund(
            user_id=self.user_id,
            order_id="FD_PENDING_001",
            amount=-10,
            reason="Test"
        )
        assert result["status"] == "error"
        assert "Refund amount" in result["error"]

    def test_apply_refund_empty_reason(self):
        """The reason for the test refund is empty."""
        result = self.api.apply_refund(
            user_id=self.user_id,
            order_id="FD_PENDING_001",
            amount=50.0,
            reason=""
        )
        assert result["status"] == "error"
        assert "reason" in result["error"].lower()

    def test_get_refund_success(self):
        """Test inquiry refund successful"""
        # Apply for a refund first
        apply_result = self.api.apply_refund(
            user_id=self.user_id,
            order_id="FD_PENDING_001",
            amount=50.0,
            reason="Test refund"
        )
        refund_id = apply_result["data"]["refund_id"]

        # Inquire about refund
        result = self.api.get_refund(self.user_id, refund_id)
        assert result["status"] == "success"
        assert result["data"]["refund_id"] == refund_id

    def test_get_refund_not_found(self):
        """Test query for non-existent refunds"""
        result = self.api.get_refund(self.user_id, "NON_EXISTENT_REFUND")
        assert result["status"] == "error"
        assert "does not exist" in result["error"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
