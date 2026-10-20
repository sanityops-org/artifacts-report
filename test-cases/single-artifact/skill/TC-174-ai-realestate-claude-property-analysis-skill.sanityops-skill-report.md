# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-174-ai-realestate-claude-property-analysis-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 2, P1 = 7, P2 = 0 (QD-S: P0 2 / P1 6 / P2 0; embedded-code QC: 1 finding, QC-0.2 P1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound on the number or size of inputs.
  2. QD-S-1.3 - the Skill launches WebSearch and five parallel subagents but declares no retry count, tool-invocation count or execution timeout.
  3. QD-S-2.3 - open-ended enumeration present ("SFR, Condo, Multi-family, etc.").
  4. QD-S-1.4 / QD-S-5.1 - no read/write/delete permission-type distinction for the WebSearch calls, the subagent dispatch and the written report file.
  5. QC-0.2 - fenced blocks (WebSearch/Task/formula snippets) carry no language identifier.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed; QC-1.x-QC-4.x did not run because the QC-0 gate did not pass).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-174-ai-realestate-claude-property-analysis-skill.md, front matter (lines 14-29): identifier `skill: realestate-analyze`, display `name: Full Property Analysis Orchestrator`, and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | required fields carry content; `version`, `triggers`, `tags`, `author` are populated |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 14-29) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`skill`/`version`/`author` are strings; `triggers`/`tags` are sequences |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Execution Flow x3 phases / Output Template / Error Handling / Performance Notes) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill performs resource access - it calls `WebSearch`, launches five parallel subagents via `Task`, and writes a report file to disk - but all declared operations are recoverable (search, analysis, and a written markdown report); no deletion, irreversible action, or permission change is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: the disclaimer "For educational/research purposes only. Not financial or investment advice. Always consult licensed real estate professionals." (repeated in the frontmatter body, every subagent prompt, and the footer) declares what the Skill does NOT do and defers the decision to a licensed professional.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration for the `WebSearch` calls, the `Task` subagent dispatch, and the written report file (`PROPERTY-ANALYSIS-[ADDRESS].md`).
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence: data is sourced from `WebSearch` and user-supplied details ("If WebSearch returns no listing data, inform the user and ask them to provide property details manually"), with "Always disclose data limitations in the report."
- QD-S-2.4 PASS (P1): no broad manage/handle/process verb is used as the capability statement; the capability is specific ("produce a comprehensive property analysis with composite Property Score (0-100), investment grade, and actionable recommendations").
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: explicit `triggers` list ("/realestate analyze", "full property analysis", "analyze property", "property report").
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the artifact lists positive triggers only; no statement of when the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: Full Property Analysis Orchestrator` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs. Evidence: the Skill accepts an address (and falls back to user-supplied property details) with no declared cap on the number or size of inputs.
- QD-S-3.3 PASS (P1, optional): ambiguous/missing input is handled. Evidence: "If any critical data point is missing after discovery, note it as 'Not Available' and instruct subagents to work with what is known."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): execution resource boundary missing. Evidence: the Skill launches `WebSearch` and five parallel `Task` subagents ("launch all 5 agents simultaneously") but declares no retry count, tool-invocation count, or execution timeout.
- QD-S-2.1 PASS (P0): no unbounded quantity directive used as an execution instruction.
- QD-S-2.2 PASS (P0): no unterminated-execution wording present.
- QD-S-5.4 PASS (P1): the downstream subagents are explicitly enumerated (`realestate-comps`, `realestate-rental`, `realestate-neighborhood`, `realestate-invest`, `realestate-market`), which declares the invoked scope.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on total output size. Evidence: the Output Template fixes sections but states no total-size bound for the assembled report.
- QD-S-2.3 FAIL (P1): open-ended enumeration present. Evidence: the core profile table lists "Property Type | SFR, Condo, Multi-family, etc."

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): failure behavior is declared. Evidence: the "Error Handling" section - "If a subagent fails or times out, note the missing section in the report and score only available dimensions".
- QD-S-4.2 PASS (P1): degradation paths are declared. Evidence: "score only available dimensions"; "If fewer than 3 comps are found, flag the Comps Score as 'Low Confidence'".
- QD-S-4.3 PASS (P1): post-failure prohibitions are declared. Evidence: "note it as 'Not Available'" rather than inventing values; "Always disclose data limitations in the report."

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-174-ai-realestate-claude-property-analysis-skill.md, Phase 1 - inputs accepted with no cap on number or size
QD-S-1.2 | FAIL | evidence: same file, Output Template - no bound on total output size
QD-S-1.3 | FAIL | evidence: same file, Phase 2 - "launch all 5 agents simultaneously using `Task`" with no retry/timeout/call-count bound
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Error Handling - "ask them to provide property details manually"; data limitations disclosed
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording used as an execution instruction
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | FAIL | evidence: same file, Step 1.2 table - "Property Type | SFR, Condo, Multi-family, etc."
QD-S-2.4 | PASS | evidence: same file, description - specific capability statement
QD-S-3.1 | PASS | evidence: same file, front matter - explicit triggers ("/realestate analyze", "full property analysis")
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Phase 1 - "note it as 'Not Available' and instruct subagents to work with what is known"
QD-S-3.4 | PASS | evidence: same file, DISCLAIMER - "Not financial or investment advice. Always consult licensed real estate professionals."
QD-S-3.6 | PASS | evidence: same file, front matter - name consistent with the description
QD-S-4.1 | PASS | evidence: same file, Error Handling - "If a subagent fails or times out, note the missing section ..."
QD-S-4.2 | PASS | evidence: same file - "score only available dimensions"
QD-S-4.3 | PASS | evidence: same file, Error Handling - "Always disclose data limitations in the report."
QD-S-5.1 | FAIL | evidence: same file - read/write/delete scopes not distinguished (report file written)
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file, Phase 2 - downstream subagents explicitly enumerated

### A.4 Defect list (sorted P0 first)

P0 (2): QD-S-1.1, QD-S-1.3
P1 (6): QD-S-1.2, QD-S-1.4, QD-S-2.3, QD-S-3.2, QD-S-5.1, QD-S-5.3
P2 (0): none
Embedded-code QC (1): QC-0.2 (P1).

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds fenced snippets: a `WebSearch` illustration, five `Task(...)` prompt templates, and a composite-score formula block (the case notes them as prompt templates, not executable source), plus a `markdown`-tagged output template. QC-0 was run first.

QC-0.1 Syntax Parsability | PASS | evidence: the `WebSearch(...)` / `Task(...)` blocks are illustrative pseudo/prompt snippets; per the illustrative-snippet rule they are exempt from the parse-completeness requirement.
QC-0.2 Language Declaration | FAIL | evidence: the `WebSearch` block, the five `Task(...)` blocks and the composite-score block are fenced with a bare ``` and carry no language identifier.
QC-0.3 Structural Completeness | PASS | evidence: illustrative snippets; per the illustrative-snippet rule they are exempt from the standalone-parse requirement.
QC-0.4 Fence Integrity | PASS | evidence: every code fence opens and closes correctly.
QC-0.5 Language-Content Mismatch | PASS | evidence: the one tagged block (`markdown`) contains markdown, consistent with its tag.
QC-0 gate: FAIL (QC-0.2, P1). Per the entry gate, QC-1 through QC-4 were NOT executed.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 2 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own disclaimer boundary is locatable in the frontmatter body, each subagent prompt, and the footer.
- G0-4 (each Tool Schema's name/description/parameter descriptions are complete): NOT satisfied - the artifact set contains no Tool Schema.

Result: Gate-0 Not passed - G0-4 (no Tool Schema present in the artifact set; per-Tool name/description/parameter completeness cannot be verified).

## Stage D - Permission proportionality (QD-PM)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - incomplete artifact set (a full set requires System Prompt + Skill + all Tool Schemas; only a single Skill is present).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.
Nothing else is reported for Permission - no defect list, no score, no partial conclusions. (Permission did not execute due to Gate-0 not satisfied.)

## Stage E - Risk Explicit (EX)  [separate from the Inspect verdicts]

Static scan of the Skill description and body across the EX families (NL-A, NL-B, NR-O, NR-S) found no expression matching an EX subcategory:
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The repeated disclaimer and the "mark missing data 'Not Available'" rule are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The `Task(...)` parameter values are prompt templates and placeholder tokens (`[ADDRESS]`, `[PRICE]`), not secrets, callbacks or dangerous defaults.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it did not pass its gate, so QC-1.x-QC-4.x did not run either); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.4, QD-S-5.1, QD-S-5.3 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-2.3 | AS-06 Resource Exhaustion and Runaway Execution; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Conditional |
| QD-S-3.2 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |
| QC-0.2 | no candidate mapping defined in relevance-map.md (the map covers QD-* defect IDs only) | - | - | - |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability.

These lines are candidate associations only ("may", "needs dynamic verification"); they do not indicate that the backend is exploitable. v1 scope: single-defect mapping only; defect chains are out of scope.

## Status board

Stage A (Single-artifact):  Executed - single Skill inspected (QD-S + embedded-code QC)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 qualifying risk items
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - report self-checked

## Stage G - Self-verification (report self-check, not a verdict on the artifact)

Self-verification: ID back-closure OK - red-line wording OK - output contract OK

In-place self-corrections: (1) artifact dashes and arrows were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, all QC IDs are present in code-contract-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
