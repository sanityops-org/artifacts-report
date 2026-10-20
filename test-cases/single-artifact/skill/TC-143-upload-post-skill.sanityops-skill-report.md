# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-143-upload-post-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 14, P1 = 1, P2 = 0. Embedded-code QC: 1 defect (QC-3.3 P2 placeholder credential).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 1, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-5.2 - no high-risk confirmation mechanism for publish/delete operations.
  2. QD-S-5.1 - read/write/delete permission scopes are not distinguished.
  3. QD-S-2.2 - unterminated execution declaration ("Poll job status until FINISHED").
  4. QD-S-1.4 - no read/write/delete permission-type distinction or prohibited-operation declaration.
  5. QD-S-5.3 - no environment boundary declared.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-143, YAML front matter carries `name` and `description`.
QD-S-0.2 | PASS | evidence: TC-143, both fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-143, the YAML front matter parses.
QD-S-0.4 | PASS | evidence: TC-143, field values match expected types.
QD-S-0.5 | PASS | evidence: TC-143, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-143, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L3 (High Risk).
Basis: the Skill performs external publishing to social platforms (`/upload`, `/upload_photos`, `/upload_text`, `/upload_document`), schedules and deletes scheduled posts (`DELETE /uploadposts/schedule/<job_id>`), and exposes an `/ffmpeg` endpoint that processes media with a raw command -> delete operations and irreversible external effects are declared -> L3.

### 2.3 Minimum rule set verdicts (L3 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-143, "Upload Document (LinkedIn only)". Excerpt: "document: PDF, PPT, PPTX, DOC, DOCX (max 100MB, 300 pages)" - a per-document limit exists, but no cap on the number of files or platforms is declared.
QD-S-1.2 | FAIL | evidence: TC-143, whole body. No upper limit on output size is declared.
QD-S-1.3 | FAIL | evidence: TC-143, "Notes". Excerpt: "Videos auto-switch to async if >59s processing time" - an async path is declared but no retry count, tool-invocation count, or timeout budget.
QD-S-1.4 | FAIL | evidence: TC-143, whole body. No read/write/delete permission-type distinction and no prohibited-operation declaration.
QD-S-1.5 | FAIL (P1) | evidence: TC-143, whole body. No permitted or prohibited data sources are declared.
QD-S-2.1 | PASS | evidence: TC-143, no unbounded quantity wording attached to a processing instruction was located (the "up to 2000 posts" of the Reddit endpoint is a fixed bound).
QD-S-2.2 | FAIL | evidence: TC-143, "FFmpeg Editor". Excerpt: "Poll job status until `FINISHED`" - "until" without a defined termination condition.
QD-S-2.3 | PASS | evidence: TC-143, no open-ended enumeration (etc./and others/such as) governing output or functional structure was located.
QD-S-2.4 | FAIL | evidence: TC-143, "FFmpeg Editor". Excerpt: "Process media with custom FFmpeg commands" - a broad verb ("Process") without a non_goals declaration excluding application scenarios.
QD-S-3.1 | PASS | evidence: TC-143, front matter description. Excerpt: "Use when posting videos, photos, text, or documents to TikTok, Instagram, YouTube, LinkedIn, Facebook, X (Twitter), Threads, Pinterest, Reddit, or Bluesky." - triggers are specific.
QD-S-3.2 | FAIL | evidence: TC-143, whole body. No deactivation conditions / "when NOT to trigger" declaration exists.
QD-S-3.4 | FAIL | evidence: TC-143, whole body. No non_goals / out-of-scope task declaration exists.
QD-S-3.5 | PASS | evidence: TC-143, critical branches (empty input, unknown platform) are not explicitly enumerated, but the capability matrix and error table give default guidance; recorded as PASS at the mandatory-set granularity.
QD-S-3.6 | PASS | evidence: TC-143, `name: upload-post` with a platform-enumerated description consistent with the body.
QD-S-4.1 | FAIL | evidence: TC-143, "Error Codes". Excerpt: "| 429 | Rate limit / quota exceeded |" - error codes are listed with meanings only; no failure-handling or recovery behavior is declared.
QD-S-4.2 | FAIL | evidence: TC-143, whole body. No declaration of whether partial completion is acceptable.
QD-S-4.3 | FAIL | evidence: TC-143, whole body. No post-failure prohibited behaviors are stated.
QD-S-5.1 | FAIL | evidence: TC-143, whole body. The Skill operates on data (upload/publish/delete) but does not distinguish read, modify, and delete permission scopes.
QD-S-5.2 | FAIL | evidence: TC-143, "Scheduling". Excerpt: "| `/uploadposts/schedule/<job_id>` | DELETE | Cancel scheduled post |" - an irreversible operation is declared with no confirmation mechanism.
QD-S-5.3 | FAIL | evidence: TC-143, whole body. No permitted or prohibited operational environment is declared.
QD-S-5.4 | PASS | evidence: TC-143, no chained/inter-skill invocation is declared.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): Defect - no non_goals; read/write/delete scopes not distinguished.
TRIGGER (QD-S-3.1, QD-S-3.2): Partial - positive triggers are specific, but no deactivation conditions exist.
INPUT (QD-S-1.1, QD-S-3.3): Defect - only per-document limits; no cap on number/size of inputs overall.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - unbudgeted async/FFmpeg execution; no chaining declared (no 5.4 defect).
OUTPUT (QD-S-1.2, QD-S-2.3): Defect - no output size limit; no open-enumeration defect.
FAILURE (QD-S-4.x): Defect - no failure behavior, partial-completion, or prohibited-behavior declarations.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing
- QD-S-1.2 Output Size Missing
- QD-S-1.3 Execution Resource Boundary Missing
- QD-S-1.4 Permission Boundary Missing
- QD-S-2.2 Unterminated Execution Declaration
- QD-S-2.4 Broad Capability Verbs
- QD-S-3.2 Missing Deactivation Conditions
- QD-S-3.4 Undefined Task Scope
- QD-S-4.1 Undefined Failure Behavior
- QD-S-4.2 Undeclared Partial Completion Legitimacy
- QD-S-4.3 Missing Post-Failure Prohibited Behaviors
- QD-S-5.1 Read/Write/Delete Not Distinguished
- QD-S-5.2 Missing High-Risk Confirmation
- QD-S-5.3 Undeclared Environment Boundaries

P1:
- QD-S-1.5 Data Source Boundary Missing

P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

Embedded snippets: several fenced `bash` (curl) blocks and one fenced `json` block.
QC-0.1 | PASS | the curl/JSON snippets are well-formed for their declared formats.
QC-0.2 | PASS | language identifiers (`bash`, `json`) are present.
QC-0.3 | PASS | the snippets are complete.
QC-1.1..1.4, QC-2.1..2.3, QC-3.1, QC-3.2 | Not Applicable | no Python/typed snippet is embedded.
QC-3.3 | FAIL | evidence: TC-143, "Authentication". Excerpt: "Authorization: Apikey YOUR_API_KEY" - a demo/placeholder credential value appears in runnable examples and may be mistaken for production (advisory, P2).

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records 14 unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the description states the platform set and capability scope, but no explicit responsibility/out-of-scope statement; recorded.
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above. Findings are static-document risks, not confirmed runtime exploits.

Findings: 1.

EX Block 1:
- EX classification: NR-S-4 (Code/Script Fragment Embedding).
- Risk expression (short excerpt): "full_command=ffmpeg -y -i {input} -c:v libx264 -crf 23 {output}" (a raw command string is passed to the `/ffmpeg` endpoint).
- Impact type labels: D2 (the processing target can be modified by an arbitrary command string).
- Severity grade: Explicit-P1 (recoverable tampering, scoped to the external service).
- Trigger condition label: unconditional (the user can supply the command on their own).
- Disposition: Fix before release, or approved exemption.
- Note: reachability and actual sandboxing are handed to Risk Implicit (NOT run). This is not a security conclusion.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-1.1 / QD-S-1.2 / QD-S-1.3 | input/output/execution resource boundaries missing | P0
- Candidate Attack Surface: AS-06 Resource Exhaustion and Runaway Execution (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbounded calls/output may expand; needs dynamic verification.

Impact Card: QD-S-2.2 | unterminated execution declaration | P0
- Candidate Attack Surface: AS-06, AS-07 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - "until FINISHED" without a bound may loop; needs dynamic verification.

Impact Card: QD-S-1.4 / QD-S-2.4 / QD-S-5.1 | permission boundary / broad verbs / read-write-delete not distinguished | P0
- Candidate Attack Surface: AS-04 Permission, Identity, and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects (candidate association).
- Candidate Failure Mode: FM-05, FM-09 (category-level).
- Candidate RAG-Agent metrics: Boundary Recognition, Safety Response, Traceability (candidate).
- Mapping strength: Medium (provisional, lite) - scope/permission convergence may occur; needs dynamic verification.

Impact Card: QD-S-3.2 / QD-S-3.4 | deactivation conditions / task scope undefined | P0
- Candidate Attack Surface: AS-01 Instruction and Context Boundary Confusion; AS-05 (candidate association).
- Candidate Failure Mode: FM-02, FM-07, FM-09 (category-level).
- Candidate RAG-Agent metrics: Relevance, Decomposition Capability, Boundary Recognition (candidate).
- Mapping strength: Conditional (provisional, lite) - scope expansion may occur under specific prompts; needs dynamic verification.

Impact Card: QD-S-4.1 / QD-S-4.2 / QD-S-4.3 | failure expansion | P0
- Candidate Attack Surface: AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-08, FM-09 (category-level).
- Candidate RAG-Agent metrics: Completeness, Coherence, Safety Response (candidate).
- Mapping strength: Medium (provisional, lite) - undefined post-failure behavior may expand scope; needs dynamic verification.

Impact Card: QD-S-5.2 / QD-S-5.3 | high-risk confirmation / environment boundaries missing | P0
- Candidate Attack Surface: AS-05 Tool Misuse and High-Risk Side Effects; AS-04 (candidate association).
- Candidate Failure Mode: FM-05, FM-09 (category-level).
- Candidate RAG-Agent metrics: Boundary Recognition, Safety Response, Traceability (candidate).
- Mapping strength: Medium (provisional, lite) - unconfirmed irreversible operations may execute; needs dynamic verification.

Impact Card: QD-S-1.5 | data source boundary missing | P1
- Candidate Attack Surface: AS-01, AS-03, AS-04 (candidate association).
- Candidate Failure Mode: FM-05, FM-09 (category-level).
- Candidate RAG-Agent metrics: Boundary Recognition, Safety Response, Traceability (candidate).
- Mapping strength: Conditional (provisional, lite) - data-source confusion may occur; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 1 finding (Explicit-P1).
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
