# SanityOps Inspect-Lite Report - TC-064-anthropic-customer-support-agent.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: System Prompt (the assembled prompt template in `app/api/chat/route.ts`) - type = System Prompt. Basis: prose instructions establishing role/behavior; not a SKILL.md manifest.
- Artifact 2: Tool Schema (the Zod `responseSchema` structured output contract) - type = Tool Schema. Basis: a machine-validated schema with named fields and types (function-calling/structured-output definition shape). Note: it carries no `name`/`description`/`inputSchema` tool fields.
- The support-category taxonomy JSON is structured configuration data injected into the prompt (not one of the three logic-artifact types); it is not inspected as an artifact.
- Embedded TypeScript code snippet -> Stage A QC.
- Same-agent scope: both artifacts belong to the same agent ("Anthropic customer-support agent").

## Executive Summary
- Stages executed: A (System Prompt L2 + Tool Schema L1 + QC), B (Cross: Prompt <-> Tool, L2 scope), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts: P0 = 5 (4 prompt + 1 tool), P1 = 5 (4 prompt + 1 cross), P2 = 2 (tool).
- Gate-0 result: Not passed - G0-4 (the inspected Tool Schema has no `name`, `description`, or parameter descriptions).
- Risk-Explicit summary: Executed, 0 explicit risk items.
- Top findings:
  - QD-P-1.1.3 - example category IDs contradict the declared category-ID list.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-1.6.1 - vague decision words carry the redirect decision.
  - QD-T-1.1 - the schema lacks the required tool base fields.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - System Prompt (`app/api/chat/route.ts`)
Tier determination: L2 (Multi-turn Interactive) - basis: multi-turn dialogue, 1-3 tool interactions (RAG retrieval + classification), simple workflow (checklist Sec.3.1).
Part 1 - logic defects:
QD-P-1.1.1 | PASS | evidence: TC-064 lines 42-48 - no mutually exclusive directives.
QD-P-1.1.2 | PASS | evidence: TC-064 lines 42-95 - no conflicting MUST constraints without priority.
QD-P-1.1.3 | FAIL | evidence: TC-064 lines 75, 89 - examples use category IDs "account_management"/"technical_support" while the declared category list (line 102) is "account, billing, feature, internal, legal, other, technical, usage"; the example contradicts the rule-defined ID set.
QD-P-1.2.1 | PASS | evidence: TC-064 lines 42-48 - the assistant role matches the support responsibilities.
QD-P-1.2.2 | PASS | evidence: TC-064 line 42 - tone guidance (concise, polite, professional) matches the role.
QD-P-1.2.3 | PASS | evidence: TC-064 lines 42-48 - no constraint prohibiting the core responsibility.
QD-P-1.3.1 | PASS | evidence: TC-064 lines 42-63 - no quantifier scope error.
QD-P-1.3.2 | PASS | evidence: TC-064 lines 42-95 - vague style words are style, not boundary decisions.
QD-P-1.3.3 | PASS | evidence: TC-064 lines 47-48 - handoff/scope boundaries are declared (out-of-scope -> redirect).
QD-P-1.4.1 | PASS | evidence: TC-064 lines 42-95 - no duplicated constraint.
QD-P-1.4.2 | PASS | evidence: TC-064 lines 56-58, 121-130 - debug/optional fields are reachable.
QD-P-1.4.3 | PASS | evidence: TC-064 lines 97-104 - the classification instruction is validly defined.
QD-P-1.5.1 | PASS | evidence: TC-064 lines 42-63 - responsibilities support the support-bot objective.
QD-P-1.5.2 | PASS | evidence: TC-064 lines 43-45 - the RAG context resource is declared.
QD-P-1.6.1 | FAIL | evidence: TC-064 lines 45, 47 - vague decision words carry the redirect judgment ("if the information is not relevant for answering the question", "If the question is unrelated") without defining criteria.
QD-P-1.6.2 | FAIL | evidence: TC-064 line 48 - "If you are unable to help the user" depends on the model's internal self-assessment.
QD-P-1.6.3 | PASS | evidence: TC-064 lines 42-95 - no interwoven soft-rule conflict.
QD-P-1.6.4 | PASS | evidence: TC-064 lines 42-95 - no reasoning-method constraint.
QD-P-1.6.5 | PASS | evidence: TC-064 lines 42-95 - no self-referential/recursive constraint.
QD-P-1.6.6 | PASS | evidence: TC-064 lines 43-45 - the "no relevant context" case is explicitly handled.
QD-P-1.6.7 | PASS | evidence: TC-064 lines 42-95 - stateless single-response policy; no stale-conclusion rule.
Part 2 - completeness/security defects (L2 set):
QD-P-2.2.1 | PASS | evidence: TC-064 lines 42-45 - input sources (user message, RAG context) are declared.
QD-P-2.2.2 | PASS | evidence: TC-064 lines 42-45 - the input is free-form user chat; no parsing format required.
QD-P-2.2.3 | PASS | evidence: TC-064 lines 42-63 - no structured input parameters to mark required/optional.
QD-P-2.2.4 | PASS | evidence: TC-064 line 44 - missing RAG input handled ("No information found for this query.").
QD-P-2.3.1 | PASS | evidence: TC-064 lines 50-64 - output format (JSON) is defined.
QD-P-2.3.2 | PASS | evidence: TC-064 lines 50-64 - the output schema fields are enumerated.
QD-P-2.3.3 | FAIL | evidence: TC-064 lines 42-64 - no output-stability assurance mechanism declared.
QD-P-2.3.4 | FAIL | evidence: TC-064 lines 42-95 - no security/privacy filtering rules declared (only a grounding instruction).
QD-P-2.4.1 | PASS | evidence: TC-064 lines 43-45 - the retrieve-then-respond flow is declared.
QD-P-2.4.2 | PASS | evidence: TC-064 lines 43-45 - the RAG retrieval resource is declared.
QD-P-2.4.3 | PASS | evidence: TC-064 lines 43-45 - retrieval is system-side before generation; no model tool invocation required.
QD-P-2.5.1 | PASS | evidence: TC-064 lines 42-95 - no retry/loop, so no termination constraint needed.
QD-P-2.5.2 | FAIL | evidence: TC-064 lines 42-95 - no prohibited operations / sensitive-data access / external-access boundary declared.
QD-P-2.5.3 | PASS | evidence: TC-064 lines 42-95 - no permission-controlled operations in scope.
QD-P-2.5.4 | PASS | evidence: TC-064 lines 42-95 - no conflicting constraints needing priority.
QD-P-2.5.5 | PASS | evidence: TC-064 lines 42-95 - no resource invocations by the model.
QD-P-2.7.1 | PASS | evidence: TC-064 lines 65-94 - two representative positive examples (normal + redirect).
QD-P-2.7.2 | FAIL | evidence: TC-064 lines 65-94 - no counter-example covering typical error patterns.
QD-P-2.7.3 | FAIL | evidence: TC-064 lines 65-94 - no boundary-case example (empty/no-context input).

### Artifact 2 - Tool Schema (`responseSchema`, Zod)
Tier determination: L1 (Low Risk) - basis: a read-only structured output contract; no state change (tool-checklist tiers).
QD-T-1.1 | FAIL | evidence: TC-064 lines 109-131 - the schema exposes no `name`, `description`, or `inputSchema`/tool base fields.
QD-T-1.2 | PASS | evidence: TC-064 lines 109-131 - required fields (response/thinking/user_mood/suggested_questions/debug) are all declared.
QD-T-1.3 | PASS | evidence: TC-064 lines 112-119 - the `user_mood` enum values are unique.
QD-T-1.4 | PASS | evidence: TC-064 lines 109-131 - Zod object semantics strip unknown keys; no uncontrolled passthrough declared.
QD-T-2.1 | FAIL | evidence: TC-064 lines 110-111 - `response: z.string()` / `thinking: z.string()` have no length bound.
QD-T-2.3 | PASS | evidence: TC-064 lines 109-131 - no numeric parameter declared.
QD-T-4.1 | FAIL | evidence: TC-064 lines 110-130 - schema fields carry no descriptions (bare Zod types).

### Embedded code snippets (QC)
Snippet inspected: the TypeScript `responseSchema` block (TC-064 lines 108-132).
QC-0.1 | PASS | evidence: TC-064 lines 109-131 - the TypeScript parses.
QC-0.2 | PASS | evidence: TC-064 line 108 - code block carries the ```typescript``` identifier.
QC-0.3 | PASS | evidence: TC-064 lines 109-131 - the snippet is complete.
QC-1.1 | PASS | evidence: TC-064 lines 109-131 - `z` is referenced and (per the source) imported; no undefined name shown.
QC-1.2 | PASS | evidence: TC-064 lines 109-131 - no invalid import shown.
QC-1.3 | PASS | evidence: TC-064 lines 109-131 - no deprecated API usage.
QC-1.4 | PASS | evidence: TC-064 lines 109-131 - no type mismatch.
QC-2.1 | PASS | evidence: TC-064 lines 109-131 - no file handle opened.
QC-2.2 | PASS | evidence: TC-064 lines 109-131 - no network connection opened.
QC-2.3 | PASS | evidence: TC-064 lines 109-131 - no high-risk operation lacking guard.
QC-3.1 | PASS | evidence: TC-064 lines 109-131 - no unused import.
QC-3.2 | PASS | evidence: TC-064 lines 109-131 - no missing import in the quoted snippet.
QC-3.3 | PASS | evidence: TC-064 lines 109-131 - no hardcoded demo credential.

## Stage B - Cross-artifact inspection
Executed - System Prompt + Tool Schema of the same agent are both present (L2 scope; no Skill artifact, so QD-PS / QD-ST / QD-CYC-1.2 not applicable).
QD-PT-2.1 | PASS | evidence: Prompt TC-064 lines 43-45 (RAG resource) <-> Tool Schema TC-064 lines 109-131; no declared callable Tool is missing from the schema list.
QD-PT-2.2 | PASS | evidence: Prompt TC-064 lines 50-64 (declared JSON response structure) <-> Tool Schema TC-064 lines 109-131 (Zod object); the response field set matches.
QD-PT-2.3 | FAIL | evidence: Prompt TC-064 lines 59-60 (presents `matched_categories` as a normal field) <-> Tool Schema TC-064 line 124 (`matched_categories: z.array(z.string()).optional()`); required/optional nature is not consistently declared across the two artifacts.
QD-PT-2.4 | PASS | evidence: Prompt TC-064 lines 42-95 <-> Tool Schema TC-064 lines 109-131; no high-risk Tool requires a Prompt security boundary.
QD-CYC-1.1 | PASS | evidence: no cross-artifact closed loop detected (TC-064 lines 42-45).
QD-CYC-1.2 | PASS | evidence: single-agent prompt (no orchestrated roles); not applicable.
QD-PS / QD-ST | N/A | evidence: no Skill artifact present for this agent; not evaluated.

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 4 unfixed Stage A P0 recorded and carried forward.
- G0-2: informational only (non-blocking), no Stage B P0 (Stage B FAILs are P1).
- G0-3: satisfied - responsibility statements locatable (TC-064 lines 42-48).
- G0-4: NOT satisfied - the inspected Tool Schema has no `name`, `description`, or parameter descriptions (TC-064 lines 109-131).
Gate-0 result: Not passed - G0-4.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed.
Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (and the full artifact set is incomplete: no Skill)
Blocking Reasons:
  G0-4 - the Tool Schema lacks name/description/parameter descriptions, so operation semantics are undeterminable for permission categorization.
Remediation Actions: Fix the above upstream item, then re-run Gate-0. No defect list, score, or partial conclusion is emitted here.

## Stage E - Risk Explicit (EX)
Executed. 0 explicit risk items discovered. The escalation and grounding instructions (TC-064 lines 45-48) are controls, not risk expressions. Risk Implicit was NOT run; dynamic exploitability (e.g. prompt injection) is unverified.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-P-1.1.3 (example-rule contradiction, P0) - candidate attack surface: AS-01, AS-04, AS-05 (relevance-map.md A.1); potential impact: D1, D2, D3; strength: Medium, provisional (lite); FM: FM-01, FM-02, FM-07, FM-09.
- QD-P-2.5.2 / QD-P-2.3.4 (P0) - candidate attack surface: AS-01, AS-03, AS-04; potential impact: D1, D2, D3; strength: Medium, provisional (lite); FM: FM-08, FM-09, FM-10.
- QD-P-1.6.1 / QD-P-1.6.2 (P0/P1) - candidate attack surface: AS-01, AS-07; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-01, FM-02.
- QD-P-2.7.2 / QD-P-2.7.3 / QD-P-2.3.3 (P1) - candidate attack surface: AS-01, AS-05, AS-09; potential impact: D1, D2, D3; strength: Conditional, provisional (lite).
- QD-T-1.1 (P0) - candidate attack surface: AS-05, AS-09; potential impact: D2, Availability; strength: Medium, provisional (lite); FM: FM-03, FM-04, FM-05.
- QD-PT-2.3 (cross, P1) - candidate attack surface: AS-02, AS-05, AS-09; note only.
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. Risk Implicit and Runtime Quality subsets were NOT run; per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent. QD-PM-* mapping does not apply (Stage D not executed).

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(No in-place self-corrections were required.)

## Status board
Stage A (Single-artifact):  Executed - System Prompt (L2) + Tool Schema (L1) + QC
Stage B (Cross):            Executed - Prompt <-> Tool (L2 scope; no Skill present)
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 unsatisfied (and incomplete artifact set)
Stage E (Risk Explicit EX): Executed - 0 risk items
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
