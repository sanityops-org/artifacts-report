# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-162-sergebulaev-linkedin-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 2, P1 = 5, P2 = 0 (QD-S: P0 2 / P1 5 / P2 0; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.3 - external tool calls (`lib.illustrate`, `lib.publish`) are declared but no retry count, invocation count, or execution timeout is set.
  2. QD-S-1.1 - no upper limit on input number or size.
  3. QD-S-2.3 - open-ended enumeration present ("... false-binary, and more").
  4. QD-S-1.4 - no read/write/delete permission-type distinction or prohibited-operation declaration for the publish operation.
  5. QD-S-5.3 - no environment boundary declared for the live LinkedIn publish endpoint.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-162-sergebulaev-linkedin-skills-skill.md, front matter (lines 14-15): `name: linkedin-post-writer` and `description: "..."` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (quoted `description`) |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (When to use, Formulas table, Steps 1-8, Hard rules, Anti-patterns, Resources, Related skills) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: per the checklist's risk-level semantics, L2 = resource access, may involve sensitive data. The Skill loads voice/story data files, generates images with a stated cost (`lib.illustrate`), and publishes externally via `lib.publish`. The publish path is approval-gated and reversible (`lib.unpublish` is declared), so it is not classified L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a non_goals declaration is present. Evidence: the description states "Not for reviewing existing drafts (use linkedin-humanizer --mode audit)."
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: "Call `lib.publish(kind=\"post\", draft_text=<approved>, target_url=\"https://www.linkedin.com/post/new/\", platforms=[{\"platform\":\"linkedin\",\"platformId\":<id>}], scheduled_time=<iso_or_None>, media_urls=<list_or_None>)." declares an external write with no prohibited-operation boundary.
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence: "If `../../references/story-bank.md` has `filled: yes`, load it too and take concrete details (numbers, dates, named projects) from there instead of asking mid-draft. Never invent a figure that is not in it".

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: "## When to use - User says \"write me a LinkedIn post about X\" - User has a topic + a rough angle and needs a hook + structure".
- QD-S-3.2 PASS (P1): deactivation conditions are declared. Evidence: the description states "Not for reviewing existing drafts (use linkedin-humanizer --mode audit)."
- QD-S-3.6 PASS (P1): `name: linkedin-post-writer` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: "1. **Gather inputs.** Topic, angle, draft ideas if the user has them, target audience (founders / operators / marketers), desired length (short 300-500 / medium 900-1300 / long 1500-1900 chars)." declares no cap on the number or size of inputs.
- QD-S-3.3 PASS (P1): ambiguous/insufficient input is handled. Evidence: "if the bank has nothing that fits, ask the user or offer `linkedin-interviewer`."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): external tool calls are declared but no retry count, tool-invocation count, or execution timeout is set. Evidence: "generate it with `lib.illustrate(prompt, kind=\"wide\")`, pulling brand handle/color from Voice & Brand Profile §6 for the overlay. Show the returned `url` + `cost` in the approval card" declares a cost-bearing external call with no invocation budget.
- QD-S-5.4 FAIL (P1): sibling Skills are invoked without declaring the permitted/prohibited downstream scope. Evidence: "## Related skills - `linkedin-humanizer` - aggressive AI-tell scrubber, plus `--mode audit` for pre-publish review - `linkedin-hook-extractor` - reverse-engineer a hook from a viral post you admire".

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): an explicit output-size bound is declared. Evidence: "The one hard limit is LinkedIn's 3,000 characters."
- QD-S-2.3 FAIL (P1): open-ended enumeration present. Evidence: "20 2026 hook formulas (anaphora, R.I.P., time-anchor, curiosity-gap, contrarian, controlled A/B, false-binary, and more)".
- QD-S-4.2 PASS (P1): the target length is user-controlled and explicitly declared. Evidence: "the target the user picked in step 1 wins. 900-1,300 chars is the default when they express no preference, not a ceiling over their choice."

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): failure/degradation behavior is declared. Evidence: "No Pixfaro key -> it drafts the prompt for the user to generate manually." and "If the user reconsiders after approving, call `lib.unpublish(...)` to cancel it before it goes out."
- QD-S-4.3 PASS (P1): post-failure/prohibited behaviors are declared. Evidence: the "## Anti-patterns (skill will refuse)" section and "Never invent a figure that is not in it".

(Additional L2 items carried here for completeness)
- QD-S-2.1 PASS (P0): no unbounded exhaustive-processing directive; "Voice profile first (all drafts)" is a scope descriptor, not an "all items with no cap" instruction.
- QD-S-2.2 PASS (P0): no "keep trying / until success / ensure complete / persist until" wording present.
- QD-S-2.4 PASS (P1): verbs are specific ("Draft a new LinkedIn post from scratch"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 FAIL (P1): a data operation is declared but read/write/delete scopes are not distinguished. Evidence: "**On approval.** Call `lib.publish(...)`. The wrapper handles Publora / manual / diy routing. If the user reconsiders after approving, call `lib.unpublish(post_group_id=<postGroupId from the response>)` to cancel it before it goes out."
- QD-S-5.3 FAIL (P1): no environment boundary declared. Evidence: "target_url=\"https://www.linkedin.com/post/new/\"" targets a live production endpoint with no environment-boundary statement.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-162-sergebulaev-linkedin-skills-skill.md, Step 1 - "Topic, angle, draft ideas if the user has them..." with no input cap
QD-S-1.2 | PASS | evidence: same file, Step 3 - "The one hard limit is LinkedIn's 3,000 characters."
QD-S-1.3 | FAIL | evidence: same file, Step 6 - "`lib.illustrate(prompt, kind=\"wide\")`" with no retry/timeout budget
QD-S-1.4 | FAIL | evidence: same file, Step 8 - "Call `lib.publish(kind=\"post\", ...)`" with no prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Steps - "Never invent a figure that is not in it"
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording used as an execution instruction
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | FAIL | evidence: same file, description - "anaphora, R.I.P., time-anchor, curiosity-gap, contrarian, controlled A/B, false-binary, and more"
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Draft a new LinkedIn post"
QD-S-3.1 | PASS | evidence: same file, "## When to use" - concrete user intents
QD-S-3.2 | PASS | evidence: same file, description - "Not for reviewing existing drafts (use linkedin-humanizer --mode audit)."
QD-S-3.3 | PASS | evidence: same file, Steps - "if the bank has nothing that fits, ask the user"
QD-S-3.4 | PASS | evidence: same file, description - "Not for reviewing existing drafts..."
QD-S-3.6 | PASS | evidence: same file, front matter - name `linkedin-post-writer` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Step 6 - "No Pixfaro key -> it drafts the prompt for the user to generate manually."
QD-S-4.2 | PASS | evidence: same file, Step 3 - "the target the user picked in step 1 wins"
QD-S-4.3 | PASS | evidence: same file, "## Anti-patterns (skill will refuse)" - prohibited behaviors declared
QD-S-5.1 | FAIL | evidence: same file, Step 8 - publish/unpublish declared without read/write/delete scope distinction
QD-S-5.3 | FAIL | evidence: same file, Step 8 - "target_url=\"https://www.linkedin.com/post/new/\"" with no environment boundary
QD-S-5.4 | FAIL | evidence: same file, "## Related skills" - sibling skills named without a permitted/prohibited scope

### A.4 Defect list (sorted P0 first)

P0 (2): QD-S-1.1, QD-S-1.3
P1 (5): QD-S-1.4, QD-S-2.3, QD-S-5.1, QD-S-5.3, QD-S-5.4
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no code snippets (it uses inline-code conventions such as `lib.publish(...)` within prose, but no fenced code blocks). QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute - there are no embedded fenced snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 2 P0 findings (QD-S-1.1, QD-S-1.3); recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The "Anti-patterns (skill will refuse)" and "Never invent a figure" rules are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The publish target is a legitimate LinkedIn endpoint; no credential literals appear (the skill explicitly states "No Pixfaro key").

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-2.3 | AS-06; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Conditional |
| QD-S-1.4, QD-S-5.1 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |
| QD-S-5.4 | AS-04; AS-05; AS-07 | D1, D2, D3 | FM-05, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability; failure expansion -> Completeness, Coherence, Safety Response.

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

In-place self-corrections: (1) artifact arrows/en dashes were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
