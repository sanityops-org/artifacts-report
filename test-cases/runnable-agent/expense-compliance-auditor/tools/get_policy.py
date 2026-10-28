#!/usr/bin/env python3
"""
get_policy: Return the effective expense policy (built-in defaults plus overrides).

The default policy is a module-level constant, not a configuration file: this
module is the single source of truth for every threshold the auditor applies.
Overrides merge per rule and per field, and each change is reported back so a
report can show which values were non-default.
"""

import copy
import json
import sys
from typing import Any, Dict, List, Optional


DEFAULT_POLICY = {
    "version": "2026.1",
    "currency": "USD",
    "rules": [
        {
            "id": "meal_limit_per_person",
            "description": "Meals must not exceed $75 per person",
            "type": "per_unit_limit",
            "category": "meals",
            "limit": 75.00,
            "unit_field": "attendees",
            "severity": "high",
        },
        {
            "id": "hotel_limit_per_night",
            "description": "Lodging must not exceed $250 per night",
            "type": "per_unit_limit",
            "category": "lodging",
            "limit": 250.00,
            "unit_field": "nights",
            "severity": "high",
        },
        {
            "id": "receipt_required_above",
            "description": "Receipts are required for any expense of $25 or more",
            "type": "receipt_required",
            "threshold": 25.00,
            "severity": "medium",
        },
        {
            "id": "prohibited_category",
            "description": "Certain categories are never reimbursable",
            "type": "category_blocklist",
            "blocked": ["alcohol", "gambling", "personal_items", "fines"],
            "severity": "high",
        },
        {
            "id": "submission_window",
            "description": "Expenses must be submitted within 60 days of the expense date",
            "type": "date_window",
            "max_days": 60,
            "severity": "medium",
        },
        {
            "id": "approval_required_above",
            "description": "Expenses of $500 or more require a manager approval ID",
            "type": "approval_required",
            "threshold": 500.00,
            "severity": "medium",
        },
        {
            "id": "weekend_non_travel_meal",
            "description": "Weekend meals not marked as travel require manual review",
            "type": "review_flag",
            "category": "meals",
            "condition": "weekend_and_not_travel",
            "severity": "low",
        },
    ],
    "duplicate_detection": {
        "id": "duplicate_suspected",
        "description": "Same merchant and amount submitted more than once",
        "amount_tolerance_pct": 1.0,
        "date_window_days": 3,
        "severity": "high",
    },
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return the effective expense policy.

    Args:
        params: {
            "overrides": dict | None,   # {rule_id: {field: value, ...}, ...}
            "rule_ids": list | None     # Return only these rules (duplicate_detection
                                        # is independent and always returned)
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "version": str,
                "currency": str,
                "rules": [rule],
                "duplicate_detection": {...},
                "overrides_applied": [
                    {"rule_id": str, "field": str, "default": Any, "effective": Any}
                ]
            },
            "error": str | None
        }
    """
    overrides = params.get("overrides")
    if overrides is None:
        overrides = {}
    if not isinstance(overrides, dict):
        return {
            "status": "error",
            "error": "overrides must be an object keyed by rule_id",
        }

    policy = copy.deepcopy(DEFAULT_POLICY)
    rules_by_id = {rule["id"]: rule for rule in policy["rules"]}
    rules_by_id[policy["duplicate_detection"]["id"]] = policy["duplicate_detection"]
    valid_ids = ", ".join(sorted(rules_by_id))

    unknown = sorted(rule_id for rule_id in overrides if rule_id not in rules_by_id)
    if unknown:
        return {
            "status": "error",
            "error": (
                f"Unknown rule id(s): {', '.join(unknown)}. "
                f"Valid rule ids: {valid_ids}"
            ),
        }

    applied: List[Dict[str, Any]] = []
    for rule_id, changes in overrides.items():
        if not isinstance(changes, dict):
            return {
                "status": "error",
                "error": (
                    f"Override for '{rule_id}' must be an object of "
                    "field: value pairs"
                ),
            }

        rule = rules_by_id[rule_id]
        for field, value in changes.items():
            if field not in rule:
                available = ", ".join(sorted(rule))
                return {
                    "status": "error",
                    "error": (
                        f"Rule '{rule_id}' has no field '{field}'. "
                        f"Available fields: {available}"
                    ),
                }
            applied.append(
                {
                    "rule_id": rule_id,
                    "field": field,
                    "default": rule[field],
                    "effective": value,
                }
            )
            rule[field] = value

    rule_ids = params.get("rule_ids")
    if rule_ids is not None:
        if not isinstance(rule_ids, list):
            return {"status": "error", "error": "rule_ids must be a list of rule ids"}

        unknown_filter = [
            rule_id for rule_id in rule_ids if rule_id not in rules_by_id
        ]
        if unknown_filter:
            return {
                "status": "error",
                "error": (
                    f"Unknown rule id(s) in rule_ids: {', '.join(unknown_filter)}. "
                    f"Valid rule ids: {valid_ids}"
                ),
            }

        allowed = set(rule_ids)
        policy["rules"] = [r for r in policy["rules"] if r["id"] in allowed]

    return {
        "status": "success",
        "data": {
            "version": policy["version"],
            "currency": policy["currency"],
            "rules": policy["rules"],
            "duplicate_detection": policy["duplicate_detection"],
            "overrides_applied": applied,
        },
    }


if __name__ == "__main__":
    payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(execute(payload), indent=2))