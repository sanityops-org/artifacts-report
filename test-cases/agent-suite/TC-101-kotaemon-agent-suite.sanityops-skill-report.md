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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 9, P1 = 0, P2 = 0. The embedded-snippet QC adds one P1 (QC-0.2) and one P1 (QC-3.2).
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the reasoning pipelines `ReactAgentPipeline`/`RewooAgentPipeline` are referenced by class name only, with no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - the QA prompts declare no security boundary and no permission-control boundary for multi-user document Q&A.
  2. QD-P-2.3.4 - no sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 - the retrieved-context input has no declared format and no required/optional marking.
  4. QD-P-2.3.3 - no output-stability assurance mechanism is declared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - no positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-101 bundles one document-QA RAG suite (kotaemon: 5 prompt templates, a ReAct and a ReWOO agent pipeline, and a hybrid retrieval/answer orchestration). Artifact types present, by structural signature:

- System Prompt (present, quoted, 5): `DEFAULT_QA_TEXT_PROMPT`, `DEFAULT_QA_TABLE_PROMPT`, `DEFAULT_QA_CHATBOT_PROMPT`, `DEFAULT_QA_FIGURE_PROMPT`, and `DEFAULT_REWRITE_PROMPT` from `libs/ktem/ktem/reasoning/simple.py`. Basis: prose/instruction strings assigned to prompt constants.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): the reasoning pipelines (`ReactAgentPipeline`, `RewooAgentPipeline`, `FullQAPipeline`, `FullDecomposeQAPipeline`) are registered by class name in `flowsettings.py`; no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the five prompt strings, the `KH_REASONINGS` registration block, the `PrepareEvidencePipeline` header, and the evidence-mode constants.
- Out of coverage: `react.py`, `rewoo.py`, `prompt_optimization/`, the hybrid retrievers, and the Gradio UI are described but not quoted.

Scope note: all five prompts plus the ReAct/ReWOO pipelines belong to the same kotaemon document-QA agent (one retrieval -> evidence -> optional rewrite/decompose -> answer -> citation chain), so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (5 QA/rewrite templates)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the agent runs a hybrid retrieval + reranking pipeline plus selectable agentic modes (ReAct, ReWOO) that invoke multiple tools (>3 tool invocations); the workflow exceeds 5 steps (retrieve -> rerank -> assemble evidence -> optional rewrite/decompose -> answer -> citation); it is security-sensitive (multi-user private-document access). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-101, sections 1.1-1.5, no mutually exclusive directive found.
- QD-P-1.1.2 | PASS | evidence: TC-101, sections 1.1-1.5, the context-grounding rules and the rewrite rules do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-101, sections 1.1-1.5, no worked example contradicts a rule (none is given).
- QD-P-1.2.1 | PASS | evidence: TC-101, sections 1.1-1.5, each template's task (answer from context / rephrase the question) matches its stated role.
- QD-P-1.2.2 | PASS | evidence: TC-101, sections 1.1-1.4, the answer style matches the declared behaviour ("answer ... in detail with clear explanation", "Keep the answer as concise as possible").
- QD-P-1.2.3 | PASS | evidence: TC-101, sections 1.1-1.5, the constraints (do not make up answers) do not prohibit the core answering responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-101, section 1.5, the rewrite instruction is bounded ("Maintain all information in the original question. Keep the question as concise as possible").
- QD-P-1.3.2 | PASS | evidence: TC-101, sections 1.1-1.4, the vague terms ("in detail with clear explanation") are secondary style descriptors.
- QD-P-1.3.3 | PASS | evidence: TC-101, section 1.1, a grounding boundary is declared ("Use the following pieces of context to answer the question").
- QD-P-1.4.1 | PASS | evidence: TC-101, sections 1.1-1.5, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-101, sections 1.1-1.4, both branches (answer present / unknown) are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-101, sections 1.1-1.5, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-101, sections 1.1-1.5, the responsibilities (answer, or rewrite the question) support the objective (grounded document Q&A).
- QD-P-1.5.2 | PASS | evidence: TC-101, section 1.1, the prompt reasons over the provided `{context}`; it declares no unresolved resource/tool invocation.
- QD-P-1.6.1 | PASS | evidence: TC-101, sections 1.1-1.5, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-101, sections 1.1-1.4, control flow keys on presence of the answer in context, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-101, sections 1.1-1.4, the "in detail" vs "as concise as possible" rules are applied per distinct templates (TEXT vs CHATBOT), not interwoven.
- QD-P-1.6.4 | PASS | evidence: TC-101, sections 1.1-1.5, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-101, sections 1.1-1.5, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-101, sections 1.1-1.4, the assumed availability of an answer in context fails gracefully ("If you don't know the answer, just say that you don't know").
- QD-P-1.6.7 | PASS | evidence: TC-101, both the rewrite and the decompose pipelines re-derive the question per turn (determination basis: a declared re-derivation path exists).
- QD-P-2.1.1 | PASS | evidence: TC-101, sections 1.1-1.5, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-101, sections 1.1-1.4, the referenced inputs (`{context}`, `{question}`, `{lang}`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-101, sections 1.1-1.5, the context / question / answer hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-101, sections 1.1-1.5, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-101, sections 1.1-1.4, the input sources are declared (retrieved `{context}` and the user `{question}`).
- QD-P-2.2.2 | FAIL | evidence: TC-101, sections 1.1-1.4, the retrieved-context input format is unconstrained (texts, tables and figures may be supplied, but no format, encoding, or size limit is declared).
- QD-P-2.2.3 | FAIL | evidence: TC-101, sections 1.1-1.4, no input is marked required or optional.
- QD-P-2.2.4 | PASS | evidence: TC-101, sections 1.1-1.4, insufficient input is handled - "If you don't know the answer, just say that you don't know".
- QD-P-2.3.1 | PASS | evidence: TC-101, sections 1.1-1.4, the answer is a text/markdown reply in the requested `{lang}` (format guidance present).
- QD-P-2.3.2 | PASS | evidence: TC-101, sections 1.1-1.4, no structured schema is required for a chat answer.
- QD-P-2.3.3 | FAIL | evidence: TC-101, sections 1.1-1.4, no output-stability assurance mechanism is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-101, sections 1.1-1.5, no sensitive-data filtering, privacy handling, or security output constraint is declared (despite multi-user private documents).
- QD-P-2.4.1 | PASS | evidence: TC-101, section 1.1, the answer flow is complete (use context -> answer / say unknown).
- QD-P-2.4.2 | PASS | evidence: TC-101, section 1.1, the prompt reasons over the provided `{context}`; no tool invocation is declared within the prompt (vacuous).
- QD-P-2.4.3 | PASS | evidence: TC-101, sections 1.1-1.4, no tool invocation is declared within the prompt (vacuous).
- QD-P-2.5.1 | PASS | evidence: TC-101, sections 1.1-1.5, no loop or recursion is declared in the prompts (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-101, sections 1.1-1.5, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-101, sections 1.1-1.5, no permission scope or privilege-escalation boundary is declared (multi-user per-document access is not bounded in the prompt).
- QD-P-2.5.4 | PASS | evidence: TC-101, sections 1.1-1.5, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-101, sections 1.1-1.5, no resource-invocation frequency limit is declared (determination basis: no unbounded invocation declared).
- QD-P-2.6.1 | PASS | evidence: TC-101, sections 1.1-1.4, no external call is made in the prompt and the applicable anomaly (unknown answer) is handled.
- QD-P-2.6.2 | PASS | evidence: TC-101, sections 1.1-1.4, degradation is defined (say "don't know" rather than fabricate).
- QD-P-2.6.3 | PASS | evidence: TC-101, sections 1.1-1.5, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-101, sections 1.1-1.5, no positive worked example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-101, sections 1.1-1.5, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-101, sections 1.1-1.5, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-101 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-101 carries no Tool Schema artifact (determination basis: the reasoning pipelines are registered by class name only, with no JSON `parameters`/`inputSchema` schema). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the `simple.py` / `flowsettings.py` snippets parse as valid Python; the `KH_REASONINGS` block declares `python`, but the prompt-string and evidence-mode blocks carry no language identifier.

- QC-0.1 | PASS | evidence: TC-101, sections 1-3, the snippets parse as valid Python syntax.
- QC-0.2 | FAIL | evidence: TC-101, sections 1.1-1.5 and 3, the prompt-string blocks and the evidence-mode block carry no explicit language identifier.
- QC-0.3 | PASS | evidence: TC-101, sections 1-3, each snippet is complete for its purpose (not truncated mid-statement).
- QC-0.4 | PASS | evidence: TC-101, all code fences open and close correctly.
- QC-0.5 | N/A | evidence: TC-101, the unlabeled blocks declare no language, so a language-content match cannot be assessed (determination basis: no declared language).
- QC-1.1 | PASS | evidence: TC-101, the only name undefined within the snippets is the base class `BaseComponent`; recorded once under QC-3.2.
- QC-1.2 | Not Executed | evidence: TC-101, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-101, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-101, `max_context_length: int = 32000` and the evidence-mode integers are used consistently; no type-mismatched call.
- QC-2.1 | N/A | evidence: TC-101, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-101, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-101, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-101, no import is present to check for unused modules (determination basis: no import block shown).
- QC-3.2 | FAIL | evidence: TC-101, section 3, `class PrepareEvidencePipeline(BaseComponent):` references `BaseComponent`, which is not imported or defined in the snippet.
- QC-3.3 | PASS | evidence: TC-101, the literals (`EVIDENCE_MODE_TEXT = 0`, `MAX_IMAGES = 10`, `max_context_length: int = 32000`) are configuration values, not demo credentials or machine-specific values.
- QC-4.1 | PASS | evidence: TC-101, the templates use the same placeholder names (`{context}`, `{question}`, `{lang}`) as the surrounding pipeline.
- QC-4.2 | PASS | evidence: TC-101, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the pipelines (`FullQAPipeline`, `FullDecomposeQAPipeline`, `ReactAgentPipeline`, `RewooAgentPipeline`) are selectable, sequential reasoning flows, not mutually-calling roles. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the prompts state the answering responsibility and its grounding boundary (e.g. section 1.1 "Use the following pieces of context to answer the question at the end ... If you don't know the answer, just say that you don't know").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the agent pipelines are registered by class name only, with no parameter schema).

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

Audit object: TC-101 System Prompt set (5 QA/rewrite templates) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit·P0 (Block release): 0 items
- Explicit·P1 (Fix / exemption): 0 items
- Explicit·P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The anti-hallucination clause ("don't try to make up an answer") and the `{lang}` output slot are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity undeclared) |
| QD-P-2.3.3, QD-P-2.3.4 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-0.2, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Relevance, Traceability, Format Compliance, Boundary Recognition. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 5 QA/rewrite templates), QD-S (N/A, no Skill), QD-T (N/A, no Tool Schema), QC (embedded snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
