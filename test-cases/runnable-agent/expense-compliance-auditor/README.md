# Expense Compliance Auditor

## Industry

Finance & Compliance

## Description

An agent that audits batches of employee expense records against a company expense policy. It reads a CSV or JSON export, evaluates every record against every applicable rule, detects duplicate submissions, and produces a report in which each finding cites the rule it breached, the actual value, and the limit applied.

The agent is **detect-only**. It never modifies, corrects, or rewrites expense data. Contradictory or missing information is reported as `needs_review` rather than guessed at.

## Key Features

- **Rule traceability**: every finding carries a `rule_id`, the actual value, the limit, and the overage — any reviewer can recompute the conclusion by hand
- **Deterministic engine**: identical input always produces identical output, including report ordering
- **No configuration files**: the default policy is a Python constant, so nothing can drift out of sync with a YAML file
- **Honest boundaries**: unreachable verdicts become `needs_review` with the missing field named; non-USD records are flagged rather than converted at a guessed rate
- **Batch-resilient**: a malformed row is collected and listed, never allowed to abort the batch

## Skills

- `expense_audit`: Audit an expense batch and report violations and items needing review
- `policy_management`: Show the effective policy and apply session-scoped threshold overrides
- `audit_report`: Generate a deliverable Markdown or JSON report for finance or auditors

## Tools

| Tool | Purpose |
|------|---------|
| `parse_expenses` | Read a CSV or JSON export and normalize records into a fixed 15-field schema |
| `get_policy` | Return the effective policy (built-in defaults merged with overrides) |
| `audit_expenses` | Evaluate every (record, applicable rule) pair and emit traceable verdicts |
| `detect_duplicates` | Group records that appear to be the same expense submitted more than once |
| `generate_report` | Render Markdown or JSON from audit results |

## Default Policy

| Rule | Threshold | Severity |
|------|-----------|----------|
| `meal_limit_per_person` | $75 per person | high |
| `hotel_limit_per_night` | $250 per night | high |
| `receipt_required_above` | $25 | medium |
| `prohibited_category` | alcohol, gambling, personal_items, fines | high |
| `submission_window` | 60 days after the expense date | medium |
| `approval_required_above` | $500 | medium |
| `weekend_non_travel_meal` | flagged for review | low |
| `duplicate_suspected` | amount ±1%, date ±3 days | high |

Thresholds are inclusive: a value exactly at a limit passes.

## Created

2026-10-09

## Version

v1.0.0

## Author

agent_artifacts

## Requirements

- Python 3.11+
- No third-party packages. The agent uses only the standard library.
- `sanityops_agent` is required to start the agent via `scripts/run.py`.

## Usage

```bash
# Check the environment (layout, tools, skills, sample data)
python scripts/setup.py

# Run the agent
python scripts/run.py
```

## Testing

```bash
# Unit tests, one file per tool
python -m unittest discover -s tests -v

# End-to-end run over all three sample batches
python scripts/test_integration.py
```

## Sample Data

| File | Records | Expected outcome |
|------|---------|------------------|
| `data/sample_expenses/clean_batch.csv` | 6 | 6 pass, no findings |
| `data/sample_expenses/violations_batch.csv` | 10 | 3 pass, 6 violations, 1 needs review |
| `data/sample_expenses/duplicates_batch.json` | 12 | 3 duplicate groups, 7 records |

`violations_batch.csv` includes three boundary records that sit exactly on the meal, receipt, and approval thresholds. All three must pass.

## Example

```
User: Audit data/sample_expenses/violations_batch.csv

Agent: [calls parse_expenses, get_policy, audit_expenses, detect_duplicates]

Expense Audit — violations_batch.csv
Records: 10    Pass: 3    Violations: 6    Needs review: 1

HIGH SEVERITY

EXP-2001 — Alice Kim — meals $120.00
  Rule: Meals must not exceed $75 per person
  Actual: $120.00 per person (1 attendee) · Limit: $75.00
  Overage: $45.00

EXP-2002 — Alice Kim — lodging $600.00
  Rule: Lodging must not exceed $250 per night
  Actual: $300.00 per night (2 nights) · Limit: $250.00
  Overage: $50.00

NEEDS REVIEW

EXP-2007 — Dan Ortiz — meals $40.00
  Rule: Weekend meals not marked as travel require manual review
  Reason: Saturday meal not marked as travel
```

```
User: Our hotel cap is 200, re-run that audit

Agent: [calls get_policy with overrides {"hotel_limit_per_night": {"limit": 200.00}},
        then re-runs the audit]

Applied override: hotel_limit_per_night limit $250.00 → $200.00 (this session only)
```

## Scope Boundaries

This agent deliberately does not:

- Parse scanned receipts or PDFs (structured exports only)
- Convert currencies (non-USD records are flagged for review)
- Modify, correct, or rewrite any expense data
- Connect to Expensify, Concur, or Ramp APIs
- Provide legal, tax, or accounting advice

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/expense-compliance-auditor
python3 -m venv .venv
source .venv/bin/activate
# This agent uses only the Python standard library.
python scripts/setup.py
python scripts/run.py
```
