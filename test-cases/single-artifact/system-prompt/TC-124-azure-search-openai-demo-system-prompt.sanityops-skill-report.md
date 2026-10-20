# SanityOps Inspect Lite - Report

Artifact: TC-124-azure-search-openai-demo-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 4, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared for source content.
  - QD-P-2.5.2 - no security boundary constraints declared (untrusted source content is not declared as data-not-instructions).
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs are not distinguished.
  - QD-P-2.7.2 - no counter-examples provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-124-azure-search-openai-demo-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried content is a Jinja2 system-message template (`chat_answer.system.jinja2`) of prose instructions, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: no Tool Schema is referenced or supplied. Retrieval and citation pipeline logic live in the surrounding `app/backend/approaches/` modules, which are out of scope. Only the Prompt is present.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the template generates a single grounded answer with citations from the retrieved source list; it declares no tool invocations and no multi-turn state. L1 criteria ("single skill", "no tool invocations") are satisfied with 2+ matches. L2 criteria (multi-turn dialogue, 1-3 tools, simple workflow, limited state) are not satisfied by the quoted artifact. The L1 tier matrix (30 items) is applied; the L1 minimum P0 set is 8 items.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-124 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-124 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-124 - the citation examples (`[info1.txt]`, `[info1.txt][info2.pdf]`, `<<...>>`) are consistent with the stated rules.
- QD-P-1.2.1 | PASS | evidence: TC-124 - the internal-document assistant role supports the grounded-answer responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-124 - the "Be brief in your answers" style matches the employee-assistant role.
- QD-P-1.2.3 | PASS | evidence: TC-124 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-124 - no quantifier scope error found ("Generate 3 very brief follow-up questions" is bounded).
- QD-P-1.3.2 | PASS | evidence: TC-124 - "Be brief" is a style directive, not a decision-carrying vague qualifier on a behavioral boundary.
- QD-P-1.3.3 | PASS | evidence: TC-124 - the scope is fixed; excerpt: "Assistant helps the company employees with their questions about internal documents."
- QD-P-1.4.1 | PASS | evidence: TC-124 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-124 - no never-triggered condition found.
- QD-P-1.5.1 | PASS | evidence: TC-124 - the grounding and citation behaviors support the document-Q&A objective.
- QD-P-1.6.1 | PASS | evidence: TC-124 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-124 - no rule keyed on the model's internal state (confidence/intent/motivation) found.
- QD-P-1.6.3 | PASS | evidence: TC-124 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-124 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-124 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-124 - the empty/insufficient-source case is handled explicitly, so no unstated assumption is relied on.
- QD-P-1.6.7 | PASS | evidence: TC-124 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-124 - the input source is declared; excerpt: "Answer ONLY with the facts listed in the list of sources below" (the retrieved source list, plus the user's question and the materialized `citations`).
- QD-P-2.2.2 | FAIL | evidence: TC-124 - no input format/encoding/size constraint declared for the question or the source set (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-124 - required vs optional inputs are not distinguished (absence); the `citations` and `image_sources` branches are not documented as required/optional at the prompt level.
- QD-P-2.2.4 | PASS | evidence: TC-124 - missing-source handling is declared; excerpt: "If there isn't enough information below, say you don't know."
- QD-P-2.3.1 | PASS | evidence: TC-124 - the output format is declared (brief answers, square-bracket inline citations, one bracket per source, `<<...>>` follow-up questions).
- QD-P-2.3.2 | PASS | evidence: TC-124 - free-text output with a declared citation format; no structured schema is required.
- QD-P-2.3.4 | FAIL | evidence: TC-124 - no security/privacy filtering declared (absence); no rule governs sensitive content inside the retrieved internal documents or the user's question.
- QD-P-2.5.2 | FAIL | evidence: TC-124 - no security boundary constraint declared (absence); the untrusted status of retrieved source content is not stated as data-not-instructions (the prompt-injection boundary is delegated to the runtime `injected_prompt`).
- QD-P-2.7.1 | PASS | evidence: TC-124 - positive examples are provided (the citation and follow-up-question examples).
- QD-P-2.7.2 | FAIL | evidence: TC-124 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-124 - no boundary-case examples provided (absence); the empty-source case is stated as a rule, not exemplified.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-124, `chat_answer.system.jinja2` block - the template is valid for its declared language (balanced `{% if %}`/`{% endif %}` blocks).
- QC-0.2 | PASS | evidence: TC-124 - the fenced block carries an explicit language identifier (`jinja2`).
- QC-0.3 | PASS | evidence: TC-124 - the template is structurally complete (all conditional blocks are closed).
- QC-0.4 | PASS | evidence: TC-124 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-124 - the declared language (`jinja2`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-124 - the referenced symbols (`citation`, `override_prompt`, `image_sources`, `injected_prompt`, `include_follow_up_questions`) are template variables; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-124 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-124 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-124 - no file handles, network connections, or high-risk operations appear in the template.
- QC-3.1, QC-3.2 | PASS | evidence: TC-124 - no unused/missing imports (no imports in the snippet).
- QC-3.3 | PASS | evidence: TC-124 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-124 - the template's variables are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. No Tool Schema is referenced by this prompt.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the template; excerpt: "Assistant helps the company employees with their questions about internal documents."
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
No explicitly expressed risk item matching an EX classification was found. The grounding constraints ("Answer ONLY with the facts listed in the list of sources below"), the "say you don't know" fallback, and the citation rules are constraint statements, not risk expressions. The template variables `override_prompt` and `injected_prompt` are runtime substitution points, not explicit risk instructions, so no EX classification is assigned to them. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

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

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Relevance, Traceability, Boundary Recognition. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
