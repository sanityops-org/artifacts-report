#!/usr/bin/env python3
"""
Route planning skill test
"""

import sys
from pathlib import Path

# Calculate the root directory of the agent project
agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


class TestPlanRouteTool(unittest.TestCase):
    """Test route planning tools"""

    def setUp(self):
        from skills.route_planning.tools.plan_route import PlanRouteTool
        self.tool = PlanRouteTool()

    def test_plan_route_success(self):
        """Test normal route inquiry"""
        result = asyncio.run(self.tool.execute(origin="L-001", destination="L-002"))

        self.assertTrue(result.success)
        self.assertIn("distance_km", result.metadata)
        self.assertIn("duration_min", result.metadata)
        self.assertGreater(result.metadata["distance_km"], 0)

    def test_plan_route_unknown_origin(self):
        """The test starting point does not exist."""
        result = asyncio.run(self.tool.execute(origin="L-999", destination="L-002"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_plan_route_unknown_destination(self):
        """The test endpoint does not exist."""
        result = asyncio.run(self.tool.execute(origin="L-001", destination="L-999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_plan_route_same_location(self):
        """The test starts and ends at the same."""
        result = asyncio.run(self.tool.execute(origin="L-001", destination="L-001"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["distance_km"], 0)


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def test_handler_success(self):
        """The test processor is working normally."""
        from skills.route_planning.handler import run

        result = run({"origin": "L-001", "destination": "L-002"})

        self.assertEqual(result["status"], "success")
        self.assertIn("route", result["data"])

    def test_handler_missing_origin(self):
        """The test lacks a starting point."""
        from skills.route_planning.handler import run

        result = run({"destination": "L-002"})

        self.assertEqual(result["status"], "error")
        self.assertIn("starting point", result["message"])

    def test_handler_missing_destination(self):
        """The test is missing the end point."""
        from skills.route_planning.handler import run

        result = run({"origin": "L-001"})

        self.assertEqual(result["status"], "error")
        self.assertIn("destination", result["message"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
