# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-147-revealjs-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 5, P1 = 10, P2 = 0 (QD-S: P0 5 / P1 10 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared; the LLM can expand task boundaries on its own.
  2. QD-S-1.1 - no upper bound on the number or size of inputs (slide count, content volume).
  3. QD-S-1.3 - tool invocations (node scripts, npx decktape) with no retry count or execution timeout declared.
  4. QD-S-2.1 - unbounded quantity wording ("review screenshots of EVERY SINGLE SLIDE") with no cap.
  5. QD-S-4.1 - no declared failure behavior; the Dependencies section only states tools "should be already installed".
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-147-revealjs-skill.md, front matter (lines 13-16): `name: revealjs` and `description` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry non-empty content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-16) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (What You Create / Design Principles / Workflow / CSS Components Reference / Advanced Features) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it executes local tooling (`node scripts/create-presentation.js`, `node scripts/check-overflow.js`, `npx decktape`, `npm install puppeteer`) and writes files (presentation.html, styles.css, screenshot folders). These are recoverable resource operations with no deletion, no payment, and no permission change, so it is not L3; it is above L1 because tool invocations occur.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Create polished, professional reveal.js presentations ..." with no statement of what the skill does NOT do.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: the skill runs scripts and writes files with no permission-type or prohibited-operation statement.
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration; the output loads reveal.js from a CDN and Google Fonts / Font Awesome without declaring allowed sources.
- QD-S-2.4 PASS: the capability verb is specific ("Create HTML presentations using reveal.js"); no broad manage/handle/process verb.
- QD-S-5.1 FAIL (P1): the skill writes files (presentation.html, styles.css) but read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: "Use when the user asks to create slides, a presentation, a deck, or a slideshow."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared (no statement of when the skill should NOT trigger).
- QD-S-3.6 PASS: name `revealjs` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input size. Evidence: Step 1 "determine how many slides are needed" sets no maximum slide count or content volume.
- QD-S-3.3 FAIL (P1): no declared handling of incomplete or malformed input. Evidence: Step 1 assumes "the user's content" is available; no insufficient-input branch.

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count, tool-invocation count, or execution timeout declared although the skill runs node scripts, `npx decktape`, and `npm install puppeteer`.
- QD-S-2.1 FAIL (P0): unbounded quantity wording used as a directive. Evidence: "You MUST review screenshots of EVERY SINGLE SLIDE."
- QD-S-2.2 PASS: no unterminated-execution wording ("until success", "keep trying") present.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared. Evidence: the workflow produces a full HTML file plus CSS and a screenshot set with no size cap.
- QD-S-2.3 FAIL (P1): open-ended enumeration present. Evidence: "Use web-safe fonts (Arial, Helvetica, Georgia, Verdana, etc.)".

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no declared failure behavior. Evidence: the Dependencies section states Node.js / Puppeteer "should be already installed" with no fallback if a script fails.
- QD-S-4.2 FAIL (P1): partial-completion legitimacy not declared.
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-147-revealjs-skill.md, Workflow Step 1 - "determine how many slides are needed" with no input maximum
QD-S-1.2 | FAIL | evidence: same file - generates full HTML/CSS plus screenshot sets with no output-size limit
QD-S-1.3 | FAIL | evidence: same file, Workflow Steps 2/5/6 - node scripts and `npx decktape` with no retry count or timeout
QD-S-1.4 | FAIL | evidence: same file - runs scripts / writes files with no read/write/delete distinction
QD-S-1.5 | FAIL | evidence: same file - no permitted/prohibited data sources declared (CDN + Google Fonts loads undeclared)
QD-S-2.1 | FAIL | evidence: same file, Workflow Step 6 - "review screenshots of EVERY SINGLE SLIDE" (unbounded)
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | FAIL | evidence: same file, Design Principles - "Arial, Helvetica, Georgia, Verdana, etc." (open-ended enumeration)
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Create polished, professional reveal.js presentations"
QD-S-3.1 | PASS | evidence: same file, description - enumerated trigger phrases (slides, presentation, deck, slideshow)
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | FAIL | evidence: same file - no handling declared for incomplete or malformed input
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter - name `revealjs` consistent with the description
QD-S-4.1 | FAIL | evidence: same file, Dependencies - tools listed as "should be already installed" with no failure handling
QD-S-4.2 | FAIL | evidence: same file - partial-completion legitimacy not declared
QD-S-4.3 | FAIL | evidence: same file - post-failure prohibited behaviors not declared
QD-S-5.1 | FAIL | evidence: same file - writes files but no read/write/delete scope distinction
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (5): QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-3.4, QD-S-4.1
P1 (10): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-3.2, QD-S-3.3, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the bash, CSS, HTML, JS, and JSON snippets parse as valid syntax for their languages.
QC-0.2 Language Declaration | PASS | evidence: fenced blocks carry language tags (`bash`, `css`, `html`, `javascript`).
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent (full CSS blocks, full initialize object).
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `Reveal` is a documented external library global; `node`, `npx` are external binaries.
QC-1.2 Invalid Import | PASS | evidence: no imports referenced.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connection objects in the snippets (CDN links are HTML attributes).
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | PASS | evidence: no placeholder credentials; hex strings are color values only.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 5 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The workflow text is design and presentation guidance.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, abnormal callback addresses, or hardcoded credentials. The Google Fonts and reveal.js CDN URLs are ordinary asset loads, not callback/endpoint fields, so NR-S-7 does not apply.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
| QD-S-1.4 | AS-04 Permission/Identity/Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-1.5 | AS-01 Instruction/Context Boundary Confusion; AS-03 Output Handling and Sensitive Data Exfiltration; AS-04 | D1, D3 | FM-05, FM-09 | Conditional |
| QD-S-2.1, QD-S-2.3 | AS-06; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Medium |
| QD-S-3.2, QD-S-3.3, QD-S-3.4 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 | AS-07 | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
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

In-place self-corrections: (1) artifact text containing emoji markers and em/en dashes was paraphrased or rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are rendered as ASCII hyphens to satisfy the zero-non-ASCII output contract; (3) no fabricated rule IDs were emitted (all QD-S IDs are from skill-checklist.md).
