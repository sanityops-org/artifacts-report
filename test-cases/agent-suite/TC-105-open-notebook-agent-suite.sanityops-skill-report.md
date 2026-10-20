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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 10, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the document chat tool is referenced as "specialized tools" but no JSON `parameters`/`inputSchema` schema is shown).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared for a document-analysis agent.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking, and missing-input handling are all undeclared.
  4. QD-P-2.4.3 - No tool invocation specification is declared for the "specialized tools".
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-105 bundles one coordinated single-agent suite (Open Notebook research/podcast assistant). Artifact types present, by structural signature:

- System Prompt (present, verbatim, 2): the document-chat system prompt (`prompts/chat/system.jinja`) and the podcast-outline prompt (`prompts/podcast/outline.jinja`). Basis: Jinja instruction templates with `# SYSTEM ROLE` / `# CAPABILITIES` sections and a role declaration.
- System Prompt (identified, not quoted): the `ask/`, `pattern/`, `source_chat/` and `transformation/` prompt groups exist per the directory listing but their bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability (the artifacts are Jinja templates and Python graph code).
- Tool Schema (absent): the chat prompt references "specialized tools" for document analysis but no JSON `parameters`/`inputSchema` schema is quoted.
- Embedded code snippets (QC scope): the Jinja prompt templates, the `open_notebook/graphs/chat.py` Python excerpt and the `EpisodeProfile` model excerpt.
- Out of coverage: the `ask/`, `pattern/`, `source_chat/`, `transformation/` prompts, the podcast transcript/TTS stages and the `open_notebook/graphs/` package are described but not quoted.

Scope note: the chat prompt, the podcast-outline prompt and the chat graph are capabilities of one notebook-assistant suite, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (chat system + podcast outline)

Tier determination: **L2 Multi-turn Interactive**. Basis (any 2 or more of the L2 criteria): the chat assistant runs multi-turn dialogue over the workspace context and a limited set of document-query tools; the podcast pipeline (briefing -> outline -> transcript -> TTS) is a workflow of <= 5 steps with limited state management. Only one L3 criterion is present (an exception guard, `IncompleteGenerationError`), so the tier is L2. Upward-compatible L2 scope = 40 items.

- QD-P-1.1.1 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, the citation rule ("Do not make up documents or document ids") and the strict-output rule do not conflict with the stated role.
- QD-P-1.1.2 | PASS | evidence: TC-105, chat/system.jinja, no conflicting directives found.
- QD-P-1.1.3 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-105, chat/system.jinja, the identity ("a cognitive study assistant") matches the responsibilities (research and learn from workspace documents).
- QD-P-1.2.2 | PASS | evidence: TC-105, chat/system.jinja, the "academic rigor" voice matches the declared style.
- QD-P-1.2.3 | PASS | evidence: TC-105, chat/system.jinja, the constraints (cite real ids; do not make up documents) do not prohibit the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-105, podcast/outline.jinja, quantities are bounded ("a list of exactly {{ num_segments }} entries").
- QD-P-1.3.2 | PASS | evidence: TC-105, chat/system.jinja, "academic rigor" is a secondary descriptor, not an undefined decision boundary.
- QD-P-1.3.3 | PASS | evidence: TC-105, chat/system.jinja, the citing-instruction boundary ("Only use the ids of the documents that you have access through the query you made") is declared.
- QD-P-1.4.1 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-105, chat/system.jinja, the conditional branches ({% if notebook %}, {% if context %}) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no Skill definition is given in the prompt set (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-105, chat/system.jinja, the responsibilities support the objective (grounded document chat).
- QD-P-1.5.2 | PASS | evidence: TC-105, chat/system.jinja, the workflow resources (project context, selected documents, document-query tools) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-105, chat/system.jinja, no vague word carries a security or permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-105, chat/system.jinja, control flow keys on the query context and user intent, not on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-105, chat/system.jinja, the natural-dialogue and academic-rigor soft rules are not declared in mutual tension.
- QD-P-1.6.4 | PASS | evidence: TC-105, chat/system.jinja, no constraint fixes the model's internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-105, chat/system.jinja, the notebook/context inputs are handled conditionally rather than assumed.
- QD-P-1.6.7 | PASS | evidence: TC-105, chat/system.jinja, the prompt declares no knowledge-revision mechanism across turns (determination basis: multi-turn chat over a fixed context).
- QD-P-2.2.1 | PASS | evidence: TC-105, chat/system.jinja, the input source is declared - the user question plus the CONTEXT ("The user has selected this context to help you with your response").
- QD-P-2.2.2 | FAIL | evidence: TC-105, chat/system.jinja, the input data format is unconstrained - the context/notebook/query carry no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-105, chat/system.jinja, no input field is marked required or optional (no default handling declared).
- QD-P-2.2.4 | FAIL | evidence: TC-105, chat/system.jinja, handling of missing input is undefined - no behavior is declared when the question or context is absent.
- QD-P-2.3.1 | PASS | evidence: TC-105, chat/system.jinja, the output rules are declared (display math as "$$...$$", inline math as "$...$", cited references to searched documents).
- QD-P-2.3.2 | PASS | evidence: TC-105, podcast/outline.jinja, the output schema is declared ('a single root key "segments" whose value is a list of exactly {{ num_segments }} entries ... exactly three keys: "name" and "description" (strings) and "size"').
- QD-P-2.3.3 | PASS | evidence: TC-105, chat/system.jinja + graphs/chat.py, output stability is bounded by the strict-output rules and the `IncompleteGenerationError` guard on empty responses.
- QD-P-2.3.4 | FAIL | evidence: TC-105, chat/system.jinja, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-105, chat/system.jinja, the workflow steps are complete (identify query context and intent -> query the documents -> compose a cited answer).
- QD-P-2.4.2 | PASS | evidence: TC-105, chat/system.jinja, the resources/tools used are declared (project information, selected documents, the document-query tool).
- QD-P-2.4.3 | FAIL | evidence: TC-105, chat/system.jinja, no tool invocation specification is declared - the "specialized tools" are named with no parameter, sequence, or failure-handling specification.
- QD-P-2.5.1 | PASS | evidence: TC-105, chat/system.jinja, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-105, chat/system.jinja, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-105, chat/system.jinja, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-105, chat/system.jinja, no resource-invocation frequency issue is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no representative positive worked interaction is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-105, chat/system.jinja + podcast/outline.jinja, no boundary-case examples (empty context, fabricated id) are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-105 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability; the prompt library and graph code are not Skill definitions). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-105 carries no Tool Schema artifact (determination basis: the document-query "specialized tools" are referenced by description but no JSON `parameters`/`inputSchema` schema is shown). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the case embeds Jinja prompt templates and a Python excerpt (`open_notebook/graphs/chat.py`); the Python snippet is marked as an excerpt (the enclosing function is shown and elided with `...`).

- QC-0.1 | PASS | evidence: TC-105, graphs/chat.py, the shown `call_model_with_messages` function parses as valid Python.
- QC-0.2 | FAIL | evidence: TC-105, the `graphs/chat.py` block and the Jinja template blocks carry no explicit language identifier on the fence.
- QC-0.3 | PASS | evidence: TC-105, graphs/chat.py, the shown function body is complete enough to read (imports precede the excerpt and the tail is elided).
- QC-0.4 | PASS | evidence: TC-105, the fenced blocks open and close correctly.
- QC-0.5 | N/A | evidence: TC-105, no fence declares a language to compare against content (determination basis: no language identifier).
- QC-1.1 | N/A | evidence: TC-105, graphs/chat.py references project helpers (`Prompter`, `extract_text_content`, `clean_thinking_content`, `IncompleteGenerationError`) defined outside the shown excerpt (determination basis: excerpt).
- QC-1.2 | Not Executed | evidence: TC-105, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-105, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-105, no function call with clearly incompatible argument types (determination basis: excerpt).
- QC-2.1 | N/A | evidence: TC-105, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-105, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-105, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-105, imports are not shown in the excerpt (determination basis: excerpt).
- QC-3.2 | N/A | evidence: TC-105, referenced helpers are project modules imported above the excerpt (determination basis: excerpt).
- QC-3.3 | PASS | evidence: TC-105, the only literals are functional (e.g. `"source:randomstring"`, `"chat/system"`); no credential, local path, or machine-specific value.
- QC-4.1 | PASS | evidence: TC-105, graphs/chat.py renders `prompt_template="chat/system"`, matching the `prompts/chat/system.jinja` declaration.
- QC-4.2 | PASS | evidence: TC-105, no version/API drift between the snippet and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the chat, podcast, transformation and ask/pattern capabilities are separate prompt groups invoked by distinct graph nodes; no cyclic role orchestration is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the chat prompt states its role and scope (e.g. chat/system.jinja "You are a cognitive study assistant that helps users research and learn by engaging in focused discussions about documents in their workspace.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the document-query tools are only referenced by description).

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

Audit object: TC-105 System Prompt set (chat system + podcast outline) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The citation rule ("Do not make up documents or document ids") and the strict-output rule are integrity constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| (QC-0.2) | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Traceability, Consistency, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L2, chat system + podcast outline), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (Jinja templates + Python excerpt).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
