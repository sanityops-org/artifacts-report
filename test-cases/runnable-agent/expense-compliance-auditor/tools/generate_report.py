#!/usr/bin/env python3
"""
generate_report: Render expense audit results as a Markdown or JSON report.

Pure renderer: the audit timestamp is supplied by the caller rather than read
from the clock, so identical input always produces identical output. The report
records compliance status only and never approves or rejects an expense.
"""

import json
import sys
from typing import Any, Dict, List, Optional


SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_LABEL = {"high": "High", "medium": "Medium", "low": "Low"}
UNIT_LABELS = {"attendees": "person", "nights": "night"}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render audit results as a deliverable report.

    Args:
        params: {
            "evaluations": [ <from audit_expenses> ],
            "record_summary": [ <from audit_expenses> ],
            "totals": { <from audit_expenses> },
            "duplicate_groups": [ <from detect_duplicates> ],
            "parse_failures": [ <from parse_expenses> ],
            "policy": { <effective policy from get_policy> },
            "batch_metadata": {
                "source_file": str,
                "audited_at": str,
                "records": [ <normalized record> ]
            },
            "format": "markdown" | "json"
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "report": str,
                "format": "markdown" | "json",
                "summary": {
                    "records": int, "pass": int, "violation": int,
                    "needs_review": int, "high": int, "medium": int, "low": int
                }
            },
            "error": str | None
        }
    """
    evaluations = params.get("evaluations")
    record_summary = params.get("record_summary")
    totals = params.get("totals")
    policy = params.get("policy")
    batch_metadata = params.get("batch_metadata")
    report_format = params.get("format") or "markdown"

    if not isinstance(evaluations, list):
        return {
            "status": "error",
            "error": "evaluations must be a list from audit_expenses",
        }
    if not isinstance(record_summary, list):
        return {
            "status": "error",
            "error": "record_summary must be a list from audit_expenses",
        }
    if not isinstance(totals, dict):
        return {"status": "error", "error": "totals must be the object from audit_expenses"}
    if not isinstance(policy, dict):
        return {"status": "error", "error": "policy must be the object from get_policy"}
    if not isinstance(batch_metadata, dict):
        return {
            "status": "error",
            "error": "batch_metadata must be an object with source_file, audited_at, and records",
        }
    if report_format not in ("markdown", "json"):
        return {
            "status": "error",
            "error": (
                f"Unsupported format '{report_format}'. "
                "Supported formats: markdown, json"
            ),
        }

    duplicate_groups = params.get("duplicate_groups") or []
    parse_failures = params.get("parse_failures") or []
    records = batch_metadata.get("records") or []
    records_by_id = {
        record.get("record_id"): record for record in records if isinstance(record, dict)
    }

    findings = [e for e in evaluations if e.get("verdict") != "pass"]
    findings.sort(key=_finding_sort_key)

    violations = [e for e in findings if e.get("verdict") == "violation"]
    needs_review = [e for e in findings if e.get("verdict") == "needs_review"]

    summary = {
        "records": totals.get("records", 0),
        "pass": totals.get("pass", 0),
        "violation": totals.get("violation", 0),
        "needs_review": totals.get("needs_review", 0),
        "high": sum(1 for e in findings if e.get("severity") == "high"),
        "medium": sum(1 for e in findings if e.get("severity") == "medium"),
        "low": sum(1 for e in findings if e.get("severity") == "low"),
    }

    if report_format == "json":
        report = json.dumps(
            {
                "batch": {
                    "source_file": batch_metadata.get("source_file"),
                    "policy_version": policy.get("version"),
                    "audited_at": batch_metadata.get("audited_at"),
                    "records": summary["records"],
                },
                "summary": summary,
                "violations": violations,
                "needs_review": needs_review,
                "duplicates": duplicate_groups,
                "policy": {
                    "version": policy.get("version"),
                    "currency": policy.get("currency"),
                    "rules": policy.get("rules", []),
                    "duplicate_detection": policy.get("duplicate_detection"),
                    "overrides_applied": policy.get("overrides_applied", []),
                },
                "parse_failures": parse_failures,
            },
            indent=2,
        )
    else:
        report = _render_markdown(
            violations,
            needs_review,
            duplicate_groups,
            parse_failures,
            policy,
            batch_metadata,
            summary,
            records_by_id,
        )

    return {
        "status": "success",
        "data": {"report": report, "format": report_format, "summary": summary},
    }


def _finding_sort_key(evaluation: Dict[str, Any]):
    """Order findings by severity, then record id, then rule id."""
    severity = evaluation.get("severity", "medium")
    return (
        SEVERITY_ORDER.get(severity, 1),
        str(evaluation.get("record_id") or ""),
        str(evaluation.get("rule_id") or ""),
    )


def _render_markdown(
    violations: List[Dict[str, Any]],
    needs_review: List[Dict[str, Any]],
    duplicate_groups: List[Dict[str, Any]],
    parse_failures: List[Dict[str, Any]],
    policy: Dict[str, Any],
    batch_metadata: Dict[str, Any],
    summary: Dict[str, Any],
    records_by_id: Dict[Any, Dict[str, Any]],
) -> str:
    """Render the Markdown report."""
    lines: List[str] = []

    lines.append("# Expense Audit Report")
    lines.append("")
    lines.append(f"**Batch**: {batch_metadata.get('source_file', 'unknown')}")
    lines.append(f"**Policy version**: {policy.get('version', 'unknown')}")
    lines.append(f"**Audited**: {batch_metadata.get('audited_at', 'unknown')}")
    lines.append(f"**Records**: {summary['records']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Verdict | Count |")
    lines.append("|---------|-------|")
    lines.append(f"| Pass | {summary['pass']} |")
    lines.append(f"| Violation | {summary['violation']} |")
    lines.append(f"| Needs review | {summary['needs_review']} |")
    lines.append("")
    lines.append("| Severity | Findings |")
    lines.append("|----------|----------|")
    lines.append(f"| High | {summary['high']} |")
    lines.append(f"| Medium | {summary['medium']} |")
    lines.append(f"| Low | {summary['low']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Violations")
    lines.append("")
    if violations:
        for evaluation in violations:
            record = records_by_id.get(evaluation.get("record_id"), {})
            heading = " — ".join(
                part
                for part in (
                    SEVERITY_LABEL.get(evaluation.get("severity"), "Medium"),
                    str(evaluation.get("record_id")),
                    record.get("employee_name"),
                    _summarize_record(record),
                )
                if part
            )
            lines.append(f"### {heading}")
            lines.append("")
            lines.append(
                f"- **Rule**: `{evaluation.get('rule_id')}` — "
                f"{evaluation.get('rule_description')}"
            )
            lines.append(f"- **Actual**: {_format_actual(evaluation.get('actual'))}")
            lines.append(f"- **Limit**: {_format_value(evaluation.get('limit'))}")
            lines.append(f"- **Overage**: {_format_value(evaluation.get('overage'))}")
            lines.append("")
    else:
        lines.append("No violations found.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Needs Review")
    lines.append("")
    if needs_review:
        for evaluation in needs_review:
            record = records_by_id.get(evaluation.get("record_id"), {})
            heading = " — ".join(
                part
                for part in (
                    str(evaluation.get("record_id")),
                    record.get("employee_name"),
                )
                if part
            )
            lines.append(f"### {heading}")
            lines.append("")
            lines.append(
                f"- **Rule**: `{evaluation.get('rule_id')}` — "
                f"{evaluation.get('rule_description')}"
            )
            lines.append(f"- **Reason**: {evaluation.get('message')}")
            lines.append("")
    else:
        lines.append("Nothing flagged for review.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Suspected Duplicates")
    lines.append("")
    if duplicate_groups:
        for group in duplicate_groups:
            lines.append(
                f"### {group.get('merchant')} — {_format_value(group.get('amount'))}"
            )
            lines.append("")
            lines.append("| Record | Employee | Date | Amount |")
            lines.append("|--------|----------|------|--------|")
            for member in group.get("records", []):
                lines.append(
                    f"| {member.get('record_id')} | {member.get('employee_name')} "
                    f"| {member.get('expense_date')} "
                    f"| {_format_value(member.get('amount'))} |"
                )
            lines.append("")
            basis = group.get("matching_basis", {})
            lines.append(
                f"**Matching basis**: amount within {basis.get('amount_tolerance_pct')}% "
                f"and date within {basis.get('date_window_days')} day(s)"
            )
            lines.append("")
    else:
        lines.append("No suspected duplicates.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Policy Reference")
    lines.append("")
    lines.append("| Rule | Description | Value |")
    lines.append("|------|-------------|-------|")
    overridden = _overridden_fields(policy)
    for rule in policy.get("rules", []):
        marker = " (overridden)" if overridden.get(rule.get("id")) else ""
        lines.append(
            f"| `{rule.get('id')}` | {rule.get('description')} "
            f"| {_rule_value(rule)}{marker} |"
        )
    lines.append("")

    if parse_failures:
        lines.append("---")
        lines.append("")
        lines.append("## Parse Failures")
        lines.append("")
        lines.append("| Row | Reason |")
        lines.append("|-----|--------|")
        for failure in parse_failures:
            lines.append(f"| {failure.get('row')} | {failure.get('reason')} |")
        lines.append("")

    return "\n".join(lines)


def _overridden_fields(policy: Dict[str, Any]) -> Dict[str, set]:
    """Map rule id to the set of fields changed by an override."""
    changed: Dict[str, set] = {}
    for entry in policy.get("overrides_applied", []) or []:
        changed.setdefault(entry.get("rule_id"), set()).add(entry.get("field"))
    return changed


def _rule_value(rule: Dict[str, Any]) -> str:
    """Render a rule's active value for the policy reference table."""
    rule_type = rule.get("type")

    if rule_type == "per_unit_limit":
        label = UNIT_LABELS.get(rule.get("unit_field"), rule.get("unit_field"))
        return f"{_format_value(rule.get('limit'))} per {label}"
    if rule_type in ("receipt_required", "approval_required"):
        return _format_value(rule.get("threshold"))
    if rule_type == "category_blocklist":
        return ", ".join(rule.get("blocked", []))
    if rule_type == "date_window":
        return f"{rule.get('max_days')} days"
    if rule_type == "review_flag":
        return "flagged for review"

    return "n/a"


def _summarize_record(record: Dict[str, Any]) -> str:
    """Render a compact record description for a finding heading."""
    category = record.get("category")
    amount = record.get("amount")
    parts = [part for part in (category, _format_value(amount)) if part]
    return " ".join(parts)


def _format_actual(actual: Optional[Dict[str, Any]]) -> str:
    """Render the actual-values object as a readable list."""
    if not actual:
        return "n/a"
    return ", ".join(f"{key} {_format_value(actual[key])}" for key in sorted(actual))


def _format_value(value: Any) -> str:
    """Render a scalar for a report: numbers with two decimals, None as n/a."""
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return str(value)
    return str(value)


if __name__ == "__main__":
    payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(execute(payload), indent=2))
