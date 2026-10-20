# SanityOps Inspect Lite - Report

Artifact: TC-112-vane-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 6, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-1.3.2 - vague qualifiers ("as needed", "where appropriate").
  - QD-P-1.6.2 - behavior keyed on the model's own vagueness judgment.
  - QD-P-2.2.2 - no input format constraints declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Stage A - System Prompt inspection (QD-P)

Tier determination: L1 (Single-turn Task). Basis: the writer prompt receives a context block, system instructions, and a mode, and produces a single cited answer; no tool invocations, no multi-turn state, and no complex reasoning are declared. L1 criteria satisfied; L2/L3 criteria not met.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-112, getWriterPrompt - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-112 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-112, Citation Requirements / Example Output - examples consistent with rules.
- QD-P-1.2.1 | PASS | evidence: TC-112 - role supports the writing/citation task.
- QD-P-1.2.2 | PASS | evidence: TC-112, Formatting Instructions - output style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-112 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-112 - no quantifier scope error found ("every sentence" is a bounded per-sentence rule).
- QD-P-1.3.2 | FAIL | evidence: TC-112, Formatting Instructions / Special Instructions - vague qualifiers used; excerpt: "Include a concluding paragraph that synthesizes the provided information or suggests potential next steps, where appropriate".
- QD-P-1.3.3 | PASS | evidence: TC-112 - behavior is bounded by the provided context and mode; no tool/permission/handoff scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-112 - citation requirements are consistently stated, not a duplicate-constraint defect.
- QD-P-1.4.2 | PASS | evidence: TC-112 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-112 - stated behavior supports the answer-generation objective.
- QD-P-1.6.1 | PASS | evidence: TC-112 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | FAIL | evidence: TC-112, Special Instructions - a rule is keyed on the model's own judgment; excerpt: "If the user provides vague input or if relevant information is missing, explain what additional details might help refine the search".
- QD-P-1.6.3 | PASS | evidence: TC-112 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-112 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-112 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-112 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-112 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-112, getWriterPrompt - input sources declared (the user's query and the injected context).
- QD-P-2.2.2 | FAIL | evidence: TC-112 - no input query format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-112 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-112, Special Instructions - missing-input handling declared; excerpt: "If the user provides vague input or if relevant information is missing, explain what additional details might help refine the search".
- QD-P-2.3.1 | PASS | evidence: TC-112, Formatting Instructions - output format declared (Markdown, headings, bullets).
- QD-P-2.3.2 | PASS | evidence: TC-112 - free-text output with declared structure; no structured schema required.
- QD-P-2.3.4 | FAIL | evidence: TC-112 - no sensitive-data filtering or privacy handling rules declared (absence) for web-context content.
- QD-P-2.5.2 | FAIL | evidence: TC-112 - no prohibition/security boundary constraints declared (absence).
- QD-P-2.7.1 | PASS | evidence: TC-112, Example Output - a positive example structure is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-112 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-112 - no boundary-case examples provided (absence), beyond the no-info fallback sentence.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-112, getWriterPrompt block - the TypeScript template snippet parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-112 - fenced block carries explicit language identifier (`typescript`).
- QC-0.3 | PASS | evidence: TC-112 - snippet is a structurally parseable template function.
- QC-1.1..1.4, QC-2.1..2.3, QC-3.1..3.3 | PASS | evidence: TC-112 - the embedded TypeScript is a prompt-template function; interpolations (context, systemInstructions, mode) are runtime inputs, not hardcoded credentials; no file handles, network connections, or hardcoded secrets detected.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in getWriterPrompt.
- G0-4 (each Tool Schema name/description/parameter descriptions complete): FAIL - no Tool Schema is supplied; field-by-field completeness cannot be verified.
- Gate-0 result: Not passed - G0-4.

## Stage D - Permission proportionality (QD-PM, Quick Mode)
Not Executed - incomplete artifact set (Gate-0 G0-4 unsatisfied; no Tool Schema supplied).

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - no Tool Schema supplied; operation semantics undeterminable; permission items cannot be categorized.
Remediation Actions: Fix above upstream items, then re-run Gate-0

(Wording note: the Permission stage was "Not Executed" because Gate-0 was not satisfied; it is not reported as FAIL and no ERROR/BLOCKED status is asserted.)

## Stage E - Risk Explicit (EX) - physically separated from Inspect verdicts
Scan scope: System Prompt static text (NL-A / NL-B / NR-O / NR-S).
Findings: none.
No explicitly expressed risk item matching an EX classification was found in the artifact text. The explicit priority statement ("give them less priority than the above instructions") subordinates user instructions to system rules; it is an anti-override constraint, not a risk expression. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
