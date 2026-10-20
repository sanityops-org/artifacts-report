# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-169-k-dense-ai-scientific-agent-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 0, P1 = 1, P2 = 0 (QD-S: P0 0 / P1 1 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.2 - no deactivation condition declared (no statement of when the skill should NOT trigger).
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-169-k-dense-ai-scientific-agent-skills-skill.md, front matter (lines 14-23): `name: database-lookup`, `description`, `allowed-tools: Read Bash`, `license: MIT`, and a `metadata` block all present |
| QD-S-0.2 Field Content Non-Empty | PASS | all present fields carry content; `metadata` holds `version`, `last-reviewed`, `skill-author` |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (block scalar and nested `metadata`) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`allowed-tools`/`license` are strings; `metadata` is a mapping |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (core workflow, database selection guide, identifier formats, API keys, making API calls, pagination, output format, available databases) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: per the checklist's risk-level semantics, L2 = resource access, may involve sensitive data. This Skill makes bounded, rate-limited API calls (`allowed-tools: Read Bash`), reads API-key presence, and writes optional local output. These are recoverable resource operations; no delete, irreversible action, or permission change is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: the description limits the Skill to "documented public database APIs", and the workflow states "Do not fan out across many APIs just because they are available."
- QD-S-1.4 PASS (P1): permission boundaries are declared. Evidence: `allowed-tools: Read Bash` scopes the capability set, and "Never concatenate untrusted text into shell commands."
- QD-S-1.5 PASS (P1): data sources are declared. Evidence: the "## Available Databases" inventory bounds sources to the cataloged databases and their reference files ("Read the relevant reference file before making any API call").
- QD-S-2.4 PASS (P1): verbs are specific ("Queries documented public database APIs"); no broad manage/handle verb is used as the capability statement.
- QD-S-5.1 PASS (P1): read/write/delete are not conflated; the Skill is retrieval (read) with optional local file writes, and it never deletes.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation is concrete. Evidence: the description states "Used when a scientific, regulatory, financial, or other database-backed fact must be retrieved reproducibly from a named source", and the "## Core Workflow" defines the retrieval contract up front.
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the artifact defines activation and several in-skill constraints ("Do not fan out across many APIs just because they are available"), but states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): name `database-lookup` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 PASS (P0): an input boundary is declared. Evidence: "Ask for confirmation before a retrieval would exceed 10,000 records, 100 API calls, or the selected API's documented bulk-use guidance."
- QD-S-3.3 PASS (P1): ambiguous/insufficient input is handled. Evidence: "If a required scientific constraint is missing and affects correctness, ask a clarifying question rather than guessing."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 PASS (P0): an execution resource boundary is declared. Evidence: "Keep at most 5 independent API requests in flight at once"; "If you get a rate-limit error (HTTP 429 or 503), wait briefly and retry once"; "Do not continue past 10,000 records or 100 API calls without explicit user confirmation".
- QD-S-5.4 PASS (P1): no chained invocation of other Skills is declared; the tooling is standard HTTP clients.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): the output is bounded. Evidence: "Always return: A concise answer or structured result table, not an unbounded raw dump by default"; "If results are very large, present the most relevant portion and note how much additional data is available."
- QD-S-2.3 PASS (P1): no open-ended enumeration in a functional structure; the identifier table and database inventory are closed lists.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): failure behavior is declared. Evidence: an "### Error recovery" section (check identifier format; try alternatives; try another database; report the failure) and "Fail visible, not plausible".
- QD-S-4.2 PASS (P1): partial/incomplete completion is handled. Evidence: "if pagination stops early, counts disagree, filters are ambiguous ... report the limitation before drawing conclusions."
- QD-S-4.3 PASS (P1): post-failure/forbidden behaviors are declared. Evidence: "Do not feed raw response text into later shell, Python, SQL, ADQL, or GraphQL commands without extracting and re-validating the specific field needed."

(Additional L2 items carried here for completeness)
- QD-S-2.1 PASS (P0): "all records" usage is accompanied by a corresponding limit (the 10,000-record / 100-call cap plus explicit confirmation), so it is not unbounded.
- QD-S-2.2 PASS (P0): no unterminated-execution wording (`keep trying / until success / ensure complete / persist until`) present.
- QD-S-5.3 PASS (P1): the Skill operates on public/registered database APIs and is local-first for outputs; no production-environment operation is introduced.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | PASS | evidence: TC-169-k-dense-ai-scientific-agent-skills-skill.md, Core Workflow - "Ask for confirmation before a retrieval would exceed 10,000 records, 100 API calls"
QD-S-1.2 | PASS | evidence: same file, Output Format - "not an unbounded raw dump by default"
QD-S-1.3 | PASS | evidence: same file, Making API Calls - "Keep at most 5 independent API requests in flight at once"; "retry once"
QD-S-1.4 | PASS | evidence: same file, front matter - `allowed-tools: Read Bash`; "Never concatenate untrusted text into shell commands"
QD-S-1.5 | PASS | evidence: same file, "## Available Databases" - "Read the relevant reference file before making any API call"
QD-S-2.1 | PASS | evidence: same file - "all records" pairs with the 10,000-record / 100-call cap and confirmation
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - identifier table and database inventory are closed lists
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Queries documented public database APIs"
QD-S-3.1 | PASS | evidence: same file, description - states when a database-backed fact must be retrieved reproducibly
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Core Workflow - "ask a clarifying question rather than guessing"
QD-S-3.4 | PASS | evidence: same file - scope bounded to cataloged public database APIs
QD-S-3.6 | PASS | evidence: same file, front matter - name `database-lookup` consistent with the description
QD-S-4.1 | PASS | evidence: same file, "### Error recovery" - report the failure; "Fail visible, not plausible"
QD-S-4.2 | PASS | evidence: same file - "report the limitation before drawing conclusions"
QD-S-4.3 | PASS | evidence: same file - "Do not feed raw response text into later shell, Python, SQL ... commands"
QD-S-5.1 | PASS | evidence: same file - retrieval (read) with optional local writes; no delete operation
QD-S-5.3 | PASS | evidence: same file - public/registered database APIs; local-first outputs
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (0): none
P1 (1): QD-S-3.2
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds two runnable `bash` snippets: a silent presence test `test -n "${FRED_API_KEY:-}"` and a `curl` example (`curl --fail-with-body --silent --show-error -H "Accept: application/json" "https://rest.uniprot.org/uniprotkb/P04637.json"`). One plain-text output-format template is also fenced.

QC-0.1 Syntax Parsability | PASS | evidence: both snippets are valid shell syntax.
QC-0.2 Language Declaration | PASS | evidence: the code fences carry the `bash` language tag.
QC-0.3 Structural Completeness | PASS | evidence: the snippets are complete for their illustrative intent.
QC-0.4 Fence Integrity | PASS | evidence: every fence opens and closes correctly.
QC-0.5 Language-Content Mismatch | PASS | evidence: declared `bash` matches the content.
QC-0 gate: PASS. Proceed to QC-1 through QC-4.

QC-1.1 Undefined Name Reference | PASS | evidence: `curl` and `test` are standard shell commands.
QC-1.2 Invalid Import | Not Executed | evidence: no dependency list is declared; snippet contains no import statements.
QC-1.3 Deprecated API Usage | Not Executed | evidence: no API version database available; no internally evident deprecated call.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: `curl` closes its connection per invocation.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | PASS | evidence: API keys are referenced as environment variables (`${FRED_API_KEY:-}`), not hardcoded literals.
QC-4.1 Snippet-Artifact Declaration Mismatch | PASS | evidence: the snippets use parameters consistent with the artifact's own description.
QC-4.2 Snippet-Body Version/API Drift | PASS | evidence: no body/snippet version contradiction found.

QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 0 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the Skill's scope statements and `allowed-tools` are the nearest locatable analogues in this artifact.
- G0-4 (each Tool Schema's name/description/parameter descriptions are complete): NOT satisfied - the artifact set contains no Tool Schema.

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

Static scan of the Skill description and body across the EX families (NL-A, NL-B, NR-O, NR-S) found no expression matching an EX subcategory:
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The untrusted-data and injection-safety rules are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. Credentials are referenced only by environment-variable name (for example `FRED_API_KEY`) with registration URLs; no literal secret value, and no hardcoded personal data, is present.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no code defect); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-3.2 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition.

These lines are candidate associations only ("may", "needs dynamic verification"); they do not indicate that the backend is exploitable. v1 scope: single-defect mapping only; defect chains are out of scope.

## Status board

Stage A (Single-artifact):  Executed - single Skill inspected (QD-S + embedded-code QC)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 qualifying risk items
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - report self-checked

## Stage G - Self-verification (report self-check, not a verdict on the artifact)

Self-verification: ID back-closure OK - red-line wording OK - output contract OK

In-place self-corrections: (1) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (2) all emitted QD-S and QC IDs are present in skill-checklist.md / code-contract-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md; (3) no CJK characters appear anywhere in this report.
