> **STALE (2026-10-20)**: the inspected artifact was replaced with upstream-verified content. Re-run the inspection before using these findings.

# SanityOps Inspect Lite - Report

Artifact: TC-127-slack-it-rag-agent-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L2): P0 = 4, P1 = 7, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints declared (no untrusted-content / indirect-injection rule for retrieved KB text).
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.3.3 - no output stability/consistency assurance declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-127-slack-it-rag-agent-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a four-line instruction block (role, retrieval-only scope, citation discipline, fallback), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the n8n retrieval workflow (Google Drive ingestion, LlamaParse, Supabase pgvector, GPT-4) that performs the knowledge-base retrieval. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: the artifact is a RAG assistant that answers only from a provided knowledge base (a tool-mediated retrieval step) and is deployed in a conversational-memory pipeline (context carried across messages, per the case's Deployment Fit section). Two L2 criteria are satisfied (multi-turn dialogue; 1-3 simple tool invocations for retrieval), so L2 applies; L3 criteria are not met (no 4+ tools, no >5-step workflow declared in the artifact). The L2 tier matrix (40 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-127 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-127 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-127 - the citation example format ("Source: [filename]") is consistent with the citation rule.
- QD-P-1.2.1 | PASS | evidence: TC-127 - the "IT support assistant" role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-127 - the concise support tone matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-127 - no constraint prohibits a core responsibility; the "only the knowledge base" scope is the retrieval duty itself.
- QD-P-1.3.1 | PASS | evidence: TC-127 - no quantifier scope error found.
- QD-P-1.3.2 | PASS | evidence: TC-127 - no vague qualifier used to bound behavior found.
- QD-P-1.3.3 | PASS | evidence: TC-127 - behavior is bounded by the retrieval-only scope and the helpdesk escalation rule; no unbounded tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-127 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-127 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-127 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-127 - stated behaviors support the IT-support objective.
- QD-P-1.5.2 | PASS | evidence: TC-127 - the workflow's resource ("the knowledge base provided") is declared.
- QD-P-1.6.1 | PASS | evidence: TC-127 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-127 - the "information isn't available" condition keys on a retrieval fact, not on the model's internal state.
- QD-P-1.6.3 | PASS | evidence: TC-127 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-127 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-127 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-127 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-127 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-127 - input sources are declared (the user's questions and "the knowledge base provided").
- QD-P-2.2.2 | FAIL | evidence: TC-127 - no input question format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-127 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-127 - a fallback for unavailable information is declared; excerpt: "If information isn't available, say so and direct users to IT helpdesk".
- QD-P-2.3.1 | PASS | evidence: TC-127 - the citation output convention is declared; excerpt: "Always cite your sources as \"Source: [filename]\"", so the required output element and free-text answer form are fixed.
- QD-P-2.3.2 | PASS | evidence: TC-127 - free-text output with a declared citation convention; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-127 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-127 - no sensitive-data filtering or privacy handling rules declared (absence) for the knowledge-base content.
- QD-P-2.4.1 | PASS | evidence: TC-127 - no multi-step workflow is declared in the prompt, so there is no incomplete-workflow defect.
- QD-P-2.4.2 | PASS | evidence: TC-127 - the resource used (the provided knowledge base) is declared.
- QD-P-2.4.3 | PASS | evidence: TC-127 - no tool invocation is declared within this artifact (retrieval is handled by the hosting workflow), so no invocation specification is applicable here.
- QD-P-2.5.1 | PASS | evidence: TC-127 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-127 - no prohibition/security boundary constraints declared (absence); retrieved knowledge-base text is not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-127 - no permission control boundary declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-127 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-127 - no resource invocation frequency limits declared (absence).
- QD-P-2.7.1 | FAIL | evidence: TC-127 - no positive example provided (absence).
- QD-P-2.7.2 | FAIL | evidence: TC-127 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-127 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- Note: no executable code snippet is embedded in this artifact; the single fenced block is natural-language prompt text.
- QC-0.1 | PASS | evidence: TC-127 - the fenced block is well-formed prompt text.
- QC-0.2 | PASS | evidence: TC-127 - the fenced block carries an explicit language identifier (`text`).
- QC-0.3 | PASS | evidence: TC-127 - the block is a complete prompt fragment.
- QC-0.4 | PASS | evidence: TC-127 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-127 - the declared language (`text`) matches the content.
- QC-1.1 .. QC-4.2 | Not Executed | evidence: TC-127 - no executable code snippet is embedded, so QC-1/QC-2/QC-3/QC-4 have no object to inspect.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The n8n retrieval workflow and its retrieval tool were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the artifact ("You are an IT support assistant for [YOUR_COMPANY].").
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
No explicitly expressed risk item matching an EX classification was found. The scope restriction ("Answer questions using only the knowledge base provided") and the escalation rule are constraint declarations, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

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
| QD-P-2.7.1 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Traceability, Boundary Recognition, Safety Response, Consistency. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
