#!/usr/bin/env python3
"""Test the intelligent dispatch engine"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


class TestDispatchEngineTool(unittest.TestCase):
    """Test the dispatch engine tool"""

    def test_dispatch_noise_complaint(self):
        """Test noise complaint distribution"""
        from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool

        tool = DispatchEngineTool()
        result = asyncio.run(tool.execute(
            content="Construction noise at night disturbs people",
            ticket_type="complaint"
        ))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["dept_id"], "eco_env")
        self.assertEqual(result.metadata["dept_name"], "Ecology and Environment Bureau")
        self.assertIn(result.metadata["urgency_level"], ["urgent", "normal"])

    def test_dispatch_fire_critical(self):
        """Test fire emergency dispatch"""
        from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool

        tool = DispatchEngineTool()
        result = asyncio.run(tool.execute(
            content="There was a fire in the community.",
            ticket_type="complaint"
        ))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["dept_id"], "emergency")
        self.assertEqual(result.metadata["urgency_level"], "critical")
        self.assertEqual(result.metadata["deadline_hours"], 2)

    def test_dispatch_consultation_normal(self):
        """Test consultation work order ordinary level"""
        from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool

        tool = DispatchEngineTool()
        result = asyncio.run(tool.execute(
            content="I want to inquire about the medical insurance reimbursement policy.",
            ticket_type="consultation"
        ))

        self.assertTrue(result.success)
        # The default ordinary level of the consulting class
        self.assertEqual(result.metadata["urgency_level"], "normal")

    def test_dispatch_consultation_with_urgency_keyword(self):
        """When the content of the test consultation work order contains urgent keywords, it is still at the ordinary level and the deadline is correct."""
        from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool

        tool = DispatchEngineTool()
        result = asyncio.run(tool.execute(
            content="Consult the investigation of fire safety hazards",
            ticket_type="consultation"
        ))

        self.assertTrue(result.success)
        # The consultation coverage emergency level is normal, and the deadline is reset to 72 hours.
        self.assertEqual(result.metadata["urgency_level"], "normal")
        self.assertEqual(result.metadata["deadline_hours"], 72)

    def test_dispatch_fallback_department(self):
        """When testing non-matched keywords, the bottom department"""
        from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool

        tool = DispatchEngineTool()
        result = asyncio.run(tool.execute(
            content="There is a question I want to reflect.",
            ticket_type="complaint"
        ))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["dept_id"], "default")
        self.assertFalse(result.metadata["is_auto"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
