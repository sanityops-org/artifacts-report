#!/usr/bin/env python3
"""Cost estimation skill test"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


class TestEstimateFareTool(unittest.TestCase):
    """Test cost estimation tool"""

    def setUp(self):
        from skills.fare_estimation.tools.estimate_fare import EstimateFareTool
        self.tool = EstimateFareTool()

    def test_estimate_fare_success(self):
        """Estimated normal cost of testing"""
        result = asyncio.run(self.tool.execute(origin="L-001", destination="L-002"))

        self.assertTrue(result.success)
        self.assertIn("fares", result.metadata)
        self.assertIn("economic", result.metadata["fares"])

    def test_estimate_fare_specific_category(self):
        """Test the estimated cost of the designated model"""
        result = asyncio.run(self.tool.execute(origin="L-001", destination="L-002", category="comfort"))

        self.assertTrue(result.success)
        self.assertIn("fare", result.metadata)
        self.assertEqual(result.metadata["category"], "comfort")

    def test_estimate_fare_night(self):
        """Test the night cost estimate (short route < 15km, only trigger the night price increase)"""
        # Use the short route L-004 -> L-005 (5.0 km) to avoid triggering long-distance price increase interference.
        result = asyncio.run(self.tool.execute(origin="L-004", destination="L-005", time_of_day="night"))

        self.assertTrue(result.success)
        # The cost at night should be higher than that during the day: there should be a price increase at night.
        night_total = result.metadata["fares"]["economic"]["total"]
        day_result = asyncio.run(self.tool.execute(origin="L-004", destination="L-005", time_of_day="day"))
        day_total = day_result.metadata["fares"]["economic"]["total"]
        self.assertGreater(night_total, day_total)
        # The price increase at night will be increased according to the multiplier (economical night multiplier 1.2，36.6 > 30.5）
        self.assertGreater(result.metadata["fares"]["economic"]["night_surcharge"], 0)

    def test_estimate_fare_unknown_location(self):
        """The test location does not exist."""
        result = asyncio.run(self.tool.execute(origin="L-999", destination="L-002"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def test_handler_success(self):
        """The test processor is working normally."""
        from skills.fare_estimation.handler import run

        result = run({"origin": "L-001", "destination": "L-002"})

        self.assertEqual(result["status"], "success")
        self.assertIn("fares", result["data"])

    def test_handler_with_category(self):
        """Test the designated model"""
        from skills.fare_estimation.handler import run

        result = run({"origin": "L-001", "destination": "L-002", "category": "premium"})

        self.assertEqual(result["status"], "success")
        self.assertIn("fare", result["data"])
        self.assertEqual(result["data"]["category"], "premium")


if __name__ == "__main__":
    unittest.main(verbosity=2)
