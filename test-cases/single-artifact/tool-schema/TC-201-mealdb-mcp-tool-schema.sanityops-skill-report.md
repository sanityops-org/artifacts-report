# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-201-mealdb-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `description` + `inputSchema`). The inspected artifact is the `search_meals` tool: a hand-written raw JSON Schema `inputSchema` plus the `ListToolsRequestSchema` registration, quoted from `src/index.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): Tool `search_meals` (L1) - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 1. Embedded-code QC: P0 = 1, P1 = 1, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  - QD-T-1.4 - the object inputSchema does not declare `additionalProperties`, so arbitrary extra fields are accepted by default.
  - QD-T-2.1 - the `query` string declares no `maxLength` / `minLength`.
  - QC-0.1 (QC-P0) - the quoted sibling-tool excerpt contains literal `...` tokens and is not valid TypeScript.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `search_meals` -> **L1 (Low Risk)**.
Basis: read-only recipe search - the tool queries TheMealDB API and returns matching meals; it performs no write, deletion, payment, or permission change, and no API key/credential (free tier) or sensitive-data handling is declared. Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` - `name` = `search_meals`, a `description`, and an `inputSchema` are all present. |
| QD-T-1.2 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` `inputSchema` - `required` is `["query"]` and `query` is defined in `properties`; no `required` entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` `inputSchema` - no `enum` keyword appears, so no invalid enum exists to flag. |
| QD-T-1.4 | FAIL | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` `inputSchema`. The object schema declares `properties` but no `"additionalProperties": false`. Offending excerpt: `"inputSchema": { "type": "object", "properties": { "query": { ... } }, "required": ["query"] }` (no `additionalProperties` declaration), so arbitrary extra fields are accepted by default. |
| QD-T-2.1 | FAIL | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` `inputSchema` (`query`). Offending excerpt: `"query": { "type": "string", "description": "Name of the meal to search for" }` - no `maxLength` / `minLength` is set. |
| QD-T-2.3 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` `inputSchema` - the schema declares no `number`-type parameter, so no unbounded number exists to flag. |
| QD-T-4.1 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` - the tool description states the capability and the parameter carries a human-readable `description`. |

Tool totals: P0 = 0; P1 = 1 (QD-T-1.4); P2 = 1 (QD-T-2.1).

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the `ListToolsRequestSchema` registration, the server bootstrap, and the sibling-tool headers). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | FAIL | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` (sibling-tool headers block). Offending excerpt: `{ name: "get_meal_details", description: "Get detailed information about a specific meal by ID", ... }` - the literal `...` ellipsis is not a valid TypeScript token in that object position, so the snippet does not parse as declared-language syntax. |
| QC-0.2 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | FAIL | evidence: `TC-201-mealdb-mcp-tool-schema.md`, `src/index.ts` (registration and bootstrap). Offending excerpt: `server.setRequestHandler(ListToolsRequestSchema, async () => { return { tools: [ { name: "search_meals", ... },` and `const server = new Server(\n  {\n    name: "mealdb-server",\n    version: "1.0.0",` - both snippets are left unclosed; they are not complete enough for standalone parsing. |
| QC-1.1 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - `server`, `ListToolsRequestSchema`, and `Server` are defined in the snippet or SDK-provided. |
| QC-1.2 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no import of an unavailable module is present in the quoted snippets. |
| QC-1.3 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no imported module is left unused in the quoted snippets. |
| QC-3.2 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no referenced module is missing an import within the quoted snippets. |
| QC-3.3 | PASS | evidence: `TC-201-mealdb-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

QC totals: P0 = 1 (QC-0.1); P1 = 1 (QC-0.3); P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): satisfied - Stage A produced no P0 findings (the QC-0.1 P0 is an embedded-code finding; no QD-T P0). Recorded as informational.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `search_meals` has a `name`, a tool `description`, and a `description` on its parameter.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / `inputSchema`) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example value, and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema. (The `MEALDB_BASE_URL` constant is a plain module constant for the public TheMealDB endpoint, not a schema field or a caller-controlled callback address; it is not an NR-S-7 issue.)
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Candidate associations below are advisory context, physically separated from the stage verdicts, and use candidate wording only.

### Impact Card: QD-T-1.4 | additionalProperties not controlled | Inspect-P1 (Tool Schema)

- Static Discovery: artifact tool `search_meals`; version label `2026-10-13`; evidence - `inputSchema` object declares `properties` with no `additionalProperties`.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion). Potential Impact D1 / D2 / D3. Mapping Strength: Medium - provisional (lite); per relevance-map.md section 1.3, a control-gap in the object schema may have impact under specific conditions (additional/reserved fields), pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

### Impact Card: QD-T-2.1 | string without length constraint | Inspect-P2 (Tool Schema)

- Static Discovery: artifact tool `search_meals`; version label `2026-10-13`; evidence - `query` is a `string` type with no length bound.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution). Potential Impact D2 / D3 / Availability. Mapping Strength: Conditional - provisional (lite); per relevance-map.md section 1.3, impact may depend on downstream handling and runtime behavior, pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

### QC FAILs

QC-0.1 and QC-0.3 (invalid/truncated excerpt) have no QD-level mapping row in relevance-map.md (the map covers QD-* defects only); no candidate AS-*/FM-* association is emitted for them.

Not run: Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifacts are absent. v1 scope: single-defect mapping only; defect chains are out of scope.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 1, P2 1); embedded-code QC (P0 1, P1 1, P2 0).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - 2 QD-T FAILs mapped; QC FAILs have no mapping row.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
