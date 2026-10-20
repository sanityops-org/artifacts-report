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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 9, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the `search`/`retrieve` tools and the render-spec tools are named but no JSON `parameters`/`inputSchema` schema is shown).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared for a search agent that drives search/retrieve tools.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking, and missing-input handling are all undeclared.
  4. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided in the quoted prompt text.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-103 bundles one coordinated single-agent suite (Morphic AI answer engine). Artifact types present, by structural signature:

- System Prompt (present, verbatim, 3 blocks): the identity guidance, the source-direction guidance and the Quick-mode system prompt in `lib/agents/prompts/search-mode-prompts.ts`. Basis: prose/instruction strings composed by `getIdentityGuidance()`, the source-direction block and `getQuickModePrompt()`.
- System Prompt (identified, not quoted, 1): the Adaptive-mode prompt is referenced ("Search modes: Quick and Adaptive") but its body was not retrieved; it is therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability (the artifacts are TypeScript prompt modules).
- Tool Schema (absent): `search` (with `include_domains`/`exclude_domains`), `retrieve` and the render-spec tools are named but no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the fenced prompt excerpts; no standalone executable source is quoted.
- Out of coverage: `researcher.ts`, `title-generator.ts`, `getImageSpecPrompt` / `getRelatedQuestionsSpecPrompt` and the Adaptive-mode prompt are described but not quoted.

Scope note: the identity block, the source-direction block and the Quick/Adaptive mode prompts are composed into one research agent (`createResearcher`), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (identity + source-direction + Quick-mode)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the agent drives 4+ tools (`search`, `retrieve`, and the generative-UI spec tools) and runs a search -> retrieve -> answer -> render-spec pipeline whose workflow exceeds 5 steps; it declares a conditional provider adjustment (`hasGeneralProvider`) and a defined fallback. Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the identity directive ("Never claim to be ChatGPT, Claude, Gemini ...") is consistent with the rest of the prompt.
- QD-P-1.1.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the domain-filter guidance ("Only apply domain filters when the user's intent clearly points to a source") does not conflict with the efficiency guideline.
- QD-P-1.1.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the worked mapping examples ("search reddit" -> `include_domains: ["reddit.com"]`) match the stated rule.
- QD-P-1.2.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the identity ("You are Morphic, an AI-powered answer engine") matches the responsibilities (grounded, cited answers).
- QD-P-1.2.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the voice and the fixed identity match the declared output style.
- QD-P-1.2.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the constraints (do not invent restrictions; do not name the underlying model) do not prohibit the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-103, search-mode-prompts.ts, quantities are bounded ("Use exactly one search tool call for informational questions without URLs").
- QD-P-1.3.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the vague term "clearly points to a source" is bounded by the worked domain examples beside it and is secondary, not a decision boundary.
- QD-P-1.3.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the filter boundary and fallback are declared ("Only apply domain filters when ..."; "Fallback: if a domain-restricted search returns too few or no results ...").
- QD-P-1.4.1 | PASS | evidence: TC-103, search-mode-prompts.ts, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the include/exclude/plain branches are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-103, search-mode-prompts.ts, no Skill definition is given in the prompt set (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the responsibilities (grounded, cited answers with optional domain direction) support the objective.
- QD-P-1.5.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the workflow resources (`search`, `retrieve`, render-spec tools) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-103, search-mode-prompts.ts, no vague word carries a security or permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-103, search-mode-prompts.ts, control flow keys on the user's stated source preference, not on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the efficiency guidance and the source-direction guidance do not interweave into an unarbitrated conflict.
- QD-P-1.6.4 | PASS | evidence: TC-103, search-mode-prompts.ts, no constraint fixes the model's internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-103, search-mode-prompts.ts, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-103, search-mode-prompts.ts, the availability of a general search provider is handled by `hasGeneralProvider` rather than assumed.
- QD-P-1.6.7 | PASS | evidence: TC-103, search-mode-prompts.ts, the prompt declares no multi-turn knowledge-update path (determination basis: per-query answer composition).
- QD-P-2.1.1 | PASS | evidence: TC-103, search-mode-prompts.ts, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the references (`include_domains` / `exclude_domains`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the composed section hierarchy (identity -> source direction -> instructions) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-103, search-mode-prompts.ts, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the input source is declared - the user's query and stated source preference.
- QD-P-2.2.2 | FAIL | evidence: TC-103, search-mode-prompts.ts, the input data format is unconstrained - the query carries no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-103, search-mode-prompts.ts, no input field is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-103, search-mode-prompts.ts, handling of missing input is undefined - no behavior is declared when the query is empty or malformed.
- QD-P-2.3.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the output contract is declared through the grounded/cited answer plus the generative-UI spec steps (the answer format is owned by the render prompts).
- QD-P-2.3.2 | PASS | evidence: TC-103, search-mode-prompts.ts, no free-text output schema is required (determination basis: the output structure is owned by the render-spec prompts referenced by the prompt).
- QD-P-2.3.3 | PASS | evidence: TC-103, search-mode-prompts.ts, the mode-specific efficiency budget bounds output consistency.
- QD-P-2.3.4 | FAIL | evidence: TC-103, search-mode-prompts.ts, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the search -> retrieve -> answer -> render-spec workflow is a complete step sequence.
- QD-P-2.4.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the resources/tools used are declared (`search`, `retrieve`, render-spec tools).
- QD-P-2.4.3 | PASS | evidence: TC-103, search-mode-prompts.ts, an invocation specification is given (pass `include_domains` / `exclude_domains` to the search tool only on clear source intent).
- QD-P-2.5.1 | PASS | evidence: TC-103, search-mode-prompts.ts, the Quick-mode one-call budget bounds execution and no loop is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-103, search-mode-prompts.ts, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-103, search-mode-prompts.ts, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-103, search-mode-prompts.ts, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-103, search-mode-prompts.ts, an invocation budget is declared ("Use exactly one search tool call ...").
- QD-P-2.6.1 | PASS | evidence: TC-103, search-mode-prompts.ts, a fallback is declared ("Fallback: if a domain-restricted search returns too few or no results ...").
- QD-P-2.6.2 | PASS | evidence: TC-103, search-mode-prompts.ts, the under-return fallback is a declared degradation path.
- QD-P-2.6.3 | PASS | evidence: TC-103, search-mode-prompts.ts, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-103, search-mode-prompts.ts, no representative positive worked interaction is provided (only inline mapping examples for parameter values).
- QD-P-2.7.2 | FAIL | evidence: TC-103, search-mode-prompts.ts, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-103, search-mode-prompts.ts, no boundary-case examples (empty query, ambiguous source intent) are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-103 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-103 carries no Tool Schema artifact (determination basis: `search`/`retrieve` and the render-spec tools are named with prose parameters but no JSON `parameters`/`inputSchema` schema is shown). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the fenced blocks contain prompt/instruction text, not standalone executable code.

- QC-0.1 | N/A | evidence: TC-103, the blocks carry prompt text (determination basis: no code snippet present).
- QC-0.2 | N/A | evidence: TC-103, no code snippet requiring a language identifier (determination basis: prompt-text blocks).
- QC-0.3 | N/A | evidence: TC-103, no standalone code to test for structural completeness (determination basis: prompt-text blocks).
- QC-0.4 | PASS | evidence: TC-103, the fenced blocks open and close correctly.
- QC-0.5 | N/A | evidence: TC-103, no code fence with a declared language (determination basis: prompt-text blocks).
- QC-1.1 | N/A | evidence: TC-103, no executable code with name references (determination basis: prompt-text blocks).
- QC-1.2 | Not Executed | evidence: TC-103, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-103, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-103, no function call with typed arguments (determination basis: prompt-text blocks).
- QC-2.1 | N/A | evidence: TC-103, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-103, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-103, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-103, no imports present (determination basis: prompt-text blocks).
- QC-3.2 | N/A | evidence: TC-103, no referenced symbols requiring imports (determination basis: prompt-text blocks).
- QC-3.3 | PASS | evidence: TC-103, the only literals are domain examples ("reddit.com", "pubmed.ncbi.nlm.nih.gov"); no credential, local path, or machine-specific value.
- QC-4.1 | N/A | evidence: TC-103, no snippet-parameter/declaration pair to compare (determination basis: no tool schema present).
- QC-4.2 | N/A | evidence: TC-103, no version/API drift to compare (determination basis: prompt-text blocks).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the identity, source-direction and Quick/Adaptive mode prompts are composed into a single research agent; no cyclic role orchestration is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the prompt states its role and scope (e.g. search-mode-prompts.ts "You are Morphic, an AI-powered answer engine." with the source-direction block).
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (tools are named with prose parameters only).

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

Audit object: TC-103 System Prompt set (identity + source-direction + Quick-mode).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The identity directive ("Never claim to be ChatGPT, Claude, Gemini ...") and the domain-filter guidance are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Relevance, Consistency, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, identity + source-direction + Quick-mode), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (prompt-text snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
