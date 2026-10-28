# Data Quality Validator

## Industry
Data Engineering / Analytics

## Description
A file-based data quality scanner that validates CSV, JSON, Parquet, and Excel files for schema integrity, completeness, anomalies, and statistical health — producing actionable Markdown reports.

## Key Features
- **Multi-format Support**: CSV, JSON, Parquet, Excel (.xlsx) in one tool
- **One-Shot Analysis**: All five check categories run automatically without configuration
- **Actionable Reports**: Clear findings with specific column names and values
- **Read-Only Guarantee**: Never modifies user files

## Skills
- `data_quality_scan`: Scan data files for quality issues across all five dimensions

## Created
2026-10-09

## Version
v1.0.0

## Author
agent_artifacts

## Requirements
- Python 3.11+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- pyarrow >= 10.0.0
- chardet >= 5.0.0

## Usage

```bash
# Install dependencies
pip install pandas openpyxl pyarrow chardet

# Run the agent
python scripts/run.py
```

## Example

```
User: Check the quality of /data/sales.csv
Agent: [Produces Markdown report with schema, completeness, integrity, anomaly, and statistics findings]

User: What issues were found?
Agent: [Summarizes issues from the report with specific column names and values]
```

## Quality Check Categories

1. **Schema Validation**: Column names, data types, mixed types, format consistency
2. **Completeness**: Null/NaN counts, empty strings, sparse columns, incomplete rows
3. **Integrity**: Duplicate rows, unique constraint violations
4. **Anomalies**: Numeric outliers, format anomalies, rare categories
5. **Statistics**: Distribution summaries, cardinality, top values

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/data-quality-validator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas openpyxl pyarrow chardet sanityops_agent
python scripts/run.py
```

The runner automatically loads the shared `test-cases/runnable-agent/.env` configuration. If no shared configuration exists, it falls back to an agent-local `.env` file.
