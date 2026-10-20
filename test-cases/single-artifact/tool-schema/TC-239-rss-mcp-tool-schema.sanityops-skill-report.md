# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-239-rss-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition registered through `server.registerTool(name, { description, inputSchema }, handler)`; structural signature `name` + `description` + a Zod parameter object). The inspected object is the single `get_feed` tool quoted from `src/index.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): `get_feed` - **L1** - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 2. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings:
  1. QD-T-1.4 (P1) - the Zod `inputSchema` object declares no `additionalProperties` control and is not `.strict()`.
  2. QD-T-2.1 (P2) - the string parameter `url` carries no `minLength`/`maxLength`.
  3. QD-T-2.3 (P2) - the number parameter `count` carries no `minimum`/`maximum`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `get_feed` -> **L1 (Low Risk)**.
Basis: the tool performs a read-only fetch and parse of an RSS/Atom feed and returns the parsed items. There is no write, deletion/payment, permission change, or sensitive-data handling declared. Per the tier rules ("any write operation -> L2 minimum; irreversible operations -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts` - the tool provides a `name` (`"get_feed"`), a `description`, and an `inputSchema`. |
| QD-T-1.2 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts` - the Zod object declares `url` (required, no `.optional()`) and `count` (optional); no required entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts` - no `enum` is declared in the schema, so no invalid enum exists to flag. |
| QD-T-1.4 | FAIL | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts`. The parameter object is a plain Zod object with no `.strict()` and no `additionalProperties` control. Offending text: `inputSchema: { url: z.string().describe("URL of the RSS feed. ..."), count: z.number().optional().describe("Number of RSS feed items to retrieve. ...") }` (Zod object without `.strict()`). |
| QD-T-2.1 | FAIL | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts`. Offending text: `url: z.string().describe("URL of the RSS feed. ...")` - no `minLength`/`maxLength`. |
| QD-T-2.3 | FAIL | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts`. Offending text: `count: z.number().optional().describe("Number of RSS feed items to retrieve. Defaults to 1. Set to 0 to retrieve all items.")` - no `minimum`/`maximum` (or exclusive variants). |
| QD-T-4.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md`, `src/index.ts` - the tool description states the capability and the `url`/`count` descriptions document their meaning, default, and sentinel value. |

Tool totals: P0 = 0; P1 = 1; P2 = 2.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here. The `get_feed` implementation body and the RSSHub failover list are described in the prose but not quoted; per the single-artifact boundary they are not graded here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the `server.registerTool(...)` registration and the exported `get_feed` signature). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - the first fence parses as valid TypeScript; the second fence is a verbatim signature excerpt (treated as illustrative per the illustrative-snippet rule). |
| QC-0.2 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - the first block is complete (the `registerTool` call and the handler close); the second block is a verbatim signature excerpt. |
| QC-0.4 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - referenced names (`server`, `get_feed`, `RssFeed`, `Error`, `error`, `feedResult`) are defined in the snippet or referenced consistently. |
| QC-1.2 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no import of an unavailable module is present in the quoted snippets. |
| QC-1.3 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no raw network connection is opened in the quoted snippets (the fetch happens inside the elided `get_feed` implementation). |
| QC-2.3 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - the handler wraps its work in `try { ... } catch (error) { ... }`, so a high-risk operation is not left without exception handling. |
| QC-3.1 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no referenced module is missing an import within the quoted snippets. |
| QC-3.3 | PASS | evidence: `TC-239-rss-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): satisfied - Stage A produced no P0 findings. Recorded as informational.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `get_feed` carries a `name`, a tool `description`, and per-parameter `.describe(...)` text.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - Gate-0 not satisfied, and the full artifact set is unavailable.

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-3
Blocking Reasons:
  G0-3 - no responsibility-boundary / duty baseline statement exists in a lone Tool Schema; proportionality has no reference.
  Artifact set - the full set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.
Remediation Actions: Fix the above upstream item, then re-run Gate-0.

Scope statement (permission-checklist.md section 5): this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / `inputSchema`) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Phase 1 - Discovery and classification: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present (the `url` parameter is an ordinary `z.string()`; no `type: "any"` or `pattern: ".*"` is declared).
- NR-S-5/6: no instruction poisoning in the description and no injected instruction/dangerous value in a default/example field.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema (the `url` is a caller-supplied fetch target, not a declared fixed callback address or abnormal pointing).
- NR-S-8: the tool surface is a single distinctly named tool (`get_feed`); no conflicting or approximate-duplicate name is declared.
- NR-S-9/10: no hardcoded literal secret and no PII value is declared.

Risk-Explicit totals: Explicit·P0 = 0; Explicit·P1 = 0; Explicit·P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced three FAIL verdicts (QD-T-1.4, QD-T-2.1, QD-T-2.3); candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (L1)

- Static Discovery: artifact tool `get_feed`; evidence - the Zod parameter object is not `.strict()` and declares no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by the schema; impact depends on how arguments are forwarded to the fetch layer.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-2.1 | String Without Length Constraint | Inspect-P2 (L1)

- Static Discovery: artifact tool `get_feed`; evidence - the `url` string carries no `minLength`/`maxLength`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded string may yield an oversized input; impact depends on the fetch layer's own validation.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

### Impact Card: QD-T-2.3 | Number Without Boundary | Inspect-P2 (L1)

- Static Discovery: artifact tool `get_feed`; evidence - the `count` number carries no `minimum`/`maximum`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded count may request an unexpectedly large result set; impact depends on feed and fetch-layer limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 1, P2 2); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit·P0 0, Explicit·P1 0, Explicit·P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4, QD-T-2.1, and QD-T-2.3.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
