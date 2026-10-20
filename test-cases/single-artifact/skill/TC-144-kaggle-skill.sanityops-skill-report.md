# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-144-kaggle-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 2, P1 = 0, P2 = 0. Embedded-code QC: 0 defects (QC-0 baseline PASS; QC-1..3 Not Applicable - the snippet is a shell invocation).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-2.3 - open-ended enumeration in functional structure ("Anything else the Kaggle CLI does" via `cli --`).
  2. QD-S-5.3 - no permitted or prohibited operational environment declared.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-144, YAML front matter carries `name`, `description`, `license`, `compatibility`, `allowed-tools`, and `metadata`.
QD-S-0.2 | PASS | evidence: TC-144, all required fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-144, the YAML front matter parses (nested `metadata` mappings).
QD-S-0.4 | PASS | evidence: TC-144, field values match expected types.
QD-S-0.5 | PASS | evidence: TC-144, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-144, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L3 (High Risk).
Basis: the Skill performs account-changing external writes (submit submissions, publish datasets/models, start notebook runs) and exposes an open-ended `cli --` passthrough to the Kaggle CLI -> external writes plus an unbounded operation channel -> L3.

### 2.3 Minimum rule set verdicts (L3 mandatory set)

QD-S-1.1 | PASS | evidence: TC-144, "Exit codes". Excerpt: "| 5 | Refused for safety: ... a download above the size limit, a download folder that is not empty ..." - an input/download size bound and refusal conditions are declared.
QD-S-1.2 | PASS | evidence: TC-144, "Run a command". Excerpt: "A long text (a page, a writeup) is cut with a note that says how to get the rest" - output truncation is declared.
QD-S-1.3 | PASS | evidence: TC-144, "Exit codes". Excerpt: "| 124 | Timed out while a notebook was running or a submission was being scored |" - a timeout boundary is declared.
QD-S-1.4 | PASS | evidence: TC-144, "Before any action that changes the account". Excerpt: "Stay read-only until the user asks for a change." - read vs write is explicitly distinguished.
QD-S-1.5 | PASS | evidence: TC-144, "Credentials". Excerpt: "Public content needs no credential." - permitted data sources and credential scope are declared.
QD-S-2.1 | PASS | evidence: TC-144, no unbounded quantity wording attached to a processing instruction was located.
QD-S-2.2 | PASS | evidence: TC-144, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-2.3 | FAIL | evidence: TC-144, "Pick the command". Excerpt: "| Anything else the Kaggle CLI does | `cli -- <kaggle arguments>` |" - an open-ended enumeration that allows the LLM to extend the operation set on its own.
QD-S-2.4 | PASS | evidence: TC-144, no broad capability verb (manage/handle/coordinate/automate/process/address) is used without an accompanying scope exclusion.
QD-S-3.1 | PASS | evidence: TC-144, front matter description. Excerpt: "Use when the user explicitly mentions Kaggle, kaggle.com, a Kaggle URL, Kaggle competitions..." - triggers are precise.
QD-S-3.2 | PASS | evidence: TC-144, front matter description. Excerpt: "Do not use for generic ML, GPU/TPU, notebook, dataset, benchmark, or data-science tasks unless the user clearly ties them to Kaggle." - deactivation conditions are stated.
QD-S-3.4 | PASS | evidence: TC-144, front matter description and body. Excerpt: "Do not use this skill for generic machine learning, GPU, notebook, dataset, model, benchmark, or data-science work unless the user ties the task to Kaggle." - a non_goals declaration is present.
QD-S-3.5 | PASS | evidence: TC-144, "Pick the command" and "Credentials". Excerpt: "Setup problems | `doctor`; `credentials --verify`" - default handling for the empty/setup-missing branch is declared.
QD-S-3.6 | PASS | evidence: TC-144, `name: kaggle` with an accurate, scope-bounded description.
QD-S-4.1 | PASS | evidence: TC-144, "Exit codes" table. Excerpt: "| 2 | Wrong arguments, or a credential is needed and none works |", "| 127 | ... the message has the install command |" - failure behavior is declared.
QD-S-4.2 | PASS | evidence: TC-144, "Run a command". Excerpt: "A long text (a page, a writeup) is cut with a note" - partial output is legitimate and declared.
QD-S-4.3 | PASS | evidence: TC-144, "Before any action that changes the account". Excerpt: "when a command is refused, say so and leave the switch alone" - a post-refusal behavior constraint is stated.
QD-S-5.1 | PASS | evidence: TC-144, "Before any action that changes the account". Excerpt: "Stay read-only until the user asks for a change." - read and write scopes are distinguished.
QD-S-5.2 | PASS | evidence: TC-144, "Before any action that changes the account". Excerpt: "Run it without `--yes`. That is a dry run ... After the user says yes, run it again with `--yes`" - an explicit confirmation mechanism exists for irreversible operations.
QD-S-5.3 | FAIL | evidence: TC-144, whole body. No permitted or prohibited operational environment is declared.
QD-S-5.4 | PASS | evidence: TC-144, whole body: no chained/inter-skill invocation is declared.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): No defect - scope and read/write distinction are declared.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect - trigger and deactivation conditions are precise.
INPUT (QD-S-1.1, QD-S-3.3): No defect - input/download bounds and refusal conditions declared.
EXECUTION (QD-S-1.3, QD-S-5.4): No defect - timeout boundary declared; no chaining.
OUTPUT (QD-S-1.2, QD-S-2.3): Defect - open-ended enumeration ("Anything else the Kaggle CLI does").
FAILURE (QD-S-4.x): No defect - exit-code semantics and refusal handling are declared.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-2.3 Open-Ended Enumeration in Structure - "Anything else the Kaggle CLI does" (`cli --`).
- QD-S-5.3 Undeclared Environment Boundaries - no permitted/prohibited environment declaration.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

Embedded snippets: one fenced `bash` block ("Run a command") and one untagged block showing the `untrusted-content-...` wrapper (a data sample, not code).
QC-0.1 | PASS | the `bash` snippet is well-formed.
QC-0.2 | PASS | a language identifier (`bash`) is present on the runnable snippet.
QC-0.3 | PASS | the runnable snippet is complete.
QC-1.1..1.4, QC-2.1..2.3, QC-3.1..3.3 | Not Applicable | the snippet is a shell invocation, not Python/typed code; the untagged block is a data sample.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records 2 unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Satisfied - the description and "Before any action that changes the account" section state scope and the read-only responsibility boundary (locatable in the front matter and body).
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text. The Skill states explicit prohibitions ("Never echo, log, or commit a credential value") and a read-only default; no data-exfiltration instruction, encoded payload, obfuscation, dangerous config flag, hardcoded credential/PII, or reverse-constraint-removal wording was located. The embedded `untrusted-content-...` handling is an anti-injection control, not an EX risk expression. This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-2.3 | open-ended enumeration in structure | P0
- Candidate Attack Surface: AS-06 Resource Exhaustion and Runaway Execution; AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - an open operation channel may extend the action set beyond the enumerated reads; needs dynamic verification.

Impact Card: QD-S-5.3 | environment boundary not declared | P0
- Candidate Attack Surface: AS-04 Permission, Identity, and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects (candidate association).
- Candidate Failure Mode: FM-05, FM-09 (category-level).
- Candidate RAG-Agent metrics: Boundary Recognition, Safety Response, Traceability (candidate).
- Mapping strength: Conditional (provisional, lite) - may matter under specific deployment settings; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
