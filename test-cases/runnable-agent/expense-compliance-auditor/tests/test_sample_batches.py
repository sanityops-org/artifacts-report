#!/usr/bin/env python3
"""End-to-end tests asserting the expected outcome of each sample batch."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from audit_expenses import execute as audit_expenses
from detect_duplicates import execute as detect_duplicates
from generate_report import execute as generate_report
from get_policy import execute as get_policy
from parse_expenses import execute as parse_expenses


SAMPLES = PROJECT_ROOT / "data" / "sample_expenses"
AUDITED_AT = "2026-10-09T12:00:00"


def run_audit(filename):
    """Run the full audit chain over one sample file."""
    parsed = parse_expenses({"file_path": str(SAMPLES / filename)})
    assert parsed["status"] == "success", parsed.get("error")

    policy = get_policy({})["data"]
    audited = audit_expenses(
        {"records": parsed["data"]["records"], "policy": policy}
    )
    assert audited["status"] == "success", audited.get("error")

    duplicates = detect_duplicates(
        {"records": parsed["data"]["records"], "policy": policy}
    )
    assert duplicates["status"] == "success", duplicates.get("error")

    return parsed["data"], audited["data"], duplicates["data"], policy


def build_report(filename):
    """Run the full chain and render the report."""
    parsed_data, audited_data, duplicates_data, policy = run_audit(filename)
    report = generate_report(
        {
            "evaluations": audited_data["evaluations"],
            "record_summary": audited_data["record_summary"],
            "totals": audited_data["totals"],
            "duplicate_groups": duplicates_data["groups"],
            "parse_failures": parsed_data["parse_failures"],
            "policy": policy,
            "batch_metadata": {
                "source_file": filename,
                "audited_at": AUDITED_AT,
                "records": parsed_data["records"],
            },
            "format": "markdown",
        }
    )
    assert report["status"] == "success", report.get("error")
    return parsed_data, audited_data, duplicates_data, report["data"]


class TestCleanBatch(unittest.TestCase):
    """The clean batch must produce no findings at all."""

    def test_every_record_is_read(self):
        parsed, _, _, _ = build_report("clean_batch.csv")
        self.assertEqual(parsed["parse_failures"], [])
        self.assertEqual(parsed["record_count"], 6)

    def test_totals_are_all_passing(self):
        _, audited, _, _ = build_report("clean_batch.csv")
        self.assertEqual(
            audited["totals"],
            {"records": 6, "pass": 6, "violation": 0, "needs_review": 0},
        )

    def test_no_evaluation_is_a_finding(self):
        _, audited, _, _ = build_report("clean_batch.csv")
        findings = [e for e in audited["evaluations"] if e["verdict"] != "pass"]
        self.assertEqual(findings, [])

    def test_report_summary_is_empty(self):
        _, _, _, report = build_report("clean_batch.csv")
        self.assertEqual(report["summary"]["violation"], 0)
        self.assertEqual(report["summary"]["needs_review"], 0)
        self.assertEqual(report["summary"]["high"], 0)

    def test_no_duplicate_groups(self):
        _, _, duplicates, _ = build_report("clean_batch.csv")
        self.assertEqual(duplicates["groups"], [])


class TestViolationsBatch(unittest.TestCase):
    """The violations batch must trip each rule exactly once."""

    def test_every_record_is_read(self):
        parsed, _, _, _ = build_report("violations_batch.csv")
        self.assertEqual(parsed["parse_failures"], [])
        self.assertEqual(parsed["record_count"], 10)

    def test_totals(self):
        _, audited, _, _ = build_report("violations_batch.csv")
        self.assertEqual(
            audited["totals"],
            {"records": 10, "pass": 3, "violation": 6, "needs_review": 1},
        )

    def test_severity_counts(self):
        _, _, _, report = build_report("violations_batch.csv")
        summary = report["summary"]
        self.assertEqual(summary["high"], 3)
        self.assertEqual(summary["medium"], 3)
        self.assertEqual(summary["low"], 1)

    def test_each_rule_fires_exactly_once(self):
        _, audited, _, _ = build_report("violations_batch.csv")
        violations = [
            e for e in audited["evaluations"] if e["verdict"] == "violation"
        ]
        by_rule = {}
        for evaluation in violations:
            by_rule.setdefault(evaluation["rule_id"], []).append(
                evaluation["record_id"]
            )

        self.assertEqual(by_rule["meal_limit_per_person"], ["EXP-2001"])
        self.assertEqual(by_rule["hotel_limit_per_night"], ["EXP-2002"])
        self.assertEqual(by_rule["receipt_required_above"], ["EXP-2003"])
        self.assertEqual(by_rule["prohibited_category"], ["EXP-2004"])
        self.assertEqual(by_rule["submission_window"], ["EXP-2005"])
        self.assertEqual(by_rule["approval_required_above"], ["EXP-2006"])

    def test_weekend_meal_is_flagged_for_review(self):
        _, audited, _, _ = build_report("violations_batch.csv")
        flagged = [
            e for e in audited["evaluations"] if e["verdict"] == "needs_review"
        ]
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0]["rule_id"], "weekend_non_travel_meal")
        self.assertEqual(flagged[0]["record_id"], "EXP-2007")

    def test_boundary_records_pass(self):
        """Records sitting exactly on a threshold must pass, not violate."""
        _, audited, _, _ = build_report("violations_batch.csv")
        summary = {
            entry["record_id"]: entry["overall"]
            for entry in audited["record_summary"]
        }

        self.assertEqual(summary["EXP-2008"], "pass")
        self.assertEqual(summary["EXP-2009"], "pass")
        self.assertEqual(summary["EXP-2010"], "pass")

    def test_meal_overage_is_reported_exactly(self):
        _, audited, _, _ = build_report("violations_batch.csv")
        evaluation = next(
            e
            for e in audited["evaluations"]
            if e["record_id"] == "EXP-2001" and e["verdict"] == "violation"
        )

        self.assertEqual(evaluation["actual"]["per_person"], 120.00)
        self.assertEqual(evaluation["limit"], 75.00)
        self.assertEqual(evaluation["overage"], 45.00)

    def test_late_submission_reports_elapsed_days(self):
        _, audited, _, _ = build_report("violations_batch.csv")
        evaluation = next(
            e
            for e in audited["evaluations"]
            if e["record_id"] == "EXP-2005" and e["verdict"] == "violation"
        )

        self.assertEqual(evaluation["actual"]["days_elapsed"], 96)
        self.assertEqual(evaluation["overage"], 36)

    def test_report_lists_every_violation(self):
        _, _, _, report = build_report("violations_batch.csv")
        text = report["report"]
        for record_id in (
            "EXP-2001", "EXP-2002", "EXP-2003",
            "EXP-2004", "EXP-2005", "EXP-2006",
        ):
            self.assertIn(record_id, text)
        self.assertIn("EXP-2007", text)


class TestDuplicatesBatch(unittest.TestCase):
    """The duplicates batch must group only the intended records."""

    def test_every_record_is_read(self):
        parsed, _, _, _ = build_report("duplicates_batch.json")
        self.assertEqual(parsed["parse_failures"], [])
        self.assertEqual(parsed["record_count"], 12)

    def test_three_groups_are_found(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        self.assertEqual(len(duplicates["groups"]), 3)
        self.assertEqual(
            [g["group_id"] for g in duplicates["groups"]],
            ["DUP-001", "DUP-002", "DUP-003"],
        )

    def test_exact_duplicate_pair(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        group = duplicates["groups"][0]
        self.assertEqual(
            [r["record_id"] for r in group["records"]], ["EXP-3001", "EXP-3002"]
        )
        self.assertEqual(group["merchant"], "Blue Bottle Coffee")
        self.assertEqual(group["amount"], 64.50)

    def test_within_tolerance_pair(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        group = duplicates["groups"][1]
        self.assertEqual(
            [r["record_id"] for r in group["records"]], ["EXP-3003", "EXP-3004"]
        )

    def test_transitive_chain_is_one_group(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        group = duplicates["groups"][2]
        self.assertEqual(
            [r["record_id"] for r in group["records"]],
            ["EXP-3007", "EXP-3008", "EXP-3009"],
        )

    def test_out_of_tolerance_pair_not_grouped(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        grouped = {
            member["record_id"]
            for group in duplicates["groups"]
            for member in group["records"]
        }
        self.assertNotIn("EXP-3005", grouped)
        self.assertNotIn("EXP-3006", grouped)

    def test_different_employee_not_grouped(self):
        """EXP-3010 matches EXP-3003 on merchant and amount but not on employee."""
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        grouped = {
            member["record_id"]
            for group in duplicates["groups"]
            for member in group["records"]
        }
        self.assertNotIn("EXP-3010", grouped)

    def test_records_without_merchant_or_date_are_excluded(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        grouped = {
            member["record_id"]
            for group in duplicates["groups"]
            for member in group["records"]
        }
        self.assertNotIn("EXP-3011", grouped)
        self.assertNotIn("EXP-3012", grouped)

    def test_duplicate_record_count(self):
        _, _, duplicates, _ = build_report("duplicates_batch.json")
        self.assertEqual(duplicates["duplicate_record_count"], 7)

    def test_report_lists_the_groups(self):
        _, _, _, report = build_report("duplicates_batch.json")
        text = report["report"]
        self.assertIn("## Suspected Duplicates", text)
        self.assertIn("Blue Bottle Coffee", text)
        self.assertIn("Corner Deli", text)

    def test_duplicates_are_not_reported_as_violations(self):
        """Duplication is advisory: it never adds a violation."""
        _, audited, duplicates, _ = build_report("duplicates_batch.json")
        rule_ids = {e["rule_id"] for e in audited["evaluations"]}
        self.assertNotIn("duplicate_suspected", rule_ids)
        self.assertTrue(duplicates["groups"])


if __name__ == "__main__":
    unittest.main()
