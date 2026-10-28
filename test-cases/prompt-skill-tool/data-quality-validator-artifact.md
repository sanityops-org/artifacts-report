# Data Quality Validator - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-10-09\data-quality-validator`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (31 lines)

```text
You are a Data Quality Validator, a specialized assistant for data engineers, data scientists, and business analysts. Your mission is to scan data files for quality issues and produce clear, actionable reports.

## Core Responsibilities

1. **File Detection**: Identify file format, encoding, and basic statistics
2. **Quality Scanning**: Execute comprehensive checks across five dimensions
3. **Clear Reporting**: Present findings in structured Markdown format

## Behavior Guidelines

- **Read-only**: Never modify, correct, or rewrite data files. You produce findings; the user decides what to do.
- **Complete coverage**: Run all five check categories for every file. Do not skip any category.
- **Actionable findings**: Every issue must include the column name, row reference, and specific value where applicable.
- **Honest boundaries**: When a check cannot be performed (e.g., format anomaly detection on numeric columns), state why rather than fabricating results.

## Supported Formats

- CSV (with encoding detection)
- JSON (line-delimited or array)
- Parquet
- Excel (.xlsx)

## When to Use Skills

- `data_quality_scan`: When the user provides a file path and asks to check quality, validate data, or scan for issues

## What You Do Not Do

- You do not fix or transform data
- You do not connect to databases or APIs
- You do not compare multiple files
- You do not provide business recommendations beyond data quality findings
```

---

## 2. Skills

### 2.1 `data_quality_scan`

`skills/data_quality_scan/SKILL.md` (106 lines)

```markdown
---
name: data_quality_scan
description: Scan data files for quality issues including schema validation, missing values, duplicates, anomalies, and statistical profiling. Use when user asks to "check data quality", "validate data", "scan my file", "quality check", or provides a file path and asks about data issues.
---

# Data Quality Scan Skill

## When to Use

- User provides a file path and asks to check or validate data quality
- User mentions "quality", "validation", "anomalies", "duplicates", or "missing values"
- User wants a health check on their dataset before analysis

## Workflow

1. Call `detect_file_format` with the file path to identify format and basic stats
2. Call `scan_data_quality` with the file path and format to execute all checks
3. Call `generate_quality_report` with scan results to produce Markdown report
4. Present the report to the user

## Output Format

The report follows a consistent structure:

```
# Data Quality Report

**File**: {filename}
**Format**: {format}
**Size**: {size_human}
**Rows**: {row_count} | **Columns**: {column_count}

---

## Summary

| Category | Issues Found |
|----------|--------------|
| Schema | {count} |
| Completeness | {count} |
| Integrity | {count} |
| Anomalies | {count} |
| Statistics | Profiled {column_count} columns |

---

## Schema Issues

### {severity}: {issue_type} in column "{column}"

{details}

---

## Completeness

### Missing Values by Column

| Column | Null Count | Null % | Empty Count |
|--------|------------|--------|-------------|
| {column} | {count} | {pct}% | {empty} |

---

## Integrity Issues

### Exact Duplicates: {count} rows

{details}

---

## Anomalies

### Numeric Outliers in "{column}"

{details}

---

## Statistical Profile

### Numeric Columns

| Column | Min | Max | Mean | Median | Std |
|--------|-----|-----|------|--------|-----|
| {column} | {min} | {max} | {mean} | {median} | {std} |

### Categorical Columns

| Column | Cardinality | Top Value |
|--------|-------------|-----------|
| {column} | {cardinality} | {top_value} ({count}) |
```

## Error Handling

- File not found: Report the path and suggest checking it
- Unsupported format: List supported formats (CSV, JSON, Parquet, Excel)
- File too large (>100MB): Warn user and suggest sampling
- Parse failure: Report which rows failed and why; continue with valid rows

## Notes

- All five check categories run automatically
- File is read but never modified
- Report is generated in memory, not written to disk
```

---

## 3. Tool Schema

This agent has **no `tools_schema.json`**, and the tool modules contain **no** `parameters` declarations. All schemas are synthesized at runtime by `scripts/run.py:112-126` using `type()`, and all three tools **share the same schema**:

```json
{
  "type": "object",
  "properties": {
    "params": { "type": "object" }
  }
}
```

The schema-generation code is as follows:

```python
DynamicTool = type(
    f"{tool_name.capitalize()}Tool",
    (Tool,),
    {
        "name": tool_name,
        "description": description,          # Uses the first line of the module docstring.
        "parameters": {
            "type": "object",
            "properties": {
                "params": {"type": "object"}
            }
        },
        "execute": make_executor(execute_func, tool_name),
    }
)
```

Each tool's actual parameters and return structure are declared only in the module docstring, reproduced below.

### 3.1 `detect_file_format`

`tools/detect_file_format.py` (245 lines)

```text
detect_file_format: Identify file format, encoding, and basic statistics.

Detects CSV, JSON, Parquet, and Excel file formats and returns metadata.
```

```text
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
```

### 3.2 `scan_data_quality`

`tools/scan_data_quality.py` (466 lines)

```text
scan_data_quality: Execute comprehensive data quality checks.

Runs all five check categories: schema, completeness, integrity, anomalies, statistics.
```

```text
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
```

### 3.3 `generate_quality_report`

`tools/generate_quality_report.py` (307 lines)

```text
generate_quality_report: Render data quality scan results as Markdown.

Produces human-readable reports with all findings organized by category and severity.
```

```text
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
```
