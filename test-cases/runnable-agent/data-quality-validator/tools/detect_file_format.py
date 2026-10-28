#!/usr/bin/env python3
"""
detect_file_format: Identify file format, encoding, and basic statistics.

Detects CSV, JSON, Parquet, and Excel file formats and returns metadata.
"""

import json
from pathlib import Path
from typing import Any, Dict

# Size threshold for large files (50MB)
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024

# Maximum file size (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024

# Supported formats
SUPPORTED_FORMATS = {"csv", "json", "parquet", "excel"}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Identify file format, encoding, and basic statistics.

    Args:
        params: {
            "file_path": str  # Path to the data file
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "format": "csv" | "json" | "parquet" | "excel",
                "encoding": str,  # Detected encoding for text files
                "row_count": int,
                "column_count": int,
                "size_bytes": int,
                "columns": [str, ...]
            },
            "error": str | None
        }
    """
    file_path = params.get("file_path")
    if not file_path:
        return {
            "status": "error",
            "error": "Missing required parameter: file_path"
        }

    path = Path(file_path)

    # Check file exists
    if not path.exists():
        return {
            "status": "error",
            "error": f"File not found: {file_path}"
        }

    # Check it's a file (not a directory)
    if not path.is_file():
        return {
            "status": "error",
            "error": f"Path is not a file: {file_path}"
        }

    # Check file size
    size_bytes = path.stat().st_size
    if size_bytes > MAX_FILE_SIZE:
        size_mb = size_bytes / (1024 * 1024)
        return {
            "status": "error",
            "error": f"File too large ({size_mb:.1f}MB). Maximum supported size is 100MB. Consider splitting or sampling the file."
        }

    # Determine format from extension
    ext = path.suffix.lower()
    format_map = {
        ".csv": "csv",
        ".json": "json",
        ".parquet": "parquet",
        ".xlsx": "excel"
    }

    if ext not in format_map:
        return {
            "status": "error",
            "error": f"Unsupported file format: {ext}. Supported formats: {', '.join(format_map.keys())}"
        }

    file_format = format_map[ext]

    # Get format-specific metadata
    try:
        if file_format == "csv":
            return _analyze_csv(path, size_bytes)
        elif file_format == "json":
            return _analyze_json(path, size_bytes)
        elif file_format == "parquet":
            return _analyze_parquet(path, size_bytes)
        elif file_format == "excel":
            return _analyze_excel(path, size_bytes)
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error analyzing {file_format} file: {str(e)}"
        }


def _analyze_csv(path: Path, size_bytes: int) -> Dict[str, Any]:
    """Analyze CSV file."""
    try:
        import chardet
    except ImportError:
        chardet = None

    # Detect encoding, with a UTF-8 fallback when chardet is unavailable.
    raw_data = path.read_bytes()
    if chardet is None:
        encoding = "utf-8"
    else:
        encoding_result = chardet.detect(raw_data)
        encoding = encoding_result.get("encoding", "utf-8") or "utf-8"

    # Use pandas for robust CSV parsing
    import pandas as pd

    try:
        df = pd.read_csv(path, encoding=encoding, nrows=10000)
    except Exception:
        # Fallback to no encoding specification
        df = pd.read_csv(path, nrows=10000)
        encoding = "utf-8"

    # Count total rows (may be more than loaded)
    with open(path, "r", encoding=encoding, errors="replace") as f:
        total_rows = sum(1 for _ in f) - 1  # Subtract header

    return {
        "status": "success",
        "data": {
            "format": "csv",
            "encoding": encoding.lower(),
            "row_count": total_rows,
            "column_count": len(df.columns),
            "size_bytes": size_bytes,
            "columns": list(df.columns)
        }
    }


def _analyze_json(path: Path, size_bytes: int) -> Dict[str, Any]:
    """Analyze JSON file."""
    import pandas as pd

    content = path.read_text(encoding="utf-8")

    # Try to parse as JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Try line-delimited JSON
        lines = content.strip().split("\n")
        data = [json.loads(line) for line in lines if line.strip()]

    # Normalize to list of records
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # Try common keys for records
        for key in ["records", "data", "items", "results"]:
            if key in data and isinstance(data[key], list):
                records = data[key]
                break
        else:
            # Single record
            records = [data]
    else:
        return {
            "status": "error",
            "error": "JSON must contain an array of records or an object with a records array"
        }

    df = pd.json_normalize(records[:10000])

    return {
        "status": "success",
        "data": {
            "format": "json",
            "encoding": "utf-8",
            "row_count": len(records),
            "column_count": len(df.columns),
            "size_bytes": size_bytes,
            "columns": list(df.columns)
        }
    }


def _analyze_parquet(path: Path, size_bytes: int) -> Dict[str, Any]:
    """Analyze Parquet file."""
    import pyarrow.parquet as pq

    table = pq.read_table(path)

    return {
        "status": "success",
        "data": {
            "format": "parquet",
            "encoding": "binary",
            "row_count": table.num_rows,
            "column_count": table.num_columns,
            "size_bytes": size_bytes,
            "columns": table.column_names
        }
    }


def _analyze_excel(path: Path, size_bytes: int) -> Dict[str, Any]:
    """Analyze Excel file."""
    import pandas as pd

    # Read first sheet
    df = pd.read_excel(path, nrows=10000, engine="openpyxl")

    # Get total row count
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    total_rows = ws.max_row - 1  # Subtract header
    wb.close()

    return {
        "status": "success",
        "data": {
            "format": "excel",
            "encoding": "binary",
            "row_count": total_rows,
            "column_count": len(df.columns),
            "size_bytes": size_bytes,
            "columns": list(df.columns)
        }
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = execute({"file_path": sys.argv[1]})
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python detect_file_format.py <file_path>")