# SanityOps Inspect-Lite Report - TC-051-jarvis-system-prompt.md

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label; Collection Date: 2026-10-13)

## 1. Executive Summary

- Executed stages: Stage A (single-artifact System Prompt inspection, QD-P, plus embedded-code QC on the YAML carrier), Stage C (Gate-0 admission check), Stage E (Risk Explicit), Stage F (Impact outlook), Stage G (self-verification).
- Inspect defect findings (Stage A, QD-P): P0 = 11, P1 = 2, P2 = 0 (13 FAIL over the 47 applicable L3 rules). Embedded-code QC: 13 items, 0 FAIL.
- Gate-0 result: Not passed - G0-4.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no explicitly declared risk item identified in the static text).
- Top findings (up to five, rule ID - one-line defect):
  - QD-P-2.5.2 - No security boundary constraints are declared for the orchestration.
  - QD-P-2.3.4 - No security/privacy filtering mechanism is declared.
  - QD-P-2.6.1 - Runtime exceptions (model-invocation failures) are not covered.
  - QD-P-2.6.2 - No degradation and recovery strategy is declared.
  - QD-P-2.5.5 - No resource (model) invocation frequency limits are declared.
- What was NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran inside Stage A.
- Upgrade pointer: for the full inspect ruleset plus Risk and Quality, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md
- This report states no security conclusion and no quality conclusion; Inspect PASS is not Risk PASS and is not Quality PASS.

## 2. Stage A - System Prompt Inspection (QD-P)

Artifact inventory: one markdown transcript classified as a System Prompt by structural signature (stage prompt strings inside a YAML config). The artifact is the multi-stage controller prompt of HuggingGPT (parse_task / choose_model / response_results). The embedded YAML carrier is inspected under the lite embedded-code QC sub-check.

Tier determination: L3 (Complex Agent). Basis: the controller orchestrates many external expert models (far more than 4 model/task invocations), across a multi-stage workflow with task dependencies, and relies on fallback handling for unparseable input. At least two L3 determination criteria are satisfied (4+ tool invocations, multi-stage orchestration / dependency handling). The L3 tier item set (47 items) is applied.

Not applicable at L3: none (all 47 items give a verdict).

### Part 1 - Logic defects
- QD-P-1.1.1 | PASS | P0 | evidence: TC-051, tprompt; no mutually exclusive directive on the same object.
- QD-P-1.1.2 | PASS | P0 | evidence: TC-051, parse_task; "Parse out as few tasks as possible while ensuring that the user request can be resolved" self-arbitrates the minimality/completeness tension.
- QD-P-1.1.3 | PASS | P0 | evidence: TC-051; the referenced few-shot demos are declared consistent inputs; no example contradicts a rule.
- QD-P-1.2.1 | PASS | P0 | evidence: TC-051; the orchestrator role matches the planning/selection/response responsibilities.
- QD-P-1.2.2 | PASS | P1 | evidence: TC-051, response_results; the "friendly tone" matches the stated assistant role.
- QD-P-1.2.3 | PASS | P0 | evidence: TC-051; the constrained task enumeration does not prohibit the orchestration responsibility.
- QD-P-1.3.1 | PASS | P1 | evidence: TC-051, parse_task; quantifiers attach to concrete objects ("as few tasks as possible", the model list).
- QD-P-1.3.2 | FAIL | P1 | evidence: TC-051, choose_model; excerpt: "find the model that has the most potential to solve requests and tasks" - an undefined qualitative term carries model selection.
- QD-P-1.3.3 | PASS | P0 | evidence: TC-051; the action space is bounded by the fixed task enumeration.
- QD-P-1.4.1 | PASS | P2 | evidence: TC-051; no duplicated constraint detected.
- QD-P-1.4.2 | PASS | P2 | evidence: TC-051; no unreachable branch detected.
- QD-P-1.4.3 | PASS | P0 | evidence: TC-051; no Skill definitions are declared in the artifact.
- QD-P-1.5.1 | PASS | P0 | evidence: TC-051; the three stages cover the orchestration objective.
- QD-P-1.5.2 | PASS | P0 | evidence: TC-051, choose_model; the model resource list is supplied via the "{{metas}}" placeholder.
- QD-P-1.6.1 | PASS | P0 | evidence: TC-051; no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | P0 | evidence: TC-051; no rule is keyed on unobservable internal state such as "when you are uncertain".
- QD-P-1.6.3 | PASS | P0 | evidence: TC-051, response_results; the "detail the process" and "filter out irrelevant information" rules do not form an unarbitrated soft-rule conflict.
- QD-P-1.6.4 | FAIL | P1 | evidence: TC-051, parse_task; excerpt: "Think step by step about all the tasks needed to resolve the user's request." - an internal reasoning procedure the model cannot guarantee.
- QD-P-1.6.5 | PASS | P1 | evidence: TC-051; no self-referential/recursive constraint.
- QD-P-1.6.6 | FAIL | P0 | evidence: TC-051, parse_task/prompt; excerpt: "The chat log [ {{context}} ] may contain the resources I mentioned." - unstated preconditions on {{context}}/{{input}} validity with no precondition check.
- QD-P-1.6.7 | PASS | P0 | evidence: TC-051; a single-pass parse per request, no knowledge-revision rule implicated.

### Part 2 - Completeness/security defects
- QD-P-2.1.1 | PASS | P2 | evidence: TC-051, tprompt; the three stage blocks follow a consistent "#1/#2/#4 ... Stage" form.
- QD-P-2.1.2 | PASS | P1 | evidence: TC-051; the "<GENERATED>-dep_id" reference convention is defined before use.
- QD-P-2.1.3 | PASS | P2 | evidence: TC-051; the stage structure (tprompt staging + prompt templates) is readable.
- QD-P-2.1.4 | PASS | P2 | evidence: TC-051; the parse_task prompt is verbose but not contradictory.
- QD-P-2.2.1 | PASS | P0 | evidence: TC-051, prompt; the input source is declared ("{{context}}", "{{input}}").
- QD-P-2.2.2 | FAIL | P0 | evidence: TC-051, parse_task; excerpt: "Now I input { {{input}} }" - no format, encoding, or size limit is declared for the injected input.
- QD-P-2.2.3 | FAIL | P0 | evidence: TC-051; required vs optional nature of "{{context}}", "{{input}}", "{{metas}}", "{{task}}" is not distinguished.
- QD-P-2.2.4 | FAIL | P0 | evidence: TC-051, choose_model; excerpt: "Please choose the most suitable model from {{metas}} for the task {{task}}." - no handling when {{metas}} or {{task}} is empty/missing.
- QD-P-2.3.1 | PASS | P0 | evidence: TC-051, parse_task/choose_model; the JSON output formats are declared with exact keys.
- QD-P-2.3.2 | PASS | P0 | evidence: TC-051, parse_task; the task object schema ("task", "id", "dep", "args") is specified.
- QD-P-2.3.3 | PASS | P0 | evidence: TC-051, choose_model; the "strict JSON format" constraint supplies an output-stability mechanism.
- QD-P-2.3.4 | FAIL | P0 | evidence: TC-051; no sensitive-data filtering, privacy handling, or security output constraint declared (absence confirmed).
- QD-P-2.4.1 | PASS | P0 | evidence: TC-051; the pipeline stages (parse -> choose -> execute -> respond) and the dependency ordering are enumerated.
- QD-P-2.4.2 | PASS | P0 | evidence: TC-051, choose_model; the external models used are declared via "{{metas}}".
- QD-P-2.4.3 | PASS | P0 | evidence: TC-051, parse_task; invocation sequencing is specified through the "dep"/"<GENERATED>-dep_id" convention.
- QD-P-2.5.1 | PASS | P0 | evidence: TC-051; no loop/recursion is declared, so no termination constraint is required.
- QD-P-2.5.2 | FAIL | P0 | evidence: TC-051; no prohibited operations, sensitive-data access boundary, or external access boundary declared (absence confirmed).
- QD-P-2.5.3 | PASS | P0 | evidence: TC-051; the assistant holds no declared data permissions to bound.
- QD-P-2.5.4 | PASS | P0 | evidence: TC-051, parse_task; the minimality rule names the arbitration ("while ensuring that the user request can be resolved").
- QD-P-2.5.5 | FAIL | P0 | evidence: TC-051; no frequency limit is declared for the number of model invocations across the task list.
- QD-P-2.6.1 | FAIL | P0 | evidence: TC-051; no handling is declared for external model-invocation failures (only the unparseable-input case is covered).
- QD-P-2.6.2 | FAIL | P0 | evidence: TC-051; no functional degradation or error-recovery strategy is declared (absence confirmed).
- QD-P-2.6.3 | PASS | P1 | evidence: TC-051; no retry mechanism is declared, so no unreasonable retry is present.
- QD-P-2.7.1 | PASS | P0 | evidence: TC-051, demos_or_presteps; per-stage few-shot demonstrations are declared.
- QD-P-2.7.2 | FAIL | P0 | evidence: TC-051; no counter-example is declared for the stages (absence confirmed).
- QD-P-2.7.3 | FAIL | P0 | evidence: TC-051; no boundary-case example (e.g. empty {{metas}}) is declared (absence confirmed).

### QC - embedded code (YAML carrier)
- QC-0.1 | PASS | P0 | evidence: TC-051, config block; the YAML parses (folded scalars, list-free mappings).
- QC-0.2 | PASS | P1 | evidence: TC-051; the code block is labeled ```yaml.
- QC-0.3 | PASS | P1 | evidence: TC-051; the config snippet is structurally complete.
- QC-1.1 | PASS | P1 | evidence: TC-051; no undefined name references in a config context.
- QC-1.2 | PASS | P2 | evidence: TC-051; no import statements, nothing invalid.
- QC-1.3 | PASS | P2 | evidence: TC-051; no deprecated API usage detected.
- QC-1.4 | PASS | P2 | evidence: TC-051; no argument type incompatibility detected.
- QC-2.1 | PASS | P1 | evidence: TC-051; no file handle opened.
- QC-2.2 | PASS | P2 | evidence: TC-051; no network connection opened.
- QC-2.3 | PASS | P2 | evidence: TC-051; no high-risk file/network/DB call in the config snippet.
- QC-3.1 | PASS | P2 | evidence: TC-051; no unused import.
- QC-3.2 | PASS | P1 | evidence: TC-051; no missing import.
- QC-3.3 | PASS | P2 | evidence: TC-051; no hardcoded demo credential/value ("model: text-davinci-003" is configuration).

Stage A summary: 47 applicable QD-P rules, 13 FAIL (11 P0, 2 P1, 0 P2); QC 13 items, 0 FAIL. P0 findings are carried forward and do not halt the flow.

## 3. Stage B - Cross-Artifact Inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. No cross results are invented.

## 4. Stage C - Gate-0 (admission to Permission)

Conditions verified per permission-checklist section 3.2:
- G0-1 (no unfixed P0 in Stage A): informational only; 11 P0 findings recorded and carried forward (does not gate in this non-blocking flow).
- G0-2 (no unfixed P0 in Stage B): informational only; Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): the controller declares stage roles ("Task Planning Stage", "Model Selection Stage", "Response Generation Stage"), so a responsibility baseline is locatable.
- G0-4 (each Tool Schema's name, description, and parameter descriptions are complete): unsatisfiable - the artifact set contains no Tool Schema, so no Tool-schema completeness can be verified.

Gate-0 result: Not passed - G0-4 (no Tool Schema present, so per-Tool completion of name/description/parameter descriptions cannot be verified).

## 5. Stage D - Permission Proportionality (QD-PM)

Not Executed - incomplete artifact set (precondition: full set Prompt + Skill + all Tool Schemas required; only a System Prompt is present).

## 6. Stage E - Risk Explicit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above. It is not a defect verdict and not a security conclusion. Explicit-P0/P1/P2 is a Risk-Explicit assessment.

Audit object: TC-051 System Prompt. Scan path: NL-A (sentence-by-sentence) -> NL-B (cross-sentence) -> NR-O (decode) -> NR-S (structure/field).

Risk Item Summary
- Total risk items: 0
- Explicit-P0 (Block release): 0 items
- Explicit-P1 (Fix / exemption): 0 items
- Explicit-P2 (Risk ledger): 0 items

Note: no explicit risk expression (external export instruction, security-constraint removal, credential/PII/secret, dangerous flag, or external callback) was found in the static text. Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact Outlook (candidate mapping, advisory only)

Advisory context only; this section does not change, soften, or escalate any Inspect verdict. Candidate language only; strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; only Stage E (Risk Explicit) and the Stage A lite embedded-code QC ran. Per relevance.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

| Defect ID (severity) | Candidate AS-* | Candidate FM-* | Candidate RAG metrics | Strength (provisional lite) |
|---|---|---|---|---|
| QD-P-1.3.2 (P1) | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Correctness, Relevance, Consistency, Format Compliance | Conditional - vague model-selection term |
| QD-P-1.6.4 (P1) | AS-01, AS-06, AS-07 | FM-01, FM-02, FM-07, FM-09 | Consistency, Robustness, Boundary Recognition, Safety Response | Conditional - internal reasoning-method constraint |
| QD-P-1.6.6 (P0) | AS-01, AS-06, AS-07 | FM-01, FM-02, FM-07, FM-09 | Consistency, Robustness, Boundary Recognition, Safety Response | Medium - unstated context/input preconditions |
| QD-P-2.2.2 (P0) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - unconstrained injected input format |
| QD-P-2.2.3 (P0) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - required/optional not distinguished |
| QD-P-2.2.4 (P0) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - missing-input path undefined |
| QD-P-2.3.4 (P0) | AS-03 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Medium - no privacy/sensitive-data output filtering |
| QD-P-2.5.2 (P0) | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no security boundary constraints declared |
| QD-P-2.5.5 (P0) | AS-06 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no resource invocation frequency limit |
| QD-P-2.6.1 (P0) | AS-07 | FM-08, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - runtime exceptions not covered |
| QD-P-2.6.2 (P0) | AS-07 | FM-08, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no degradation/recovery strategy |
| QD-P-2.7.2 (P0) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no counter-examples |
| QD-P-2.7.3 (P0) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no boundary-case examples |

Boundary reminders: candidate associations only ("may", "needs dynamic verification"); no causal claim is made. Single-defect mapping only (v1 scope); defect chains are out of scope.

## 8. Stage G - Self-Verification

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. All emitted QD-P / QC / EX IDs were confirmed against the reference files; no fabricated IDs; no causal wording in Stage F; no "secure"/"high quality" claim; no "Permission = ERROR/BLOCKED" wording. No in-place self-corrections were required.

## 9. Status Board

Stage A (Single-artifact):  Executed - System Prompt L3 inspection + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 risk items (Explicit-P0=0, Explicit-P1=0, Explicit-P2=0).
Stage F (Impact outlook):   Executed - candidate mapping for 13 Stage A FAILs (advisory only).
Stage G (Self-verification): Executed - ID back-closure OK, red-line wording OK, output contract OK.
