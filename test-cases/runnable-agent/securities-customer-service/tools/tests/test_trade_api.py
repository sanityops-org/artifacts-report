#!/usr/bin/env python3
"""Transaction interface unit test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.trade_api import TradeAPI


class TestTradeAPI:
    """Transaction interface test class"""

    def setup_method(self):
        self.api = TradeAPI()
        self.user_id = "test_user_001"

    def test_get_balance(self):
        """Test to check the balance"""
        result = self.api.get_balance(self.user_id)
        assert result["status"] == "success"
        assert "balance" in result["data"]
        assert "available" in result["data"]

    def test_bank_transfer_in(self):
        """Test bank certificate transfer - deposit"""
        result = self.api.bank_transfer(
            user_id=self.user_id,
            amount=10000,
            direction="in"
        )
        assert result["status"] == "success"
        assert result["data"]["amount"] == 10000
        assert result["data"]["direction"] == "in"

    def test_bank_transfer_out(self):
        """Test bank certificate transfer - withdrawal"""
        result = self.api.bank_transfer(
            user_id=self.user_id,
            amount=5000,
            direction="out"
        )
        assert result["status"] == "success"
        assert result["data"]["direction"] == "out"

    def test_get_position(self):
        """Test and query the position"""
        result = self.api.get_position(self.user_id)
        assert result["status"] == "success"
        assert isinstance(result["data"]["positions"], list)

    def test_place_order(self):
        """Test and place an order"""
        result = self.api.place_order(
            user_id=self.user_id,
            stock_code="600036",
            direction="buy",
            price=36.50,
            quantity=1000
        )
        assert result["status"] == "success"
        assert "order_id" in result["data"]

    def test_cancel_order(self):
        """Test withdrawal order"""
        result = self.api.cancel_order(
            user_id=self.user_id,
            order_id="202609030001"
        )
        assert result["status"] == "success"

    def test_get_products(self):
        """Test and query the products that can be subscribed"""
        result = self.api.get_products(self.user_id)
        assert result["status"] == "success"
        assert isinstance(result["data"]["products"], list)

    def test_purchase(self):
        """Test and apply"""
        result = self.api.purchase(
            user_id=self.user_id,
            product_code="FUND001",
            amount=10000
        )
        assert result["status"] == "success"

    def test_redeem(self):
        """Test redemption"""
        result = self.api.redeem(
            user_id=self.user_id,
            product_code="FUND001",
            amount=5000
        )
        assert result["status"] == "success"

    def test_new_stock_apply(self):
        """Test the subscription of new shares"""
        result = self.api.new_stock_apply(
            user_id=self.user_id,
            stock_code="001001",
            amount=10000
        )
        assert result["status"] == "success"

    def test_get_subscription(self):
        """Test and query the subscription record"""
        result = self.api.get_subscription(self.user_id)
        assert result["status"] == "success"
        assert isinstance(result["data"]["records"], list)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
