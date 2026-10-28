#!/usr/bin/env python3
"""Test work order storage tool"""

import sys
from pathlib import Path

agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio


class TestTicketStoreTool(unittest.TestCase):
    """Test work order storage tool"""

    def setUp(self):
        """Empty the work order library before each test"""
        from data.sim_db import TICKETS
        TICKETS.clear()

    def test_create_ticket_success(self):
        """Test the creation of the work order successfully"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(
            action="create",
            ticket_type="complaint",
            content="The noise in the community disturbs people.",
            dept_id="eco_env",
            urgency_level="urgent",
            reporter_name="Mr. Zhang",
            reporter_phone="13800138000"
        ))

        self.assertTrue(result.success)
        self.assertIn("ticket_id", result.metadata)
        self.assertEqual(result.metadata["ticket_type"], "complaint")
        self.assertEqual(result.metadata["status"], "pending")

    def test_create_ticket_anonymous(self):
        """Test to create a work order anonymously"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(
            action="create",
            ticket_type="complaint",
            content="Garbage piled up on the roadside",
            dept_id="urban_mgmt",
            urgency_level="normal",
            reporter_name=None,
            reporter_phone=None
        ))

        self.assertTrue(result.success)
        self.assertIsNone(result.metadata["reporter_phone"])

    def test_get_ticket_by_id(self):
        """Test query the work order by ID"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool
        from data.sim_db import TICKETS

        # Create a work order first.
        TICKETS["GH-20260904-0001"] = {
            "ticket_id": "GH-20260904-0001",
            "ticket_type": "complaint",
            "content": "Test work order",
            "status": "pending"
        }

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(action="get_by_id", ticket_id="GH-20260904-0001"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["content"], "Test work order")

    def test_get_ticket_by_id_not_found(self):
        """Test query non-existent work orders"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(action="get_by_id", ticket_id="GH-99999999-9999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_get_tickets_by_phone(self):
        """Test the list of work orders by mobile phone number"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool
        from data.sim_db import TICKETS

        # Create two work orders
        TICKETS["GH-20260904-0001"] = {
            "ticket_id": "GH-20260904-0001",
            "reporter_phone": "13800138000",
            "content": "Work order1",
            "status": "pending"
        }
        TICKETS["GH-20260904-0002"] = {
            "ticket_id": "GH-20260904-0002",
            "reporter_phone": "13800138000",
            "content": "Work order2",
            "status": "resolved"
        }
        TICKETS["GH-20260904-0003"] = {
            "ticket_id": "GH-20260904-0003",
            "reporter_phone": "13900139000",
            "content": "Work order3",
            "status": "pending"
        }

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(action="get_by_phone", phone="13800138000"))

        self.assertTrue(result.success)
        self.assertEqual(len(result.metadata["tickets"]), 2)

    def test_update_ticket_status(self):
        """Test and update the work order status"""
        from skills.government_ticket.tools.ticket_store import TicketStoreTool
        from data.sim_db import TICKETS

        TICKETS["GH-20260904-0001"] = {
            "ticket_id": "GH-20260904-0001",
            "status": "pending"
        }

        tool = TicketStoreTool()
        result = asyncio.run(tool.execute(
            action="update_status",
            ticket_id="GH-20260904-0001",
            new_status="processing"
        ))

        self.assertTrue(result.success)
        self.assertEqual(TICKETS["GH-20260904-0001"]["status"], "processing")


if __name__ == "__main__":
    unittest.main(verbosity=2)
