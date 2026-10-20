# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-197-todoist-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `description` + `inputSchema`). The inspected artifact is the `todoist_create_task` tool: a hand-written raw JSON Schema `inputSchema`, quoted from `src/index.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): Tool `todoist_create_task` (L2) - Inspect-P0 = 1, Inspect-P1 = 1, Inspect-P2 = 0. Embedded-code QC: P0 = 1, P1 = 1, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  - QD-T-1.4 (Inspect-P0) - the object inputSchema does not declare `additionalProperties`, so arbitrary extra fields are accepted by default.
  - QD-T-2.1 - the `content` / `description` / `due_string` strings declare no `maxLength` / `minLength`.
  - QD-T-3.2 - evaluated: no free-form command/query interpreter passthrough is declared (see verdict note).
  - QC-0.1 (QC-P0) - the quoted sibling-tool excerpt contains a literal `...` token and is not valid TypeScript.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `todoist_create_task` -> **L2 (Medium Risk)**.
Basis: the tool performs a **write operation** - it creates a new task in Todoist (`Create a new task in Todoist ...`). Per the tier rules, "any write operation -> L2 minimum". The side effect is a recoverable/overwritable state change (a created task can be deleted or updated) and no deletion, payment, permission change, or sensitive-data handling is declared, so the L3 triggers do not apply. The Tool is therefore tiered L2, and the L2 checklist (which contains all L1 items) is run.

### QD-T L2 full checklist (12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` - `name` = `todoist_create_task`, a `description`, and an `inputSchema` are all present. |
| QD-T-1.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `inputSchema` - `required` is `["content"]` and `content` is defined in `properties`; `description`/`due_string`/`priority` are defined and not required. No `required` entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `priority` - `enum: [1, 2, 3, 4]` has no empty, duplicate, or type-inconsistent value. |
| QD-T-1.4 | FAIL | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `inputSchema`. The object schema declares `properties` but no `"additionalProperties": false`. Offending excerpt: `"inputSchema": { "type": "object", "properties": { ... }, "required": ["content"] }` (no `additionalProperties` declaration), so arbitrary extra fields are accepted by default. Level at L2 = P0. |
| QD-T-2.1 | FAIL | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `inputSchema` (`content`, `description`, `due_string`). Offending excerpt: `"content": { "type": "string", "description": "The content/title of the task" }` - no `maxLength` / `minLength` is set. The same holds for `description` and `due_string`. Level at L2 = P1. |
| QD-T-2.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `due_string` - the field is explicitly declared as **natural language** (`"Natural language due date like 'tomorrow', 'next Monday', 'Jan 23'"`); no single machine format is declared as required, so no missing `pattern`/`format` defect is established. |
| QD-T-2.3 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `priority` - the `number` parameter is fully bounded by `enum: [1, 2, 3, 4]`; the allowed value set is enumerated, so the number is not left unbounded. |
| QD-T-2.4 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `inputSchema` - the schema declares no array-type parameter, so no missing `maxItems`/`minItems` exists to flag. |
| QD-T-3.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` - the tool description opens with `Create a new task in Todoist ...`, which explicitly identifies the write/create operation; the write is not concealed. |
| QD-T-3.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` `inputSchema`. The free-form fields (`content`, `description`, `due_string`) are stored as task data values passed to the Todoist API; no backend command/query interpreter (e.g. a SQL/expression string) is declared as an input. No raw command-passthrough defect is established from the artifact. |
| QD-T-4.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` - the tool description states the capability, each parameter carries a human-readable `description`, and optionality is stated inline ("(optional)"). |
| QD-T-4.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` - the only side effect declared is the task creation named in the description; no undeclared side effect (notification, integration, external send) is described. |

Tool totals: P0 = 1 (QD-T-1.4); P1 = 1 (QD-T-2.1); P2 = 0.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (`CREATE_TASK_TOOL`, the server bootstrap, and the sibling-tool headers). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | FAIL | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` (sibling-tool headers block). Offending excerpt: `const GET_TASKS_TOOL: Tool = { name: "todoist_get_tasks", ... };` - the literal `...` ellipsis is not a valid TypeScript token in that object position, so the snippet does not parse as declared-language syntax. (The server-bootstrap block is likewise left unclosed.) |
| QC-0.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | FAIL | evidence: `TC-197-todoist-mcp-tool-schema.md`, `src/index.ts` (server bootstrap and sibling headers). Offending excerpt: `const server = new Server(\n  {\n    name: "todoist-mcp-server",\n    version: "0.1.0",` - the call is truncated (no closing `}`/`);`), and the sibling-tool lines are `...`-elided; the snippets are not complete enough for standalone parsing. |
| QC-1.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - `CREATE_TASK_TOOL` and `Server` are defined in the snippet or SDK-provided. |
| QC-1.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no import of an unavailable module is present in the quoted snippets. |
| QC-1.3 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no imported module is left unused in the quoted snippets. |
| QC-3.2 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no referenced module is missing an import within the quoted snippets. |
| QC-3.3 | PASS | evidence: `TC-197-todoist-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code (the API token is read from `TODOIST_API_TOKEN`). |

QC totals: P0 = 1 (QC-0.1); P1 = 1 (QC-0.3); P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): **not satisfied** - Stage A produced one P0 finding (QD-T-1.4). In this non-blocking lite flow this is recorded as an informational finding and does not gate admission.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `todoist_create_task` has a `name`, a tool `description`, and a `description` on every parameter.

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
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared (the API token is read from an environment variable, not embedded).

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Candidate associations below are advisory context, physically separated from the stage verdicts, and use candidate wording only.

### Impact Card: QD-T-1.4 | additionalProperties not controlled | Inspect-P0 (Tool Schema)

- Static Discovery: artifact tool `todoist_create_task`; version label `2026-10-13`; evidence - `inputSchema` object declares `properties` with no `additionalProperties`.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion). Potential Impact D1 / D2 / D3. Mapping Strength: Medium - provisional (lite); per relevance-map.md section 1.3, a control-gap in the object schema may have impact under specific conditions (additional/reserved fields), pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

### Impact Card: QD-T-2.1 | string without length constraint | Inspect-P1 (Tool Schema)

- Static Discovery: artifact tool `todoist_create_task`; version label `2026-10-13`; evidence - `content`, `description`, and `due_string` are `string` types with no length bound.
- Potential Security Associations - candidate only: Candidate Attack Surface AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution). Potential Impact D2 / D3 / Availability. Mapping Strength: Conditional - provisional (lite); per relevance-map.md section 1.3, impact may depend on downstream handling and runtime behavior, pending dynamic verification. Strength is not severity.
- Note: This conclusion indicates priority for validation; it does not yet indicate that the backend is exploitable.
- Recommended Validation - NOT run by this lite inspector: Risk Explicit NOT run for association; Risk Implicit NOT run - dynamic exploitability is unverified. External controls: presence/absence UNKNOWN; per relevance-map.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

### QC FAILs

QC-0.1 and QC-0.3 (invalid/truncated excerpt) have no QD-level mapping row in relevance-map.md (the map covers QD-* defects only); no candidate AS-*/FM-* association is emitted for them.

Not run: Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifacts are absent. v1 scope: single-defect mapping only; defect chains are out of scope.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L2 checklist (P0 1, P1 1, P2 0); embedded-code QC (P0 1, P1 1, P2 0).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - 2 QD-T FAILs mapped; QC FAILs have no mapping row.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
