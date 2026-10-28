#!/usr/bin/env python3
"""Capital skills test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.fund_operation.handler import main


class TestFundOperationHandler:
    """Capital skill test class"""

    def setup_method(self):
        self.user_id = "test_user_001"

    def test_query_balance(self):
        """Test to check the balance"""
        result = main({
            "action": "query_balance",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "balance" in result["data"]

    def test_bank_transfer_in_small_amount(self):
        """Test small deposit (no password required)"""
        result = main({
            "action": "bank_transfer",
            "params": {
                "user_id": self.user_id,
                "amount": 10000,
                "direction": "in"
            }
        })
        assert result["status"] == "success"
        assert result["data"]["need_password"] is False

    def test_bank_transfer_in_large_amount_need_password(self):
        """Test large deposit (password required)"""
        result = main({
            "action": "bank_transfer",
            "params": {
                "user_id": self.user_id,
                "amount": 80000,
                "direction": "in"
            }
        })
        assert result["status"] == "need_password"
        assert result["data"]["need_password"] is True

    def test_bank_transfer_with_correct_password(self):
        """Test large transfer and enter the correct password"""
        result = main({
            "action": "bank_transfer",
            "params": {
                "user_id": self.user_id,
                "amount": 80000,
                "direction": "in",
                "password": "123456"
            }
        })
        assert result["status"] == "success"

    def test_bank_transfer_with_wrong_password(self):
        """Test the large transfer and enter the wrong password"""
        result = main({
            "action": "bank_transfer",
            "params": {
                "user_id": self.user_id,
                "amount": 80000,
                "direction": "in",
                "password": "wrong"
            }
        })
        assert result["status"] == "error"
        assert "Wrong password" in result["message"]

    def test_query_transfer_records(self):
        """Test and query the transfer record"""
        result = main({
            "action": "query_transfer_records",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "records" in result["data"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
