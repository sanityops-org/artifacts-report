#!/usr/bin/env python3
"""Tests for scan_data_quality tool."""

import sys
import json
from pathlib import Path

# Add tools to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "tools"))

import scan_data_quality


def test_scan_json_basic():
    """Test basic JSON scan executes all five categories."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success", f"Expected success, got: {result}"
    data = result["data"]

    # All five categories must be present
    assert "schema" in data
    assert "completeness" in data
    assert "integrity" in data
    assert "anomalies" in data
    assert "statistics" in data
    assert "issue_summary" in data


def test_scan_detects_nulls():
    """Test completeness check detects null values."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    completeness = result["data"]["completeness"]

    # Check that null counts were detected
    found_null = False
    for col in completeness["by_column"]:
        if col["null_count"] > 0:
            found_null = True
            break

    assert found_null, "Expected to find null values in completeness check"


def test_scan_detects_duplicates():
    """Test integrity check detects duplicate rows."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    integrity = result["data"]["integrity"]

    # Should have exact duplicates (rows 1 and 4)
    assert integrity["exact_duplicates"]["count"] >= 1


def test_scan_detects_outliers():
    """Test anomaly detection finds numeric outliers."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    anomalies = result["data"]["anomalies"]

    # Should detect outliers in age (200, -5) or price (1000000)
    assert len(anomalies.get("numeric_outliers", [])) > 0 or \
           len(anomalies.get("value_anomalies", [])) > 0


def test_scan_detects_format_anomalies():
    """Test anomaly detection finds format issues."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    anomalies = result["data"]["anomalies"]

    # Should detect invalid email
    format_issues = anomalies.get("format_anomalies", [])
    email_issues = [f for f in format_issues if f.get("column") == "email"]
    assert len(email_issues) > 0 or len(format_issues) > 0


def test_scan_statistics_profile():
    """Test statistical profiling generates correct stats."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    stats = result["data"]["statistics"]

    # Should have numeric and categorical columns
    assert "numeric_columns" in stats or "statistics" in stats


def test_scan_issue_summary():
    """Test issue summary aggregates counts correctly."""
    json_path = project_root / "data" / "sample_data" / "issues_data.json"

    result = scan_data_quality.execute({
        "file_path": str(json_path),
        "format": "json"
    })

    assert result["status"] == "success"
    summary = result["data"]["issue_summary"]

    assert "total_issues" in summary
    assert summary["total_issues"] > 0  # We know this file has issues


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])