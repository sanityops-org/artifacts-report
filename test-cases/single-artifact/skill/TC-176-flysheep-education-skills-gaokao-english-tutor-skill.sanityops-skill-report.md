# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-176-flysheep-education-skills-gaokao-english-tutor-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

> Language note: the inspected artifact is written in Chinese. Per the skill output contract, every evidence excerpt below is rendered in English as a translation and marked "(translated)". No CJK characters are emitted in this report.

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 1, P1 = 3, P2 = 1 (QD-S: P0 1 / P1 3 / P2 1; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found; the artifact is a defensive tutoring persona).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared (the "Absolutely must not do" list forbids pedagogical style, not out-of-scope tasks).
  2. QD-S-1.1 - no upper limit on the number or size of inputs (a student may submit any number/length of passages or essays).
  3. QD-S-1.2 - no upper limit on output size for open-ended tutoring deliverables.
  4. QD-S-4.1 - no failure-behavior declaration for a failed or unsatisfiable request.
  5. QD-S-3.2 - no deactivation conditions declared.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed, and it found no code snippets).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-176-flysheep-education-skills-gaokao-english-tutor-skill.md, front matter (lines 13-16): `name: gaokao-english-tutor` and a `description` are present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | the YAML front matter parses (lines 13-16) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | the description emphasizes ability, question technique and vocabulary; the body's "comprehension first, technique second" principle and its closing "ability, not exam technique" line are reconcilable role framing, not a mutual contradiction |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Teaching principles / Teaching flow / Question-type guidance / Grammar topics / Handling cases / Language style / Do-and-Do-not / Exam norms / Conclusion) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L1 (Low Risk).
Basis: per the checklist's risk-level semantics, L1 = text-processing only, no tool invocations. This Skill is a tutoring persona that explains, guides and corrects English answers as prose; it declares no tool invocation, no external system access, no file/data write, and no sensitive-data handling. No delete or irreversible operation is declared, so L3 does not apply.
Applied rule set: the L1 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.2, QD-S-2.1, QD-S-3.4, QD-S-4.1, QD-S-3.6) + 3 optional items (QD-S-3.1, QD-S-3.2, QD-S-3.3). Items outside this set are out of lite scope for an L1 Skill and are not emitted.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: the description scopes the Skill to English tutoring ("simulate a senior-year English tutor, tutoring reading comprehension, cloze, grammar fill-in and writing" - translated), but the body never states what tasks the Skill does NOT perform (e.g. declining non-English subjects). The "Absolutely must not do" list (translated) forbids pedagogical style only ("do not only teach techniques and neglect comprehension"; "do not give the answer without the process"), which is not a task-scope boundary.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1, optional): activation conditions are concrete. Evidence: "use when the student asks an English question, requests a grammar explanation, analyses a reading passage, or asks to revise an essay" (translated).
- QD-S-3.2 FAIL (P2, optional): no deactivation conditions declared. Evidence: the artifact lists activation triggers but states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: gaokao-english-tutor` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P1): no upper limit on input number or size. Evidence: the Skill accepts any English question, passage or essay to review with no cap on count or length declared.
- QD-S-3.3 PASS (P1, optional): the flow asks the student for missing information rather than inferring. Evidence: "first, read the question/passage; mark the words you do not know" (translated) - a guided clarification step.

EXECUTION (boundaries, retries, tool calls, chained calls)
- No L1 execution items apply (QD-S-1.3 and QD-S-5.4 are outside the L1 set). No tool invocation or chained call is declared, consistent with the L1 determination.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: the five-step flow and the per-question-type guidance ("summarise the method for this question type: 1. step one; 2. step two; 3. note" - translated) declare no bound on output length.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P1): no failure behavior declared. Evidence: the "Handling different situations" section (translated) adapts teaching to a student's level ("insufficient vocabulary", "weak grammar", "slow answering"), but declares no behavior for an execution failure or an unsatisfiable request (e.g. a non-English or off-topic request), so the LLM's post-failure path is undefined.

(Additional L1 items carried here for completeness)
- QD-S-2.1 PASS (P1): no unbounded exhaustive-processing directive. The phrase "grasp the whole text" (translated) and "summarise the common test points" describe teaching completeness, not a quantity directive over an unbounded set.

### A.3 Full L1 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-176-flysheep-education-skills-gaokao-english-tutor-skill.md, whole body - no input count/size cap declared for questions, passages or essays
QD-S-1.2 | FAIL | evidence: same file, Teaching flow - five-step output with no size bound
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording ("all/every/entire/complete") used as an execution directive
QD-S-3.1 | PASS | evidence: same file, description - concrete triggers ("asks an English question", "requests a grammar explanation") (translated)
QD-S-3.2 | FAIL | evidence: same file - no statement of when the Skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Teaching flow step 1 - guided clarification ("read it once, mark the words you do not know") (translated)
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration; the "Absolutely must not do" list is pedagogical style, not scope
QD-S-3.6 | PASS | evidence: same file, front matter - name `gaokao-english-tutor` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration (the "Handling different situations" section adapts teaching, not failure handling)

### A.4 Defect list (sorted P0 first)

P0 (1): QD-S-3.4
P1 (3): QD-S-1.1, QD-S-1.2, QD-S-4.1
P2 (1): QD-S-3.2

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact's fenced blocks contain natural-language dialogue templates (Chinese prose prompts), not programming-language code snippets. There is therefore no embedded code snippet in scope for the QC checklist; QC-0.1-QC-0.5 and QC-1.x-QC-4.x did not execute. Note: the fenced templates carry no language identifier, but since they are prose, not code, the QC scope ("code snippets embedded in Logic Artifacts") is not triggered. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent is available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 1 P0 finding; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass or constraint-removal statement. The "Absolutely must not do" list and the closing reminders (translated) are defensive pedagogy constraints.
- NR-O (obfuscation): no encoded, zero-width or homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. No structured fields other than the front-matter metadata.
- NR-S-9 / NR-S-10: no plaintext sensitive values or personal data values are embedded in the artifact.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no code snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-3.4 | AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-02, FM-07, FM-09 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
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

In-place self-corrections: (1) all Chinese evidence was rendered in English and marked "(translated)" to satisfy the zero-CJK contract; (2) the EX domain-prefix separator and the status-board dash are non-CJK; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
