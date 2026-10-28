#!/usr/bin/env python3
"""Order API test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.order_api import OrderAPI


class TestOrderAPI:
    """Order API test class"""

    def setup_method(self):
        self.api = OrderAPI()
        self.user_id = "test_user_001"

    def test_create_order_success(self):
        """Test to create the order successfully"""
        result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
            address="No. xxx, xxx Street, Chaoyang District, Beijing"
        )
        assert result["status"] == "success"
        assert "order_id" in result["data"]
        assert result["data"]["items"][0]["name"] == "Kung Pao Chicken"

    def test_create_order_with_remark(self):
        """Test to create orders with notes"""
        result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Spicy hot pot", "quantity": 2, "price": 68.0}],
            address="No. xxx, xxx Road, Haidian District, Beijing",
            remark="Add less spicy and more green onions."
        )
        assert result["status"] == "success"
        assert result["data"]["remark"] == "Add less spicy and more green onions."

    def test_create_order_empty_items(self):
        """Test to create an order item is empty"""
        result = self.api.create_order(
            user_id=self.user_id,
            items=[],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        assert result["status"] == "error"
        assert "The product list cannot be empty." in result["error"]

    def test_get_order_success(self):
        """Test query order successfully"""
        # Create an order first
        create_result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Braised chicken and rice", "quantity": 1, "price": 25.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        # Check the order
        result = self.api.get_order(self.user_id, order_id)
        assert result["status"] == "success"
        assert result["data"]["order_id"] == order_id

    def test_get_order_not_found(self):
        """Test query non-existent orders"""
        result = self.api.get_order(self.user_id, "NON_EXISTENT_ORDER")
        assert result["status"] == "error"
        assert "does not exist" in result["error"]

    def test_remind_order_success(self):
        """The test reminder is successful."""
        # Create an order first
        create_result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Hamburger set meal", "quantity": 1, "price": 35.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        result = self.api.remind_order(self.user_id, order_id)
        assert result["status"] == "success"
        assert result["data"]["reminded"] is True

    def test_modify_order_address(self):
        """Test and modify the order address"""
        # Create an order first
        create_result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Pizza", "quantity": 1, "price": 58.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        result = self.api.modify_order(
            user_id=self.user_id,
            order_id=order_id,
            address="New address No. xxx, Haidian District, Beijing"
        )
        assert result["status"] == "success"
        assert result["data"]["address"] == "New address No. xxx, Haidian District, Beijing"

    def test_modify_order_remark(self):
        """Test and modify order notes"""
        create_result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Sushi set meal", "quantity": 1, "price": 88.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        result = self.api.modify_order(
            user_id=self.user_id,
            order_id=order_id,
            remark="No mustard"
        )
        assert result["status"] == "success"
        assert result["data"]["remark"] == "No mustard"

    def test_cancel_order_success(self):
        """The test cancels the order successfully."""
        create_result = self.api.create_order(
            user_id=self.user_id,
            items=[{"name": "Fried chicken set meal", "quantity": 1, "price": 42.0}],
            address="Xxx Street, Chaoyang District, Beijing"
        )
        order_id = create_result["data"]["order_id"]

        result = self.api.cancel_order(self.user_id, order_id)
        assert result["status"] == "success"
        assert result["data"]["status"] == "cancelled"

    def test_cancel_order_already_delivering(self):
        """The order failed to test and cancel the delivery"""
        # Use the preset delivery order
        result = self.api.cancel_order(self.user_id, "FD_DELIVERING_001")
        assert result["status"] == "error"
        assert "Delivered" in result["error"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
