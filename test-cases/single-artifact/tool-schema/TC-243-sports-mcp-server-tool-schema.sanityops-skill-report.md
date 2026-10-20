# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-243-sports-mcp-server-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition authored as Zod via the `@cyanheads/mcp-ts-core` `tool(name, {...})` builder; structural signature `name` + `description` + `annotations` + Zod `input`/`output` converted to JSON Schema). The inspected object is the `sports_get_scores` tool, quoted from `src/mcp-server/tools/definitions/sports-get-scores.tool.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): `sports_get_scores` - **L1** - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-1.4 (P1) - the Zod `input` object (`z.object({...})`) is not declared `.strict()` and carries no `additionalProperties` control, so extra fields are accepted by default.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `sports_get_scores` -> **L1 (Low Risk)**.
Basis: a read-only scores query - the tool fetches live and final scores for a league on a date, with no state change; the annotations declare `readOnlyHint: true` and `openWorldHint: true`. No write, deletion/payment, permission change, or sensitive-data operation is declared. Per the tier rules ("any write operation -> L2 minimum; irreversible operations -> L3; sensitive data -> L3"), no higher-tier trigger applies, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - the tool carries a `name` (`sports_get_scores`), a `description`, and an `input` (`z.object(...)`). |
| QD-T-1.2 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - only `league` is non-optional (required); `date` and `team_name` are `.optional()`. No `required` entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - `LEAGUE_ENUM` (13 distinct league identifiers), the `status` enum, and the `source` enum contain no empty or duplicate value. |
| QD-T-1.4 | FAIL | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts`. Offending text: `input: z.object({ league: ..., date: ..., team_name: ... })` - the object is not `.strict()` and no `additionalProperties` control is declared. |
| QD-T-2.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - the string `team_name` carries `.max(200)`, and `date` is fixed-length via `.regex(/^\d{4}-\d{2}-\d{2}$/)`; no quoted string parameter is wholly unconstrained. |
| QD-T-2.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - the `input` object declares no `number`-type parameter, so no unbounded number exists to flag. |
| QD-T-4.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md`, `sports-get-scores.tool.ts` - the description states the capability and return surface, and every input parameter has a Zod `.describe(...)`. |

Tool totals: P0 = 0; P1 = 1; P2 = 0.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here. The `output` and `enrichment` schemas are output-side declarations, not input parameters, and are not the subject of the L1 parameter-constraint items. The sibling tools (`sports_get_schedule`, `sports_get_game`, ...) are referenced but not quoted; per the single-artifact boundary they are not judged here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (a `tool(name, {...})` definition whose Zod `input`/`output` generate the JSON Schema). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-4.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - the quoted TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - the code fence is labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - the quoted block is complete enough for standalone parsing (the imports, the `LEAGUE_ENUM`, and the `tool(...)` call open and close; the `handler`/`format` bodies are elided with `...`, which the illustrative-snippet rule permits). |
| QC-0.4 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - the code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - referenced names (`tool`, `z`, `easternToday`, `getEspnService`, `getMlbService`, `LEAGUE_ROUTES`, `inline`) are referenced consistently. |
| QC-1.2 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - imports (`@cyanheads/mcp-ts-core`, `@/services/...`) reference declared dependencies; no obviously nonexistent module is imported. |
| QC-1.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no file handle is opened in the quoted snippet. |
| QC-2.2 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no raw network connection is opened in the quoted snippet; calls go through the service helpers. |
| QC-2.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippet. |
| QC-3.1 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-243-sports-mcp-server-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `sports_get_scores` carries a `name`, a tool `description`, and a Zod `.describe(...)` on every parameter.

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

This stage scans the Tool Schema (`name` / `description` / input schema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no permission-level field, no dangerous capability boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example value, and no conflicting/approximate tool name is declared (`sports_get_scores` is semantically distinct from its siblings).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced one FAIL verdict; the candidate mapping follows. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P1 (L1)

- Static Discovery: artifact tool `sports_get_scores`; evidence - the Zod `input` object is not `.strict()` and no `additionalProperties` control is declared.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by the schema; impact depends on how the arguments are handled downstream.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 1, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Card for QD-T-1.4.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
