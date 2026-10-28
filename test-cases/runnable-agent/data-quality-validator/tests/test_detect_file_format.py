#!/usr/bin/env python3
"""Tests for detect_file_format tool."""

import sys
import tempfile
from pathlib import Path

# Add tools to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "tools"))

import detect_file_format


def test_detect_csv_format():
    """Test CSV format detection."""
    # Use the sample data file
    csv_path = project_root / "data" / "sample_data" / "clean_data.csv"

    result = detect_file_format.execute({"file_path": str(csv_path)})

    assert result["status"] == "success", f"Expected success, got: {result}"
    data = result["data"]

    assert data["format"] == "csv"
    assert data["row_count"] == 3
    assert data["column_count"] == 5
    assert "id" in data["columns"]
    assert "name" in data["columns"]
    assert data["encoding"] in ("utf-8", "ascii")


def test_detect_missing_file():
    """Test error handling for missing file."""
    result = detect_file_format.execute({"file_path": "/nonexistent/path/file.csv"})

    assert result["status"] == "error"
    assert "not found" in result["error"].lower() or "does not exist" in result["error"].lower()


def test_detect_unsupported_format():
    """Test error handling for unsupported file extension."""
    # Create a temporary unsupported file
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        f.write(b"test content")
        temp_path = f.name

    try:
        result = detect_file_format.execute({"file_path": temp_path})

        assert result["status"] == "error"
        assert "unsupported" in result["error"].lower()
    finally:
        Path(temp_path).unlink()


def test_detect_csv_columns():
    """Test column extraction from CSV."""
    csv_path = project_root / "data" / "sample_data" / "clean_data.csv"

    result = detect_file_format.execute({"file_path": str(csv_path)})

    assert result["status"] == "success"
    columns = result["data"]["columns"]

    assert columns == ["id", "name", "email", "age", "created_at"]


def test_detect_file_size():
    """Test file size reporting."""
    csv_path = project_root / "data" / "sample_data" / "clean_data.csv"

    result = detect_file_format.execute({"file_path": str(csv_path)})

    assert result["status"] == "success"
    assert result["data"]["size_bytes"] > 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])