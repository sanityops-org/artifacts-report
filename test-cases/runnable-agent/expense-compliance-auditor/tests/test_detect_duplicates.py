#!/usr/bin/env python3
"""Tests for the detect_duplicates tool."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from detect_duplicates import execute
from get_policy import execute as get_policy


POLICY = get_policy({})["data"]


def _record(**overrides):
    """Build a normalized record that matches the default duplicate criteria."""
    base = {
        "record_id": "EXP-1",
        "employee_id": "E-1",
        "employee_name": "Jane Doe",
        "expense_date": "2026-10-05",
        "submitted_date": "2026-10-06",
        "category": "supplies",
        "merchant": "Acme",
        "amount": 100.00,
        "currency": "USD",
        "attendees": None,
        "nights": None,
        "receipt_attached": True,
        "approval_id": None,
        "is_travel": False,
        "notes": None,
    }
    base.update(overrides)
    return base


class TestDetectDuplicates(unittest.TestCase):
    """Test cases for cross-record duplicate detection."""

    def _run(self, *records):
        return execute({"records": list(records), "policy": POLICY})

    def test_exact_duplicate_is_grouped(self):
        """Two identical records form one group."""
        result = self._run(
            _record(record_id="EXP-1"),
            _record(record_id="EXP-2"),
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["groups"]), 1)
        group = result["data"]["groups"][0]
        self.assertEqual(group["group_id"], "DUP-001")
        self.assertEqual(group["rule_id"], "duplicate_suspected")
        self.assertEqual(
            [r["record_id"] for r in group["records"]], ["EXP-1", "EXP-2"]
        )
        self.assertEqual(result["data"]["duplicate_record_count"], 2)

    def test_distinct_records_produce_no_groups(self):
        """Different merchants or amounts do not group."""
        result = self._run(
            _record(record_id="EXP-1", merchant="Acme"),
            _record(record_id="EXP-2", merchant="Other Co"),
        )

        self.assertEqual(result["data"]["groups"], [])
        self.assertEqual(result["data"]["duplicate_record_count"], 0)

    def test_amount_within_tolerance_is_grouped(self):
        """A 0.5% amount difference falls inside the 1% tolerance."""
        result = self._run(
            _record(record_id="EXP-1", amount=100.00),
            _record(record_id="EXP-2", amount=100.50),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)

    def test_amount_exactly_at_tolerance_is_grouped(self):
        """A difference of exactly 1% is grouped; the tolerance is inclusive."""
        result = self._run(
            _record(record_id="EXP-1", amount=99.00),
            _record(record_id="EXP-2", amount=100.00),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)

    def test_amount_outside_tolerance_is_not_grouped(self):
        """A 2% amount difference falls outside the tolerance."""
        result = self._run(
            _record(record_id="EXP-1", amount=98.00),
            _record(record_id="EXP-2", amount=100.00),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_date_within_window_is_grouped(self):
        """Dates 3 days apart group; the window is inclusive."""
        result = self._run(
            _record(record_id="EXP-1", expense_date="2026-10-05"),
            _record(record_id="EXP-2", expense_date="2026-10-08"),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)

    def test_date_outside_window_is_not_grouped(self):
        """Dates 4 days apart do not group."""
        result = self._run(
            _record(record_id="EXP-1", expense_date="2026-10-05"),
            _record(record_id="EXP-2", expense_date="2026-10-09"),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_transitive_chain_forms_one_group(self):
        """A matches B and B matches C, so all three land in a single group."""
        result = self._run(
            _record(record_id="EXP-1", expense_date="2026-10-05", amount=30.00),
            _record(record_id="EXP-2", expense_date="2026-10-07", amount=30.20),
            _record(record_id="EXP-3", expense_date="2026-10-09", amount=30.40),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)
        group = result["data"]["groups"][0]
        self.assertEqual(
            [r["record_id"] for r in group["records"]],
            ["EXP-1", "EXP-2", "EXP-3"],
        )
        self.assertEqual(result["data"]["duplicate_record_count"], 3)

    def test_chain_endpoints_are_outside_tolerance_but_still_grouped(self):
        """The endpoints of a transitive chain need not match each other directly."""
        chain = [
            _record(record_id="EXP-1", expense_date="2026-10-05", amount=30.00),
            _record(record_id="EXP-2", expense_date="2026-10-07", amount=30.20),
            _record(record_id="EXP-3", expense_date="2026-10-09", amount=30.40),
        ]

        direct = self._run(chain[0], chain[2])
        chained = self._run(*chain)

        self.assertEqual(direct["data"]["groups"], [])
        self.assertEqual(len(chained["data"]["groups"]), 1)

    def test_different_employees_do_not_group(self):
        """Identical expenses by different employees are separate records."""
        result = self._run(
            _record(record_id="EXP-1", employee_id="E-1"),
            _record(record_id="EXP-2", employee_id="E-2"),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_falls_back_to_employee_name_when_id_is_missing(self):
        """Without an employee_id, the name identifies the submitter."""
        result = self._run(
            _record(record_id="EXP-1", employee_id=None, employee_name="Jane Doe"),
            _record(record_id="EXP-2", employee_id=None, employee_name="Jane Doe"),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)

    def test_missing_employee_identity_excludes_the_record(self):
        """A record with no employee_id and no name cannot be matched."""
        result = self._run(
            _record(record_id="EXP-1", employee_id=None, employee_name=None),
            _record(record_id="EXP-2", employee_id=None, employee_name=None),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_merchant_matching_ignores_case_and_whitespace(self):
        """Merchant comparison normalizes case and internal whitespace."""
        result = self._run(
            _record(record_id="EXP-1", merchant="Office  Depot"),
            _record(record_id="EXP-2", merchant="office depot"),
        )

        self.assertEqual(len(result["data"]["groups"]), 1)

    def test_null_merchant_is_excluded(self):
        """A record with no merchant is not grouped by a null value."""
        result = self._run(
            _record(record_id="EXP-1", merchant=None),
            _record(record_id="EXP-2", merchant=None),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_null_expense_date_is_excluded(self):
        """A record with no expense date is not grouped by a null value."""
        result = self._run(
            _record(record_id="EXP-1", expense_date=None),
            _record(record_id="EXP-2", expense_date=None),
        )

        self.assertEqual(result["data"]["groups"], [])

    def test_multiple_independent_groups(self):
        """Unrelated duplicate sets become separate groups with sequential ids."""
        result = self._run(
            _record(record_id="EXP-1", merchant="Acme", amount=10.00),
            _record(record_id="EXP-2", merchant="Acme", amount=10.00),
            _record(record_id="EXP-3", merchant="Beta", amount=90.00),
            _record(record_id="EXP-4", merchant="Beta", amount=90.00),
        )

        groups = result["data"]["groups"]
        self.assertEqual(len(groups), 2)
        self.assertEqual([g["group_id"] for g in groups], ["DUP-001", "DUP-002"])
        self.assertEqual(groups[0]["merchant"], "Acme")
        self.assertEqual(groups[1]["merchant"], "Beta")
        self.assertEqual(result["data"]["duplicate_record_count"], 4)

    def test_group_ids_are_stable_across_runs(self):
        """Re-running on the same input yields identical group ids and ordering."""
        records = [
            _record(record_id="EXP-1", merchant="Acme", amount=10.00),
            _record(record_id="EXP-2", merchant="Acme", amount=10.00),
            _record(record_id="EXP-3", merchant="Beta", amount=90.00),
            _record(record_id="EXP-4", merchant="Beta", amount=90.00),
        ]

        self.assertEqual(self._run(*records), self._run(*records))

    def test_group_records_are_in_input_order(self):
        """Members of a group appear in the order they were submitted."""
        result = self._run(
            _record(record_id="EXP-9", amount=100.00),
            _record(record_id="EXP-1", amount=100.00),
            _record(record_id="EXP-5", amount=100.00),
        )

        group = result["data"]["groups"][0]
        self.assertEqual(
            [r["record_id"] for r in group["records"]],
            ["EXP-9", "EXP-1", "EXP-5"],
        )

    def test_single_record_produces_no_groups(self):
        """One record can never duplicate itself."""
        result = self._run(_record(record_id="EXP-1"))

        self.assertEqual(result["data"]["groups"], [])
        self.assertEqual(result["data"]["duplicate_record_count"], 0)

    def test_matching_basis_is_reported(self):
        """Each group states the tolerance and window that produced it."""
        result = self._run(
            _record(record_id="EXP-1"),
            _record(record_id="EXP-2"),
        )

        basis = result["data"]["groups"][0]["matching_basis"]
        self.assertEqual(basis["amount_tolerance_pct"], 1.0)
        self.assertEqual(basis["date_window_days"], 3)

    def test_custom_tolerance_from_policy_is_honored(self):
        """A tuned duplicate_detection block changes the matching behaviour."""
        policy = get_policy(
            {"overrides": {"duplicate_suspected": {"date_window_days": 10}}}
        )["data"]

        result = execute(
            {
                "records": [
                    _record(record_id="EXP-1", expense_date="2026-10-05"),
                    _record(record_id="EXP-2", expense_date="2026-10-12"),
                ],
                "policy": policy,
            }
        )

        self.assertEqual(len(result["data"]["groups"]), 1)
        self.assertEqual(
            result["data"]["groups"][0]["matching_basis"]["date_window_days"], 10
        )

    def test_records_must_be_a_list(self):
        """A non-list records value is an error."""
        result = execute({"records": "nope", "policy": POLICY})

        self.assertEqual(result["status"], "error")
        self.assertIn("records", result["error"])

    def test_missing_duplicate_detection_block_is_an_error(self):
        """A policy without duplicate_detection is an error."""
        result = execute({"records": [], "policy": {"rules": []}})

        self.assertEqual(result["status"], "error")
        self.assertIn("duplicate_detection", result["error"])

    def test_empty_record_list_succeeds_with_no_groups(self):
        """An empty record list is a valid, empty result."""
        result = execute({"records": [], "policy": POLICY})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["groups"], [])
        self.assertEqual(result["data"]["duplicate_record_count"], 0)


if __name__ == "__main__":
    unittest.main()