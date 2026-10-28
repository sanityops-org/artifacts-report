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