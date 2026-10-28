#!/usr/bin/env python3
"""Tests for generate_quality_report tool."""

import sys
from pathlib import Path

# Add tools to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "tools"))

import generate_quality_report


def test_generate_report_structure():
    """Test report has required sections."""
    scan_results = {
        "schema": {"columns": [], "issues": []},
        "completeness": {"by_column": [], "sparse_columns": [], "incomplete_rows": 0, "total_rows": 100},
        "integrity": {"exact_duplicates": {"count": 0, "groups": []}, "near_duplicates": {"count": 0, "sample": []}, "unique_violations": []},
        "anomalies": {"numeric_outliers": [], "format_anomalies": [], "category_outliers": [], "value_anomalies": []},
        "statistics": {"numeric_columns": [], "categorical_columns": []},
        "issue_summary": {"total_issues": 0, "by_severity": {"high": 0, "medium": 0, "low": 0, "info": 0}}
    }

    file_info = {
        "format": "csv",
        "row_count": 100,
        "column_count": 5,
        "size_bytes": 1024,
        "columns": ["id", "name", "email"]
    }

    result = generate_quality_report.execute({
        "scan_results": scan_results,
        "file_info": file_info,
        "file_path": "/path/to/file.csv"
    })

    assert result["status"] == "success", f"Expected success, got: {result}"
    report = result["data"]["report"]

    # Check required sections
    assert "# Data Quality Report" in report
    assert "## Summary" in report
    assert "## Schema" in report or "## Schema Issues" in report
    assert "## Completeness" in report
    assert "## Integrity" in report or "## Integrity Issues" in report
    assert "## Anomalies" in report
    assert "## Statistics" in report or "## Statistical Profile" in report


def test_generate_report_includes_file_info():
    """Test report includes file metadata."""
    scan_results = {
        "schema": {"columns": [], "issues": []},
        "completeness": {"by_column": [], "sparse_columns": [], "incomplete_rows": 0, "total_rows": 100},
        "integrity": {"exact_duplicates": {"count": 0, "groups": []}, "near_duplicates": {"count": 0, "sample": []}, "unique_violations": []},
        "anomalies": {"numeric_outliers": [], "format_anomalies": [], "category_outliers": [], "value_anomalies": []},
        "statistics": {"numeric_columns": [], "categorical_columns": []},
        "issue_summary": {"total_issues": 0, "by_severity": {"high": 0, "medium": 0, "low": 0, "info": 0}}
    }

    file_info = {
        "format": "csv",
        "row_count": 100,
        "column_count": 5,
        "size_bytes": 1024,
        "columns": ["id", "name"]
    }

    result = generate_quality_report.execute({
        "scan_results": scan_results,
        "file_info": file_info,
        "file_path": "/path/to/data.csv"
    })

    assert result["status"] == "success"
    report = result["data"]["report"]

    assert "data.csv" in report
    assert "CSV" in report
    assert "100" in report


def test_generate_report_shows_issues():
    """Test report shows issues when present."""
    scan_results = {
        "schema": {
            "columns": [{"name": "id", "inferred_type": "integer", "mixed_types": False}],
            "issues": [{"column": "price", "issue": "mixed_types", "severity": "high", "details": "Mixed types detected"}]
        },
        "completeness": {
            "by_column": [{"column": "id", "null_count": 0, "null_pct": 0.0, "empty_count": 0}],
            "sparse_columns": [],
            "incomplete_rows": 5,
            "total_rows": 100
        },
        "integrity": {"exact_duplicates": {"count": 2, "groups": []}, "near_duplicates": {"count": 0, "sample": []}, "unique_violations": []},
        "anomalies": {"numeric_outliers": [], "format_anomalies": [], "category_outliers": [], "value_anomalies": []},
        "statistics": {"numeric_columns": [], "categorical_columns": []},
        "issue_summary": {"total_issues": 3, "by_severity": {"high": 1, "medium": 0, "low": 0, "info": 0}}
    }

    file_info = {
        "format": "csv",
        "row_count": 100,
        "column_count": 5,
        "size_bytes": 1024,
        "columns": ["id", "price"]
    }

    result = generate_quality_report.execute({
        "scan_results": scan_results,
        "file_info": file_info,
        "file_path": "/path/to/data.csv"
    })

    assert result["status"] == "success"
    report = result["data"]["report"]

    assert "mixed_types" in report.lower() or "Mixed types" in report


def test_generate_report_zero_issues():
    """Test report for clean data (zero issues)."""
    scan_results = {
        "schema": {"columns": [{"name": "id", "inferred_type": "integer", "mixed_types": False}], "issues": []},
        "completeness": {"by_column": [{"column": "id", "null_count": 0, "null_pct": 0.0, "empty_count": 0}], "sparse_columns": [], "incomplete_rows": 0, "total_rows": 100},
        "integrity": {"exact_duplicates": {"count": 0, "groups": []}, "near_duplicates": {"count": 0, "sample": []}, "unique_violations": []},
        "anomalies": {"numeric_outliers": [], "format_anomalies": [], "category_outliers": [], "value_anomalies": []},
        "statistics": {"numeric_columns": [], "categorical_columns": []},
        "issue_summary": {"total_issues": 0, "by_severity": {"high": 0, "medium": 0, "low": 0, "info": 0}}
    }

    file_info = {
        "format": "csv",
        "row_count": 100,
        "column_count": 5,
        "size_bytes": 1024,
        "columns": ["id"]
    }

    result = generate_quality_report.execute({
        "scan_results": scan_results,
        "file_info": file_info,
        "file_path": "/path/to/clean.csv"
    })

    assert result["status"] == "success"
    assert result["data"]["issue_count"] == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])