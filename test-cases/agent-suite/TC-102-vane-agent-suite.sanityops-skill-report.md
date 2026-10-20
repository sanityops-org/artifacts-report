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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 8, P1 = 1, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; tools are referenced by name only and no JSON `parameters`/`inputSchema` schema is shown).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared for an orchestrator that drives web and uploaded-file tools.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking, and missing-input handling are all undeclared.
  4. QD-P-1.3.2 - Vague intensity qualifiers carry the research-depth boundary of the prompt.
  5. QD-P-2.6.2 / QD-P-2.7.3 - No degradation/recovery strategy and no boundary-case examples are declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-102 bundles one coordinated single-agent suite (Vane / former Perplexica search-answering engine). Artifact types present, by structural signature:

- System Prompt (present, verbatim, 2): the Speed-mode orchestrator prompt and the Quality-mode orchestrator prompt in `src/lib/prompts/search/researcher.ts`. Basis: prose/instruction strings with XML sections (`<goal>`, `<core_principle>`, `<response_protocol>`).
- System Prompt (identified, not quoted, 2): `writer.ts` (final-answer composition) and `classifier.ts` (query/source classification) are listed with byte sizes but their prompt bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability (the artifacts are TypeScript prompt modules and a directory listing).
- Tool Schema (absent): the tools are referenced by name only (`web_search`, `__reasoning_preamble`, `done`, the uploaded-files search tool) and no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the fenced prompt excerpts and the `<user_uploaded_files>` template fragment (containing `${fileDesc}`); no standalone executable source is quoted.
- Out of coverage: `writer.ts`, `classifier.ts`, and the `suggestions/` and `media/` prompt groups are described but not quoted.

Scope note: the Speed/Quality orchestrators, the writer and the classifier are role prompts of the same multi-mode search suite, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (Speed + Quality orchestrators)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the orchestrator drives 4+ tools (`web_search`, `__reasoning_preamble`, `done`, uploaded-files search) and runs an iterative reason-act loop ("iterative loop: __reasoning_preamble -> tool call(s) -> ... -> done") whose workflow exceeds 5 steps; it declares exception-handling-style anti-loop guidance. Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-102, researcher.ts (Speed + Quality), the directives "Never output text directly" and "only call tools" are mutually consistent, not exclusive.
- QD-P-1.1.2 | PASS | evidence: TC-102, researcher.ts, "use [web search] to ground answers even for seemingly basic facts" does not conflict with "keep queries targeted (max 3 per call)".
- QD-P-1.1.3 | PASS | evidence: TC-102, researcher.ts, the worked example ("Example 1: Unknown Subject ... Action: web_search [...] then done.") matches the tool-only rule.
- QD-P-1.2.1 | PASS | evidence: TC-102, researcher.ts, the "action orchestrator" identity matches the responsibility "fulfill user requests by selecting and executing the available tools".
- QD-P-1.2.2 | PASS | evidence: TC-102, researcher.ts, the tool-only output style matches the orchestrator role.
- QD-P-1.2.3 | PASS | evidence: TC-102, researcher.ts, the constraints (tool-only, no free-form replies) do not prohibit the core orchestration responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-102, researcher.ts, quantities are bounded ("You can call up to 10 tools total per turn", "max 3 per call").
- QD-P-1.3.2 | FAIL | evidence: TC-102, researcher.ts, vague intensity qualifiers carry the research-depth boundary - "Fulfill the user's request as quickly as possible"; "the most thorough, comprehensive research possible"; "be exhaustive".
- QD-P-1.3.3 | PASS | evidence: TC-102, researcher.ts, a prohibition scope is declared ("Do not invent tools. Do not return JSON.") and termination is defined by the `done` tool.
- QD-P-1.4.1 | PASS | evidence: TC-102, researcher.ts, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-102, researcher.ts, the reason-act branches are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-102, researcher.ts, no Skill definition is given in the orchestrator prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-102, researcher.ts, the responsibilities (select and execute tools) support the objective (fulfill the request).
- QD-P-1.5.2 | PASS | evidence: TC-102, researcher.ts, the tools are declared as injected via the `${actionDesc}` placeholder and the workflow only calls those tools.
- QD-P-1.6.1 | PASS | evidence: TC-102, researcher.ts, no vague word carries a security or permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-102, researcher.ts, control flow keys on tool results, not on unreportable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-102, researcher.ts, the depth-vs-efficiency tension is separated by mode (Speed vs Quality prompts), not interwoven without arbitration.
- QD-P-1.6.4 | PASS | evidence: TC-102, researcher.ts, the `__reasoning_preamble` rule constrains tool-call order, not the model's internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-102, researcher.ts, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-102, researcher.ts, the availability of web search is stated conditionally ("if you have web search, use it").
- QD-P-1.6.7 | PASS | evidence: TC-102, researcher.ts, the orchestrator runs once per request and declares no multi-turn knowledge-update path (determination basis: single-shot orchestration).
- QD-P-2.1.1 | PASS | evidence: TC-102, researcher.ts, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-102, researcher.ts, the references (`${actionDesc}`, `${fileDesc}`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-102, researcher.ts, the XML section hierarchy (`<goal>`, `<core_principle>`, `<examples>`, `<mistakes_to_avoid>`, `<response_protocol>`) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-102, researcher.ts, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-102, researcher.ts, the input source is declared - the user request plus the `<user_uploaded_files>` block ("The user has uploaded the following files ...").
- QD-P-2.2.2 | FAIL | evidence: TC-102, researcher.ts, the input data format is unconstrained - the user request and the uploaded files carry no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-102, researcher.ts, no input field is marked required or optional (no default or handling declared for the request or the uploaded files).
- QD-P-2.2.4 | FAIL | evidence: TC-102, researcher.ts, handling of missing input is undefined - no behavior is declared when the request is empty or the uploaded files are absent.
- QD-P-2.3.1 | PASS | evidence: TC-102, researcher.ts, the orchestrator output contract is declared ("NEVER output normal text to the user. ONLY call tools."); the cited prose answer is owned by the referenced `writer.ts`.
- QD-P-2.3.2 | PASS | evidence: TC-102, researcher.ts, no textual output schema is required for the tool-only orchestrator (determination basis: the answer schema is owned by the referenced writer prompt, not by the orchestrator).
- QD-P-2.3.3 | PASS | evidence: TC-102, researcher.ts, output stability is bounded by "NEVER output normal text" plus the fixed tool contract.
- QD-P-2.3.4 | FAIL | evidence: TC-102, researcher.ts, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-102, researcher.ts, the reason-act loop is a complete step sequence ending in the `done` tool.
- QD-P-2.4.2 | PASS | evidence: TC-102, researcher.ts, the resources/tools used are declared (`web_search`, `__reasoning_preamble`, `done`, the uploaded-files search tool).
- QD-P-2.4.3 | PASS | evidence: TC-102, researcher.ts, an invocation specification is given (`__reasoning_preamble` before every tool call; "max 3 [queries] per call").
- QD-P-2.5.1 | PASS | evidence: TC-102, researcher.ts, termination is declared (`done` required) with anti-loop guidance ("If 2-3 tool calls don't find something ... move on").
- QD-P-2.5.2 | FAIL | evidence: TC-102, researcher.ts, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-102, researcher.ts, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-102, researcher.ts, no unarbitrated soft-constraint conflict found within one prompt.
- QD-P-2.5.5 | PASS | evidence: TC-102, researcher.ts, an invocation budget is declared ("up to 10 tools total per turn"; "max 3 per call").
- QD-P-2.6.1 | PASS | evidence: TC-102, researcher.ts, a fallback is declared ("Default to web_search when information is missing or stale") together with the anti-loop rule.
- QD-P-2.6.2 | FAIL | evidence: TC-102, researcher.ts, no degradation or recovery strategy is declared for a tool or external-service failure.
- QD-P-2.6.3 | PASS | evidence: TC-102, researcher.ts, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | PASS | evidence: TC-102, researcher.ts, a positive worked example is provided ("## Example 1: Unknown Subject").
- QD-P-2.7.2 | PASS | evidence: TC-102, researcher.ts, error-pattern coverage is provided by `<mistakes_to_avoid>` ("Over-assuming", "Verification obsession", "Endless loops").
- QD-P-2.7.3 | FAIL | evidence: TC-102, researcher.ts, no boundary-case examples (empty input, extremely long input, anomalous input) are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-102 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-102 carries no Tool Schema artifact (determination basis: `web_search`, `__reasoning_preamble`, `done` and the uploaded-files search tool are named but no JSON `parameters`/`inputSchema` schema is shown). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the fenced blocks contain prompt/instruction text and one template fragment, not standalone executable code.

- QC-0.1 | N/A | evidence: TC-102, the blocks carry prompt text, not executable code (determination basis: no code snippet present).
- QC-0.2 | N/A | evidence: TC-102, no code snippet requiring a language identifier (determination basis: prompt-text blocks).
- QC-0.3 | N/A | evidence: TC-102, no standalone code to test for structural completeness (determination basis: prompt-text blocks).
- QC-0.4 | PASS | evidence: TC-102, the fenced blocks open and close correctly.
- QC-0.5 | N/A | evidence: TC-102, no code fence with a declared language (determination basis: prompt-text blocks).
- QC-1.1 | N/A | evidence: TC-102, no executable code with name references (determination basis: prompt-text blocks).
- QC-1.2 | Not Executed | evidence: TC-102, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-102, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-102, no function call with typed arguments (determination basis: prompt-text blocks).
- QC-2.1 | N/A | evidence: TC-102, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-102, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-102, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-102, no imports present (determination basis: prompt-text blocks).
- QC-3.2 | N/A | evidence: TC-102, no referenced symbols requiring imports (determination basis: prompt-text blocks).
- QC-3.3 | PASS | evidence: TC-102, the only literal is a template placeholder (`${fileDesc}`); no credential, local path, or machine-specific value.
- QC-4.1 | N/A | evidence: TC-102, no snippet-parameter/declaration pair to compare (determination basis: no tool schema present).
- QC-4.2 | N/A | evidence: TC-102, no version/API drift to compare (determination basis: prompt-text blocks).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the Speed/Quality orchestrators, the writer and the classifier are independent role prompts invoked per request; no cyclic role orchestration (Agent A calling Agent B and back) is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each orchestrator states its role and scope (e.g. researcher.ts "Assistant is an action orchestrator. Your job is to fulfill user requests by selecting and executing the available tools").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (tools are referenced by name only with no parameter schema).

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

Audit object: TC-102 System Prompt set (Speed + Quality orchestrators) + the embedded template fragment.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The tool-only contract ("Do not invent tools. Do not return JSON.") and the tool-call protocol are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional (depth boundary may drift between runs) |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, Speed + Quality orchestrators), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (prompt-text snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
