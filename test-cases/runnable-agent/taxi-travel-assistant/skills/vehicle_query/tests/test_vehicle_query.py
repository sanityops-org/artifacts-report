#!/usr/bin/env python3
"""Vehicle query skill test"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


class TestQueryVehicleTool(unittest.TestCase):
    """Test vehicle query tool"""

    def setUp(self):
        from skills.vehicle_query.tools.query_vehicle import QueryVehicleTool
        self.tool = QueryVehicleTool()

    def test_query_vehicle_available(self):
        """Test to find available vehicles"""
        result = asyncio.run(self.tool.execute(location="L-001"))

        self.assertTrue(result.success)
        self.assertIn("vehicles", result.metadata)
        self.assertGreater(len(result.metadata["vehicles"]), 0)

    def test_query_vehicle_by_category(self):
        """Test and screen by car model"""
        result = asyncio.run(self.tool.execute(location="L-001", category="comfort"))

        self.assertTrue(result.success)
        self.assertGreater(len(result.metadata["vehicles"]), 0)
        for vehicle in result.metadata["vehicles"]:
            self.assertEqual(vehicle["category"], "comfort")

    def test_query_vehicle_no_results(self):
        """There are no available vehicles for testing"""
        result = asyncio.run(self.tool.execute(location="L-001", category="premium", radius_km=0.1))

        # premium If the vehicle is not near L-001, it should return to an empty list.
        self.assertTrue(result.success)
        self.assertEqual(len(result.metadata["vehicles"]), 0)

    def test_query_vehicle_unknown_location(self):
        """The test location does not exist."""
        result = asyncio.run(self.tool.execute(location="L-999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def test_handler_success(self):
        """The test processor is working normally."""
        from skills.vehicle_query.handler import run

        result = run({"location": "L-001"})

        self.assertEqual(result["status"], "success")
        self.assertIn("vehicles", result["data"])

    def test_handler_missing_location(self):
        """The test is missing a position."""
        from skills.vehicle_query.handler import run

        result = run({})

        self.assertEqual(result["status"], "error")
        self.assertIn("location", result["message"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
