#!/usr/bin/env python3
"""Amount threshold judgment unit test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from risk.amount_checker import AmountChecker


class TestAmountChecker:
    """Amount threshold judgment test class"""

    def setup_method(self):
        self.checker = AmountChecker()

    def test_check_below_threshold(self):
        """The test amount is below the threshold."""
        result = self.checker.check(10000)
        assert result["need_password"] is False
        assert result["threshold"] == 50000
        assert result["amount"] == 10000

    def test_check_equal_threshold(self):
        """The test amount is equal to the threshold (not triggered)"""
        result = self.checker.check(50000)
        assert result["need_password"] is False

    def test_check_above_threshold(self):
        """The test amount exceeds the threshold."""
        result = self.checker.check(80000)
        assert result["need_password"] is True
        assert result["threshold"] == 50000
        assert result["amount"] == 80000

    def test_check_zero_amount(self):
        """The amount of the test is0"""
        result = self.checker.check(0)
        assert result["need_password"] is False

    def test_check_negative_amount(self):
        """Test the negative amount"""
        result = self.checker.check(-1000)
        assert result["need_password"] is False
        assert result["amount"] == -1000


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
