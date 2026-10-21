# Inspect Report

- **Generated**: 2026-10-20 18:52:10
- **Check level**: L2
- **Status**: failed
- **Execution time**: 487.92s

## Code Contract Inspection (QC Lint)

> Code Contract inspection runs BEFORE LLM-based defect check, using pure AST parsing and pattern matching (no LLM required).

| Metric | Value |
|---|---|
| Total artifacts | 1 |
| Total defects | 2 |
| P0 (blocking) | 0 |
| P1 (warning) | 2 |
| P2 (advisory) | 0 |
| QC Gate | PASS |
| Inspection time | 0.00s |

### Prompts

#### TC-111-salesgpt-system-prompt.prompt.txt

- **Path**: `/Users/a1234/Documents/project/tmp/artifacts-report/report-onlybyLLM/TC-111+213+140/artifacts/TC-111-salesgpt-system-prompt.prompt.txt`
- **Defects**: 2

| Rule | Severity | Line | Description | Fix |
|---|---|---|---|---|
| QC-0.2 | P1 | 24 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |
| QC-0.2 | P1 | 32 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |

### QC Rule Reference

| Rule ID | Name | Severity | Description |
|---|---|---|---|
| QC-0.1 | Syntax Parsability | P0 | Code snippet parses as valid syntax for its declared language |
| QC-0.2 | Language Declaration | P1 | Code block has explicit language identifier |
| QC-0.3 | Structural Completeness | P1 | Code snippet is complete enough for standalone parsing |
| QC-1.1 | Undefined Name Reference | P1 | Uses class/function/variable not defined in snippet or standard library |
| QC-1.4 | Type Mismatch | P2 | Function argument types clearly incompatible |
| QC-2.1 | Unclosed File Handle | P1 | File opened without corresponding close or with statement |
| QC-2.2 | Unreleased Network Connection | P2 | HTTP/socket connection opened without explicit close or context manager |
| QC-2.3 | Missing Exception Handling | P2 | High-risk operation without try-catch |
| QC-3.1 | Unused Import | P2 | Module imported but never referenced |
| QC-3.2 | Missing Import | P1 | Module referenced but never imported |
| QC-3.3 | Hardcoded Demo Value | P2 | Uses placeholder/demo values that may be mistaken for production |

## Summary

| Metric | Value |
|---|---|
| Total defects | 0 |
| Severity | P0: 0 / P1: 0 / P2: 0 |
| Gate | PASS |

## Prompt TC-111-salesgpt-system-prompt.prompt.txt — failed

> [!CAUTION]
> **Prompts inspection failed (INSPECTION_FAILED)**: Request timed out or interrupted. This could be due to a network timeout, dropped connection, or request cancellation. See https://docs.anthropic.com/en/api/errors#long-requests for more details.

## Permission — skipped

> [!WARNING]
> **Permission inspection skipped (GATE0_BLOCKED)**: evaluation cannot be performed effectively: Gate-0 pre-check failed: responsibility boundary statement missing; unable to locate a specific position
> - Blocked by upstream failures: G0-3
