#!/usr/bin/env python3
"""
parse_expenses: Read a CSV or JSON expense export and normalize records.

Resolves column names through an alias table, converts values to a fixed schema,
and collects unreadable rows instead of aborting the batch. Every record carries
all schema fields; fields that are absent or unparsable become null.
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


ALL_FIELDS = (
    "record_id",
    "employee_id",
    "employee_name",
    "expense_date",
    "submitted_date",
    "category",
    "merchant",
    "amount",
    "currency",
    "attendees",
    "nights",
    "receipt_attached",
    "approval_id",
    "is_travel",
    "notes",
)

# Built-in alias table, lowercased. Order within each list is priority order.
FIELD_ALIASES = {
    "record_id": ["record_id", "id", "expense_id", "expense id", "report_id", "entry_id"],
    "employee_id": ["employee_id", "employee id", "emp_id", "user_id", "submitter_id"],
    "employee_name": ["employee_name", "employee", "name", "submitter", "full_name"],
    "expense_date": ["expense_date", "date", "transaction_date", "purchase_date", "incurred_date"],
    "submitted_date": ["submitted_date", "submitted", "submit_date", "created_date", "report_date"],
    "category": ["category", "type", "expense_type", "expense category", "gl_category"],
    "merchant": ["merchant", "vendor", "payee", "supplier", "merchant_name"],
    "amount": ["amount", "total", "total_amount", "value", "cost", "gross_amount"],
    "currency": ["currency", "ccy", "currency_code", "curr"],
    "attendees": ["attendees", "attendee_count", "headcount", "guests", "party_size"],
    "nights": ["nights", "nights_stayed", "room_nights"],
    "receipt_attached": ["receipt_attached", "receipt", "has_receipt", "receipt_status"],
    "approval_id": ["approval_id", "approver", "approval_reference", "manager_approval"],
    "is_travel": ["is_travel", "travel", "business_travel", "travel_flag"],
    "notes": ["notes", "note", "description", "memo", "comment"],
}

# Canonical categories, plus the synonyms and plural forms that collapse into them.
CATEGORY_ALIASES = {
    "meal": "meals",
    "meals": "meals",
    "food": "meals",
    "dining": "meals",
    "restaurant": "meals",
    "restaurants": "meals",
    "hotel": "lodging",
    "hotels": "lodging",
    "lodging": "lodging",
    "accommodation": "lodging",
    "flight": "flights",
    "flights": "flights",
    "airfare": "flights",
    "air": "flights",
    "taxi": "ground_transport",
    "uber": "ground_transport",
    "lyft": "ground_transport",
    "car_rental": "ground_transport",
    "parking": "ground_transport",
    "mileage": "ground_transport",
    "train": "ground_transport",
    "alcohol": "alcohol",
    "bar": "alcohol",
    "drinks": "alcohol",
    "gambling": "gambling",
    "casino": "gambling",
    "personal": "personal_items",
    "personal_item": "personal_items",
    "personal_items": "personal_items",
    "fine": "fines",
    "fines": "fines",
    "penalty": "fines",
}

DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d")
TRUE_TOKENS = {"true", "yes", "y", "1", "attached"}
FALSE_TOKENS = {"false", "no", "n", "0", "missing"}
JSON_RECORD_KEYS = ("records", "expenses", "items")


class UnparseableRow(Exception):
    """Raised when a row cannot be converted into a record at all."""


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse an expense export into normalized records.

    Args:
        params: {
            "file_path": str,            # Path to a .csv or .json export
            "column_map": dict | None,   # Explicit {field: source_column} overrides
            "defaults": dict | None      # Values to use for fields absent from the file
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "records": [ <normalized record> ],
                "record_count": int,
                "source_file": str,
                "resolved_columns": {field: source_column_or_None},
                "parse_failures": [{"row": int, "reason": str, "raw": dict}]
            },
            "error": str | None
        }
    """
    file_path = params.get("file_path")
    if not file_path:
        return {"status": "error", "error": "file_path parameter is required"}

    path = Path(file_path)
    if not path.exists():
        return {"status": "error", "error": f"File does not exist: {file_path}"}

    suffix = path.suffix.lower()
    if suffix not in (".csv", ".json"):
        shown = suffix or path.name
        return {
            "status": "error",
            "error": (
                f"Unsupported file format '{shown}'. "
                "Supported formats: .csv, .json"
            ),
        }

    try:
        rows = _read_csv(path) if suffix == ".csv" else _read_json(path)
    except Exception as exc:  # noqa: BLE001 - any read failure is reported, never raised
        return {"status": "error", "error": f"Failed to read {file_path}: {exc}"}

    if not rows:
        return {"status": "error", "error": f"No expense records found in {file_path}"}

    defaults = dict(params.get("defaults") or {})
    resolved_columns = _resolve_columns(rows, params.get("column_map") or {})

    records: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        try:
            records.append(_normalize_row(row, resolved_columns, defaults, index))
        except Exception as exc:  # noqa: BLE001 - one bad row never aborts the batch
            failures.append({"row": index, "reason": str(exc), "raw": dict(row)})

    if not records:
        return {
            "status": "error",
            "error": (
                f"No readable expense records in {file_path}; "
                f"all {len(rows)} row(s) failed to parse"
            ),
        }

    return {
        "status": "success",
        "data": {
            "records": records,
            "record_count": len(records),
            "source_file": str(path),
            "resolved_columns": resolved_columns,
            "parse_failures": failures,
        },
    }


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    """Read a CSV file into a list of row dictionaries."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_json(path: Path) -> List[Dict[str, Any]]:
    """Read a JSON file into a list of row dictionaries."""
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = None
        for key in JSON_RECORD_KEYS:
            if isinstance(data.get(key), list):
                rows = data[key]
                break
        if rows is None:
            raise ValueError(
                "JSON object must contain a records array under one of: "
                + ", ".join(JSON_RECORD_KEYS)
            )
    else:
        raise ValueError(
            "JSON root must be an array of records, or an object containing one"
        )

    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Every JSON record must be an object")

    return [dict(row) for row in rows]


def _resolve_columns(rows: List[Dict[str, Any]], column_map: Dict[str, str]) -> Dict[str, Optional[str]]:
    """Map each schema field to a source column name, or None when absent."""
    available: List[str] = []
    for row in rows:
        for key in row.keys():
            if isinstance(key, str) and key not in available:
                available.append(key)

    resolved: Dict[str, Optional[str]] = {}
    for field in ALL_FIELDS:
        if field in column_map:
            resolved[field] = column_map[field]
            continue

        match = None
        for alias in FIELD_ALIASES[field]:
            for candidate in available:
                # Normalize spaces to underscores for comparison
                normalized = candidate.strip().lower().replace(' ', '_')
                if normalized == alias:
                    match = candidate
                    break
            if match is not None:
                break
        resolved[field] = match

    return resolved


def _normalize_row(
    row: Dict[str, Any],
    resolved_columns: Dict[str, Optional[str]],
    defaults: Dict[str, Any],
    index: int,
) -> Dict[str, Any]:
    """Convert one raw row into a normalized record."""
    raw: Dict[str, Any] = {}
    for field in ALL_FIELDS:
        column = resolved_columns.get(field)
        value = row.get(column) if column else None
        if _is_blank(value) and field in defaults:
            value = defaults[field]
        raw[field] = value

    amount = _parse_amount(raw["amount"])
    if amount is None:
        raise UnparseableRow(
            f"amount is missing or not a number: {raw['amount']!r}"
        )

    return {
        "record_id": _clean_str(raw["record_id"]) or f"ROW-{index}",
        "employee_id": _clean_str(raw["employee_id"]),
        "employee_name": _clean_str(raw["employee_name"]),
        "expense_date": _parse_date(raw["expense_date"]),
        "submitted_date": _parse_date(raw["submitted_date"]),
        "category": _normalize_category(raw["category"]),
        "merchant": _clean_str(raw["merchant"]),
        "amount": amount,
        "currency": (_clean_str(raw["currency"]) or "USD").upper(),
        "attendees": _parse_int(raw["attendees"]),
        "nights": _parse_int(raw["nights"]),
        "receipt_attached": _parse_bool(raw["receipt_attached"]),
        "approval_id": _clean_str(raw["approval_id"]),
        "is_travel": _parse_bool(raw["is_travel"]) is True,
        "notes": _clean_str(raw["notes"]),
    }


def _is_blank(value: Any) -> bool:
    """True for None and for whitespace-only strings."""
    return value is None or (isinstance(value, str) and not value.strip())


def _clean_str(value: Any) -> Optional[str]:
    """Trim to a string, or None when blank."""
    if _is_blank(value):
        return None
    return str(value).strip()


def _parse_amount(value: Any) -> Optional[float]:
    """Parse an amount, stripping currency symbols and thousands separators."""
    if _is_blank(value):
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = re.sub(r"[^\d.\-]", "", str(value).strip())
    if not text or text in ("-", ".", "-."):
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_int(value: Any) -> Optional[int]:
    """Parse an integer, or None when blank or unparsable."""
    if _is_blank(value):
        return None
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None


def _parse_date(value: Any) -> Optional[str]:
    """Normalize a date to ISO 8601, or None when blank or unparsable."""
    if _is_blank(value):
        return None
    text = str(value).strip()
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format).date().isoformat()
        except ValueError:
            continue
    return None


def _parse_bool(value: Any) -> Optional[bool]:
    """Parse a boolean token, or None when blank or unrecognized."""
    if _is_blank(value):
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in TRUE_TOKENS:
        return True
    if text in FALSE_TOKENS:
        return False
    return None


def _normalize_category(value: Any) -> Optional[str]:
    """Collapse a category to its canonical form."""
    if _is_blank(value):
        return None
    slug = re.sub(r"[\s_]+", "_", str(value).strip().lower())
    return CATEGORY_ALIASES.get(slug, slug)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(execute({"file_path": sys.argv[1]}), indent=2))
    else:
        print("Usage: python parse_expenses.py <file_path>")