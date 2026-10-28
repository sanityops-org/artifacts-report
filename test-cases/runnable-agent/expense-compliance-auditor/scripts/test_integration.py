#!/usr/bin/env python3
"""Integration script: run the full audit chain over every sample batch."""

import sys
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


def audit_one(filename):
    """Run the chain over a single sample file and print its report."""
    print("=" * 68)
    print(f"  {filename}")
    print("=" * 68)

    parsed = parse_expenses({"file_path": str(SAMPLES / filename)})
    if parsed["status"] != "success":
        print(f"  PARSE ERROR: {parsed['error']}")
        return 1

    data = parsed["data"]
    print(f"  Records: {data['record_count']}   Parse failures: {len(data['parse_failures'])}")

    policy = get_policy({})["data"]
    audited = audit_expenses({"records": data["records"], "policy": policy})["data"]
    duplicates = detect_duplicates({"records": data["records"], "policy": policy})["data"]

    report = generate_report(
        {
            "evaluations": audited["evaluations"],
            "record_summary": audited["record_summary"],
            "totals": audited["totals"],
            "duplicate_groups": duplicates["groups"],
            "parse_failures": data["parse_failures"],
            "policy": policy,
            "batch_metadata": {
                "source_file": filename,
                "audited_at": AUDITED_AT,
                "records": data["records"],
            },
            "format": "markdown",
        }
    )

    if report["status"] != "success":
        print(f"  REPORT ERROR: {report['error']}")
        return 1

    print()
    print(report["data"]["report"])
    return 0


def main():
    """Audit every sample batch."""
    print()
    print("Expense Compliance Auditor - Integration Test")
    print()

    failures = 0
    for filename in ("clean_batch.csv", "violations_batch.csv", "duplicates_batch.json"):
        failures += audit_one(filename)
        print()

    if failures:
        print(f"Integration test failed for {failures} batch(es).")
        return 1

    print("Integration test completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
