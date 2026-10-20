# SanityOps Inspect Lite - Report

Artifact: TC-135-search-with-lepton-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 5, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-1.3.2 - vague qualifier ("worthwhile topics") carries the follow-up selection.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared for the contexts.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-135-search-with-lepton-system-prompt.md` -> **System Prompt** (two Python prompt-string constants). Basis: the case metadata declares Artifact Type = System Prompt; the carried content is the answer prompt (`_rag_query_text`) and the follow-up-question prompt (`_more_questions_prompt`), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: no Tool Schema and no Skill definition accompany the prompt. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the artifact is two stateless single-invocation prompt templates (answer generation and related-question generation); the inputs (a user question and a set of injected contexts) are supplied per call, and no state retention, tool invocation, multi-turn dialogue, or complex reasoning is declared in the artifact. All four L1 criteria are satisfied; L2/L3 criteria are not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-135 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-135 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-135 - no worked output example is given, so no example-rule contradiction exists.
- QD-P-1.2.1 | PASS | evidence: TC-135 - the assistant role supports the cited answer-generation responsibility.
- QD-P-1.2.2 | PASS | evidence: TC-135 - the cited, professional-tone output matches the assistant role.
- QD-P-1.2.3 | PASS | evidence: TC-135 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-135 - bounded quantifiers only ("limit to 1024 tokens", "three such further questions", "no longer than 20 words").
- QD-P-1.3.2 | FAIL | evidence: TC-135, `_more_questions_prompt` - a vague qualifier carries the selection decision; excerpt: "Please identify worthwhile topics that can be follow-ups".
- QD-P-1.3.3 | PASS | evidence: TC-135 - scope is bounded to answering the given question from the provided contexts; no unbounded tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-135 - the citation rules are consistently stated, not a duplicate-constraint defect.
- QD-P-1.4.2 | PASS | evidence: TC-135 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-135 - the stated behaviors support the grounded-answer objective.
- QD-P-1.6.1 | PASS | evidence: TC-135 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-135 - no rule keyed on the model's own confidence/intent/motivation state found.
- QD-P-1.6.3 | PASS | evidence: TC-135 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-135 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-135 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-135 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-135 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-135 - input sources declared (the user question and the injected contexts, each beginning with `[[citation:x]]`).
- QD-P-2.2.2 | FAIL | evidence: TC-135 - no input format/encoding/size limits declared for the injected contexts (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-135 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-135 - a fixed insufficient-context fallback is declared; excerpt: "Say \"information is missing on\" followed by the related topic, if the given context do not provide sufficient information."
- QD-P-2.3.1 | PASS | evidence: TC-135 - output format declared (a cited answer with `[citation:x]` markers).
- QD-P-2.3.2 | PASS | evidence: TC-135 - the free-text output structure is bounded by the citation format and the 1024-token cap.
- QD-P-2.3.4 | FAIL | evidence: TC-135 - no sensitive-data filtering or privacy handling rules declared (absence) for the retrieved contexts.
- QD-P-2.5.2 | FAIL | evidence: TC-135 - no prohibition/security boundary constraints declared (absence); untrusted retrieved contexts are not declared as data-not-instructions.
- QD-P-2.7.1 | PASS | evidence: TC-135 - an inline positive example of the multi-source citation format is provided ("[citation:3][citation:5]").
- QD-P-2.7.2 | FAIL | evidence: TC-135 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-135 - no boundary-case examples provided (absence), e.g. an empty context set.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-135, module constants - the two Python string assignments parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-135 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-135 - the snippet is a structurally complete set of module-level string constants.
- QC-0.4 | PASS | evidence: TC-135 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-135 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-135 - the interpolations ({context}) are runtime template placeholders; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-135 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-135 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-135 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-135 - no imports in the snippet, so no unused/missing import.
- QC-3.3 | PASS | evidence: TC-135 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-135 - the snippet's placeholders are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available (only the System Prompt was supplied).

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in `_rag_query_text` ("You are a large language AI assistant built by Lepton AI.").
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
No explicitly expressed risk item matching an EX classification was found. The grounding rules (cite the contexts, do not repeat verbatim, use the "information is missing on" fallback) and the language rule are constraint statements, not risk expressions; no override, exfiltration, credential or PII value is present. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Traceability, Relevance, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
