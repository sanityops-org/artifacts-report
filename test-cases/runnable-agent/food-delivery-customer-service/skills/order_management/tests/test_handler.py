#!/usr/bin/env python3
"""Order management skill test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.order_management.handler import main


class TestOrderManagementHandler:
    """Order management skills test class"""

    def setup_method(self):
        self.user_id = "test_user_001"

    def test_create_order(self):
        """Test to create an order"""
        result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
                "address": "Xxx Street, Chaoyang District, Beijing"
            }
        })
        assert result["status"] == "success"
        assert "order_id" in result["data"]

    def test_create_order_with_remark(self):
        """Test to create orders with notes"""
        result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Spicy hot pot", "quantity": 2, "price": 68.0}],
                "address": "Xxx Road, Haidian District, Beijing",
                "remark": "Less spicy"
            }
        })
        assert result["status"] == "success"
        assert result["data"]["remark"] == "Less spicy"

    def test_query_order(self):
        """Test and query orders"""
        # Create an order first
        create_result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Braised chicken and rice", "quantity": 1, "price": 25.0}],
                "address": "Xxx Street, Chaoyang District, Beijing"
            }
        })
        order_id = create_result["data"]["order_id"]

        # Check the order
        result = main({
            "action": "query_order",
            "params": {"user_id": self.user_id, "order_id": order_id}
        })
        assert result["status"] == "success"
        assert result["data"]["order_id"] == order_id

    def test_query_order_not_found(self):
        """Test query non-existent orders"""
        result = main({
            "action": "query_order",
            "params": {"user_id": self.user_id, "order_id": "NON_EXISTENT"}
        })
        assert result["status"] == "error"

    def test_remind_order(self):
        """Test reminder"""
        # Create an order first
        create_result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Hamburger set meal", "quantity": 1, "price": 35.0}],
                "address": "Xxx Street, Chaoyang District, Beijing"
            }
        })
        order_id = create_result["data"]["order_id"]

        result = main({
            "action": "remind_order",
            "params": {"user_id": self.user_id, "order_id": order_id}
        })
        assert result["status"] == "success"
        assert result["data"]["reminded"] is True

    def test_modify_order_address(self):
        """Test and modify the order address"""
        # Create an order first
        create_result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Pizza", "quantity": 1, "price": 58.0}],
                "address": "Xxx Street, Chaoyang District, Beijing"
            }
        })
        order_id = create_result["data"]["order_id"]

        result = main({
            "action": "modify_order",
            "params": {
                "user_id": self.user_id,
                "order_id": order_id,
                "address": "New address in Haidian District, Beijing"
            }
        })
        assert result["status"] == "success"
        assert result["data"]["address"] == "New address in Haidian District, Beijing"

    def test_cancel_order_success(self):
        """The test cancels the order successfully."""
        # Create an order first
        create_result = main({
            "action": "create_order",
            "params": {
                "user_id": self.user_id,
                "items": [{"name": "Fried chicken set meal", "quantity": 1, "price": 42.0}],
                "address": "Xxx Street, Chaoyang District, Beijing"
            }
        })
        order_id = create_result["data"]["order_id"]

        result = main({
            "action": "cancel_order",
            "params": {"user_id": self.user_id, "order_id": order_id}
        })
        assert result["status"] == "success"
        assert result["data"]["status"] == "cancelled"

    def test_cancel_order_delivering(self):
        """The order failed to test and cancel the delivery"""
        result = main({
            "action": "cancel_order",
            "params": {"user_id": self.user_id, "order_id": "FD_DELIVERING_001"}
        })
        assert result["status"] == "error"
        assert "Delivered" in result["message"]

    def test_unknown_action(self):
        """Test unknown operations"""
        result = main({
            "action": "unknown_action",
            "params": {}
        })
        assert result["status"] == "error"
        assert "Unknown" in result["message"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
