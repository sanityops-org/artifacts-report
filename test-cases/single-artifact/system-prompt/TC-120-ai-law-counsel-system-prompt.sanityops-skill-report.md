# SanityOps Inspect Lite - Report

Artifact: TC-120-ai-law-counsel-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L3): P0 = 12, P1 = 0, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no prohibition/security boundary constraints declared.
  - QD-P-2.5.3 - no permission control boundary declared.
  - QD-P-2.3.4 - no security/privacy filtering declared for uploaded legal documents.
  - QD-P-2.5.4 - no arbitration rule for potentially conflicting soft constraints declared.
  - QD-P-2.6.1 - runtime exceptions from tool invocation not covered.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-120-ai-law-counsel-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried content is a Korean-language prompt string returned by `buildSystemPrompt(today)` (prose/markdown instructions), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the tool schemas for `search_law_articles`, `get_law_detail`, `search_law`, `search_precedent`, `search_administrative_rule`, `get_precedent_detail`, and `clarify_situation`, plus the `korean-law-mcp` server. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.
- Note: the artifact text is Korean. Per the report language contract, quoted evidence is rendered in English and marked as a translation; no verbatim CJK text is reproduced.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L3 (Complex Agent)**. Basis: the prompt declares 7 tools (search_law_articles, get_law_detail, search_law, search_precedent, search_administrative_rule, get_precedent_detail, clarify_situation) - satisfying the "4+ tool invocations" criterion - and it runs three distinct operating modes (legal Q&A, uploaded-document analysis, guided template generation), each with its own multi-step procedure, forming a complex multi-mode workflow. L3 criteria satisfied; L2 (multi-turn dialogue, limited state) is covered by upward compatibility. The L3 tier matrix (47 items) is applied. Note: the L3 matrix shows 35 P0 items while Appendix A.3 lists a 34-item L3 minimum P0 set (it omits QD-P-1.4.3); this report evaluates the full matrix and reports Appendix A.3's count as the source's stated compliance basis.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-120 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-120 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-120, Citation Format - the `cite:statute/...` and `cite:precedent/...` examples are consistent with the stated citation rule.
- QD-P-1.2.1 | PASS | evidence: TC-120 - the plain-language legal-information-counselor role supports the stated explanation responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-120 - the plain-Korean explainer style matches the layperson audience.
- QD-P-1.2.3 | PASS | evidence: TC-120 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-120 - quantifiers are bounded ("usually 3-6 tool calls is enough"; "1-2 precedents").
- QD-P-1.3.2 | PASS | evidence: TC-120 - no vague qualifier carries a critical behavioral or boundary decision; open-ended lists are explicitly marked "usually" / "in general".
- QD-P-1.3.3 | PASS | evidence: TC-120 - behavior is bounded by the three declared modes and the mandatory disclaimer; no unbounded authorization/handoff scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-120 - no duplicate-constraint defect found (the disclaimer is a required output, restated consistently).
- QD-P-1.4.2 | PASS | evidence: TC-120 - no never-triggered condition found.
- QD-P-1.4.3 | PASS | evidence: TC-120 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-120 - the stated behaviors support the grounded legal-explanation objective.
- QD-P-1.5.2 | PASS | evidence: TC-120 - every tool the workflow names is declared in the prompt.
- QD-P-1.6.1 | PASS | evidence: TC-120 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-120 - no rule keyed on the model's internal state (confidence/intent/motivation) found.
- QD-P-1.6.3 | PASS | evidence: TC-120 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-120 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-120 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-120 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-120 - no static-knowledge conclusion-revision gap found; grounding is required per conversation.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | PASS | evidence: TC-120 - the markdown structure is readable; no format-compliance defect found.
- QD-P-2.1.2 | PASS | evidence: TC-120 - tool names and section references are named clearly.
- QD-P-2.1.3 | PASS | evidence: TC-120 - section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-120 - no language-conciseness defect found.
- QD-P-2.2.1 | PASS | evidence: TC-120, Document Analysis Mode - input sources declared (the user's question, and, for uploads, the injected "[document analysis request]" marker plus extracted text).
- QD-P-2.2.2 | FAIL | evidence: TC-120 - no input format/encoding/size limits declared for user questions or uploaded legal documents (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-120 - required vs optional inputs are not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-120 - behavior for general/under-specified questions is declared; translated excerpt: "For a general question, do not ask back; answer based on the ordinary case first, then briefly ask for the facts needed for a more accurate judgment."
- QD-P-2.3.1 | PASS | evidence: TC-120, Answer Structure - a fixed markdown section order is prescribed (headings `## At a glance`, `## Related statutes`, `## Steps and deadlines`, `## Related precedents`, `## Cautions`).
- QD-P-2.3.2 | PASS | evidence: TC-120 - free-text markdown with a declared section order; no structured schema is required.
- QD-P-2.3.3 | FAIL | evidence: TC-120 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-120 - no sensitive-data filtering or privacy handling rules declared (absence), despite a mode that ingests user-uploaded legal documents.
- QD-P-2.4.1 | PASS | evidence: TC-120 - the workflow steps are enumerated (tool-first grounded answer; 4-step document analysis; 4-step template generation).
- QD-P-2.4.2 | PASS | evidence: TC-120 - the tools used are declared (search_law_articles, get_law_detail, search_law, search_precedent, search_administrative_rule, get_precedent_detail, clarify_situation).
- QD-P-2.4.3 | PASS | evidence: TC-120 - invocation parameter specification and sequence are declared (for example get_law_detail takes lawName and articles; precedent holdings require get_precedent_detail).
- QD-P-2.5.1 | PASS | evidence: TC-120 - a tool-call budget is referenced; translated excerpt: "usually 3-6 tool calls is enough".
- QD-P-2.5.2 | FAIL | evidence: TC-120 - no prohibition/security boundary constraints declared (absence); the untrusted status of uploaded document text and of tool-returned statute text is not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-120 - no permission control boundary declared (absence); the scope of document access and any elevated operations are not bounded.
- QD-P-2.5.4 | FAIL | evidence: TC-120 - no arbitration rule for potentially conflicting soft constraints declared (absence), for example between "answer first without asking back" and "use clarify_situation only in specific cases".
- QD-P-2.5.5 | FAIL | evidence: TC-120 - no resource invocation frequency limits declared (absence), despite guidance to issue several parallel calls at once.
- QD-P-2.6.1 | FAIL | evidence: TC-120 - runtime exceptions from tool invocation are not covered (absence).
- QD-P-2.6.2 | FAIL | evidence: TC-120 - no degradation/recovery strategy declared (absence).
- QD-P-2.6.3 | PASS | evidence: TC-120 - no retry mechanism is declared, so no unreasonable-retry defect exists.
- QD-P-2.7.1 | PASS | evidence: TC-120 - positive examples are provided (citation-link formats, good/bad search-term examples, deadline-quoting examples).
- QD-P-2.7.2 | FAIL | evidence: TC-120 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-120 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-120, `buildSystemPrompt` block - the TypeScript template function parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-120 - the fenced block carries an explicit language identifier (`typescript`).
- QC-0.3 | PASS | evidence: TC-120 - the snippet is a structurally complete function; the helper it references is a module-level function outside the quoted excerpt.
- QC-0.4 | PASS | evidence: TC-120 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-120 - the declared language (`typescript`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-120 - template interpolations are runtime inputs; no undefined names or type mismatches inside the quoted excerpt.
- QC-1.2 | Not Executed | evidence: TC-120 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-120 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-120 - no file handles, network connections, or high-risk operations appear in the prompt snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-120 - no unused/missing imports (no imports in the snippet).
- QC-3.3 | PASS | evidence: TC-120 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-120 - snippet fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the returned prompt; translated excerpt: "You are an AI counselor who explains Korean legal information in plain language."
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
No explicitly expressed risk item matching an EX classification was found. The grounding rules ("cite only article text confirmed by tools", "do not invent article numbers") and the mandatory-disclaimer instructions are constraint statements, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.6.1 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response, Traceability. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
