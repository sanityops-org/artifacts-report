#!/usr/bin/env python3
"""Consulting skills test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.inquiry.handler import main


class TestInquiryHandler:
    """Consulting skill test"""

    def test_query_quote(self):
        """Test and query the stock market"""
        result = main({
            "action": "query_quote",
            "params": {"stock_code": "600036"}
        })
        assert result["status"] == "success"
        assert result["data"]["code"] == "600036"
        assert result["data"]["name"] == "China Merchants Bank"

    def test_query_quote_not_found(self):
        """Test and query non-existent stocks"""
        result = main({
            "action": "query_quote",
            "params": {"stock_code": "999999"}
        })
        assert result["status"] == "error"

    def test_query_fund_nav(self):
        """Test and query the net value of the fund"""
        result = main({
            "action": "query_fund_nav",
            "params": {"fund_code": "FUND001"}
        })
        assert result["status"] == "success"
        assert "nav" in result["data"]

    def test_business_guide(self):
        """Test business guidelines"""
        result = main({
            "action": "business_guide",
            "params": {"topic": "How to transfer money"}
        })
        assert result["status"] == "success"
        assert "guide" in result["data"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
