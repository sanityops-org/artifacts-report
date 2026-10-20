# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-050-librechat-tool-schemas.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- The artifact contains several structures; they are classified as follows:
  - Tool Schema A: the Tavily search tool - identity (`name`, `description`) plus the `tavilySearchJsonSchema` JSON Schema rendered as a JavaScript object literal.
  - Tool Schema B: the OpenWeather tool - identity (`name`, `description`) plus the `openWeatherJsonSchema` JSON Schema rendered as a JavaScript object literal.
  - Registry / export surface (NOT a Tool Schema): `manifest.json` (a plugin registry of `name` / `pluginKey` / `description` / `icon` / `authConfig` entries) and `index.js` (a CommonJS re-export module). These carry no `inputSchema`/`parameters`, so they are registry metadata rather than Tool Schemas and receive no QD-T verdicts.
- Two tool schemas are inspected, each with its own tier determination and verdict set.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): Tool A (Tavily, L1) - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 2; Tool B (OpenWeather, L1) - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 2. Combined: P0 = 0, P1 = 2, P2 = 4. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in lone Tool Schemas) is unsatisfiable.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (up to five):
  1. QD-T-1.4 (Tavily) - the root schema object declares no `additionalProperties` control.
  2. QD-T-1.4 (OpenWeather) - the root schema object declares no `additionalProperties` control.
  3. QD-T-2.1 (OpenWeather) - string parameters (`city`, `exclude`, `lang`, `date`, `tz`) have no length bound.
  4. QD-T-2.3 (OpenWeather) - `lat` / `lon` numbers have no `minimum`/`maximum`.
  5. QD-T-2.3 (Tavily) - `days` declares `minimum` but no `maximum`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determinations

- Tool A `tavily_search_results_json` -> **L1 (Low Risk)**. Basis: read-only search query; no state change, no deletion/payment, no sensitive-data handling inside the schema.
- Tool B `open_weather` -> **L1 (Low Risk)**. Basis: read-only weather data retrieval; no state change and no sensitive-data handling inside the schema.

Both tools are tiered L1, so the L1 minimal set (7 items) is run for each.

### Tool A - `tavily_search_results_json` (L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 3 - `this.name`, `this.description`, and `this.schema` are all present. |
| QD-T-1.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 3 - `required: ['query']` and `query` is defined in `properties`. No inconsistency. |
| QD-T-1.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 3 - `search_depth` enum `['basic','advanced']`, `topic` enum `['general','news','finance']`, `time_range` enum `['day','week','month','year','d','w','m','y']` - no empty/duplicate/type-inconsistent values. |
| QD-T-1.4 | FAIL (P1) | evidence: `TC-050-librechat-tool-schemas.md`, section 3, root object. Offending text: `type: 'object', properties: { ... }, required: ['query']` - no `additionalProperties` key, so arbitrary extra fields are accepted by default. |
| QD-T-2.1 | FAIL (P2) | evidence: `TC-050-librechat-tool-schemas.md`, section 3, `properties.query`. Offending text: `query: { type: 'string', minLength: 1, description: 'The search query string.' }` - a lower bound only; no `maxLength` upper bound. |
| QD-T-2.3 | FAIL (P2) | evidence: `TC-050-librechat-tool-schemas.md`, section 3, `properties.days`. Offending text: `days: { type: 'number', minimum: 1, description: 'Number of days back from the current date to include. Only if topic is news.' }` - no `maximum` (`max_results` is bounded and passes). |
| QD-T-4.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 3 - descriptions are detailed and clear (including default/behavior notes). |

Tool A totals: P0 = 0; P1 = 1 (QD-T-1.4); P2 = 2 (QD-T-2.1, QD-T-2.3).

### Tool B - `open_weather` (L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 4 - `name`, `description`, and `schema` are all present. |
| QD-T-1.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 4 - `required: ['action']` and `action` is defined in `properties`. No inconsistency. |
| QD-T-1.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 4 - `action` enum and `units` enum `['Celsius','Kelvin','Fahrenheit']` - no empty/duplicate/type-inconsistent values. |
| QD-T-1.4 | FAIL (P1) | evidence: `TC-050-librechat-tool-schemas.md`, section 4, root object. Offending text: `type: 'object', properties: { ... }, required: ['action']` - no `additionalProperties` key. |
| QD-T-2.1 | FAIL (P2) | evidence: `TC-050-librechat-tool-schemas.md`, section 4, `properties.city` (also `exclude`, `lang`, `date`, `tz`). Offending text: `city: { type: 'string', description: 'City name for geocoding if lat/lon not provided' }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | FAIL (P2) | evidence: `TC-050-librechat-tool-schemas.md`, section 4, `properties.lat` and `properties.lon`. Offending text: `lat: { type: 'number', description: 'Latitude coordinate' }` - no `minimum`/`maximum`. |
| QD-T-4.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 4 - descriptions are clear and include action/units/default guidance. |

Tool B totals: P0 = 0; P1 = 1 (QD-T-1.4); P2 = 2 (QD-T-2.1, QD-T-2.3).

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes JavaScript source/schema snippets (the `index.js` module, the Tavily and OpenWeather schema object literals, and the tool-identity fragments). QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, sections 2-4 - all quoted JavaScript parses (complete `require`/`module.exports` module and complete object literals). |
| QC-0.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, sections 2-4 - code fences are labeled `javascript`. |
| QC-0.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, sections 2-4 - the `index.js` module is complete; the schema literals are complete; the `this.name`/`this.description`/`this.schema` identity fragment is a quoted class-body excerpt (no truncation marker). |
| QC-1.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - all referenced modules/identifiers are resolved through `require` or are object-literal keys. |
| QC-1.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 2 - every `require('./...)` path is a local module of the same project. |
| QC-1.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no file handle is opened. |
| QC-2.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-050-librechat-tool-schemas.md`, section 2 - every required module is used (spread into `module.exports` or exported). |
| QC-3.2 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-050-librechat-tool-schemas.md` - no hardcoded credential/demo value appears in the quoted code (the registry lists only environment-variable field names). |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): satisfied - Stage A produced no P0 findings. Recorded as informational.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected objects are lone Tool Schemas; no responsibility-boundary / duty baseline statement exists within them. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `tavily_search_results_json` and `open_weather` each have a `name`, a tool `description`, and a `description` on every parameter.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only Tool Schemas are present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schemas (`name` / `description` / inputSchema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission fields, no dangerous boolean/enum flags, no anomalous type constraints (`type: any`, `pattern: .*`) are declared.
- NR-S-5/6/8: no instruction poisoning in tool descriptions, no injected default/example values, no name-conflict/homoglyph issues.
- NR-S-7: `SD_WEBUI_URL` is a URL-typed auth field, but no actual address value is declared, so no callback-address anomaly can be established.
- NR-S-9/10: the registry lists environment-variable field names (e.g. `TAVILY_API_KEY`) only - no literal secret or PII values are present.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

For each Stage A FAIL, the candidate directions below are taken from relevance-map.md. The wording is candidate-only ("may", "candidate association", "needs dynamic verification"). Mapping strength is NOT severity and is labeled "provisional (lite)". Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (Tool A and Tool B)
- Static Discovery: Artifacts tool:`tavily_search_results_json`, tool:`open_weather`; Evidence: root schema objects declare no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Medium (provisional (lite)) - may have impact under specific parameter conditions.
- Note: indicates priority for validation; it does not indicate the backend is exploitable.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-2.1 / QD-T-2.3 | Parameter Constraint Missing | Inspect-P2 (Tool A and Tool B)
- Static Discovery: Artifacts tool:`tavily_search_results_json` (`query` length, `days` bound), tool:`open_weather` (`city`/`exclude`/`lang`/`date`/`tz` length, `lat`/`lon` bound); Evidence: constraints absent on the named parameters.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution).
- Potential Impact: D2 / D3 / Availability.
- Mapping Strength: Conditional (provisional (lite)) - impact depends on how the downstream service consumes unconstrained values.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist for Tool A (P0 0, P1 1, P2 2) and Tool B (P0 0, P1 1, P2 2); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate mapping for each Stage A FAIL.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
