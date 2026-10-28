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