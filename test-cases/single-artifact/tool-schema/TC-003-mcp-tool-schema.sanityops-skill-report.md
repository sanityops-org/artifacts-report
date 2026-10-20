# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-003-mcp-tool-schema.json` (raw JSON; the file has no Markdown `## Metadata` block).
- Classification: **Tool Schema** (structural signature: an object carrying `name` + `description` + an input-schema container).
- Inspected artifact content: the `tool_schema` object (`name: "github_mcp_research"`, its `description`, and its `parameters` JSON Schema). The surrounding `meta`, `example_usage`, `evaluation_dimensions`, `scoring_template`, `test_cases` and `notes` fields are treated as case scaffolding; the `example_usage.python_code` snippet is additionally passed to the lite embedded-code QC.
- Working version label: `2026-10-10` (the case's `meta.collection_date`).
- The inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T) result for `github_mcp_research`: Inspect-P0 = 7, Inspect-P1 = 0, Inspect-P2 = 0. Embedded-code QC result: P0 = 0, P1 = 0, P2 = 2.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema) is unsatisfiable.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 1.
- Top findings (up to five):
  1. QD-T-3.4 - schema exposes caller-supplied `command` / `args` / `env` parameters that should be system-controlled.
  2. QD-T-3.2 - free-form `command` and `query` strings are accepted and passed through to backend process launch / the research backend.
  3. QD-T-4.2 - launching an external MCP server process is an undeclared side effect of the tool.
  4. QD-T-2.4 / QD-T-3.3 - the `mcp_configs` array declares no `maxItems`, i.e. an unbounded batch.
  5. QD-T-1.4 - parameter objects declare no `additionalProperties` control.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `github_mcp_research` -> **L3 (High Risk)**.
Basis: the schema exposes `mcp_configs[].command` and `mcp_configs[].args` (a command used to launch an external MCP server process) together with `mcp_configs[].env` (caller-supplied environment variables; the artifact's own example passes `GITHUB_TOKEN`). External process launch plus caller-supplied credential/environment values are sensitive-data handling -> per the tier rules ("sensitive data -> L3") the Tool is tiered L3.

### QD-T L3 full checklist (16 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema` - `name`, `description`, and the input schema (under the OpenAI-convention key `parameters`) are all present. |
| QD-T-1.2 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/required` = `["query"]`, and `query` is defined in `properties`; inner item `required` = `["name","command","args"]` all defined. No inconsistency. |
| QD-T-1.3 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `report_source` enum `["web","local","hybrid"]` and `report_format` enum `["apa","mla","chicago","ieee"]` - no empty, duplicate, or type-inconsistent values. |
| QD-T-1.4 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters` and its `mcp_configs/items` object - both declare `"type":"object"` + `properties` but no `"additionalProperties": false`. Offending text: `"parameters": { "type": "object", "properties": { ... }, "required": ["query"] }` (no `additionalProperties` key on either object). |
| QD-T-2.1 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties/query`. Offending text: `"query": { "type": "string", "description": "The research query to investigate" }` - no `maxLength`/`minLength` (also `name`, `command`, and the `env` values are unbounded strings). |
| QD-T-2.2 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `report_source` / `report_format` are enum-constrained; no string parameter declares a required format that is missing a `pattern`/`format`. |
| QD-T-2.3 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties` - no number-type parameter is present (rule subject absent). |
| QD-T-2.4 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties/mcp_configs`. Offending text: `"mcp_configs": { "type": "array", "description": "List of MCP server configurations", "items": { ... } }` - no `maxItems`/`minItems` (the inner `args` array is likewise unbounded). |
| QD-T-3.1 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema` - the tool performs research/collation (read-oriented); no data-write operation is expressed, so no write-operation notice is required by this rule. |
| QD-T-3.2 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties/mcp_configs/items/properties/command`. Offending text: `"command": { "type": "string", "description": "Command to launch the MCP server" }` - a free-form string passed directly to process launch (likewise `query` is a free-form string passed to the backend). |
| QD-T-3.3 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties/mcp_configs`. Offending text: `"mcp_configs"` is a batch array of server configurations with no quantity limit (`maxItems` absent). |
| QD-T-3.4 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/parameters/properties/mcp_configs/items/properties`. Offending text: `"command": { ... "Command to launch the MCP server" }` and `"env": { ... "Environment variables for the MCP server" }` are exposed as caller-supplied parameters rather than being controlled internally by the system. |
| QD-T-3.5 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema` - a single Tool is defined; no cross-Tool data flow is expressed within this schema. |
| QD-T-4.1 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/description` and parameter descriptions - present and reasonably clear for the declared fields. |
| QD-T-4.2 | FAIL | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema/description`. Offending text: `"description": "MCP tool configuration for researching GitHub repositories alongside web search"` - the description does not declare the side effect of launching an external MCP server process via `command`. |
| QD-T-4.3 | PASS | evidence: `TC-003-mcp-tool-schema.json`, `/tool_schema` - only one Tool is defined; no semantically similar Tool names/descriptions are present. |

Inspect verdict totals for `github_mcp_research`: P0 = 7 (QD-T-1.4, 2.1, 2.4, 3.2, 3.3, 3.4, 4.2); P1 = 0; P2 = 0.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the Tool Schema embeds an example code snippet in `example_usage.python_code`. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `example_usage.python_code` - the Python snippet parses as valid syntax (balanced delimiters, valid `async def`). |
| QC-0.2 | PASS | evidence: `example_usage.python_code` - the language is identified by the enclosing `python_code` field key. |
| QC-0.3 | PASS | evidence: `example_usage.python_code` - imports (`from gpt_researcher import ...`, `import asyncio`, `import os`) are present and the function body is not truncated. |
| QC-1.1 | PASS | evidence: `example_usage.python_code` - `GPTResearcher`, `os`, `asyncio` are all defined via imports. |
| QC-1.2 | PASS | evidence: `example_usage.python_code` - `gpt_researcher` is the declared source-project dependency. |
| QC-1.3 | PASS | evidence: `example_usage.python_code` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `example_usage.python_code` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `example_usage.python_code` - no file handle is opened. |
| QC-2.2 | PASS | evidence: `example_usage.python_code` - network access is library-managed; no explicit connection object is created. |
| QC-2.3 | FAIL (P2) | evidence: `example_usage.python_code`. Offending text: `research_result = await researcher.conduct_research()` - a network operation performed with no `try/except` handling. |
| QC-3.1 | FAIL (P2) | evidence: `example_usage.python_code`. Offending text: `import asyncio` - `asyncio` is imported but never referenced (no `asyncio.` usage in the snippet). |
| QC-3.2 | PASS | evidence: `example_usage.python_code` - every referenced name is imported. |
| QC-3.3 | PASS | evidence: `example_usage.python_code` - the snippet uses `os.getenv("GITHUB_TOKEN")` rather than a hardcoded literal (the artifact's placeholder value is assessed under Stage E, NR-S-9). |

QC verdict totals: P0 = 0; P1 = 0; P2 = 2 (QC-2.3, QC-3.1). These are lite Quality checks only and are not a quality conclusion.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A produced 7 unfixed P0 findings. Per the lite non-blocking note this is recorded as an informational finding and does not gate.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected object is a lone Tool Schema; it contains no responsibility-boundary / duty baseline statement, and no such statement can be located within it. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - `github_mcp_research` has a `name`, a tool `description`, and a `description` on each parameter (`query`, `mcp_configs`, `name`, `command`, `args`, `env`, `report_source`, `report_format`).

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only a single Tool Schema is present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schema (`name` / `description` / inputSchema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. The findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Assessing only explicitly declared content; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> one item.

### Risk item details

- EX classification: **NR-S-9** (Hardcoded Credential / Secret Exposure - placeholder)
- Risk expression (verbatim excerpt): `"GITHUB_TOKEN": "<your_github_token>"` (in `/example_usage/env_config`)
- Impact type labels: D1 (data / secret exposure category)
- Severity grade: **Explicit-P2**
- Trigger condition label: unconditional
- Disposition: Record in risk ledger (Explicit-P2).
- Reason: the value is a placeholder/demo credential, which the NR-S-9 boundary note rates at P2; it is a static-document risk, not a confirmed runtime exploit.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 1.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

For each Stage A FAIL, the candidate directions below are taken from relevance-map.md. The wording is candidate-only ("may", "candidate association", "needs dynamic verification"). Mapping strength is NOT severity and is labeled "provisional (lite)". Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains (SC-* / QC-*) are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: parameter objects declare no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Medium (provisional (lite)) - may have impact under specific parameter/tenant conditions.
- Note: indicates priority for validation; it does not indicate the backend is exploitable.
- Recommended Validation - NOT run: Risk Explicit already scanned (no EX classification attached to this defect); Risk Implicit (dynamic exploitability) NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05 (category-level); RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-2.1 / QD-T-2.4 | Parameter Constraint Missing | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: `query` has no length bound; `mcp_configs`/`args` arrays have no item-count bound.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution).
- Potential Impact: D2 / D3 / Availability.
- Mapping Strength: Medium (provisional (lite)) - may have impact via oversized input.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-3.2 | Raw Input Passthrough | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: free-form `command` string passed to process launch; free-form `query` passed to the backend.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Strong (provisional (lite)) - the free-form string is passed to backend process launch.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-08, FM-09, FM-10; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-3.3 | Batch Operation Unrestricted | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: `mcp_configs` batch array without `maxItems`.
- Candidate Attack Surface: AS-05 (Tool Misuse and High-Risk Side Effects), AS-06 (Resource Exhaustion and Runaway Execution).
- Potential Impact: D2 / Availability.
- Mapping Strength: Medium (provisional (lite)).
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-08, FM-09, FM-10; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-3.4 | Internal Parameter Exposure | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: `command` / `args` / `env` exposed as caller-supplied parameters.
- Candidate Attack Surface: AS-04 (Permission, Identity, and Delegation Expansion).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Strong (provisional (lite)) - process-launch and environment control are exposed to the caller.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-08, FM-09, FM-10; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-4.2 | Undeclared Side Effects | Inspect-P0
- Static Discovery: Artifact tool:`github_mcp_research`; Evidence: external process launch not declared in the description.
- Candidate Attack Surface: AS-05 (Tool Misuse and High-Risk Side Effects), AS-08 (Configuration, Naming, and Supply Chain Confusion).
- Potential Impact: D2 / D3 / Availability.
- Mapping Strength: Medium (provisional (lite)).
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L3 checklist (7 P0, 0 P1, 0 P2) plus embedded-code QC (0 P0, 0 P1, 2 P2).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 1.
Stage F (Impact outlook):   Executed - candidate mapping for each Stage A FAIL.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
