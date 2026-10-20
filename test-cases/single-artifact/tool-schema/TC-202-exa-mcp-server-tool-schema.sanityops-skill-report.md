# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-202-exa-mcp-server-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `description` + parameter schema). The inspected artifact is the `web_search_exa` tool: the `server.tool(name, description, params, annotations, handler)` registration whose parameter schema is authored with the `lenientString` / `lenientOptionalNumber` helpers, quoted from `src/tools/webSearch.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): Tool `web_search_exa` (L1) - Inspect-P0 = 0, Inspect-P1 = 0, Inspect-P2 = 2. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  - QD-T-2.1 - the `query` string declares no length bound in the quoted schema.
  - QD-T-2.3 - the `numResults` number declares no `minimum` / `maximum` in the quoted schema.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `web_search_exa` -> **L1 (Low Risk)**.
Basis: read-only web search - the tool queries the Exa search API and returns sanitized content; the registration declares `readOnlyHint: true` and `destructiveHint: false`. There is no write, deletion/payment, permission change, or sensitive-data handling declared in the schema (the API key is passed through `config`). Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` - the tool is registered with a `name` (`web_search_exa` or the override), a `description`, and a parameters object. |
| QD-T-1.2 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` - `query` is declared mandatory (essential to the call) and `numResults` is declared optional with a documented default ("default: 10"); no required entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` - no `enum` is declared in the parameter schema (the `category:` filter is parsed in the handler), so no invalid enum exists to flag. |
| QD-T-1.4 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` - the parameters are authored with typed schema helpers (`lenientString`, `lenientOptionalNumber`); no arbitrary extra-field acceptance is declared, so no uncontrolled-additionalProperties defect is established from the artifact. |
| QD-T-2.1 | FAIL | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` (`query`). Offending excerpt: `query: lenientString().describe("Natural language search query. ...")` - no `maxLength` / `minLength` is declared in the quoted schema. (Any length bound would live inside the `lenientString` helper in `validation.ts`, which the artifact references but does not quote; per the single-artifact boundary this is judged on the quoted schema.) |
| QD-T-2.3 | FAIL | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` (`numResults`). Offending excerpt: `numResults: lenientOptionalNumber().describe("Number of search results to return (default: 10).")` - no `minimum` / `maximum` is declared in the quoted schema. |
| QD-T-4.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md`, `src/tools/webSearch.ts` - the tool description states the capability, when to use it, the return shape, and non-obvious query guidance; both parameters carry descriptive `.describe(...)` text. |

Tool totals: P0 = 0; P1 = 0; P2 = 2 (QD-T-2.1, QD-T-2.3).

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the full `registerWebSearchTool` factory). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the quoted TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the code fence is labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the module has its imports and the function closes; the snippet is complete enough for standalone parsing. |
| QC-1.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - referenced names (`server`, `config`, `createExaClient`, `retryWithBackoff`, `formatToolError`, `withTimeout`, `sanitizeSearchResponse`, `lenientString`, `lenientOptionalNumber`, `checkpoint`) are imported in the snippet. |
| QC-1.2 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the imports correspond to declared project modules (`config.js`, `../utils/...`, `./validation.js`) plus the SDK and `agnost`. |
| QC-1.3 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - no file handle is opened in the quoted snippet. |
| QC-2.2 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the request is issued through the `exa` client wrapper with retry/timeout helpers; no bare unmanaged connection is opened. |
| QC-2.3 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - the network call is wrapped in `try ... catch`, which returns `formatToolError(...)`. |
| QC-3.1 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - all listed imports are referenced in the body. |
| QC-3.2 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-202-exa-mcp-server-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `web_search_exa` has a `name`, a tool `description`, and a `.describe(...)` on every parameter.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / parameter schema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning in the description (the query tips are legitimate usage guidance), no injected default/example value, and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared (the API key is passed through `config`).

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Candidate associations below are advisory context, physically separated from the stage verdicts, and use candidate wording only.

### Impact Card: QD-T-2.1 | string without length constraint | Inspect-P2 (Tool Schema)

- Static Discovery: artifact tool `web_search_exa`; version label `2026-10-14`; evidence - the `query` string declares no length bound in the quoted schema.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution). Potential Impact D2 / D3 / Availability. Mapping Strength: Conditional - provisional (lite); per relevance-map.md section 1.3, impact may depend on downstream handling and runtime behavior, pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

### Impact Card: QD-T-2.3 | number without boundary | Inspect-P2 (Tool Schema)

- Static Discovery: artifact tool `web_search_exa`; version label `2026-10-14`; evidence - `numResults` is a number with no schema-level `minimum` / `maximum`.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution). Potential Impact D2 / D3 / Availability. Mapping Strength: Conditional - provisional (lite); the handler applies `numResults || API_CONFIG.DEFAULT_NUM_RESULTS`, so a bound may be enforced elsewhere; pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

Not run: Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifacts are absent. v1 scope: single-defect mapping only; defect chains are out of scope.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 0, P2 2); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - 2 QD-T FAILs mapped.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
