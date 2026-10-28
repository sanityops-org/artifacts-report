#!/usr/bin/env python3
"""Amount threshold judgment"""

import yaml
from pathlib import Path
from typing import Dict, Any


class AmountChecker:
    """Amount threshold judgment

    Determine whether the transaction amount needs to be confirmed by the transaction password.
    The threshold is read from the configuration file, and the default is 50,000 yuan.
    """

    DEFAULT_THRESHOLD = 50000

    def __init__(self, config_path: str = None):
        """Initialize the amount checker

        Args:
            config_path: The configuration file path, the default is config/thresholds.yaml
        """
        self.threshold = self.DEFAULT_THRESHOLD

        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "thresholds.yaml"

        self._load_config(config_path)

    def _load_config(self, config_path: Path) -> None:
        """Load the configuration file

        Args:
            config_path: Configuration file path
        """
        try:
            if Path(config_path).exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config and 'password_threshold' in config:
                        self.threshold = config['password_threshold']
        except Exception:
            # Use the default value when the configuration fails to load
            pass

    def check(self, amount: float) -> Dict[str, Any]:
        """Determine whether the amount needs a password confirmation

        Args:
            amount: Transaction amount (unit: yuan)

        Returns:
            Dictionaries containing the following fields:
            - need_password: bool, Do you need a password confirmation?
            - threshold: float, Current threshold
            - amount: float, Operation amount
        """
        need_password = amount > self.threshold

        return {
            "need_password": need_password,
            "threshold": self.threshold,
            "amount": amount
        }


if __name__ == "__main__":
    # Local test
    checker = AmountChecker()
    print("Test 10,000 yuan:")
    print(checker.check(10000))
    print("\nTest 80,000 yuan:")
    print(checker.check(80000))
