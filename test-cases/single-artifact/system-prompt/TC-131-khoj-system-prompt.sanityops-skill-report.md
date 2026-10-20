# SanityOps Inspect Lite - Report

Artifact: TC-131-khoj-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L3): P0 = 15, P1 = 1, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints declared (retrieved note/web content not declared as data-not-instructions).
  - QD-P-2.3.4 - no security/privacy filtering declared for the user's notes/documents.
  - QD-P-2.5.3 - no permission control boundary declared.
  - QD-P-2.6.1 - runtime exceptions from tool invocation are not covered.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-131-khoj-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a set of persona/style prompt constants (`personality`, `custom_personality`, `gemini_verbose_language_personality`), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the tools implied by the capability list (notes/documents lookup, image generation, internet search, data analysis). Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L3 (Complex Agent)**. Basis: the prompt defines a personal assistant with 4+ distinct capabilities/tools ("You can generate images, look-up real-time information from the internet, analyze data and answer questions based on the user's notes"), operates over multi-turn conversation and the user's synced notes/documents, and is privacy-sensitive (the user's own private notes and files). L3 criteria satisfied (4+ tool invocations; security-sensitive; multi-turn). The L3 tier matrix (47 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-131 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-131 - the Gemini-variant statements on follow-up questions ("You may ask necessary, limited follow-up questions" and "without relying on follow-up questions") can be simultaneously satisfied and do not form an unresolved MUST-conflict.
- QD-P-1.1.3 | PASS | evidence: TC-131 - the inline citation example ("The weather today is sunny [1](https://weather.com).") is consistent with the citation style rule.
- QD-P-1.2.1 | PASS | evidence: TC-131 - the "smart, curious, empathetic and helpful personal assistant" role supports the stated capabilities.
- QD-P-1.2.2 | PASS | evidence: TC-131 - the conversational style matches the personal-assistant role.
- QD-P-1.2.3 | PASS | evidence: TC-131 - no constraint prohibits a core responsibility (the code-suppression rule governs output style, not the assistance duty).
- QD-P-1.3.1 | PASS | evidence: TC-131 - no quantifier scope error found.
- QD-P-1.3.2 | FAIL | evidence: TC-131, # Style - vague qualifiers used to bound behavior; excerpt: "Your responses should be helpful, conversational and tuned to the user's communication style."
- QD-P-1.3.3 | PASS | evidence: TC-131 - behavior is bounded by the enumerated capabilities and the user's own notes/documents; no unbounded authorization scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-131 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-131 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-131 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-131 - stated behaviors support the personal-assistant objective.
- QD-P-1.5.2 | PASS | evidence: TC-131 - the workflow's resources are described (the user's notes/documents plus the enumeration of image/internet/data capabilities).
- QD-P-1.6.1 | PASS | evidence: TC-131 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | FAIL | evidence: TC-131, # Style - a rule is keyed on the model's own judgment about the user; excerpt: "Do not respond with raw programs or scripts in your final response unless you know the user is a programmer or has explicitly requested code."
- QD-P-1.6.3 | PASS | evidence: TC-131 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-131 - no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-131 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-131 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-131 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | PASS | evidence: TC-131 - the sectioned prompt structure (Capabilities / Style / Instructions) is readable; no format-compliance defect found.
- QD-P-2.1.2 | PASS | evidence: TC-131 - section and capability references are named clearly.
- QD-P-2.1.3 | PASS | evidence: TC-131 - section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-131 - no language-conciseness defect found.
- QD-P-2.2.1 | PASS | evidence: TC-131 - input sources are declared (the user's query, the user's synced notes/documents, and past conversation).
- QD-P-2.2.2 | FAIL | evidence: TC-131 - no input query format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-131 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-131 - no handling declared for missing or anomalous input within the supplied constants (absence).
- QD-P-2.3.1 | PASS | evidence: TC-131 - output format declared (markdown responses with inline markdown citations; Gemini variant mandates markdown).
- QD-P-2.3.2 | PASS | evidence: TC-131 - free-text output with a declared citation scheme; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-131 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-131 - no sensitive-data filtering or privacy handling rules declared (absence) for the user's private notes/documents.
- QD-P-2.4.1 | PASS | evidence: TC-131 - no explicit multi-step workflow is declared in the supplied constants, so there is no incomplete-workflow defect.
- QD-P-2.4.2 | PASS | evidence: TC-131 - the resources used are described at the capability level (the user's notes/documents, internet lookup, image generation, data analysis).
- QD-P-2.4.3 | FAIL | evidence: TC-131 - no tool invocation specification declared for the enumerated capabilities (absence).
- QD-P-2.5.1 | PASS | evidence: TC-131 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-131 - no prohibition/security boundary constraints declared (absence); retrieved notes/web content is not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-131 - no permission control boundary declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-131 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-131 - no resource invocation frequency limits declared (absence).
- QD-P-2.6.1 | FAIL | evidence: TC-131 - runtime exceptions from tool invocation / retrieval are not covered (absence).
- QD-P-2.6.2 | FAIL | evidence: TC-131 - no degradation/recovery strategy declared (absence).
- QD-P-2.6.3 | PASS | evidence: TC-131 - no retry mechanism is declared, so no unreasonable-retry defect exists.
- QD-P-2.7.1 | PASS | evidence: TC-131 - a positive citation example is provided ("The weather today is sunny [1](https://weather.com).").
- QD-P-2.7.2 | FAIL | evidence: TC-131 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-131 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-131, PromptTemplate block - the Python template constants parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-131 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-131 - the snippet is a structurally complete module (the `PromptTemplate` import is present).
- QC-0.4 | PASS | evidence: TC-131 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-131 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-131 - template variables (day_of_week, current_date, name, bio) are runtime inputs; `PromptTemplate` is imported; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-131 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-131 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-131 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-131 - the `PromptTemplate` import is used; no missing imports referenced.
- QC-3.3 | PASS | evidence: TC-131 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-131 - snippet fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the capability list were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the artifact ("You are Khoj, a smart, curious, empathetic and helpful personal assistant.").
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
No explicitly expressed risk item matching an EX classification was found. The grounding/citation requirements ("Use your general knowledge and past conversation with the user as context to inform your responses.") and the code-suppression style rule are constraint declarations, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.6.1 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Relevance, Traceability, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
