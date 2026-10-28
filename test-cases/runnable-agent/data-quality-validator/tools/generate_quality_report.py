#!/usr/bin/env python3
"""
generate_quality_report: Render data quality scan results as Markdown.

Produces human-readable reports with all findings organized by category and severity.
"""

from pathlib import Path
from typing import Any, Dict


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render data quality scan results as Markdown.

    Args:
        params: {
            "scan_results": {...},
            "file_info": {...},
            "file_path": str
        }

    Returns:
        {
            "status": "success",
            "data": {
                "report": str,
                "issue_count": int,
                "summary": {...}
            }
        }
    """
    scan_results = params.get("scan_results")
    file_info = params.get("file_info")
    file_path = params.get("file_path")

    if not scan_results:
        return {"status": "error", "error": "Missing required parameter: scan_results"}
    if not file_info:
        return {"status": "error", "error": "Missing required parameter: file_info"}

    try:
        report = _render_report(scan_results, file_info, file_path)

        # Calculate issue counts
        issue_summary = scan_results.get("issue_summary", {})

        return {
            "status": "success",
            "data": {
                "report": report,
                "issue_count": issue_summary.get("total_issues", 0),
                "summary": {
                    "schema_issues": len(scan_results.get("schema", {}).get("issues", [])),
                    "completeness_issues": len(scan_results.get("completeness", {}).get("sparse_columns", [])),
                    "integrity_issues": scan_results.get("integrity", {}).get("exact_duplicates", {}).get("count", 0),
                    "anomaly_issues": len(scan_results.get("anomalies", {}).get("numeric_outliers", [])) +
                                     len(scan_results.get("anomalies", {}).get("format_anomalies", []))
                }
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Error generating report: {str(e)}"}


def _render_report(scan_results: Dict, file_info: Dict, file_path: str) -> str:
    """Render full Markdown report."""
    lines = []

    # Header
    filename = Path(file_path).name if file_path else "unknown"
    size_human = _format_size(file_info.get("size_bytes", 0))

    lines.append("# Data Quality Report")
    lines.append("")
    lines.append(f"**File**: {filename}")
    lines.append(f"**Format**: {file_info.get('format', 'unknown').upper()}")
    lines.append(f"**Size**: {size_human}")
    lines.append(f"**Rows**: {file_info.get('row_count', 0)} | **Columns**: {file_info.get('column_count', 0)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    issue_summary = scan_results.get("issue_summary", {})

    lines.append("| Category | Issues Found |")
    lines.append("|----------|--------------|")
    lines.append(f"| Schema | {len(scan_results.get('schema', {}).get('issues', []))} |")
    lines.append(f"| Completeness | {len(scan_results.get('completeness', {}).get('sparse_columns', []))} sparse columns |")
    lines.append(f"| Integrity | {scan_results.get('integrity', {}).get('exact_duplicates', {}).get('count', 0)} duplicates |")
    lines.append(f"| Anomalies | {issue_summary.get('by_severity', {}).get('high', 0) + issue_summary.get('by_severity', {}).get('medium', 0)} issues |")
    lines.append(f"| Statistics | Profiled {file_info.get('column_count', 0)} columns |")
    lines.append("")

    # Severity breakdown
    by_severity = issue_summary.get("by_severity", {})
    total = issue_summary.get("total_issues", 0)

    if total > 0:
        lines.append(f"**Total Issues**: {total}")
        lines.append(f"- High: {by_severity.get('high', 0)}")
        lines.append(f"- Medium: {by_severity.get('medium', 0)}")
        lines.append(f"- Low: {by_severity.get('low', 0)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Schema Issues
    lines.append("## Schema")
    lines.append("")
    schema = scan_results.get("schema", {})
    issues = schema.get("issues", [])

    if issues:
        for issue in issues:
            severity = issue.get("severity", "medium").upper()
            lines.append(f"### {severity}: {issue.get('issue', 'unknown')} in column \"{issue.get('column', 'unknown')}\"")
            lines.append("")
            lines.append(issue.get("details", "No details available"))
            lines.append("")
    else:
        lines.append("No schema issues detected.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Completeness
    lines.append("## Completeness")
    lines.append("")
    completeness = scan_results.get("completeness", {})
    by_column = completeness.get("by_column", [])

    if by_column:
        lines.append("### Missing Values by Column")
        lines.append("")
        lines.append("| Column | Null Count | Null % | Empty Count |")
        lines.append("|--------|------------|--------|-------------|")

        for col in by_column:
            lines.append(f"| {col.get('column', 'unknown')} | {col.get('null_count', 0)} | {col.get('null_pct', 0)}% | {col.get('empty_count', 0)} |")

        lines.append("")

    sparse = completeness.get("sparse_columns", [])
    if sparse:
        lines.append(f"### Sparse Columns (>50% missing)")
        lines.append("")
        lines.append(", ".join(sparse))
        lines.append("")

    incomplete_rows = completeness.get("incomplete_rows", 0)
    if incomplete_rows > 0:
        lines.append(f"**Rows with missing values**: {incomplete_rows}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Integrity
    lines.append("## Integrity")
    lines.append("")
    integrity = scan_results.get("integrity", {})

    # Exact duplicates
    exact_dups = integrity.get("exact_duplicates", {})
    dup_count = exact_dups.get("count", 0)

    if dup_count > 0:
        lines.append(f"### Exact Duplicates: {dup_count} rows")
        lines.append("")
        groups = exact_dups.get("groups", [])
        for group in groups[:5]:
            indices = group.get("row_indices", [])
            lines.append(f"- Rows {', '.join(str(i) for i in indices[:10])} are identical")
        lines.append("")
    else:
        lines.append("No exact duplicates found.")
        lines.append("")

    # Unique violations
    unique_violations = integrity.get("unique_violations", [])
    if unique_violations:
        lines.append("### Unique Constraint Violations")
        lines.append("")
        for violation in unique_violations:
            col = violation.get("column", "unknown")
            lines.append(f"- Column `{col}` has duplicate values that should be unique")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Anomalies
    lines.append("## Anomalies")
    lines.append("")
    anomalies = scan_results.get("anomalies", {})

    # Numeric outliers
    numeric_outliers = anomalies.get("numeric_outliers", [])
    if numeric_outliers:
        lines.append("### Numeric Outliers")
        lines.append("")
        for outlier in numeric_outliers:
            col = outlier.get("column", "unknown")
            count = outlier.get("outlier_count", 0)
            lines.append(f"- Column `{col}`: {count} outliers detected")
        lines.append("")

    # Format anomalies
    format_anomalies = anomalies.get("format_anomalies", [])
    if format_anomalies:
        lines.append("### Format Anomalies")
        lines.append("")
        for anomaly in format_anomalies:
            col = anomaly.get("column", "unknown")
            count = anomaly.get("invalid_count", 0)
            samples = anomaly.get("sample_invalid", [])
            lines.append(f"- Column `{col}`: {count} invalid values")
            if samples:
                lines.append(f"  - Examples: {', '.join(str(s) for s in samples[:3])}")
        lines.append("")

    # Value anomalies
    value_anomalies = anomalies.get("value_anomalies", [])
    if value_anomalies:
        lines.append("### Value Anomalies")
        lines.append("")
        for anomaly in value_anomalies:
            col = anomaly.get("column", "unknown")
            issue = anomaly.get("issue", "unknown")
            count = anomaly.get("count", 0)
            lines.append(f"- Column `{col}`: {count} {issue}")
        lines.append("")

    if not (numeric_outliers or format_anomalies or value_anomalies):
        lines.append("No anomalies detected.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Statistics
    lines.append("## Statistical Profile")
    lines.append("")
    statistics = scan_results.get("statistics", {})

    # Numeric columns
    numeric_cols = statistics.get("numeric_columns", [])
    if numeric_cols:
        lines.append("### Numeric Columns")
        lines.append("")
        lines.append("| Column | Min | Max | Mean | Median | Std |")
        lines.append("|--------|-----|-----|------|--------|-----|")

        for col in numeric_cols:
            lines.append(f"| {col.get('column', 'unknown')} | {col.get('min', 0):.2f} | {col.get('max', 0):.2f} | {col.get('mean', 0):.2f} | {col.get('median', 0):.2f} | {col.get('std', 0):.2f} |")

        lines.append("")

    # Categorical columns
    categorical_cols = statistics.get("categorical_columns", [])
    if categorical_cols:
        lines.append("### Categorical Columns")
        lines.append("")
        lines.append("| Column | Cardinality | Top Value |")
        lines.append("|--------|-------------|-----------|")

        for col in categorical_cols:
            top_values = col.get("top_values", [])
            top = top_values[0] if top_values else {}
            lines.append(f"| {col.get('column', 'unknown')} | {col.get('cardinality', 0)} | {top.get('value', 'N/A')} ({top.get('count', 0)}) |")

        lines.append("")

    return "\n".join(lines)


def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable form."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            scan_results = json.load(f)

        result = execute({
            "scan_results": scan_results,
            "file_info": {"format": "csv", "row_count": 100, "column_count": 5, "size_bytes": 1024, "columns": ["id"]},
            "file_path": sys.argv[1]
        })
        print(result["data"]["report"])
    else:
        print("Usage: python generate_quality_report.py <scan_results.json>")