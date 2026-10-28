#!/usr/bin/env python3
"""Tests for the parse_expenses tool."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from parse_expenses import execute


class TestParseExpenses(unittest.TestCase):
    """Test cases for expense batch parsing and normalization."""

    def _write(self, tmpdir, name, content):
        path = Path(tmpdir) / name
        path.write_text(content, encoding="utf-8")
        return str(path)

    def test_alias_resolution(self):
        """Columns named with common export aliases resolve to canonical fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.csv",
                "Expense ID,Employee,Date,Vendor,Amount\n"
                "EXP-1,Jane Doe,2026-09-12,Nobu,120.00\n",
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            record = result["data"]["records"][0]
            self.assertEqual(record["record_id"], "EXP-1")
            self.assertEqual(record["employee_name"], "Jane Doe")
            self.assertEqual(record["expense_date"], "2026-09-12")
            self.assertEqual(record["merchant"], "Nobu")
            self.assertEqual(record["amount"], 120.00)
            resolved = result["data"]["resolved_columns"]
            self.assertEqual(resolved["record_id"], "Expense ID")
            self.assertEqual(resolved["merchant"], "Vendor")

    def test_aliases_are_case_insensitive(self):
        """Alias matching ignores case and surrounding whitespace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.csv",
                "  TOTAL , Date \n" "  99.50 ,2026-09-12 \n",
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            record = result["data"]["records"][0]
            self.assertEqual(record["amount"], 99.50)
            self.assertEqual(record["expense_date"], "2026-09-12")

    def test_explicit_column_map_overrides_aliases(self):
        """An explicit column_map wins over the built-in alias table."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.csv",
                "Amount,Date,Retailer Code\n" "10.00,2026-09-12,ACME-9\n",
            )

            result = execute(
                {"file_path": path, "column_map": {"merchant": "Retailer Code"}}
            )

            self.assertEqual(result["status"], "success")
            record = result["data"]["records"][0]
            self.assertEqual(record["merchant"], "ACME-9")
            self.assertEqual(record["amount"], 10.00)

    def test_amount_formats(self):
        """Currency symbols and thousands separators are stripped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.csv",
                'Amount,Date\n"$1,234.56",2026-09-12\n',
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            self.assertEqual(result["data"]["records"][0]["amount"], 1234.56)

    def test_date_formats(self):
        """All supported date formats normalize to ISO 8601."""
        cases = [
            ("2026-09-12", "2026-09-12"),
            ("09/12/2026", "2026-09-12"),
            ("12-Sep-2026", "2026-09-12"),
            ("2026/09/12", "2026-09-12"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = self._write(
                        tmpdir, "batch.csv", f"Amount,Date\n10.00,{raw}\n"
                    )

                    result = execute({"file_path": path})

                    self.assertEqual(result["status"], "success")
                    self.assertEqual(
                        result["data"]["records"][0]["expense_date"], expected
                    )

    def test_unparseable_date_becomes_null(self):
        """A date that cannot be parsed degrades to null; the row still parses."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount,Date\n10.00,not-a-date\n")

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            record = result["data"]["records"][0]
            self.assertIsNone(record["expense_date"])
            self.assertEqual(record["amount"], 10.00)

    def test_boolean_variants(self):
        """Boolean fields accept the documented token sets."""
        true_tokens = ["true", "yes", "y", "1", "attached"]
        false_tokens = ["false", "no", "n", "0", "missing"]

        for token in true_tokens:
            with self.subTest(token=token):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = self._write(
                        tmpdir,
                        "batch.csv",
                        f"Amount,Receipt Attached\n10.00,{token}\n",
                    )
                    record = execute({"file_path": path})["data"]["records"][0]
                    self.assertIs(record["receipt_attached"], True)

        for token in false_tokens:
            with self.subTest(token=token):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = self._write(
                        tmpdir,
                        "batch.csv",
                        f"Amount,Receipt Attached\n10.00,{token}\n",
                    )
                    record = execute({"file_path": path})["data"]["records"][0]
                    self.assertIs(record["receipt_attached"], False)

    def test_unrecognized_boolean_becomes_null(self):
        """An unrecognized boolean token becomes null, not False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir, "batch.csv", "Amount,Receipt Attached\n10.00,maybe\n"
            )

            record = execute({"file_path": path})["data"]["records"][0]

            self.assertIsNone(record["receipt_attached"])

    def test_category_normalization(self):
        """Category synonyms and plural forms collapse to canonical values."""
        cases = [
            ("Meal", "meals"),
            ("Meals", "meals"),
            ("meal", "meals"),
            ("MEALS", "meals"),
            ("Food", "meals"),
            ("Hotel", "lodging"),
            ("Accommodation", "lodging"),
            ("Expense Category", None),
        ]
        for raw, expected in cases[:7]:
            with self.subTest(raw=raw):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = self._write(
                        tmpdir, "batch.csv", f"Amount,Category\n10.00,{raw}\n"
                    )
                    record = execute({"file_path": path})["data"]["records"][0]
                    self.assertEqual(record["category"], expected)

    def test_unknown_category_is_lowercased_and_underscored(self):
        """A category absent from the alias table is normalized, not dropped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir, "batch.csv", "Amount,Category\n10.00,Team Offsite\n"
            )

            record = execute({"file_path": path})["data"]["records"][0]

            self.assertEqual(record["category"], "team_offsite")

    def test_synthesized_record_id(self):
        """A missing record_id is synthesized from the data row number."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir, "batch.csv", "Amount\n10.00\n20.00\n"
            )

            result = execute({"file_path": path})

            ids = [r["record_id"] for r in result["data"]["records"]]
            self.assertEqual(ids, ["ROW-1", "ROW-2"])

    def test_missing_amount_fails_only_that_row(self):
        """A row without a parsable amount is collected, and the batch continues."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.csv",
                "Record ID,Amount\n"
                "EXP-1,10.00\n"
                "EXP-2,\n"
                "EXP-3,not-a-number\n"
                "EXP-4,40.00\n",
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            self.assertEqual(result["data"]["record_count"], 2)
            self.assertEqual(
                [r["record_id"] for r in result["data"]["records"]], ["EXP-1", "EXP-4"]
            )
            failures = result["data"]["parse_failures"]
            self.assertEqual([f["row"] for f in failures], [2, 3])
            self.assertIn("amount", failures[0]["reason"])

    def test_all_rows_failing_is_an_error(self):
        """A batch where no row has a parsable amount is an error, not an empty success."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount\nabc\ndef\n")

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "error")
            self.assertIn("No readable expense records", result["error"])

    def test_defaults_fill_absent_columns(self):
        """The defaults parameter supplies values for columns absent from the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount,Date\n10.00,2026-09-12\n")

            result = execute(
                {"file_path": path, "defaults": {"currency": "EUR", "is_travel": True}}
            )

            record = result["data"]["records"][0]
            self.assertEqual(record["currency"], "EUR")
            self.assertIs(record["is_travel"], True)

    def test_currency_defaults_to_usd(self):
        """Currency falls back to USD when the file has no currency column."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount\n10.00\n")

            record = execute({"file_path": path})["data"]["records"][0]

            self.assertEqual(record["currency"], "USD")

    def test_every_record_has_every_field(self):
        """All 15 schema fields are present on every record, missing ones as null."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount\n10.00\n")

            record = execute({"file_path": path})["data"]["records"][0]

            expected_fields = {
                "record_id", "employee_id", "employee_name", "expense_date",
                "submitted_date", "category", "merchant", "amount", "currency",
                "attendees", "nights", "receipt_attached", "approval_id",
                "is_travel", "notes",
            }
            self.assertEqual(set(record.keys()), expected_fields)

    def test_json_array_shape(self):
        """A JSON root that is an array of objects is accepted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir,
                "batch.json",
                json.dumps([{"Amount": 10.00, "Date": "2026-09-12"}]),
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "success")
            self.assertEqual(result["data"]["records"][0]["amount"], 10.00)

    def test_json_wrapped_object_shape(self):
        """A JSON root wrapping the array under a known key is accepted."""
        for key in ("records", "expenses", "items"):
            with self.subTest(key=key):
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = self._write(
                        tmpdir,
                        "batch.json",
                        json.dumps({key: [{"Amount": 25.00, "Date": "2026-09-12"}]}),
                    )

                    result = execute({"file_path": path})

                    self.assertEqual(result["status"], "success")
                    self.assertEqual(result["data"]["records"][0]["amount"], 25.00)

    def test_json_wrapped_object_with_unknown_key_is_an_error(self):
        """A JSON object whose array is under an unrecognized key is an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(
                tmpdir, "batch.json", json.dumps({"rows": [{"Amount": 10.00}]})
            )

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "error")
            self.assertIn("records", result["error"])

    def test_missing_file_is_an_error(self):
        """A nonexistent path reports an error naming the path."""
        result = execute({"file_path": "/nonexistent/path/batch.csv"})

        self.assertEqual(result["status"], "error")
        self.assertIn("/nonexistent/path/batch.csv", result["error"])

    def test_missing_file_path_is_an_error(self):
        """Omitting file_path reports an error."""
        result = execute({})

        self.assertEqual(result["status"], "error")
        self.assertIn("file_path", result["error"])

    def test_unsupported_extension_is_an_error(self):
        """A file type other than CSV or JSON is rejected with the supported list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.xlsx", "not really a spreadsheet")

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "error")
            self.assertIn(".csv", result["error"])
            self.assertIn(".json", result["error"])

    def test_empty_csv_is_an_error(self):
        """A CSV with headers but no data rows reports an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write(tmpdir, "batch.csv", "Amount,Date\n")

            result = execute({"file_path": path})

            self.assertEqual(result["status"], "error")
            self.assertIn("No expense records found", result["error"])


if __name__ == "__main__":
    unittest.main()