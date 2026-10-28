#!/usr/bin/env python3
"""Work order API test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.ticket_api import TicketAPI


class TestTicketAPI:
    """Work order API test class"""

    def setup_method(self):
        self.api = TicketAPI()
        self.user_id = "test_user_001"

    def test_create_ticket_success(self):
        """Test the creation of the work order successfully"""
        result = self.api.create_ticket(
            user_id=self.user_id,
            order_id="FD001",
            reason="Refund disputes",
            detail="The order has been delivered, but there is a quality problem with the goods."
        )
        assert result["status"] == "success"
        assert "ticket_id" in result["data"]
        assert result["data"]["status"] == "pending"

    def test_create_ticket_empty_reason(self):
        """The reason for testing and creating a work order is empty."""
        result = self.api.create_ticket(
            user_id=self.user_id,
            order_id="FD001",
            reason="",
            detail="Test"
        )
        assert result["status"] == "error"
        assert "reason" in result["error"].lower()

    def test_create_ticket_empty_detail(self):
        """The details of the test creation work order are empty."""
        result = self.api.create_ticket(
            user_id=self.user_id,
            order_id="FD001",
            reason="Refund issues",
            detail=""
        )
        assert result["status"] == "error"
        assert "details" in result["error"].lower()

    def test_get_ticket_success(self):
        """The test query work order is successful"""
        # Create a work order first
        create_result = self.api.create_ticket(
            user_id=self.user_id,
            order_id="FD001",
            reason="After-sales problems",
            detail="The product does not match the description."
        )
        ticket_id = create_result["data"]["ticket_id"]

        # Query the work order
        result = self.api.get_ticket(self.user_id, ticket_id)
        assert result["status"] == "success"
        assert result["data"]["ticket_id"] == ticket_id

    def test_get_ticket_not_found(self):
        """Test query non-existent work orders"""
        result = self.api.get_ticket(self.user_id, "NON_EXISTENT_TICKET")
        assert result["status"] == "error"
        assert "does not exist" in result["error"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
