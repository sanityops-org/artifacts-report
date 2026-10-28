#!/usr/bin/env python3
"""Tests for the generate_report tool."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from generate_report import execute
from get_policy import execute as get_policy


POLICY = get_policy({})["data"]
AUDITED_AT = "2026-10-09T12:00:00"


def _record(record_id="EXP-1", **overrides):
    base = {
        "record_id": record_id,
        "employee_id": "E-1",
        "employee_name": "Jane Doe",
        "expense_date": "2026-10-05",
        "submitted_date": "2026-10-06",
        "category": "meals",
        "merchant": "Acme",
        "amount": 120.00,
        "currency": "USD",
        "attendees": 1,
        "nights": None,
        "receipt_attached": True,
        "approval_id": None,
        "is_travel": False,
        "notes": None,
    }
    base.update(overrides)
    return base


def _evaluation(record_id, rule_id, verdict, severity, **overrides):
    evaluation = {
        "record_id": record_id,
        "rule_id": rule_id,
        "rule_description": f"Description for {rule_id}",
        "verdict": verdict,
        "severity": severity,
        "actual": {"amount": 120.00},
        "limit": 75.00,
        "overage": 45.00,
        "message": f"Message for {rule_id}",
    }
    evaluation.update(overrides)
    return evaluation


def _totals(records=1, passed=0, violation=0, needs_review=0):
    return {
        "records": records,
        "pass": passed,
        "violation": violation,
        "needs_review": needs_review,
    }


def _batch(records=None, source_file="batch.csv"):
    return {
        "source_file": source_file,
        "audited_at": AUDITED_AT,
        "records": records if records is not None else [_record()],
    }


def _markdown(evaluations, totals, batch, **extras):
    params = {
        "evaluations": evaluations,
        "record_summary": [],
        "totals": totals,
        "policy": POLICY,
        "batch_metadata": batch,
        "format": "markdown",
    }
    params.update(extras)
    return execute(params)


class TestGenerateReport(unittest.TestCase):
    """Test cases for report rendering."""

    def test_header_carries_batch_policy_and_timestamp(self):
        """The report header names the batch, policy version, time, and record count."""
        result = _markdown(
            [_evaluation("EXP-1", "meal_limit_per_person", "violation", "high")],
            _totals(records=1, violation=1),
            _batch(source_file="my_batch.csv"),
        )

        self.assertEqual(result["status"], "success")
        report = result["data"]["report"]
        self.assertIn("my_batch.csv", report)
        self.assertIn("2026.1", report)
        self.assertIn(AUDITED_AT, report)
        self.assertIn("**Records**: 1", report)

    def test_summary_counts_by_verdict_and_severity(self):
        """The summary reflects totals and the severity of the findings."""
        result = _markdown(
            [
                _evaluation("EXP-1", "meal_limit_per_person", "violation", "high"),
                _evaluation("EXP-2", "receipt_required_above", "violation", "medium"),
                _evaluation("EXP-3", "weekend_non_travel_meal", "needs_review", "low"),
            ],
            _totals(records=4, passed=1, violation=2, needs_review=1),
            _batch(),
        )

        summary = result["data"]["summary"]
        self.assertEqual(summary["records"], 4)
        self.assertEqual(summary["pass"], 1)
        self.assertEqual(summary["violation"], 2)
        self.assertEqual(summary["needs_review"], 1)
        self.assertEqual((summary["high"], summary["medium"], summary["low"]), (1, 1, 1))

    def test_findings_are_ordered_by_severity_then_record(self):
        """Findings sort high, then medium, then low; within a severity by record id."""
        result = _markdown(
            [
                _evaluation("EXP-9", "submission_window", "violation", "low"),
                _evaluation("EXP-5", "receipt_required_above", "violation", "medium"),
                _evaluation("EXP-3", "prohibited_category", "violation", "high"),
                _evaluation("EXP-1", "meal_limit_per_person", "violation", "high"),
            ],
            _totals(records=4, violation=4),
            _batch(),
        )

        report = result["data"]["report"]
        positions = [report.index(f"`{rule}`") for rule in (
            "meal_limit_per_person",
            "prohibited_category",
            "receipt_required_above",
            "submission_window",
        )]
        self.assertEqual(positions, sorted(positions))

    def test_ordering_is_stable_across_runs(self):
        """Identical input renders identical output."""
        evaluations = [
            _evaluation("EXP-2", "receipt_required_above", "violation", "medium"),
            _evaluation("EXP-1", "meal_limit_per_person", "violation", "high"),
        ]
        first = _markdown(evaluations, _totals(records=2, violation=2), _batch())
        second = _markdown(evaluations, _totals(records=2, violation=2), _batch())

        self.assertEqual(first, second)

    def test_passing_evaluations_are_not_listed_as_findings(self):
        """Only violations and flagged items appear in the findings sections."""
        result = _markdown(
            [
                _evaluation("EXP-1", "meal_limit_per_person", "violation", "high"),
                _evaluation("EXP-1", "submission_window", "pass", "medium"),
            ],
            _totals(records=1, violation=1),
            _batch(),
        )

        report = result["data"]["report"]
        violations_section = report.split("## Needs Review")[0]
        self.assertIn("meal_limit_per_person", violations_section)
        self.assertNotIn("submission_window", violations_section)

    def test_violation_entry_carries_traceability_fields(self):
        """A violation entry shows the rule id, description, actual, limit, and overage."""
        result = _markdown(
            [_evaluation("EXP-1", "meal_limit_per_person", "violation", "high")],
            _totals(records=1, violation=1),
            _batch(),
        )

        report = result["data"]["report"]
        self.assertIn("`meal_limit_per_person`", report)
        self.assertIn("Description for meal_limit_per_person", report)
        self.assertIn("amount", report)
        self.assertIn("75.00", report)
        self.assertIn("45.00", report)

    def test_record_context_appears_in_the_finding_heading(self):
        """The heading names the employee, category, and amount from the record."""
        result = _markdown(
            [_evaluation("EXP-1", "meal_limit_per_person", "violation", "high")],
            _totals(records=1, violation=1),
            _batch(records=[_record("EXP-1", employee_name="Jane Doe", category="meals")]),
        )

        self.assertIn("Jane Doe", result["data"]["report"])
        self.assertIn("EXP-1", result["data"]["report"])

    def test_needs_review_section_lists_the_reason(self):
        """A flagged record appears under Needs Review with its message."""
        result = _markdown(
            [
                _evaluation(
                    "EXP-1",
                    "hotel_limit_per_night",
                    "needs_review",
                    "high",
                    message="Cannot evaluate: 'nights' is missing from this record",
                )
            ],
            _totals(records=1, needs_review=1),
            _batch(),
        )

        report = result["data"]["report"]
        self.assertIn("## Needs Review", report)
        self.assertIn("'nights' is missing", report)

    def test_duplicates_section_rendered(self):
        """Duplicate groups appear with their matching basis."""
        groups = [
            {
                "group_id": "DUP-001",
                "rule_id": "duplicate_suspected",
                "merchant": "Blue Bottle Coffee",
                "amount": 64.50,
                "records": [
                    {
                        "record_id": "EXP-1",
                        "employee_id": "E-1",
                        "employee_name": "Jane Doe",
                        "expense_date": "2026-10-05",
                        "amount": 64.50,
                    },
                    {
                        "record_id": "EXP-2",
                        "employee_id": "E-1",
                        "employee_name": "Jane Doe",
                        "expense_date": "2026-10-05",
                        "amount": 64.50,
                    },
                ],
                "matching_basis": {"amount_tolerance_pct": 1.0, "date_window_days": 3},
                "severity": "high",
            }
        ]

        result = _markdown(
            [], _totals(records=2, passed=2), _batch(), duplicate_groups=groups
        )

        report = result["data"]["report"]
        self.assertIn("## Suspected Duplicates", report)
        self.assertIn("Blue Bottle Coffee", report)
        self.assertIn("EXP-2", report)

    def test_policy_reference_lists_every_rule(self):
        """The policy reference makes the report self-contained."""
        result = _markdown([], _totals(records=0, passed=0), _batch(records=[]))

        report = result["data"]["report"]
        self.assertIn("## Policy Reference", report)
        for rule_id in (
            "meal_limit_per_person",
            "hotel_limit_per_night",
            "receipt_required_above",
            "prohibited_category",
            "submission_window",
            "approval_required_above",
            "weekend_non_travel_meal",
        ):
            self.assertIn(f"`{rule_id}`", report)

    def test_policy_reference_marks_overridden_values(self):
        """A rule changed by an override is flagged as non-default."""
        policy = get_policy(
            {"overrides": {"hotel_limit_per_night": {"limit": 200.00}}}
        )["data"]

        result = execute(
            {
                "evaluations": [],
                "record_summary": [],
                "totals": _totals(records=0, passed=0),
                "policy": policy,
                "batch_metadata": _batch(records=[]),
                "format": "markdown",
            }
        )

        report = result["data"]["report"]
        self.assertIn("200.00", report)
        self.assertIn("overridden", report)

    def test_parse_failures_are_listed(self):
        """Unreadable rows are surfaced so a reader knows the batch was partial."""
        result = _markdown(
            [],
            _totals(records=1, passed=1),
            _batch(),
            parse_failures=[
                {"row": 7, "reason": "amount is missing or not a number: ''", "raw": {}}
            ],
        )

        report = result["data"]["report"]
        self.assertIn("## Parse Failures", report)
        self.assertIn("| 7 |", report)

    def test_parse_failures_section_omitted_when_none(self):
        """With no failures the section is not emitted."""
        result = _markdown([], _totals(records=1, passed=1), _batch())

        self.assertNotIn("## Parse Failures", result["data"]["report"])

    def test_report_carries_no_approval_language(self):
        """The report records status only; it never approves or rejects."""
        result = _markdown(
            [_evaluation("EXP-1", "meal_limit_per_person", "violation", "high")],
            _totals(records=1, violation=1),
            _batch(),
        )

        report = result["data"]["report"].lower()
        for phrase in ("approved", "approve this", "rejected", "denied"):
            self.assertNotIn(phrase, report)

    def test_json_format_returns_a_parseable_document(self):
        """The JSON format emits structured findings with the same ordering."""
        result = execute(
            {
                "evaluations": [
                    _evaluation("EXP-2", "receipt_required_above", "violation", "medium"),
                    _evaluation("EXP-1", "meal_limit_per_person", "violation", "high"),
                ],
                "record_summary": [],
                "totals": _totals(records=2, violation=2),
                "policy": POLICY,
                "batch_metadata": _batch(),
                "format": "json",
            }
        )

        self.assertEqual(result["data"]["format"], "json")
        document = json.loads(result["data"]["report"])
        self.assertEqual(document["batch"]["source_file"], "batch.csv")
        self.assertEqual(document["batch"]["policy_version"], "2026.1")
        self.assertEqual(
            [v["rule_id"] for v in document["violations"]],
            ["meal_limit_per_person", "receipt_required_above"],
        )
        self.assertEqual(document["summary"]["high"], 1)
        self.assertEqual(document["summary"]["medium"], 1)

    def test_json_format_includes_policy_and_failures(self):
        """The JSON document carries the policy reference and parse failures."""
        result = execute(
            {
                "evaluations": [],
                "record_summary": [],
                "totals": _totals(records=0, passed=0),
                "policy": POLICY,
                "batch_metadata": _batch(records=[]),
                "format": "json",
                "parse_failures": [{"row": 3, "reason": "bad amount", "raw": {}}],
            }
        )

        document = json.loads(result["data"]["report"])
        self.assertEqual(document["policy"]["version"], "2026.1")
        self.assertEqual(len(document["policy"]["rules"]), 7)
        self.assertEqual(document["parse_failures"][0]["row"], 3)

    def test_format_defaults_to_markdown(self):
        """Omitting the format renders Markdown."""
        result = execute(
            {
                "evaluations": [],
                "record_summary": [],
                "totals": _totals(records=0, passed=0),
                "policy": POLICY,
                "batch_metadata": _batch(records=[]),
            }
        )

        self.assertEqual(result["data"]["format"], "markdown")
        self.assertTrue(result["data"]["report"].startswith("# Expense Audit Report"))

    def test_unsupported_format_is_an_error(self):
        """A format other than markdown or json is rejected."""
        result = execute(
            {
                "evaluations": [],
                "record_summary": [],
                "totals": _totals(records=0, passed=0),
                "policy": POLICY,
                "batch_metadata": _batch(records=[]),
                "format": "pdf",
            }
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("pdf", result["error"])

    def test_evaluations_must_be_a_list(self):
        """A non-list evaluations value is an error."""
        result = execute(
            {
                "evaluations": "nope",
                "record_summary": [],
                "totals": _totals(),
                "policy": POLICY,
                "batch_metadata": _batch(),
            }
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("evaluations", result["error"])

    def test_batch_metadata_is_required(self):
        """Missing batch metadata is an error."""
        result = execute(
            {
                "evaluations": [],
                "record_summary": [],
                "totals": _totals(),
                "policy": POLICY,
            }
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("batch_metadata", result["error"])


if __name__ == "__main__":
    unittest.main()
