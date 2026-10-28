#!/usr/bin/env python3
"""Order system interface encapsulation (simulated data)"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from risk.order_state import OrderStatus


class OrderAPI:
    """Order system interface encapsulation

    Simulate the takeaway order system interface, including creation, query, order reminder, modification, cancellation and other functions.
    All data are analog data for development and testing.
    """

    # Class-level order storage ensures that all instances share the same mock data
    _orders: Dict[str, Dict[str, Any]] = {}
    _order_counter = 1000
    _initialized = False

    def __init__(self):
        """Initialize the order interface"""
        # Preset some test orders (only when instantiating for the first time)
        if not OrderAPI._initialized:
            self._init_mock_orders()
            OrderAPI._initialized = True

    def _init_mock_orders(self):
        """Initialize simulated order data"""
        # Orders to be paid
        OrderAPI._orders["FD_PENDING_001"] = {
            "order_id": "FD_PENDING_001",
            "user_id": "test_user_001",
            "merchant": "Test restaurantC",
            "items": [{"name": "Package to be paid", "quantity": 1, "price": 50.0}],
            "total": 50.0,
            "address": "Test address of Dongcheng District, Beijing",
            "status": OrderStatus.PENDING,
            "created_at": "2026-09-04 09:00:00",
            "remark": None
        }
        # Orders in delivery
        OrderAPI._orders["FD_DELIVERING_001"] = {
            "order_id": "FD_DELIVERING_001",
            "user_id": "test_user_001",
            "merchant": "Test restaurantA",
            "items": [{"name": "Test package", "quantity": 1, "price": 50.0}],
            "total": 50.0,
            "address": "Test address of Chaoyang District, Beijing",
            "status": OrderStatus.DELIVERING,
            "created_at": "2026-09-04 10:00:00",
            "remark": None
        }
        # Completed orders
        OrderAPI._orders["FD_COMPLETED_001"] = {
            "order_id": "FD_COMPLETED_001",
            "user_id": "test_user_001",
            "merchant": "Test restaurantB",
            "items": [{"name": "Completed the package", "quantity": 1, "price": 60.0}],
            "total": 60.0,
            "address": "Test address in Haidian District, Beijing",
            "status": OrderStatus.COMPLETED,
            "created_at": "2026-09-04 08:00:00",
            "remark": None
        }
        # Refunded orders
        OrderAPI._orders["FD_REFUNDED_001"] = {
            "order_id": "FD_REFUNDED_001",
            "user_id": "test_user_001",
            "merchant": "Test restaurantD",
            "items": [{"name": "Refunded package", "quantity": 1, "price": 50.0}],
            "total": 50.0,
            "address": "Test address in Fengtai District, Beijing",
            "status": OrderStatus.REFUNDED,
            "created_at": "2026-09-04 07:00:00",
            "remark": None
        }

    def _generate_order_id(self) -> str:
        """Generate the order number"""
        OrderAPI._order_counter += 1
        return f"FD{datetime.now().strftime('%Y%m%d')}{OrderAPI._order_counter:04d}"

    def _success_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build a successful response"""
        return {
            "status": "success",
            "data": data,
            "error": "",
            "error_code": ""
        }

    def _error_response(self, error: str, code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
        """Build an error response"""
        return {
            "status": "error",
            "data": {},
            "error": error,
            "error_code": code
        }

    def create_order(
        self,
        user_id: str,
        items: List[Dict[str, Any]],
        address: str,
        remark: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an order

        Args:
            user_id: ConsumerID
            items: List of goods, each item contains name, quantity, price
            address: Delivery address
            remark: Remarks (optional)

        Returns:
            Create results
        """
        # Parameter verification
        if not items:
            return self._error_response("The product list cannot be empty.", "EMPTY_ITEMS")

        if not address:
            return self._error_response("The delivery address cannot be empty.", "EMPTY_ADDRESS")

        # Calculate the total price
        total = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)

        # Generate orders
        order_id = self._generate_order_id()
        order = {
            "order_id": order_id,
            "user_id": user_id,
            "merchant": "Simulated restaurant",
            "items": items,
            "total": total,
            "address": address,
            "status": OrderStatus.PENDING,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "remark": remark
        }

        # Store orders
        OrderAPI._orders[order_id] = order

        return self._success_response(order)

    def get_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Check the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            Order details
        """
        if order_id not in OrderAPI._orders:
            return self._error_response(f"The order {order_id} does not exist", "ORDER_NOT_FOUND")

        order = OrderAPI._orders[order_id]

        # Permission check
        if order["user_id"] != user_id:
            return self._error_response("No right to view this order", "PERMISSION_DENIED")

        return self._success_response(order)

    def remind_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Follow up on the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            The result of the order reminder
        """
        if order_id not in OrderAPI._orders:
            return self._error_response(f"The order {order_id} does not exist", "ORDER_NOT_FOUND")

        order = OrderAPI._orders[order_id]

        if order["user_id"] != user_id:
            return self._error_response("I don't have the right to operate this order", "PERMISSION_DENIED")

        # Simulated reminder
        return self._success_response({
            "order_id": order_id,
            "reminded": True,
            "message": "The merchant has been notified to deal with it as soon as possible."
        })

    def modify_order(
        self,
        user_id: str,
        order_id: str,
        address: Optional[str] = None,
        remark: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Modify the order

        Args:
            user_id: ConsumerID
            order_id: Order number
            address: New address (optional)
            remark: New remarks (optional)
            items: List of new products (optional)

        Returns:
            Modified results
        """
        if order_id not in OrderAPI._orders:
            return self._error_response(f"The order {order_id} does not exist", "ORDER_NOT_FOUND")

        order = OrderAPI._orders[order_id]

        if order["user_id"] != user_id:
            return self._error_response("I don't have the right to operate this order", "PERMISSION_DENIED")

        # Check the order status
        if order["status"] in {OrderStatus.DELIVERING, OrderStatus.COMPLETED, OrderStatus.CANCELLED, OrderStatus.REFUNDED}:
            return self._error_response(f"The order has been {order['status']} and cannot be modified.", "ORDER_STATUS_ERROR")

        # Update the field
        if address:
            order["address"] = address
        if remark is not None:
            order["remark"] = remark
        if items:
            order["items"] = items
            order["total"] = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)

        OrderAPI._orders[order_id] = order

        return self._success_response(order)

    def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Cancel the order

        Args:
            user_id: ConsumerID
            order_id: Order number

        Returns:
            Cancel the result
        """
        if order_id not in OrderAPI._orders:
            return self._error_response(f"The order {order_id} does not exist", "ORDER_NOT_FOUND")

        order = OrderAPI._orders[order_id]

        if order["user_id"] != user_id:
            return self._error_response("I don't have the right to operate this order", "PERMISSION_DENIED")

        # Check the order status
        if order["status"] == OrderStatus.DELIVERING:
            return self._error_response("Delivered orders cannot be canceled. Please contact the merchant or request after-sales service.", "ORDER_DELIVERING")

        if order["status"] == OrderStatus.COMPLETED:
            return self._error_response("The order has been completed and cannot be canceled. Please apply for after-sales service.", "ORDER_COMPLETED")

        if order["status"] in {OrderStatus.CANCELLED, OrderStatus.REFUNDED}:
            return self._error_response(f"The order has been {order['status']}, no need to repeat the operation", "ORDER_ALREADY_DONE")

        # Update the status
        order["status"] = OrderStatus.CANCELLED
        OrderAPI._orders[order_id] = order

        return self._success_response({
            "order_id": order_id,
            "status": OrderStatus.CANCELLED,
            "message": "The order has been cancelled."
        })


if __name__ == "__main__":
    # Local test
    api = OrderAPI()
    print("Test to create an order:")
    result = api.create_order(
        user_id="test_user",
        items=[{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
        address="Xxx Street, Chaoyang District, Beijing"
    )
    print(result)
