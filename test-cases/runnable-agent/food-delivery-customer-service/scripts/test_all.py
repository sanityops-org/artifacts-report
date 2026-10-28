#!/usr/bin/env python3
"""Integrated test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.order_management.handler import main as order_main
from skills.after_sale.handler import main as after_sale_main


def test_all_skills():
    """Test all skills"""

    user_id = "test_user_001"

    # Test order management skills
    print("Test order management skills...")

    # Create an order
    create_result = order_main({
        "action": "create_order",
        "params": {
            "user_id": user_id,
            "items": [{"name": "Kung Pao Chicken", "quantity": 1, "price": 38.0}],
            "address": "Xxx Street, Chaoyang District, Beijing"
        }
    })
    assert create_result["status"] == "success", f"Failed to create an order: {create_result}"
    order_id = create_result["data"]["order_id"]
    print(f"✓ Successfully created the order: {order_id}")

    # Check the order
    query_result = order_main({
        "action": "query_order",
        "params": {"user_id": user_id, "order_id": order_id}
    })
    assert query_result["status"] == "success", f"Failed to query the order: {query_result}"
    print(f"✓ Check the order successfully")

    # Follow up on the order
    remind_result = order_main({
        "action": "remind_order",
        "params": {"user_id": user_id, "order_id": order_id}
    })
    assert remind_result["status"] == "success", f"Failed to urge the order: {remind_result}"
    print(f"✓ Successful order reminder")

    # Modify the order
    modify_result = order_main({
        "action": "modify_order",
        "params": {"user_id": user_id, "order_id": order_id, "remark": "Less spicy"}
    })
    assert modify_result["status"] == "success", f"Failed to modify the order: {modify_result}"
    print(f"✓ Successfully modified the order")

    # Cancel the order
    cancel_result = order_main({
        "action": "cancel_order",
        "params": {"user_id": user_id, "order_id": order_id}
    })
    assert cancel_result["status"] == "success", f"Failed to cancel the order: {cancel_result}"
    print(f"✓ Cancel the order successfully")

    # Test after-sales service skills
    print("\nTest after-sales service skills...")

    # Apply for automatic refund
    refund_result = after_sale_main({
        "action": "apply_refund",
        "params": {
            "user_id": user_id,
            "order_id": "FD_PENDING_001",
            "amount": 50.0,
            "reason": "I don't want it anymore"
        }
    })
    assert refund_result["status"] == "success", f"Failed to apply for refund: {refund_result}"
    print(f"✓ Successfully applied for refund (automatic refund)")

    # Apply for a manual refund
    manual_result = after_sale_main({
        "action": "apply_refund",
        "params": {
            "user_id": user_id,
            "order_id": "FD_DELIVERING_001",
            "amount": 50.0,
            "reason": "Commodity quality problems"
        }
    })
    assert manual_result["status"] == "success", f"Failed to transfer manually: {manual_result}"
    assert manual_result["data"]["decision"] == "manual"
    print(f"✓ Successfully applied for a refund (transferred to manual)")

    # Create a work order
    ticket_result = after_sale_main({
        "action": "create_ticket",
        "params": {
            "user_id": user_id,
            "order_id": "FD001",
            "reason": "Abnormal distribution",
            "detail": "The rider was not delivered to the designated location."
        }
    })
    assert ticket_result["status"] == "success", f"Failed to create a work order: {ticket_result}"
    print(f"✓ Successfully created the work order")

    print("\nAll skill tests have passed. ✓")


if __name__ == "__main__":
    test_all_skills()
