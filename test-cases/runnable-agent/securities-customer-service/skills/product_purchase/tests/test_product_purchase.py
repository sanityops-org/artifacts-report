#!/usr/bin/env python3
"""Application skills test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.product_purchase.handler import main


class TestProductPurchaseHandler:
    """Application type skill test class"""

    def setup_method(self):
        self.user_id = "test_user_001"

    def test_query_products(self):
        """Test and query the products that can be subscribed"""
        result = main({
            "action": "query_products",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "products" in result["data"]

    def test_purchase_small_amount(self):
        """Test small subscription"""
        result = main({
            "action": "purchase",
            "params": {
                "user_id": self.user_id,
                "product_code": "FUND001",
                "amount": 10000
            }
        })
        assert result["status"] == "success"

    def test_purchase_large_amount_need_password(self):
        """Test large subscription (password required)"""
        result = main({
            "action": "purchase",
            "params": {
                "user_id": self.user_id,
                "product_code": "FUND001",
                "amount": 80000
            }
        })
        assert result["status"] == "need_password"

    def test_redeem(self):
        """Test redemption"""
        result = main({
            "action": "redeem",
            "params": {
                "user_id": self.user_id,
                "product_code": "FUND001",
                "amount": 5000
            }
        })
        assert result["status"] == "success"

    def test_new_stock_apply(self):
        """Test the subscription of new shares"""
        result = main({
            "action": "new_stock_apply",
            "params": {
                "user_id": self.user_id,
                "stock_code": "001001",
                "amount": 10000
            }
        })
        assert result["status"] == "success"

    def test_query_subscription(self):
        """Test and query the subscription record"""
        result = main({
            "action": "query_subscription",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "records" in result["data"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
