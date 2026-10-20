# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-237-tmdb-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definitions registered through `server.registerTool(name, { title, description, inputSchema, outputSchema, annotations }, handler)`; structural signature `name` + `description` + a Zod parameter object). The inspected object is the TMDB tool set: `search_movies`, `search_tv`, `search_multi`, and `get_movie` (representative focus), with additional tools named (`search_people`, `search_keywords`, `search_companies`, `search_watch_providers`, `get_tv`, `get_movies`, `get_tv_shows`, `get_person`, `get_person_credits`, `get_tv_season`, `discover_movies`, `discover_tv`), quoted verbatim from `src/tools/tmdb/search.ts` and `src/tools/tmdb/details.ts`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): TMDB tool set - **L1** - Inspect-P0 = 0, Inspect-P1 = 0, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 1.
- Top findings: none from Inspect - the L1 minimal set produced no FAIL verdicts (the input schemas are `z.strictObject`, which surfaces as `additionalProperties: false`, and the quoted string field `query` carries `.min(1)`). One Risk-Explicit static item was recorded (see Stage E): the near-identical tool names `get_movie` vs `get_movies` (NR-S-8).
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool set (`search_movies`, `search_tv`, `search_multi`, `get_movie`, plus the named companions) -> **L1 (Low Risk)**.
Basis: every quoted tool is a read-only TMDB search/detail lookup; the registrations carry `annotations: READ_ONLY`. There is no write, deletion/payment, permission change, or sensitive-data handling declared. Per the tier rules ("any write operation -> L2 minimum; irreversible operations -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` / `details.ts` - each tool provides a `name` (`search_movies`, `search_tv`, `search_multi`, `get_movie`), a `description`, and an `inputSchema`. |
| QD-T-1.2 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` / `details.ts` - each `inputSchema` is a `z.strictObject({...})` whose members (`query`, `year`, `include_adult`, `language`, `region`, `page`, `id`, `include_ratings`) are declared with the corresponding optionality (`page: page.optional()`); no required entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` / `details.ts` - no `enum` is declared in the quoted schemas, so no invalid enum exists to flag. |
| QD-T-1.4 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` / `details.ts` - every input schema is a Zod `strictObject` (e.g. `inputSchema: z.strictObject({ query: z.string().min(1).describe(...), ... })`), which surfaces as JSON Schema `additionalProperties: false`; the object accepts no uncontrolled extra fields. |
| QD-T-2.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` - the only fully quoted string parameter, `query: z.string().min(1).describe("Movie title to search for.")`, carries a `minLength` bound; the remaining string-like fields (`year`, `language`, `region`) are shared field schemas defined in `src/tools/tmdb/fields.ts`, which the artifact states were not fetched and are therefore not judged here (single-artifact boundary). |
| QD-T-2.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no `number`-type parameter is quoted (the `year` field is a shared schema not fetched), so no unbounded number is established. |
| QD-T-4.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md`, `src/tools/tmdb/search.ts` / `details.ts` - the descriptions are explicit about each tool's return shape, tool boundaries, and chaining contract, and each quoted field carries a `.describe(...)`. |

Tool-set totals: P0 = 0; P1 = 0; P2 = 0.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not graded here. The shared field schemas (`year`, `include_adult`, `language`, `region`, `page`, `tmdbId`, `include_ratings`) are referenced by name; their internal definitions were not fetched, so per the single-artifact boundary they are not judged here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the tool registrations and their `z.strictObject` parameter objects). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - the quoted TypeScript parses as valid syntax (each `server.registerTool(...)` call closes). |
| QC-0.2 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - the quoted blocks are complete enough for standalone parsing (each `registerTool` call is fully closed). |
| QC-0.4 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - referenced names (`z`, `yearFilter`, `includeAdult`, `language`, `region`, `page`, `tmdbId`, `pageSchema`, `movieSummarySchema`, `READ_ONLY`, `requireTmdb`, `getEnrichedDetail`, `tmdb`, `omdb`) are module-scope symbols referenced consistently in the excerpt. |
| QC-1.2 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no import of an unavailable module is present in the quoted snippets. |
| QC-1.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no raw network connection is opened in the quoted snippets (calls go through the injected `tmdb`/`omdb` clients). |
| QC-2.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no unused import is evident. |
| QC-3.2 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no referenced module is missing an import within the quoted snippets. |
| QC-3.3 | PASS | evidence: `TC-237-tmdb-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - each quoted tool carries a `name` (the registration's first argument), a tool `description`, and the quoted parameter `query` carries a `.describe(...)`; shared-field descriptors live in `fields.ts` and were not quoted.

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

Phase 1 - Discovery and classification: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> one item (NR-S-8).

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present.
- NR-S-5/6: no instruction poisoning in a description and no injected instruction/dangerous value in a default/example field.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret and no PII value is declared (the `OMDB_API_KEY` reference is an environment-variable name, not a literal credential).

Risk Item 1
- EX Classification: NR-S-8 (Tool Name Conflict/Approximate Misleading)
- Risk Expression: the near-identical tool names `get_movie` versus `get_movies` (and the parallel `get_tv` versus `get_tv_shows`) are declared in the same tool surface.
- Impact Type Labels: D2
- Severity Grade: Explicit·P2
- Reason: worst consequence is a tool mis-selection between two read-only detail lookups that return differently-shaped payloads; both operate read-only within the same permission scope, so this is graded Explicit·P2 (read-only / within existing scope). The item's descriptions do disambiguate the two tools explicitly ("use get_movies instead; it's trimmed on purpose"), which mitigates the trigger likelihood but is not used to downgrade the grade.
- Trigger Condition Label: unconditional
- Disposition: Record in risk ledger

Risk-Explicit totals: Explicit·P0 = 0; Explicit·P1 = 0; Explicit·P2 = 1.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced **no FAIL verdicts** for this schema, so there are **no Inspect candidate mappings to emit**. The Stage E NR-S-8 item is a Risk-Explicit static-document risk finding, physically separated from the Inspect verdicts, and the relevance-map.md single-defect tables map QD IDs only (no AS-*/FM-* association is defined there for EX classifications); no mapping is emitted for it.

Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist (P0 0, P1 0, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit·P0 0, Explicit·P1 0, Explicit·P2 1 (NR-S-8).
Stage F (Impact outlook):   Executed - no Stage A FAILs to map.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
