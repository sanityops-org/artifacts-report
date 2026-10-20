# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-175-commercial-legal-pl-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

Note on evidence language: the inspected artifact is written in Polish. Per the report-language rule, its evidence excerpts below are rendered in English (marked "translation"), not quoted verbatim.

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 2, P1 = 6, P2 = 0 (QD-S: P0 2 / P1 5 / P2 0; embedded-code QC: 1 finding, QC-0.2 P1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 1, Explicit-P2 = 0 (1 qualifying explicitly declared risk item).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper limit on the number or size of inputs (an arbitrarily long contract may be pasted in).
  2. QD-S-1.3 - the Skill calls an external MCP tool and opens workflow files but declares no retry count, tool-invocation count or execution timeout.
  3. QD-S-1.2 - no upper limit on output size for generated documents.
  4. QD-S-1.4 / QD-S-5.1 - no read/write/delete permission-type distinction for the document reads, the MCP call and the generated files.
  5. QC-0.2 - several fenced blocks carry no language identifier.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed; QC-1.x-QC-4.x did not run because the QC-0 gate did not pass).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-175-commercial-legal-pl-skill.md, front matter (lines 14-16): `name: commercial-legal-pl` and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 14-16) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (role detection / firm config / core rules / workflow selection / architecture / MCP tool / format / limits / gates / disclaimers) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill performs resource access - it reads a firm profile file (translation: "If a file `practice-profile.md` exists in the root directory - read it before the first action"), reads a large bundled reference/workflow tree, calls an external MCP tool (`legal-cite` via `uvx`), and generates documents. These are recoverable resource operations; no deletion, irreversible action, or permission change is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence (translation of the disclaimer): "The skill does not replace legal advice. It is an operational tool supporting the work of a qualified lawyer - legal counsel, attorney or tax adviser, as appropriate to the scope of the specific engagement." and "The results of the skill's work require individual verification by a lawyer before use in a specific case." This declares what the Skill does NOT do (it is not a substitute for advice and defers to a qualified lawyer).
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration for the profile/reference reads, the `legal-cite` MCP call, and the generated documents.
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence (translation): sources are the firm profile (`practice-profile.md`), the bundled clause/knowledge base, the user's pasted document, and the `legal-cite` MCP server.
- QD-S-2.4 PASS (P1): verbs are specific (description, translation: "a skill for the analysis and drafting of contracts under Polish law"); no broad manage/handle/process verb is used as the capability statement.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence (translation): "Use it always when the user asks to analyse a Polish contract, audit contractual risks, generate a new contract in the KTZR style, add/edit a clause, check contract consistency, or when they paste/attach a Polish contractual document for review."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared for the skill as a whole. Evidence: the role-detection table (LAWYER / LAYPERSON) governs the user's role, not whether the Skill should trigger; no "do not trigger when..." statement is present.
- QD-S-3.6 PASS (P1): `name: commercial-legal-pl` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs. Evidence: the Skill accepts a pasted or attached contract of arbitrary length (the body itself discusses documents ">15 pages" and ">5,000 words") but declares no cap on input size.
- QD-S-3.3 PASS (P1, optional): ambiguous input is handled. Evidence (translation): "If it is not clear what the user wants - ask first, only then start the workflow."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): execution resource boundary missing. Evidence: the Skill calls the external `legal-cite` MCP tool ("`verify_article()` is OBLIGATORY before every citation") and opens workflow files, but declares no retry count, tool-invocation count, or execution timeout.
- QD-S-2.1 PASS (P0): no unbounded quantity directive used as an execution instruction.
- QD-S-2.2 PASS (P0): no unterminated-execution wording present.
- QD-S-5.4 PASS (P1): no chained invocation of other Skills declared (the `legal-cite` MCP tool and the `workflows/*` files belong to this Skill).
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: the Skill generates contracts and regulations with no bound on total output length.
- QD-S-2.3 PASS (P1): the only "etc."-equivalents ("itd.") appear in an illustrative vocabulary list, not in an output/functional structure that lets the LLM add items on its own.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): failure behavior is declared. Evidence (translation): "When MCP is unavailable: append [UNVERIFIED] to every citation."
- QD-S-4.2 PASS (P1): partial/non-final completion is handled. Evidence (translation): "In LAYPERSON mode do not generate a final document ready to sign - generate a draft marked [DRAFT - REQUIRES LAWYER VERIFICATION]".
- QD-S-4.3 PASS (P1): post-failure / never-do prohibitions are declared. Evidence (translation): "Never mark a document as 'ready to send / sign' without the user's explicit confirmation." and the anti-hallucination rule "never invent clauses or statutes; cite from the KTZR base or mark unverified".

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-175-commercial-legal-pl-skill.md - contract input accepted with no cap on size (body itself discusses documents >15 pages)
QD-S-1.2 | FAIL | evidence: same file, output formats - no bound on generated-document size
QD-S-1.3 | FAIL | evidence: same file, MCP section - "verify_article() is OBLIGATORY before every citation" with no retry/timeout/call-count bound
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file - sources declared (firm profile, clause/knowledge base, user document, MCP tool)
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording used as an execution instruction
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - the "itd." (etc.) appears in an illustrative vocabulary list, not an output structure
QD-S-2.4 | PASS | evidence: same file, description - specific verb "analysis and drafting of contracts"
QD-S-3.1 | PASS | evidence: same file, description - concrete triggers (contract analysis, risk audit, generation, clause edit, consistency check)
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file - "If it is not clear what the user wants - ask first" (translation)
QD-S-3.4 | PASS | evidence: same file, disclaimer - "The skill does not replace legal advice" (translation)
QD-S-3.6 | PASS | evidence: same file, front matter - name `commercial-legal-pl` consistent with the description
QD-S-4.1 | PASS | evidence: same file, MCP section - "When MCP is unavailable: append [UNVERIFIED] to every citation." (translation)
QD-S-4.2 | PASS | evidence: same file - "[DRAFT - REQUIRES LAWYER VERIFICATION]" marking (translation)
QD-S-4.3 | PASS | evidence: same file - "Never mark a document as 'ready to send / sign' without the user's explicit confirmation." (translation)
QD-S-5.1 | FAIL | evidence: same file - read/write/delete scopes not distinguished (files read, documents generated)
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (2): QD-S-1.1, QD-S-1.3
P1 (5): QD-S-1.2, QD-S-1.4, QD-S-3.2, QD-S-5.1, QD-S-5.3
P2 (0): none
Embedded-code QC (1): QC-0.2 (P1).

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds fenced snippets: a `verify_article(...)` usage example, a format-checklist block, a JSON MCP-install block, and a pre-final confirmation-gate block. QC-0 was run first.

QC-0.1 Syntax Parsability | PASS | evidence: the `verify_article(...)` example and the checklist/gate blocks are illustrative pseudo snippets; per the illustrative-snippet rule they are exempt from the parse-completeness requirement.
QC-0.2 Language Declaration | FAIL | evidence: the `verify_article(...)` block, the format-checklist block and the confirmation-gate block are fenced with a bare ``` and carry no language identifier (only the MCP-install block is tagged `json`).
QC-0.3 Structural Completeness | PASS | evidence: illustrative snippets; per the illustrative-snippet rule they are exempt from the standalone-parse requirement.
QC-0.4 Fence Integrity | PASS | evidence: every code fence opens and closes correctly.
QC-0.5 Language-Content Mismatch | PASS | evidence: the one tagged block (`json`) contains JSON, consistent with its tag.
QC-0 gate: FAIL (QC-0.2, P1). Per the entry gate, QC-1 through QC-4 were NOT executed.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 2 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's own responsibility boundary is locatable at the disclaimer and the pre-final confirmation gate.
- G0-4 (each Tool Schema's name/description/parameter descriptions are complete): NOT satisfied - the artifact set contains no Tool Schema (the `legal-cite` MCP server is referenced but its schema is not included).

Result: Gate-0 Not passed - G0-4 (no Tool Schema present in the artifact set; per-Tool name/description/parameter completeness cannot be verified).

## Stage D - Permission proportionality (QD-PM)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - incomplete artifact set (a full set requires System Prompt + Skill + all Tool Schemas; only a single Skill is present).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.
Nothing else is reported for Permission - no defect list, no score, no partial conclusions. (Permission did not execute due to Gate-0 not satisfied.)

## Stage E - Risk Explicit (EX)  [separate from the Inspect verdicts]

Static scan of the Skill description and body across the EX families (NL-A, NL-B, NR-O, NR-S) produced 1 risk item. The Skill is otherwise defensive (disclaimers, a pre-final confirmation gate, anti-hallucination rules); no NL-B, NR-O or NR-S subcategory matched, and no dangerous flag, credential or PII is present. The role-detection default (translation: "No signals - assume LAWYER, do not ask explicitly") was considered but not classified, because the top-level disclaimer is still emitted in every mode.

Risk Item Details:

[Risk Item 1]
- EX Classification: NL-A-7 (Reverse Constraint Removal)
- Risk Expression (translation): "Exception: if the user said 'express mode' or 'do it without asking' - generate, but add a header [DRAFT - REQUIRES VERIFICATION]."
- Severity Grade: Explicit-P1
- Reason: the statement explicitly removes a named safeguard - the mandatory pre-final confirmation gate (the "BRAMKA" that verifies party data, statute citations, and lawyer review) - on the user's own instruction. The worst consequence is producing a legal document without the human confirmation step; because the compensating draft header is retained, the crossing is partial and recoverable, so it is graded Explicit-P1 rather than Explicit-P0.
- Impact Type Labels: D2
- Trigger Condition Label: unconditional (the user can satisfy the condition on their own)
- Disposition: Fix before release, or obtain an approved exemption (e.g., bind the exemption to explicit, logged consent).
- Remediation Suggestion: restrict scope of the exemption / require explicit auditable consent instead of a free-form phrase.

Risk Item Summary: Total 1; Explicit-P0 = 0; Explicit-P1 = 1; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding is a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it did not pass its gate, so QC-1.x-QC-4.x did not run either); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.4, QD-S-5.1, QD-S-5.3 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-3.2 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |
| QC-0.2 | no candidate mapping defined in relevance-map.md (the map covers QD-* defect IDs only) | - | - | - |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability.

These lines are candidate associations only ("may", "needs dynamic verification"); they do not indicate that the backend is exploitable. v1 scope: single-defect mapping only; defect chains are out of scope.

## Status board

Stage A (Single-artifact):  Executed - single Skill inspected (QD-S + embedded-code QC)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 1 qualifying risk item (Explicit-P1 = 1)
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - report self-checked

## Stage G - Self-verification (report self-check, not a verdict on the artifact)

Self-verification: ID back-closure OK - red-line wording OK - output contract OK

In-place self-corrections: (1) all Polish evidence was rendered as English translation (no non-English text retained in the report); (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, the QC ID is present in code-contract-checklist.md, the EX ID is present in explicit-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
