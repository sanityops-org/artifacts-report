# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-214-elevenlabs-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + docstring `description` + signature-derived `inputSchema`). The inspected object is the `text_to_speech` tool: its FastMCP `@mcp.tool(...)` decorator (description + `ToolAnnotations`) and typed function signature from `elevenlabs_mcp/server.py`.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): `text_to_speech` - **L2** - Inspect-P0 = 1, Inspect-P1 = 3, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema). G0-1 is not satisfied (1 unfixed Stage A P0) but is informational only in this non-blocking flow.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-1.4 (P0) - the signature-derived object schema declares no `additionalProperties` control.
  2. QD-T-2.1 (P1) - the string parameters (`text`, `voice_name`, `output_directory`, `voice_id`, `language`, `model_id`) carry no `minLength`/`maxLength`.
  3. QD-T-2.2 (P1) - `language` and `output_format` require specific formats but are declared as plain `str` with no `pattern`/`format`/`enum`.
  4. QD-T-2.3 (P1) - the numeric parameters (`stability`, `similarity_boost`, `style`, `speed`) carry no `minimum`/`maximum` in the schema (ranges documented only in prose).
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `text_to_speech` -> **L2 (Medium Risk)**.

Basis: state-changing, recoverable. The tool converts text to speech and, per its signature (`output_directory: str | None`) and description, saves the generated audio to files or returns it as an MCP resource ("Directory where files should be saved"); it also performs an external API call that may incur cost. It performs a write (audio-file output) and no deletion/payment or sensitive-data handling is declared, so per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3") the Tool is tiered L2. (The declared `readOnlyHint: true` does not remove the declared file-write behaviour.)

### QD-T L2 full checklist (12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py` - the tool provides a `name` (`text_to_speech`), a decorator `description` ("Convert text to speech with a given voice."), and a signature-derived `inputSchema` (`text: str, voice_name: str | None = None, ...`). |
| QD-T-1.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py` - `text` has no default (required) and is present in the signature; all other parameters have defaults (optional). The required/optional split is consistent with the declared properties. |
| QD-T-1.3 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no `enum` is declared in the schema, so no invalid enum exists to flag (the allowed `output_format`/`model_id` values are listed only in prose). |
| QD-T-1.4 | FAIL | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py`. The signature-derived object schema declares no `additionalProperties` control. Offending text: `def text_to_speech(text: str, voice_name: str | None = None, output_directory: str | None = None, ...)` (FastMCP-derived object schema with no declared `additionalProperties`, so arbitrary extra fields are accepted by default at the JSON-Schema level). |
| QD-T-2.1 | FAIL | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py`. Offending text: `text: str, ... voice_name: str | None = None, output_directory: str | None = None, voice_id: str | None = None, ... language: str = "en", ... model_id: str | None = None` - no `minLength`/`maxLength` is declared for these string parameters. |
| QD-T-2.2 | FAIL | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py`. Offending text: `language: str = "en"` (documented as "ISO 639-1 language code") and `output_format: str = "mp3_44100_128"` (documented as "Must be one of:" a fixed codec list) - both require a specific format but are declared as plain `str` with no `pattern`/`format`/`enum`. |
| QD-T-2.3 | FAIL | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py`. Offending text: `stability: float = 0.5, similarity_boost: float = 0.75, style: float = 0, ... speed: float = 1.0` - no `minimum`/`maximum` is declared for these numeric parameters (the ranges 0-1 and 0.7-1.2 are documented only in the docstring prose). |
| QD-T-2.4 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no `array`-type parameter is declared, so no unbounded array exists to flag. |
| QD-T-3.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py` - the description and the `output_directory` parameter document that generated audio is returned/saved ("Directory where files should be saved ... Returns: Text content with file path or MCP resource with audio data"); the write/output behaviour is identified. |
| QD-T-3.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - `text` is the content to synthesize (a data value), not a free-form query/command string passed to a backend interpreter; no raw command-passthrough is established. |
| QD-T-4.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md`, `elevenlabs_mcp/server.py` - the description is detailed (capability, mutual-exclusion rule, cost warning, per-parameter ranges, enumerated `output_format`/`model_id` values, return shape). |
| QD-T-4.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the declared side effects (external API call with possible cost, and audio file/resource output) are documented; no undeclared side effect is declared. |

Tool totals: P0 = 1; P1 = 3; P2 = 0.

Note on rule subjects absent at this tier: no `enum` (QD-T-1.3) and no array parameter (QD-T-2.4); those subjects are not present to flag.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes Python source (the FastMCP decorator, description, and typed signature). No code is embedded inside schema description/default/example fields; the quoted schema-source code is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the quoted Python parses as valid syntax. |
| QC-0.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the code fences are labeled `python`. |
| QC-0.3 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the decorator/signature block is complete; the trailing function body is explicitly elided by the enclosing text ("The function body continues in `server.py` ..."), which the illustrative-snippet rule exempts from the parse-completeness requirement. |
| QC-0.4 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - each code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the declared `python` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - referenced names (`ToolAnnotations`, `FastMCP`, `make_error`, `client`, `DEFAULT_VOICE_ID`, `Union`, `TextContent`, `EmbeddedResource`, `get_output_mode_description`) are referenced consistently; the snippet is an excerpt of `server.py`. |
| QC-1.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - the quoted fragment imports no module; no invalid import is established. |
| QC-1.3 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no file handle is opened in the quoted snippet (output handling is in the elided body). |
| QC-2.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no network connection is opened in the quoted snippet (the API call is via the injected `client` in the elided body). |
| QC-2.3 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippet. |
| QC-3.1 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no import statement is present in the quoted fragment, so no unused import exists. |
| QC-3.2 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-214-elevenlabs-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted code (the credential comes from `ELEVENLABS_API_KEY`; the `$HOME/Desktop` default is a generic placeholder, not a machine-specific literal). |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): **not satisfied** - Stage A produced 1 P0 finding (QD-T-1.4). Recorded as informational; it does not gate in this non-blocking flow.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; no responsibility-boundary / duty baseline statement exists within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - the tool carries a `name`, a decorator `description`, and an `Args:` block describing every parameter.

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

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present (the cost warning is a usage caution, not a dangerous capability flag).
- NR-S-5/6/8: no instruction poisoning, no injected default/example value, and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared in the schema.
- NR-S-9/10: no hardcoded literal secret or PII value is declared (the API key and base path come from environment variables).

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced four FAIL verdicts; candidate mappings follow. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P0 (L2)

- Static Discovery: artifact tool `text_to_speech`; evidence - the signature-derived object schema declares no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted at the JSON-Schema level; impact depends on whether the framework maps them onto the call.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable.

### Impact Card: QD-T-2.1 / QD-T-2.2 / QD-T-2.3 | Parameter Constraint Missing (length / format / number) | Inspect-P1 (L2)

- Static Discovery: artifact tool `text_to_speech`; evidence - strings carry no length bound, `language`/`output_format` carry no `pattern`/`format`/`enum`, and the numeric parameters carry no `minimum`/`maximum`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - unconstrained `text`/`output_format`/numeric values may reach the synthesis backend before validation; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L2 checklist (P0 1, P1 3, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1/2.2/2.3.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
