# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-177-skills-for-architects-site-visit-report-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 3, P1 = 4, P2 = 0 (QD-S: P0 3 / P1 4 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found; the artifact is a guardrail-heavy reporting contract).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper limit on the number or size of inputs (notes, photos and project files).
  2. QD-S-1.3 - the Skill involves tool invocations but declares no retry count, tool-invocation count or timeout.
  3. QD-S-4.1 - no failure-behavior declaration for a failed or unsatisfiable operation.
  4. QD-S-1.2 - no upper limit declared on output size for the produced report.
  5. QD-S-3.2 - no deactivation conditions declared.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed, and it found no code snippets).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-177-skills-for-architects-site-visit-report-skill.md, front matter (lines 13-24): `name: site-visit-report`, a `description`, and an `allowed-tools` list are present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content; the `allowed-tools` list is populated |
| QD-S-0.3 Syntax Parsability | PASS | the YAML front matter parses (lines 13-24) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description` are strings; `allowed-tools` is a sequence |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found (read-only vs persistent publication is consistently separated) |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (harness compatibility / document ownership / mutation sequence / publication set / promotion boundary) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it uses an `allowed-tools` allowlist (Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion), writes a persistent `site-visit` document plus `DOCUMENTS.csv`, and registers attachments. These are recoverable resource/write operations; no deletion, irreversible action or permission change is declared (the contract explicitly preserves old bytes and forbids silent mutation), so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: "This record does not certify code, life-safety, structural, MEP, accessibility, environmental or contractual compliance; route substantive conclusions to the relevant specialist/professional workflow."
- QD-S-1.4 PASS (P1): permission types are distinguished in substance. Evidence: "Read-only requests and inline drafts need no publication sequence." plus "No silent mutation of PROJECT.md, TASKS.csv or decision records."
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence: "Resolve the project and authorized notes/photos." and "a filename or caption alone is not visual evidence."
- QD-S-2.4 PASS (P1): the capability verbs are specific ("Prepare a sourced site-visit record ..."; "Own authored event documents of kind `site-visit`"); no broad manage/handle/process verb is used as the capability statement.
- QD-S-5.1 PASS (P1): the read-only path is separated from the write path (read guards vs the publication set), so read/modify scopes are distinguished.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation is command-scoped and specific (`/as:site-visit-report`), with a stated output contract; activation is not overly broad.
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the artifact defines the document it owns and what it does not certify, but states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: site-visit-report` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: "Resolve the project and authorized notes/photos." declares no cap on the count or size of notes, photos or project files.
- QD-S-3.3 PASS (P1): ambiguous/missing input is handled by an explicit ask. Evidence: "ask only for material missing information or missing permission."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): involves tool invocations with no declared execution-resource bound. Evidence: "Use the host adapter and available native tools or ordinary task-specific code." declares no retry count, tool-invocation count or timeout.
- QD-S-2.1 PASS (P0): no unbounded quantity directive. The words "every saved original and prepared file", "complete actual bytes" and "the entire affected result" quantify a bounded, artifact-defined set ("the complete site-visit document plus DOCUMENTS.csv and any explicitly authorized attachment registrations"), not an open-ended processing directive.
- QD-S-2.2 PASS (P0): no unterminated-execution wording ("keep trying / until success / persist until") present.
- QD-S-5.4 PASS (P1): chaining is excluded, not left undeclared. Evidence: "no installed library, nested skill invocation, runner or executable reconstruction is required."

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: the report is produced from "the [site template](templates/site-visit-report.md)" with no bound on length or item count.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure-behavior declaration. Evidence: the artifact prescribes a mutation sequence and verification but declares no behavior for a failed tool/write operation, so the post-failure path is undefined.
- QD-S-4.2 FAIL (P1): no declaration of whether partial completion is acceptable. Evidence: "Apply only that verified set." describes the write set but states nothing about task-level partial completion.
- QD-S-4.3 FAIL (P1): no post-failure prohibited behaviors are stated. Evidence: explicit prohibitions ("Do not fabricate ...", "No silent mutation ...") are not framed as post-failure behavior.
- QD-S-5.3 PASS (P1): the operational context is declared as the project workspace (the host contract / workspace model govern), and no production-environment operation is declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-177-skills-for-architects-site-visit-report-skill.md - no input count/size cap on notes/photos/project files
QD-S-1.2 | FAIL | evidence: same file, final body - report produced with no output-size bound
QD-S-1.3 | FAIL | evidence: same file, harness-compatibility paragraph - "available native tools" with no retry/timeout/call-count bound
QD-S-1.4 | PASS | evidence: same file - "Read-only requests and inline drafts need no publication sequence."
QD-S-1.5 | PASS | evidence: same file - "Resolve the project and authorized notes/photos."
QD-S-2.1 | PASS | evidence: same file - "every/complete/entire" quantify the bounded site-visit document set
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration marker ("etc.") present
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Prepare a sourced site-visit record"
QD-S-3.1 | PASS | evidence: same file, heading `/as:site-visit-report` - command-scoped activation
QD-S-3.2 | FAIL | evidence: same file - no statement of when the Skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file - "ask only for material missing information or missing permission."
QD-S-3.4 | PASS | evidence: same file - "This record does not certify code, life-safety, structural, MEP, accessibility, environmental or contractual compliance."
QD-S-3.6 | PASS | evidence: same file, front matter - name `site-visit-report` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration for a failed tool/write operation
QD-S-4.2 | FAIL | evidence: same file - no task-level partial-completion statement
QD-S-4.3 | FAIL | evidence: same file - prohibitions not framed as post-failure behavior
QD-S-5.1 | PASS | evidence: same file - read guards separated from the write publication set
QD-S-5.3 | PASS | evidence: same file - operations confined to the project workspace; no production operation declared
QD-S-5.4 | PASS | evidence: same file - "no ... nested skill invocation ... is required"

### A.4 Defect list (sorted P0 first)

P0 (3): QD-S-1.1, QD-S-1.3, QD-S-4.1
P1 (4): QD-S-1.2, QD-S-3.2, QD-S-4.2, QD-S-4.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no code snippets - its fenced content is absent and the body is prose only. QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute; there are no embedded snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent is available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 3 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own responsibility boundary is locatable ("This record does not certify code, life-safety, structural, MEP, accessibility, environmental or contractual compliance").
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass or constraint-removal statement. The anti-fabrication rule ("Do not fabricate photo identity, location, dates or certainty about concealed conditions") and the "no silent mutation" rule are defensive constraints.
- NR-O (obfuscation): no encoded, zero-width or homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The relative links (`../../docs/...`) are workspace references, not callback endpoints; no NR-S-7 abnormal callback address is present.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no code snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-4.2 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-3.2 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; failure expansion -> Completeness, Coherence, Safety Response.

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

In-place self-corrections: (1) artifact em dashes and the arrow sequence were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are non-CJK; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
