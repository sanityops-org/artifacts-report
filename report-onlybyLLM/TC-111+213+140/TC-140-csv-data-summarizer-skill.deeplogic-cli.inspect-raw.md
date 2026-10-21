# Inspect Report

- **Generated**: 2026-10-20 18:43:13
- **Check level**: L2
- **Status**: completed
- **Execution time**: 97.74s

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
| Total defects | 16 |
| Severity | P0: 5 / P1: 11 / P2: 0 |
| Gate | FAIL |

## Skill csv-data-summarizer — completed, score 20.55/100.0, grade D, gate FAIL

| ID | Name | Severity | Description | Location | Impact | Fix |
|---|---|---|---|---|---|---|
| QDS-1.1 | Missing input-count limit | P0 | The skill declares no maximum number of rows, columns, or file size, so it will process entire CSV files and can overflow context/token limits. | Skill metadata and Automatic Analysis Steps: &#x27;Load and inspect the CSV file into pandas DataFrame&#x27; | The LLM processes all submitted content without truncation; if the user submits 500 items, it processes all 500, causing token overflow and uncontrolled cost | Add a limit: &#x27;Process at most 50 items. If more are provided, process the first 50 and notify the user.&#x27; |
| QDS-1.2 | Missing output-size limit | P1 | The skill requires comprehensive output and multiple visualizations but declares no output-size bound, which can overflow the context window. | Automatic Analysis Steps: &#x27;Generate comprehensive output automatically&#x27; and Example Output | The response size explodes and overflows the context window, and the LLM may generate extremely long output | Add: &#x27;Limit output to 1,500 Chinese characters or 1,000 English words.&#x27; |
| QDS-1.3 | Missing execution-resource boundaries | P0 | No max_retries, max_tool_calls, or timeout are declared, so the LLM may retry or run tools without limit. | Skill metadata and Files section | The LLM retries or calls tools without limit, with every retry or call consuming tokens and time | Add: &#x27;Maximum retries: 3. Timeout: 60 seconds. Maximum tool calls per execution: 10.&#x27; |
| QDS-1.4 | Missing permission boundaries | P1 | The skill does not explicitly declare read/write/delete permissions; it only implies analysis, leaving broader operations unconstrained. | Description: &#x27;Analyzes CSV files, generates summary stats, and plots quick visualizations&#x27; | The LLM interprets a broad capability description such as &#x27;manage data&#x27; as implicit authorization for every operation, including DELETE | List explicitly: &#x27;Allowed: read and list. Prohibited: write, delete, update, and overwrite.&#x27; |
| QDS-1.5 | Missing data-source boundaries | P1 | The skill does not declare permitted or prohibited data sources, so the LLM may read arbitrary file paths or external data. | Usage: &#x27;Accepts a path to a CSV file&#x27; | The LLM gathers data from conversation history, external systems, or other Skills on its own | Declare: &#x27;Use only data explicitly provided in the current request. Do not access conversation history or external systems.&#x27; |
| QDS-2.1 | Unbounded comprehensive analysis and output | P0 | Instructs the LLM to &#x27;Run the comprehensive analysis&#x27; and &#x27;Generate ALL relevant visualizations/charts&#x27; without any upper-bound constraint, leading to exhaustive processing. | Critical Behavior Requirement and Automatic Analysis Steps sections | The LLM attempts exhaustive processing; &#x27;process all files&#x27; means the LLM tries to process every single file | Replace &#x27;all&#x27; with &#x27;at most N items,&#x27; or add an explicit upper bound after the unbounded term. |
| QDS-3.2 | Missing non-activation conditions | P1 | The skill does not specify when it should not trigger, so it may activate for any CSV-related mention (e.g., a quick column rename or a CSV format question) and run an unwanted full analysis. | When to Use This Skill / trigger conditions | The LLM forcibly activates the Skill in borderline scenarios and executes unrelated operations | Add: &#x27;Do not activate for debugging, code review, or system-administration requests.&#x27; |
| QDS-3.3 | No ambiguous-input handling policy | P1 | There is no policy for missing file paths or unparseable input; the &#x27;DO NOT ASK THE USER&#x27; instruction could cause the LLM to fabricate data instead of requesting the CSV. | How It Works - CRITICAL BEHAVIOR REQUIREMENT / Usage | The LLM fills in missing input itself and may fabricate content, producing incorrect results | Add: &#x27;When input is incomplete or ambiguous, ask the user instead of guessing.&#x27; |
| QDS-3.4 | Missing non_goals | P0 | The skill does not declare what it does not do, allowing scope creep beyond CSV summarization into data cleaning, transformation, or modeling. | Skill description / top-level metadata | The LLM expands the task boundary to matters it considers reasonably related and executes operations beyond the intended scope | Add a &#x27;Does not do&#x27; section: &#x27;Does not infer from conversation history, add facts that were not provided, or expand into related tasks.&#x27; |
| QDS-3.6 | Inaccurate capability description | P1 | Notes claim visualizations are generated only when date columns exist, but the analysis steps also create histograms, heatmaps, and category charts; this contradiction misleads expected behavior. | Notes - &#x27;Generates visualizations only when date columns are present&#x27; | The LLM misunderstands the Skill&#x27;s capabilities during the trigger stage, causing subsequent behavior to diverge from expectations | Rename it to describe the capability accurately, such as &#x27;readonly-database-diagnostic&#x27; instead of &#x27;database-maintenance-assistant.&#x27; |
| QDS-4.1 | No failure-handling policy | P0 | Skill instructs automatic comprehensive analysis but does not define stop, retry, report, or escalate behavior for failures such as missing files, parse errors, or empty data. | Skill Content / How It Works / Automatic Analysis Steps | The LLM explores alternative paths on its own, making its behavior unpredictable and potentially creating greater risk | Add: &#x27;If execution fails, stop immediately and report the error. Do not attempt alternatives.&#x27; |
| QDS-4.2 | Partial completion acceptability not declared | P1 | Skill demands complete analysis and forbids follow-up questions, but does not declare whether partial results are acceptable if full analysis cannot be completed. | Skill Content / How It Works / Behavior Guidelines | The LLM insists on completeness and enters an endless iteration cycle, consuming large amounts of tokens and time | Add: &#x27;Partial results are acceptable. When information is insufficient for a section, skip it or mark it as insufficient.&#x27; |
| QDS-4.3 | No prohibited post-failure behaviors | P1 | Skill does not explicitly prohibit scope expansion or fabricated data after failure, allowing the LLM to lower standards or invent insights when analysis fails. | Skill Content / How It Works / Behavior Guidelines | After a failure, the LLM lowers its standards or broadens the search scope and may fabricate data or execute unauthorized operations | Add: &#x27;After a failure, do not expand the task scope, fabricate data to fill gaps, or lower quality standards.&#x27; |
| QDS-5.1 | Missing explicit read/write permissions | P1 | The skill does not explicitly distinguish read, write, update, or delete permissions, leaving the LLM to infer an implicit operational boundary. | description; Usage: summarize_csv(file_path) | The LLM interprets DELETE as a reasonable data operation and may execute destructive operations | List explicitly: &#x27;Allowed: read, list, and query. Prohibited: write, update, delete, insert, and DROP.&#x27; |
| QDS-5.3 | No environment boundary declaration | P1 | The skill does not declare whether operations are restricted to local/sandbox environments or prohibit production/external/third-party targets. | description; Automatic Analysis Steps; Usage | The LLM treats production environments, external networks, cloud storage, or third-party services as valid operation targets | Add: &#x27;Do not access production databases, production APIs, live systems, or unauthorized external services. Use only local, test, or sandbox environments.&#x27; |
| QDS-5.4 | Missing chained-invocation permissions | P1 | The skill does not declare permitted or prohibited downstream Skills/tools, creating risk of indirect high-privilege operations. | metadata.dependencies; Automatic Analysis Steps | A low-privilege Skill indirectly reaches high-privilege operations by invoking another Skill, creating a privilege-escalation chain | Add: &#x27;May invoke only skill-A and skill-B. Invocation of skill-C, which has administrator privileges, is prohibited.&#x27; |

## Permission — skipped

> [!WARNING]
> **Permission inspection skipped (GATE0_BLOCKED)**: evaluation cannot be performed effectively: Gate-0 pre-check failed: single-artifact check (QD-P / QD-S / QD-T) has an unfixed P0; responsibility boundary statement missing; unable to locate a specific position
> - Blocked by upstream failures: G0-1, G0-3
