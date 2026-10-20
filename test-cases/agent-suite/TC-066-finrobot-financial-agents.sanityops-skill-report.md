# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one Logic Artifact type is present). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A, System Prompt set): Inspect P0 = 11, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.2.2 / QD-P-2.2.3 - The upstream analysis payload and the evidence set carry no declared input format and no required/optional marking.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared for a financial pipeline.
  3. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared.
  4. QD-P-2.6.1 - Tool/valuation failure handling is not declared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A (no embedded code was found).
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-066 bundles one coordinated multi-agent equity-research suite (FinRobot). Artifact types present, by structural signature:

- System Prompt (present, 3 verbatim): the role instruction prompts `analysis_agent.md` (peer/comps analyst), `report_agent.md` (report editor) and `bull_agent.md` (long-side investment-committee PM). Basis: prose/instruction text prepended to each specialized agent.
- Skill (absent): the case's "Skill Definitions" section holds reference tables (agent role matrix, number-labeling contract, structured uncertainty fields). Basis: none is a markdown file with `name`/`description` front matter.
- Tool Schema (absent): the evidence set and structured fields (`price_target`, `warnings`, `peer_analysis.median_*`) are data contracts, not JSON function-calling schemas (`parameters` + `description`). Basis: no schema object is present.
- Embedded code snippets (QC scope): none found in the three prompt bodies (confirmed after full read).
- Out of coverage: the deterministic compute layer, the render layer and the verification layer are referenced but not quoted.

Scope note: the analyst, the editor and the investment-committee PM are roles of one orchestrated research pipeline (analysis -> report -> committee), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (financial-agent roles)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the suite is a multi-agent orchestration (analyst -> editor -> long-side committee member) whose pipeline exceeds 5 steps and is grounded in a deterministic compute/render/verification layer; it is finance-sensitive (it produces equity research and investment arguments). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-066, analysis_agent.md / report_agent.md / bull_agent.md, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-066, report_agent.md, the "polished professional report" directive and the "never smooth uncertainty" directive are arbitrated ("Manufacturing confidence ... is the worst failure this report can have").
- QD-P-1.1.3 | PASS | evidence: TC-066, analysis_agent.md / report_agent.md / bull_agent.md, no worked example contradicts a rule (no worked examples are given).
- QD-P-1.2.1 | PASS | evidence: TC-066, analysis_agent.md / report_agent.md / bull_agent.md, each role identity matches its stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-066, bull_agent.md, the persona voice matches the declared output ("long-side PM in an investment-bank style, concise and forceful").
- QD-P-1.2.3 | PASS | evidence: TC-066, analysis_agent.md / report_agent.md / bull_agent.md, the constraints (no self-authored numbers, no new analysis) do not prohibit the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-066, analysis_agent.md + bull_agent.md, quantities are bounded ("Identify 3-5 relevant peer companies", "up to 5").
- QD-P-1.3.2 | PASS | evidence: TC-066, report_agent.md, the vague terms found ("polished, professional", "no filler") are secondary style descriptors, not a decision boundary.
- QD-P-1.3.3 | PASS | evidence: TC-066, report_agent.md + bull_agent.md, boundaries are defined (what the editor must not infer; what the bull agent may not cite).
- QD-P-1.4.1 | PASS | evidence: TC-066, the three prompts, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-066, bull_agent.md, the empty-arguments branch is reachable ("if nothing is supportable, return an empty arguments list").
- QD-P-1.4.3 | PASS | evidence: TC-066, the three prompts, no Skill definition is given in the prompt set (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-066, the three prompts, the responsibilities support the objectives (analyst analysis; editor assembly; bull argumentation).
- QD-P-1.5.2 | PASS | evidence: TC-066, report_agent.md, the workflow resources (prior-step structured output, tool output) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-066, the three prompts, the decision conditions (withheld target, outlier methods, data warnings) are explicitly enumerated.
- QD-P-1.6.2 | PASS | evidence: TC-066, bull_agent.md, argumentation is keyed on the evidence set, not on unreportable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-066, report_agent.md, the soft rules (concise + complete uncertainty) are arbitrated by an explicit priority.
- QD-P-1.6.4 | PASS | evidence: TC-066, the three prompts, no constraint fixes an internal reasoning method beyond the stated rules.
- QD-P-1.6.5 | PASS | evidence: TC-066, the three prompts, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-066, report_agent.md + bull_agent.md, the assumed availability of prior-step/structured data is handled (withheld target, empty evidence set).
- QD-P-1.6.7 | PASS | evidence: TC-066, the three prompts, each role runs once per pipeline stage and declares no multi-turn knowledge-update path (determination basis: single-shot pipeline stages).
- QD-P-2.1.1 | PASS | evidence: TC-066, the three prompts, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-066, the three prompts, the referenced entities (evidence_id, price_target, outlier_methods, warnings) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-066, the three prompts, the hierarchy (role -> number discipline -> uncertainty -> output format) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-066, the three prompts, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-066, analysis_agent.md + bull_agent.md, the input source is declared ("All numbers must come from the prompt context or tool output"; "the given deterministic evidence set").
- QD-P-2.2.2 | FAIL | evidence: TC-066, report_agent.md + bull_agent.md, the input format is unconstrained - the prior-step payload is referenced only as "previous-step data" / "structured output" with no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-066, bull_agent.md, no required/optional marking for the evidence-set fields (evidence_id / label / value / unit) or for the prior-step sections.
- QD-P-2.2.4 | PASS | evidence: TC-066, report_agent.md + bull_agent.md, missing input is handled (withheld `price_target`; empty evidence set returns an empty list).
- QD-P-2.3.1 | PASS | evidence: TC-066, report_agent.md, the output format is declared (Markdown with headers/tables; standard section list).
- QD-P-2.3.2 | PASS | evidence: TC-066, report_agent.md + bull_agent.md, the output schema is described (sections; SideCase with side="bull" and an arguments list).
- QD-P-2.3.3 | PASS | evidence: TC-066, report_agent.md, output stability is bounded by the fixed section list and "numbers consistent across sections".
- QD-P-2.3.4 | FAIL | evidence: TC-066, analysis_agent.md / report_agent.md / bull_agent.md, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-066, the three prompts, the workflow steps for each role are complete.
- QD-P-2.4.2 | PASS | evidence: TC-066, analysis_agent.md, the resources used (prompt context, tool output, skill methodology) are declared.
- QD-P-2.4.3 | FAIL | evidence: TC-066, analysis_agent.md / bull_agent.md, no tool invocation specification is given - the analyst invokes "tool output" and the bull agent cites evidence_ids through a "render layer", with no parameter/invocation spec.
- QD-P-2.5.1 | PASS | evidence: TC-066, the three prompts, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-066, the three prompts, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-066, the three prompts, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-066, report_agent.md + bull_agent.md, the potentially conflicting rules (up to 5 points; evidence required) are arbitrated.
- QD-P-2.5.5 | PASS | evidence: TC-066, the three prompts, no resource/resource-invocation frequency is declared by the roles themselves (vacuous).
- QD-P-2.6.1 | FAIL | evidence: TC-066, the three prompts, runtime exception handling is not declared (tool failure, valuation/data parsing failure have no defined behavior).
- QD-P-2.6.2 | FAIL | evidence: TC-066, the three prompts, no explicit degradation or recovery strategy is declared for pipeline-stage failure.
- QD-P-2.6.3 | PASS | evidence: TC-066, the three prompts, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-066, the three prompts, no positive worked example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-066, the three prompts, no counter-examples are provided (the prompts describe forbidden behavior but give no worked negative examples).
- QD-P-2.7.3 | FAIL | evidence: TC-066, the three prompts, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-066 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability; the "Skill Definitions" tables are reference material). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-066 carries no Tool Schema artifact (determination basis: the evidence set and structured fields are data contracts, not JSON `parameters`+`description` schemas). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

- QC-0.1 .. QC-4.2 | N/A | evidence: TC-066, the three prompt bodies contain no embedded code snippets (determination basis: the artifacts are pure markdown prose; the QC entry gate has no snippet to evaluate). No QC verdict is emitted as PASS/FAIL.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the analyst, editor and committee member are sequential roles in one pipeline (analysis -> report -> committee), with no cyclic role orchestration declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each role prompt states its role and scope (e.g. analysis_agent.md "You are an equity research analyst specializing in peer analysis and comparable company evaluation."; bull_agent.md "You are the long-side PM on the investment committee.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill, no Tool Schema).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-066 System Prompt set (analysis_agent, report_agent, bull_agent).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The anti-fabrication rules (no memory-recalled figures; no self-authored numbers; no invented evidence_ids) are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A (no snippets). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Traceability, Robustness, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, analysis/report/bull prompts), QD-S (N/A, no Skill), QD-T (N/A, no Tool Schema), QC (N/A, no embedded snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
