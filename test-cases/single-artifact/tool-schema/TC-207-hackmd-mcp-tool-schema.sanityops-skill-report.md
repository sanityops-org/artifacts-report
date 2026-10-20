# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-207-hackmd-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definitions registered through `server.tool(name, description, params, annotations, handler)`; structural signature `name` + `description` + a Zod parameter object). The inspected object is the HackMD user-note tool set: `create_note` (the case's representative focus) together with the companion tools `list_user_notes`, `get_note`, `update_note`, and `delete_note`, plus the shared payload schemas `CreateNoteOptionsSchema` / `UpdateNoteOptionsSchema`, quoted from `tools/userNotes.ts` and `utils/schemas.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): user-note tool set (`create_note` representative) - **L3** - Inspect-P0 = 2, Inspect-P1 = 0, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema). G0-1 is not satisfied (2 unfixed Stage A P0) but is informational only in this non-blocking flow.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-1.4 (P0) - the payload object schema (`CreateNoteOptionsSchema = z.object({...})`) declares no `additionalProperties` control and is not `.strict()`.
  2. QD-T-2.1 (P0) - note string parameters (`title`, `content`, `permalink`, `noteId`) carry no `minLength`/`maxLength`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool set (representative `create_note` + `list_user_notes` / `get_note` / `update_note` / `delete_note`) -> **L3 (High Risk)**.

Basis: the quoted set contains an irreversible operation. `delete_note` performs deletion ("Delete a note"; annotations `destructiveHint: true`), and `update_note` also declares `destructiveHint: true`. Per the tier rules ("any write operation -> L2 minimum; irreversible operations -> L3; sensitive data -> L3"), the presence of the irreversible `delete_note` operation raises the tier to L3. (Had only `create_note`/`update_note` been quoted, the tier would be L2.) Note also that `update_note`/`delete_note` share the `CreateNoteOptionsSchema` / `UpdateNoteOptionsSchema` dependency, so the write and delete surfaces are inspected together.

### QD-T L3 full checklist (16 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `tools/userNotes.ts` - each tool provides a `name` (`create_note`, `list_user_notes`, `get_note`, `update_note`, `delete_note`), a `description` ("Create a new note", ...), and a parameter object. |
| QD-T-1.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `tools/userNotes.ts` - `noteId` is a required `z.string()` present in the parameter object for get/update/delete, and `payload` is required and present for create/update; no `required` entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `utils/schemas.ts` - the `readPermission`/`writePermission` enums (`owner`/`signed_in`/`guest`) and the `commentPermission` enum (`disabled`/`forbidden`/`owners`/`signed_in_users`/`everyone`) contain no empty or duplicate value. |
| QD-T-1.4 | FAIL | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `utils/schemas.ts`. The payload object schema is not declared `.strict()` and no `additionalProperties` control is declared. Offending text: `export const CreateNoteOptionsSchema = z.object({ title: z.string().optional().describe("Note title"), ... })` (Zod object without `.strict()`, no `additionalProperties`). |
| QD-T-2.1 | FAIL | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `utils/schemas.ts` / `tools/userNotes.ts`. Offending text: `content: z.string().optional().describe("Note content")` - no `minLength`/`maxLength` (likewise `title`, `permalink`, and `noteId`). |
| QD-T-2.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no quoted string parameter requires a specific format (permissions are enum-constrained), so no missing `pattern`/`format` is established. |
| QD-T-2.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no `number`-type parameter is declared, so no unbounded number exists to flag. |
| QD-T-2.4 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no `array`-type parameter is declared, so no unbounded array exists to flag. |
| QD-T-3.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md`, `tools/userNotes.ts` - the write tools identify the write action ("Create a new note", "Update an existing note", "Delete a note"); the write is not concealed. |
| QD-T-3.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - `title`/`content` are stored note data values, not a free-form query/command string passed to a backend interpreter; no raw command-passthrough is declared. |
| QD-T-3.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no batch operation is declared; each call acts on a single note (`noteId` scalar). |
| QD-T-3.4 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no internal-control parameter (`tenantId`, `admin`, `token`, role) is exposed in `properties`. |
| QD-T-3.5 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no cross-tool sensitive-data flow is declared (the tools operate on the caller's own HackMD notes; no external send is declared). |
| QD-T-4.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - tool descriptions and per-field `.describe(...)` texts are clear and self-describing. |
| QD-T-4.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the create/update/delete side effects are declared by the descriptions; no undeclared side effect is declared. |
| QD-T-4.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the tool names are semantically distinct (`list_user_notes`/`get_note`/`create_note`/`update_note`/`delete_note`); no near-duplicate competition is evident. |

Tool-set totals: P0 = 2; P1 = 0; P2 = 0.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (tool registrations and Zod payload schemas). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the quoted TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the quoted blocks are complete enough for standalone parsing (imports present, statements and the `registerUserNotesApiTools` function close). |
| QC-0.4 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - referenced names (`z`, `McpServer`, `API`, `CreateNoteOptionsSchema`, `UpdateNoteOptionsSchema`) are defined in the snippet or referenced consistently. |
| QC-1.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - imports (`@modelcontextprotocol/sdk`, `@hackmd/api`, `zod`) reference declared dependencies; no obviously nonexistent module is imported. |
| QC-1.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no raw network connection is opened in the quoted snippets (calls go through the injected `client`). |
| QC-2.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-207-hackmd-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): **not satisfied** - Stage A produced 2 P0 findings (QD-T-1.4, QD-T-2.1). Recorded as informational; it does not gate in this non-blocking flow.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - the tools carry a `name`, a tool `description`, and per-parameter `.describe(...)` text.

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

This stage scans the Tool Schema (`name` / `description` / parameter schema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: the `readPermission`/`writePermission`/`commentPermission` enum fields are the tool's declared sharing model (an intended domain field, not a permission level exceeding design scope); no dangerous boolean/enum flag and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example value, and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced two FAIL verdicts; candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P0 (L3)

- Static Discovery: artifact tool `create_note` (and the shared `CreateNoteOptionsSchema`/`UpdateNoteOptionsSchema`); evidence - the Zod payload object is not `.strict()` and no `additionalProperties` control is declared.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by the schema; impact depends on how the payload is forwarded to the HackMD API.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-2.1 | String Without Length Constraint | Inspect-P0 (L3)

- Static Discovery: artifact tool `create_note` (and companions); evidence - `content: z.string().optional()` (likewise `title`, `permalink`, `noteId`) carries no `minLength`/`maxLength`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded string may yield an oversized payload; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L3 checklist (P0 2, P1 0, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
