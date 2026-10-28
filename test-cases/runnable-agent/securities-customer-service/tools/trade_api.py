#!/usr/bin/env python3
"""Transaction system interface encapsulation (analog data)"""

from typing import Dict, Any, Optional
from datetime import datetime
import random


class TradeAPI:
    """Transaction system interface encapsulation

    Simulate various interfaces of the securities trading system, including funds, stock trading, product subscription and other functions.
    All data are analog data for development and testing.
    """

    def __init__(self):
        """Initialize the transaction interface"""
        self._order_counter = 1000

    def _generate_order_id(self) -> str:
        """Generate the commission number"""
        self._order_counter += 1
        return f"20260903{self._order_counter:04d}"

    def _success_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build a successful response"""
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

    def _error_response(self, error: str, code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
        """Build an error response"""
        return {
            "status": "error",
            "error": error,
            "error_code": code,
            "timestamp": datetime.now().isoformat()
        }

    # ==================== Fund-related ====================

    def get_balance(self, user_id: str) -> Dict[str, Any]:
        """Check the balance of funds

        Args:
            user_id: ConsumerID

        Returns:
            Dictionaries containing total assets, available funds and frozen funds
        """
        return self._success_response({
            "user_id": user_id,
            "total_asset": 150000.00,
            "balance": 85000.00,
            "available": 80000.00,
            "frozen": 5000.00,
            "currency": "CNY"
        })

    def bank_transfer(self, user_id: str, amount: float, direction: str) -> Dict[str, Any]:
        """Bank certificate transfer

        Args:
            user_id: ConsumerID
            amount: Transfer amount
            direction: Transfer direction, "in" means deposit (bank → securities), "out" means withdrawal (securities → bank)

        Returns:
            Transfer result
        """
        if amount <= 0:
            return self._error_response("The transfer amount must be greater than0", "INVALID_AMOUNT")

        if direction not in ["in", "out"]:
            return self._error_response("The transfer direction must be 'in' or 'out'", "INVALID_DIRECTION")

        transfer_id = f"TR{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"

        return self._success_response({
            "user_id": user_id,
            "transfer_id": transfer_id,
            "amount": amount,
            "direction": direction,
            "bank_account": "**** **** **** 1234",
            "status": "success",
            "message": "Transfer successful" if direction == "in" else "withdrawal successful"
        })

    def get_transfer_records(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Check the transfer record

        Args:
            user_id: ConsumerID
            limit: Return the number of records

        Returns:
            List of transfer records
        """
        records = [
            {
                "transfer_id": "TR20260903100001",
                "amount": 10000.00,
                "direction": "in",
                "status": "success",
                "created_at": "2026-09-03 10:00:01"
            },
            {
                "transfer_id": "TR20260903110002",
                "amount": 5000.00,
                "direction": "out",
                "status": "success",
                "created_at": "2026-09-03 11:00:02"
            }
        ]

        return self._success_response({
            "user_id": user_id,
            "records": records[:limit],
            "total": len(records)
        })

    # ==================== Related to stock trading ====================

    def get_position(self, user_id: str) -> Dict[str, Any]:
        """Inquire about the position

        Args:
            user_id: ConsumerID

        Returns:
            List of positions
        """
        positions = [
            {
                "stock_code": "600036",
                "stock_name": "China Merchants Bank",
                "quantity": 1000,
                "available": 1000,
                "cost_price": 35.20,
                "current_price": 36.50,
                "profit_loss": 1300.00,
                "profit_loss_pct": 3.69
            },
            {
                "stock_code": "600519",
                "stock_name": "Maotai, Guizhou",
                "quantity": 100,
                "available": 100,
                "cost_price": 1680.00,
                "current_price": 1725.00,
                "profit_loss": 4500.00,
                "profit_loss_pct": 2.68
            }
        ]

        total_value = sum(p["quantity"] * p["current_price"] for p in positions)
        total_profit = sum(p["profit_loss"] for p in positions)

        return self._success_response({
            "user_id": user_id,
            "positions": positions,
            "total_value": total_value,
            "total_profit": total_profit
        })

    def get_orders(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Inquire about the power of attorney

        Args:
            user_id: ConsumerID
            status: Delegate status filtering, optional values:pending, filled, cancelled

        Returns:
            List of orders
        """
        orders = [
            {
                "order_id": "202609030001",
                "stock_code": "600036",
                "stock_name": "China Merchants Bank",
                "direction": "buy",
                "price": 36.50,
                "quantity": 500,
                "filled_quantity": 500,
                "status": "filled",
                "created_at": "2026-09-03 09:30:00"
            },
            {
                "order_id": "202609030002",
                "stock_code": "000001",
                "stock_name": "Ping An Bank",
                "direction": "sell",
                "price": 12.00,
                "quantity": 1000,
                "filled_quantity": 0,
                "status": "pending",
                "created_at": "2026-09-03 10:15:00"
            }
        ]

        if status:
            orders = [o for o in orders if o["status"] == status]

        return self._success_response({
            "user_id": user_id,
            "orders": orders,
            "total": len(orders)
        })

    def get_deals(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Check the transaction record

        Args:
            user_id: ConsumerID
            limit: Return the number of records

        Returns:
            List of transaction records
        """
        deals = [
            {
                "deal_id": "D202609030001",
                "order_id": "202609030001",
                "stock_code": "600036",
                "stock_name": "China Merchants Bank",
                "direction": "buy",
                "price": 36.50,
                "quantity": 500,
                "amount": 18250.00,
                "commission": 5.48,
                "created_at": "2026-09-03 09:30:05"
            }
        ]

        return self._success_response({
            "user_id": user_id,
            "deals": deals[:limit],
            "total": len(deals)
        })

    def place_order(self, user_id: str, stock_code: str, direction: str,
                    price: float, quantity: int) -> Dict[str, Any]:
        """Place an order

        Args:
            user_id: ConsumerID
            stock_code: Stock code
            direction: Buying and selling direction, "buy" or "sell"
            price: Entrusted price
            quantity: Number of commissions

        Returns:
            Entrusted results
        """
        if direction not in ["buy", "sell"]:
            return self._error_response("The direction of buying and selling must be 'buy' or 'sell'", "INVALID_DIRECTION")

        if price <= 0:
            return self._error_response("The entrusted price must be greater than0", "INVALID_PRICE")

        if quantity <= 0 or quantity % 100 != 0:
            return self._error_response("The number of commissions must be an integer multiple of 100.", "INVALID_QUANTITY")

        order_id = self._generate_order_id()
        stock_names = {
            "600036": "China Merchants Bank",
            "600519": "Maotai, Guizhou",
            "000001": "Ping An Bank",
            "000002": "VankeA"
        }

        return self._success_response({
            "order_id": order_id,
            "user_id": user_id,
            "stock_code": stock_code,
            "stock_name": stock_names.get(stock_code, "Unknown stocks"),
            "direction": direction,
            "price": price,
            "quantity": quantity,
            "amount": price * quantity,
            "status": "pending",
            "message": "Successful entrustment"
        })

    def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Withdraw the order

        Args:
            user_id: ConsumerID
            order_id: Entrustment number

        Returns:
            The result of withdrawing the order
        """
        return self._success_response({
            "order_id": order_id,
            "user_id": user_id,
            "status": "cancelled",
            "message": "Successful withdrawal of the order"
        })

    # ==================== Subscription-related ====================

    def get_products(self, user_id: str) -> Dict[str, Any]:
        """Inquire about products that can be subscribed

        Args:
            user_id: ConsumerID

        Returns:
            List of products that can be subscribed
        """
        products = [
            {
                "product_code": "FUND001",
                "product_name": "Steady Growth Fund",
                "product_type": "fund",
                "nav": 1.2500,
                "nav_date": "2026-09-02",
                "min_amount": 1000,
                "risk_level": "Medium and low risk"
            },
            {
                "product_code": "FUND002",
                "product_name": "Science and Technology Growth Fund",
                "product_type": "fund",
                "nav": 2.1800,
                "nav_date": "2026-09-02",
                "min_amount": 1000,
                "risk_level": "Medium and high risk"
            },
            {
                "product_code": "FIN001",
                "product_name": "Quarterly financial management for 360 days",
                "product_type": "wealth",
                "expected_return": 3.5,
                "min_amount": 50000,
                "risk_level": "Low risk"
            }
        ]

        return self._success_response({
            "user_id": user_id,
            "products": products,
            "total": len(products)
        })

    def purchase(self, user_id: str, product_code: str, amount: float) -> Dict[str, Any]:
        """Subscription financial management/fund

        Args:
            user_id: ConsumerID
            product_code: Product code
            amount: Subscription amount

        Returns:
            Application result
        """
        if amount <= 0:
            return self._error_response("The subscription amount must be greater than0", "INVALID_AMOUNT")

        subscription_id = f"SUB{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return self._success_response({
            "subscription_id": subscription_id,
            "user_id": user_id,
            "product_code": product_code,
            "amount": amount,
            "status": "success",
            "message": "Successful application"
        })

    def redeem(self, user_id: str, product_code: str, amount: float) -> Dict[str, Any]:
        """Redemption financial management/fund

        Args:
            user_id: ConsumerID
            product_code: Product code
            amount: Redemption amount

        Returns:
            Redemption result
        """
        if amount <= 0:
            return self._error_response("The redemption amount must be greater than0", "INVALID_AMOUNT")

        redeem_id = f"RDM{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return self._success_response({
            "redeem_id": redeem_id,
            "user_id": user_id,
            "product_code": product_code,
            "amount": amount,
            "status": "processing",
            "message": "The redemption application has been submitted, and T+1 is expected to arrive."
        })

    def new_stock_apply(self, user_id: str, stock_code: str, amount: float) -> Dict[str, Any]:
        """Subscription of new shares/new bonds

        Args:
            user_id: ConsumerID
            stock_code: New stock/new bond code
            amount: Subscription amount

        Returns:
            Application result
        """
        if amount <= 0:
            return self._error_response("The subscription amount must be greater than0", "INVALID_AMOUNT")

        apply_id = f"NEW{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return self._success_response({
            "apply_id": apply_id,
            "user_id": user_id,
            "stock_code": stock_code,
            "stock_name": "New stock simulation",
            "amount": amount,
            "status": "success",
            "message": "Successful subscription of new shares, waiting for the number to be assigned"
        })

    def get_subscription(self, user_id: str) -> Dict[str, Any]:
        """Check the subscription/signing record

        Args:
            user_id: ConsumerID

        Returns:
            List of subscription records
        """
        records = [
            {
                "subscription_id": "SUB202609010001",
                "product_code": "FUND001",
                "product_name": "Steady Growth Fund",
                "amount": 10000.00,
                "status": "success",
                "created_at": "2026-09-01 10:00:00"
            },
            {
                "apply_id": "NEW202609020001",
                "stock_code": "001001",
                "stock_name": "A new stock",
                "amount": 10000.00,
                "lot_number": "123456",
                "win_status": "pending",
                "created_at": "2026-09-02 09:30:00"
            }
        ]

        return self._success_response({
            "user_id": user_id,
            "records": records,
            "total": len(records)
        })


if __name__ == "__main__":
    # Local test
    api = TradeAPI()
    print("Test to check the balance:")
    print(api.get_balance("test_user"))
    print("\nTest and place an order:")
    print(api.place_order("test_user", "600036", "buy", 36.50, 1000))
