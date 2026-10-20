# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-182-brave-search-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `description` + `inputSchema`). The inspected schema is the `brave_web_search` tool: the identity/description/registration snippet and the `params` Zod input schema (which the MCP TypeScript SDK converts to JSON Schema at registration time).
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): Tool `brave_web_search` (L1) - Inspect-P0 = 0, Inspect-P1 = 0, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema) is unsatisfiable.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings: none - the L1 minimal set produced no FAIL verdicts for this schema.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `brave_web_search` -> **L1 (Low Risk)**.
Basis: read-only web search - it queries an external search index and returns results; no data write, no deletion/payment, no permission change, and no sensitive-data handling inside the schema. Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, sections 1-2 - `name` = `brave_web_search`, a tool `description`, and an `inputSchema` (`params`) are all present. |
| QD-T-1.2 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - only `query` is required (no `.optional()`); every other field is `.optional()` and defined in the object. No `required` references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - `country`, `search_lang`, `ui_lang`, `safesearch`, `result_filter` enums contain no empty, duplicate, or type-inconsistent values. |
| QD-T-1.4 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - the schema is a Zod `z.object({...})`; Zod object semantics do not accept arbitrary extra fields as declared, so no uncontrolled-additionalProperties defect is established from the artifact. No arbitrary extra-field acceptance is declared. |
| QD-T-2.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2, `query`. `query: z.string().max(400)...` declares an upper length bound; the remaining string fields are enum-constrained. No length-unbounded plain string is present. |
| QD-T-2.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - `count: z.int().min(1).max(20)` and `offset: z.int().min(0).max(9)` are both bounded; no number parameter lacks a boundary. |
| QD-T-4.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, sections 1-2 - the tool description enumerates "When to use" scenarios and every parameter carries an inline human-readable `.describe(...)`. |

Tool totals: P0 = 0; P1 = 0; P2 = 0.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so the union-typed `goggles` field and the array-typed `result_filter` field are not separately graded here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes TypeScript code (the tool identity/registration snippet and the `params.ts` Zod module). QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, sections 1-2 - the TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, sections 1-2 - code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - the module has its `import { z } from 'zod'` and is not truncated. |
| QC-1.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - `z` and `params` are defined in the snippet. |
| QC-1.2 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - `zod` is the declared schema dependency. |
| QC-1.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md` - no file handle is opened. |
| QC-2.2 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - `z` is used throughout. |
| QC-3.2 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md`, section 2 - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-182-brave-search-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `brave_web_search` has a `name`, a tool `description`, and a `.describe(...)` on every parameter.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / inputSchema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission fields, no dangerous boolean/enum flags, no anomalous type constraints are declared.
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example values, no name-conflict/homoglyph issues.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced **no FAIL verdicts** for this schema, so there are **no candidate mappings to emit**.

Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 0, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - no Stage A FAILs to map.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
