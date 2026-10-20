# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one Logic Artifact type is present). Stage D did not run (Gate-0 not satisfied / incomplete artifact set).
- Finding counts (Stage A): QD-P = Not Applicable (no System Prompt text is provided); embedded-code QC: P0 = 0, P1 = 1, P2 = 0.
- Gate-0 result: Not passed (G0-3 not satisfied - no responsibility boundary statement is locatable in a provided Logic Artifact; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P - Not Applicable: no System Prompt body is quoted in the case (the prompt components are referenced only), so no QD-P verdict is emitted.
  2. QC-0.2 - The embedded Python snippet (`prompt_helper.py`) carries no explicit language identifier on its fence.
  3. Gate-0 G0-3 - The responsibility baseline is not locatable in a Logic Artifact (only dispatch code and README prose are provided).
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-106 bundles one single-agent suite (PrivateGPT local-AI application layer). Artifact types present, by structural signature:

- System Prompt (identified, not quoted): `private_gpt/components/prompts/` is verified as a directory (prompt components), and prompt-style dispatch is wired in `private_gpt/components/llm/prompt_helper.py`, but no natural-language system-prompt body is quoted. Basis: the retrieved files are a Python dispatch helper, directory listings and README prose; no instruction string is provided. It is therefore not inspected and no QD-P verdict is emitted.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability (the artifacts are Python code, a markdown capability table and a directory listing).
- Tool Schema (absent): the README's Claude-API compatibility table lists capabilities (web search, web fetch, code execution, database querying, CSV analysis) but no JSON `parameters`/`inputSchema` schema is quoted.
- Embedded code snippets (QC scope): the `private_gpt/components/llm/prompt_helper.py` Python excerpt and the README capability table.
- Out of coverage: the built-in tool components (`code_execution/`, `database/`, `multimodality/`, `files/`), the chat processors and the MCP connectors are described but not quoted.

Scope note: the tools, prompt components and skills are features of one application layer (the PrivateGPT workbench assistant), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt

- QD-P-1.x .. QD-P-2.x | N/A | evidence: TC-106 provides no System Prompt body (determination basis: only `prompt_helper.py` dispatch code, directory listings and README prose are retrieved; the prompt components are referenced but their instruction text is not quoted). No QD-P verdict is emitted.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-106 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability; the capability table is README reference material). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-106 carries no Tool Schema artifact (determination basis: the Claude-API compatibility table lists capability names, not JSON `parameters`/`inputSchema` schemas). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the case embeds one Python excerpt (`prompt_helper.py`) showing the `get_prompt_style` dispatch function.

- QC-0.1 | PASS | evidence: TC-106, prompt_helper.py, the `get_prompt_style` function parses as valid Python.
- QC-0.2 | FAIL | evidence: TC-106, the `prompt_helper.py` block carries no explicit language identifier on the fence.
- QC-0.3 | PASS | evidence: TC-106, prompt_helper.py, the shown function (signature, docstring, local import, return) is complete and is not truncated.
- QC-0.4 | PASS | evidence: TC-106, the fenced block opens and closes correctly.
- QC-0.5 | N/A | evidence: TC-106, no fence declares a language to compare against content (determination basis: no language identifier).
- QC-1.1 | N/A | evidence: TC-106, prompt_helper.py references `Any` and `PromptStyleBase`, which are defined/imported outside the shown excerpt (determination basis: excerpt).
- QC-1.2 | Not Executed | evidence: TC-106, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-106, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-106, no function call with clearly incompatible argument types (determination basis: excerpt).
- QC-2.1 | N/A | evidence: TC-106, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-106, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-106, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-106, no unused import shown (the only import is a local, used import; determination basis: excerpt).
- QC-3.2 | N/A | evidence: TC-106, referenced symbols are project modules imported above the excerpt (determination basis: excerpt).
- QC-3.3 | PASS | evidence: TC-106, the only literals are functional (module path, style name); no credential, local path, or machine-specific value.
- QC-4.1 | N/A | evidence: TC-106, no snippet-parameter/declaration pair to compare (determination basis: no tool schema present).
- QC-4.2 | N/A | evidence: TC-106, no version/API drift to compare (determination basis: single dispatch helper).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: no Prompt/Skill/Tool pair exists (no System Prompt body, no Skill, no Tool Schema are provided), so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the README describes a single application-layer assistant (chat, tools, skills) with no multi-agent role orchestration declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): NOT passed - no responsibility boundary statement is locatable in a provided Logic Artifact; the only quoted materials are a Python dispatch helper, directory listings and README prose, and no instruction/responsibility baseline is provided.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (only a capability table is shown).

Gate-0 result: **Not passed - G0-3, G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-3 and G0-4 (structural admission); additionally the full artifact set is incomplete (no System Prompt body, no Skill, no Tool Schema).
Blocking Reasons:
  G0-3 - No responsibility baseline is locatable in a Logic Artifact (no System Prompt body is provided).
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-106 bundle (prompt-helper snippet + README capability table + directory listings).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The README capability table lists standard tools (web search, web fetch, code execution, database querying) as feature names; these are product capability declarations, not risk expressions matching a defined EX subcategory. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QC-0.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

No Stage A QD-P FAIL exists to map (no System Prompt body was provided). Candidate RAG-Agent quality metrics: none applicable (no Prompt-level defect). Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (N/A, no System Prompt body provided), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (Python dispatch snippet).
Stage B (Cross):            Not Executed - no Prompt/Skill/Tool pair exists (no System Prompt body, Skill or Tool Schema provided).
Stage C (Gate-0):           Not passed - G0-3, G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-3 and G0-4 not satisfied; full artifact set incomplete.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - no mappable Stage A QD-P FAIL (QC-0.2 is out of Appendix A mapping scope).
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
