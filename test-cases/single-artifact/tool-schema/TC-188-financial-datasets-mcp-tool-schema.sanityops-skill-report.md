# SanityOps Inspect Lite - Skill Report

Artifact: TC-188-financial-datasets-mcp-tool-schema.md (Tool Schema; Financial Datasets MCP server, five quoted tools)

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## 1. Executive summary

- Stages executed: Stage A (single-artifact QD-T inspection + embedded-code QC baseline), Stage C (Gate-0 verification), Stage E (Risk Explicit audit), Stage F (candidate impact outlook). Stages B and D Not Executed for structural reasons (see status board).
- Inspected tools: the five functions quoted verbatim (get_income_statements, get_current_stock_price, get_historical_stock_prices, get_company_news, get_sec_filings). The case note states the repository also defines six more tools using the same pattern, but those are not quoted in the artifact and therefore are outside the inspected content.
- Finding counts (counted as (tool, rule) FAIL verdicts across the five tools):
  - P0 = 0
  - P1 = 5
  - P2 = 8
- Distinct failed rule IDs: QD-T-1.4, QD-T-2.1, QD-T-2.3.
- Gate result: Gate-0 Not passed - G0-3 unsatisfied (a lone Tool Schema carries no responsibility boundary baseline).
- Risk-Explicit summary: 0 items. Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-T-1.4 - each tool declares an object schema (signature-derived) with no additionalProperties control.
  2. QD-T-2.1 - string parameters (ticker, period, dates, interval, filing_type) carry no minLength/maxLength.
  3. QD-T-2.3 - integer parameters (limit; interval_multiplier) carry no minimum/maximum.
- NOT run by this lite inspector: Risk Implicit (dynamic exploitability) and the runtime Quality subset. The only Quality check executed is the lite QC baseline over embedded code snippets (see Stage A, QC block).
- Upgrade pointer: for the full Inspect ruleset plus Risk (Explicit/Implicit) and Quality subsets, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md

This summary states no security and no quality conclusion.

## 2. Stage A - Tool Schema inspection (QD-T)

### 2.0 Tier determination (per tool, with basis)

| Tool | Tier | Basis |
| --- | --- | --- |
| get_income_statements | L1 | read-only data query; no state change |
| get_current_stock_price | L1 | read-only data query; no state change |
| get_historical_stock_prices | L1 | read-only data query; no state change |
| get_company_news | L1 | read-only data query; no state change |
| get_sec_filings | L1 | read-only data query; no state change |

Tier rule applied: L1 read-only; any write operation -> L2 minimum; irreversible operation -> L3; sensitive data -> L3 (tool-checklist.md "Tool risk tiers").

### 2.1 Tool: get_income_statements (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | TC-188-financial-datasets-mcp-tool-schema.md, tool "get_income_statements": name + docstring description + signature-derived inputSchema present |
| QD-T-1.2 | PASS | ticker required (no default); period/limit declare defaults; consistent with properties |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: signature `get_income_statements(ticker: str, period: str = "annual", limit: int = 4)` |
| QD-T-2.1 | FAIL | string parameters unbounded: `ticker: str` and `period: str = "annual"` (no minLength/maxLength) |
| QD-T-2.3 | FAIL | integer parameter unbounded: `limit: int = 4` (no minimum/maximum) |
| QD-T-4.1 | PASS | docstring and Args: block are clear |

### 2.2 Tool: get_current_stock_price (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + docstring description + inputSchema present |
| QD-T-1.2 | PASS | ticker required; no conflicting required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: `get_current_stock_price(ticker: str)` |
| QD-T-2.1 | FAIL | string parameter unbounded: `ticker: str` (no minLength/maxLength) |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-4.1 | PASS | docstring clear |

### 2.3 Tool: get_historical_stock_prices (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + docstring description + inputSchema present |
| QD-T-1.2 | PASS | ticker/start_date/end_date required; interval/interval_multiplier defaulted; consistent |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: signature with five parameters |
| QD-T-2.1 | FAIL | string parameters unbounded: `start_date: str`, `end_date: str`, `interval: str = "day"` (no minLength/maxLength) |
| QD-T-2.3 | FAIL | integer parameter unbounded: `interval_multiplier: int = 1` (no minimum/maximum) |
| QD-T-4.1 | PASS | docstring and Args: block are clear |

### 2.4 Tool: get_company_news (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + docstring description + inputSchema present |
| QD-T-1.2 | PASS | ticker required; no conflicting required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: `get_company_news(ticker: str)` |
| QD-T-2.1 | FAIL | string parameter unbounded: `ticker: str` (no minLength/maxLength) |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-4.1 | PASS | docstring clear |

### 2.5 Tool: get_sec_filings (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + docstring description + inputSchema present |
| QD-T-1.2 | PASS | ticker required; limit default; filing_type optional (str | None = None); consistent |
| QD-T-1.3 | PASS | no enum declared (filing_type is free text, e.g. 10-K, 10-Q, 8-K) |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: signature with three parameters |
| QD-T-2.1 | FAIL | string parameters unbounded: `ticker: str` and `filing_type: str | None = None` (no minLength/maxLength) |
| QD-T-2.3 | FAIL | integer parameter unbounded: `limit: int = 10` (no minimum/maximum) |
| QD-T-4.1 | PASS | docstring and Args: block are clear |

### 2.6 Stage A summary counts

- P0 (0).
- P1 (5): QD-T-1.4 for each of the five tools.
- P2 (8): QD-T-2.1 for all five tools (5) plus QD-T-2.3 for get_income_statements, get_historical_stock_prices and get_sec_filings (3).

### 2.7 QC - embedded code contract (Stage A Quality sub-check)

- QC-0.1 / QC-0.2 / QC-0.3: Not applicable - no code snippet is embedded in a Tool Schema description, default, or example field. (The quoted `@mcp.tool()` functions and the `make_request` usage are the tool handlers/source, which are outside QC scope; QC inspects embedded snippets only.)
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
| G0-4 (each Tool Schema name/description/parameter descriptions complete) | field-by-field | Satisfied - each tool carries a name, a docstring description, and per-parameter documentation |

Gate-0 result: Not passed - G0-3 unsatisfied (no responsibility baseline; proportionality has no reference). Gate-0 is not an inspection item and produces no score; "not passed" is not FAIL and is not a permission conclusion.

## 5. Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set (only a Tool Schema was supplied; no System Prompt and no Skill).
Wording note: Permission is reported as "Not Executed"; it is never reported as FAIL or "ERROR/BLOCKED".
Mandatory scope statement: this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

## 6. Stage E - Risk Explicit (EX) audit

Physically separated from the Inspect verdicts above. Risk Explicit is a static-text risk scan, not a defect verdict and not a security conclusion.

Audit object: TC-188-financial-datasets-mcp-tool-schema.md (five tools). Scan order: NL-A -> NL-B -> NR-O -> NR-S.

| EX ID | Risk expression (short excerpt) | Impact labels | Grade | Trigger | Disposition |
| --- | --- | --- | --- | --- | --- |
| (none) | no explicitly expressed risk item found | - | - | - | - |

Risk Item Summary: Total = 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

Notes:
- The tools are read-only data queries; descriptions and error branches do not express hidden instructions or capability-enabling flags. No hardcoded credential or PII value appears in the quoted text (NR-S-9 / NR-S-10 not hit).
- Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Physically separated from the stage verdicts. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subset were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md (relevance.md Sec. 1.4), no assumption is made that controls outside the artifacts are absent. This section is single-defect mapping only.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | P1 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-08 (Configuration, Naming, and Supply Chain Confusion)
- Potential Impact: D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted by default; a backend may or may not validate.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

### Impact Card: QD-T-2.1 / QD-T-2.3 | Parameter constraint missing (string length / number bound) | P2 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - missing bounds may allow oversized inputs or large result counts; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

Mandatory statements for every card: Risk Explicit was executed in Stage E (0 items); Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

## 8. Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist run for the five quoted tools; QC baseline applied (no embedded snippets)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-3 unsatisfied (no responsibility boundary baseline in a lone Tool Schema)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 items (Explicit-P0 0, Explicit-P1 0, Explicit-P2 0)
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1/2.3
Stage G (Self-verification): Executed - report-level checks

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
