# Inspect Report

- **Generated**: 2026-10-20 19:07:04
- **Check level**: L1
- **Status**: completed
- **Execution time**: 381.62s

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
| Total defects | 3 |
| Severity | P0: 1 / P1: 2 / P2: 0 |
| Gate | FAIL |

## Prompt TC-111-salesgpt-system-prompt.prompt.txt — completed, score 89.22/100.0, grade B, gate FAIL

| ID | Name | Severity | Description | Location | Impact | Fix |
|---|---|---|---|---|---|---|
| QDP-1.1.1 | Direct Conflict | P0 | The first-turn rule instructs the salesperson to only greet the prospect and ask how they are doing (&#x27;without pitching&#x27;), while the Introduction stage rule requires introducing the salesperson and company and always clarifying the reason for the call in the greeting. These cannot both be followed on the first turn. | &#x27;Start the conversation by just a greeting and how is the prospect doing without pitching in your first turn.&#x27; vs &#x27;1: Introduction... Always clarify in your greeting the reason why you are calling.&#x27; | The LLM&#x27;s behavior is unpredictable under contradictory instructions; it may choose any one of them, resulting in inconsistent output | Remove one of the conflicting rules, or add a priority declaration specifying which rule takes precedence |
| QDP-1.3.2 | Vague Qualifier | P1 | &#x27;short length&#x27; is not operationalized; the prompt does not specify a word count, sentence count, or other objective measure, so the required response length is ambiguous. | &#x27;Keep your responses in short length to retain the user&#x27;s attention.&#x27; | The LLM interprets vague qualifiers inconsistently, causing substantial output variation across calls | Replace vague qualifiers with quantifiable criteria, such as no more than 500 characters or within 30 seconds |
| QDP-2.3.1 | Undefined Output Format | P1 | The prompt does not define how the &lt;END_OF_CALL&gt; token should be formatted in relation to the required response format. It is unclear whether the final output should consist solely of the token, include it in the salesperson line, or append it after a Thought line. | &#x27;When the conversation is over, output &lt;END_OF_CALL&gt;&#x27; vs &#x27;you MUST use the format: Thought: ... {salesperson_name}: [your response here]&#x27; | The LLM produces inconsistent output formats that downstream systems cannot parse | Declare the output format: output must be JSON containing the fields title, content, and summary |

## Permission — skipped

> [!WARNING]
> **Permission inspection skipped (GATE0_BLOCKED)**: evaluation cannot be performed effectively: Gate-0 pre-check failed: single-artifact check (QD-P / QD-S / QD-T) has an unfixed P0; responsibility boundary statement missing; unable to locate a specific position
> - Blocked by upstream failures: G0-1, G0-3
