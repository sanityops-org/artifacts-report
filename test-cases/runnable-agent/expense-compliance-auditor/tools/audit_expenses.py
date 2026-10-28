#!/usr/bin/env python3
"""
audit_expenses: Evaluate expense records against policy rules.

Produces one evaluation per (record, applicable rule) pair, including passes, so
a report can state which rules ran rather than only which failed. Pure function:
no I/O, no clock reads, no randomness.
"""

import json
import sys
from datetime import date
from typing import Any, Dict, List, Optional


VERDICT_PASS = "pass"
VERDICT_VIOLATION = "violation"
VERDICT_REVIEW = "needs_review"

# Amount-threshold rule types are affected by a currency mismatch; the others are not.
AMOUNT_THRESHOLD_TYPES = ("per_unit_limit", "receipt_required", "approval_required")

UNIT_LABELS = {"attendees": "person", "nights": "night"}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate expense records against policy rules.

    Args:
        params: {
            "records": [ <normalized record from parse_expenses> ],
            "policy": { <effective policy from get_policy> }
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "evaluations": [
                    {
                        "record_id": str,
                        "rule_id": str,
                        "rule_description": str,
                        "verdict": "pass" | "violation" | "needs_review",
                        "severity": str,
                        "actual": dict,
                        "limit": Any | None,
                        "overage": float | None,
                        "message": str
                    }
                ],
                "record_summary": [
                    {
                        "record_id": str,
                        "overall": str,
                        "violation_count": int,
                        "review_count": int
                    }
                ],
                "totals": {
                    "records": int, "pass": int,
                    "violation": int, "needs_review": int
                }
            },
            "error": str | None
        }
    """
    records = params.get("records")
    policy = params.get("policy")

    if not isinstance(records, list):
        return {
            "status": "error",
            "error": "records must be a list of normalized records from parse_expenses",
        }
    if not isinstance(policy, dict) or not isinstance(policy.get("rules"), list):
        return {
            "status": "error",
            "error": "policy must be the object returned by get_policy, with a 'rules' list",
        }

    policy_currency = policy.get("currency", "USD")
    duplicate_id = (policy.get("duplicate_detection") or {}).get("id")
    rules = [rule for rule in policy["rules"] if rule.get("id") != duplicate_id]

    evaluations: List[Dict[str, Any]] = []
    record_summary: List[Dict[str, Any]] = []
    totals = {"records": len(records), "pass": 0, "violation": 0, "needs_review": 0}

    for record in records:
        if not isinstance(record, dict):
            return {
                "status": "error",
                "error": "every entry in records must be a normalized record object",
            }

        record_evaluations: List[Dict[str, Any]] = []
        for rule in rules:
            if not _applies(rule, record):
                continue
            record_evaluations.append(_evaluate(rule, record, policy_currency))

        evaluations.extend(record_evaluations)

        overall = _rollup(record_evaluations)
        record_summary.append(
            {
                "record_id": record.get("record_id"),
                "overall": overall,
                "violation_count": sum(
                    1 for e in record_evaluations if e["verdict"] == VERDICT_VIOLATION
                ),
                "review_count": sum(
                    1 for e in record_evaluations if e["verdict"] == VERDICT_REVIEW
                ),
            }
        )
        totals[overall] += 1

    return {
        "status": "success",
        "data": {
            "evaluations": evaluations,
            "record_summary": record_summary,
            "totals": totals,
        },
    }


def _applies(rule: Dict[str, Any], record: Dict[str, Any]) -> bool:
    """A rule naming a category applies only to records in that category."""
    category = rule.get("category")
    if category is None:
        return True
    return record.get("category") == category


def _rollup(evaluations: List[Dict[str, Any]]) -> str:
    """Collapse a record's evaluations: violation dominates, then needs_review."""
    if any(e["verdict"] == VERDICT_VIOLATION for e in evaluations):
        return VERDICT_VIOLATION
    if any(e["verdict"] == VERDICT_REVIEW for e in evaluations):
        return VERDICT_REVIEW
    return VERDICT_PASS


def _evaluation(
    rule: Dict[str, Any],
    record: Dict[str, Any],
    verdict: str,
    actual: Dict[str, Any],
    limit: Any,
    overage: Optional[float],
    message: str,
) -> Dict[str, Any]:
    """Build the traceable evaluation object."""
    return {
        "record_id": record.get("record_id"),
        "rule_id": rule.get("id"),
        "rule_description": rule.get("description"),
        "verdict": verdict,
        "severity": rule.get("severity", "medium"),
        "actual": actual,
        "limit": limit,
        "overage": overage,
        "message": message,
    }


def _evaluate(
    rule: Dict[str, Any], record: Dict[str, Any], policy_currency: str
) -> Dict[str, Any]:
    """Dispatch a rule to its evaluator."""
    rule_type = rule.get("type")

    if rule_type in AMOUNT_THRESHOLD_TYPES and record.get("currency") != policy_currency:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={
                "amount": record.get("amount"),
                "currency": record.get("currency"),
            },
            limit=rule.get("limit", rule.get("threshold")),
            overage=None,
            message=(
                f"Record is in {record.get('currency')}, policy is in {policy_currency}; "
                "no exchange rate is applied"
            ),
        )

    if rule_type == "per_unit_limit":
        return _eval_per_unit_limit(rule, record)
    if rule_type == "receipt_required":
        return _eval_receipt_required(rule, record)
    if rule_type == "category_blocklist":
        return _eval_category_blocklist(rule, record)
    if rule_type == "date_window":
        return _eval_date_window(rule, record)
    if rule_type == "approval_required":
        return _eval_approval_required(rule, record)
    if rule_type == "review_flag":
        return _eval_review_flag(rule, record)

    return _evaluation(
        rule,
        record,
        VERDICT_REVIEW,
        actual={},
        limit=None,
        overage=None,
        message=f"Unknown rule type '{rule_type}'",
    )


def _eval_per_unit_limit(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Compare a per-unit cost against the limit."""
    unit_field = rule["unit_field"]
    limit = rule["limit"]
    units = record.get(unit_field)
    unit_label = UNIT_LABELS.get(unit_field, unit_field)

    if units is None:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"amount": record.get("amount")},
            limit=limit,
            overage=None,
            message=f"Cannot evaluate: '{unit_field}' is missing from this record",
        )

    if units <= 0:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"amount": record.get("amount"), unit_field: units},
            limit=limit,
            overage=None,
            message=f"Cannot evaluate: '{unit_field}' must be greater than zero",
        )

    per_unit = round(record["amount"] / units, 2)
    actual = {"amount": record["amount"], unit_field: units, f"per_{unit_label}": per_unit}

    if per_unit > limit:
        overage = round(per_unit - limit, 2)
        return _evaluation(
            rule,
            record,
            VERDICT_VIOLATION,
            actual,
            limit,
            overage,
            message=(
                f"Per-{unit_label} cost of ${per_unit:.2f} exceeds the "
                f"${limit:.2f} limit by ${overage:.2f}"
            ),
        )

    return _evaluation(
        rule,
        record,
        VERDICT_PASS,
        actual,
        limit,
        None,
        message=f"Per-{unit_label} cost of ${per_unit:.2f} is within the ${limit:.2f} limit",
    )


def _eval_receipt_required(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Require a receipt at or above the threshold."""
    threshold = rule["threshold"]
    amount = record["amount"]
    receipt_attached = record.get("receipt_attached")

    if amount < threshold:
        return _evaluation(
            rule,
            record,
            VERDICT_PASS,
            actual={"amount": amount, "receipt_attached": receipt_attached},
            limit=threshold,
            overage=None,
            message=f"Receipt not required below ${threshold:.2f}",
        )

    if receipt_attached is None:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"amount": amount},
            limit=threshold,
            overage=None,
            message="Cannot evaluate: 'receipt_attached' is missing from this record",
        )

    if receipt_attached:
        return _evaluation(
            rule,
            record,
            VERDICT_PASS,
            actual={"amount": amount, "receipt_attached": True},
            limit=threshold,
            overage=None,
            message=f"Receipt attached for an expense of ${amount:.2f}",
        )

    return _evaluation(
        rule,
        record,
        VERDICT_VIOLATION,
        actual={"amount": amount, "receipt_attached": False},
        limit=threshold,
        overage=None,
        message=(
            f"Receipt missing for an expense of ${amount:.2f} "
            f"(receipts required at ${threshold:.2f} or more)"
        ),
    )


def _eval_category_blocklist(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Check the record's category against the blocklist."""
    blocked = rule.get("blocked", [])
    category = record.get("category")
    actual = {"category": category}

    if category is None:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual,
            limit=None,
            overage=None,
            message="Cannot evaluate: 'category' is missing from this record",
        )

    if category in blocked:
        return _evaluation(
            rule,
            record,
            VERDICT_VIOLATION,
            actual,
            limit=None,
            overage=None,
            message=f"Category '{category}' is not reimbursable",
        )

    return _evaluation(
        rule,
        record,
        VERDICT_PASS,
        actual,
        limit=None,
        overage=None,
        message=f"Category '{category}' is reimbursable",
    )


def _eval_date_window(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Check the elapsed days between the expense date and the submission date."""
    max_days = rule["max_days"]
    expense_date = record.get("expense_date")
    submitted_date = record.get("submitted_date")

    if expense_date is None or submitted_date is None:
        missing = "expense_date" if expense_date is None else "submitted_date"
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"expense_date": expense_date, "submitted_date": submitted_date},
            limit=max_days,
            overage=None,
            message=f"Cannot evaluate: '{missing}' is missing from this record",
        )

    try:
        elapsed = (
            date.fromisoformat(submitted_date) - date.fromisoformat(expense_date)
        ).days
    except (ValueError, TypeError):
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"expense_date": expense_date, "submitted_date": submitted_date},
            limit=max_days,
            overage=None,
            message=(
                "Cannot evaluate: dates are not valid ISO 8601 "
                f"({expense_date!r}, {submitted_date!r})"
            ),
        )

    actual = {"days_elapsed": elapsed}

    if elapsed > max_days:
        return _evaluation(
            rule,
            record,
            VERDICT_VIOLATION,
            actual,
            max_days,
            elapsed - max_days,
            message=(
                f"Submitted {elapsed} days after the expense date; "
                f"the limit is {max_days} days"
            ),
        )

    return _evaluation(
        rule,
        record,
        VERDICT_PASS,
        actual,
        max_days,
        None,
        message=(
            f"Submitted {elapsed} days after the expense date, "
            f"within the {max_days}-day limit"
        ),
    )


def _eval_approval_required(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Require an approval ID at or above the threshold."""
    threshold = rule["threshold"]
    amount = record["amount"]
    approval_id = record.get("approval_id")

    if amount < threshold:
        return _evaluation(
            rule,
            record,
            VERDICT_PASS,
            actual={"amount": amount, "approval_id": approval_id},
            limit=threshold,
            overage=None,
            message=f"Approval not required below ${threshold:.2f}",
        )

    actual = {"amount": amount, "approval_id": approval_id}

    if approval_id:
        return _evaluation(
            rule,
            record,
            VERDICT_PASS,
            actual,
            threshold,
            None,
            message=f"Approval '{approval_id}' present for an expense of ${amount:.2f}",
        )

    return _evaluation(
        rule,
        record,
        VERDICT_VIOLATION,
        actual,
        threshold,
        None,
        message=(
            f"No approval ID for an expense of ${amount:.2f} "
            f"(approval required at ${threshold:.2f} or more)"
        ),
    )


def _eval_review_flag(rule: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch a named review condition."""
    condition = rule.get("condition")

    if condition == "weekend_and_not_travel":
        return _eval_weekend_and_not_travel(rule, record)

    return _evaluation(
        rule,
        record,
        VERDICT_REVIEW,
        actual={},
        limit=None,
        overage=None,
        message=f"Unknown review condition '{condition}'",
    )


def _eval_weekend_and_not_travel(
    rule: Dict[str, Any], record: Dict[str, Any]
) -> Dict[str, Any]:
    """Flag weekend expenses that are not marked as travel."""
    expense_date = record.get("expense_date")

    if expense_date is None:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"expense_date": None},
            limit=None,
            overage=None,
            message="Cannot evaluate: 'expense_date' is missing from this record",
        )

    try:
        parsed = date.fromisoformat(expense_date)
    except (ValueError, TypeError):
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual={"expense_date": expense_date},
            limit=None,
            overage=None,
            message=(
                "Cannot evaluate: 'expense_date' is not a valid ISO 8601 date "
                f"({expense_date!r})"
            ),
        )

    is_travel = bool(record.get("is_travel"))
    weekday = parsed.strftime("%A")
    actual = {"expense_date": expense_date, "weekday": weekday, "is_travel": is_travel}

    if parsed.weekday() >= 5 and not is_travel:
        return _evaluation(
            rule,
            record,
            VERDICT_REVIEW,
            actual,
            limit=None,
            overage=None,
            message=f"{weekday} meal not marked as travel; requires manual review",
        )

    return _evaluation(
        rule,
        record,
        VERDICT_PASS,
        actual,
        limit=None,
        overage=None,
        message=f"{weekday} meal does not require review",
    )


if __name__ == "__main__":
    payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(execute(payload), indent=2))