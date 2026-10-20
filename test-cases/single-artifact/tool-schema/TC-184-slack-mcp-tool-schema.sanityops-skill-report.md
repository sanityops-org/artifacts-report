# SanityOps Inspect Lite - Tool Schema Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Inspection target and input classification

- Artifact under inspection: `TC-184-slack-mcp-tool-schema.md`.
- Working version label: `2026-10-13` (the case's Collection Date).
- Classification: **Tool Schemas** (MCP tool definitions; structural signature `name` + `description` + `inputSchema`). The artifact quotes one tightly-related tool group from a single file, comprising eight tools: `slack_list_channels`, `slack_post_message`, `slack_reply_to_thread`, `slack_add_reaction`, `slack_get_channel_history`, `slack_get_thread_replies`, `slack_get_users`, `slack_get_user_profile`.
- Each tool is given its own tier determination and per-tool verdict set.
- Inspection is Detect-only: nothing in the artifact is rewritten, patched, or regenerated.

---

## Executive summary (SKILL.md section 6.1)

- Executed stages: A (single-artifact QD-T + QC), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Not executed: B (single artifact), D (incomplete artifact set).
- Stage A (QD-T): five read tools are L1, three write tools are L2. Combined Inspect-P0 = 3, Inspect-P1 = 12, Inspect-P2 = 8. Embedded-code QC: P0 = 0, P1 = 0, P2 = 0.
- Gate-0 result: **Not passed** - G0-3 (no responsibility-boundary baseline exists in lone Tool Schemas) is unsatisfiable.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (up to five):
  1. QD-T-1.4 - the three write-tool schemas declare no `additionalProperties` (Inspect-P0); the five read-tool schemas likewise (Inspect-P1).
  2. QD-T-3.1 - the three write-tool descriptions carry no explicit data-modification notice.
  3. QD-T-2.1 - string parameters (`channel_id`, `text`, `thread_ts`, `timestamp`, `reaction`, `cursor`, `user_id`) carry no length bound.
  4. QD-T-2.2 - `thread_ts` documents a specific timestamp format but sets no `pattern`/`format`.
  5. QD-T-2.3 - the `limit` number parameters carry no `minimum`/`maximum`.
- Not run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The only Quality check exercised here is the lite embedded-code QC (Stage A). Per relevance-map.md section 1.4, no assumption is made that controls outside the artifact are absent.
- Upgrade pointer: for a full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

This summary states no security conclusion and no quality conclusion.

---

## Stage A - Single-artifact Tool Schema inspection (QD-T)

### Tier determinations

- `slack_list_channels`, `slack_get_channel_history`, `slack_get_thread_replies`, `slack_get_users`, `slack_get_user_profile` -> **L1 (Low Risk)**. Basis: read-only retrieval (list channels, read history/threads, list users, read a profile); no state change, no irreversible operation, no sensitive-data handling declared by the schema.
- `slack_post_message`, `slack_reply_to_thread`, `slack_add_reaction` -> **L2 (Medium Risk)**. Basis: each creates state (a message / a thread reply / a reaction), i.e. a write operation whose effect is recoverable or overwritable -> per the tier rules ("any write operation -> L2 minimum"), these are L2.

The five L1 tools are run against the L1 minimal set (7 items); the three L2 tools against the L2 minimal set (12 items).

### Tool 1 - `slack_list_channels` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `TC-184-slack-mcp-tool-schema.md` - `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: no `required` array is declared (no required fields), so no inconsistency can arise. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `listChannelsTool.inputSchema`. Offending text: `{ type: "object", properties: { limit: {...}, cursor: {...} } }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.cursor`. Offending text: `"cursor": { "type": "string", "description": "Pagination cursor for next page of results" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | FAIL (P2) | evidence: `properties.limit`. Offending text: `"limit": { "type": "number", "description": "Maximum number of channels to return (default 100, max 200)", "default": 100 }` - the "max 200" is prose only; no `maximum` keyword. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 2 - `slack_get_channel_history` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["channel_id"]`; `channel_id` defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `getChannelHistoryTool.inputSchema`. Offending text: `{ type: "object", properties: {...}, required: ["channel_id"] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.channel_id`. Offending text: `"channel_id": { "type": "string", "description": "The ID of the channel" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | FAIL (P2) | evidence: `properties.limit`. Offending text: `"limit": { "type": "number", "description": "Number of messages to retrieve (default 10)", "default": 10 }` - no `minimum`/`maximum`. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 3 - `slack_get_thread_replies` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["channel_id", "thread_ts"]`; both defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `getThreadRepliesTool.inputSchema`. Offending text: `{ type: "object", properties: {...}, required: [...] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.channel_id` / `properties.thread_ts`. Offending text: `"thread_ts": { "type": "string", "description": "The timestamp of the parent message in the format '1234567890.123456'..." }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: descriptions are clear (including the timestamp-format note). |

### Tool 4 - `slack_get_users` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: no `required` array is declared (no required fields). |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `getUsersTool.inputSchema`. Offending text: `{ type: "object", properties: { cursor: {...}, limit: {...} } }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.cursor`. Offending text: `"cursor": { "type": "string", "description": "Pagination cursor for next page of results" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | FAIL (P2) | evidence: `properties.limit`. Offending text: `"limit": { "type": "number", "description": "Maximum number of users to return (default 100, max 200)", "default": 100 }` - no `maximum` keyword. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 5 - `slack_get_user_profile` (L1)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["user_id"]`; `user_id` defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P1) | evidence: `getUserProfileTool.inputSchema`. Offending text: `{ type: "object", properties: { user_id: {...} }, required: ["user_id"] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P2) | evidence: `properties.user_id`. Offending text: `"user_id": { "type": "string", "description": "The ID of the user" }` - no `maxLength`/`minLength`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |

### Tool 6 - `slack_post_message` (L2, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["channel_id", "text"]`; both defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P0) | evidence: `postMessageTool.inputSchema`. Offending text: `{ type: "object", properties: {...}, required: ["channel_id","text"] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P1) | evidence: `properties.channel_id` / `properties.text`. Offending text: `"text": { "type": "string", "description": "The message text to post" }` - no `maxLength`/`minLength`. |
| QD-T-2.2 | PASS | evidence: `channel_id` is an opaque identifier; no specific format is declared that would require a `pattern`/`format`. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-2.4 | PASS | evidence: no array-type parameter is present. |
| QD-T-3.1 | FAIL (P1) | evidence: `postMessageTool.description`. Offending text: `"description": "Post a new message to a Slack channel"` - the description does not append an explicit statement that the operation will modify/create data. |
| QD-T-3.2 | PASS | evidence: `text` is the tool's intended message content, not a raw passthrough to a query/command backend; no free-form query string is passed to a backend. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |
| QD-T-4.2 | PASS | evidence: no side effect beyond the declared message post is expressed. |

### Tool 7 - `slack_reply_to_thread` (L2, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["channel_id", "thread_ts", "text"]`; all defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P0) | evidence: `replyToThreadTool.inputSchema`. Offending text: `{ type: "object", properties: {...}, required: [...] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P1) | evidence: `properties.channel_id` / `properties.thread_ts` / `properties.text`. Offending text: `"text": { "type": "string", "description": "The reply text" }` - no `maxLength`/`minLength`. |
| QD-T-2.2 | FAIL (P1) | evidence: `properties.thread_ts`. Offending text: `"thread_ts": { "type": "string", "description": "The timestamp of the parent message in the format '1234567890.123456'..." }` - a specific format is documented but no `pattern`/`format` is set. |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-2.4 | PASS | evidence: no array-type parameter is present. |
| QD-T-3.1 | FAIL (P1) | evidence: `replyToThreadTool.description`. Offending text: `"description": "Reply to a specific message thread in Slack"` - no explicit data-modification notice. |
| QD-T-3.2 | PASS | evidence: `text` is the intended reply content; no raw query/command passthrough. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |
| QD-T-4.2 | PASS | evidence: no side effect beyond the declared reply is expressed. |

### Tool 8 - `slack_add_reaction` (L2, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | evidence: `name`, `description`, `inputSchema` present. |
| QD-T-1.2 | PASS | evidence: `required: ["channel_id", "timestamp", "reaction"]`; all defined in `properties`. |
| QD-T-1.3 | PASS | evidence: no `enum` is present. |
| QD-T-1.4 | FAIL (P0) | evidence: `addReactionTool.inputSchema`. Offending text: `{ type: "object", properties: {...}, required: [...] }` - no `additionalProperties`. |
| QD-T-2.1 | FAIL (P1) | evidence: `properties.channel_id` / `properties.timestamp` / `properties.reaction`. Offending text: `"reaction": { "type": "string", "description": "The name of the emoji reaction (without ::)" }` - no `maxLength`/`minLength`. |
| QD-T-2.2 | PASS | evidence: no parameter declares a specific format that is missing a `pattern`/`format` (the reaction note "without ::" is guidance, not a declared format). |
| QD-T-2.3 | PASS | evidence: no number-type parameter is present. |
| QD-T-2.4 | PASS | evidence: no array-type parameter is present. |
| QD-T-3.1 | FAIL (P1) | evidence: `addReactionTool.description`. Offending text: `"description": "Add a reaction emoji to a message"` - no explicit data-modification notice. |
| QD-T-3.2 | PASS | evidence: no raw query/command passthrough to a backend. |
| QD-T-4.1 | PASS | evidence: descriptions are clear. |
| QD-T-4.2 | PASS | evidence: no side effect beyond the declared reaction is expressed. |

### Stage A totals

- P0 = 3 (QD-T-1.4 for `slack_post_message`, `slack_reply_to_thread`, `slack_add_reaction`).
- P1 = 12 (QD-T-1.4 for the five L1 tools = 5; plus QD-T-2.1 / QD-T-2.2 / QD-T-3.1 for the three L2 tools = 7).
- P2 = 8 (QD-T-2.1 / QD-T-2.3 across the five L1 tools).

### QC - embedded-code check (code-contract-checklist.md; QC-0 baseline first)

Scope: the artifact quotes TypeScript tool-definition code (one verbatim excerpt of a single source file). QC-0 baseline is run first and gates QC-1 through QC-3.

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QC-0.1 | PASS | evidence: the quoted TypeScript parses as valid syntax (complete `const ... = { ... }` declarations). |
| QC-0.2 | PASS | evidence: code fences are labeled `typescript`. |
| QC-0.3 | PASS | evidence: the quoted declarations are syntactically complete and untruncated. Note: the excerpt starts at `// Tool definitions` and the enclosing module's imports (`Tool`, `McpServer`, `ListToolsRequestSchema`) are outside the quoted range; the code is an excerpt, not a standalone file. |
| QC-1.1 | PASS | evidence: in the authored module the referenced names (`Tool`, `Server`/`McpServer`, `ListToolsRequestSchema`) are imported; within the excerpt they are type/import references, not undefined locals. |
| QC-1.2 | PASS | evidence: no non-standard import is introduced by the quoted code. |
| QC-1.3 | PASS | evidence: no deprecated API usage is evident. |
| QC-1.4 | PASS | evidence: no argument type incompatibility is evident. |
| QC-2.1 | PASS | evidence: no file handle is opened. |
| QC-2.2 | PASS | evidence: no network connection is opened in the quoted snippets. |
| QC-2.3 | PASS | evidence: no high-risk file/network/DB operation is performed in the quoted snippets. |
| QC-3.1 | PASS | evidence: no unused import appears in the quoted code. |
| QC-3.2 | PASS | evidence: no referenced module is missing an import in the authored module. |
| QC-3.3 | PASS | evidence: no hardcoded credential/demo value appears in the quoted code. |

QC totals: P0 = 0; P1 = 0; P2 = 0.

---

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

---

## Stage C - Gate-0 (admission to Permission)

Verification of the four admission conditions (permission-checklist.md section 3.2):

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A produced 3 unfixed P0 findings. Per the lite non-blocking note this is recorded as an informational finding and does not gate.
- G0-2 (cross-artifact inspection has no unfixed P0): not applicable / informational - Stage B was Not Executed (single artifact).
- G0-3 (responsibility boundary statements exist and are locatable): **FAIL** - the inspected objects are lone Tool Schemas; no responsibility-boundary / duty baseline statement exists within them. The condition is structurally unsatisfiable for a single Tool Schema.
- G0-4 (each Tool Schema's `name`, `description`, and parameter descriptions are complete): PASS - each of the eight tools has a `name`, a tool `description`, and a description on every declared parameter.

Gate-0 result: **Not passed - G0-3** (no responsibility baseline is present in a lone Tool Schema; proportionality has no reference).

---

## Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set. The full artifact set (System Prompt + Skill + all Tool Schemas) is not available; only Tool Schemas are present.

(Per the wording red line, the Permission stage is reported as "Not Executed"; it is not reported as FAIL, and it is not reported as "Permission = ERROR/BLOCKED".)

---

## Stage E - Risk Explicit audit (EX: NL-A / NL-B / NR-O / NR-S)

This stage scans the Tool Schemas (`name` / `description` / inputSchema) for risk that is **explicitly expressed** in static text, without running the Agent. It is detect + classify + grade, not a PASS/FAIL inspection. Findings below are a static-document risk scan and are physically separated from the Stage A inspect verdicts. Only explicitly declared content is assessed; Risk Implicit (dynamic exploitability) was NOT run.

Scan summary: NL-A (continuous) -> none found; NL-B (non-continuous) -> none found (single artifact); NR-O (obfuscated) -> none found; NR-S (structured configuration) -> none found.

- NR-S-1/2/3: no excessive permission fields, no dangerous boolean/enum flags, no anomalous type constraints are declared.
- NR-S-5/6/8: no instruction poisoning in descriptions, no injected default/example values, no name-conflict/homoglyph issues (all names carry a distinct `slack_` prefix).
- NR-S-7: no endpoint/callback/webhook/url/server field is declared.
- NR-S-9/10: no hardcoded literal secret or PII value is declared.

Risk-Explicit totals: Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

---

## Stage F - Impact outlook (candidate mapping, advisory only)

For each Stage A FAIL, the candidate directions below are taken from relevance-map.md. The wording is candidate-only ("may", "candidate association", "needs dynamic verification"). Mapping strength is NOT severity and is labeled "provisional (lite)". Risk Implicit and the runtime Quality subsets were NOT run; per relevance-map.md section 1.4 no assumption is made that controls outside the artifact are absent. This section is advisory context, physically separated from the stage verdicts. v1 scope: single-defect mapping only; defect chains are out of scope.

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | Inspect-P0/P1 (all eight tools)
- Static Discovery: Artifacts tool:`slack_post_message`, tool:`slack_reply_to_thread`, tool:`slack_add_reaction` (P0) and the five read tools (P1); Evidence: root schema objects declare no `additionalProperties` control.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion).
- Potential Impact: D1 / D2 / D3.
- Mapping Strength: Medium (provisional (lite)) - may have impact under specific parameter/tenant conditions.
- Note: indicates priority for validation; it does not indicate the backend is exploitable.
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-2.1 / QD-T-2.2 / QD-T-2.3 | Parameter Constraint Missing | Inspect-P1/P2
- Static Discovery: Artifacts the eight Slack tools; Evidence: the named string parameters carry no length bound, `thread_ts` carries a documented format but no `pattern`/`format`, and `limit` carries no numeric bound.
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution).
- Potential Impact: D2 / D3 / Availability.
- Mapping Strength: Medium (provisional (lite)).
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-03, FM-04, FM-05; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

### Impact Card: QD-T-3.1 | Write Operation Not Identified | Inspect-P1
- Static Discovery: Artifacts tool:`slack_post_message`, tool:`slack_reply_to_thread`, tool:`slack_add_reaction`; Evidence: descriptions do not declare the data-modification effect.
- Candidate Attack Surface: AS-05 (Tool Misuse and High-Risk Side Effects).
- Potential Impact: D2.
- Mapping Strength: Medium (provisional (lite)).
- Recommended Validation - NOT run: Risk Implicit NOT run; external controls unknown.
- Potential Quality Associations: Tool-Agent FM-08, FM-09, FM-10; RAG-Agent candidate metrics: Correctness, Relevance, Traceability, Format Compliance.

---

## Status board

Stage A (Single-artifact):  Executed - QD-T L1 checklist for five read tools and L2 checklist for three write tools (combined P0 3, P1 12, P2 8); embedded-code QC clean.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-3.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - Explicit-P0 0, Explicit-P1 0, Explicit-P2 0.
Stage F (Impact outlook):   Executed - candidate mapping for each Stage A FAIL.
Stage G (Self-verification): Executed - report self-check completed.

Self-verification: ID back-closure OK (all emitted QD-T / QC / EX / AS / FM IDs exist in references/) - red-line wording OK (no causal language, no security/quality conclusion, Permission stage written as "Not Executed") - output contract OK (header provenance facts present, executive summary present, seven-line status board present, report in English with zero CJK characters). No in-place self-corrections were required.
