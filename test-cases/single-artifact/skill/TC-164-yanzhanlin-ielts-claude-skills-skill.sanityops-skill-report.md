# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-164-yanzhanlin-ielts-claude-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 0, P1 = 3, P2 = 0 (QD-S: P0 0 / P1 3 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper limit declared on input number or size (word minimums are declared, no maximum).
  2. QD-S-1.2 - no upper limit declared on output size (the rewrite produces a full target-score essay plus the whole report).
  3. QD-S-4.1 - no execution-failure behavior declared anywhere in the Skill.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-164-yanzhanlin-ielts-claude-skills-skill.md, front matter (lines 15-22): `name: ielts-writing` and a multiline `description` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (block-scalar `description`, nested `metadata.version`) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description` are strings; `metadata.version` is a string |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found (the "does not write essays" boundary and the "rewrite for comparison" phase are explicitly distinguished) |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (SOUL / three modes / prompt-analysis / correction with five phases / practice / calibration / boundary) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L1 (Low Risk).
Basis: per the checklist's risk-level semantics, L1 = text-processing only, no tool invocations. This Skill scores, annotates and rewrites essays as prose. It declares no tool invocation, no external system access, no live data read/write, and no sensitive-data handling. Therefore L1 applies.
Applied rule set: the L1 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.2, QD-S-2.1, QD-S-3.4, QD-S-4.1, QD-S-3.6) + 3 optional items (QD-S-3.1, QD-S-3.2, QD-S-3.3). Items outside this set are out of lite scope for an L1 Skill and are not emitted.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence (translated from the original Chinese): "You do not write essays for the user -- you correct, diagnose, and rewrite"; the boundary section also routes non-writing requests to sibling skills.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1, optional): activation conditions are concrete. Evidence (translated): triggers such as "/ielts-writing", "correct my essay", "help me look at this one", "analyze the prompt", "writing practice", plus a three-mode input-to-behavior table.
- QD-S-3.2 PASS (P2, optional): deactivation is declared via the boundary section, which routes overall planning, reading and speaking requests away to sibling skills (so the skill is not triggered for them).
- QD-S-3.6 PASS (P1): `name: ielts-writing` and the description (four-dimension scoring / sentence-level annotation / rewrite comparison / prompt analysis) are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P1): no upper limit on input number or size. Evidence (translated): the skill states word minimums ("Task 1 >= 150, Task 2 >= 250") but declares no maximum on the size or count of submitted material.
- QD-S-3.3 PASS (P1, optional): ambiguous/incomplete input is routed by the mode table (topic only -> prompt-analysis mode; topic + essay -> correction mode; "give me a question" -> practice mode).

EXECUTION (boundaries, retries, tool calls, chained calls)
- No L1 execution items apply (QD-S-1.3 and QD-S-5.4 are outside the L1 set). No tool invocation or chained call is declared, consistent with the L1 determination.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence (translated): "Phase 4 - Rewrite comparison" rewrites the user's essay into a target-score version and then a full report is produced, with no declared bound on output length.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P1): no failure behavior declared. Evidence (translated): the artifact closes on a "scoring calibration reminder" and a "boundary" list and contains no execution-failure handling declaration anywhere (no rule for a failed or unsatisfiable request).

(Additional L1 item carried here for completeness)
- QD-S-2.1 PASS (P1): no unbounded exhaustive-processing directive. Evidence (translated): "mark every part that must be answered" is bounded by the parts of the exam prompt; no "all / every / entire / complete" wording is used as an unbounded execution instruction.

### A.3 Full L1 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-164-yanzhanlin-ielts-claude-skills-skill.md, body (translated) - word minimums are declared ("Task 1 >= 150, Task 2 >= 250") but no maximum input is declared
QD-S-1.2 | FAIL | evidence: same file, "Phase 4 - Rewrite comparison" (translated) - rewrites the essay into a target-score version plus a full report with no output-size bound
QD-S-2.1 | PASS | evidence: same file - no unbounded exhaustive-processing wording used as an execution instruction
QD-S-3.1 | PASS | evidence: same file, description - concrete triggers ("/ielts-writing", "correct my essay", "writing practice") plus a three-mode table
QD-S-3.2 | PASS | evidence: same file, "Boundary" section (translated) - sibling skills to route to (does not do overall planning / reading / speaking)
QD-S-3.3 | PASS | evidence: same file - the mode table handles input-state ambiguity
QD-S-3.4 | PASS | evidence: same file, "Boundary" section (translated) - "You do not write essays for the user -- you correct, diagnose, and rewrite"
QD-S-3.6 | PASS | evidence: same file, front matter - name `ielts-writing` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no execution-failure-behavior declaration present

### A.4 Defect list (sorted P0 first)

P0 (0): none
P1 (3): QD-S-1.1, QD-S-1.2, QD-S-4.1
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no executable code snippets. Its fenced blocks are illustrative Markdown output templates (the four-dimension scoring report format, the sentence-level annotation example) and one plain-text structure outline; these are not code. QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute - there are no code snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 0 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own "Boundary" section is locatable in this artifact.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The "does not write essays" rule and the boundary routing are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The named third-party scoring tools are public product names, not secrets.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; failure expansion -> Completeness, Coherence, Safety Response.

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

In-place self-corrections: (1) all CJK artifact text (the original SKILL.md is Chinese-first) was rendered as English translations and marked as translations, per the zero-CJK contract; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
