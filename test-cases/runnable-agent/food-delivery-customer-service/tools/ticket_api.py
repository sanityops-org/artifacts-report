#!/usr/bin/env python3
"""Work order system interface packaging (analog data, transfer to manual)"""

from typing import Dict, Any
from datetime import datetime


class TicketAPI:
    """Work order system interface packaging

    Simulate the interface of manual customer service work order system, which is used to deal with after-sales problems that require manual intervention.
    All data are analog data for development and testing.
    """

    def __init__(self):
        """Initialize the work order interface"""
        self._ticket_counter = 1000
        # Simulate work order storage
        self._tickets: Dict[str, Dict[str, Any]] = {}

    def _generate_ticket_id(self) -> str:
        """Generate the work order number"""
        self._ticket_counter += 1
        return f"T{datetime.now().strftime('%Y%m%d')}{self._ticket_counter:04d}"

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

    def create_ticket(
        self,
        user_id: str,
        order_id: str,
        reason: str,
        detail: str
    ) -> Dict[str, Any]:
        """Create a manual work order

        Args:
            user_id: ConsumerID
            order_id: Order number
            reason: The reason for the work order (e.g. refund dispute, distribution abnormality, etc.)
            detail: Detailed description

        Returns:
            The result of work order creation
        """
        # Parameter verification
        if not reason or not reason.strip():
            return self._error_response("The reason for the work order cannot be empty.", "EMPTY_REASON")

        if not detail or not detail.strip():
            return self._error_response("The details of the problem cannot be empty.", "EMPTY_DETAIL")

        # Generate a work order
        ticket_id = self._generate_ticket_id()
        ticket = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "order_id": order_id,
            "reason": reason,
            "detail": detail,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_response": "30Within minutes"
        }

        # Storage work order
        self._tickets[ticket_id] = ticket

        return self._success_response(ticket)

    def get_ticket(self, user_id: str, ticket_id: str) -> Dict[str, Any]:
        """Check the status of the work order

        Args:
            user_id: ConsumerID
            ticket_id: Work order number

        Returns:
            Details of the work order
        """
        if ticket_id not in self._tickets:
            return self._error_response(f"The ticket {ticket_id} does not exist", "TICKET_NOT_FOUND")

        ticket = self._tickets[ticket_id]

        # Permission check
        if ticket["user_id"] != user_id:
            return self._error_response("No right to view the work order", "PERMISSION_DENIED")

        return self._success_response(ticket)


if __name__ == "__main__":
    # Local test
    api = TicketAPI()
    print("Test to create a work order:")
    result = api.create_ticket(
        user_id="test_user",
        order_id="FD001",
        reason="Refund disputes",
        detail="The order has been delivered, but there is a quality problem with the goods."
    )
    print(result)
