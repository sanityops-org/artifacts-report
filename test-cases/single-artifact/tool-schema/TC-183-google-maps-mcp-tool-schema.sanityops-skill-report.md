# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-183-google-maps-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schemas** (MCP tool definitions; structural signature `name` + `description` + `inputSchema`). The artifact quotes one tightly-related tool group from a single file, comprising seven tools: `maps_geocode`, `maps_reverse_geocode`, `maps_search_places`, `maps_place_details`, `maps_distance_matrix`, `maps_elevation`, `maps_directions`.
- Each tool is given its own tier determination and per-tool verdict set.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): all seven tools are L1 - combined Inspect-P0 = 0, Inspect-P1 = 7, Inspect-P2 = 7. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in lone Tool Schemas) is unsatisfiable.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (up to five):
  1. QD-T-1.4 - none of the seven root schema objects declares `additionalProperties`.
  2. QD-T-2.1 - string parameters carried without a length bound (`address`, `query`, `place_id`, `origin`, `destination`).
  3. QD-T-2.3 - number parameters without bounds (`latitude`/`longitude`, `radius`) on the tools that carry them.
  4. QD-T-1.4 (nested) - nested object sub-schemas (`location`, `locations[]` items) also declare no `additionalProperties`.
  5. No P0 finding was produced at the L1 tier.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determinations

All seven tools -> **L1 (Low Risk)**. Basis: every tool is a read-only lookup (geocoding, place search/details, distance matrix, elevation, directions); none creates/updates recoverable state (no L2 trigger) and none is irreversible or handles sensitive data (no L3 trigger).

Consequently the L1 minimal set (7 items: QD-T-1.1, 1.2, 1.3, 1.4, 2.1, 2.3, 4.1) is run for each tool.

### Tool 1 - `maps_geocode` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-183-google-maps-mcp-tool-schema.md` - `name`, `description` ("Convert an address into geographic coordinates"), `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["address"]`; `address` is defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present (rule subject absent). |
| QD-T-1.4 | FAIL (P1) | evidence: `GEOCODE_TOOL.inputSchema`. Offending text: `{ type: "object", properties: { address: {...} }, required: ["address"] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.address`. Offending text: `"address": { "type": "string", "description": "The address to geocode" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: description "Convert an address into geographic coordinates" and the `address` description are clear. |

### Tool 2 - `maps_reverse_geocode` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["latitude", "longitude"]`; both defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `REVERSE_GEOCODE_TOOL.inputSchema`. Offending text: `{ type: "object", properties: { latitude: {...}, longitude: {...} }, required: [...] }` - no `additionalProperties`. |
| QD-T-2.1 | PASS | evidence: no string-type parameter is present. |
| QD-T-2.3 | FAIL (P2) | evidence: `properties.latitude` / `properties.longitude`. Offending text: `"latitude": { "type": "number", "description": "Latitude coordinate" }` - no `minimum`/`maximum`. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 3 - `maps_search_places` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["query"]`; `query` defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `SEARCH_PLACES_TOOL.inputSchema` (and its nested `location` object). Offending text: `{ type: "object", properties: {...} }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.query`. Offending text: `"query": { "type": "string", "description": "Search query" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | FAIL (P2) | evidence: `properties.radius` and nested `properties.location.properties.latitude`/`longitude`. Offending text: `"radius": { "type": "number", "description": "Search radius in meters (max 50000)" }` - the bound is in prose only; no `maximum` keyword. |
| QD-T-4.1 | PASS | evidence: descriptions are clear (including the "max 50000" note). |

### Tool 4 - `maps_place_details` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["place_id"]`; `place_id` defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `PLACE_DETAILS_TOOL.inputSchema`. Offending text: `{ type: "object", properties: { place_id: {...} }, required: ["place_id"] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.place_id`. Offending text: `"place_id": { "type": "string", "description": "The place ID to get details for" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 5 - `maps_distance_matrix` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["origins", "destinations"]`; both defined in `properties`. |
| QD-T-1.3 | PASS | evidence: `mode` enum `["driving","walking","bicycling","transit"]` - no empty/duplicate values. |
| QD-T-1.4 | FAIL (P1) | evidence: `DISTANCE_MATRIX_TOOL.inputSchema`. Offending text: `{ type: "object", properties: {...} }` - no `additionalProperties`. |
| QD-T-2.1 | PASS | evidence: no plain string parameter is present (`origins`/`destinations` are arrays, `mode` is enum-constrained). |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: descriptions are clear (including the `mode` list). |

### Tool 6 - `maps_elevation` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["locations"]`; and the item sub-object `required: ["latitude","longitude"]` both defined. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `ELEVATION_TOOL.inputSchema` and its `locations` items object. Offending text: `{ type: "object", properties: {...} }` - no `additionalProperties` at either level. |
| QD-T-2.1 | PASS | evidence: no string-type parameter is present. |
| QD-T-2.3 | FAIL (P2) | evidence: `locations.items.properties.latitude` / `longitude`. Offending text: `"latitude": { "type": "number" }` - no `minimum`/`maximum`. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 7 - `maps_directions` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["origin", "destination"]`; both defined in `properties`. |
| QD-T-1.3 | PASS | evidence: `mode` enum `["driving","walking","bicycling","transit"]` - no empty/duplicate values. |
| QD-T-1.4 | FAIL (P1) | evidence: `DIRECTIONS_TOOL.inputSchema`. Offending text: `{ type: "object", properties: {...} }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.origin` / `properties.destination`. Offending text: `"origin": { "type": "string", "description": "Starting point address or coordinates" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Stage A totals

- P0 = 0.
- P1 = 7 (QD-T-1.4 for each of the seven tools).
- P2 = 7 (QD-T-2.1 or QD-T-2.3 for the six tools that carry an unbounded string or number parameter; `maps_distance_matrix` contributes none).

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes TypeScript tool-definition code (one verbatim excerpt of a single source file). QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: the quoted TypeScript parses as valid syntax (complete `const ... = { ... }` declarations). |
| QC-0.2 | PASS | evidence: code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: the quoted declarations are syntactically complete and untruncated. Note: the excerpt starts at `// Tool definitions` and the enclosing module's imports (`Tool`, `Server`, `ListToolsRequestSchema`) are outside the quoted range; the code is an excerpt, not a standalone file. |
| QC-1.1 | PASS | evidence: in the authored module the referenced names (`Tool`, `Server`, `ListToolsRequestSchema`) are imported; within the excerpt they are type/import references, not undefined locals. |
| QC-1.2 | PASS | evidence: no non-standard import is introduced by the quoted code. |
| QC-1.3 | PASS | evidence: no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: no file handle is opened. |
| QC-2.2 | PASS | evidence: no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: no unused import appears in the quoted code. |
| QC-3.2 | PASS | evidence: no referenced module is missing an import in the authored module. |
| QC-3.3 | PASS | evidence: no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - every tool has a `name`, a tool `description`, and a description on each declared top-level parameter. Observation (not a G0-4 failure at the parameter level): the nested coordinate sub-properties (`location.latitude`/`longitude` in `maps_search_places`, `locations[]` items in `maps_elevation`) carry no inline description.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only Tool Schemas are present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schemas (`name` / `description` / inputSchema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission fields, no dangerous boolean/enum flags, no anomalous type constraints are declared (the `mode` enums are ordinary travel-mode choices).
- NR-S-5/6/8: no instruction poisoning in descriptions, no injected default/example values, no name-conflict/homoglyph issues (all names carry a distinct `maps_` prefix).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

For each Stage A FAIL, the candidate directions below are taken from relevance-map.md. The wording is candidate-only ("may", "candidate association", "needs dynamic verification"). Mapping strength is NOT severity and is labeled "provisional (lite)". Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (all seven tools)
- Static Discovery: Artifacts tool:`maps_geocode` ... tool:`maps_directions`; Evidence: root schema objects (and nested object sub-schemas) declare no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Conditional (provisional (lite)) - the tools are read-only, so impact may depend on downstream handling of extra fields.
- Note: indicates priority for validation; it does not indicate the backend is exploitable.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-2.1 / QD-T-2.3 | Parameter Constraint Missing | Inspect-P2 (tools carrying unbounded string/number parameters)
- Static Discovery: Artifacts tool:`maps_geocode`, tool:`maps_reverse_geocode`, tool:`maps_search_places`, tool:`maps_place_details`, tool:`maps_elevation`, tool:`maps_directions`; Evidence: the named string/number parameters carry no length or numeric bounds.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution).
- Potential Impact: D2 / D3 / Availability.
- Mapping Strength: Conditional (provisional (lite)) - impact depends on how the Google Maps backend consumes unconstrained values.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist for all seven tools (combined P0 0, P1 7, P2 7); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate mapping for each Stage A FAIL.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
