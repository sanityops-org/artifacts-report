#!/usr/bin/env python3
"""
scan_data_quality: Execute comprehensive data quality checks.

Runs all five check categories: schema, completeness, integrity, anomalies, statistics.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import numpy as np

# Thresholds
SPARSE_THRESHOLD = 0.5  # Columns with >50% missing flagged as sparse
OUTLIER_IQR_MULTIPLIER = 3.0  # Values beyond 3×IQR are outliers
RARE_CATEGORY_THRESHOLD = 0.01  # Categories with <1% are rare

# Maximum file size
MAX_FILE_SIZE = 100 * 1024 * 1024


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute comprehensive data quality checks.

    Args:
        params: {
            "file_path": str,
            "format": "csv" | "json" | "parquet" | "excel",
            "sample_rows": int | None  # Optional: sample N rows for large files
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "schema": {...},
                "completeness": {...},
                "integrity": {...},
                "anomalies": {...},
                "statistics": {...},
                "issue_summary": {...}
            },
            "error": str | None
        }
    """
    file_path = params.get("file_path")
    file_format = params.get("format")

    if not file_path:
        return {"status": "error", "error": "Missing required parameter: file_path"}

    if not file_format:
        return {"status": "error", "error": "Missing required parameter: format"}

    path = Path(file_path)
    if not path.exists():
        return {"status": "error", "error": f"File not found: {file_path}"}

    try:
        # Load data
        df = _load_data(path, file_format, params.get("sample_rows"))

        # Run all checks
        schema = _check_schema(df)
        completeness = _check_completeness(df)
        integrity = _check_integrity(df)
        anomalies = _check_anomalies(df)
        statistics = _profile_statistics(df)

        # Summarize issues
        issue_summary = _summarize_issues(schema, completeness, integrity, anomalies)

        return {
            "status": "success",
            "data": {
                "schema": schema,
                "completeness": completeness,
                "integrity": integrity,
                "anomalies": anomalies,
                "statistics": statistics,
                "issue_summary": issue_summary
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Error scanning data: {str(e)}"}


def _load_data(path: Path, file_format: str, sample_rows: int = None) -> pd.DataFrame:
    """Load data from file into DataFrame."""
    if file_format == "csv":
        # Detect encoding
        import chardet
        raw = path.read_bytes()
        encoding = chardet.detect(raw).get("encoding", "utf-8") or "utf-8"
        df = pd.read_csv(path, encoding=encoding)
    elif file_format == "json":
        content = path.read_text(encoding="utf-8")
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Line-delimited JSON
            data = [json.loads(line) for line in content.strip().split("\n") if line.strip()]

        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            for key in ["records", "data", "items", "results"]:
                if key in data and isinstance(data[key], list):
                    records = data[key]
                    break
            else:
                records = [data]
        else:
            raise ValueError("Invalid JSON structure")

        df = pd.json_normalize(records)
    elif file_format == "parquet":
        df = pd.read_parquet(path)
    elif file_format == "excel":
        df = pd.read_excel(path, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported format: {file_format}")

    if sample_rows and len(df) > sample_rows:
        df = df.sample(n=sample_rows, random_state=42)

    return df


def _check_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Check schema: column names, data types, mixed types."""
    columns = []
    issues = []

    for col in df.columns:
        # Check for column name issues
        name_issues = []
        if re.search(r'[\s\W]', str(col)):
            name_issues.append("special_characters")
        if str(col).strip() != str(col):
            name_issues.append("leading_trailing_spaces")

        # Infer dominant type
        series = df[col]
        non_null = series.dropna()

        if len(non_null) == 0:
            inferred_type = "null"
            mixed_types = False
            type_breakdown = {}
        else:
            # Get type counts
            type_counts = {}
            for val in non_null:
                t = type(val).__name__
                type_counts[t] = type_counts.get(t, 0) + 1

            dominant_type = max(type_counts, key=type_counts.get)
            inferred_type = _map_python_type(dominant_type)
            mixed_types = len(type_counts) > 1
            type_breakdown = type_counts

            if mixed_types:
                total = sum(type_counts.values())
                breakdown_str = ", ".join(f"{t}: {c} ({c*100/total:.0f}%)" for t, c in type_counts.items())
                issues.append({
                    "column": col,
                    "issue": "mixed_types",
                    "severity": "high",
                    "details": breakdown_str
                })

        col_info = {
            "name": col,
            "inferred_type": inferred_type,
            "mixed_types": mixed_types
        }
        if mixed_types:
            col_info["type_breakdown"] = type_breakdown

        columns.append(col_info)

        if name_issues:
            issues.append({
                "column": col,
                "issue": "column_name_issues",
                "severity": "medium",
                "details": ", ".join(name_issues)
            })

    return {
        "columns": columns,
        "issues": issues
    }


def _map_python_type(py_type: str) -> str:
    """Map Python type names to user-friendly types."""
    type_map = {
        "int": "integer",
        "float": "float",
        "str": "string",
        "bool": "boolean",
        "NoneType": "null",
        "list": "array",
        "dict": "object"
    }
    return type_map.get(py_type, py_type)


def _check_completeness(df: pd.DataFrame) -> Dict[str, Any]:
    """Check completeness: nulls, empty strings, sparse columns."""
    by_column = []
    sparse_columns = []
    total_rows = len(df)

    for col in df.columns:
        series = df[col]
        null_count = series.isna().sum()
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0

        # Count empty strings (non-null but empty)
        empty_count = (series == "").sum() if series.dtype == object else 0

        by_column.append({
            "column": col,
            "null_count": int(null_count),
            "null_pct": round(null_pct, 1),
            "empty_count": int(empty_count)
        })

        # Check sparse
        if null_pct >= SPARSE_THRESHOLD * 100:
            sparse_columns.append(col)

    # Count rows with any missing
    incomplete_rows = df.isna().any(axis=1).sum()

    return {
        "by_column": by_column,
        "sparse_columns": sparse_columns,
        "incomplete_rows": int(incomplete_rows),
        "total_rows": total_rows
    }


def _check_integrity(df: pd.DataFrame) -> Dict[str, Any]:
    """Check integrity: duplicates, unique constraint violations."""
    # Exact duplicates
    duplicated = df.duplicated(keep=False)
    dup_indices = duplicated[duplicated].index.tolist()

    # Group duplicates
    groups = []
    if dup_indices:
        seen = set()
        for idx in dup_indices:
            if idx not in seen:
                # Find all rows with same values
                row = df.iloc[idx]
                matching = df[(df == row).all(axis=1)].index.tolist()
                if len(matching) > 1:
                    groups.append({
                        "row_indices": matching,
                        "count": len(matching)
                    })
                    seen.update(matching)

    exact_duplicates = {
        "count": len(dup_indices),
        "groups": groups[:10]  # Limit to 10 groups
    }

    # Unique constraint violations (high-cardinality columns)
    unique_violations = []
    pk_patterns = ["id", "_id", "pk", "key", "code", "uuid"]

    for col in df.columns:
        col_lower = str(col).lower()
        if any(p in col_lower for p in pk_patterns):
            if df[col].duplicated().any():
                dup_vals = df[df[col].duplicated(keep=False)][col].value_counts()
                dup_vals = dup_vals[dup_vals > 1]
                if len(dup_vals) > 0:
                    unique_violations.append({
                        "column": col,
                        "duplicate_values": [
                            {"value": v, "count": int(c)}
                            for v, c in dup_vals.head(5).items()
                        ]
                    })

    return {
        "exact_duplicates": exact_duplicates,
        "near_duplicates": {"count": 0, "sample": []},  # Simplified
        "unique_violations": unique_violations
    }


def _check_anomalies(df: pd.DataFrame) -> Dict[str, Any]:
    """Check anomalies: outliers, format issues, rare categories."""
    numeric_outliers = []
    format_anomalies = []
    value_anomalies = []
    category_outliers = []

    for col in df.columns:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        # Numeric outliers
        if pd.api.types.is_numeric_dtype(series):
            outliers = _detect_outliers_iqr(series)
            if len(outliers) > 0:
                numeric_outliers.append({
                    "column": col,
                    "outlier_count": len(outliers),
                    "range": [float(outliers.min()), float(outliers.max())],
                    "iqr_range": [float(series.quantile(0.25)), float(series.quantile(0.75))]
                })

            # Value anomalies: negatives in positive-only columns
            col_lower = str(col).lower()
            if any(w in col_lower for w in ["age", "count", "quantity", "amount", "price"]):
                negatives = series[series < 0]
                if len(negatives) > 0:
                    value_anomalies.append({
                        "column": col,
                        "issue": "negative_values",
                        "count": int(len(negatives))
                    })

        # Format anomalies (strings)
        if pd.api.types.is_string_dtype(series) or series.dtype == object:
            # Email validation
            if "email" in str(col).lower():
                invalid = series[~series.astype(str).str.match(r'^[^@]+@[^@]+\.[^@]+$', na=False)]
                if len(invalid) > 0:
                    format_anomalies.append({
                        "column": col,
                        "invalid_count": int(len(invalid)),
                        "sample_invalid": invalid.head(5).tolist()
                    })

            # Rare categories
            if len(series) > 10:
                val_counts = series.value_counts()
                rare = val_counts[val_counts / len(series) < RARE_CATEGORY_THRESHOLD]
                if len(rare) > 0:
                    category_outliers.append({
                        "column": col,
                        "rare_values": [
                            {"value": str(v), "count": int(c)}
                            for v, c in rare.head(5).items()
                        ]
                    })

    return {
        "numeric_outliers": numeric_outliers,
        "format_anomalies": format_anomalies,
        "category_outliers": category_outliers,
        "value_anomalies": value_anomalies
    }


def _detect_outliers_iqr(series: pd.Series) -> pd.Series:
    """Detect outliers using IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - OUTLIER_IQR_MULTIPLIER * iqr
    upper = q3 + OUTLIER_IQR_MULTIPLIER * iqr

    outliers = series[(series < lower) | (series > upper)]
    return outliers


def _profile_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Profile statistics: distribution summaries."""
    numeric_columns = []
    categorical_columns = []

    for col in df.columns:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        if pd.api.types.is_numeric_dtype(series):
            stats = {
                "column": col,
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()) if len(series) > 1 else 0.0
            }
            numeric_columns.append(stats)
        else:
            val_counts = series.value_counts()
            stats = {
                "column": col,
                "cardinality": int(len(val_counts)),
                "top_values": [
                    {"value": str(v), "count": int(c)}
                    for v, c in val_counts.head(5).items()
                ]
            }
            categorical_columns.append(stats)

    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns
    }


def _summarize_issues(schema: Dict, completeness: Dict, integrity: Dict, anomalies: Dict) -> Dict[str, Any]:
    """Summarize issue counts by category and severity."""
    total = 0
    by_severity = {"high": 0, "medium": 0, "low": 0, "info": 0}

    # Schema issues
    for issue in schema.get("issues", []):
        total += 1
        sev = issue.get("severity", "medium")
        by_severity[sev] = by_severity.get(sev, 0) + 1

    # Completeness issues (sparse columns)
    total += len(completeness.get("sparse_columns", []))
    by_severity["high"] += len(completeness.get("sparse_columns", []))

    # Integrity issues
    total += integrity.get("exact_duplicates", {}).get("count", 0)
    by_severity["high"] += integrity.get("exact_duplicates", {}).get("count", 0)
    total += len(integrity.get("unique_violations", []))
    by_severity["high"] += len(integrity.get("unique_violations", []))

    # Anomaly issues
    for category in ["numeric_outliers", "format_anomalies", "value_anomalies"]:
        items = anomalies.get(category, [])
        total += len(items)
        by_severity["medium"] += len(items)

    by_severity["low"] += len(anomalies.get("category_outliers", []))

    return {
        "total_issues": total,
        "by_severity": by_severity
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        result = execute({
            "file_path": sys.argv[1],
            "format": sys.argv[2]
        })
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python scan_data_quality.py <file_path> <format>")