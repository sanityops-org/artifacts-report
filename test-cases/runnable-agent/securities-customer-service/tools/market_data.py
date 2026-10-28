#!/usr/bin/env python3
"""Market data interface (analog data)"""

from typing import Dict, Any
from datetime import datetime


class MarketData:
    """Market data interface

    Simulate the stock market and fund net value inquiry interface.
    All data are analog data for development and testing.
    """

    # Simulated stock data
    STOCK_DATA = {
        "600036": {
            "code": "600036",
            "name": "China Merchants Bank",
            "price": 36.50,
            "change": 0.45,
            "change_pct": 1.25,
            "open": 36.10,
            "high": 36.80,
            "low": 36.00,
            "volume": 12580000,
            "amount": 458000000
        },
        "600519": {
            "code": "600519",
            "name": "Maotai, Guizhou",
            "price": 1725.00,
            "change": 45.00,
            "change_pct": 2.68,
            "open": 1690.00,
            "high": 1730.00,
            "low": 1685.00,
            "volume": 850000,
            "amount": 1460000000
        },
        "000001": {
            "code": "000001",
            "name": "Ping An Bank",
            "price": 12.05,
            "change": -0.15,
            "change_pct": -1.23,
            "open": 12.20,
            "high": 12.30,
            "low": 11.95,
            "volume": 35000000,
            "amount": 420000000
        },
        "000002": {
            "code": "000002",
            "name": "VankeA",
            "price": 8.50,
            "change": 0.10,
            "change_pct": 1.19,
            "open": 8.40,
            "high": 8.60,
            "low": 8.35,
            "volume": 50000000,
            "amount": 425000000
        }
    }

    # Simulated fund data
    FUND_DATA = {
        "FUND001": {
            "code": "FUND001",
            "name": "Steady Growth Fund",
            "nav": 1.2500,
            "nav_date": "2026-09-02",
            "accumulated_nav": 1.5800,
            "daily_change": 0.0020,
            "daily_change_pct": 0.16
        },
        "FUND002": {
            "code": "FUND002",
            "name": "Science and Technology Growth Fund",
            "nav": 2.1800,
            "nav_date": "2026-09-02",
            "accumulated_nav": 2.4500,
            "daily_change": 0.0350,
            "daily_change_pct": 1.63
        }
    }

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

    def get_quote(self, stock_code: str) -> Dict[str, Any]:
        """Check the real-time stock market

        Args:
            stock_code: Stock code, such as "600036"

        Returns:
            Dictionaries containing real-time stock prices:
            - code: Stock code
            - name: Stock name
            - price: Current price
            - change: The amount of increase and fall
            - change_pct: Percentage of rise and fall
            - open: Opening price
            - high: The highest price
            - low: The lowest price
            - volume: Trading volume (shares)
            - amount: Turnover (yuan)
        """
        if stock_code in self.STOCK_DATA:
            return self._success_response(self.STOCK_DATA[stock_code])

        return self._error_response(
            f"No stock code found {stock_code}",
            "STOCK_NOT_FOUND"
        )

    def get_fund_nav(self, fund_code: str) -> Dict[str, Any]:
        """Check the net value of the fund

        Args:
            fund_code: Fund code, such as "FUND001"

        Returns:
            Dictionary containing the net value information of the fund:
            - code: Fund code
            - name: Name of the fund
            - nav: Unit net value
            - nav_date: Net value date
            - accumulated_nav: Cumulative net worth
            - daily_change: Daily rise and fall amount
            - daily_change_pct: Percentage of daily rise and fall
        """
        if fund_code in self.FUND_DATA:
            return self._success_response(self.FUND_DATA[fund_code])

        return self._error_response(
            f"No fund code found {fund_code}",
            "FUND_NOT_FOUND"
        )


if __name__ == "__main__":
    # Local test
    market = MarketData()
    print("Test stock market inquiry:")
    print(market.get_quote("600036"))
    print("\nTest fund net value inquiry:")
    print(market.get_fund_nav("FUND001"))
