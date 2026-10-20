# SanityOps Inspect Lite - Skill Report

Artifact: TC-194-airbnb-mcp-tool-schema.md (Tool Schema; openbnb-org/mcp-server-airbnb, tool `airbnb_search`)

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## 1. Executive summary

- Stages executed: Stage A (single-artifact QD-T inspection + embedded-code QC baseline), Stage C (Gate-0 verification), Stage E (Risk Explicit audit), Stage F (candidate impact outlook). Stages B and D Not Executed for structural reasons (see status board).
- Inspected tool: `airbnb_search` (the case's one logical artifact). Sibling `airbnb_listing_details` is mentioned but not quoted, so it is outside the inspected content.
- Finding counts (counted as (tool, rule) FAIL verdicts):
  - P0 = 0
  - P1 = 1
  - P2 = 2
- Distinct failed rule IDs: QD-T-1.4, QD-T-2.1, QD-T-2.3.
- Gate result: Gate-0 Not passed - G0-3 unsatisfied (a lone Tool Schema carries no responsibility boundary baseline).
- Risk-Explicit summary: 1 item - Explicit-P0 = 0, Explicit-P1 = 1, Explicit-P2 = 0 (see Stage E).
- Top findings (rule ID - one-line defect):
  1. QD-T-1.4 - the raw object inputSchema declares no additionalProperties control.
  2. QD-T-2.3 - the number parameters (adults, children, infants, pets, minPrice, maxPrice) carry no minimum/maximum.
  3. QD-T-2.1 - the string parameters (location, placeId, checkin, checkout, cursor) carry no minLength/maxLength.
- NOT run by this lite inspector: Risk Implicit (dynamic exploitability) and the runtime Quality subset. The only Quality check executed is the lite QC baseline over embedded code snippets (see Stage A, QC block).
- Upgrade pointer: for the full Inspect ruleset plus Risk (Explicit/Implicit) and Quality subsets, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md

This summary states no security and no quality conclusion.

## 2. Stage A - Tool Schema inspection (QD-T)

### 2.0 Tier determination

| Tool | Tier | Basis |
| --- | --- | --- |
| airbnb_search | L1 | read-only listing search; no state change |

Tier rule applied: L1 read-only; any write operation -> L2 minimum; irreversible operation -> L3; sensitive data -> L3 (tool-checklist.md "Tool risk tiers").

### 2.1 Tool: airbnb_search (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | TC-194-airbnb-mcp-tool-schema.md, tool "airbnb_search": name + description ("Search for Airbnb listings with various filters and pagination. Provide direct links to the user") + inputSchema present |
| QD-T-1.2 | PASS | inputSchema.required = ["location"] is present in inputSchema.properties; consistent |
| QD-T-1.3 | PASS | propertyType enum has four unique valid values (entire_home, private_room, shared_room, hotel_room) |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: `inputSchema: {type: "object", properties: {...}, required: ["location"]}` |
| QD-T-2.1 | FAIL | string parameters unbounded: `checkin: {type: "string", description: "Check-in date (YYYY-MM-DD)"}` (and location/placeId/checkout/cursor; no minLength/maxLength) |
| QD-T-2.3 | FAIL | number parameters unbounded: `adults: {type: "number", description: "Number of adults"}` (and children/infants/pets/minPrice/maxPrice; no minimum/maximum) |
| QD-T-4.1 | PASS | tool/parameter descriptions are clear; placeId documents its override of location |

### 2.2 Stage A summary counts

- P0 (0).
- P1 (1): QD-T-1.4.
- P2 (2): QD-T-2.1, QD-T-2.3.

### 2.3 QC - embedded code contract (Stage A Quality sub-check)

- QC-0.1 / QC-0.2 / QC-0.3: Not applicable - no code snippet is embedded in a Tool Schema description, default, or example field. (The quoted `Tool` object and `Server` setup are the schema/source, outside QC scope.)
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
| G0-4 (each Tool Schema name/description/parameter descriptions complete) | field-by-field | Satisfied - the tool carries a name, a description, and per-parameter descriptions |

Gate-0 result: Not passed - G0-3 unsatisfied (no responsibility baseline; proportionality has no reference). Gate-0 is not an inspection item and produces no score; "not passed" is not FAIL and is not a permission conclusion.

## 5. Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set (only a Tool Schema was supplied; no System Prompt and no Skill).
Wording note: Permission is reported as "Not Executed"; it is never reported as FAIL or "ERROR/BLOCKED".
Mandatory scope statement: this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

## 6. Stage E - Risk Explicit (EX) audit

Physically separated from the Inspect verdicts above. Risk Explicit is a static-text risk scan, not a defect verdict and not a security conclusion.

Audit object: TC-194-airbnb-mcp-tool-schema.md (airbnb_search). Scan order: NL-A -> NL-B -> NR-O -> NR-S.

| EX ID | Risk expression (short excerpt) | Impact labels | Grade | Trigger | Disposition |
| --- | --- | --- | --- | --- | --- |
| NR-S-2 | `"ignoreRobotsText": {"type": "boolean", "description": "Ignore robots.txt rules for this request"}` | D3 | Explicit-P1 | unconditional | Fix before release, or approved exemption |

Risk Item Summary: Total = 1; Explicit-P0 = 0; Explicit-P1 = 1; Explicit-P2 = 0.

Detail of the item:
- EX Classification: NR-S-2 (Dangerous Capability Flag Explicitly Enabled)
- Risk Expression: a boolean field `ignoreRobotsText` whose description is "Ignore robots.txt rules for this request" (a declared flag that turns off a site's robots.txt control).
- Reason (worst consequence): the flag explicitly disables an external access-policy control; the worst consequence is a policy/compliance breach for the request, not data modification (the tool is read-only). Graded Explicit-P1 (limited restriction crossing with recoverable consequence). Not P0: no data leakage, no irreversible consequence, and robots.txt is not a server-enforced security boundary.
- Impact Type Labels: D3 (a declared restriction is crossed).
- Trigger Condition Label: unconditional - the model or user can set the flag on their own (the condition is not system-enforced and does not require server-side verification).
- Disposition: Fix before release, or approved exemption. Documentation-context note: the TC states the server respects robots.txt by default, so this is the opt-out surface.
- Remediation Suggestion (advisory): remove the field from the model-visible surface, or gate it behind an explicit out-of-band operator configuration rather than a model-settable parameter.

Items considered and not classified: `placeId` ("overrides the location parameter") is an override of a sibling parameter, not a control bypass; the tool description "Provide direct links to the user" is an output-behavior instruction, not a risk expression.

Risk Implicit (dynamic exploitability) was NOT run; this EX item is a static-document risk, never a confirmed exploit.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Physically separated from the stage verdicts. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subset were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md (relevance.md Sec. 1.4), no assumption is made that controls outside the artifacts are absent. This section is single-defect mapping only. (Note: the EX item in Stage E is a Risk-Explicit finding, not a QD FAIL, and is not mapped here; Stage F maps Stage A FAILs only.)

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | P1 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-08 (Configuration, Naming, and Supply Chain Confusion)
- Potential Impact: D2, D3
- Mapping Strength: Conditional (provisional (lite)) - extra fields may be accepted; impact depends on how the search backend treats unexpected arguments.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

### Impact Card: QD-T-2.1 / QD-T-2.3 | Parameter constraint missing (string length / number bound) | P2 (L1)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Conditional (provisional (lite)) - unbounded guest counts or price bounds may be passed through inconsistently; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

Mandatory statements for every card: Risk Explicit was executed in Stage E (1 item); Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

## 8. Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist run for airbnb_search; QC baseline applied (no embedded snippets)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-3 unsatisfied (no responsibility boundary baseline in a lone Tool Schema)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 1 item (Explicit-P0 0, Explicit-P1 1, Explicit-P2 0; NR-S-2)
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4 and QD-T-2.1/2.3
Stage G (Self-verification): Executed - report-level checks

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
