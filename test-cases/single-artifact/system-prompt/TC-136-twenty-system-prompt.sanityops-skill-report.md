# SanityOps Inspect Lite - Report

Artifact: TC-136-twenty-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; single artifact, no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 3, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-1.3.2 - vague qualifier ("the most important terms") carries the Keyword selection.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared for the transcript.
  - QD-P-2.7.2 - no counter-examples provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-136-twenty-system-prompt.md` -> **System Prompt** (a joined string-array prompt). Basis: the case metadata declares Artifact Type = System Prompt; the carried content is `DEFAULT_CALL_RECORDING_SUMMARY_PROMPT`, a meeting-note-taker instruction prompt, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: no Tool Schema and no Skill definition accompany the prompt. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the prompt converts one diarized, time-stamped transcript into fixed-format meeting notes in a single invocation; no state retention, tool invocations, multi-turn dialogue, or complex reasoning are declared. All four L1 criteria are satisfied; L2/L3 criteria are not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-136 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-136 - no conflicting MUST constraints; the admin-instruction clause subordinates itself to format and grounding rules.
- QD-P-1.1.3 | PASS | evidence: TC-136 - the inline examples (bold owner line plus bullets; timestamped Notes headings) are consistent with the rules.
- QD-P-1.2.1 | PASS | evidence: TC-136 - the meeting-note-taker role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-136 - the GitHub-flavored-Markdown output style matches the note-taking role.
- QD-P-1.2.3 | PASS | evidence: TC-136 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-136 - bounded quantifiers only ("A single sentence", "One paragraph of 2-4 sentences", "exactly one line").
- QD-P-1.3.2 | FAIL | evidence: TC-136, ## Keywords - a vague qualifier carries the selection decision; excerpt: "A single comma-separated line of the most important terms, names, and topics from the call."
- QD-P-1.3.3 | PASS | evidence: TC-136 - output is bounded to facts observable in the transcript; no unbounded tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-136 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-136 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-136 - the stated behaviors support the meeting-notes objective.
- QD-P-1.6.1 | PASS | evidence: TC-136 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-136 - no rule keyed on the model's own confidence/intent/motivation state found.
- QD-P-1.6.3 | PASS | evidence: TC-136 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-136 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-136 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-136 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-136 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-136 - input sources declared (the diarized, time-stamped transcript and the optional workspace-admin instructions).
- QD-P-2.2.2 | FAIL | evidence: TC-136 - no input format/encoding/size limits declared for the transcript (absence).
- QD-P-2.2.3 | PASS | evidence: TC-136 - the optional nature of the admin instructions is distinguished ("The message may include additional instructions from the workspace admin.").
- QD-P-2.2.4 | PASS | evidence: TC-136 - degenerate-input handling declared; excerpt: "If the transcript is too short, unintelligible, or contains no substantive discussion, ... return exactly one line in this format".
- QD-P-2.3.1 | PASS | evidence: TC-136 - output format declared (GitHub-flavored Markdown, fixed sections, no code fences).
- QD-P-2.3.2 | PASS | evidence: TC-136 - the per-section output shape is fully specified (Gist, Overview, Action Items, Notes, Keywords).
- QD-P-2.3.4 | FAIL | evidence: TC-136 - no sensitive-data filtering or privacy handling rules declared (absence) for the recorded call content.
- QD-P-2.5.2 | FAIL | evidence: TC-136 - no prohibition/security boundary constraints declared (absence).
- QD-P-2.7.1 | PASS | evidence: TC-136 - positive examples are provided (owner-grouped action items; timestamped Notes headings).
- QD-P-2.7.2 | FAIL | evidence: TC-136 - no counter-examples provided (absence).
- QD-P-2.7.3 | PASS | evidence: TC-136 - boundary cases are exemplified (the "None." line; the "Unassigned" owner; the unavailable-prefix fallback example).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-136, `DEFAULT_CALL_RECORDING_SUMMARY_PROMPT` block - the TypeScript array/join expression parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-136 - the fenced block carries an explicit language identifier (`typescript`).
- QC-0.3 | PASS | evidence: TC-136 - the snippet is a structurally complete exported constant.
- QC-0.4 | PASS | evidence: TC-136 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-136 - the declared language (`typescript`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-136 - the symbol `CALL_RECORDING_SUMMARY_UNAVAILABLE_PREFIX` is brought in by the import; the `${...}` interpolation is a runtime template placeholder; no type mismatch.
- QC-1.2 | Not Executed | evidence: TC-136 - the import targets a local module path and no dependency list is supplied (dependency-context rule); no internally evident non-existent module.
- QC-1.3 | Not Executed | evidence: TC-136 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-136 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1 | PASS | evidence: TC-136 - the single import is referenced by the interpolation, so it is not unused.
- QC-3.2 | PASS | evidence: TC-136 - no referenced symbol lacks an import/definition.
- QC-3.3 | PASS | evidence: TC-136 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-136 - the snippet is consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available (only the System Prompt was supplied).

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in the array ("You are an AI meeting note-taker for a CRM.").
- G0-4 (each Tool Schema name/description/parameter descriptions complete): FAIL - no Tool Schema is supplied; field-by-field completeness cannot be verified.
- Gate-0 result: Not passed - G0-4.

## Stage D - Permission proportionality (QD-PM, Quick Mode)
Not Executed - incomplete artifact set (Gate-0 G0-4 unsatisfied; no Tool Schema supplied).

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - no Tool Schema supplied; operation semantics undeterminable; permission items cannot be categorized.
Remediation Actions: Fix above upstream items, then re-run Gate-0

(Wording note: the Permission stage was "Not Executed" because Gate-0 was not satisfied; it is not reported as FAIL and no ERROR/BLOCKED status is asserted.)

## Stage E - Risk Explicit (EX) - physically separated from Inspect verdicts
Scan scope: System Prompt static text (NL-A / NL-B / NR-O / NR-S).
Findings: none.
No explicitly expressed risk item matching an EX classification was found. The grounding rules ("use only information present in the transcript"; "Never invent names, numbers, commitments, outcomes, or times") and the unavailable-transcript fallback are constraint statements, not risk expressions. The instruction-layering clause ("The message may include additional instructions from the workspace admin. Apply them on top of these rules without breaking the output format or the grounding rules above.") is a bounded, subordinate instruction statement from a trusted source, not a priority-override or exfiltration expression. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Consistency, Format Compliance. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
