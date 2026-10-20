# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-235-lastfm-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definitions registered through `server.registerTool(name, { description, inputSchema }, handler)`; structural signature `name` + `description` + a Zod parameter object). The inspected object is the Last.fm public tool set: `ping`, `server_info`, `get_track_info`, `get_artist_info`, `get_album_info`, `get_artist_top_tracks`, and `get_similar_artists`, quoted verbatim from `src/mcp/tools/public.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): public tool set - **L1** - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 1. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings:
  1. QD-T-1.4 (P1) - the Zod `inputSchema` objects (`z.object({...})`) declare no `additionalProperties` control and are not `.strict()`.
  2. QD-T-2.1 (P2) - the string parameters (`message`, `artist`, `track`, `album`, `username`, `mbid`) carry no `minLength`/`maxLength`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool set (`ping`, `server_info`, `get_track_info`, `get_artist_info`, `get_album_info`, `get_artist_top_tracks`, `get_similar_artists`) -> **L1 (Low Risk)**.
Basis: every quoted tool is a read-only query over public Last.fm data ("No authentication required"). There is no write, deletion/payment, permission change, or sensitive-data handling declared. Per the tier rules ("any write operation -> L2 minimum; irreversible operations -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts` - each tool provides a `name` (`ping`, `get_track_info`, ...), a `description`, and an `inputSchema` (`z.object({...})`). |
| QD-T-1.2 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts` - required fields (`artist`, `track`, `album`) are declared without `.optional()` and present in the object; optional fields (`username`, `mbid`, `limit`) are `.optional()`. No required entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts` - no `enum` is declared in the quoted schemas, so no invalid enum exists to flag. |
| QD-T-1.4 | FAIL | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts`. The parameter objects are plain Zod objects with no `.strict()` and no `additionalProperties` control. Offending text: `inputSchema: z.object({ artist: z.string().describe('Artist name'), track: z.string().describe('Track name'), username: z.string().optional().describe('Last.fm username (optional, for user-specific data)') })` (Zod object without `.strict()`). |
| QD-T-2.1 | FAIL | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts`. Offending text: `artist: z.string().describe('Artist name')` - no `minLength`/`maxLength` (likewise `track`, `album`, `message`, `username`, `mbid`). |
| QD-T-2.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts` - the only number parameter, `limit: z.coerce.number().min(1).max(50)` (and `.min(1).max(100)` in `get_similar_artists`), carries a boundary. |
| QD-T-4.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md`, `src/mcp/tools/public.ts` - the tool descriptions state what each tool returns and every field carries a `.describe(...)` naming its meaning. |

Tool-set totals: P0 = 0; P1 = 1; P2 = 1.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here. The additional public tool `get_artist_top_albums` is described in the prose but its schema block is not quoted; per the single-artifact boundary it is not graded here, and the authenticated tools in `src/mcp/tools/authenticated.ts` are outside the quoted artifact.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the tool registrations and their Zod parameter objects). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - the quoted TypeScript parses as valid syntax (handler bodies are elided with `/* ... */`, so the excerpt is illustrative per the illustrative-snippet rule). |
| QC-0.2 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - the code fence is labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - the handler bodies are elided with `/* ... */`; treated as an illustrative snippet per the illustrative-snippet rule. |
| QC-0.4 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - the code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - referenced names (`McpServer`, `CachedLastfmClient`, `z`) are declared types or referenced consistently in the excerpt. |
| QC-1.2 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no import of an unavailable module is present in the quoted snippet. |
| QC-1.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no file handle is opened in the quoted snippet. |
| QC-2.2 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no raw network connection is opened in the quoted snippet. |
| QC-2.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippet. |
| QC-3.1 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no referenced module is missing an import within the quoted snippet. |
| QC-3.3 | PASS | evidence: `TC-235-lastfm-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - each tool carries a `name`, a tool `description`, and per-field `.describe(...)` text.

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

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6: no instruction poisoning in a description and no injected instruction/dangerous value in a default/example field (the numeric `limit` defaults are benign domain values).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-8: the tool names are semantically distinct and parallel (`get_track_info` / `get_artist_info` / `get_album_info`; `get_artist_top_tracks` / `get_artist_top_albums`); no conflicting or approximate-duplicate name is declared.
- NR-S-9/10: no hardcoded literal secret and no PII value is declared.

Risk-Explicit totals: Explicit·P0 = 0; Explicit·P1 = 0; Explicit·P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced two FAIL verdicts; candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (L1)

- Static Discovery: artifact tools `ping`, `get_track_info`, `get_artist_info`, `get_album_info`, `get_artist_top_tracks`, `get_similar_artists`; evidence - the Zod parameter objects are not `.strict()` and declare no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by the schema; impact depends on how arguments are forwarded to the Last.fm API.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-2.1 | String Without Length Constraint | Inspect-P2 (L1)

- Static Discovery: artifact tools as above; evidence - `artist` / `track` / `album` / `message` / `username` / `mbid` strings carry no `minLength`/`maxLength`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded string may yield an oversized query; impact depends on backend limits.
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
Stage E (Risk Explicit EX): Executed - Explicit·P0 0, Explicit·P1 0, Explicit·P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
