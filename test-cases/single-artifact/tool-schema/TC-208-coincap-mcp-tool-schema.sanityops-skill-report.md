# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-208-coincap-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definitions; structural signature `name` + `description` + hand-written JSON-Schema `inputSchema`). The inspected object is the CoinCap tool set: `get_crypto_price` (the case's representative focus) and the companion `list_assets`, plus the shared `BaseTool` contract, quoted from `src/tools/GetCryptoPrice.ts`, `src/tools/ListAssets.ts`, and `src/tools/BaseTool.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): `get_crypto_price` / `list_assets` - **L1** - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 1. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-1.4 (P1) - the object `inputSchema` declares no `additionalProperties` control (both tools).
  2. QD-T-2.1 (P2) - the `name` string parameter carries no `minLength`/`maxLength`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool set (`get_crypto_price` representative + `list_assets`) -> **L1 (Low Risk)**.

Basis: read-only price queries. `get_crypto_price` fetches realtime crypto price data and returns it; `list_assets` fetches the list of available crypto assets. Neither declares a write, deletion/payment, permission change, or sensitive-data handling; both only read an upstream price API. Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool set is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md`, `src/tools/GetCryptoPrice.ts` / `src/tools/ListAssets.ts` - each tool provides a `name` (`get_crypto_price`, `list_assets`), a `description`, and an `inputSchema`. |
| QD-T-1.2 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md`, `src/tools/GetCryptoPrice.ts` - the schema declares `properties.name` and no `required` list; an absent `required` list is self-consistent and references no undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no `enum` is declared, so no invalid enum exists to flag. |
| QD-T-1.4 | FAIL | evidence: `TC-208-coincap-mcp-tool-schema.md`, `src/tools/GetCryptoPrice.ts` / `src/tools/ListAssets.ts`. Offending text: `"inputSchema": { "type": "object", "properties": { "name": { ... } } }` - no `"additionalProperties": false` (likewise `list_assets`: `"inputSchema": { "type": "object" }`), so arbitrary extra fields are accepted by default. |
| QD-T-2.1 | FAIL | evidence: `TC-208-coincap-mcp-tool-schema.md`, `src/tools/GetCryptoPrice.ts`. Offending text: `"name": { "type": "string", "description": "Name of the crypto coin" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no `number`-type parameter is declared, so no unbounded number exists to flag. |
| QD-T-4.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md`, `src/tools/GetCryptoPrice.ts` / `src/tools/ListAssets.ts` - the descriptions ("Get realtime crypto price on crypto", "Get all available crypto assets") name the capability and the `name` parameter carries a human-readable `description`; the tool description is terse and its phrasing is awkward, but it is specific enough to identify the operation. |

Tool-set totals: P0 = 0; P1 = 1; P2 = 1.

Note on rule subjects absent at this tier: no `enum` (QD-T-1.3), no `number` parameter (QD-T-2.3), no string requiring a specific format (QD-T-2.2, not in the L1 set), and no array parameter (QD-T-2.4, not in the L1 set). The `BaseTool`/`BaseToolImplementation` contract is a shared interface, not a tool schema, and is not itself tiered.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the tool definitions, handlers, and the shared base class). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - the quoted TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - the quoted blocks are complete enough for standalone parsing (imports present, class bodies and exports close). |
| QC-0.4 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - referenced names (`Tool`, `z`, `CONSTANTS`, `BaseToolImplementation`, `CallToolRequestSchema`) are imported or referenced consistently. |
| QC-1.2 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - imports (`@modelcontextprotocol/sdk`, `zod`, `../constants.js`, `./BaseTool.js`) reference declared/local dependencies; no obviously nonexistent module is imported. |
| QC-1.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - an outbound `fetch(url)` is used without an explicit connection handle; no unclosed connection object is created in the snippets (an API-level fetch call, not a retained socket). |
| QC-2.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - the network call is wrapped in `try { ... } catch (error) { ... }`, so no high-risk operation is left without exception handling in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-208-coincap-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code (the upstream endpoint comes from `CONSTANTS.CRYPTO_PRICE_URL`). |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - both tools carry a `name`, a tool `description`, and the `name` parameter carries a human-readable `description`.

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

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example value, and no conflicting/approximate tool name is declared (`get_crypto_price` vs `list_assets` are distinct).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema (the upstream endpoint is a shared constant, not a user-supplied callback address).
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced two FAIL verdicts; candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (L1)

- Static Discovery: artifacts tool `get_crypto_price` and tool `list_assets`; evidence - the object `inputSchema` declares no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by the schema; impact depends on how the arguments are forwarded to the CoinCap API.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-2.1 | String Without Length Constraint | Inspect-P2 (L1)

- Static Discovery: artifact tool `get_crypto_price`; evidence - `name` is a plain `string` with no `maxLength`/`minLength`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded `name` may yield an oversized request/result; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 1, P2 1); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
