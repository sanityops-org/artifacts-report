#!/usr/bin/env python3
"""Tests for the audit_expenses rule engine."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from audit_expenses import execute
from get_policy import execute as get_policy


POLICY = get_policy({})["data"]


def _record(**overrides):
    """Build a normalized record that passes every default rule."""
    base = {
        "record_id": "EXP-1",
        "employee_id": "E-1",
        "employee_name": "Jane Doe",
        "expense_date": "2026-10-05",
        "submitted_date": "2026-10-06",
        "category": "supplies",
        "merchant": "Acme",
        "amount": 10.00,
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


def _evaluations(result, rule_id):
    return [e for e in result["data"]["evaluations"] if e["rule_id"] == rule_id]


def _one(result, rule_id):
    matches = _evaluations(result, rule_id)
    assert len(matches) == 1, f"expected 1 evaluation for {rule_id}, got {len(matches)}"
    return matches[0]


class TestAuditExpenses(unittest.TestCase):
    """Test cases for per-record, per-rule evaluation."""

    def _run(self, *records):
        return execute({"records": list(records), "policy": POLICY})

    # --- per_unit_limit: meals ---

    def test_meal_limit_violation(self):
        """A per-person meal cost over the limit is a violation with an overage."""
        result = self._run(
            _record(category="meals", amount=120.00, attendees=1)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["severity"], "high")
        self.assertEqual(evaluation["limit"], 75.00)
        self.assertEqual(evaluation["actual"]["per_person"], 120.00)
        self.assertEqual(evaluation["actual"]["attendees"], 1)
        self.assertEqual(evaluation["overage"], 45.00)

    def test_meal_limit_pass(self):
        """A per-person meal cost under the limit passes."""
        result = self._run(
            _record(category="meals", amount=45.00, attendees=1)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertIsNone(evaluation["overage"])

    def test_meal_limit_boundary_exactly_at_limit_passes(self):
        """A per-person cost exactly equal to the limit passes, not violates."""
        result = self._run(
            _record(category="meals", amount=75.00, attendees=1)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertEqual(evaluation["actual"]["per_person"], 75.00)

    def test_meal_limit_divides_by_attendees(self):
        """The per-person figure divides the amount by the attendee count."""
        result = self._run(
            _record(category="meals", amount=225.00, attendees=3)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertEqual(evaluation["actual"]["per_person"], 75.00)

    def test_meal_limit_missing_attendees_is_needs_review(self):
        """A meal without an attendee count cannot be evaluated."""
        result = self._run(
            _record(category="meals", amount=120.00, attendees=None)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("attendees", evaluation["message"])

    def test_meal_limit_zero_attendees_is_needs_review(self):
        """A zero attendee count would divide by zero, so it is flagged instead."""
        result = self._run(
            _record(category="meals", amount=120.00, attendees=0)
        )

        evaluation = _one(result, "meal_limit_per_person")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("attendees", evaluation["message"])

    # --- per_unit_limit: lodging ---

    def test_hotel_limit_violation(self):
        """A per-night lodging cost over the limit is a violation."""
        result = self._run(
            _record(category="lodging", amount=600.00, nights=2, approval_id="APR-1")
        )

        evaluation = _one(result, "hotel_limit_per_night")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["actual"]["per_night"], 300.00)
        self.assertEqual(evaluation["overage"], 50.00)

    def test_hotel_limit_boundary_exactly_at_limit_passes(self):
        """A per-night cost exactly equal to the limit passes."""
        result = self._run(
            _record(category="lodging", amount=500.00, nights=2, approval_id="APR-1")
        )

        evaluation = _one(result, "hotel_limit_per_night")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_hotel_limit_missing_nights_is_needs_review(self):
        """Lodging without a night count cannot be evaluated."""
        result = self._run(
            _record(category="lodging", amount=600.00, nights=None, approval_id="APR-1")
        )

        evaluation = _one(result, "hotel_limit_per_night")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("nights", evaluation["message"])

    # --- receipt_required ---

    def test_receipt_required_violation(self):
        """An expense at or above the threshold without a receipt violates."""
        result = self._run(_record(amount=80.00, receipt_attached=False))

        evaluation = _one(result, "receipt_required_above")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["severity"], "medium")

    def test_receipt_required_boundary_at_threshold_with_receipt_passes(self):
        """Exactly at the threshold with a receipt attached passes."""
        result = self._run(_record(amount=25.00, receipt_attached=True))

        evaluation = _one(result, "receipt_required_above")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_receipt_required_boundary_at_threshold_without_receipt_violates(self):
        """Exactly at the threshold without a receipt violates."""
        result = self._run(_record(amount=25.00, receipt_attached=False))

        evaluation = _one(result, "receipt_required_above")
        self.assertEqual(evaluation["verdict"], "violation")

    def test_receipt_not_required_below_threshold(self):
        """Below the threshold, a missing receipt is not a violation."""
        result = self._run(_record(amount=24.99, receipt_attached=False))

        evaluation = _one(result, "receipt_required_above")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_receipt_missing_field_is_needs_review(self):
        """An unknown receipt status at or above the threshold is flagged."""
        result = self._run(_record(amount=80.00, receipt_attached=None))

        evaluation = _one(result, "receipt_required_above")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("receipt_attached", evaluation["message"])

    # --- category_blocklist ---

    def test_prohibited_category_violation(self):
        """A blocked category is a violation."""
        result = self._run(_record(category="alcohol", amount=55.00))

        evaluation = _one(result, "prohibited_category")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["severity"], "high")
        self.assertEqual(evaluation["actual"]["category"], "alcohol")

    def test_prohibited_category_pass(self):
        """An allowed category passes."""
        result = self._run(_record(category="supplies"))

        evaluation = _one(result, "prohibited_category")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_prohibited_category_missing_is_needs_review(self):
        """A record with no category cannot be checked against the blocklist."""
        result = self._run(_record(category=None))

        evaluation = _one(result, "prohibited_category")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("category", evaluation["message"])

    # --- date_window ---

    def test_submission_window_violation(self):
        """Submitting more than 60 days after the expense date violates."""
        result = self._run(
            _record(expense_date="2026-07-01", submitted_date="2026-10-05")
        )

        evaluation = _one(result, "submission_window")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["actual"]["days_elapsed"], 96)
        self.assertEqual(evaluation["overage"], 36)

    def test_submission_window_boundary_exactly_60_days_passes(self):
        """Exactly 60 days elapsed passes."""
        result = self._run(
            _record(expense_date="2026-08-06", submitted_date="2026-10-05")
        )

        evaluation = _one(result, "submission_window")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertEqual(evaluation["actual"]["days_elapsed"], 60)

    def test_submission_window_same_day_passes(self):
        """A same-day submission passes."""
        result = self._run(
            _record(expense_date="2026-10-05", submitted_date="2026-10-05")
        )

        evaluation = _one(result, "submission_window")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertEqual(evaluation["actual"]["days_elapsed"], 0)

    def test_submission_window_missing_submitted_date_is_needs_review(self):
        """Without a submission date the window cannot be computed."""
        result = self._run(_record(submitted_date=None))

        evaluation = _one(result, "submission_window")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("submitted_date", evaluation["message"])

    def test_submission_window_missing_expense_date_is_needs_review(self):
        """Without an expense date the window cannot be computed."""
        result = self._run(_record(expense_date=None))

        evaluation = _one(result, "submission_window")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("expense_date", evaluation["message"])

    # --- approval_required ---

    def test_approval_required_violation(self):
        """At or above the threshold without an approval ID violates."""
        result = self._run(_record(amount=750.00, approval_id=None))

        evaluation = _one(result, "approval_required_above")
        self.assertEqual(evaluation["verdict"], "violation")
        self.assertEqual(evaluation["severity"], "medium")

    def test_approval_required_boundary_at_threshold_with_approval_passes(self):
        """Exactly at the threshold with an approval ID passes."""
        result = self._run(_record(amount=500.00, approval_id="APR-5555"))

        evaluation = _one(result, "approval_required_above")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_approval_required_boundary_at_threshold_without_approval_violates(self):
        """Exactly at the threshold without an approval ID violates."""
        result = self._run(_record(amount=500.00, approval_id=None))

        evaluation = _one(result, "approval_required_above")
        self.assertEqual(evaluation["verdict"], "violation")

    def test_approval_not_required_below_threshold(self):
        """Below the threshold, a missing approval ID is not a violation."""
        result = self._run(_record(amount=499.99, approval_id=None))

        evaluation = _one(result, "approval_required_above")
        self.assertEqual(evaluation["verdict"], "pass")

    # --- review_flag ---

    def test_weekend_non_travel_meal_needs_review(self):
        """A Saturday meal not marked as travel is flagged for review."""
        result = self._run(
            _record(
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-10",
                is_travel=False,
            )
        )

        evaluation = _one(result, "weekend_non_travel_meal")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertEqual(evaluation["severity"], "low")
        self.assertEqual(evaluation["actual"]["weekday"], "Saturday")

    def test_sunday_non_travel_meal_needs_review(self):
        """A Sunday meal not marked as travel is flagged for review."""
        result = self._run(
            _record(
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-11",
                is_travel=False,
            )
        )

        evaluation = _one(result, "weekend_non_travel_meal")
        self.assertEqual(evaluation["verdict"], "needs_review")

    def test_weekend_travel_meal_passes(self):
        """A weekend meal marked as travel is not flagged."""
        result = self._run(
            _record(
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-10",
                is_travel=True,
            )
        )

        evaluation = _one(result, "weekend_non_travel_meal")
        self.assertEqual(evaluation["verdict"], "pass")

    def test_weekday_meal_passes_review_flag(self):
        """A weekday meal is not flagged."""
        result = self._run(
            _record(
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-05",
                is_travel=False,
            )
        )

        evaluation = _one(result, "weekend_non_travel_meal")
        self.assertEqual(evaluation["verdict"], "pass")
        self.assertEqual(evaluation["actual"]["weekday"], "Monday")

    def test_weekend_meal_missing_date_is_needs_review(self):
        """A weekend check without an expense date cannot be evaluated."""
        result = self._run(
            _record(category="meals", amount=40.00, attendees=1, expense_date=None)
        )

        evaluation = _one(result, "weekend_non_travel_meal")
        self.assertEqual(evaluation["verdict"], "needs_review")
        self.assertIn("expense_date", evaluation["message"])

    # --- applicability ---

    def test_category_scoped_rules_emit_nothing_for_other_categories(self):
        """Rules naming a category produce no evaluation at all for other categories."""
        result = self._run(_record(category="supplies", amount=10.00))

        self.assertEqual(_evaluations(result, "meal_limit_per_person"), [])
        self.assertEqual(_evaluations(result, "hotel_limit_per_night"), [])
        self.assertEqual(_evaluations(result, "weekend_non_travel_meal"), [])

    def test_category_agnostic_rules_apply_to_every_record(self):
        """Threshold, receipt, window, and approval rules apply regardless of category."""
        result = self._run(_record(category="supplies", amount=10.00))

        for rule_id in (
            "receipt_required_above",
            "prohibited_category",
            "submission_window",
            "approval_required_above",
        ):
            self.assertEqual(
                len(_evaluations(result, rule_id)), 1, f"{rule_id} should apply"
            )

    # --- currency ---

    def test_non_usd_record_flags_every_amount_threshold_rule(self):
        """A non-USD record is flagged on every rule that compares an amount."""
        result = self._run(
            _record(
                currency="EUR",
                category="meals",
                amount=120.00,
                attendees=1,
                approval_id=None,
            )
        )

        for rule_id in (
            "meal_limit_per_person",
            "receipt_required_above",
            "approval_required_above",
        ):
            evaluation = _one(result, rule_id)
            self.assertEqual(evaluation["verdict"], "needs_review", rule_id)
            self.assertIn("EUR", evaluation["message"])
            self.assertIn("exchange rate", evaluation["message"])

    def test_non_usd_record_does_not_affect_non_amount_rules(self):
        """Category, date, and review rules still evaluate normally for a non-USD record."""
        result = self._run(
            _record(
                currency="EUR",
                category="alcohol",
                amount=55.00,
                expense_date="2026-07-01",
                submitted_date="2026-10-05",
            )
        )

        self.assertEqual(_one(result, "prohibited_category")["verdict"], "violation")
        self.assertEqual(_one(result, "submission_window")["verdict"], "violation")

    # --- rollup and totals ---

    def test_violation_dominates_needs_review_in_rollup(self):
        """A record with both a violation and a flagged rule rolls up as a violation."""
        result = self._run(
            _record(
                category="meals",
                amount=120.00,
                attendees=1,
                expense_date="2026-10-10",
                is_travel=False,
            )
        )

        summary = result["data"]["record_summary"][0]
        self.assertEqual(summary["overall"], "violation")
        self.assertGreater(summary["review_count"], 0)
        self.assertGreater(summary["violation_count"], 0)

    def test_needs_review_rollup_when_no_violation(self):
        """A record with only flags rolls up as needs_review."""
        result = self._run(
            _record(
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-10",
                is_travel=False,
            )
        )

        summary = result["data"]["record_summary"][0]
        self.assertEqual(summary["overall"], "needs_review")
        self.assertEqual(summary["violation_count"], 0)

    def test_pass_rollup(self):
        """A record satisfying every applicable rule rolls up as pass."""
        result = self._run(_record(amount=10.00))

        summary = result["data"]["record_summary"][0]
        self.assertEqual(summary["overall"], "pass")
        self.assertEqual(summary["violation_count"], 0)
        self.assertEqual(summary["review_count"], 0)

    def test_pass_evaluations_are_emitted_alongside_violations(self):
        """Passing evaluations are returned, not only failures."""
        result = self._run(_record(amount=10.00))

        verdicts = {e["verdict"] for e in result["data"]["evaluations"]}
        self.assertEqual(verdicts, {"pass"})

    def test_totals_counts(self):
        """Totals tally records by their overall verdict."""
        result = self._run(
            _record(record_id="A", amount=10.00),
            _record(record_id="B", amount=750.00, approval_id=None),
            _record(
                record_id="C",
                category="meals",
                amount=40.00,
                attendees=1,
                expense_date="2026-10-10",
                is_travel=False,
            ),
        )

        self.assertEqual(
            result["data"]["totals"],
            {"records": 3, "pass": 1, "violation": 1, "needs_review": 1},
        )

    def test_duplicate_detection_is_not_a_per_record_rule(self):
        """The duplicate_suspected block is never evaluated per record."""
        result = self._run(_record(amount=10.00))

        self.assertEqual(_evaluations(result, "duplicate_suspected"), [])

    def test_every_evaluation_carries_traceability_fields(self):
        """Each evaluation names its rule, describes it, and reports actual vs limit."""
        result = self._run(_record(category="meals", amount=120.00, attendees=1))

        for evaluation in result["data"]["evaluations"]:
            self.assertIn("record_id", evaluation)
            self.assertIn("rule_id", evaluation)
            self.assertIn("rule_description", evaluation)
            self.assertIn("actual", evaluation)
            self.assertIn("limit", evaluation)
            self.assertIn("message", evaluation)

    def test_engine_is_pure(self):
        """Auditing the same records twice yields identical results."""
        records = [_record(category="meals", amount=120.00, attendees=1)]

        first = self._run(*records)
        second = self._run(*records)

        self.assertEqual(first, second)

    # --- error handling ---

    def test_records_must_be_a_list(self):
        """A non-list records value is an error."""
        result = execute({"records": "nope", "policy": POLICY})

        self.assertEqual(result["status"], "error")
        self.assertIn("records", result["error"])

    def test_policy_must_carry_rules(self):
        """A policy without a rules list is an error."""
        result = execute({"records": [], "policy": {}})

        self.assertEqual(result["status"], "error")
        self.assertIn("policy", result["error"])

    def test_empty_record_list_succeeds_with_zero_totals(self):
        """An empty record list is a valid, empty audit."""
        result = execute({"records": [], "policy": POLICY})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["evaluations"], [])
        self.assertEqual(
            result["data"]["totals"],
            {"records": 0, "pass": 0, "violation": 0, "needs_review": 0},
        )


if __name__ == "__main__":
    unittest.main()