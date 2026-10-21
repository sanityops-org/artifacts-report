# Inspect Report

- **Generated**: 2026-10-20 18:40:56
- **Check level**: L2
- **Status**: completed
- **Execution time**: 226.59s

## Code Contract Inspection (QC Lint)

> Code Contract inspection runs BEFORE LLM-based defect check, using pure AST parsing and pattern matching (no LLM required).

| Metric | Value |
|---|---|
| Total artifacts | 1 |
| Total defects | 0 |
| P0 (blocking) | 0 |
| P1 (warning) | 0 |
| P2 (advisory) | 0 |
| QC Gate | PASS |
| Inspection time | 0.00s |

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
| Total defects | 3 |
| Severity | P0: 3 / P1: 0 / P2: 0 |
| Gate | FAIL |

## Tool firecrawl_agent — completed, score 78.26/100.0, grade B, gate FAIL

| ID | Name | Severity | Description | Location | Impact | Fix |
|---|---|---|---|---|---|---|
| QD-T-1.1 | Missing core fields | P0 | &#x27;parameters.type&#x27; must be &#x27;object&#x27; | $.parameters.type | The Agent cannot invoke the Tool correctly | Add the missing required fields and ensure that name, description, and inputSchema are complete |
| QD-T-1.1 | Missing core fields | P0 | The tool schema declares &#x27;parameters&#x27; as an empty object and does not define the required inputSchema/parameter properties. It omits all declared call parameters mentioned in the description, such as prompt, schema, urls, mode, exchange, effort, maxCredits, and strictConstrainToURLs. A complete parameter schema or inputSchema is required. | $.parameters | The Agent cannot invoke the Tool correctly | Add the missing required fields and ensure that name, description, and inputSchema are complete |
| QD-T-3.2 | Raw input passthrough | P0 | The tool accepts unstructured user-supplied instructions via &#x27;prompt&#x27; and passes them to a backend research agent. With no input schema or validation, raw user input can reach the backend directly, allowing prompt injection, unintended web navigation, or unconstrained agent actions. | $.parameters | Users can manipulate Tool parameters through prompt injection, creating a security risk | Use parameterized, predefined query conditions to avoid passing through raw input |

## Permission — skipped

> [!WARNING]
> **Permission inspection skipped (GATE0_BLOCKED)**: evaluation cannot be performed effectively: Gate-0 pre-check failed: single-artifact check (QD-P / QD-S / QD-T) has an unfixed P0; responsibility boundary statement missing; unable to locate a specific position
> - Blocked by upstream failures: G0-1, G0-3
