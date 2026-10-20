# SanityOps Inspect Lite - Skill Report

Artifact: TC-192-spotify-mcp-tool-schema.md (Tool Schema; varunneal/spotify-mcp, tool `SpotifySearch`)

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## 1. Executive summary

- Stages executed: Stage A (single-artifact QD-T inspection + embedded-code QC baseline), Stage C (Gate-0 verification), Stage E (Risk Explicit audit), Stage F (candidate impact outlook). Stages B and D Not Executed for structural reasons (see status board).
- Inspected tool: `SpotifySearch` (the case's one logical artifact; generated inputSchema from the Pydantic `Search` model). Siblings (Playback/Queue/GetInfo/Playlist) are listed but not quoted, so they are outside the inspected content.
- Finding counts (counted as (tool, rule) FAIL verdicts):
  - P0 = 0
  - P1 = 1
  - P2 = 2
- Distinct failed rule IDs: QD-T-1.4, QD-T-2.1, QD-T-2.3.
- Gate result: Gate-0 Not passed - G0-3 unsatisfied (a lone Tool Schema carries no responsibility boundary baseline).
- Risk-Explicit summary: 0 items. Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-T-1.4 - the generated object schema declares no additionalProperties control.
  2. QD-T-2.3 - `limit: Optional[int] = Field(default=10, ...)` has no minimum/maximum.
  3. QD-T-2.1 - string parameters (query, qtype) carry no minLength/maxLength.
- NOT run by this lite inspector: Risk Implicit (dynamic exploitability) and the runtime Quality subset. The only Quality check executed is the lite QC baseline over embedded code snippets (see Stage A, QC block).
- Upgrade pointer: for the full Inspect ruleset plus Risk (Explicit/Implicit) and Quality subsets, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md

This summary states no security and no quality conclusion.

## 2. Stage A - Tool Schema inspection (QD-T)

### 2.0 Tier determination

| Tool | Tier | Basis |
| --- | --- | --- |
| SpotifySearch | L1 | read-only catalog search; no state change |

Tier rule applied: L1 read-only; any write operation -> L2 minimum; irreversible operation -> L3; sensitive data -> L3 (tool-checklist.md "Tool risk tiers"). Note (scope): the server also exposes playback/queue tools that may change state, but their schemas are not quoted; only `SpotifySearch` is inspected.

### 2.1 Tool: SpotifySearch (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | TC-192-spotify-mcp-tool-schema.md, tool "SpotifySearch": name (prefixed "Spotify" + class name) + description (class docstring "Search for tracks, albums, artists, or playlists on Spotify.") + inputSchema (model_json_schema()) present |
| QD-T-1.2 | PASS | query required (no default); qtype/limit have defaults; consistent with properties |
| QD-T-1.3 | PASS | no enum declared (qtype is a free string with an inline value list) |
| QD-T-1.4 | FAIL | generated object schema declares no additionalProperties: `inputSchema=cls.model_json_schema()` (the quoted Pydantic `Search` model declares no extra-key handling) |
| QD-T-2.1 | FAIL | string parameters unbounded: `query: str = Field(description="query term")` and `qtype: Optional[str] = Field(default="track", ...)` (no minLength/maxLength) |
| QD-T-2.3 | FAIL | integer parameter unbounded: `limit: Optional[int] = Field(default=10, description="Maximum number of items to return")` (no minimum/maximum) |
| QD-T-4.1 | PASS | description and field descriptions are present and clear |

### 2.2 Stage A summary counts

- P0 (0).
- P1 (1): QD-T-1.4.
- P2 (2): QD-T-2.1, QD-T-2.3.

### 2.3 QC - embedded code contract (Stage A Quality sub-check)

- QC-0.1 / QC-0.2 / QC-0.3: Not applicable - no code snippet is embedded in a Tool Schema description, default, or example field. (The quoted `ToolModel`/`Search` Python models are the schema definition, outside QC scope.)
- QC-1/QC-2/QC-3: Not applicable.
- QC-0 baseline status: no snippets to validate.

## 3. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission)

| Condition | Verification | Result |
| --- | --- | --- |
| G0-1 (no unfixed P0 in Stage A) | read Stage A | Satisfied - Stage A has no P0 findings |
| G0-2 (no unfixed P0 in Stage B) | read Stage B | Informational - Stage B Not Executed |
| G0-3 (responsibility boundary statements exist and are locatable) | locatability check | Not satisfied - a lone Tool Schema declares no responsibility boundary baseline |
| G0-4 (each Tool Schema name/description/parameter descriptions complete) | field-by-field | Satisfied - the tool carries a name, a description, and per-field descriptions |

Gate-0 result: Not passed - G0-3 unsatisfied (no responsibility baseline; proportionality has no reference). Gate-0 is not an inspection item and produces no score; "not passed" is not FAIL and is not a permission conclusion.

## 5. Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set (only a Tool Schema was supplied; no System Prompt and no Skill).
Wording note: Permission is reported as "Not Executed"; it is never reported as FAIL or "ERROR/BLOCKED".
Mandatory scope statement: this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

## 6. Stage E - Risk Explicit (EX) audit

Physically separated from the Inspect verdicts above. Risk Explicit is a static-text risk scan, not a defect verdict and not a security conclusion.

Audit object: TC-192-spotify-mcp-tool-schema.md (SpotifySearch). Scan order: NL-A -> NL-B -> NR-O -> NR-S.

| EX ID | Risk expression (short excerpt) | Impact labels | Grade | Trigger | Disposition |
| --- | --- | --- | --- | --- | --- |
| (none) | no explicitly expressed risk item found | - | - | - | - |

Risk Item Summary: Total = 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

Notes:
- The tool is read-only search. Spotify credentials are read from environment variables (SPOTIFY_CLIENT_ID/SECRET/REDIRECT_URI), so no secret value appears in the text (NR-S-9 not hit). No hidden instructions or capability-enabling flags are present.
- Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Physically separated from the stage verdicts. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subset were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md (relevance.md Sec. 1.4), no assumption is made that controls outside the artifacts are absent. This section is single-defect mapping only.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | P1 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-08 (Configuration, Naming, and Supply Chain Confusion)
- Potential Impact: D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted; impact depends on how the search backend treats unexpected arguments.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

### Impact Card: QD-T-2.1 / QD-T-2.3 | Parameter constraint missing (string length / number bound) | P2 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded query/limit may yield an oversized result set; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

Mandatory statements for every card: Risk Explicit was executed in Stage E (0 items); Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

## 8. Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist run for SpotifySearch; QC baseline applied (no embedded snippets)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-3 unsatisfied (no responsibility boundary baseline in a lone Tool Schema)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 items (Explicit-P0 0, Explicit-P1 0, Explicit-P2 0)
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1/2.3
Stage G (Self-verification): Executed - report-level checks

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
