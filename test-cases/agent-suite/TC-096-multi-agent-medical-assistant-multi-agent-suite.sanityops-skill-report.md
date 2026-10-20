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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 9, P1 = 0, P2 = 0. The embedded-snippet QC adds one P1 finding (QC-3.2).
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the web-search/CV/orchestrator modules are described by module name only and show no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - the RAG prompt declares no security boundary and no permission-control boundary for a medical-consultation agent.
  2. QD-P-2.3.4 - no sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 - the retrieved-context input has no declared format and no required/optional marking.
  4. QD-P-2.3.3 - no output-stability assurance mechanism is declared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - no positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-096 bundles one coordinated multi-agent medical-consultation suite (LangGraph workflow: RAG agent, web-search processor agent, image-analysis agents, confidence router, guardrails, human-in-the-loop). Artifact types present, by structural signature:

- System Prompt (present, quoted, 1): the RAG agent's response prompt built in `agents/rag_agent/response_generator.py` (a `f"""..."""` instruction string), together with its embedded `response_format_instructions` and `table_instructions` blocks. Basis: prose/instruction strings assigned to a `prompt` variable.
- System Prompt (identified, not quoted, 3): the `web_search_processor_agent`, `image_analysis_agent`, and `agent_decision.py` orchestrator prompts exist per the directory/module structure and README but their bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): the web-search components (`pubmed_search.py`, `tavily_search.py`) and the CV models are described by module name only; no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the `f"""..."""` prompt-building string and the `_calculate_confidence(self, documents: List[Dict[str, Any]])` method quoted from `response_generator.py`.
- Out of coverage: `doc_parser.py`, `content_processor.py`, `query_expander.py`, `vectorstore_qdrant.py`, `reranker.py`, and the guardrails configuration are described but not quoted.

Scope note: every module is a sub-agent of the same orchestrated medical suite (shared LangGraph state, confidence-based handoff, shared guardrails). All artifacts belong to the same agent suite, so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (RAG agent)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the suite is a multi-agent orchestration (RAG + web search + CV + router + guardrails + human-in-the-loop) whose workflow exceeds 5 steps (query -> route -> retrieve/search/analyse -> guardrails -> human gate -> respond); it is security-sensitive (medical/patient data and clinical decision support); the orchestrator declares exception handling (human-in-the-loop validation via LangGraph `NodeInterrupt`). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-096, section 1 (RAG prompt + response_format_instructions), no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-096, section 1, the grounding rules ("Answer the query based ONLY on the information provided in the context", "Do not use prior knowledge") do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-096, section 1, the only worked example is the markdown-table skeleton, which matches the stated rule "Present tabular data using proper markdown table formatting with headers".
- QD-P-1.2.1 | PASS | evidence: TC-096, section 1, the role identity ("You are a medical assistant providing accurate information based on verified medical sources") matches the task ("answer the user's question thoroughly but concisely").
- QD-P-1.2.2 | PASS | evidence: TC-096, section 1, the role voice matches the output style rule (a structured markdown chatbot reply).
- QD-P-1.2.3 | PASS | evidence: TC-096, section 1, the constraints (context-only answering, no invented source links) do not prohibit the core answering responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-096, section 1, no misused quantifier found ("the last few messages", "top 3").
- QD-P-1.3.2 | PASS | evidence: TC-096, section 1, the vague terms found ("thoroughly but concisely", "Be concise and accurate") are secondary style descriptors, not decision boundaries.
- QD-P-1.3.3 | PASS | evidence: TC-096, section 1, a prohibition scope is declared ("Do not use prior knowledge not contained in the context", "Do not make up any source link").
- QD-P-1.4.1 | PASS | evidence: TC-096, section 1, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-096, section 1, both branches (answer present in context / not present) are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-096, section 1, no Skill definition is given in the prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-096, section 1, the responsibilities (answer from retrieved verified sources) support the objective of grounded medical Q&A.
- QD-P-1.5.2 | PASS | evidence: TC-096, section 1, the prompt reasons over the provided `{context}`; it declares no unresolved resource/tool invocation.
- QD-P-1.6.1 | PASS | evidence: TC-096, section 1, the vague words steer reply formatting ("if required", "if appropriate"), not a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-096, section 1, control flow keys on presence of the answer in context, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-096, section 1, the "thoroughly but concisely" soft rules are not declared in mutual tension.
- QD-P-1.6.4 | PASS | evidence: TC-096, section 1, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-096, section 1, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-096, section 1, the assumed availability of an answer in context fails gracefully ("acknowledge the limitations of the available information").
- QD-P-1.6.7 | PASS | evidence: TC-096, section 1, each turn re-grounds on freshly retrieved context and the insufficient-context rule applies (determination basis: per-turn retrieval, no stale-conclusion path declared).
- QD-P-2.1.1 | PASS | evidence: TC-096, section 1, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-096, section 1, the referenced inputs (`{chat_history}`, `{query}`, `{context}`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-096, section 1, the role / grounding instructions / table instructions / response-format hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-096, section 1, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-096, section 1, the input source is declared ("The user has asked the following question: {query}" and "I've retrieved the following information to help answer this question: {context}").
- QD-P-2.2.2 | FAIL | evidence: TC-096, section 1, the retrieved-context input format is unconstrained - the context may contain prose, tables and figures, but no format, encoding, or size limit is declared.
- QD-P-2.2.3 | FAIL | evidence: TC-096, section 1, no input is marked required or optional (the handling of an empty `{chat_history}` or `{context}` is not distinguished).
- QD-P-2.2.4 | PASS | evidence: TC-096, section 1, missing/insufficient input is handled - "If the context doesn't contain relevant information to answer the query, state: 'I don't have enough information to answer this question based on the provided context.'"
- QD-P-2.3.1 | PASS | evidence: TC-096, section 1, output format is declared ("a well-structured response with heading, sub-headings and tabular structure ... in markdown format").
- QD-P-2.3.2 | PASS | evidence: TC-096, section 1, the required output structure is described (headings, sub-headings, markdown tables, perfect values from context).
- QD-P-2.3.3 | FAIL | evidence: TC-096, section 1, no output-stability assurance mechanism is declared (no format/consistency check or repeat-run stability rule for the free-form markdown reply).
- QD-P-2.3.4 | FAIL | evidence: TC-096, section 1, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-096, section 1, the numbered instruction list is a complete sequence ending in a defined output.
- QD-P-2.4.2 | PASS | evidence: TC-096, section 1, the prompt invokes no tool (vacuous; retrieval is upstream).
- QD-P-2.4.3 | PASS | evidence: TC-096, section 1, no tool invocation is declared (vacuous).
- QD-P-2.5.1 | PASS | evidence: TC-096, section 1, no loop, retry, or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-096, section 1, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-096, section 1, no permission scope or privilege-escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-096, section 1, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-096, section 1, no resource invocation is declared (vacuous).
- QD-P-2.6.1 | PASS | evidence: TC-096, section 1, no external call is made in the prompt and the one applicable anomaly (insufficient context) is handled.
- QD-P-2.6.2 | PASS | evidence: TC-096, section 1, degradation is defined - insufficient context degrades to an explicit "not enough information" reply rather than fabrication.
- QD-P-2.6.3 | PASS | evidence: TC-096, section 1, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-096, section 1, no positive worked example is provided (only the markdown-table skeleton).
- QD-P-2.7.2 | FAIL | evidence: TC-096, section 1, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-096, section 1, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-096 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-096 carries no Tool Schema artifact (determination basis: the web-search and CV modules are described by module name only; no JSON `parameters`/`inputSchema` schema is present). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the `response_generator.py` snippets parse as valid Python (QC-0.1 PASS) and the fenced blocks declare `python` (QC-0.2 PASS).

- QC-0.1 | PASS | evidence: TC-096, section 1, the prompt string and the confidence method parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-096, both snippets are fenced as `python`.
- QC-0.3 | PASS | evidence: TC-096, section 1 and section 2, the prompt-building block and the `_calculate_confidence` method are complete bodies (not mid-statement truncation); the missing imports are recorded under QC-3.2.
- QC-0.4 | PASS | evidence: TC-096, all code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-096, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-096, the only names undefined within the snippets are the typing symbols `List`/`Dict`/`Any`; recorded once under QC-3.2.
- QC-1.2 | Not Executed | evidence: TC-096, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-096, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-096, the annotated call `documents: List[Dict[str, Any]]` is used consistently; no type-mismatched call.
- QC-2.1 | N/A | evidence: TC-096, no file-handle pattern in the snippets (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-096, no network-connection constructor in the snippets (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-096, no high-risk file/network/DB call in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-096, no import statement is present (determination basis: no import block shown).
- QC-3.2 | FAIL | evidence: TC-096, section 2, `List`, `Dict` and `Any` are referenced in `_calculate_confidence(self, documents: List[Dict[str, Any]])` but are never imported in the snippet.
- QC-3.3 | PASS | evidence: TC-096, the literals (`0.0`, `documents[:3]`, `"combined_score"`) are logic values, not demo credentials or machine-specific values.
- QC-4.1 | PASS | evidence: TC-096, the snippet uses the same field names as the prompt text (`context`, `query`).
- QC-4.2 | PASS | evidence: TC-096, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the RAG, web-search, and image-analysis agents are dispatched by a one-way confidence router with a human-in-the-loop gate; no cyclic role orchestration (Agent A calling Agent B and back) is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the RAG prompt states its role and scope (e.g. section 1 "You are a medical assistant providing accurate information based on verified medical sources." followed by the grounding rules).
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the web-search/CV modules are named only, with no parameter schema).

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

Audit object: TC-096 System Prompt (RAG agent) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit·P0 (Block release): 0 items
- Explicit·P1 (Fix / exemption): 0 items
- Explicit·P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The grounding rules ("Answer the query based ONLY on the information provided in the context", "Do not make up any source link") are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity undeclared) |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Traceability, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, RAG agent prompt), QD-S (N/A, no Skill), QD-T (N/A, no Tool Schema), QC (embedded snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
