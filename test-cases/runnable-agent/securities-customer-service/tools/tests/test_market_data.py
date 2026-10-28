#!/usr/bin/env python3
"""Market data interface unit test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.market_data import MarketData


class TestMarketData:
    """Market data interface test class"""

    def setup_method(self):
        self.market = MarketData()

    def test_get_quote_success(self):
        """Test and query the stock market"""
        result = self.market.get_quote("600036")
        assert result["status"] == "success"
        assert result["data"]["code"] == "600036"
        assert "name" in result["data"]
        assert "price" in result["data"]
        assert "change" in result["data"]
        assert "change_pct" in result["data"]

    def test_get_quote_with_name(self):
        """Test the stock market including the name"""
        result = self.market.get_quote("600036")
        assert result["data"]["name"] == "China Merchants Bank"

    def test_get_fund_nav_success(self):
        """Test and query the net value of the fund"""
        result = self.market.get_fund_nav("FUND001")
        assert result["status"] == "success"
        assert result["data"]["code"] == "FUND001"
        assert "name" in result["data"]
        assert "nav" in result["data"]
        assert "nav_date" in result["data"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
