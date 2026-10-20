# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-230-mcp-open-library-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `title` + `description` + a Zod `schema`, converted to JSON Schema by the MCP SDK). The inspected object is the `search_books` tool: its `ToolDefinition` (`name` / `title` / `description` / `schema` / `annotations`) plus the `SearchBooksArgsSchema` argument schema, quoted from `src/tools/search-books/index.ts`. The case lists sibling tools (`get_book_by_id`, `get_book_by_title`, `get_book_cover`, `get_author_info`, `get_authors_by_name`, `get_author_photo`) by name only; they are not quoted and are outside the inspected content.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): Tool `search_books` (L1) - Inspect-P0 = 0, Inspect-P1 = 0, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings: none - the L1 minimal set produced no FAIL verdicts for this schema.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `search_books` -> **L1 (Low Risk)**.

Basis: read-only catalog query. The tool searches the public Open Library catalog and returns matching works; the definition carries the `READ_ONLY_LOOKUP` annotation and declares no write, deletion/payment, permission change, or sensitive-data handling. Per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3"), none of the higher-tier triggers apply, so the Tool is tiered L1.

### QD-T L1 full checklist (7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the `search_books` definition provides a `name` (`search_books`), a `title` ("Search books"), a `description`, and an `inputSchema` (`SearchBooksArgsSchema`). |
| QD-T-1.2 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - every field of `SearchBooksArgsSchema` is `.optional()`, so no `required` entry is declared and none references an undefined property; the "at least one criterion" rule is expressed by `.refine(...)`, not by a `required` list. |
| QD-T-1.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the `sort` enum is built from `SORT_VALUES` (new/old/random/key/rating/readinglog/want_to_read/currently_reading/already_read/title); it contains no empty, duplicate, or type-inconsistent value. |
| QD-T-1.4 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the argument schema is a Zod `z.object({...}).refine(...)`; Zod object semantics do not accept arbitrary extra fields as declared, and the schema declares no arbitrary extra-field acceptance, so no uncontrolled-additionalProperties defect is established from the artifact. |
| QD-T-2.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - every free-text string field declares a length bound (`q`, `title`, `author`, `subject`, `place`, `person`, `publisher`, `isbn` each use `.min(1)`), `language` uses a fixed-length `.regex(/^[a-z]{3}$/)`, and `sort` is enum-constrained. No length-unbounded plain string is present. |
| QD-T-2.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no literal number-type parameter is declared in the quoted schema; the pagination fields (`limit`, `offset`) delegate to the shared `searchLimitSchema`/`searchOffsetSchema`, which the artifact documents as bounded and does not quote, so no unbounded number is established from the quoted schema (per the single-artifact boundary). |
| QD-T-4.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the tool description is detailed (capability, the criterion list, the paging contract, and the downstream `edition_key` -> `get_book_by_id` affordance) and every parameter carries a `.describe(...)` string. |

Tool totals: P0 = 0; P1 = 0; P2 = 0.

Note on rule subjects absent at this tier: the L1 set does not include the string-format (QD-T-2.2) or array-length (QD-T-2.4) items, so those are not separately graded here.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes schema-source TypeScript (the imports/enums, the `SearchBooksArgsSchema`, and the `searchBooksTool` definition). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the quoted TypeScript parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - the code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - the quoted blocks are complete enough for standalone parsing (the first block carries its imports and closes the `z.object({...}).refine(...)` expression; the second block is a complete `export const searchBooksTool: ToolDefinition = {...};`). |
| QC-0.4 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - the declared `typescript` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - referenced names (`z`, `parseArgs`, `toErrorResult`, `jsonResult`, `textResult`, `OpenLibrarySearchResponse`, `SEARCH_FIELDS`, `searchLimitSchema`, `searchOffsetSchema`, `toSearchResults`, `READ_ONLY_LOOKUP`, `ToolDefinition`, `ToolHandler`) are imported in the first block; `handleSearchBooks` is the module's local handler. All are referenced consistently. |
| QC-1.2 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - the imports (`../../utils/errors.js`, `../../utils/results.js`, `../../utils/search.js`, `../types.js`, `zod`) reference declared project modules and the `zod` dependency; no obviously nonexistent module is imported. |
| QC-1.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no file handle is opened in the quoted snippets. |
| QC-2.2 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md`, `src/tools/search-books/index.ts` - the import list belongs to the module whose handler (`handleSearchBooks`) is not quoted; within the quoted excerpt no unused-import defect is established. |
| QC-3.2 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no referenced module is missing an import within the quoted excerpt. |
| QC-3.3 | PASS | evidence: `TC-230-mcp-open-library-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `search_books` carries a `name`, a `title`, a tool `description`, and a `.describe(...)` on every parameter.

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

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present (the `sort` enum values - new/old/random/key/rating/readinglog/want_to_read/currently_reading/already_read/title - are the catalog's declared ordering options, not permission levels).
- NR-S-5/6/8: no instruction poisoning in the description, no injected default/example value, and no conflicting/approximate tool name is declared (`search_books` is unique and stable).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
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
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - no Stage A FAILs to map.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
