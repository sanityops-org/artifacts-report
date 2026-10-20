# SanityOps Inspect-Lite Report - TC-060-cowagent-general-assistant.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: System Prompt (assembled prompt text of `agent/prompt/builder.py`: section order, Tooling, Skills, Response-language) - type = System Prompt. Basis: prose/model-facing instructions, not a SKILL.md manifest and not a JSON tool schema.
- Artifact 2: Tool Schema (`agent/tools/base_tool.py` `BaseTool.get_json_schema` returning name/description/parameters) - type = Tool Schema. Basis: function-calling definition shape (name + description + parameters).
- Embedded Python code snippets in both artifacts -> Stage A QC.
- The channel/README descriptions and the Skill Hub surfaces are referenced material, not logic artifacts.
- Same-agent scope: both artifacts belong to the same agent ("CowAgent").

## Executive Summary
- Stages executed: A (System Prompt L3 + Tool Schema L2 + QC), B (Cross: Prompt <-> Tool, L3 scope), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts: P0 = 26 (24 prompt + 1 tool + 1 cross), P1 = 7 (1 prompt + 3 tool + 1 QC + 2 cross), P2 = 1 (cross).
- Gate-0 result: Not passed - G0-4 (the inspected Tool Schema has no parameter descriptions; `params` is an empty dict).
- Risk-Explicit summary: Executed, 0 explicit risk items.
- Top findings:
  - QD-P-2.5.1 - unbounded execution wording "Keep going until the task is done" (no termination constraint).
  - QD-P-2.5.2 - no security boundary constraints declared in the prompt text.
  - QD-P-2.5.3 - permission control boundaries referenced but not declared.
  - QD-PT-2.4 - high-risk tool capabilities (write/edit/bash) have no security boundary declaration in the prompt.
  - QD-T-1.4 - the tool schema declares no `additionalProperties` control.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - System Prompt (assembled prompt text of `agent/prompt/builder.py`)
Tier determination: L3 (Complex Agent) - basis: 4+ tool invocations (read/write/edit/ls/bash/send/memory/web_search/vision/browser), subagent delegation, 3-tier memory, permissions subsystem (checklist Sec.3.1).
Part 1 - logic defects:
QD-P-1.1.1 | PASS | evidence: TC-060 lines 78-100 - no mutually exclusive directives on one object.
QD-P-1.1.2 | PASS | evidence: TC-060 lines 78-139 - no conflicting MUST constraints without priority.
QD-P-1.1.3 | PASS | evidence: TC-060 lines 78-139 - no examples contradicting the rules.
QD-P-1.2.1 | PASS | evidence: TC-060 lines 35-48 - role (general assistant) matches the tool-orchestration responsibilities.
QD-P-1.2.2 | PASS | evidence: TC-060 lines 130-139 - no role/output-style mismatch.
QD-P-1.2.3 | PASS | evidence: TC-060 lines 78-100 - no constraint prohibiting the core responsibility.
QD-P-1.3.1 | PASS | evidence: TC-060 lines 78-100 - no quantifier scope error.
QD-P-1.3.2 | FAIL | evidence: TC-060 line 88 - vague qualifiers "multi-step tasks, complex decisions or sensitive operations, briefly explain".
QD-P-1.3.3 | FAIL | evidence: TC-060 lines 78-140 - authorization scope / prohibition scope / handoff conditions are undefined in the prompt text.
QD-P-1.4.1 | PASS | evidence: TC-060 lines 78-100 - no duplicated constraint.
QD-P-1.4.2 | PASS | evidence: TC-060 lines 95-99 - the subagent line is conditionally emitted; no never-triggered branch in the excerpt.
QD-P-1.4.3 | PASS | evidence: TC-060 lines 106-125 - the skill-selection rules are internally valid.
QD-P-1.5.1 | PASS | evidence: TC-060 lines 78-100 - responsibilities support the objective.
QD-P-1.5.2 | PASS | evidence: TC-060 lines 54-73, 80-99 - tools referenced by the workflow are declared.
QD-P-1.6.1 | FAIL | evidence: TC-060 line 88 - "sensitive operations" carries a behavioral decision (explain vs act) without defining criteria.
QD-P-1.6.2 | FAIL | evidence: TC-060 line 88 - "complex decisions" depends on the model's internal judgment.
QD-P-1.6.3 | FAIL | evidence: TC-060 lines 87-90 - soft rules interweave without arbitration ("briefly explain" + "Keep going until the task is done" + "only reply with plain text once the work is genuinely finished").
QD-P-1.6.4 | PASS | evidence: TC-060 lines 78-100 - no reasoning-method constraint.
QD-P-1.6.5 | PASS | evidence: TC-060 lines 78-139 - no self-referential/recursive constraint.
QD-P-1.6.6 | FAIL | evidence: TC-060 lines 87-92 - rules assume preconditions (tool present, context valid) with no precondition check.
QD-P-1.6.7 | FAIL | evidence: TC-060 lines 78-139 - no knowledge-update / conclusion-revision mechanism declared.
Part 2 - completeness/security defects:
QD-P-2.1.1 | PASS | evidence: TC-060 lines 34-48 - minimal formatting conventions present.
QD-P-2.1.2 | PASS | evidence: TC-060 lines 110-119 - references (`<available_skills>`, `<description>`, `<location>`) are clear.
QD-P-2.1.3 | PASS | evidence: TC-060 lines 36-48 - numbered section hierarchy is reasonable.
QD-P-2.1.4 | PASS | evidence: TC-060 lines 78-139 - prose is concise.
QD-P-2.2.1 | PASS | evidence: TC-060 lines 35-48 - input source (user conversation) is evident from the agent role.
QD-P-2.2.2 | FAIL | evidence: TC-060 lines 78-139 - no input format/encoding/size constraint declared.
QD-P-2.2.3 | FAIL | evidence: TC-060 lines 78-139 - required/optional nature of inputs not distinguished.
QD-P-2.2.4 | FAIL | evidence: TC-060 lines 78-139 - no missing-input handling declared.
QD-P-2.3.1 | FAIL | evidence: TC-060 lines 130-139 - output format is not defined (only response language).
QD-P-2.3.2 | FAIL | evidence: TC-060 lines 78-139 - no output schema defined.
QD-P-2.3.3 | FAIL | evidence: TC-060 lines 78-139 - no output stability mechanism declared.
QD-P-2.3.4 | PASS | evidence: TC-060 line 91 - "Always redact secrets, tokens and other sensitive info in replies".
QD-P-2.4.1 | FAIL | evidence: TC-060 lines 78-139 - no workflow steps defined in the prompt text.
QD-P-2.4.2 | PASS | evidence: TC-060 lines 80-84, 99 - available tools are declared.
QD-P-2.4.3 | FAIL | evidence: TC-060 lines 78-100 - no invocation parameter specification / failure handling for tools declared.
QD-P-2.5.1 | FAIL | evidence: TC-060 line 90 - unbounded execution "Keep going until the task is done"; no loop/iteration bound.
QD-P-2.5.2 | FAIL | evidence: TC-060 lines 78-139 - no prohibited operations / sensitive-data access / external-access boundary declared.
QD-P-2.5.3 | FAIL | evidence: TC-060 line 44 - permission control is referenced (Permissions section "omitted for full access") but not declared in the prompt text.
QD-P-2.5.4 | FAIL | evidence: TC-060 lines 78-139 - no constraint-priority arbitration declared.
QD-P-2.5.5 | FAIL | evidence: TC-060 lines 78-139 - no resource-invocation frequency limits declared.
QD-P-2.6.1 | FAIL | evidence: TC-060 lines 78-139 - runtime exception handling not defined.
QD-P-2.6.2 | FAIL | evidence: TC-060 lines 78-139 - no degradation/recovery strategy declared.
QD-P-2.6.3 | PASS | evidence: TC-060 lines 78-139 - no unreasonable retry mechanism present.
QD-P-2.7.1 | FAIL | evidence: TC-060 lines 78-139 - no positive examples provided.
QD-P-2.7.2 | FAIL | evidence: TC-060 lines 78-139 - no counter-examples provided.
QD-P-2.7.3 | FAIL | evidence: TC-060 lines 78-139 - no boundary-case examples provided.

### Artifact 2 - Tool Schema (`BaseTool` contract, `get_json_schema`)
Tier determination: L2 (Medium Risk) - basis: the framework hosts state-changing tools (write/edit/create-or-overwrite), so any write operation sets the tier to L2 minimum (tool-checklist tiers).
QD-T-1.1 | PASS | evidence: TC-060 lines 199-210 - the schema exposes `name`, `description`, `parameters`.
QD-T-1.2 | PASS | evidence: TC-060 lines 199-210 - no required/properties inconsistency.
QD-T-1.3 | PASS | evidence: TC-060 lines 199-210 - no enum declared.
QD-T-1.4 | FAIL | evidence: TC-060 line 188 - `params: dict = {}` and the schema expose no `additionalProperties` control.
QD-T-2.1 | PASS | evidence: TC-060 lines 199-210 - no string parameter declared at the contract level.
QD-T-2.2 | PASS | evidence: TC-060 lines 199-210 - no formatted string parameter declared.
QD-T-2.3 | PASS | evidence: TC-060 lines 199-210 - no numeric parameter declared.
QD-T-2.4 | PASS | evidence: TC-060 lines 199-210 - no array parameter declared.
QD-T-3.1 | FAIL | evidence: TC-060 line 187 - `description: str = "Base tool"` gives no write-operation notice for the state-changing tools built on it.
QD-T-3.2 | PASS | evidence: TC-060 lines 199-210 - no raw user-input passthrough parameter defined in the base schema.
QD-T-4.1 | FAIL | evidence: TC-060 line 187 - description "Base tool" is overly vague.
QD-T-4.2 | FAIL | evidence: TC-060 lines 180-186 - side effects (e.g. writes/sends) are not declared at the schema/description level.

### Embedded code snippets (QC)
Snippets inspected: the Python code blocks (TC-060 lines 34-140, 150-211).
QC-0.1 | PASS | evidence: TC-060 lines 34-140 - snippets parse as valid Python fragments.
QC-0.2 | PASS | evidence: TC-060 line 34 - code blocks carry the ```python``` identifier.
QC-0.3 | FAIL | evidence: TC-060 line 159 - class body is truncated with `...` ("Store JSON Schema") so the snippet is not standalone-complete.
QC-1.1 | PASS | evidence: TC-060 lines 171-210 - referenced names (`ToolStage`) are defined within the artifact.
QC-1.2 | PASS | evidence: TC-060 lines 150-211 - no invalid import shown.
QC-1.3 | PASS | evidence: TC-060 lines 150-211 - no deprecated API usage.
QC-1.4 | PASS | evidence: TC-060 lines 150-211 - no type mismatch.
QC-2.1 | PASS | evidence: TC-060 lines 150-211 - no file handle opened.
QC-2.2 | PASS | evidence: TC-060 lines 150-211 - no network connection opened.
QC-2.3 | PASS | evidence: TC-060 lines 213 - availability checks that throw return True (documented exception posture).
QC-3.1 | PASS | evidence: TC-060 lines 150-211 - no unused import.
QC-3.2 | PASS | evidence: TC-060 lines 150-211 - no missing import in the quoted fragments.
QC-3.3 | PASS | evidence: TC-060 lines 150-211 - no hardcoded demo credential.

## Stage B - Cross-artifact inspection
Executed - System Prompt + Tool Schema of the same agent are both present (L3 scope; no Skill artifact, so QD-PS / QD-ST / QD-CYC-1.2 not applicable).
QD-PT-2.1 | PASS | evidence: Prompt TC-060 lines 80-84 (tool names listed) <-> Tool Schema TC-060 lines 199-210 (name/description/parameters exposed); declarations consistent.
QD-PT-2.2 | PASS | evidence: Prompt TC-060 line 82 ("call exactly as listed") <-> Tool Schema TC-060 lines 199-210 (name/description/parameters); names/descriptions align.
QD-PT-2.3 | FAIL | evidence: Prompt TC-060 lines 78-100 (no parameter constraints) <-> Tool Schema TC-060 line 188 (`params: dict = {}`); no parameter constraints declared for the declared tools.
QD-PT-2.4 | FAIL | evidence: Prompt TC-060 lines 78-100 (no security boundary for high-risk tools such as bash/write) <-> Tool Schema TC-060 lines 180-186 (write-capable tools); high-risk Tool lacks a security boundary declaration in the Prompt.
QD-PT-2.5 | FAIL | evidence: Prompt TC-060 lines 78-100 (no tool error handling) <-> Tool Schema TC-060 lines 199-210 (no error types); Tool error coverage not declared.
QD-PT-2.6 | FAIL | evidence: Prompt TC-060 lines 78-139 (no invocation frequency limits) <-> Tool Schema TC-060 lines 199-210; no frequency limit declared.
QD-CYC-1.1 | PASS | evidence: no cross-artifact closed loop detected in the Prompt/Tool invocation relationships (TC-060 lines 95-99).
QD-PS / QD-ST | N/A | evidence: no Skill artifact present for this agent; not evaluated.

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 24 unfixed Stage A P0 recorded and carried forward.
- G0-2: informational only (non-blocking), 1 unfixed Stage B P0 (QD-PT-2.4) recorded.
- G0-3: satisfied - responsibility statements locatable (TC-060 lines 35-48, 78-99).
- G0-4: NOT satisfied - the inspected Tool Schema exposes no parameter descriptions (`params: dict = {}`, TC-060 line 188).
Gate-0 result: Not passed - G0-4.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed.
Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (and the full artifact set is incomplete: no Skill)
Blocking Reasons:
  G0-4 - the inspected Tool Schema has no parameter descriptions, so operation semantics are undeterminable for permission categorization.
Remediation Actions: Fix the above upstream item (complete tool parameter descriptions), then re-run Gate-0. No defect list, score, or partial conclusion is emitted here.

## Stage E - Risk Explicit (EX)
Executed. 0 explicit risk items discovered. Lines such as "Always redact secrets, tokens and other sensitive info in replies" (TC-060 line 91) are mitigations, not risk expressions. Risk Implicit was NOT run; dynamic exploitability is unverified.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-P-2.5.1 / QD-P-2.5.2 / QD-P-2.5.3 (P0) - candidate attack surface: AS-01, AS-03, AS-04, AS-06 (relevance-map.md A.1); potential impact: D1, D2, D3, Availability; strength: Medium, provisional (lite); FM: FM-08, FM-09, FM-10 (category "Prompt boundary, frequency, and termination defects").
- QD-P-2.2.x / QD-P-2.3.x (P0) - candidate attack surface: AS-02, AS-03, AS-09; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-01, FM-04, FM-06.
- QD-P-1.6.1 / QD-P-1.6.2 / QD-P-1.6.3 / QD-P-1.6.6 / QD-P-1.6.7 (P0) - candidate attack surface: AS-01, AS-06, AS-07; potential impact: D1, D2, D3; strength: Conditional, provisional (lite); FM: FM-01, FM-02, FM-07, FM-09.
- QD-PT-2.4 (cross, P0) - candidate attack surface: AS-04, AS-05; potential impact: D2, D3; strength: Medium, provisional (lite); FM: FM-04, FM-05, FM-06, FM-08 ("Cross contract defects").
- QD-T-1.4 (P0) - candidate attack surface: AS-02, AS-04; potential impact: D1, D2, D3; strength: Medium, provisional (lite); FM: FM-03, FM-04, FM-05 ("Tool structure and parameter defects").
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. Risk Implicit and Runtime Quality subsets were NOT run; per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent. QD-PM-* mapping does not apply (Stage D not executed).

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(In-place self-correction: section heading emoji present in the source artifact were omitted from evidence to satisfy the ASCII-only requirement.)

## Status board
Stage A (Single-artifact):  Executed - System Prompt (L3) + Tool Schema (L2) + QC
Stage B (Cross):            Executed - Prompt <-> Tool (L3 scope; no Skill present)
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 unsatisfied (and incomplete artifact set)
Stage E (Risk Explicit EX): Executed - 0 risk items
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
