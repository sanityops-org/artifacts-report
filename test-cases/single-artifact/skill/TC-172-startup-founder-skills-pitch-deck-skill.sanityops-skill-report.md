# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-172-startup-founder-skills-pitch-deck-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 3, P1 = 7, P2 = 0 (QD-S: P0 3 / P1 7 / P2 0; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound on the number or size of inputs.
  2. QD-S-1.3 - the Skill chains to another Skill but declares no retry count, tool-invocation count or execution timeout.
  3. QD-S-4.1 - no failure behavior declared.
  4. QD-S-5.4 - chained invocation of the pptx Skill declared without a permitted/prohibited downstream scope.
  5. QD-S-1.4 / QD-S-5.1 - no read/write/delete permission-type distinction for the context-file read and the downstream deck build.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-172-startup-founder-skills-pitch-deck-skill.md, front matter (lines 13-18): `name: pitch-deck` and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content; `related` and `reads` lists are populated |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-18) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description` are strings; `related`/`reads` are sequences |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (When to Use / Context Required / Workflow / Output Format / Frameworks / Related Skills / Examples) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - the workflow reads a system context artifact ("Read startup context - Pull from `.agents/startup-context.md`") and hands off to another Skill ("chain to the Anthropic pptx skill"), which produces a `.pptx` file. These are resource operations (resource access plus a chained Skill invocation). No deletion, irreversible action, or permission change is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: the workflow states "If the user wants a `.pptx`, chain to the Anthropic pptx skill after content is finalized" (the Skill does not itself produce the deck file), and the body scopes the stage to seed / Series A; the "Related Skills" section hands backup materials to `data-room` and outreach to `fundraising-email`.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration for the context-file read or the downstream pptx chain.
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence: "From `startup-context`: company one-liner, stage, ... If any of these are missing, prompt the founder before drafting slides." and "From the user: target round size, target investor type ...".
- QD-S-2.4 PASS (P1): verbs are specific ("create, review, or restructure a fundraising pitch deck"); no broad manage/handle/coefficient verb is used as the capability statement.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: description "Also activates when the user mentions 'deck', 'pitch', 'investor presentation', or 'slide structure'."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the "When to Use" list gives positive conditions only; no statement of when the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: pitch-deck` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs. Evidence: the Skill accepts a company context and a deck scope with no declared cap on the number or size of inputs.
- QD-S-3.3 PASS (P1, optional): insufficient-context handling is declared. Evidence: "If any of these are missing, prompt the founder before drafting slides."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): execution resource boundary missing. Evidence: the workflow chains to the pptx Skill ("chain to the Anthropic pptx skill after content is finalized") but declares no retry count, tool-invocation count, or execution timeout.
- QD-S-2.1 PASS (P0): no unbounded quantity directive (sets are bounded: "10-12 slides", "no more than 3 fonts and 2 brand colors").
- QD-S-2.2 PASS (P0): no unterminated-execution wording present.
- QD-S-5.4 FAIL (P1): chained invocation of another Skill declared without a permitted/prohibited downstream Skill scope. Evidence: "chain to the Anthropic pptx skill after content is finalized" names no downstream-scope whitelist or prohibition.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): output is bounded per slide and by slide count. Evidence: "live-pitch deck (visual-heavy, 30-40 words per slide max) or a send-ahead deck ... 60-80 words per slide"; the framework enumerates "the 10-12 slide framework".
- QD-S-2.3 PASS (P1): no open-ended enumeration present ("e.g." is used only to illustrate a required style, not as an open structural list).

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure behavior declared. Evidence: the workflow ends at "Produce final output - Deliver the deck outline as structured markdown"; no execution-failure handling declaration appears anywhere.
- QD-S-4.2 FAIL (P1): no declaration of whether partial completion is acceptable.
- QD-S-4.3 FAIL (P1): no post-failure prohibited-behavior declaration.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-172-startup-founder-skills-pitch-deck-skill.md, Context Required - inputs accepted with no cap on number or size
QD-S-1.2 | PASS | evidence: same file, Workflow step 2 - "30-40 words per slide max" / "60-80 words per slide"; 10-12 slide bound
QD-S-1.3 | FAIL | evidence: same file, Workflow step 6 - "chain to the Anthropic pptx skill" with no retry/timeout/call-count bound
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Context Required - "From `startup-context`: ..." and "From the user: ..."
QD-S-2.1 | PASS | evidence: same file - bounded sets ("10-12 slides"; "no more than 3 fonts and 2 brand colors")
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration ("etc." / "and others")
QD-S-2.4 | PASS | evidence: same file, description - specific verbs "create, review, or restructure"
QD-S-3.1 | PASS | evidence: same file, description - concrete triggers ("deck", "pitch", "investor presentation", "slide structure")
QD-S-3.2 | FAIL | evidence: same file, When to Use - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Context Required - "prompt the founder before drafting slides"
QD-S-3.4 | PASS | evidence: same file, Workflow step 6 - "chain to the Anthropic pptx skill after content is finalized"
QD-S-3.6 | PASS | evidence: same file, front matter - name `pitch-deck` consistent with the description
QD-S-4.1 | FAIL | evidence: same file, Workflow step 6 - no failure-behavior declaration present
QD-S-4.2 | FAIL | evidence: same file - no partial-completion-legitimacy declaration
QD-S-4.3 | FAIL | evidence: same file - no post-failure prohibited-behavior declaration
QD-S-5.1 | FAIL | evidence: same file - read/write/delete scopes not distinguished (`.pptx` build chained downstream)
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | FAIL | evidence: same file, Workflow step 6 - downstream pptx Skill chained with no declared scope

### A.4 Defect list (sorted P0 first)

P0 (3): QD-S-1.1, QD-S-1.3, QD-S-4.1
P1 (7): QD-S-1.4, QD-S-3.2, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no code snippets (the worked output is a Markdown blockquote, and other content is prose, tables and lists; there are no fenced code blocks). QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute - there are no embedded snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 3 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own stage/handoff boundary is locatable in the description and the Related Skills section.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The anti-vanity-metrics guidance ("Vanity metrics; hiding the Y-axis") and "No fabricated financial promises" posture are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The front-matter `reads: [startup-context]` and `related: [...]` values are ordinary Skill-name references, not secrets or callback addresses.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-1.4, QD-S-5.1, QD-S-5.3 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.4 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects; AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3 | FM-05, FM-09 | Medium |
| QD-S-3.2, QD-S-4.2, QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability; failure expansion -> Completeness, Coherence, Safety Response.

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
