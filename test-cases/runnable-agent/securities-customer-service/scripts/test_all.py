#!/usr/bin/env python3
"""Integrated test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.fund_operation.handler import main as fund_main
from skills.stock_trading.handler import main as stock_main
from skills.product_purchase.handler import main as purchase_main
from skills.inquiry.handler import main as inquiry_main


def test_all_skills():
    """Test all skills"""

    user_id = "test_user"

    # Test capital skills
    assert fund_main({
        "action": "query_balance",
        "params": {"user_id": user_id}
    })["status"] == "success"

    assert fund_main({
        "action": "bank_transfer",
        "params": {"user_id": user_id, "amount": 10000, "direction": "in"}
    })["status"] == "success"
    print("✓ Passed the capital skills test")

    # Test trading skills
    assert stock_main({
        "action": "query_position",
        "params": {"user_id": user_id}
    })["status"] == "success"

    assert stock_main({
        "action": "buy_stock",
        "params": {"user_id": user_id, "stock_code": "600036", "quantity": 100}
    })["status"] == "success"
    print("✓ Passed the trading skills test")

    # Test the application skills
    assert purchase_main({
        "action": "query_products",
        "params": {"user_id": user_id}
    })["status"] == "success"

    assert purchase_main({
        "action": "purchase",
        "params": {"user_id": user_id, "product_code": "FUND001", "amount": 10000}
    })["status"] == "success"
    print("✓ Passed the application skills test")

    # Test consulting skills
    assert inquiry_main({
        "action": "query_quote",
        "params": {"stock_code": "600036"}
    })["status"] == "success"

    assert inquiry_main({
        "action": "business_guide",
        "params": {"topic": "How to transfer money"}
    })["status"] == "success"
    print("✓ Passed the consulting skills test")

    print("\nAll skill tests have passed. ✓")


if __name__ == "__main__":
    test_all_skills()
