# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-170-onewave-ai-claude-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 0, P1 = 4, P2 = 1 (QD-S: P0 0 / P1 4 / P2 1; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound on the number or size of contract inputs.
  2. QD-S-1.2 - no upper bound on output size for the analysis report.
  3. QD-S-4.1 - no failure behavior declared for the review workflow.
  4. QD-S-3.3 - no handling declared for incomplete or malformed contract input.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-170-onewave-ai-claude-skills-skill.md, front matter (lines 13-16): `name: contract-analyzer` and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-16) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Contents map + numbered Workflow) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L1 (Low Risk).
Basis: per the checklist's risk-level semantics, L1 = text-processing only, no tool invocations. This Skill reads contract text and produces an informational analysis report as prose; it dispatches only to four bundled reference files (`references/key-terms.md`, `risk-flags.md`, `output-template.md`, `examples.md`) that are part of its own instruction set. It declares no external system access, no live data read/write, and no sensitive-data handling. Therefore L1 applies.
Applied rule set: the L1 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.2, QD-S-2.1, QD-S-3.4, QD-S-4.1, QD-S-3.6) + 3 optional items (QD-S-3.1, QD-S-3.2, QD-S-3.3). Items outside this set are out of lite scope for an L1 Skill and are not emitted.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: workflow step 1 fixes the mandatory disclaimer "This is informational analysis only, not legal advice. Always consult with a qualified attorney for legal matters. Contract interpretation can be complex and jurisdiction-specific." This statement declares what the Skill does NOT do (it does not provide legal advice and defers to a qualified attorney), so a non_goals boundary is present.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1, optional): activation conditions are concrete. Evidence: description "Use when user needs contract review, legal document analysis, or agreement evaluation."
- QD-S-3.2 FAIL (P2, optional): no deactivation conditions declared. Evidence: the artifact enumerates trigger intents ("contract review, legal document analysis, or agreement evaluation") but states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: contract-analyzer` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P1): no upper limit on the number or size of inputs. Evidence: the workflow accepts a contract of any length or count ("Identify the contract type ... Extract key terms ...") and declares no cap on the number or size of documents supplied.
- QD-S-3.3 FAIL (P1, optional): no handling declared for incomplete or malformed input. Evidence: the workflow declares no behavior for a malformed, truncated, or non-contract input (it proceeds straight from "Identify the contract type" onward).

EXECUTION (boundaries, retries, tool calls, chained calls)
- No L1 execution items apply (QD-S-1.3 and QD-S-5.4 are outside the L1 set). No tool invocation or chained call is declared, consistent with the L1 determination.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: workflow step 8 "Format the report per `references/output-template.md`" declares no bound on total output length or item count.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P1): no failure behavior declared. Evidence: the 8-step workflow ends at "Format the report per `references/output-template.md`. For worked examples and best practices, see `references/examples.md`." and contains no execution-failure handling declaration anywhere (no rule for a failed or unsatisfiable review).

(Additional L1 items carried here for completeness)
- QD-S-2.1 PASS (P1): no unbounded exhaustive-processing directive. The phrase "across financial, duration/termination, intellectual property, liability/indemnification, and other critical categories" is a bounded category list tied to `references/key-terms.md`, not a quantity directive; no "all / every / entire / complete" quantity wording is used as an execution instruction.

### A.3 Full L1 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-170-onewave-ai-claude-skills-skill.md, Workflow - contract input accepted with no cap on number or size
QD-S-1.2 | FAIL | evidence: same file, Workflow step 8 - "Format the report per `references/output-template.md`" with no output-size bound
QD-S-2.1 | PASS | evidence: same file - no exhaustive quantity wording ("all/every/entire/complete") used as an execution instruction
QD-S-3.1 | PASS | evidence: same file, description - "contract review, legal document analysis, or agreement evaluation"
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | FAIL | evidence: same file, Workflow - no handling declared for incomplete or malformed contract input
QD-S-3.4 | PASS | evidence: same file, Workflow step 1 - "This is informational analysis only, not legal advice. Always consult with a qualified attorney"
QD-S-3.6 | PASS | evidence: same file, front matter - name `contract-analyzer` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration present (closes on the report-format step only)

### A.4 Defect list (sorted P0 first)

P0 (0): none
P1 (4): QD-S-1.1, QD-S-1.2, QD-S-3.3, QD-S-4.1
P2 (1): QD-S-3.2

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no code snippets (its body is prose and lists only; there are no fenced code blocks). QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute - there are no embedded snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 0 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own legal-safety boundary is locatable at the disclaimer (Workflow step 1).
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The mandatory "not legal advice" disclaimer and the "consult a qualified attorney" instruction are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The four named `references/*.md` paths are ordinary relative documentation paths, not callback or secret values.

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
| QD-S-3.3 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |
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

In-place self-corrections: (1) artifact dashes were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
