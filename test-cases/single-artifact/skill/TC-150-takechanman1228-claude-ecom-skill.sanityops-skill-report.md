# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-150-takechanman1228-claude-ecom-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 3, P1 = 3, P2 = 0 (QD-S: P0 3 / P1 3 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared.
  2. QD-S-1.1 - no upper bound on the input CSV (row count / file size).
  3. QD-S-1.3 - engine invocation with no retry count or execution timeout declared.
  4. QD-S-3.2 - no deactivation conditions declared.
  5. QD-S-5.3 - no environment boundary declared.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-150-takechanman1228-claude-ecom-skill.md, front matter (lines 14-33): `name`, `description`, `when_to_use`, `argument-hint`, `allowed-tools` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses; the folded scalars and the list value for `allowed-tools` are valid |
| QD-S-0.4 Field Type Validity | PASS | `name` string; `allowed-tools` a YAML list |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Mode Selection / Input / Running the Engine / Workflow / Report Contract / Data Rules / Quality Gates) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it runs a bundled Python engine (`ecom review ...`, or the bundled launcher), bootstraps a private venv, and writes output files (`REVIEW.md`, `REVIEW_{PERIOD}.md`, `review.json`). These are recoverable resource operations with no deletion, payment, or permission change, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Ecommerce business review for D2C stores from order transaction CSVs ..." with no statement of what the skill does NOT do.
- QD-S-1.4 PASS: the permitted operations are declared and scoped. Evidence: `allowed-tools: Read, Grep, Glob, Write, Bash(ecom *)`.
- QD-S-1.5 PASS: a data-source boundary is declared. Evidence: "review.json only. All numbers MUST come from review.json ... Never reference external sources (Shopify Analytics, GA, ...)".
- QD-S-2.4 PASS: verbs are specific ("Ecommerce business review", "interpret the results"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 PASS: read vs write are distinguished in `allowed-tools` (Read, Write) and the shell is scoped to `Bash(ecom *)`.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: `when_to_use` enumerates "ecommerce review", "store health", "how was last month", "why did revenue drop".
- QD-S-3.2 FAIL (P1): no deactivation conditions declared (no statement of when the skill should NOT trigger).
- QD-S-3.6 PASS: name `ecom` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input size. Evidence: "Order transaction CSV. Each row = one order or line item." with no row-count or file-size maximum.
- QD-S-3.3 PASS: ambiguous-input handling is declared. Evidence: "If no CSV is specified, Glob for `*.csv` ... and ask the user if multiple plausible candidates exist".

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count or execution timeout declared although the engine is invoked. Evidence: "The first run bootstraps a private Python venv ... and may take a minute" with no timeout or retry bound.
- QD-S-2.1 PASS: no unbounded quantity directive; output counts are capped ("5-7 findings max").
- QD-S-2.2 PASS: no unterminated-execution wording present.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS: an output-size limit is declared. Evidence: "Target ~150 lines total; 5-7 findings max across all periods".
- QD-S-2.3 PASS: no open-ended enumeration in the artifact.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: fallback behavior is declared. Evidence: "If `ecom` is not on PATH, use the bundled launcher"; "Incomplete Data: Omit what you can't measure."
- QD-S-4.2 PASS: partial-completion legitimacy is declared. Evidence: "Omit what you can't measure. No N/A, no empty sections".
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-150-takechanman1228-claude-ecom-skill.md, Input - order CSV with no row-count or size maximum
QD-S-1.2 | PASS | evidence: same file, Report Contract - "Target ~150 lines total; 5-7 findings max"
QD-S-1.3 | FAIL | evidence: same file, Running the Engine - engine invocation with no retry count or timeout
QD-S-1.4 | PASS | evidence: same file, front matter - `allowed-tools: Read, Grep, Glob, Write, Bash(ecom *)`
QD-S-1.5 | PASS | evidence: same file, Data Rules - "review.json only ... Never reference external sources"
QD-S-2.1 | PASS | evidence: same file - findings counts capped (5-7 max); no unbounded quantity directive
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration present
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Ecommerce business review"
QD-S-3.1 | PASS | evidence: same file, when_to_use - enumerated triggers
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Input - Glob then "ask the user if multiple plausible candidates exist"
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter - name `ecom` consistent with the description
QD-S-4.1 | PASS | evidence: same file - bundled-launcher fallback; "Omit what you can't measure"
QD-S-4.2 | PASS | evidence: same file, Incomplete Data - "Omit what you can't measure. No N/A, no empty sections"
QD-S-4.3 | FAIL | evidence: same file - post-failure prohibited behaviors not declared
QD-S-5.1 | PASS | evidence: same file, front matter - Read and Write distinguished in `allowed-tools`
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (3): QD-S-1.1, QD-S-1.3, QD-S-3.4
P1 (3): QD-S-3.2, QD-S-4.3, QD-S-5.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the bash invocation snippets parse as valid syntax.
QC-0.2 Language Declaration | PASS | evidence: the fenced blocks carry the `bash` language tag.
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `ecom` is the skill's own CLI; `$ARGUMENTS`, `<output-dir>` are placeholders.
QC-1.2 Invalid Import | PASS | evidence: no imports referenced.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | PASS | evidence: no placeholder credentials present.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 3 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The data-integrity rules ("Never reference external sources", "Never expose internal check IDs") are risk-reducing constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, callback addresses, or hardcoded credentials.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
| QD-S-3.2, QD-S-3.4 | AS-01 Instruction/Context Boundary Confusion; AS-04 Permission/Identity/Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
| QD-S-5.3 | AS-04; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; failure expansion -> Completeness, Coherence, Safety Response; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability.

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

In-place self-corrections: (1) artifact em dashes and marker glyphs were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md.
