#!/usr/bin/env python3
"""
detect_duplicates: Find suspected duplicate expense records within a batch.

Groups records that share a submitter and merchant, with amounts inside a
percentage tolerance and dates inside a day window. Grouping is transitive via
union-find, so a chain of near-matches forms a single group. The output is
advisory: it reports suspicion, never a determination that a duplicate exists.
"""

import json
import sys
from datetime import date
from typing import Any, Dict, List, Optional


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find suspected duplicate records within a batch.

    Args:
        params: {
            "records": [ <normalized record from parse_expenses> ],
            "policy": { <effective policy from get_policy> }
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "groups": [
                    {
                        "group_id": str,
                        "rule_id": str,
                        "merchant": str,
                        "amount": float,
                        "records": [
                            {
                                "record_id": str,
                                "employee_id": str | None,
                                "employee_name": str | None,
                                "expense_date": str | None,
                                "amount": float
                            }
                        ],
                        "matching_basis": {
                            "amount_tolerance_pct": float,
                            "date_window_days": int
                        },
                        "severity": str
                    }
                ],
                "duplicate_record_count": int
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
    if not isinstance(policy, dict):
        return {
            "status": "error",
            "error": "policy must be the object returned by get_policy",
        }

    config = policy.get("duplicate_detection")
    if not isinstance(config, dict):
        return {
            "status": "error",
            "error": "policy.duplicate_detection is missing; pass the object from get_policy",
        }

    tolerance_pct = config.get("amount_tolerance_pct", 1.0)
    window_days = config.get("date_window_days", 3)
    rule_id = config.get("id", "duplicate_suspected")
    severity = config.get("severity", "high")

    candidates = _build_candidates(records)

    parent = {candidate["index"]: candidate["index"] for candidate in candidates}
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            left, right = candidates[i], candidates[j]
            if not _matches(left, right, tolerance_pct, window_days):
                continue
            _union(parent, left["index"], right["index"])

    buckets: Dict[int, List[Dict[str, Any]]] = {}
    for candidate in candidates:
        root = _find(parent, candidate["index"])
        buckets.setdefault(root, []).append(candidate)

    groups: List[Dict[str, Any]] = []
    for root in sorted(buckets):
        members = buckets[root]
        if len(members) < 2:
            continue

        members.sort(key=lambda candidate: candidate["index"])
        anchor = members[0]["record"]
        groups.append(
            {
                "group_id": f"DUP-{len(groups) + 1:03d}",
                "rule_id": rule_id,
                "merchant": anchor.get("merchant"),
                "amount": anchor["amount"],
                "records": [
                    {
                        "record_id": member["record"].get("record_id"),
                        "employee_id": member["record"].get("employee_id"),
                        "employee_name": member["record"].get("employee_name"),
                        "expense_date": member["record"].get("expense_date"),
                        "amount": member["record"]["amount"],
                    }
                    for member in members
                ],
                "matching_basis": {
                    "amount_tolerance_pct": tolerance_pct,
                    "date_window_days": window_days,
                },
                "severity": severity,
            }
        )

    return {
        "status": "success",
        "data": {
            "groups": groups,
            "duplicate_record_count": sum(len(g["records"]) for g in groups),
        },
    }


def _build_candidates(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep only records that carry the fields duplicate matching needs."""
    candidates: List[Dict[str, Any]] = []

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue

        merchant = record.get("merchant")
        expense_date = record.get("expense_date")
        if merchant is None or expense_date is None:
            continue

        identity = record.get("employee_id") or _normalize_text(
            record.get("employee_name")
        )
        if identity is None:
            continue

        try:
            parsed_date = date.fromisoformat(expense_date)
        except (ValueError, TypeError):
            continue

        candidates.append(
            {
                "index": index,
                "record": record,
                "identity": identity,
                "merchant": _normalize_text(merchant),
                "amount": record["amount"],
                "date": parsed_date,
            }
        )

    return candidates


def _normalize_text(value: Any) -> Optional[str]:
    """Lowercase and collapse whitespace, or None when blank."""
    if value is None:
        return None
    normalized = " ".join(str(value).strip().lower().split())
    return normalized or None


def _within_tolerance(left: float, right: float, tolerance_pct: float) -> bool:
    """True when the two amounts differ by no more than the tolerance."""
    if left == right:
        return True
    base = max(abs(left), abs(right))
    if base == 0:
        return True
    return abs(left - right) / base * 100.0 <= tolerance_pct


def _matches(
    left: Dict[str, Any],
    right: Dict[str, Any],
    tolerance_pct: float,
    window_days: int,
) -> bool:
    """True when two candidates satisfy every duplicate criterion."""
    if left["identity"] != right["identity"]:
        return False
    if left["merchant"] != right["merchant"]:
        return False
    if not _within_tolerance(left["amount"], right["amount"], tolerance_pct):
        return False
    return abs((left["date"] - right["date"]).days) <= window_days


def _find(parent: Dict[int, int], index: int) -> int:
    """Union-find lookup with path compression."""
    while parent[index] != index:
        parent[index] = parent[parent[index]]
        index = parent[index]
    return index


def _union(parent: Dict[int, int], left: int, right: int) -> None:
    """Union-find merge."""
    left_root = _find(parent, left)
    right_root = _find(parent, right)
    if left_root != right_root:
        parent[right_root] = left_root


if __name__ == "__main__":
    payload = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(execute(payload), indent=2))