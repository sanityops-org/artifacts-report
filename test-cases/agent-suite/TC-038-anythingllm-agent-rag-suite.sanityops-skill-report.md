# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (incomplete artifact set).
- Finding counts (Stage A + B): Inspect P0 = 36, P1 = 14, P2 = 0.
- Gate-0 result: Passed (G0-3 passed; G0-4 passed for the shown rag-memory Tool Schema). Stage D still did not run because the artifact set is incomplete (Tool Schemas for docSummarizer/webScraping/webBrowsing are not provided).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-ST-3.6 / QD-PS-1.3 - The rag-memory Skill stores to memory while the Prompt authorizes no permission scope.
  2. QD-P-2.5.2 / QD-P-2.3.4 - The Prompt declares no security boundaries and no privacy filtering.
  3. QD-T-1.2 - The rag-memory Tool Schema omits `required` (action/content not marked required).
  4. QD-T-3.2 - The `content` parameter passes free-form text to search/store (raw passthrough).
  5. QD-PT-2.1 - The Prompt references the `request-user-input` tool, absent from the provided Tool Schema list.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-038 is a single workspace agent (AnythingLLM @agent). All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present, partial): the WORKSPACE_AGENT role text and the clarifying-questions note. Basis: prose/instruction strings.
- Skill (present, informal): the rag-memory skill definition (name/description/setup/handler). Basis: skill definition object (JS, not markdown front matter).
- Tool Schema (present, partial): the rag-memory function `parameters` (JSON Schema draft-07, properties action/content, enum, additionalProperties false). Basis: function-calling definition with `parameters`.
- Out of coverage: docSummarizer/webScraping/webBrowsing, plugin/flow plugins and MCP servers are named but no schemas are shown.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (WORKSPACE_AGENT role)

Tier determination: **L3 Complex Agent**. Basis: 4+ tool invocations (memory, document-summarizer, web-scraping, web-browsing, MCP), multi-step RAG workflow, security-sensitive (document ingestion). Scope = L3 (47 items).

- QD-P-1.1.1 | PASS | evidence: TC-038, the role text and the appended note are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-038, no conflicting directives.
- QD-P-1.1.3 | PASS | evidence: TC-038, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-038, the "human monitor" role matches its directives.
- QD-P-1.2.2 | PASS | evidence: TC-038, no style rule mismatch.
- QD-P-1.2.3 | PASS | evidence: TC-038, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-038, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-038, no vague qualifier carries a critical decision.
- QD-P-1.3.3 | FAIL | evidence: TC-038, no authorization/prohibition scope or handoff condition is declared.
- QD-P-1.4.1 | PASS | evidence: TC-038, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-038, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-038, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-038, the declared behaviour supports the RAG-agent objective.
- QD-P-1.5.2 | FAIL | evidence: TC-038, the note references `request-user-input` but the Prompt defines no resource set.
- QD-P-1.6.1 | PASS | evidence: TC-038, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-038, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-038, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-038, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-038, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-038, no unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-038, no rule requires revising earlier conclusions on new information.
- QD-P-2.1.1 | PASS | evidence: TC-038, prompt formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-038, the `request-user-input` reference is specific.
- QD-P-2.1.3 | PASS | evidence: TC-038, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-038, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-038, no input source (user / system / external data) is declared.
- QD-P-2.2.2 | PASS | evidence: TC-038, input is conversational (no structured parser defined).
- QD-P-2.2.3 | PASS | evidence: TC-038, no parameterized input declared (not triggered).
- QD-P-2.2.4 | PASS | evidence: TC-038, missing-input handling is declared ("When you need information from the user ... you MUST use the request-user-input tool").
- QD-P-2.3.1 | FAIL | evidence: TC-038, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-038, no output schema/fields are declared.
- QD-P-2.3.3 | FAIL | evidence: TC-038, no output stability assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-038, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | FAIL | evidence: TC-038, no workflow step sequence is defined.
- QD-P-2.4.2 | FAIL | evidence: TC-038, the tool set is injected dynamically and is not declared in the Prompt.
- QD-P-2.4.3 | FAIL | evidence: TC-038, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | FAIL | evidence: TC-038, no loop/recursion termination condition is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-038, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-038, no permission scope is declared for the memory/browsing tools.
- QD-P-2.5.4 | PASS | evidence: TC-038, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | FAIL | evidence: TC-038, no resource invocation frequency limits are declared.
- QD-P-2.6.1 | FAIL | evidence: TC-038, no runtime exception handling is declared.
- QD-P-2.6.2 | FAIL | evidence: TC-038, no degradation/recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-038, no unreasonable retry mechanism found.
- QD-P-2.7.1 | FAIL | evidence: TC-038, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-038, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-038, no boundary-case examples are provided.

### 3.A.2 Skill - rag-memory

Skill risk-level determination: rag-memory = **L2** (resource access - reads/writes the vector database, may involve sensitive documents).

QD-S-0 baseline: QD-S-0.1 PASS (`name`/`description` present); QD-S-0.2 PASS (non-empty); QD-S-0.3 PASS (the definition parses); QD-S-0.4 PASS (types valid); QD-S-0.5 PASS (no conflicting declarations); QD-S-0.6 PASS (minimum structure present). Baseline passes; proceed. Scope = L2 (6 mandatory + 14 recommended).

- QD-S-1.1 | FAIL | evidence: TC-038, rag-memory skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-038, rag-memory skill calls search/store with no retry/timeout/tool-call bound.
- QD-S-2.1 | PASS | evidence: TC-038, rag-memory skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-038, rag-memory skill uses no "until success" wording.
- QD-S-3.4 | PASS | evidence: TC-038, rag-memory description scopes store ("Use store only when explicitly asked to remember or save something").
- QD-S-4.1 | PASS | evidence: TC-038, the handler declares a failure branch (`catch (error) { console.log(error); }`).
- QD-S-1.2 | FAIL | evidence: TC-038, rag-memory skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-038, rag-memory skill searches/stores without a read/write/delete distinction.
- QD-S-1.5 | PASS | evidence: TC-038, rag-memory skill declares its data source (local documents/vector database).
- QD-S-2.3 | PASS | evidence: TC-038, rag-memory skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-038, rag-memory verbs are specific (search/store).
- QD-S-3.1 | PASS | evidence: TC-038, rag-memory trigger is specific.
- QD-S-3.2 | PASS | evidence: TC-038, rag-memory declares deactivation ("Use store only when explicitly asked").
- QD-S-3.3 | FAIL | evidence: TC-038, rag-memory skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-038, rag-memory name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-038, rag-memory skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-038, rag-memory skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-038, rag-memory skill performs writes without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-038, rag-memory skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-038, rag-memory skill calls internal search/store without declaring permitted downstream scope.

### 3.A.3 Tool Schema - rag-memory function

Tier: **L2** (search is read-only; store is a recoverable write to the vector database). Scope = L2 (12 items).

- QD-T-1.1 | PASS | evidence: TC-038, the function declares `name`, `description` and `parameters` (JSON Schema).
- QD-T-1.2 | FAIL | evidence: TC-038, `action`/`content` are defined in `properties` but not listed in a `required` array (no `required` is declared).
- QD-T-1.3 | PASS | evidence: TC-038, `enum: ["search", "store"]` has no duplicate/empty values.
- QD-T-1.4 | PASS | evidence: TC-038, `additionalProperties: false` is declared.
- QD-T-2.1 | FAIL | evidence: TC-038, the `content` string parameter has no `maxLength`/`minLength`.
- QD-T-2.2 | N/A | evidence: TC-038, no format-specific string parameter is declared (determination basis: no such field).
- QD-T-2.3 | N/A | evidence: TC-038, no number-type parameter is declared (determination basis: no such field).
- QD-T-2.4 | N/A | evidence: TC-038, no array-type parameter is declared (determination basis: no such field).
- QD-T-3.1 | FAIL | evidence: TC-038, the tool stores to memory but the description carries no explicit write-operation notice.
- QD-T-3.2 | FAIL | evidence: TC-038, the `content` parameter takes free-form plain text passed to search/store.
- QD-T-4.1 | PASS | evidence: TC-038, the description "Search your local documents ... or store information to long-term memory" is specific.
- QD-T-4.2 | FAIL | evidence: TC-038, the persistence side effect of the store action is not declared.

### 3.A.4 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-038, the `javascript` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-038, snippets are fenced with `javascript`.
- QC-0.3 | FAIL | evidence: TC-038, the memory handler is truncated at `} catch (error) { console.log(error);`.
- QC-1.1 | FAIL | evidence: TC-038, `Deduplicator`, `aibitat`, `AgentPlugins` are undefined in the snippets.
- QC-1.2 | PASS | evidence: TC-038, no unavailable-module import statement present.
- QC-1.3 | PASS | evidence: TC-038, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-038, no type-mismatched call present.
- QC-2.1 | N/A | evidence: TC-038, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-038, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-038, no high-risk file/network/DB call in the shown snippets (determination basis: the handler has try/catch).
- QC-3.1 | PASS | evidence: TC-038, no unused import present.
- QC-3.2 | FAIL | evidence: TC-038, `require(...)`-style modules (`Deduplicator`, `AgentPlugins`) are referenced but never imported/defined.
- QC-3.3 | PASS | evidence: TC-038, no hardcoded demo credential value present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: all three same-agent artifact types are present (System Prompt + Skill + Tool Schema). Tier = **L3** (Appendix C upgrades applied: Agent L3 -> global P1->P0, P2->P1).

### QD-PS (Prompt -> Skill)

- QD-PS-1.1 Skill Authorization Consistency | PASS | evidence: Prompt (TC-038, WORKSPACE_AGENT) does not restrict the skill set; the rag-memory skill is a default-enabled skill.
- QD-PS-1.2 Trigger Condition Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-038) declares no skill triggers; Skill (rag-memory) defines search/store triggers - inconsistent.
- QD-PS-1.3 Permission Boundary Consistency | FAIL (P0) | evidence: Prompt (TC-038, role text) authorizes no explicit scope; Skill (rag-memory "store information to long-term memory") exceeds it.
- QD-PS-1.4 Resource Access Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-038) declares no allowed resources; Skill (rag-memory) declares local-document/vector access.
- QD-PS-1.5 Failure Handling Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-038) defines no failure handling; Skill (rag-memory) declares only a bare catch - inconsistent.
- QD-PS-1.6 Output Constraint Consistency | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt (TC-038) declares no output constraints; Skill declares none either.

### QD-PT (Prompt -> Tool)

- QD-PT-2.1 Tool Existence | FAIL (P0) | evidence: Prompt (TC-038, "use the request-user-input tool") references a tool absent from the provided Tool Schema list (rag-memory).
- QD-PT-2.2 Invocation Specification Consistency | FAIL (P0) | evidence: Prompt (TC-038) names tools without parameters; Tool Schema (rag-memory `action`/`content`) defines typed fields - inconsistent.
- QD-PT-2.3 Parameter Constraint Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-038) declares no parameter constraints; Tool Schema constrains `action` to an enum.
- QD-PT-2.4 Permission Granularity Consistency | N/A | evidence: no RS-3 (high-risk) Tool among the provided Tool Schema (determination basis: rag-memory is L2).
- QD-PT-2.5 Error Handling Completeness | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-038) covers no tool error types; Tool Schema declares none.
- QD-PT-2.6 Invocation Frequency Reasonableness | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt declares no frequency limits; Tool Schema declares none.

### QD-ST (Skill <-> Tool)

- QD-ST-3.1 Tool Existence | PASS | evidence: Skill (TC-038, rag-memory) declares the memory tool, which matches the Tool Schema `name: rag-memory`.
- QD-ST-3.2 Input Constraint Consistency | FAIL (P0) | evidence: Skill (TC-038, rag-memory) declares no input constraint matched by the Tool Schema (`action` enum, `content` string).
- QD-ST-3.3 Required Parameter Preparation | FAIL (P0) | evidence: Tool Schema requires `action`/`content`; Skill (rag-memory) declares no source for them.
- QD-ST-3.4 Invocation Frequency Match | FAIL (P1, upgraded from P2 by L3) | evidence: Skill (rag-memory) declares no max call count; Tool Schema declares none.
- QD-ST-3.5 Output Structure Match | FAIL (P0, upgraded from P1 by L3) | evidence: Skill (rag-memory) declares no output structure matched by a Tool return value.
- QD-ST-3.6 Permission Scope Match | FAIL (P0) | evidence: Skill (rag-memory store side effect) exceeds the Skill's permission declarations (absent).
- QD-ST-3.7 Error Handling Coverage | FAIL (P0, upgraded from P1 by L3) | evidence: Skill (rag-memory) FAILURE dimension is undeclared, so tool error types are not covered.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Skill/Tool invocation relationships (TC-038) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: the Prompt defines one agent role (TC-038); no orchestration cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the WORKSPACE_AGENT role text and the rag-memory description are locatable.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): Passed - the shown rag-memory Tool Schema declares `name`, `description`, and per-parameter descriptions.

Gate-0 result: **Passed** (G0-1/G0-2 carried forward as informational).

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Reason: incomplete artifact set - the Permission stage requires System Prompt + Skill + all Tool Schemas; Tool Schemas for docSummarizer/webScraping/webBrowsing are not provided.

(This is not a FAIL and not a permission conclusion. Gate-0 passed; the stage did not run only because the tool set is incomplete.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-038 System Prompt set + Skill + Tool Schema.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed risk text (NL-A / NL-B / NR-O / NR-S) was found in the shown artifacts. The `additionalProperties: false` declaration and the single-user-only gating are protective, not risk expressions.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.3, QD-P-1.5.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.1 | AS-01, AS-02 | FM-01, FM-04 | Medium |
| QD-P-2.3.1, QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4, QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.4.1, QD-P-2.4.2, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-P-2.5.1, QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 (rag-memory) | AS-06 | Availability | Medium |
| QD-S-1.4, QD-S-5.1 (rag-memory) | AS-04, AS-05 | FM-05, FM-09 | Strong (write without scope distinction) |
| QD-S-3.3, QD-S-4.2, QD-S-4.3, QD-S-5.3, QD-S-5.4 (rag-memory) | AS-01, AS-04, AS-05, AS-07 | FM-02, FM-07, FM-09 | Medium |
| QD-T-1.2, QD-T-3.1, QD-T-3.2, QD-T-4.2 | AS-02, AS-05 | FM-08, FM-09, FM-10 | Strong |
| QD-T-2.1 | AS-02, AS-06 | FM-03, FM-04, FM-05 | Medium |
| QC-0.3, QC-1.1, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QD-PS-1.2, QD-PS-1.3, QD-PS-1.4, QD-PS-1.5, QD-PS-1.6 | AS-03, AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |
| QD-PT-2.1, QD-PT-2.2, QD-PT-2.3, QD-PT-2.5, QD-PT-2.6 | AS-02, AS-05, AS-06, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong |
| QD-ST-3.2, QD-ST-3.3, QD-ST-3.5, QD-ST-3.6, QD-ST-3.7, QD-ST-3.4 | AS-02, AS-04, AS-05, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Traceability, Safety Response, Boundary Recognition. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3), QD-S (rag-memory L2), QD-T (rag-memory L2), QC.
Stage B (Cross):            Executed - all three same-agent artifact types present.
Stage C (Gate-0):           Passed.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (Tool Schemas for other default skills not provided).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
