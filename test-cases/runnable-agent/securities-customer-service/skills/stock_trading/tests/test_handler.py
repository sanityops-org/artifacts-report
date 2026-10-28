#!/usr/bin/env python3
"""Trading skills test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.stock_trading.handler import main


class TestStockTradingHandler:
    """Trading skills test class"""

    def setup_method(self):
        self.user_id = "test_user_001"

    def test_query_position(self):
        """Test and query the position"""
        result = main({
            "action": "query_position",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "positions" in result["data"]

    def test_query_orders(self):
        """Test query entrustment"""
        result = main({
            "action": "query_orders",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "orders" in result["data"]

    def test_query_deals(self):
        """Test query transaction"""
        result = main({
            "action": "query_deals",
            "params": {"user_id": self.user_id}
        })
        assert result["status"] == "success"
        assert "deals" in result["data"]

    def test_buy_stock_small_amount(self):
        """Test small purchase (no password required)"""
        result = main({
            "action": "buy_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 100,
                "price": 36.50
            }
        })
        assert result["status"] == "success"
        assert result["data"]["need_password"] is False

    def test_buy_stock_large_amount_need_password(self):
        """Test large purchases (password required)"""
        result = main({
            "action": "buy_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 2000,
                "price": 36.50
            }
        })
        assert result["status"] == "need_password"

    def test_buy_stock_insufficient_balance(self):
        """Insufficient test purchase balance"""
        result = main({
            "action": "buy_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 10000,
                "price": 100.00
            }
        })
        assert result["status"] == "error"
        assert "Insufficient available funds" in result["message"]

    def test_buy_stock_with_correct_password(self):
        """Test large purchases and enter the correct password"""
        result = main({
            "action": "buy_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 2000,
                "price": 36.50,
                "password": "123456"
            }
        })
        assert result["status"] == "success"

    def test_buy_stock_with_wrong_password(self):
        """Test a large purchase and enter the wrong password"""
        result = main({
            "action": "buy_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 2000,
                "price": 36.50,
                "password": "wrong"
            }
        })
        assert result["status"] == "error"
        assert "Wrong password" in result["message"]

    def test_sell_stock(self):
        """Test and sell"""
        result = main({
            "action": "sell_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 100,
                "price": 36.50
            }
        })
        assert result["status"] == "success"

    def test_sell_stock_insufficient_position(self):
        """Test sell and hold insufficient positions"""
        result = main({
            "action": "sell_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "600036",
                "quantity": 10000,
                "price": 36.50
            }
        })
        assert result["status"] == "error"
        assert "The quantity available for sale is insufficient." in result["message"]

    def test_sell_stock_not_held(self):
        """Test to sell unheld stocks"""
        result = main({
            "action": "sell_stock",
            "params": {
                "user_id": self.user_id,
                "stock_code": "999999",
                "quantity": 100,
                "price": 10.00
            }
        })
        assert result["status"] == "error"
        assert "Not held" in result["message"]

    def test_cancel_order(self):
        """Test withdrawal order"""
        result = main({
            "action": "cancel_order",
            "params": {
                "user_id": self.user_id,
                "order_id": "202609030001"
            }
        })
        assert result["status"] == "success"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
