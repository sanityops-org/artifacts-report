#!/usr/bin/env python3
"""Transaction password verification"""

import yaml
import time
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict


class PasswordVerifier:
    """Transaction password verification

    Verify the user's transaction password (simulated implementation).
    The production environment should call the real password verification service.
    Support the password retry limit and account lock function.
    """

    # Simulate password storage (actually call the back-end service)
    MOCK_PASSWORD = "123456"

    # Locking time (seconds), the default is 30 minutes
    LOCK_TTL_SECONDS = 1800

    # Retry to record TTL (seconds), the default is 30 minutes
    RETRY_TTL_SECONDS = 1800

    def __init__(self, config_path: str = None):
        """Initialize the password verifier

        Args:
            config_path: Configuration file path
        """
        self.max_retry = 3

        # Failed retry count:{user_id: [(timestamp, attempt_count)]}
        self._failed_attempts: Dict[str, list] = defaultdict(list)

        # Locked status:{user_id: lock_timestamp}
        self._locked_users: Dict[str, float] = {}

        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "thresholds.yaml"

        self._load_config(config_path)

    def _load_config(self, config_path: Path) -> None:
        """Load the configuration file"""
        try:
            if Path(config_path).exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config and 'max_password_retry' in config:
                        self.max_retry = config['max_password_retry']
        except Exception:
            pass

    def _is_locked(self, user_id: str) -> bool:
        """Check whether the user is locked

        Args:
            user_id: ConsumerID

        Returns:
            If the user is locked, return True, otherwise returnFalse
        """
        if user_id not in self._locked_users:
            return False

        lock_time = self._locked_users[user_id]
        current_time = time.time()

        # Check whether the lock has expired
        if current_time - lock_time > self.LOCK_TTL_SECONDS:
            # The lock has expired. Clear the lock status.
            del self._locked_users[user_id]
            self._clear_failed_attempts(user_id)
            return False

        return True

    def _get_failed_count(self, user_id: str) -> int:
        """Get the number of failed attempts of users (valid count within the TTL range)

        Args:
            user_id: ConsumerID

        Returns:
            The number of valid failed attempts
        """
        self._cleanup_expired_attempts(user_id)
        return len(self._failed_attempts[user_id])

    def _record_failed_attempt(self, user_id: str) -> None:
        """Record failed attempts

        Args:
            user_id: ConsumerID
        """
        self._failed_attempts[user_id].append(time.time())

    def _clear_failed_attempts(self, user_id: str) -> None:
        """Clear the user's failed attempt record

        Args:
            user_id: ConsumerID
        """
        if user_id in self._failed_attempts:
            del self._failed_attempts[user_id]

    def _lock_user(self, user_id: str) -> None:
        """Lock the user

        Args:
            user_id: ConsumerID
        """
        self._locked_users[user_id] = time.time()

    def _cleanup_expired_attempts(self, user_id: str) -> None:
        """Clean up the expired failed attempt records

        Args:
            user_id: ConsumerID
        """
        if user_id not in self._failed_attempts:
            return

        current_time = time.time()
        self._failed_attempts[user_id] = [
            ts for ts in self._failed_attempts[user_id]
            if current_time - ts < self.RETRY_TTL_SECONDS
        ]

    def verify(self, user_id: str, password: str) -> Dict[str, Any]:
        """Verify the transaction password

        Args:
            user_id: ConsumerID
            password: The transaction password entered by the user

        Returns:
            Dictionaries containing the following fields:
            - success: bool, Verify whether it is successful
            - error_code: str, Error code (in case of failure)
            - message: str, Prompt message
            - retry_count: int, The number of current failures (in case of failure)
            - remaining_retries: int, Remaining number of retries (in case of failure)
        """
        # Check whether it is locked
        if self._is_locked(user_id):
            return {
                "success": False,
                "error_code": "LOCKED",
                "message": "The password is wrong too many times, and the account has been locked. Please contact manual customer service or try again after 30 minutes."
            }

        # Empty password check
        if not password:
            return {
                "success": False,
                "error_code": "EMPTY_PASSWORD",
                "message": "Please enter the transaction password."
            }

        # Simulated password verification (actually the transaction system interface should be called)
        if password == self.MOCK_PASSWORD:
            # Verification is successful, clear the failure record
            self._clear_failed_attempts(user_id)
            return {
                "success": True,
                "message": "Password verification is successful"
            }
        else:
            # Record failed attempts
            self._record_failed_attempt(user_id)
            failed_count = self._get_failed_count(user_id)
            remaining_retries = max(0, self.max_retry - failed_count)

            # Check whether the maximum number of retrials has been reached.
            if failed_count >= self.max_retry:
                # Lock the user
                self._lock_user(user_id)
                return {
                    "success": False,
                    "error_code": "LOCKED",
                    "message": "The password is wrong too many times, and the account has been locked. Please contact manual customer service or try again after 30 minutes.",
                    "retry_count": failed_count,
                    "remaining_retries": 0
                }

            return {
                "success": False,
                "error_code": "WRONG_PASSWORD",
                "message": f"Wrong password. You can try {remaining_retries} more times.",
                "retry_count": failed_count,
                "remaining_retries": remaining_retries
            }


if __name__ == "__main__":
    # Local test
    verifier = PasswordVerifier()
    print("Test the correct password:")
    print(verifier.verify("test_user", "123456"))
    print("\nTest the wrong password (the first time):")
    print(verifier.verify("test_user", "wrong"))
    print("\nTest the wrong password (the second time):")
    print(verifier.verify("test_user", "wrong"))
    print("\nTest the wrong password (the third time, trigger the lock):")
    print(verifier.verify("test_user", "wrong"))
    print("\nVerification after the test is locked:")
    print(verifier.verify("test_user", "123456"))
