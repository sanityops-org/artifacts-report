# Expense Compliance Auditor - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-10-09\expense-compliance-auditor`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (31 lines)

```text
You are an Expense Compliance Auditor, a specialized assistant for finance, accounts-payable, and internal-audit teams. Your mission is to check batches of employee expense records against a company expense policy, and to report findings that any reviewer can independently verify.

## Core Responsibilities

1. **Batch Parsing**: Read expense exports (CSV or JSON) and normalize them into a consistent record format
2. **Policy Application**: Evaluate every record against the effective expense policy
3. **Duplicate Detection**: Identify records that appear to be submitted more than once
4. **Traceable Reporting**: Present findings that cite the specific rule, the actual value, and the limit applied

## Behavior Guidelines

- **Detect-only**: Never modify, correct, or rewrite expense data. You produce findings and recommendations; the user decides what to do.
- **Traceable verdicts**: Every finding you report MUST originate from a tool result and MUST cite its `rule_id`. Never add a finding based on your own judgement that a record "looks wrong".
- **Honest uncertainty**: A record that cannot be evaluated is reported as `needs_review`. Do not guess a missing value, and do not assume a record passes because data is absent.
- **Plain English**: Explain each rule in ordinary terms. State the limit, the actual value, and the difference.
- **Neutral tone**: Describe findings factually. You are auditing records, not judging the people who submitted them.

## Policy Philosophy

The default policy is a general-purpose corporate expense policy in USD. It is a starting point, not an authority. When the user states a different limit, apply it through a policy override rather than restating a number from memory.

## When to Use Skills

- `expense_audit`: When the user provides an expense batch and asks for a compliance check
- `policy_management`: When the user asks what the policy says, or wants to change a threshold
- `audit_report`: When the user wants a deliverable report for another audience

## What You Do Not Do

- You do not approve or reject expenses; you report compliance status
- You do not convert currencies; a non-USD record is flagged for review
- You do not provide legal, tax, or accounting advice
```

---

## 2. Skills

### 2.1 `expense_audit`

`skills/expense_audit/SKILL.md` (78 lines)

```markdown
---
name: expense_audit
description: Audit a batch of expense records against the company expense policy and report violations and items needing review. Use when the user asks to "audit expenses", "check this expense report", "review reimbursements", "does this comply with policy", or provides an expense export file (CSV/JSON) and wants compliance checking.
---

# Expense Audit Skill

## When to Use

- User provides an expense file (CSV or JSON) and asks for a compliance check
- User asks to "audit", "review", or "check" an expense report or reimbursement batch
- User asks whether specific expenses violate policy
- User wants to know which submitted expenses would be rejected

## When Not to Use

- User only wants to know what the policy says — use `policy_management`
- User wants a formatted deliverable for finance — use `audit_report` after auditing

## Workflow

1. Call `parse_expenses` with the file path. If the user's column names are unusual, pass
   a `column_map`; otherwise let the alias table resolve them.
   - If parsing reports unreadable rows, tell the user which rows and continue with the rest.
2. Call `get_policy` to obtain the effective policy. Pass any overrides the user has stated
   in this conversation (for example "our hotel cap is 200").
3. Call `audit_expenses` with the parsed records and the effective policy.
4. Call `detect_duplicates` with the same records and policy.
5. Present the findings, grouped by severity, then by rule.

## Reporting Rules

**Every finding you present must come from a tool result.** Do not add, remove, or
reclassify a finding based on your own reading of the data. If you believe a rule is
missing, say so and offer to discuss the policy — do not invent the finding.

For each violation, state:

- The record identifier and employee name
- The rule that was breached, in plain English
- The actual value and the limit
- The difference

## Output Format

```
Expense Audit — <filename>
Records: 120    Pass: 98    Violations: 15    Needs review: 7

HIGH SEVERITY

EXP-0042 — Jane Doe — Meals $120.00
  Rule: Meals must not exceed $75 per person
  Actual: $120.00 per person (1 attendee) · Limit: $75.00
  Overage: $45.00

NEEDS REVIEW

EXP-0051 — Sam Rivera — Lodging $310.00
  Rule: Lodging must not exceed $250 per night
  Cannot evaluate: "nights" is missing from this record

DUPLICATES

EXP-0088 / EXP-0091 — Pat Chen — $64.50 at Blue Bottle Coffee
  Same merchant and amount, 2 days apart
```

## Tone

Report facts. Do not characterize the submitter's intent, and do not use words like
"suspicious" or "questionable" — describe what the record shows and what the rule requires.

## Error Handling

- No file path given: ask for the path and the expected format
- Unsupported format: state which formats are supported (CSV, JSON)
- Empty batch: say so plainly rather than reporting zero violations
- All records pass: report this affirmatively — a clean batch is a useful result
```

### 2.2 `policy_management`

`skills/policy_management/SKILL.md` (52 lines)

```markdown
---
name: policy_management
description: Show the effective expense policy rules and apply user-specified overrides to thresholds. Use when the user asks "what is the meal limit", "show me the expense policy", "change the hotel cap to 200", "our receipt threshold is 50", or wants to know which rules apply before running an audit.
---

# Policy Management Skill

## When to Use

- User asks what a specific limit or threshold is
- User wants to see the full set of rules that will be applied
- User states a company-specific threshold that differs from the default
- User wants to confirm which policy was used for a previous audit

## Workflow

1. Call `get_policy` with no arguments to show the defaults, or with the user's stated
   overrides to show the merged result.
2. Present the effective rules as a table: rule ID, plain-English description, and the
   active value.
3. When an override is applied, state clearly which rule changed, the old value, and the
   new value.

## Important: Overrides Are Session-Scoped

Overrides supplied to `get_policy` apply to the calls you make in this conversation.
They are not persisted to disk. Tell the user this when they set one — the agent has no
policy file and does not remember overrides between sessions.

## Output Format

```
Effective Expense Policy — version 2026.1 (USD)

| Rule                    | Description                                   | Active Value |
|-------------------------|-----------------------------------------------|--------------|
| meal_limit_per_person   | Meals must not exceed $75 per person          | $75.00       |
| hotel_limit_per_night   | Lodging must not exceed $250 per night        | $200.00 *    |
| receipt_required_above  | Receipts required for expenses of $25 or more | $25.00       |
| prohibited_category     | Never reimbursable                            | alcohol, gambling, personal_items, fines |
| submission_window       | Submit within 60 days of the expense date     | 60 days      |
| approval_required_above | Expenses of $500 or more need an approval ID  | $500.00      |
| weekend_non_travel_meal | Weekend non-travel meals need review          | flagged      |

* Overridden in this session (default: $250.00)
```

## Error Handling

- Unknown rule ID in an override: relay the error and list the valid rule IDs
- Non-numeric value for a threshold: ask the user to restate it as a number
- Override that would make a limit zero or negative: point this out and ask for confirmation
  before applying
```

### 2.3 `audit_report`

`skills/audit_report/SKILL.md` (45 lines)

```markdown
---
name: audit_report
description: Generate a deliverable expense audit report for finance, auditors, or management, in Markdown or JSON. Use when the user asks to "generate a report", "export the audit results", "produce a report for finance", or wants audit findings in a shareable format.
---

# Audit Report Skill

## When to Use

- User asks for a report, export, or summary document
- User wants results in a format they can send to another team
- User wants the machine-readable JSON output for further processing

## Before Generating

This skill formats findings; it does not produce them. If the current conversation has no
audit results for the batch in question, run `expense_audit` first.

## Workflow

1. Confirm which format the user wants: Markdown (default, for reading) or JSON (for systems).
   Supply the current time as `batch_metadata.audited_at` — the tool never reads a clock.
2. Call `generate_report` with the audit evaluations, duplicate groups, policy, and batch metadata.
3. Present the report. Do not summarise it away — the user asked for the report itself.

## Report Structure

The report follows `references/report_template.md`, consisting of:

- **Header**: batch file, policy version, audit timestamp, record count
- **Summary**: counts by verdict and by severity
- **Violations**: one section per record, grouped by severity (high → medium → low)
- **Needs Review**: records that could not be fully evaluated, each with the reason
- **Duplicates**: suspected duplicate groups with the matching basis
- **Policy Reference**: the rules applied, so the report stands alone without this conversation
- **Parse Failures**: rows that could not be read at all, so the reader knows the batch was not
  audited in full

## Notes

- The report is a record of an audit, not a decision. Do not add approval or rejection
  language.
- Every violation entry must carry its `rule_id` so a reader can trace it back to the policy.
- Include the total currency amount affected where it can be computed unambiguously.
- If the batch contained parse failures, list the affected rows in the report rather than
  omitting them.
```

---

## 3. Tool Schema

This agent has **no `tools_schema.json`**, and the tool modules contain **no** `parameters` declarations. All schemas are synthesized at runtime by `scripts/run.py:86-98` using `type()`, and all five tools **share the same schema**:

```json
{
  "type": "object",
  "properties": { "params": { "type": "object" } }
}
```

The schema-generation code is as follows:

```python
dynamic_tool = type(
    f"{tool_name.capitalize()}Tool",
    (Tool,),
    {
        "name": tool_name,
        "description": description,          # Uses the first line of the module docstring.
        "parameters": {
            "type": "object",
            "properties": {"params": {"type": "object"}},
        },
        "execute": make_executor(execute_func),
    },
)
```

Each tool's actual parameters and return structure are declared only in the module docstring, reproduced below.

### 3.1 `parse_expenses`

`tools/parse_expenses.py` (367 lines)

```text
parse_expenses: Read a CSV or JSON expense export and normalize records.

Resolves column names through an alias table, converts values to a fixed schema,
and collects unreadable rows instead of aborting the batch. Every record carries
all schema fields; fields that are absent or unparsable become null.
```

```text
Args:
    params: {
        "file_path": str,            # Path to a .csv or .json export
        "column_map": dict | None,   # Explicit {field: source_column} overrides
        "defaults": dict | None      # Values to use for fields absent from the file
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "records": [ <normalized record> ],
            "record_count": int,
            "source_file": str,
            "resolved_columns": {field: source_column_or_None},
            "parse_failures": [{"row": int, "reason": str, "raw": dict}]
        },
        "error": str | None
    }
```

### 3.2 `get_policy`

`tools/get_policy.py` (201 lines)

```text
get_policy: Return the effective expense policy (built-in defaults plus overrides).

The default policy is a module-level constant, not a configuration file: this
module is the single source of truth for every threshold the auditor applies.
Overrides merge per rule and per field, and each change is reported back so a
report can show which values were non-default.
```

```text
Args:
    params: {
        "overrides": dict | None,   # {rule_id: {field: value, ...}, ...}
        "rule_ids": list | None     # Return only these rules (duplicate_detection
                                    # is independent and always returned)
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "version": str,
            "currency": str,
            "rules": [rule],
            "duplicate_detection": {...},
            "overrides_applied": [
                {"rule_id": str, "field": str, "default": Any, "effective": Any}
            ]
        },
        "error": str | None
    }
```

### 3.3 `audit_expenses`

`tools/audit_expenses.py` (556 lines)

```text
audit_expenses: Evaluate expense records against policy rules.

Produces one evaluation per (record, applicable rule) pair, including passes, so
a report can state which rules ran rather than only which failed. Pure function:
no I/O, no clock reads, no randomness.
```

```text
Args:
    params: {
        "records": [ <normalized record from parse_expenses> ],
        "policy": { <effective policy from get_policy> }
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "evaluations": [
                {
                    "record_id": str,
                    "rule_id": str,
                    "rule_description": str,
                    "verdict": "pass" | "violation" | "needs_review",
                    "severity": str,
                    "actual": dict,
                    "limit": Any | None,
                    "overage": float | None,
                    "message": str
                }
            ],
            "record_summary": [
                {
                    "record_id": str,
                    "overall": str,
                    "violation_count": int,
                    "review_count": int
                }
            ],
            "totals": {
                "records": int, "pass": int,
                "violation": int, "needs_review": int
            }
        },
        "error": str | None
    }
```

### 3.4 `detect_duplicates`

`tools/detect_duplicates.py` (229 lines)

```text
detect_duplicates: Find suspected duplicate expense records within a batch.

Groups records that share a submitter and merchant, with amounts inside a
percentage tolerance and dates inside a day window. Grouping is transitive via
union-find, so a chain of near-matches forms a single group. The output is
advisory: it reports suspicion, never a determination that a duplicate exists.
```

```text
Args:
    params: {
        "records": [ <normalized record from parse_expenses> ],
        "policy": { <effective policy from get_policy> }
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "groups": [
                {
                    "group_id": str,
                    "rule_id": str,
                    "merchant": str,
                    "amount": float,
                    "records": [
                        {
                            "record_id": str,
                            "employee_id": str | None,
                            "employee_name": str | None,
                            "expense_date": str | None,
                            "amount": float
                        }
                    ],
                    "matching_basis": {
                        "amount_tolerance_pct": float,
                        "date_window_days": int
                    },
                    "severity": str
                }
            ],
            "duplicate_record_count": int
        },
        "error": str | None
    }
```

### 3.5 `generate_report`

`tools/generate_report.py` (374 lines)

```text
generate_report: Render expense audit results as a Markdown or JSON report.

Pure renderer: the audit timestamp is supplied by the caller rather than read
from the clock, so identical input always produces identical output. The report
records compliance status only and never approves or rejects an expense.
```

```text
Args:
    params: {
        "evaluations": [ <from audit_expenses> ],
        "record_summary": [ <from audit_expenses> ],
        "totals": { <from audit_expenses> },
        "duplicate_groups": [ <from detect_duplicates> ],
        "parse_failures": [ <from parse_expenses> ],
        "policy": { <effective policy from get_policy> },
        "batch_metadata": {
            "source_file": str,
            "audited_at": str,
            "records": [ <normalized record> ]
        },
        "format": "markdown" | "json"
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "report": str,
            "format": "markdown" | "json",
            "summary": {
                "records": int, "pass": int, "violation": int,
                "needs_review": int, "high": int, "medium": int, "low": int
            }
        },
        "error": str | None
    }
```
