> **STALE (2026-10-20)**: the inspected artifact was replaced with upstream-verified content. Re-run the inspection before using these findings.

# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (Gate-0 not satisfied / incomplete artifact set).
- Finding counts (Stage A + B): Inspect P0 = 37, P1 = 11, P2 = 5.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-PT-2.1 - Tools declared in the role prompts (init_research, plan_sections, run_research, review_draft, compile_report) do not exist in the provided Tool Schema list.
  2. QD-P-2.5.2 - No security boundary constraints are declared in any of the 8 role prompts.
  3. QD-P-2.4.3 - No tool invocation specification (parameters, sequence, failure handling) is declared for the referenced tools.
  4. QD-T-3.2 - publication_tools export functions accept a free-form `content` string passed directly downstream (raw-input passthrough).
  5. QD-P-2.5.1 - The Reviewer -> Revisor quality loop has no termination constraint (no maximum iteration count).
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-004 bundles one coordinated multi-agent suite (8 role prompts plus a shared tool surface plus configuration artifacts). Artifact types present, by structural signature:

- System Prompt (present, 8): the `system_message` text blocks for Chief Editor, Editor, Researcher, Reviewer, Revisor, Writer, Publisher, Human. Basis: prose/markdown instructions.
- Tool Schema (present, 3 tool sets): `research_tools`, `review_tools`, `publication_tools`. Basis: JSON objects with `name` + `description` + `parameters`.
- Skill (absent): no markdown file with `name`/`description` front matter defining an invokable capability.
- Configuration artifacts (task.json, ResearchState) are not one of the three Logic Artifact types; they are treated as embedded snippets/referenced material (QC scope only).

Scope note: all 8 roles are sub-agents of the same orchestrated system sharing one LangGraph `ResearchState`, so cross-artifact checks are run within this single suite; no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (8 role prompts)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool invocations are referenced across roles; the workflow exceeds 5 steps (planning -> research -> review -> revise -> write -> publish); multi-tool collaboration plus multi-agent orchestration. Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-004, sections 1.1-1.8, no mutually exclusive attributes found.
- QD-P-1.1.2 | PASS | evidence: TC-004, section 3.1 task.json guidelines ("MUST fully answer" / "MUST be written in apa format" / "MUST be written in english") do not conflict.
- QD-P-1.1.3 | FAIL | evidence: TC-004, section 1.4 Reviewer example `"overall_score": 7, ... "approval_status": "needs_revision"` conflicts with the rule "If score < 7, provide specific revision guidance".
- QD-P-1.2.1 | PASS | evidence: TC-004, sections 1.1-1.8, role identities match their stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-004, sections 1.1-1.8, no role output-style mismatch found.
- QD-P-1.2.3 | PASS | evidence: TC-004, sections 1.1-1.8, constraints do not prohibit core responsibilities.
- QD-P-1.3.1 | PASS | evidence: TC-004, section 1.3 "minimum 5 per section" is bounded.
- QD-P-1.3.2 | FAIL | evidence: TC-004, section 1.4 "Be thorough but constructive" is a vague qualifier.
- QD-P-1.3.3 | FAIL | evidence: TC-004, sections 1.1-1.8, no prohibition scope or handoff condition is declared (only responsibilities are stated).
- QD-P-1.4.1 | PASS | evidence: TC-004, sections 1.1-1.8, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-004, section 1.8 interaction modes are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-004, the prompts declare roles, not Skill definitions; no invalid Skill definition present (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-004, sections 1.1-1.8, responsibilities support each stated objective.
- QD-P-1.5.2 | FAIL | evidence: TC-004, section 1.1 lists tools "init_research / plan_sections / run_research / review_draft / compile_report" that have no corresponding resource definition.
- QD-P-1.6.1 | FAIL | evidence: TC-004, section 1.1 "Handle errors and edge cases gracefully" carries a critical decision with undefined criteria.
- QD-P-1.6.2 | FAIL | evidence: TC-004, section 1.5 "Re-submit for re-review if major changes made" depends on unobservable model judgment.
- QD-P-1.6.3 | FAIL | evidence: TC-004, section 1.6 "Maintain consistent terminology throughout" interweaves with "Ensure smooth transitions" with no arbitration.
- QD-P-1.6.4 | PASS | evidence: TC-004, sections 1.1-1.8, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-004, sections 1.1-1.8, no self-referential/recursive constraint text found.
- QD-P-1.6.6 | FAIL | evidence: TC-004, section 1.6 assumes sections and sources already exist with no precondition check.
- QD-P-1.6.7 | FAIL | evidence: TC-004, section 1.5 has no conclusion-revision mechanism when the user updates information.
- QD-P-2.1.1 | PASS | evidence: TC-004, sections 1.1-1.8, formatting is readable.
- QD-P-2.1.2 | FAIL | evidence: TC-004, section 1.3 "using the specified format (APA/MLA/etc.)" is a vague cross-reference.
- QD-P-2.1.3 | PASS | evidence: TC-004, sections 1.1-1.8, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-004, sections 1.1-1.8, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-004, each role declares its input (e.g., section 1.2 "Given a research query and initial findings").
- QD-P-2.2.2 | FAIL | evidence: TC-004, section 1.2 input "research query and initial findings" has no format/encoding declaration.
- QD-P-2.2.3 | FAIL | evidence: TC-004, sections 1.1-1.8, no required/optional marking on any input.
- QD-P-2.2.4 | FAIL | evidence: TC-004, sections 1.1-1.8, no missing-input handling declared.
- QD-P-2.3.1 | PASS | evidence: TC-004, output formats are declared (section 1.4 JSON; section 1.2 field list).
- QD-P-2.3.2 | PASS | evidence: TC-004, section 1.4 output fields are enumerated.
- QD-P-2.3.3 | FAIL | evidence: TC-004, sections 1.1-1.8, no output stability/consistency assurance declared.
- QD-P-2.3.4 | FAIL | evidence: TC-004, sections 1.1-1.8, no sensitive-data filtering or privacy handling declared.
- QD-P-2.4.1 | PASS | evidence: TC-004, sections 1.5-1.7 workflow steps are complete.
- QD-P-2.4.2 | PASS | evidence: TC-004, section 1.1 and 1.3 declare their tools.
- QD-P-2.4.3 | FAIL | evidence: TC-004, section 1.1 lists tool names only ("init_research: Initialize research...") with no parameter/sequence/failure spec.
- QD-P-2.5.1 | FAIL | evidence: TC-004, section 1.8 "Request revision - Loop back with feedback" has no maximum iteration count.
- QD-P-2.5.2 | FAIL | evidence: TC-004, sections 1.1-1.8, no prohibited operations or access boundaries declared.
- QD-P-2.5.3 | FAIL | evidence: TC-004, sections 1.1-1.8, no permission control boundary declared.
- QD-P-2.5.4 | FAIL | evidence: TC-004, sections 1.3/1.6, multiple soft constraints (source diversity vs currency) have no priority arbitration.
- QD-P-2.5.5 | FAIL | evidence: TC-004, sections 1.1-1.8, no invocation frequency limits declared.
- QD-P-2.6.1 | FAIL | evidence: TC-004, section 1.1 "Handle errors and edge cases gracefully" does not cover tool/parse/external exceptions.
- QD-P-2.6.2 | FAIL | evidence: TC-004, sections 1.1-1.8, no degradation or recovery strategy declared.
- QD-P-2.6.3 | PASS | evidence: TC-004, no retry mechanism is declared, so no unreasonable retry mechanism exists (not triggered).
- QD-P-2.7.1 | FAIL | evidence: TC-004, most role prompts (Editor, Writer, Publisher) provide no positive examples.
- QD-P-2.7.2 | FAIL | evidence: TC-004, sections 1.1-1.8, no counter-examples provided.
- QD-P-2.7.3 | FAIL | evidence: TC-004, sections 1.1-1.8, no boundary-case examples provided.

### 3.A.2 Tool Schema - `research_tools`

Tier: **L1** (read-only). Basis: `web_search` and `local_document_search` are read-only queries with no state change. Scope = L1 minimal set (7 items).

- QD-T-1.1 | FAIL | evidence: TC-004, section 2.1 `{"name": "web_search", "parameters": {...}}` has no `description` and no `inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-004, section 2.1 has no `required` array; `query` is not listed as required.
- QD-T-1.3 | PASS | evidence: TC-004, section 2.1 `"enum": ["tavily", "google", "bing"]` has no duplicate/empty values.
- QD-T-1.4 | FAIL | evidence: TC-004, section 2.1 parameter object has `properties` but no `"additionalProperties": false`.
- QD-T-2.1 | FAIL | evidence: TC-004, section 2.1 `"query": {"type": "string"}` has no `maxLength`/`minLength`.
- QD-T-2.3 | FAIL | evidence: TC-004, section 2.1 `"max_results": {"type": "integer", "default": 10}` has no `minimum`/`maximum`.
- QD-T-4.1 | FAIL | evidence: TC-004, section 2.1 `web_search` has no description text.

### 3.A.3 Tool Schema - `review_tools`

Tier: **L1** (read-only scoring, no state change). Scope = L1 minimal set (7 items).

- QD-T-1.1 | FAIL | evidence: TC-004, section 2.2 `evaluate_draft` has no `description` and no `inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-004, section 2.2 has no `required` array; `draft_content` is not listed as required.
- QD-T-1.3 | PASS | evidence: TC-004, section 2.2 `"enum": ["accuracy", "completeness", "coherence", "sources", "objectivity"]` is valid.
- QD-T-1.4 | FAIL | evidence: TC-004, section 2.2 parameter object has no `additionalProperties` declaration.
- QD-T-2.1 | FAIL | evidence: TC-004, section 2.2 `"draft_content": {"type": "string"}` has no length bound.
- QD-T-2.3 | PASS | evidence: TC-004, section 2.2 `returns.score` has `"minimum": 1, "maximum": 10`; no boundary-less number parameter.
- QD-T-4.1 | FAIL | evidence: TC-004, section 2.2 `evaluate_draft` has no description text.

### 3.A.4 Tool Schema - `publication_tools`

Tier: **L2** (creates output files; recoverable write). Basis: `export_markdown`/`export_pdf`/`export_docx` create files = write operations -> L2 minimum. Scope = L2 minimal set (12 items).

- QD-T-1.1 | FAIL | evidence: TC-004, section 2.3 `export_markdown` etc. have no `description` and no `inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-004, section 2.3 has no `required` array; `content` is not listed as required.
- QD-T-1.3 | PASS | evidence: TC-004, section 2.3 `"enum": ["academic", "business"]` is valid.
- QD-T-1.4 | FAIL | evidence: TC-004, section 2.3 parameter object has no `additionalProperties` declaration.
- QD-T-2.1 | FAIL | evidence: TC-004, section 2.3 `"content": "string"` has no length bound.
- QD-T-2.2 | PASS | evidence: TC-004, section 2.3 no string parameter requiring a specific format is present.
- QD-T-2.3 | N/A | evidence: TC-004, section 2.3 contains no number-type parameter (determination basis: no such parameter exists).
- QD-T-2.4 | N/A | evidence: TC-004, section 2.3 contains no array-type parameter (determination basis: no such parameter exists).
- QD-T-3.1 | FAIL | evidence: TC-004, section 2.3 export functions modify the filesystem but their (absent) descriptions carry no write-operation notice.
- QD-T-3.2 | FAIL | evidence: TC-004, section 2.3 `"content": "string"` accepts raw free-form input passed directly to output generation.
- QD-T-4.1 | FAIL | evidence: TC-004, section 2.3 `export_markdown` etc. have no description text.
- QD-T-4.2 | FAIL | evidence: TC-004, section 2.3 file-creation side effect is not declared in any description.

### 3.A.5 Embedded code snippets (QC)

QC-0 baseline: syntax parses for the assignment snippets and the JSON schemas (QC-0.1 PASS); language identifiers present `python`/`json` (QC-0.2 PASS). QC-0.3 for the `ResearchState` snippet fails, so QC-1..QC-3 below are reported as advisory for the parsable snippets only.

- QC-0.1 | PASS | evidence: TC-004, sections 1.1-1.8 and 3.2 snippets parse as valid Python/JSON.
- QC-0.2 | PASS | evidence: TC-004, fenced blocks declare `python`/`json`.
- QC-0.3 | FAIL | evidence: TC-004, section 3.2 `class ResearchState(TypedDict)` uses `BaseMessage`, `List`, `Dict`, `Literal`, `Annotated`, `operator` with no imports shown (fragment).
- QC-1.1 | PASS | evidence: TC-004, no undefined names beyond the un-imported symbols; reported under QC-3.2.
- QC-1.2 | PASS | evidence: TC-004, no unavailable-module import statements present.
- QC-1.3 | PASS | evidence: TC-004, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-004, no type-mismatched call present in snippets.
- QC-2.1 | N/A | evidence: TC-004, no file-handle pattern in snippets (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-004, no network-connection constructor in snippets (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-004, no high-risk file/network/DB call in snippets (determination basis: no such pattern).
- QC-3.1 | PASS | evidence: TC-004, no unused imports present.
- QC-3.2 | FAIL | evidence: TC-004, section 3.2 `class ResearchState(TypedDict)` references `TypedDict` and `BaseMessage` without an import statement.
- QC-3.3 | PASS | evidence: TC-004, no hardcoded demo credential value present in snippets.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: 2 of 3 artifact types from the same suite are present (System Prompt + Tool Schema). No Skill is present, so QD-PS (Prompt -> Skill) and QD-ST (Skill <-> Tool) are N/A.

Tier: **L3** (suite). Evaluation scope = L3 full; Appendix C upgrades applied (Agent L3 -> global P1->P0, P2->P1).

- QD-PT-2.1 Tool Existence | FAIL (P0) | evidence: Prompt (TC-004, section 1.1) declares "run_research"; Tool Schema (section 2.1-2.3) lists only `web_search`, `local_document_search`, `evaluate_draft`, `export_markdown/pdf/docx` - the declared tool does not exist.
- QD-PT-2.2 Invocation Specification Consistency | FAIL (P0) | evidence: Prompt (section 1.1) lists tool names only; Tool Schema (section 2.1-2.3) defines `parameters` - the invocation method does not match the Schema.
- QD-PT-2.3 Parameter Constraint Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (section 1.1) declares no parameter constraints; Tool Schema (section 2.1) defines `query`/`max_results`/`source`.
- QD-PT-2.4 Permission Granularity Consistency | N/A | evidence: no RS-3 (high-risk) tool among the provided Tool Schemas (determination basis: none of the provided tools is irreversible/sensitive).
- QD-PT-2.5 Error Handling Completeness | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (section 1.1) "Handle errors and edge cases gracefully"; Tool Schema (section 2.1) does not define error types.
- QD-PT-2.6 Invocation Frequency Reasonableness | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt (sections 1.1-1.3) declares no frequency limit; Tool Schema (section 2.1) `max_results` is the only quantity limit.
- QD-CYC-1.1 Cross-Artifact Circular Invocation | N/A | evidence: no Skill artifact present to form a Prompt/Skill/Tool invocation loop (determination basis: Skill absent).
- QD-CYC-1.2 Multi-Agent Circular Invocation | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt Reviewer (section 1.4) emits `"approval_status": "needs_revision"` and Revisor (section 1.5) "Re-submit for re-review if major changes made" form a Reviewer <-> Revisor loop with no termination condition.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each role prompt states its role and responsibilities (e.g., section 1.4 "You are a critical research reviewer").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - the tool definitions lack `description` fields and parameter descriptions (sections 2.1-2.3).

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (sections 2.1-2.3).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-004 System Prompt set + Tool Schemas + embedded config snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (e.g., self-contained exfiltration, identity/permission claim, constraint removal, dangerous flag, hardcoded credential/PII, abnormal callback) was found in the static artifact text. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.1.3 | AS-01, AS-04, AS-05 | FM-01, FM-02, FM-07, FM-09 | Medium (example-vs-rule gap may steer behavior) |
| QD-P-1.3.2, QD-P-1.3.3 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-1.5.2, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong (workflow tools have no declaration) |
| QD-P-1.6.1, QD-P-1.6.2, QD-P-1.6.3, QD-P-1.6.6, QD-P-1.6.7 | AS-01, AS-06, AS-07 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.1.2 | AS-09 | FM-06 | Conditional |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3, QD-P-2.3.4 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.5.1, QD-P-2.5.4, QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Strong (no termination/frequency bound; loop in section 1.8) |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-T-1.1, QD-T-1.2 | AS-05, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-T-1.4 | AS-02, AS-04 | FM-03, FM-04, FM-05 | Medium |
| QD-T-2.1, QD-T-2.3 | AS-02, AS-06 | FM-03, FM-04, FM-05 | Medium |
| QD-T-3.1, QD-T-4.2 | AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-T-3.2 | AS-02 | FM-08, FM-09, FM-10 | Strong (raw content passthrough) |
| QD-T-4.1 | AS-05, AS-08 | FM-03, FM-05 | Conditional |
| QC-0.3, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QD-PT-2.1, QD-PT-2.2, QD-PT-2.3 | AS-02, AS-05, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong (declared tools do not exist) |
| QD-PT-2.5, QD-PT-2.6 | AS-06, AS-07 | FM-04, FM-05, FM-06, FM-08 | Medium |
| QD-CYC-1.2 | (QD-CYC has no dedicated Appendix A row; mapped to Cross contract group) | FM-04, FM-05, FM-06, FM-08 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Consistency, Robustness, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, System Prompt set), QD-T (3 tool sets), QC (embedded snippets).
Stage B (Cross):            Executed - 2 same-suite artifact types present (System Prompt + Tool Schema).
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
