# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-213-firecrawl-mcp-tool-schema.md`.
- Working version label: `2026-10-14` (the case's Collection Date).
- Classification: **Tool Schema** (MCP tool definition; structural signature `name` + `description` + JSON-Schema `inputSchema` + annotations). The inspected object is the `firecrawl_agent` tool, quoted from the frozen contract snapshot `tests/contract-snapshots/tool-definitions.json` (the machine-generated tool-definition contract the client receives).
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (Gate-0 not satisfied / incomplete artifact set).
- Stage A (QD-T): `firecrawl_agent` - **L2** - Inspect-P0 = 0, Inspect-P1 = 1, Inspect-P2 = 0. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in a lone Tool Schema).
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings:
  1. QD-T-2.4 (P1) - the `urls` array parameter (and the nested `exchange.approve.callIds` array) declare no `maxItems`/`minItems`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

An Inspect PASS is not a security PASS and not a quality PASS. This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determination

Tool `firecrawl_agent` -> **L2 (Medium Risk)**.

Basis: state-changing external operation, recoverable. The tool starts a web-research job that calls external providers ("This call returns only a job ID, not the research result"), spends credits (`maxCredits`), and its annotations declare `readOnlyHint: false` (not read-only). There is no deletion/payment, permission change, or sensitive-data handling declared, and the operation is recoverable, so per the tier rules ("any write operation -> L2 minimum; irreversible -> L3; sensitive data -> L3") the Tool is tiered L2.

### QD-T L2 full checklist (12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md`, `tests/contract-snapshots/tool-definitions.json` - the entry provides `name` (`firecrawl_agent`), a `description`, and an `inputSchema`. |
| QD-T-1.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - `"required": ["prompt"]` and `prompt` is defined in `properties`; no `required` entry references an undefined property. |
| QD-T-1.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the enums (`effort`: low/medium/high; `mode`: extract/chat; `exchange.onTermsRequired`: skip/ask) contain no empty or duplicate value. |
| QD-T-1.4 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the root object declares `"additionalProperties": false`, and the nested objects (`schema`, `exchange`, `exchange.approve`, `exchange.decline`) each declare `"additionalProperties": false`. |
| QD-T-2.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the top-level string parameters are bounded: `prompt` (`minLength: 1`, `maxLength: 10000`), `threadId` (`format: "uuid"` + `pattern`), and the enum-constrained strings (`effort`, `mode`, `exchange.onTermsRequired`); no unbounded top-level string is present. |
| QD-T-2.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - strings requiring a specific format declare it: `urls.items` uses `"format": "uri"`, and `threadId`/`exchange.approve.approvalId`/`exchange.decline.approvalId` use `"format": "uuid"` with a `pattern`. |
| QD-T-2.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the number parameters are bounded: `maxCredits` (`exclusiveMinimum: 0`, `maximum: 9007199254740991`) and `exchange.maxCalls` (`minimum: 1`, `maximum: 30`). |
| QD-T-2.4 | FAIL | evidence: `TC-213-firecrawl-mcp-tool-schema.md`, `inputSchema.properties.urls`. Offending text: `"urls": { "type": "array", "items": { "type": "string", "format": "uri" } }` - no `maxItems`/`minItems` (likewise the nested `exchange.approve.callIds` array declares no `maxItems`; contrast `exchange.toolkits` which does declare `"maxItems": 5`). |
| QD-T-3.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the tool runs a research job and returns data; no data-modification write operation is declared, so the write-not-identified rule does not apply (the `readOnlyHint: false` reflects job creation and provider calls, not a declared data write). |
| QD-T-3.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - `prompt` is the tool's intended natural-language research instruction and the structured `schema` object is a requested output shape; no free-form query/command string is declared as passed to a database/OS interpreter, so no raw command-passthrough is established. |
| QD-T-4.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the tool description is detailed (capability, trigger, sibling-tool disambiguation, async contract, provider-terms workflow) and every non-trivial parameter carries a `description` with defaults/units. |
| QD-T-4.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the declared side effects (async job, credit spend via `maxCredits`, provider-terms approval via `exchange`) are all documented; no undeclared side effect is declared. |

Tool totals: P0 = 0; P1 = 1; P2 = 0.

Note on rule subjects absent at this tier: no `enum`-free case; QD-T-3.2 is judged PASS with the basis above.

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes a JSON tool-definition snapshot. No code is embedded inside schema description/default/example fields; the quoted JSON is inspected as the embedded snippet. QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the quoted JSON parses as valid JSON syntax. |
| QC-0.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the code fence is labeled `json`. |
| QC-0.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the quoted entry is structurally complete (the `firecrawl_agent@f794dfd2e454` object closes). |
| QC-0.4 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the code fence opens and closes correctly. |
| QC-0.5 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - the declared `json` identifier matches the snippet content. |
| QC-1.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no undefined name reference is present in the data snapshot. |
| QC-1.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no import statement is present, so no invalid import is established. |
| QC-1.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no file handle is opened in the quoted snippet. |
| QC-2.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no network connection is opened in the quoted snippet. |
| QC-2.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no high-risk file/network/DB operation is performed in the quoted snippet. |
| QC-3.1 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no import statement is present, so no unused import exists. |
| QC-3.2 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no referenced module is missing an import. |
| QC-3.3 | PASS | evidence: `TC-213-firecrawl-mcp-tool-schema.md` - no hardcoded credential/demo value appears in the quoted snapshot. |

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
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - the tool carries a `name`, a detailed `description`, and per-parameter `description` text.

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

- NR-S-1/2/3: no excessive permission field, no dangerous boolean/enum flag, and no anomalous type/constraint declaration is present (the `exchange`/`approve`/`decline` fields implement a documented approval workflow, not a bypass flag).
- NR-S-5: the long description embeds operational instructions, but they are legitimate provider-terms / approval-workflow guidance ("Never infer acceptance from a data request") rather than an injected instruction steering tool selection; no description-poisoning expression is present.
- NR-S-6/8: no injected default/example value and no conflicting/approximate tool name is declared.
- NR-S-7: no endpoint/callback/webhook/url/server field is declared that points to an unexpected address (the `urls` parameter is a caller-supplied research seed list, not a callback address).
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

Stage F maps only defects that actually FAILED inspection. Stage A produced one FAIL verdict; the candidate mapping follows. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-2.4 | Array Without Length Constraint | Inspect-P1 (L2)

- Static Discovery: artifact tool `firecrawl_agent`; evidence - `urls` (and the nested `exchange.approve.callIds`) declare no `maxItems`/`minItems`.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - an unbounded seed-URL list may enlarge a research request/credit spend; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: candidate association only - this does not indicate that the backend is exploitable; needs dynamic verification.

Mandatory statements for every card: Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L2 checklist (P0 0, P1 1, P2 0); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - Gate-0 not satisfied (G0-3); incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate Impact Card for QD-T-2.4.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
