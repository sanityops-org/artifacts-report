# SanityOps Inspect-Lite Report - TC-062-smartflat-ai-property-advisor.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: System Prompt (the `BaseAgent` default prompt `"You are the {name}. {description}"` and the agent declaration surface in `agent/agents/base_agent.py`) - type = System Prompt. Basis: prose/role instructions, not a SKILL.md manifest and not a JSON tool schema.
- Artifact 2: Tool Schema (`get_singapore_statistics(query: str) -> str`, a `strands` `@tool`, in `agent/tools/data_commons_tool.py`) - type = Tool Schema. Basis: function-calling definition shape (name + description + parameter).
- Embedded Python code snippets in both artifacts -> Stage A QC.
- The concrete specialist agents and supervisor are referenced from the README, not quoted; they are not inspected.
- Same-agent scope: both artifacts belong to the same agent ("SmartFlat AI / HDB Multi-Agent Advisor").

## Executive Summary
- Stages executed: A (System Prompt L3 + Tool Schema L1 + QC), B (Cross: Prompt <-> Tool, L3 scope), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts: P0 = 24 (23 prompt + 1 cross), P1 = 3 (1 QC + 2 cross), P2 = 2 (1 tool + 1 cross).
- Gate-0 result: Passed (G0-3 satisfied; G0-4 satisfied - the tool has name, description, and a described parameter).
- Risk-Explicit summary: Executed, 0 explicit risk items.
- Top findings:
  - QD-P-2.5.2 - no security boundary constraints declared in the default System Prompt.
  - QD-P-2.3.4 - no security/privacy filtering declared in the default System Prompt.
  - QD-P-2.4.3 - no tool invocation specification declared.
  - QD-PT-2.2 - no invocation specification consistent with the Tool schema.
  - QD-P-1.5.1 - the default prompt declares no responsibilities/objective.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - System Prompt (`BaseAgent` default prompt)
Tier determination: L3 (Complex Agent) - basis: multi-agent supervisor + specialists, multiple domain tools, Athena/PostgreSQL data sources (4+ tools, complex workflow) (checklist Sec.3.1).
Part 1 - logic defects:
QD-P-1.1.1 | PASS | evidence: TC-062 lines 34-60 - no mutually exclusive directives.
QD-P-1.1.2 | PASS | evidence: TC-062 lines 34-66 - no conflicting MUST constraints without priority.
QD-P-1.1.3 | PASS | evidence: TC-062 lines 34-66 - no examples contradicting the rules.
QD-P-1.2.1 | PASS | evidence: TC-062 lines 57-59 - role (name+description) is consistent with the (declared) capabilities.
QD-P-1.2.2 | PASS | evidence: TC-062 lines 57-59 - no output-style mismatch.
QD-P-1.2.3 | PASS | evidence: TC-062 lines 39-59 - no constraint prohibiting the core responsibility.
QD-P-1.3.1 | PASS | evidence: TC-062 lines 34-59 - no quantifier scope error.
QD-P-1.3.2 | PASS | evidence: TC-062 lines 34-59 - no vague qualifier carrying a decision.
QD-P-1.3.3 | FAIL | evidence: TC-062 lines 34-66 - authorization scope / prohibition scope / handoff conditions are undefined in the prompt.
QD-P-1.4.1 | PASS | evidence: TC-062 lines 34-59 - no duplicated constraint.
QD-P-1.4.2 | PASS | evidence: TC-062 lines 47-55 - abstract methods are implemented by subclasses; no dead branch in the excerpt.
QD-P-1.4.3 | PASS | evidence: TC-062 lines 51-55 - declared capabilities are valid.
QD-P-1.5.1 | FAIL | evidence: TC-062 lines 57-59 - the prompt states only "You are the {name}. {description}"; responsibilities sufficient to accomplish the objective are not declared.
QD-P-1.5.2 | PASS | evidence: TC-062 lines 42-45 - the tools list is injected at construction; referenced resources are declared.
QD-P-1.6.1 | PASS | evidence: TC-062 lines 34-66 - no vague word carrying a security/permission decision.
QD-P-1.6.2 | PASS | evidence: TC-062 lines 34-66 - no rule depending on model internal state.
QD-P-1.6.3 | PASS | evidence: TC-062 lines 34-66 - no interwoven soft rules.
QD-P-1.6.4 | PASS | evidence: TC-062 lines 34-66 - no reasoning-method constraint.
QD-P-1.6.5 | PASS | evidence: TC-062 lines 34-66 - no self-referential/recursive constraint.
QD-P-1.6.6 | FAIL | evidence: TC-062 lines 57-59 - the default prompt assumes `name`/`description` fully convey the agent's job, with no precondition handling when that assumption fails.
QD-P-1.6.7 | PASS | evidence: TC-062 lines 34-66 - no static-knowledge rule needing revision.
Part 2 - completeness/security defects:
QD-P-2.1.1 | PASS | evidence: TC-062 lines 34-59 - minimal formatting present.
QD-P-2.1.2 | PASS | evidence: TC-062 lines 34-59 - references are clear.
QD-P-2.1.3 | PASS | evidence: TC-062 lines 34-59 - structure readable.
QD-P-2.1.4 | PASS | evidence: TC-062 lines 34-59 - prose concise.
QD-P-2.2.1 | FAIL | evidence: TC-062 lines 34-66 - no input source declared in the prompt.
QD-P-2.2.2 | FAIL | evidence: TC-062 lines 34-66 - no input-format constraint.
QD-P-2.2.3 | FAIL | evidence: TC-062 lines 34-66 - required/optional inputs not distinguished.
QD-P-2.2.4 | FAIL | evidence: TC-062 lines 34-66 - no missing-input handling.
QD-P-2.3.1 | FAIL | evidence: TC-062 lines 34-66 - no output format defined in the prompt.
QD-P-2.3.2 | FAIL | evidence: TC-062 lines 47-50 - `execute` returns a Dict but no output schema is declared.
QD-P-2.3.3 | FAIL | evidence: TC-062 lines 34-66 - no output-stability mechanism.
QD-P-2.3.4 | FAIL | evidence: TC-062 lines 34-66 - no security/privacy filtering declared in the prompt.
QD-P-2.4.1 | FAIL | evidence: TC-062 lines 34-66 - no workflow steps defined.
QD-P-2.4.2 | PASS | evidence: TC-062 lines 42-45, 167-175 - tools/data sources are declared.
QD-P-2.4.3 | FAIL | evidence: TC-062 lines 34-66 - no invocation specification declared in the prompt.
QD-P-2.5.1 | FAIL | evidence: TC-062 lines 34-66 - no termination constraints declared.
QD-P-2.5.2 | FAIL | evidence: TC-062 lines 34-66 - no security boundary constraints declared.
QD-P-2.5.3 | FAIL | evidence: TC-062 lines 34-66 - no permission control boundaries declared.
QD-P-2.5.4 | FAIL | evidence: TC-062 lines 34-66 - no constraint-priority arbitration.
QD-P-2.5.5 | FAIL | evidence: TC-062 lines 34-66 - no resource-invocation frequency limits.
QD-P-2.6.1 | FAIL | evidence: TC-062 lines 34-66 - no runtime exception handling declared in the prompt.
QD-P-2.6.2 | FAIL | evidence: TC-062 lines 34-66 - no degradation/recovery strategy declared.
QD-P-2.6.3 | PASS | evidence: TC-062 lines 34-66 - no unreasonable retry mechanism.
QD-P-2.7.1 | FAIL | evidence: TC-062 lines 34-66 - no positive examples.
QD-P-2.7.2 | FAIL | evidence: TC-062 lines 34-66 - no counter-examples.
QD-P-2.7.3 | FAIL | evidence: TC-062 lines 34-66 - no boundary-case examples.

### Artifact 2 - Tool Schema (`get_singapore_statistics`)
Tier determination: L1 (Low Risk) - basis: read-only statistics query; no state change, no sensitive data (tool-checklist tiers).
QD-T-1.1 | PASS | evidence: TC-062 lines 91-101 - the tool exposes a name and a description docstring plus a parameter.
QD-T-1.2 | PASS | evidence: TC-062 lines 91-101 - no required/properties inconsistency.
QD-T-1.3 | PASS | evidence: TC-062 lines 91-101 - no enum declared.
QD-T-1.4 | PASS | evidence: TC-062 lines 91-101 - no object-type parameter schema; not applicable.
QD-T-2.1 | FAIL | evidence: TC-062 line 92 - `query: str` has no `maxLength`/`minLength` bound.
QD-T-2.3 | PASS | evidence: TC-062 lines 91-101 - no numeric parameter declared.
QD-T-4.1 | PASS | evidence: TC-062 lines 93-101 - the description and `Args: query` note are clear.

### Embedded code snippets (QC)
Snippets inspected: the Python code blocks (TC-062 lines 34-60, 72-146).
QC-0.1 | PASS | evidence: TC-062 lines 91-146 - snippets parse as valid Python fragments.
QC-0.2 | PASS | evidence: TC-062 lines 72, 106 - code blocks carry the ```python``` identifier.
QC-0.3 | FAIL | evidence: TC-062 line 135 - the result-building block is truncated with `...`, so the snippet is not standalone-complete.
QC-1.1 | PASS | evidence: TC-062 lines 107-146 - referenced names (`dc`, `os`) are imported within the snippet.
QC-1.2 | PASS | evidence: TC-062 line 108 - `import datacommons as dc` is guarded by try/except.
QC-1.3 | PASS | evidence: TC-062 lines 107-146 - no deprecated API usage.
QC-1.4 | PASS | evidence: TC-062 lines 91-146 - no type mismatch.
QC-2.1 | PASS | evidence: TC-062 lines 107-146 - no file handle opened.
QC-2.2 | PASS | evidence: TC-062 lines 107-146 - no network connection object opened directly.
QC-2.3 | PASS | evidence: TC-062 lines 107-146 - the API call is wrapped by an outer try/except returning a typed error.
QC-3.1 | PASS | evidence: TC-062 lines 107-146 - no unused import.
QC-3.2 | PASS | evidence: TC-062 lines 107-146 - no missing import in the quoted fragments.
QC-3.3 | PASS | evidence: TC-062 lines 110-113 - the API key is read from the environment (`os.getenv`), not hardcoded.

## Stage B - Cross-artifact inspection
Executed - System Prompt + Tool Schema of the same agent are both present (L3 scope; no Skill artifact, so QD-PS / QD-ST / QD-CYC-1.2 not applicable).
QD-PT-2.1 | PASS | evidence: Prompt TC-062 lines 42-45 (tools injected) <-> Tool Schema TC-062 lines 91-101 (`get_singapore_statistics`); the declared tool exists.
QD-PT-2.2 | FAIL | evidence: Prompt TC-062 lines 34-66 (no invocation specification) <-> Tool Schema TC-062 lines 91-101 (name/description/`query` parameter); the Prompt declares no invocation specification matching the Tool Schema.
QD-PT-2.3 | FAIL | evidence: Prompt TC-062 lines 34-66 (no parameter constraints) <-> Tool Schema TC-062 line 92 (`query: str`, no bound); parameter constraints are not aligned.
QD-PT-2.4 | PASS | evidence: Prompt TC-062 lines 34-66 <-> Tool Schema TC-062 lines 91-101 (read-only L1 tool); no high-risk Tool requires a Prompt security boundary.
QD-PT-2.5 | FAIL | evidence: Prompt TC-062 lines 34-66 (no error handling) <-> Tool Schema TC-062 lines 119-146 (`TOOL_UNAVAILABLE`/`TOOL_ERROR`); the Prompt does not cover the Tool's error types.
QD-PT-2.6 | FAIL | evidence: Prompt TC-062 lines 34-66 (no frequency limits) <-> Tool Schema TC-062 lines 91-146; no invocation frequency limit declared.
QD-CYC-1.1 | PASS | evidence: no cross-artifact closed loop detected (TC-062 lines 42-45).
QD-CYC-1.2 | PASS | evidence: the supervisor routes one-way to specialists (TC-062 lines 167-175); no circular role invocation detected.
QD-PS / QD-ST | N/A | evidence: no Skill artifact present for this agent; not evaluated.

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 23 unfixed Stage A P0 recorded and carried forward.
- G0-2: informational only (non-blocking), 1 unfixed Stage B P0 (QD-PT-2.2) recorded.
- G0-3: satisfied - responsibility statements locatable (TC-062 lines 39-45, 57-59).
- G0-4: satisfied - the Tool Schema has a name, a description, and a described parameter (TC-062 lines 91-101).
Gate-0 result: Passed.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed - incomplete artifact set (full set requires System Prompt + Skill + all Tool Schemas for the same agent; no Skill artifact is provided).

## Stage E - Risk Explicit (EX)
Executed. 0 explicit risk items discovered. The tool reads the API key from the environment (`os.getenv`, TC-062 lines 110-113) and returns typed errors, which are mitigations, not risk expressions. Risk Implicit was NOT run; dynamic exploitability is unverified.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-P-2.5.2 / QD-P-2.5.3 / QD-P-2.3.4 (P0) - candidate attack surface: AS-01, AS-03, AS-04; potential impact: D1, D2, D3; strength: Medium, provisional (lite); FM: FM-08, FM-09, FM-10.
- QD-P-2.2.x / QD-P-2.3.x (P0) - candidate attack surface: AS-02, AS-03, AS-09; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-01, FM-04, FM-06.
- QD-P-1.3.3 / QD-P-1.5.1 / QD-P-1.6.6 (P0) - candidate attack surface: AS-01, AS-04, AS-05; potential impact: D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-01, FM-02, FM-07, FM-09.
- QD-PT-2.2 (cross, P0) - candidate attack surface: AS-02, AS-05, AS-09; potential impact: D2, Availability; strength: Medium, provisional (lite); FM: FM-04, FM-05, FM-06, FM-08.
- QD-T-2.1 (P2) - candidate attack surface: AS-02, AS-06; potential impact: D2, D3, Availability; strength: Conditional, provisional (lite); note only.
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. Risk Implicit and Runtime Quality subsets were NOT run; per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent.

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(In-place self-correction: a non-ASCII bullet character present in the tool's result string was paraphrased rather than quoted, per the ASCII-only requirement.)

## Status board
Stage A (Single-artifact):  Executed - System Prompt (L3) + Tool Schema (L1) + QC
Stage B (Cross):            Executed - Prompt <-> Tool (L3 scope; no Skill present)
Stage C (Gate-0):           Passed
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 risk items
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
