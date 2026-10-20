# SanityOps Inspect Lite - Skill Report

Artifact: TC-185-memory-mcp-tool-schema.md (Tool Schema; MCP Knowledge-Graph Memory server, nine tools)

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## 1. Executive summary

- Stages executed: Stage A (single-artifact QD-T inspection + embedded-code QC baseline), Stage C (Gate-0 verification), Stage E (Risk Explicit audit), Stage F (candidate impact outlook). Stages B and D Not Executed for structural reasons (see status board).
- Finding counts (counted as (tool, rule) FAIL verdicts across the nine inspected tools):
  - P0 = 13
  - P1 = 9
  - P2 = 0
- Distinct failed rule IDs: QD-T-1.4, QD-T-2.1, QD-T-2.4, QD-T-3.3.
- Gate result: Gate-0 Not passed - G0-3 unsatisfied (a lone Tool Schema carries no responsibility boundary baseline).
- Risk-Explicit summary: 0 items (no explicitly expressed risk found in the schema text). Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-T-1.4 - all nine tools declare object schemas (root parameters object and/or nested EntitySchema/RelationSchema) with no additionalProperties control.
  2. QD-T-2.4 - every batch-array parameter (entities, relations, observations, deletions, entityNames) lacks maxItems/minItems.
  3. QD-T-3.3 - the three delete tools expose unbounded batch arrays with no operation-quantity limit.
  4. QD-T-2.1 - the EntitySchema/RelationSchema string fields and the entityName fields carry no minLength/maxLength.
  5. QD-T-2.3 / QD-T-2.2 - not applicable to this tool group (no number-typed or format-specific parameters were declared).
- NOT run by this lite inspector: Risk Implicit (dynamic exploitability) and the runtime Quality subset. The only Quality check executed is the lite QC baseline over embedded code snippets (see Stage A, QC block).
- Upgrade pointer: for the full Inspect ruleset plus Risk (Explicit/Implicit) and Quality subsets, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md

This summary states no security and no quality conclusion.

## 2. Stage A - Tool Schema inspection (QD-T)

### 2.0 Tier determination (per tool, with basis)

| Tool | Tier | Basis |
| --- | --- | --- |
| create_entities | L2 | creates state (write operation -> L2 minimum) |
| create_relations | L2 | creates state (write operation -> L2 minimum) |
| add_observations | L2 | mutates state (write operation -> L2 minimum) |
| delete_entities | L3 | deletion, irreversible (irreversible operation -> L3) |
| delete_observations | L3 | deletion, irreversible (irreversible operation -> L3) |
| delete_relations | L3 | deletion, irreversible (irreversible operation -> L3) |
| read_graph | L1 | read-only, no state change |
| search_nodes | L1 | read-only, no state change |
| open_nodes | L1 | read-only, no state change |

Tier rule applied: L1 read-only; any write operation -> L2 minimum; irreversible operation -> L3; sensitive data -> L3 (tool-checklist.md "Tool risk tiers"). The tier table is nested (L3 includes L2/L1 items), so each tool is run against its own tier's full checklist.

### 2.1 Tool: read_graph (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | TC-185-memory-mcp-tool-schema.md, tool "read_graph": name + description ("Read the entire knowledge graph") + inputSchema present |
| QD-T-1.2 | PASS | inputSchema.required: no required list; empty parameter object is self-consistent |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: `inputSchema: {}` (arbitrary extra fields accepted) |
| QD-T-2.1 | PASS | no string-typed parameter declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-4.1 | PASS | description "Read the entire knowledge graph" is unambiguous |

### 2.2 Tool: search_nodes (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | tool "search_nodes": name + description + inputSchema present |
| QD-T-1.2 | PASS | inputSchema.properties.query present; no conflicting required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object declares no additionalProperties: `inputSchema: { query: SearchNodesQuerySchema }` |
| QD-T-2.1 | PASS | query is `z.string().max(2048)` -> bounded (SEARCH_QUERY_MAX_LENGTH) |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-4.1 | PASS | description "Search for nodes ... based on a query"; query field described |

### 2.3 Tool: open_nodes (tier L1; L1 checklist, 7 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | tool "open_nodes": name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.names present; no conflicting required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object declares no additionalProperties: `inputSchema: { names: z.array(z.string()) }` |
| QD-T-2.1 | PASS | parameter is array-typed, not string-typed |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-4.1 | PASS | description "Open specific nodes ... by their names"; names field described |

### 2.4 Tool: create_entities (tier L2; L2 checklist, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | tool "create_entities": name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.entities present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object and nested EntitySchema declare no additionalProperties: `inputSchema: { entities: z.array(EntitySchema) }` |
| QD-T-2.1 | FAIL | nested strings unbounded: `name: z.string().describe("The name of the entity")` |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | array unbounded: `entities: z.array(EntitySchema)` (no maxItems/minItems) |
| QD-T-3.1 | PASS | description states the write: "Create multiple new entities in the knowledge graph..." |
| QD-T-3.2 | PASS | structured typed input (EntitySchema); no free-form raw passthrough to a backend |
| QD-T-4.1 | PASS | description and field descriptions are clear |
| QD-T-4.2 | PASS | creation side effect is declared |

### 2.5 Tool: create_relations (tier L2; L2 checklist, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.relations present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object and nested RelationSchema declare no additionalProperties: `relations: z.array(RelationSchema)` |
| QD-T-2.1 | FAIL | nested strings unbounded: `from: z.string().describe("The name of the entity where the relation starts")` |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | array unbounded: `relations: z.array(RelationSchema)` |
| QD-T-3.1 | PASS | description states the write: "Create multiple new relations between entities..." |
| QD-T-3.2 | PASS | structured typed input; no raw passthrough |
| QD-T-4.1 | PASS | descriptions clear |
| QD-T-4.2 | PASS | creation side effect declared |

### 2.6 Tool: add_observations (tier L2; L2 checklist, 12 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.observations present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object and nested observation objects declare no additionalProperties: `observations: z.array(z.object({...}))` |
| QD-T-2.1 | FAIL | nested string unbounded: `entityName: z.string().describe("The name of the entity to add the observations to")` |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | arrays unbounded: `observations: z.array(...)` and `contents: z.array(z.string())` (no maxItems) |
| QD-T-3.1 | PASS | description states the write: "Add new observations to existing entities..." |
| QD-T-3.2 | PASS | structured typed input; no raw passthrough |
| QD-T-4.1 | PASS | descriptions clear |
| QD-T-4.2 | PASS | mutation side effect declared |

### 2.7 Tool: delete_entities (tier L3; L3 checklist, 16 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.entityNames present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | object schema declares no additionalProperties: `inputSchema: { entityNames: z.array(z.string()) }` |
| QD-T-2.1 | PASS | parameter is array-typed, not string-typed |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | array unbounded: `entityNames: z.array(z.string())` (no maxItems) |
| QD-T-3.1 | PASS | description states the destructive write: "Delete multiple entities and their associated relations..." |
| QD-T-3.2 | PASS | structured typed input; no raw passthrough |
| QD-T-3.3 | FAIL | batch delete with no quantity limit: `entityNames: z.array(z.string())` (no maxItems, no limit stated) |
| QD-T-3.4 | PASS | no internally-controlled parameters (tenantId/admin/token) exposed |
| QD-T-3.5 | PASS | no sensitive output-to-input flow identified across tools |
| QD-T-4.1 | PASS | description clear |
| QD-T-4.2 | PASS | deletion side effect (including associated relations) is declared |
| QD-T-4.3 | PASS | name distinct from the other delete tools |

### 2.8 Tool: delete_observations (tier L3; L3 checklist, 16 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.deletions present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object and nested deletion objects declare no additionalProperties: `deletions: z.array(z.object({...}))` |
| QD-T-2.1 | FAIL | nested string unbounded: `entityName: z.string().describe("The name of the entity containing the observations")` |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | arrays unbounded: `deletions: z.array(...)` and `observations: z.array(z.string())` (no maxItems) |
| QD-T-3.1 | PASS | description states the destructive write: "Delete specific observations from entities..." |
| QD-T-3.2 | PASS | structured typed input; no raw passthrough |
| QD-T-3.3 | FAIL | batch delete with no quantity limit: `deletions: z.array(...)` (no maxItems) |
| QD-T-3.4 | PASS | no internally-controlled parameters exposed |
| QD-T-3.5 | PASS | no sensitive output-to-input flow identified |
| QD-T-4.1 | PASS | description clear |
| QD-T-4.2 | PASS | deletion side effect declared |
| QD-T-4.3 | PASS | name distinct from the other delete tools |

### 2.9 Tool: delete_relations (tier L3; L3 checklist, 16 items)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| QD-T-1.1 | PASS | name + description + inputSchema present |
| QD-T-1.2 | PASS | properties.relations present; no contradictory required list |
| QD-T-1.3 | PASS | no enum declared |
| QD-T-1.4 | FAIL | root object and nested RelationSchema declare no additionalProperties: `relations: z.array(RelationSchema)` |
| QD-T-2.1 | PASS | parameter is array-typed, not string-typed |
| QD-T-2.2 | PASS | no format-specific string declared |
| QD-T-2.3 | PASS | no number-typed parameter declared |
| QD-T-2.4 | FAIL | array unbounded: `relations: z.array(RelationSchema)` (no maxItems) |
| QD-T-3.1 | PASS | description states the destructive write: "Delete multiple relations from the knowledge graph" |
| QD-T-3.2 | PASS | structured typed input; no raw passthrough |
| QD-T-3.3 | FAIL | batch delete with no quantity limit: `relations: z.array(RelationSchema)` (no maxItems) |
| QD-T-3.4 | PASS | no internally-controlled parameters exposed |
| QD-T-3.5 | PASS | no sensitive output-to-input flow identified |
| QD-T-4.1 | PASS | description clear |
| QD-T-4.2 | PASS | deletion side effect declared |
| QD-T-4.3 | PASS | name distinct from the other delete tools |

### 2.10 Stage A summary counts

- P0 (13): QD-T-1.4 for the six L2/L3 tools (create_entities, create_relations, add_observations, delete_entities, delete_observations, delete_relations); QD-T-2.1 for delete_observations; QD-T-2.4 for the six L2/L3 tools; QD-T-3.3 for the three delete tools.
- P1 (9): QD-T-1.4 for the three L1 tools (read_graph, search_nodes, open_nodes); QD-T-2.1 and QD-T-2.4 for the three L2 write tools.
- P2 (0).

### 2.11 QC - embedded code contract (Stage A Quality sub-check)

- QC-0.1 Syntax Parsability / QC-0.2 Language Declaration / QC-0.3 Structural Completeness: Not applicable - no code snippet is embedded in any Tool Schema description, default, or example field (the quoted TypeScript/Zod is the schema definition itself, which is outside QC scope).
- QC-1/QC-2/QC-3: Not applicable (QC inspects embedded snippets only).
- QC-0 baseline status: no snippets to validate.

## 3. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission)

| Condition | Verification | Result |
| --- | --- | --- |
| G0-1 (no unfixed P0 in Stage A) | read Stage A | Informational - Stage A has 13 P0 findings; recorded and carried forward; non-blocking in this lite flow |
| G0-2 (no unfixed P0 in Stage B) | read Stage B | Informational - Stage B Not Executed |
| G0-3 (responsibility boundary statements exist and are locatable) | locatability check | Not satisfied - a lone Tool Schema declares no responsibility boundary baseline |
| G0-4 (each Tool Schema name/description/parameter descriptions complete) | field-by-field | Satisfied - all nine tools carry a name, a description, and parameter descriptions |

Gate-0 result: Not passed - G0-3 unsatisfied (no responsibility baseline; proportionality has no reference). Gate-0 is not an inspection item and produces no score; "not passed" is not FAIL and is not a permission conclusion.

## 5. Stage D - Permission proportionality (QD-PM, Quick Mode)

Not Executed - incomplete artifact set (only a Tool Schema was supplied; no System Prompt and no Skill).
Wording note: Permission is reported as "Not Executed"; it is never reported as FAIL or "ERROR/BLOCKED".
Mandatory scope statement: this stage validates declared proportionality within the Logic Artifacts only; it does not inspect IAM/IdP policy configuration, PEP/PDP runtime enforcement, or runtime permission monitoring.

## 6. Stage E - Risk Explicit (EX) audit

Physically separated from the Inspect verdicts above. Risk Explicit is a static-text risk scan, not a defect verdict and not a security conclusion.

Audit object: TC-185-memory-mcp-tool-schema.md (nine tool schemas). Scan order: NL-A -> NL-B -> NR-O -> NR-S.

| EX ID | Risk expression (short excerpt) | Impact labels | Grade | Trigger | Disposition |
| --- | --- | --- | --- | --- | --- |
| (none) | no explicitly expressed risk item found | - | - | - | - |

Risk Item Summary: Total = 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.

Notes:
- Items considered and not classified: the delete tools carry `destructiveHint: true` (an MCP client annotation describing the operation, not a capability-enabling flag -> not NR-S-2); descriptions such as "Delete multiple entities and their associated relations" are explicit statements of the operation's own purpose, not hidden instructions. `read_graph` "Read the entire knowledge graph" is a bounded read statement, not an exfiltration instruction.
- Risk Implicit (dynamic exploitability) was NOT run; an EX finding, if any, would be a static-document risk, never a confirmed exploit.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Physically separated from the stage verdicts. Candidate wording only; mapping strength is not severity. Risk Implicit and the runtime Quality subset were NOT run; the only Quality check executed is the lite QC baseline in Stage A. Per relevance-map.md (relevance.md Sec. 1.4), no assumption is made that controls outside the artifacts are absent. This section is single-defect mapping only; defect chains (SC-*/QC-*) are out of scope.

For each Stage A FAIL:

### Impact Card: QD-T-1.4 | Uncontrolled additionalProperties | P0/P1 (per tier)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-04 (Permission, Identity, and Delegation Expansion)
- Potential Impact: D1, D2, D3
- Mapping Strength: Medium (provisional (lite)) - extra fields may be accepted by default; a backend may or may not validate.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance
- Note: This indicates a validation priority only; it does not indicate the backend is exploitable (relevance.md Sec. 5.5).

### Impact Card: QD-T-2.1 / QD-T-2.3 / QD-T-2.4 | Parameter constraint missing (length/number/array) | P0/P1/P2 (per tier)
- Candidate Attack Surface: AS-02 (Input and Parameter Injection), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, D3, Availability
- Mapping Strength: Medium (provisional (lite)) - missing bounds may allow extreme values; impact depends on backend limits.
- Candidate Failure Modes: FM-03, FM-04, FM-05 (category: Tool structure and parameter defects)
- Candidate RAG-Agent metrics: Correctness, Relevance, Traceability, Format Compliance

### Impact Card: QD-T-3.3 | Batch operation without limit | P0 (L3)
- Candidate Attack Surface: AS-05 (Tool Misuse and High-Risk Side Effects), AS-06 (Resource Exhaustion and Runaway Execution)
- Potential Impact: D2, Availability
- Mapping Strength: Medium (provisional (lite)) - an unbounded batch delete may amplify a mis-selection; recovery depends on backend safeguards.
- Candidate Failure Modes: FM-08, FM-09, FM-10 (category: Tool high-risk operation defects)
- Candidate RAG-Agent metrics: (Tool parameter and semantic defects) Correctness, Relevance, Traceability, Format Compliance

Mandatory statements for every card: Risk Explicit was executed in Stage E (0 items); Risk Implicit was NOT run (dynamic exploitability unverified); the runtime Quality subset was NOT run. External controls (presence/absence) are unknown; no assumption is made that compensating controls outside the artifact are absent.

## 8. Status board

Stage A (Single-artifact):  Executed - QD-T checklists run for all nine tools, tiered L1/L2/L3; QC baseline applied (no embedded snippets)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-3 unsatisfied (no responsibility boundary baseline in a lone Tool Schema)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 items (Explicit-P0 0, Explicit-P1 0, Explicit-P2 0)
Stage F (Impact outlook):   Executed - candidate Impact Cards for QD-T-1.4, QD-T-2.1/2.3/2.4, QD-T-3.3
Stage G (Self-verification): Executed - report-level checks

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
