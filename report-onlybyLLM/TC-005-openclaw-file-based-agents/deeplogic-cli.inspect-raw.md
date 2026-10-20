# Inspect Report

- **Generated**: 2026-10-20 18:20:35
- **Check level**: L2
- **Status**: completed
- **Execution time**: 291.62s

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

#### TC-005-openclaw-file-based-agents.md

- **Path**: `/Users/a1234/Documents/project/tmp/artifacts-report/test-cases/agent-suite/TC-005-openclaw-file-based-agents.md`
- **Defects**: 2

| Rule | Severity | Line | Description | Fix |
|---|---|---|---|---|
| QC-0.2 | P1 | 140 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |
| QC-0.2 | P1 | 258 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |

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
| Total defects | 18 |
| Severity | P0: 10 / P1: 7 / P2: 1 |
| Gate | FAIL |

## Prompt TC-005-openclaw-file-based-agents.md — completed, score 52.63/100.0, grade C, gate FAIL

| ID | Name | Severity | Description | Location | Impact | Fix |
|---|---|---|---|---|---|---|
| QDP-1.1.1 | Direct Conflict — Core File Type Count | P0 | The inventory title says &#x27;4 core file types&#x27; and Key Features lists only SOUL.md, AGENTS.md, USER.md, and IDENTITY.md, but the Logical Artifact Inventory includes HEARTBEAT.md and MEMORY.md, making the count contradictory. | Logical Artifact Inventory heading / Key Features | The LLM&#x27;s behavior is unpredictable under contradictory instructions; it may choose any one of them, resulting in inconsistent output | Remove one of the conflicting rules, or add a priority declaration specifying which rule takes precedence |
| QDP-2.5.4 | Undefined Constraint Priority | P1 | Multiple routing rule sets and agent constraints apply simultaneously without any precedence or priority, so the LLM cannot determine which routing or boundary takes effect when they conflict. | AGENTS.md - Routing Rules; SOUL.md - Rules &amp; Boundaries | The LLM chooses which constraint to apply on its own and may skip critical constraints | Declare constraint priorities: safety constraints &gt; format constraints &gt; style constraints |
| QDP-1.4.2 | Unreachable Condition / Undeclared Agents | P2 | Intent-Based Routing sends messages to billing-agent, tech-support, and sales-manager, but these agents are not defined in the Agent Registry, so those routing branches and the &#x27;enterprise inquiry&#x27; handoff cannot be executed. | AGENTS.md - Intent-Based Routing / Agent Registry / sales-assistant handoff_rules | Wastes tokens, increases Prompt complexity, and interferes with the LLM&#x27;s understanding of valid conditions | Remove the unreachable conditional branch, or correct the condition so it can be triggered |
| QDP-2.4.2 | Undeclared Resource or Tool | P0 | HEARTBEAT.md invokes fetchTickets, notify, countResolved, getAvgResponseTime, countEscalations, postToSlack, findUsers, and sendEmail without declaring their source, access method, or ownership. | HEARTBEAT.md - Tasks (JavaScript code blocks) | The LLM fails when attempting to use an undeclared resource or fabricates a nonexistent tool | Declare every resource and tool used, along with its access method |
| QDP-1.4.3 | Invalid Skill Definition | P1 | SOUL.md Skills are only one-line declarations with no invocation specification, parameters, or result handling, so they cannot be reliably invoked. | SOUL.md - Skills | The LLM fails or produces erroneous results when attempting to invoke the invalid Skill | Complete the Skill definition and ensure that all required parameters and invocation procedures are fully specified |
| QDP-2.4.3 | Missing Tool-Invocation Specification | P0 | No tool-invocation parameter formats, invocation timing, or result-handling methods are defined for the declared skills or for the messaging channels in AGENTS.md. | SOUL.md - Skills; AGENTS.md - channels/bindings | The LLM uses an incorrect parameter format when invoking a tool or does not know how to process the returned result | Declare the tool-invocation specification: pass ... parameters when invoking it, and extract the ... field from the returned result |
| QDP-1.3.3 | Undefined Boundary / No Task Instruction | P0 | The overall prompt is a descriptive artifact suite but never states the required output, deliverable, or task boundary, so an LLM cannot know whether to evaluate, score, generate tests, or summarize the files. | Prompt overall (before Evaluation Dimensions) | The LLM expands or narrows the task scope on its own and may process content that should not be processed or omit critical steps | State the task boundaries explicitly: process only ..., and do not process ... |
| QDP-2.3.1 | Undefined Output Format | P0 | No output format, structure, or conventions are specified; the Scoring Criteria table has blank Score cells and no instruction to fill them, and no final report schema is defined. | Scoring Criteria / overall prompt | The LLM produces inconsistent output formats that downstream systems cannot parse | Declare the output format: output must be JSON containing the fields title, content, and summary |
| QDP-2.3.2 | Incomplete Output Schema | P0 | The Scoring Criteria table defines dimensions and weights but does not define what each score (1-5) means, how to aggregate partial scores, or what fields the final output must contain. | Scoring Criteria table | The LLM&#x27;s output lacks critical fields or uses incorrect field types, causing downstream processing to fail | Complete the output Schema by defining every required field and its type |
| QDP-2.2.1 | Undeclared Input Source | P0 | No input source or message format is declared for the agent suite; routing rules mention WhatsApp/Telegram/Slack messages but do not define the incoming payload schema or channel event format. | AGENTS.md - Routing Rules | The LLM does not know where to obtain the input and may use an incorrect data source or fabricate input | Declare the input source explicitly: the input comes from the ... section of the user&#x27;s message and is formatted as ... |
| QDP-2.2.2 | Unconstrained Input Format | P0 | The prompt does not constrain message/input format, length, encoding, or character set for any of the declared channels. | AGENTS.md - channels/bindings | The LLM accepts input in any format, potentially causing parsing errors or injection attacks | Declare input format constraints: the input must use UTF-8 encoding and must not exceed 1,000 characters |
| QDP-2.3.4 | Missing Security and Privacy Filtering | P0 | USER.md and MEMORY.md contain personal data and customer insights, but no mechanism is declared to filter PII or prevent sensitive data from being emitted by the agent. | USER.md / MEMORY.md / SOUL.md - Rules &amp; Boundaries | The LLM may disclose sensitive information in its output, such as passwords, personal data, or internal system information | Add a filtering rule: output must not contain sensitive information such as passwords, national identification numbers, or internal system addresses |
| QDP-2.5.2 | Missing Safety-Boundary Constraint | P0 | HEARTBEAT.md performs proactive outreach by sending unsolicited emails and Slack notifications without any consent, opt-out, or confirmation boundary; shell access is only loosely labeled read-only with no prohibited-operation list. | HEARTBEAT.md - Proactive Outreach; SOUL.md - shell skill | The LLM may perform dangerous operations, such as deleting data or accessing unauthorized resources | Add a safety boundary: prohibit deletion, modification, and external-transmission operations, and require user confirmation before high-risk operations |
| QDP-2.5.1 | Missing Termination Constraint | P1 | No termination condition is defined for agent conversations or for the evaluation task, so the LLM does not know when to stop processing. | SOUL.md - Response Guidelines / overall prompt | The LLM may continue indefinitely or terminate prematurely, preventing guaranteed task completion | Add a termination condition: stop after all input items have been processed, or stop after processing at most N items |
| QDP-2.7.2 | Insufficient Negative-Example Coverage | P1 | Only the SOUL.md Tone Examples section contains negative examples; other rule areas such as routing, boundaries, skills, and output have no negative examples covering common errors. | SOUL.md - Tone Examples only; AGENTS.md/MEMORY.md no negative examples | The LLM does not know which behaviors are incorrect and may produce the erroneous output described by the negative examples | Add negative examples that cover common error patterns, and label them as behaviors to avoid |
| QDP-2.7.3 | Missing Boundary-Condition Examples | P1 | No examples cover boundary conditions such as empty input, very long messages, unknown intent, malformed frontmatter, or missing user profile. | Prompt overall / Test Suggestions (only mentions corrupted Markdown runtime test) | The LLM&#x27;s behavior under boundary conditions is unpredictable and may crash or produce erroneous output | Add boundary-condition examples: return an informational message for empty input; truncate excessively long input and notify the user |
| QDP-1.3.2 | Vague Qualifiers in Evaluation Criteria | P1 | Checklist items use vague qualifiers such as &#x27;clear&#x27;, &#x27;reasonable&#x27;, and &#x27;appropriate&#x27; without operational definitions, making evaluation non-reproducible. | Evaluation Dimensions - File Organization Clarity / Markdown Structure | The LLM interprets vague qualifiers inconsistently, causing substantial output variation across calls | Replace vague qualifiers with quantifiable criteria, such as no more than 500 characters or within 30 seconds |
| QDP-2.5.5 | Missing Resource-Invocation Frequency Limit | P1 | No rate limit or frequency cap is declared for skill/tool invocations; HEARTBEAT tasks run once daily, but nested loops or repeated channel calls could overuse resources. | SOUL.md - Skills; HEARTBEAT.md - Tasks | The LLM may invoke resources or tools indefinitely, causing uncontrolled costs or service overload | Add a frequency limit: invoke the tool at most five times, then stop and report if the limit is exceeded |

## Permission — skipped

> [!WARNING]
> **Permission inspection skipped (GATE0_BLOCKED)**: evaluation cannot be performed effectively: Gate-0 pre-check failed: single-artifact check (QD-P / QD-S / QD-T) has an unfixed P0; responsibility boundary statement missing; unable to locate a specific position
> - Blocked by upstream failures: G0-1, G0-3
