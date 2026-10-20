# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-153-joellewis-finance-skills-asset-allocation-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 9, P2 = 0 (QD-S: P0 4 / P1 9 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared.
  2. QD-S-1.3 - companion-script invocation with no retry count or execution timeout declared.
  3. QD-S-1.1 - no upper bound on the number or size of inputs.
  4. QD-S-4.1 - no execution-failure behavior declared (no handling of insufficient or invalid inputs).
  5. QD-S-1.2 - no output-size limit declared.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-153-joellewis-finance-skills-asset-allocation-skill.md, front matter (lines 13-16): `name: asset-allocation` and `description` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-16) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Core Concepts / Key Formulas / Worked Examples / Common Pitfalls / Cross-References / Running the Script) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it declares and invites execution of a companion script (`uv run scripts/asset_allocation.py`, `python3 scripts/asset_allocation.py`), which is a tool invocation / resource access. It performs no deletion, payment, or permission change, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Determine how to distribute capital across asset classes ..." with no statement of what the skill does NOT do (for example, it does not state that it is not personalized investment advice).
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration.
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration although the body cross-references sibling skills (`historical-risk`, `forward-risk`) as inputs.
- QD-S-2.4 PASS: verbs are specific ("Determine how to distribute capital"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 FAIL (P1): read/write/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: the description enumerates frameworks (mean-variance optimization, Black-Litterman, risk parity, glide paths) and natural-language triggers ("60/40 portfolio", "how much in stocks vs bonds").
- QD-S-3.2 FAIL (P1): no deactivation conditions declared.
- QD-S-3.6 PASS: name `asset-allocation` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input size. Evidence: the skill accepts an arbitrary set of assets and a free-form question with no declared maximum.
- QD-S-3.3 FAIL (P1): no handling declared for incomplete or malformed input (for example, missing risk-aversion or expected-return inputs).

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count, tool-invocation count, or execution timeout declared although the companion script is invoked. Evidence: `uv run scripts/asset_allocation.py`.
- QD-S-2.1 PASS: no unbounded quantity directive (the only "all" usages are mathematical notation "for all i, j").
- QD-S-2.2 PASS: no unterminated-execution wording present.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared (cross-references are documentation links, not invocations).

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared.
- QD-S-2.3 PASS: no open-ended enumeration in the artifact.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no execution-failure behavior declared (no handling when inputs are insufficient or the script run fails).
- QD-S-4.2 FAIL (P1): partial-completion legitimacy not declared.
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-153-joellewis-finance-skills-asset-allocation-skill.md - no input maximum (any number of assets / any query)
QD-S-1.2 | FAIL | evidence: same file - no output-size limit declared
QD-S-1.3 | FAIL | evidence: same file, Running the Script - `uv run scripts/asset_allocation.py` with no retry count or timeout
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | FAIL | evidence: same file, Cross-References - sibling skills referenced as inputs with no data-source boundary
QD-S-2.1 | PASS | evidence: same file - "RC_i = RC_j for all i, j" is mathematical notation, not a processing directive
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration present
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Determine how to distribute capital"
QD-S-3.1 | PASS | evidence: same file, description - enumerated frameworks and natural-language triggers
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | FAIL | evidence: same file - no handling declared for incomplete or malformed input
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter - name `asset-allocation` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no execution-failure behavior declared
QD-S-4.2 | FAIL | evidence: same file - partial-completion legitimacy not declared
QD-S-4.3 | FAIL | evidence: same file - post-failure prohibited behaviors not declared
QD-S-5.1 | FAIL | evidence: same file - read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-3.4, QD-S-4.1
P1 (9): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-3.2, QD-S-3.3, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the bash snippet and the math expressions parse as valid syntax.
QC-0.2 Language Declaration | PASS | evidence: the fenced command blocks carry the `bash` language tag.
QC-0.3 Structural Completeness | PASS | evidence: the snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `uv` / `python3` are external binaries; the math symbols are notation, not code.
QC-1.2 Invalid Import | PASS | evidence: no imports referenced.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | PASS | evidence: no placeholder credentials; example figures are illustrative rates.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 4 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The content is quantitative finance methodology.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, callback addresses, or hardcoded credentials; the example return/volatility numbers are illustrative.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
| QD-S-1.4 | AS-04 Permission/Identity/Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Conditional |
| QD-S-1.5 | AS-01 Instruction/Context Boundary Confusion; AS-03 Output Handling and Sensitive Data Exfiltration; AS-04 | D1, D3 | FM-05, FM-09 | Conditional |
| QD-S-3.2, QD-S-3.3, QD-S-3.4 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
| QD-S-5.1, QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |

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

In-place self-corrections: (1) artifact em dashes were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md.
