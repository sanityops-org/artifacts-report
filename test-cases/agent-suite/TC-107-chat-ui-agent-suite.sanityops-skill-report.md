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
- Finding counts (Stage A): QD-P = Not Applicable (no System Prompt body is provided); embedded-code QC: P0 = 0, P1 = 1, P2 = 0.
- Gate-0 result: Not passed (G0-3 not satisfied - no responsibility boundary statement is locatable in a provided Logic Artifact; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 1.
- Top findings (rule ID - one-line defect):
  1. QD-P - Not Applicable: no System Prompt body is quoted (the "preprompt" is environment-provided and not retrieved), so no QD-P verdict is emitted.
  2. QC-0.2 - The embedded TypeScript snippet (`buildPrompt.ts`) carries no explicit language identifier on its fence.
  3. EX NR-S-2 - The environment config explicitly enables forwarding the signed-in user's Hugging Face token (`MCP_FORWARD_HF_USER_TOKEN=true`) (Risk-Explicit assessment, physically separated below).
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-107 bundles one single-agent suite (Chat UI / HuggingChat application). Artifact types present, by structural signature:

- System Prompt (identified, not quoted): the chat "preprompt" is environment/configurable and is injected by `buildPrompt.ts`, but no natural-language system-prompt body is quoted. Basis: the retrieved artifacts are a TypeScript assembly helper, an environment config block and README prose; the case states "The verbatim prompt artifact used here is `src/lib/buildPrompt.ts`". No instruction string is provided, so it is not inspected and no QD-P verdict is emitted.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability (the artifacts are TypeScript source, an env block and README prose).
- Tool Schema (absent): tools are sourced from MCP servers via an env list (`MCP_SERVERS=[{"name": ..., "url": ...}]`) and surfaced via OpenAI function calling, but no JSON `parameters`/`inputSchema` schema is quoted.
- Embedded code snippets (QC scope): the `src/lib/buildPrompt.ts` TypeScript excerpt and the `MCP_SERVERS` environment block.
- Out of coverage: `src/lib/server/*` (MCP integration, Omni router, request processing), the ML Intern mode and `PROMPTS.md` are described but not quoted (the case notes `PROMPTS.md` was not retrievable).

Scope note: the prompt assembly, the MCP tool servers, the server router and ML Intern are parts of one chat application, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt

- QD-P-1.x .. QD-P-2.x | N/A | evidence: TC-107 provides no System Prompt body (determination basis: the "preprompt" is environment/config-provided and is not quoted; only `buildPrompt.ts`, an env block and README prose are retrieved). No QD-P verdict is emitted.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-107 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-107 carries no Tool Schema artifact (determination basis: the `MCP_SERVERS` env list holds server name/url entries, not a JSON `parameters`/`inputSchema` schema for a tool). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the case embeds a TypeScript excerpt (`buildPrompt.ts`) and an environment config block (`MCP_SERVERS`).

- QC-0.1 | PASS | evidence: TC-107, buildPrompt.ts, the `buildPrompt` function parses as valid TypeScript.
- QC-0.2 | FAIL | evidence: TC-107, the `buildPrompt.ts` block carries no explicit language identifier on the fence (the `env` block does declare `env`).
- QC-0.3 | PASS | evidence: TC-107, buildPrompt.ts, the imports and the full function body are present and not truncated.
- QC-0.4 | PASS | evidence: TC-107, the fenced blocks open and close correctly.
- QC-0.5 | N/A | evidence: TC-107, the code fence declares no language to compare against content (determination basis: no language identifier on the code block).
- QC-1.1 | PASS | evidence: TC-107, buildPrompt.ts, the used names (`EndpointParameters`, `BackendModel`, `toLegacyShape`, `chatPromptRender`) are each imported at the top of the snippet.
- QC-1.2 | Not Executed | evidence: TC-107, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-107, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-107, no function call with clearly incompatible argument types (determination basis: typed assembly code).
- QC-2.1 | N/A | evidence: TC-107, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-107, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-107, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-107, each import is referenced (determination basis: imports are used).
- QC-3.2 | PASS | evidence: TC-107, buildPrompt.ts, the referenced symbols are imported in the snippet.
- QC-3.3 | PASS | evidence: TC-107, no credential, local path or machine-specific value in the snippet (the env block forwards a token by reference, not a literal).
- QC-4.1 | N/A | evidence: TC-107, no snippet-parameter/declaration pair to compare (determination basis: no tool schema present).
- QC-4.2 | N/A | evidence: TC-107, no version/API drift to compare (determination basis: single assembly helper).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: no Prompt/Skill/Tool pair exists (no System Prompt body, no Skill, no Tool Schema are provided), so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the router selects a single route/model per message (`default` / `multimodal` / `agentic`) and no cyclic role orchestration is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): NOT passed - no responsibility boundary statement is locatable in a provided Logic Artifact; the quoted materials are a TypeScript assembly helper, an env block and README prose, and the "preprompt" that would carry the responsibility baseline is not provided.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (MCP tools are listed as server entries only).

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

Audit object: TC-107 bundle (`buildPrompt.ts` snippet + `MCP_SERVERS` env block + README router/ML-Intern prose).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 1
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 1 item

Risk Item Details:
- EX Classification: NR-S-2 (Dangerous Capability Flag Explicitly Enabled)
- Risk Expression: `MCP_FORWARD_HF_USER_TOKEN=true` ("Forward the signed-in user's Hugging Face token to the official HF MCP login endpoint when no Authorization header is set on that server entry.")
- Severity Grade: Explicit.P2
- Reason: The flag explicitly enables forwarding the signed-in user's own token to the official Hugging Face MCP login endpoint; the forwarded value is a credential the user already holds and the destination is the service's own endpoint, so the capability sits within the user's existing permission scope (not data exfiltration to an unrelated party, not an irreversible action, and not a security-restriction bypass).
- Impact Type Labels: D1, D3
- Trigger Condition Label: unconditional (the triggering condition - "no Authorization header is set on that server entry" - is satisfiable by the user's ordinary behaviour)
- Disposition: Record in risk ledger
- Remediation Suggestion: Restrict scope - state the exact endpoint(s) and conditions under which the token is forwarded, and prefer per-request user consent.

Other observations: the `MCP_SERVERS` URLs (`https://mcp.exa.ai/mcp`, `https://hf.co/mcp?login`) point to their respective official services and no abnormal-callback pattern (NR-S-7) or literal credential (NR-S-9) was found. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QC-0.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

No Stage A QD-P FAIL exists to map (no System Prompt body was provided). The Stage E NR-S-2 item is a Risk-Explicit finding, not an Inspect defect, and is therefore not mapped here. Candidate RAG-Agent quality metrics: none applicable (no Prompt-level defect). Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (N/A, no System Prompt body provided), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (TypeScript assembly snippet + env block).
Stage B (Cross):            Not Executed - no Prompt/Skill/Tool pair exists (no System Prompt body, Skill or Tool Schema provided).
Stage C (Gate-0):           Not passed - G0-3, G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-3 and G0-4 not satisfied; full artifact set incomplete.
Stage E (Risk Explicit EX): Executed - 1 finding (Explicit.P2).
Stage F (Impact outlook):   Executed - no mappable Stage A QD-P FAIL (QC-0.2 is out of Appendix A mapping scope).
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
