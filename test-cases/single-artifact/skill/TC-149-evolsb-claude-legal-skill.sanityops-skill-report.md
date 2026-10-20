# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-149-evolsb-claude-legal-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 0, P1 = 2, P2 = 1 (QD-S: P0 0 / P1 2 / P2 1; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound declared on the number or size of input documents.
  2. QD-S-1.2 - no output-size limit declared.
  3. QD-S-3.2 - no deactivation conditions declared (note: the "When to Activate" section lists positive triggers only).
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-149-evolsb-claude-legal-skill.md, front matter (lines 13-17): `name: contract-review`, `description`, `version: 3.0.0` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-17) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description` strings; `version` a quoted string |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (When to Activate / Step 1 / Step 2 / Output Format / Red Flags / Checklists / Risk Categories / Benchmarks / Guardrails) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L1 (Low Risk).
Basis: the Skill is an analytical text-processing methodology - it reviews a user-supplied contract and produces a markdown report. It declares no tool, script, or external-system invocation and performs no state-changing or irreversible operation; it is therefore text-processing only.
Applied rule set: the L1 minimum rule set = 6 mandatory items (QD-S-1.1, 1.2, 2.1, 3.4, 4.1, 3.6) plus 3 optional items (QD-S-3.1, 3.2, 3.3).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS: a non_goals / scope boundary is declared. Evidence: Guardrails "Not legal advice", "Not tax advice".

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: "User mentions 'review contract', 'analyze agreement', 'check this contract'".
- QD-S-3.2 FAIL (P2): no deactivation conditions declared; the "When to Activate" section lists only positive triggers.
- QD-S-3.6 PASS: name `contract-review` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P1): no upper limit on input size. Evidence: the skill accepts one or more "PDF/DOCX legal document" inputs with no declared maximum count or size.
- QD-S-3.3 PASS: ambiguous-input handling is declared. Evidence: Step 2 "Ask if unclear: 'Which party are you?'".

EXECUTION (boundaries, retries, tool calls, chained calls)
- Not applicable at L1 beyond the mandatory items; no tool invocation or chained call is declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared for the generated review.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: deficiency handling is declared. Evidence: Step 1 "If blank fields or missing exhibits exist, flag prominently in output header" and Guardrails "Express uncertainty".

### A.3 Full L1 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-149-evolsb-claude-legal-skill.md, When to Activate - "User uploads or references a PDF/DOCX legal document" with no input maximum
QD-S-1.2 | FAIL | evidence: same file - the example review has no output-size limit
QD-S-2.1 | PASS | evidence: same file, Step 1 - "List all referenced schedules/exhibits" is bounded to a single document; no unbounded processing directive
QD-S-3.4 | PASS | evidence: same file, Guardrails - "Not legal advice", "Not tax advice"
QD-S-4.1 | PASS | evidence: same file, Step 1 + Guardrails - flag incomplete documents prominently; "Express uncertainty"
QD-S-3.6 | PASS | evidence: same file, front matter - name `contract-review` consistent with the description
QD-S-3.1 | PASS | evidence: same file, When to Activate - enumerated trigger phrases
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Step 2 - "Ask if unclear: 'Which party are you?'"

### A.4 Defect list (sorted P0 first)

P0 (0): none
P1 (2): QD-S-1.1, QD-S-1.2
P2 (1): QD-S-3.2

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact contains one fenced block - a ```markdown example-review template (prose deliverable), not executable code; there are no code snippets to inspect.
QC-0.1 Syntax Parsability | N/A | evidence: the single fenced block is a markdown template, not a code snippet.
QC-0.2 Language Declaration | N/A | evidence: no code block requires a language tag.
QC-0.3 Structural Completeness | N/A | evidence: no code snippet present.
QC-0 gate: not applicable (no embedded code snippets). QC-1 through QC-3: not applicable. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 0 P0 findings; recorded (no P0 to carry forward).
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
- NL-A / NL-B (natural language): the checklist items (for example "Pre-signed conflict waivers", "Class action waiver", "Offshore jurisdiction") are contract features the skill analyzes, not risk instructions issued by the skill. No data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, callback addresses, or hardcoded credentials; the example figures ($120K / $30K) are illustrative amounts.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-3.2 | AS-01 Instruction/Context Boundary Confusion; AS-04 Permission/Identity/Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition.

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

In-place self-corrections: (1) artifact em dashes and check glyphs were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md.
