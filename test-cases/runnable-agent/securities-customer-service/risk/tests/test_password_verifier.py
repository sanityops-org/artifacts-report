#!/usr/bin/env python3
"""Transaction password verification unit test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from risk.password_verifier import PasswordVerifier


class TestPasswordVerifier:
    """Transaction password verification test class"""

    def setup_method(self):
        self.verifier = PasswordVerifier()

    def test_verify_success(self):
        """Successful test password verification"""
        result = self.verifier.verify("test_user_001", "123456")
        assert result["success"] is True
        assert result["message"] == "Password verification is successful"

    def test_verify_wrong_password(self):
        """The test password is wrong"""
        result = self.verifier.verify("test_user_001", "wrong_password")
        assert result["success"] is False
        assert result["error_code"] == "WRONG_PASSWORD"
        assert "retry_count" in result
        assert result["retry_count"] == 1

    def test_verify_empty_password(self):
        """Test the empty password"""
        result = self.verifier.verify("test_user_001", "")
        assert result["success"] is False
        assert result["error_code"] == "EMPTY_PASSWORD"

    def test_retry_counting(self):
        """Test and retry counting"""
        # The first mistake
        result1 = self.verifier.verify("test_user_retry", "wrong1")
        assert result1["success"] is False
        assert result1["retry_count"] == 1
        assert result1["remaining_retries"] == 2

        # The second mistake
        result2 = self.verifier.verify("test_user_retry", "wrong2")
        assert result2["success"] is False
        assert result2["retry_count"] == 2
        assert result2["remaining_retries"] == 1

    def test_lockout_after_max_retries(self):
        """Locked after the test reaches the maximum number of retrials"""
        user_id = "test_user_lockout"
        # Wrong password 3 times in a row
        for i in range(3):
            result = self.verifier.verify(user_id, f"wrong{i}")
            if i < 2:
                assert result["error_code"] == "WRONG_PASSWORD"
            else:
                assert result["error_code"] == "LOCKED"

        # Even if you enter the correct password after locking, you should fail.
        result = self.verifier.verify(user_id, "123456")
        assert result["success"] is False
        assert result["error_code"] == "LOCKED"

    def test_success_clears_failed_attempts(self):
        """Clear the failure record after the test is verified successfully."""
        user_id = "test_user_clear"
        # Enter the wrong password once
        self.verifier.verify(user_id, "wrong")
        # Enter the correct password
        self.verifier.verify(user_id, "123456")
        # Enter the wrong password again, and the count should start from 1.
        result = self.verifier.verify(user_id, "wrong")
        assert result["retry_count"] == 1

    def test_different_users_independent(self):
        """Test that the failure count of different users is independent of each other."""
        user1 = "test_user_independent_1"
        user2 = "test_user_independent_2"

        # user1 Enter the wrong password
        self.verifier.verify(user1, "wrong")
        self.verifier.verify(user1, "wrong")

        # user2 Enter the wrong password (should start from 1)
        result = self.verifier.verify(user2, "wrong")
        assert result["retry_count"] == 1

    def test_remaining_retries_calculation(self):
        """Calculate the remaining number of retryes for testing"""
        user_id = "test_user_remaining"
        result1 = self.verifier.verify(user_id, "wrong")
        assert result1["remaining_retries"] == 2

        result2 = self.verifier.verify(user_id, "wrong")
        assert result2["remaining_retries"] == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
