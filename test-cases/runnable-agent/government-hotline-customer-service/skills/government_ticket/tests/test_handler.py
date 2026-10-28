#!/usr/bin/env python3
"""Test skill processor"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
from data.sim_db import TICKETS


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def setUp(self):
        """Empty the work order library"""
        TICKETS.clear()

    def test_create_complaint_ticket(self):
        """Test to create a complaint work order"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "Construction noise at night disturbs people",
            "reporter_name": "Mr. Zhang",
            "reporter_phone": "13800138000"
        })

        self.assertEqual(result["status"], "success")
        self.assertIn("ticket_id", result["data"])
        self.assertEqual(result["data"]["ticket_type"], "complaint")
        self.assertEqual(result["data"]["dept_id"], "eco_env")

    def test_create_suggestion_ticket(self):
        """Test to create a suggested work order"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "suggestion",
            "content": "It is suggested to increase bus services.",
            "reporter_phone": "13800138000"
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["ticket_type"], "suggestion")

    def test_create_consultation_ticket(self):
        """Test and create a consultation work order"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "consultation",
            "content": "Consult the medical insurance reimbursement policy"
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["ticket_type"], "consultation")

    def test_create_anonymous_ticket(self):
        """Test to create a work order anonymously"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "Garbage piled up on the roadside"
        })

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["data"]["is_anonymous"])

    def test_create_critical_ticket(self):
        """Test the creation of urgent work orders"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "There was a fire in the community."
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["urgency_level"], "critical")

    def test_query_ticket_by_id(self):
        """Test query by work order number"""
        from skills.government_ticket.handler import run

        # Create first
        create_result = run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "Test work order",
            "reporter_phone": "13800138000"
        })
        ticket_id = create_result["data"]["ticket_id"]

        # Inquire again
        result = run({
            "action": "query_ticket",
            "ticket_id": ticket_id
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["ticket_id"], ticket_id)

    def test_query_tickets_by_phone(self):
        """Test and query by mobile phone number"""
        from skills.government_ticket.handler import run

        # Create two work orders
        run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "Work order1",
            "reporter_phone": "13800138000"
        })
        run({
            "action": "create_ticket",
            "ticket_type": "suggestion",
            "content": "Work order2",
            "reporter_phone": "13800138000"
        })

        result = run({
            "action": "query_ticket_list",
            "phone": "13800138000"
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["total"], 2)

    def test_invalid_phone_format(self):
        """Test invalid mobile phone number"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "complaint",
            "content": "Test",
            "reporter_phone": "12345"
        })

        self.assertEqual(result["status"], "error")

    def test_missing_content(self):
        """The test is missing content."""
        from skills.government_ticket.handler import run

        result = run({
            "action": "create_ticket",
            "ticket_type": "complaint"
        })

        self.assertEqual(result["status"], "error")

    def test_unknown_action(self):
        """Test unknown operations"""
        from skills.government_ticket.handler import run

        result = run({
            "action": "unknown_action"
        })

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main(verbosity=2)
