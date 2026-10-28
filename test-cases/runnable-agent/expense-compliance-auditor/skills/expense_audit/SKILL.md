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