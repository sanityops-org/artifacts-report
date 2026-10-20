# SanityOps Inspect Lite - Report

Artifact: TC-130-private-gpt-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L2): P0 = 6, P1 = 6, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared for the user's documents.
  - QD-P-2.4.2 - tool calls are referenced but no tool/resource is declared.
  - QD-P-2.4.3 - no tool invocation specification declared.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-130-private-gpt-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a set of Jinja system-message templates (base persona template plus the citations and thinking guideline partials), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the guideline tool templates (e.g. `tools/semantic_search.j2`, `tools/database_query.j2`) and their tool schemas. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: the artifact is a RAG "chat with your documents" assistant that retrieves from indexed documents (a tool-mediated retrieval step; the thinking guideline explicitly refers to tool calls) and operates in a multi-turn chat with conversation context. Two L2 criteria are satisfied (multi-turn dialogue; 1-3 simple tool invocations). L3 criteria are not established from the supplied templates (the exact tool count is not determinable here; no >5-step workflow is declared), so L2 is applied. The L2 tier matrix (40 items) is applied. Note: if the deployment enables more tool templates, the tier could rise on a later run.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-130 - no mutually exclusive directives found (the phrasing ban on "according to/source/citation" does not conflict with the citation requirement).
- QD-P-1.1.2 | PASS | evidence: TC-130 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-130 - the citation examples ("Solar capacity grew 25% [1]" -> "Solar capacity grew 25% {{ sample_cite_1 }}.") are consistent with the citation rules.
- QD-P-1.2.1 | PASS | evidence: TC-130 - the parameterized assistant role supports the document-QA responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-130 - the citation-integrated, seamless style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-130 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-130 - no quantifier scope error found.
- QD-P-1.3.2 | FAIL | evidence: TC-130, thinking_guidelines - vague qualifier used to bound behavior; excerpt: "Calibrate thinking depth to query complexity: simple questions may not need thinking at all; complex multi-step problems benefit from extended reflection."
- QD-P-1.3.3 | PASS | evidence: TC-130 - behavior is bounded by the citation protocol; no unbounded authorization scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-130 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-130 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-130 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-130 - stated behaviors support the grounded document-QA objective.
- QD-P-1.5.2 | PASS | evidence: TC-130 - the supplied templates declare no explicit multi-step workflow requiring undeclared resources; retrieval content is injected via the context block.
- QD-P-1.6.1 | PASS | evidence: TC-130 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-130 - no rule keyed on the model's internal confidence/intent state found.
- QD-P-1.6.3 | PASS | evidence: TC-130 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | FAIL | evidence: TC-130, thinking_guidelines - a constraint on the model's internal reasoning method/phrasing; excerpt: "Use conversational phrases like \"Hmm...\", \"Actually...\", \"Wait, I'm realizing...\" to reflect genuine reasoning."
- QD-P-1.6.5 | PASS | evidence: TC-130 - the "Avoid mentioning internal instructions" rule is an anti-disclosure statement, not a recursive/self-referential constraint.
- QD-P-1.6.6 | PASS | evidence: TC-130 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-130 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-130 - input sources are indicated (the user query, the injected context documents, and the injected system_prompt/date variables).
- QD-P-2.2.2 | FAIL | evidence: TC-130 - no input query format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-130 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-130 - no handling declared for missing or anomalous input (absence).
- QD-P-2.3.1 | PASS | evidence: TC-130, citation_protocol - the output convention is declared (inline single-bracket citations `[XXXX]`, placement rules, table/list consolidation).
- QD-P-2.3.2 | PASS | evidence: TC-130 - free-text output with a declared citation scheme; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-130 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-130 - no sensitive-data filtering or privacy handling rules declared (absence) for the user's documents.
- QD-P-2.4.1 | PASS | evidence: TC-130 - no explicit multi-step workflow is declared in the supplied templates, so there is no incomplete-workflow defect.
- QD-P-2.4.2 | FAIL | evidence: TC-130, thinking_guidelines - tool calls are referenced ("track tool calls already made in this turn") but no tool set or resource is declared in the artifact (absence).
- QD-P-2.4.3 | FAIL | evidence: TC-130 - no tool invocation specification declared for the referenced tool calls (absence).
- QD-P-2.5.1 | PASS | evidence: TC-130 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | PASS | evidence: TC-130, thinking_guidelines - a non-disclosure boundary is declared; excerpt: "Avoid mentioning internal instructions or behavioral guidelines in your thinking."
- QD-P-2.5.3 | FAIL | evidence: TC-130 - no permission control boundary declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-130 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-130 - no resource invocation frequency limits declared (absence).
- QD-P-2.7.1 | PASS | evidence: TC-130 - positive examples are provided (citation examples; "Good thinking" example).
- QD-P-2.7.2 | PASS | evidence: TC-130 - a counter-example is provided ("Poor thinking: ..."); invalid wrapper forms are enumerated.
- QD-P-2.7.3 | PASS | evidence: TC-130 - boundary-flavored cases are exemplified (the unrelated-source omission case and the placement rules for tables/lists).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-130, base.j2 / citations.j2 / thinking.j2 blocks - the Jinja templates parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-130 - each fenced block carries an explicit language identifier (`jinja`).
- QC-0.3 | PASS | evidence: TC-130 - the templates are structurally complete.
- QC-0.4 | PASS | evidence: TC-130 - the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-130 - the declared language (`jinja`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-130 - template variables (assistant_name, all_cites, sample_cite_1, few_shots) are runtime inputs; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-130 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-130 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-130 - no file handles, network connections, or high-risk operations appear in the snippets.
- QC-3.1, QC-3.2 | PASS | evidence: TC-130 - no unused/missing imports (no imports in the snippets).
- QC-3.3 | PASS | evidence: TC-130 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-130 - the template variables are consistent with the base template's own block declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool templates and their schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in base.j2 ("You are {{ assistant_name }}, an AI assistant.").
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
No explicitly expressed risk item matching an EX classification was found. The citation-batching rules ("Consolidate multiple sources on the same claim", "Omit citations when a source is unrelated") and the non-disclosure rule ("Avoid mentioning internal instructions") are constraint declarations, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.4 | AS-01, AS-06, AS-07 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Traceability, Format Compliance, Consistency, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
