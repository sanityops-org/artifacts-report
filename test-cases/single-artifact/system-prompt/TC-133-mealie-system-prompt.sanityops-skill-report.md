# SanityOps Inspect Lite - Report

Artifact: TC-133-mealie-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; single artifact, no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 4, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.7.3 - no boundary-case examples provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-133-mealie-system-prompt.md` -> **System Prompt** (plain-text instruction prompt). Basis: the case metadata declares Artifact Type = System Prompt; the carried text is the "build recipe" conversion prompt, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: no Tool Schema and no Skill definition accompany the prompt. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the prompt converts one transcribed recipe document into structured recipe data in a single invocation; no state retention, tool invocations, multi-turn dialogue, or complex reasoning are declared. All four L1 criteria are satisfied; L2/L3 criteria are not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-133 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-133 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-133 - the inline examples ("2 cups of onions, chopped"; the "Drain the pasta ..." grouping) are consistent with the rules.
- QD-P-1.2.1 | PASS | evidence: TC-133 - the recipe-conversion role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-133 - the structured-data output style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-133 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-133 - bounded quantifiers only ("each ingredient as a single line", "one or two long steps").
- QD-P-1.3.2 | PASS | evidence: TC-133 - the step-grouping boundary is carried by enumerable triggers (a wait/cooking time begins, a pan is started, the temperature changes, something enters/leaves the oven), so the qualifiers are secondary.
- QD-P-1.3.3 | PASS | evidence: TC-133 - the source document is the declared authority; no unbounded tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-133 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-133 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-133 - the stated behaviors support the recipe-structuring objective.
- QD-P-1.6.1 | PASS | evidence: TC-133 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-133 - no rule keyed on the model's own confidence/intent/motivation state found.
- QD-P-1.6.3 | PASS | evidence: TC-133 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-133 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-133 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-133 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-133 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-133 - input source declared ("The user message contains the transcribed source.").
- QD-P-2.2.2 | FAIL | evidence: TC-133 - no input format/encoding/size limits declared for the transcribed source (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-133 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-133 - sparse-content handling declared; excerpt: "Leave a field empty rather than guessing at it."
- QD-P-2.3.1 | PASS | evidence: TC-133 - the output structure is described (ingredients, instructions, section titles, notes, time fields, nutrition).
- QD-P-2.3.2 | PASS | evidence: TC-133 - the field-level output shape is described inline; no separate structured schema is required.
- QD-P-2.3.4 | FAIL | evidence: TC-133 - no sensitive-data filtering or privacy handling rules declared (absence) for the user-supplied text section.
- QD-P-2.5.2 | FAIL | evidence: TC-133 - no prohibition/security boundary constraints declared (absence).
- QD-P-2.7.1 | PASS | evidence: TC-133 - positive examples are provided (ingredient single-line format; step grouping).
- QD-P-2.7.2 | FAIL | evidence: TC-133 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-133 - no boundary-case examples provided (absence), e.g. an empty or non-recipe source.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-133, prompt block - plain-text content; no code syntax to fail.
- QC-0.2 | PASS | evidence: TC-133 - the fenced block carries an explicit language identifier (`text`).
- QC-0.3 | PASS | evidence: TC-133 - the block is a complete prompt text, not a truncated code fragment.
- QC-0.4 | PASS | evidence: TC-133 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-133 - the declared language (`text`) matches the content.
- QC-1.1, QC-1.2, QC-1.3, QC-1.4 | Not Executed | evidence: TC-133 - no code statements, dependency list, or API version database are present (QC applies to embedded code only).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-133 - no file handles, network connections, or high-risk operations in the prompt text.
- QC-3.1, QC-3.2, QC-3.3 | PASS | evidence: TC-133 - no imports, no missing imports, no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-133 - no embedded snippet conflicts with the owning artifact's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available (only the System Prompt was supplied).

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the artifact ("You convert a transcribed recipe source document into structured recipe data.").
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
No explicitly expressed risk item matching an EX classification was found. The grounding rules ("Do not create, infer, or make up any information", "Leave a field empty rather than guessing at it") and the precedence rule ("that section is authoritative") are constraint statements, not risk expressions; the prompt contains no override, exfiltration, credential or PII value. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Format Compliance, Robustness. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
