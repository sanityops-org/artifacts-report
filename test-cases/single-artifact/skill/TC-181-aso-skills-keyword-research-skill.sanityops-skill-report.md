# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-181-aso-skills-keyword-research-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 1, P1 = 3, P2 = 0 (QD-S: P0 1 / P1 3 / P2 0; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-4.1 - no failure-behavior declaration for a failed research step or unavailable data.
  2. QD-S-1.2 - no upper limit declared on output size for the report.
  3. QD-S-4.2 - no declaration of whether partial completion is acceptable.
  4. QD-S-4.3 - no post-failure prohibited behaviors stated.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed, and it found no code snippets).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-181-aso-skills-keyword-research-skill.md, front matter (lines 13-18): `name: keyword-research`, a `description` and a `metadata` block are present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | the YAML front matter parses (lines 13-18) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description` are strings; `metadata` is a mapping with a string `version` |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Initial Assessment / Research Process 4 phases / Output Format / Tips / Related Skills) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it reads a project context file (`app-marketing-context.md`) and pulls external App Store search data (autocomplete suggestions, competitor rankings, category keywords). This is resource access. No write, deletion or irreversible operation is declared (the skill hands metadata implementation off to a sibling skill), so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: "For implementing keywords into metadata, see metadata-optimization. For auditing current keyword performance, see aso-audit." - the Skill states what it does NOT do and defers it.
- QD-S-1.4 PASS (P1): operations are read-only research/reporting (read a context file, pull ranking data); no write/delete capability is declared.
- QD-S-1.5 PASS (P1): the permitted data sources are declared. Evidence: "Check for `app-marketing-context.md` - read it for app context, competitors, and goals" plus the named research inputs.
- QD-S-2.4 PASS (P1): the verbs are specific ("discover, evaluate, or prioritize App Store keywords"); no broad manage/handle/process verb is used as the capability statement.
- QD-S-5.1 PASS (P1): read-only research; read/modify/delete scopes are not conflated.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: the description enumerates triggers ("keyword research", "find keywords", "search volume", "keyword difficulty", "what keywords should I target").
- QD-S-3.2 PASS (P1): deactivation/routing is declared. Evidence: "For implementing keywords into metadata, see metadata-optimization. For auditing current keyword performance, see aso-audit." - it states when another skill, not this one, applies.
- QD-S-3.6 PASS (P1): `name: keyword-research` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 PASS (P0): an input bound is declared. Evidence: "Ask for **seed keywords** - 3-5 words that describe the app's core function." and "Pull keyword rankings for top 3-5 competitors." bound the number of primary inputs.
- QD-S-3.3 PASS (P1): missing input is handled explicitly. Evidence: "Ask for the **App ID**", "Ask for **target country** (default: US)" - the Skill asks rather than inventing.

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 PASS (P0): the Skill declares no tool-invocation/retry workflow with execution resources; its process is a documented research method (no loop or retry directive is present).
- QD-S-2.1 PASS (P0): no unbounded exhaustive directive. The listing counts are bounded by buckets ("Primary Keywords (3-5)", "Long-tail Keywords (10-20)").
- QD-S-2.2 PASS (P0): no unterminated-execution wording ("keep trying / until success / persist until") present.
- QD-S-5.4 PASS (P1): the downstream skills it hands off to are enumerated (metadata-optimization, aso-audit, competitor-analysis, localization).

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: the report skeleton (summary, top-keywords table, strategy block, competitor gap table, recommendations) declares no bound on the number of keywords or total length.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure-behavior declaration. Evidence: the artifact defines the research process and output format but declares no behavior for a failed research step or unavailable search data, so the post-failure path is undefined.
- QD-S-4.2 FAIL (P1): no declaration of whether partial completion is acceptable. Evidence: the report skeleton uses "[N]" placeholders but states nothing about task-level partial completion.
- QD-S-4.3 FAIL (P1): no post-failure prohibited behaviors are stated. Evidence: the "Tips for the User" are positive guidance; no post-failure prohibition is declared.
- QD-S-5.3 PASS (P1): the operational context is App Store keyword research; no production-destructive environment operation is declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | PASS | evidence: TC-181-aso-skills-keyword-research-skill.md, Initial Assessment - "seed keywords - 3-5 words"
QD-S-1.2 | FAIL | evidence: same file, Output Format - report skeleton with no output-size bound
QD-S-1.3 | PASS | evidence: same file - documented research method; no tool-invocation/retry workflow declared
QD-S-1.4 | PASS | evidence: same file - read-only research/reporting; no write/delete declared
QD-S-1.5 | PASS | evidence: same file, Initial Assessment - "Check for `app-marketing-context.md`"
QD-S-2.1 | PASS | evidence: same file, Phase 4 - keyword buckets bounded ("Primary Keywords (3-5)")
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration marker ("etc.") present
QD-S-2.4 | PASS | evidence: same file, description - specific verbs "discover, evaluate, or prioritize"
QD-S-3.1 | PASS | evidence: same file, description - concrete trigger phrases
QD-S-3.2 | PASS | evidence: same file, description - routing to metadata-optimization / aso-audit
QD-S-3.3 | PASS | evidence: same file, Initial Assessment - asks for App ID, country, seeds
QD-S-3.4 | PASS | evidence: same file, description - defers non-scope tasks to sibling skills
QD-S-3.6 | PASS | evidence: same file, front matter - name `keyword-research` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration for failed research/unavailable data
QD-S-4.2 | FAIL | evidence: same file - no task-level partial-completion statement
QD-S-4.3 | FAIL | evidence: same file - no post-failure prohibited behaviors stated
QD-S-5.1 | PASS | evidence: same file - read-only research; scopes not conflated
QD-S-5.3 | PASS | evidence: same file - App Store research only; no destructive environment operation declared
QD-S-5.4 | PASS | evidence: same file, Related Skills - downstream skills enumerated

### A.4 Defect list (sorted P0 first)

P0 (1): QD-S-4.1
P1 (3): QD-S-1.2, QD-S-4.2, QD-S-4.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact's fenced blocks contain plain-text templates (the Opportunity Score formula and the Title/Subtitle/Keyword-Field character blocks), not programming-language code snippets. There is therefore no embedded code snippet in scope for the QC checklist; QC-0.1-QC-0.5 and QC-1.x-QC-4.x did not execute. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent is available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 1 P0 finding; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own scope boundary is locatable (the routing statements).
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass or constraint-removal statement. The tips and the "avoid promising rankings" guidance are defensive constraints.
- NR-O (obfuscation): no encoded, zero-width or homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The `metadata` block holds only a version string.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no code snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-4.2 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |

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

In-place self-corrections: (1) artifact arrows and em dashes were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are non-CJK; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
