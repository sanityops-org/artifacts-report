#!/usr/bin/env python3
"""Tests for the get_policy tool."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from get_policy import execute


RULE_IDS = [
    "meal_limit_per_person",
    "hotel_limit_per_night",
    "receipt_required_above",
    "prohibited_category",
    "submission_window",
    "approval_required_above",
    "weekend_non_travel_meal",
]


class TestGetPolicy(unittest.TestCase):
    """Test cases for the effective policy and override merging."""

    def _rule(self, policy, rule_id):
        return next(r for r in policy["rules"] if r["id"] == rule_id)

    def test_defaults_returned_unchanged(self):
        """With no overrides, every default rule is returned as specified."""
        result = execute({})

        self.assertEqual(result["status"], "success")
        policy = result["data"]
        self.assertEqual(policy["version"], "2026.1")
        self.assertEqual(policy["currency"], "USD")
        self.assertEqual([r["id"] for r in policy["rules"]], RULE_IDS)
        self.assertEqual(policy["overrides_applied"], [])

    def test_default_thresholds(self):
        """Every documented default value is present and exact."""
        policy = execute({})["data"]

        self.assertEqual(self._rule(policy, "meal_limit_per_person")["limit"], 75.00)
        self.assertEqual(self._rule(policy, "meal_limit_per_person")["unit_field"], "attendees")
        self.assertEqual(self._rule(policy, "hotel_limit_per_night")["limit"], 250.00)
        self.assertEqual(self._rule(policy, "hotel_limit_per_night")["unit_field"], "nights")
        self.assertEqual(self._rule(policy, "receipt_required_above")["threshold"], 25.00)
        self.assertEqual(self._rule(policy, "submission_window")["max_days"], 60)
        self.assertEqual(self._rule(policy, "approval_required_above")["threshold"], 500.00)
        self.assertEqual(
            self._rule(policy, "prohibited_category")["blocked"],
            ["alcohol", "gambling", "personal_items", "fines"],
        )

    def test_default_severities(self):
        """Each rule carries the severity specified in the design."""
        policy = execute({})["data"]

        self.assertEqual(self._rule(policy, "meal_limit_per_person")["severity"], "high")
        self.assertEqual(self._rule(policy, "hotel_limit_per_night")["severity"], "high")
        self.assertEqual(self._rule(policy, "receipt_required_above")["severity"], "medium")
        self.assertEqual(self._rule(policy, "prohibited_category")["severity"], "high")
        self.assertEqual(self._rule(policy, "submission_window")["severity"], "medium")
        self.assertEqual(self._rule(policy, "approval_required_above")["severity"], "medium")
        self.assertEqual(self._rule(policy, "weekend_non_travel_meal")["severity"], "low")
        self.assertEqual(policy["duplicate_detection"]["severity"], "high")

    def test_duplicate_detection_defaults(self):
        """Duplicate detection carries its own block with tolerance and window."""
        policy = execute({})["data"]

        config = policy["duplicate_detection"]
        self.assertEqual(config["id"], "duplicate_suspected")
        self.assertEqual(config["amount_tolerance_pct"], 1.0)
        self.assertEqual(config["date_window_days"], 3)

    def test_single_field_override_merges_and_leaves_siblings(self):
        """Overriding one field leaves the rule's other fields untouched."""
        result = execute({"overrides": {"hotel_limit_per_night": {"limit": 200.00}}})

        self.assertEqual(result["status"], "success")
        rule = self._rule(result["data"], "hotel_limit_per_night")
        self.assertEqual(rule["limit"], 200.00)
        self.assertEqual(rule["unit_field"], "nights")
        self.assertEqual(rule["category"], "lodging")
        self.assertEqual(rule["severity"], "high")
        self.assertEqual(
            rule["description"], "Lodging must not exceed $250 per night"
        )

    def test_overrides_do_not_mutate_defaults(self):
        """A second call without overrides still returns the original defaults."""
        execute({"overrides": {"hotel_limit_per_night": {"limit": 1.00}}})

        rule = self._rule(execute({})["data"], "hotel_limit_per_night")

        self.assertEqual(rule["limit"], 250.00)

    def test_overrides_applied_records_before_and_after(self):
        """Each changed field is reported with its default and effective value."""
        result = execute(
            {
                "overrides": {
                    "hotel_limit_per_night": {"limit": 200.00},
                    "submission_window": {"max_days": 90},
                }
            }
        )

        applied = result["data"]["overrides_applied"]
        self.assertEqual(len(applied), 2)
        by_rule = {entry["rule_id"]: entry for entry in applied}
        self.assertEqual(by_rule["hotel_limit_per_night"]["field"], "limit")
        self.assertEqual(by_rule["hotel_limit_per_night"]["default"], 250.00)
        self.assertEqual(by_rule["hotel_limit_per_night"]["effective"], 200.00)
        self.assertEqual(by_rule["submission_window"]["default"], 60)
        self.assertEqual(by_rule["submission_window"]["effective"], 90)

    def test_overriding_a_list_field(self):
        """A list-valued field such as the blocklist is replaced wholesale."""
        result = execute(
            {"overrides": {"prohibited_category": {"blocked": ["alcohol"]}}}
        )

        rule = self._rule(result["data"], "prohibited_category")
        self.assertEqual(rule["blocked"], ["alcohol"])

    def test_unknown_rule_id_errors_with_valid_list(self):
        """An unknown rule id is an error that lists every valid id."""
        result = execute({"overrides": {"no_such_rule": {"limit": 1}}})

        self.assertEqual(result["status"], "error")
        self.assertIn("no_such_rule", result["error"])
        for rule_id in RULE_IDS:
            self.assertIn(rule_id, result["error"])

    def test_unknown_field_in_override_errors(self):
        """An override naming a field the rule does not have is an error."""
        result = execute({"overrides": {"meal_limit_per_person": {"banana": 1}}})

        self.assertEqual(result["status"], "error")
        self.assertIn("banana", result["error"])
        self.assertIn("meal_limit_per_person", result["error"])

    def test_overrides_must_be_an_object(self):
        """A non-object overrides value is an error."""
        result = execute({"overrides": ["not", "an", "object"]})

        self.assertEqual(result["status"], "error")
        self.assertIn("overrides", result["error"])

    def test_override_value_must_be_an_object(self):
        """A non-object value for a rule's overrides is an error."""
        result = execute({"overrides": {"submission_window": 90}})

        self.assertEqual(result["status"], "error")
        self.assertIn("submission_window", result["error"])

    def test_duplicate_detection_is_overridable(self):
        """The duplicate_suspected block can be tuned through the same mechanism."""
        result = execute(
            {"overrides": {"duplicate_suspected": {"date_window_days": 7}}}
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["duplicate_detection"]["date_window_days"], 7)
        self.assertEqual(result["data"]["duplicate_detection"]["amount_tolerance_pct"], 1.0)

    def test_rule_ids_filter(self):
        """The rule_ids parameter narrows the returned rules list."""
        result = execute({"rule_ids": ["meal_limit_per_person", "submission_window"]})

        self.assertEqual(result["status"], "success")
        self.assertEqual(
            [r["id"] for r in result["data"]["rules"]],
            ["meal_limit_per_person", "submission_window"],
        )

    def test_rule_ids_filter_keeps_duplicate_detection(self):
        """Duplicate detection is an independent block and survives the filter."""
        result = execute({"rule_ids": ["meal_limit_per_person"]})

        self.assertEqual(result["data"]["duplicate_detection"]["id"], "duplicate_suspected")

    def test_rule_ids_unknown_id_errors(self):
        """An unknown id in rule_ids is an error naming it."""
        result = execute({"rule_ids": ["nope"]})

        self.assertEqual(result["status"], "error")
        self.assertIn("nope", result["error"])


if __name__ == "__main__":
    unittest.main()