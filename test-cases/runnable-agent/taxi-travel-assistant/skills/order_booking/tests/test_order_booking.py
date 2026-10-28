#!/usr/bin/env python3
"""Taxi ordering skill test"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


def tearDownModule():
    """Reset the simulation data after the order test to avoid contaminating other test modules."""
    from data import sim_db

    for vid, v in sim_db.VEHICLES.items():
        v["status"] = "idle"
    sim_db.ORDERS.clear()


class TestPlaceOrderTool(unittest.TestCase):
    """Test the order tool"""

    def setUp(self):
        from skills.order_booking.tools.place_order import PlaceOrderTool
        self.tool = PlaceOrderTool()

    def test_place_order_success(self):
        """Test and place an order normally"""
        result = asyncio.run(self.tool.execute(
            user_id="U-123",
            origin="L-001",
            destination="L-002",
            phone="138****1234"
        ))

        self.assertTrue(result.success)
        self.assertIn("order_id", result.metadata)
        self.assertIn("vehicle_id", result.metadata)

    def test_place_order_with_category(self):
        """Test the designated model and place an order"""
        result = asyncio.run(self.tool.execute(
            user_id="U-123",
            origin="L-001",
            destination="L-002",
            phone="138****1234",
            category="comfort"
        ))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["vehicle"]["category"], "comfort")

    def test_place_order_no_vehicles(self):
        """There are no available vehicles for testing"""
        # Use a location that does not exist
        result = asyncio.run(self.tool.execute(
            user_id="U-123",
            origin="L-999",
            destination="L-002",
            phone="138****1234"
        ))

        self.assertFalse(result.success)


class TestCancelOrderTool(unittest.TestCase):
    """Test the order cancellation tool"""

    def setUp(self):
        from skills.order_booking.tools.cancel_order import CancelOrderTool
        self.tool = CancelOrderTool()

    def test_cancel_order_success(self):
        """The test is canceled normally."""
        # Place an order first
        from skills.order_booking.tools.place_order import PlaceOrderTool
        place_tool = PlaceOrderTool()
        order_result = asyncio.run(place_tool.execute(
            user_id="U-123",
            origin="L-001",
            destination="L-002",
            phone="138****1234"
        ))
        order_id = order_result.metadata["order_id"]

        # Cancel again
        result = asyncio.run(self.tool.execute(order_id=order_id))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["status"], "cancelled")

    def test_cancel_order_not_found(self):
        """The test order does not exist."""
        result = asyncio.run(self.tool.execute(order_id="O-999999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def test_handler_place_order(self):
        """Test the order processor"""
        from skills.order_booking.handler import run

        result = run({
            "action": "place_order",
            "params": {
                "user_id": "U-123",
                "origin": "L-001",
                "destination": "L-002",
                "phone": "138****1234"
            }
        })

        self.assertEqual(result["status"], "success")
        self.assertIn("order_id", result["data"])

    def test_handler_cancel_order(self):
        """Test the order cancellation processor"""
        from skills.order_booking.handler import run

        # Place an order first
        place_result = run({
            "action": "place_order",
            "params": {
                "user_id": "U-123",
                "origin": "L-001",
                "destination": "L-002",
                "phone": "138****1234"
            }
        })
        order_id = place_result["data"]["order_id"]

        # Cancel again
        result = run({
            "action": "cancel_order",
            "params": {"order_id": order_id}
        })

        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main(verbosity=2)
