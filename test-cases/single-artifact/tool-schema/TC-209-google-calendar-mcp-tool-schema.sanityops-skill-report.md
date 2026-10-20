# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-209-google-calendar-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `inputSchema` as a Zod object, exposed through a `ToolSchemas` registry). The inspected object is the `list-events` tool: the `ToolSchemas['list-events']` Zod schema and its shared field schemas (`ianaTimeZone`, `timeMinSchema`, `timeMaxSchema`, `timeZoneSchema`, `fieldsSchema`, `multiAccountSchema`), quoted from `src/tools/registry.ts`, plus the matching `ListEventsArgs` interface from `src/handlers/core/ListEventsHandler.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): `list-events` - **L1** - Inspect-P0 = 1, Inspect-P1 = 1, Inspect-P2 = 1. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline in a lone Tool Schema) and G0-4 (the quoted artifact provides the tool `name` and input schema but no tool-level `description`). G0-1 is not satisfied (1 unfixed Stage A P0) but is informational only in this non-blocking flow.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-1.1 (P0) - the inspected `list-events` tool schema exposes `name` and `inputSchema` but no tool-level `description` base field.
  2. QD-T-1.4 (P1) - the `z.object({...})` schema declares no `additionalProperties` control and is not `.strict()`.
  3. QD-T-2.1 (P2) - the `calendarId` string branch carries no `minLength`/`maxLength`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `list-events` -> **L1 (Low Risk)**.

Basis: read-only calendar query. The tool lists events from one or more calendars and returns them; it performs no write, deletion/payment, permission change, or sensitive-data handling (the `ToolRegistry` maps the schema to a read handler). Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1. The other calendar tools listed in the case (create/get/update/delete event, search-events, free-busy, list-calendars) are not quoted and are therefore not tiered or inspected here.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | FAIL | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts`. The inspected tool schema provides the tool `name` (the registry key `'list-events'`) and the `inputSchema` (`z.object({...})`), but no tool-level `description` field is present in the quoted artifact. Offending text: `export const ToolSchemas = { 'list-calendars': z.object({...}), 'list-events': z.object({ ... }), }` (a bare schema-registry entry with no tool `description`). Under the single-artifact boundary (SKILL.md section 4, Stage A), a declaration missing from the inspected artifact is a defect of that artifact. |
| QD-T-1.2 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts` / `ListEventsHandler.ts` - `calendarId` (the union without `.optional()`) is required and present in the schema; the remaining fields are `.optional()`. No `required` list references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts` - the only `enum` (`z.enum(ALLOWED_EVENT_FIELDS)`) draws its members from a constant defined elsewhere in the same file; no empty, duplicate, or type-inconsistent value is evident in the quoted composition. |
| QD-T-1.4 | FAIL | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts`. The `list-events` object schema is a `z.object({...})` that is not declared `.strict()`, and no `additionalProperties` control is declared. Offending text: `'list-events': z.object({ account: multiAccountSchema, calendarId: ..., timeMin: timeMinSchema, ... })` (Zod object without `.strict()`, no `additionalProperties`). |
| QD-T-2.1 | FAIL | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts`. Offending text: `calendarId: z.union([ z.string().describe("Calendar identifier(s) to query. ..."), z.array(z.string().min(1)).min(1).max(50) ])` - the string branch carries no `minLength`/`maxLength`. (The `timeMin`/`timeMax` string fields carry a format `.refine(...)`, and the `account` string carries an `accountIdRegex`; those are treated as bounded, consistent with the template's treatment of pattern-constrained strings.) |
| QD-T-2.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no `number`-type parameter is declared, so no unbounded number exists to flag. |
| QD-T-4.1 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md`, `src/tools/registry.ts` - the parameter descriptions are detailed and give concrete examples (ISO 8601 formats, `'primary'`, `['Work', 'Personal']`, `'America/Los_Angeles'`), and the extended-property filters explain their matching semantics. (This grades the parameter-level descriptions; the missing tool-level `description` is scored under QD-T-1.1.) |

Tool totals: P0 = 1; P1 = 1; P2 = 1.

Note on rule subjects absent at this tier: no `number` parameter (QD-T-2.3); QD-T-2.2 (string format) and QD-T-2.4 (array length) are not in the L1 set (though the quoted arrays `fields`/`privateExtendedProperty`/`sharedExtendedProperty` carry no length bound, that is an out-of-L1-tier subject and is not graded here).

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the shared validation helpers, the `ToolSchemas` registry, and the handler interface). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - the quoted TypeScript parses as valid syntax; the registry block is a bounded excerpt of a larger object (the remaining tool entries are omitted), which the enclosing case notes mark as the quoted portion. |
| QC-0.2 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - the quoted helpers and the `list-events` entry are complete enough for the covered parsing; helpers referenced but not quoted (`isValidTimeZone`, `parseJsonStringArray`, `ALLOWED_EVENT_FIELDS`, `accountIdRegex`) are stated by the case notes to be defined elsewhere in the same file. |
| QC-0.4 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - referenced names (`z`, `isValidTimeZone`, `parseJsonStringArray`, `ALLOWED_EVENT_FIELDS`, `accountIdRegex`) are either defined in the snippet or stated by the case notes to be defined elsewhere in the same file. |
| QC-1.2 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - the only import is `zod`, a declared schema dependency; no obviously nonexistent module is imported. |
| QC-1.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - `z` is used throughout the quoted snippets; no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-209-google-calendar-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code (the time-zone examples are documentation examples, not machine-specific literals). |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): **not satisfied** - Stage A produced 1 P0 finding (QD-T-1.1). Recorded as informational; it does not gate in this non-blocking flow.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): **FAIL** - the quoted `list-events` schema provides `name` and parameter descriptions, but no tool-level `description` field is present, so the field-by-field completeness check is not satisfied.

Gate-0 result: **Not passed - G0-3 and G0-4**.

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - Gate-0 not satisfied, and the full artifact set is unavailable.

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-3, G0-4
Blocking Reasons:
  G0-3 - no responsibility-boundary / duty baseline statement exists in a lone Tool Schema; proportionality has no reference.
  G0-4 - the Tool Schema's `description` field is not present in the inspected artifact, so operation semantics cannot be fully determined.
  Artifact set - the full set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

Scope statement (permission-checklist.md section 5): this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / `inputSchema`) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning, no injected default/example value, and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced three FAIL verdicts; candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.1 | Base Field Missing (tool `description`) | Inspect-P0 (L1)

- Static Discovery: artifact tool `list-events`; evidence - the registry entry provides `name` and `inputSchema` but no tool-level `description`.
- Candidate Attack Surface: AS-05 (Tool Misuse and High-Risk Side Effects), AS-09 (Cross-Artifact Contract Breach)
- Potential Impact: D2, Availability
- Mapping Strength: Conditional (provisional (lite)) - a missing tool description may degrade tool-selection clarity; impact depends on the client's tool-selection context.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (L1)

- Static Discovery: artifact tool `list-events`; evidence - the `z.object({...})` schema declares no `additionalProperties` control and is not `.strict()`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted; impact depends on how the arguments reach the Calendar API.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

### Impact Card: QD-T-2.1 | String Without Length Constraint | Inspect-P2 (L1)

- Static Discovery: artifact tool `list-events`; evidence - the `calendarId` string branch carries no `minLength`/`maxLength`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded `calendarId` string may yield an oversized query; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 1, P1 1, P2 1); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3 and G0-4.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3, G0-4); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.1, QD-T-1.4, and QD-T-2.1.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
