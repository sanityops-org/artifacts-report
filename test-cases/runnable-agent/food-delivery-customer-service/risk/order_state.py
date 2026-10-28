#!/usr/bin/env python3
"""Definition of order status"""

from typing import Set


class OrderStatus:
    """Order status constant and judgment method"""

    # Order status constant
    PENDING = "pending"        # To be paid
    PAID = "paid"              # Paid
    PREPARING = "preparing"    # The merchant is preparing meals (not served)
    DELIVERING = "delivering"  # In the middle of delivery (the meal has been served)
    COMPLETED = "completed"    # Delivered/Completed
    CANCELLED = "cancelled"    # Canceled
    REFUNDED = "refunded"      # Refunded

    # Status collection that can be automatically refunded (not served)
    REFUNDABLE_STATES: Set[str] = {
        PENDING,
        PAID,
        PREPARING
    }

    # Collection of states that need to be processed manually (meals have been served)
    MANUAL_STATES: Set[str] = {
        DELIVERING,
        COMPLETED
    }

    @classmethod
    def is_refundable(cls, status: str) -> bool:
        """Determine whether the order status can be automatically refunded

        Args:
            status: Order status

        Returns:
            True It means that it can be automatically refunded (not served), False means no
        """
        return status in cls.REFUNDABLE_STATES

    @classmethod
    def is_manual(cls, status: str) -> bool:
        """Judge whether the order status needs to be processed manually

        Args:
            status: Order status

        Returns:
            True It means that it needs to be processed manually (the meal has been served), False means that it is not needed.
        """
        return status in cls.MANUAL_STATES

    @classmethod
    def all_statuses(cls) -> Set[str]:
        """Return all valid state collections"""
        return {
            cls.PENDING,
            cls.PAID,
            cls.PREPARING,
            cls.DELIVERING,
            cls.COMPLETED,
            cls.CANCELLED,
            cls.REFUNDED
        }


if __name__ == "__main__":
    # Local test
    print("Automatic refund status:", OrderStatus.REFUNDABLE_STATES)
    print("The status needs to be processed manually.:", OrderStatus.MANUAL_STATES)
    print("pending Refundable?", OrderStatus.is_refundable("pending"))
    print("delivering Refundable?", OrderStatus.is_refundable("delivering"))
