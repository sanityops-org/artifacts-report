# SanityOps Inspect-Lite Report - TC-063-claude-gym-coach-file-based-agents.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: `skills/gym/SKILL.md` - type = Skill. Basis: markdown SKILL.md with YAML front matter (`name: coach-gym`, `description:`, `argument-hint:`) (TC-063 lines 47-53).
- Artifact 2: `skills/plan/SKILL.md` - type = Skill. Basis: markdown SKILL.md with YAML front matter (`name: coach-plan`, `description:`, `argument-hint:`) (TC-063 lines 98-104).
- Athlete data files (`profile.md`, `program.md`, `gym.md`, `log/*.md`) are plain Markdown data the skills read/write, not logic artifacts.
- The Node statistics script (`scripts/stats.mjs`) is a referenced script, not a logic artifact.
- No JSON/function-calling Tool Schema and no standalone System Prompt file are provided; both provided files are Skill.
- Same-agent scope: both files belong to the same agent ("Claude Gym Coach").

## Executive Summary
- Stages executed: A (two Skills, L2; plus embedded-snippet QC), B (Not Executed), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts (Stage A): P0 = 4, P1 = 10, P2 = 0.
- Gate-0 result: Passed (G0-3 satisfied; G0-4 not applicable - no Tool Schema). G0-1 informational (4 unfixed P0 carried forward).
- Risk-Explicit summary: Executed, 0 explicit risk items.
- Top findings:
  - QD-S-1.3 - delegated planner / script invocations with no retry count, invocation count, or timeout.
  - QD-S-1.1 - no input-size/number bound declared (both Skills).
  - QD-S-5.4 - the plan Skill delegates to a subagent without a declared downstream scope.
  - QD-S-4.2 - no partial-completion policy declared.
  - QD-S-4.3 - no post-failure prohibited-behavior declaration.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - `skills/gym/SKILL.md` (Skill)
Tier determination: L2 (Medium Risk) - basis: edits the athlete's gym inventory and runs a Node helper (state-changing, recoverable resource access).
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-063 line 49 - `name: coach-gym`.
QD-S-0.2 | PASS | evidence: TC-063 line 50 - `description` non-empty.
QD-S-0.3 | PASS | evidence: TC-063 lines 48-52 - YAML parses.
QD-S-0.4 | PASS | evidence: TC-063 line 51 - `argument-hint` typed as a string.
QD-S-0.5 | PASS | evidence: TC-063 lines 48-92 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-063 lines 48-52 - front matter + body present.
Baseline passed -> mandatory set (Q6):
QD-S-1.1 | FAIL | evidence: TC-063 lines 55-92 - no input-count/size upper bound declared.
QD-S-1.3 | FAIL | evidence: TC-063 lines 80-83 - runs `stats.mjs catalog`; no retry count, invocation count, or timeout declared.
QD-S-2.1 | PASS | evidence: TC-063 lines 55-92 - no unbounded processing declaration.
QD-S-2.2 | PASS | evidence: TC-063 lines 55-92 - no unterminated-execution wording.
QD-S-3.4 | PASS | evidence: TC-063 line 62 - explicit non_goals: "It never touches `program.md`".
QD-S-4.1 | PASS | evidence: TC-063 lines 64-66 - failure behavior declared: on missing/mismatched `.coach.json`, stop without auto-migrating.
Recommended set (14, P1):
QD-S-1.2 | FAIL | evidence: TC-063 lines 55-92 - no output-size bound declared.
QD-S-1.4 | PASS | evidence: TC-063 lines 62, 88-90 - write boundary declared: "Only the inventory and the athlete's `gym` field are written".
QD-S-1.5 | PASS | evidence: TC-063 lines 55-92 - reads/writes only the athlete's own inventory files.
QD-S-2.3 | PASS | evidence: TC-063 lines 73-76 - plate lines are a closed structure.
QD-S-2.4 | PASS | evidence: TC-063 lines 55-92 - no un-excluded broad verb.
QD-S-3.1 | PASS | evidence: TC-063 line 50 - concrete trigger phrases (equipment changes / `/coach:gym`; non-English triggers paraphrased as translated).
QD-S-3.2 | FAIL | evidence: TC-063 lines 47-92 - no explicit forbidden_when / deactivation conditions declared.
QD-S-3.3 | PASS | evidence: TC-063 lines 68-71 - shared-vs-own gym ambiguity resolved by naming affected athletes.
QD-S-3.6 | PASS | evidence: TC-063 lines 49-50 - name/description consistent.
QD-S-4.2 | FAIL | evidence: TC-063 lines 55-92 - no `partial_result_allowed` declaration.
QD-S-4.3 | FAIL | evidence: TC-063 lines 55-92 - no post-failure prohibited behaviors declared.
QD-S-5.1 | PASS | evidence: TC-063 lines 62, 88-90 - writes only the inventory; read/write scope declared.
QD-S-5.3 | PASS | evidence: TC-063 lines 55-92 - operates on local athlete files; no production environment.
QD-S-5.4 | PASS | evidence: TC-063 lines 80-83 - invokes a co-located script, not another Skill.

### Artifact 2 - `skills/plan/SKILL.md` (Skill)
Tier determination: L2 (Medium Risk) - basis: writes plan/log files and delegates to a planner subagent (state-changing, recoverable resource access).
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-063 line 99 - `name: coach-plan`.
QD-S-0.2 | PASS | evidence: TC-063 line 100 - `description` non-empty.
QD-S-0.3 | PASS | evidence: TC-063 lines 98-103 - YAML parses.
QD-S-0.4 | PASS | evidence: TC-063 line 102 - `argument-hint` typed as a string.
QD-S-0.5 | PASS | evidence: TC-063 lines 98-141 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-063 lines 98-103 - front matter + body present.
Baseline passed -> mandatory set (Q6):
QD-S-1.1 | FAIL | evidence: TC-063 lines 105-141 - no input-count/size upper bound declared.
QD-S-1.3 | FAIL | evidence: TC-063 lines 128-141 - delegates to the planner subagent and runs `stats.mjs load`; no retry count, invocation count, or timeout declared.
QD-S-2.1 | PASS | evidence: TC-063 lines 105-141 - no unbounded processing declaration.
QD-S-2.2 | PASS | evidence: TC-063 lines 105-141 - no unterminated-execution wording.
QD-S-3.4 | PASS | evidence: TC-063 lines 112-141 - scope limited to writing the next session; states "this skill creates nothing on its own".
QD-S-4.1 | PASS | evidence: TC-063 lines 117-121, 133 - stale-plan handling (Log/Drop/Move) and a missing-input loop are declared.
Recommended set (14, P1):
QD-S-1.2 | FAIL | evidence: TC-063 lines 105-141 - no output-size bound declared.
QD-S-1.4 | PASS | evidence: TC-063 lines 135-141 - writes the plan/log files only; no destructive scope.
QD-S-1.5 | PASS | evidence: TC-063 lines 105-126 - reads only the athlete's own program/inventory/history.
QD-S-2.3 | PASS | evidence: TC-063 lines 117-126 - stale-plan handling is a closed three-choice set.
QD-S-2.4 | PASS | evidence: TC-063 lines 105-141 - no un-excluded broad verb.
QD-S-3.1 | PASS | evidence: TC-063 line 100 - concrete trigger phrases (`/coach:plan`; non-English triggers paraphrased as translated).
QD-S-3.2 | FAIL | evidence: TC-063 lines 98-141 - no explicit forbidden_when / deactivation conditions declared.
QD-S-3.3 | PASS | evidence: TC-063 lines 117-121, 133 - stale/missing inputs handled explicitly.
QD-S-3.6 | PASS | evidence: TC-063 lines 99-100 - name/description consistent.
QD-S-4.2 | FAIL | evidence: TC-063 lines 105-141 - no `partial_result_allowed` declaration.
QD-S-4.3 | FAIL | evidence: TC-063 lines 105-141 - no post-failure prohibited behaviors declared.
QD-S-5.1 | PASS | evidence: TC-063 lines 135-141 - no destructive data scope.
QD-S-5.3 | PASS | evidence: TC-063 lines 105-141 - operates on local athlete files; no production environment.
QD-S-5.4 | FAIL | evidence: TC-063 line 130 - delegates to `subagent_type: coach:planner` with no declared permitted/prohibited downstream scope.

### Embedded code snippets (QC)
Snippets inspected: the `stats.mjs` invocation blocks (TC-063 lines 80-83, 110, 126, 138-140).
QC-0.1 | PASS | evidence: TC-063 lines 81-82, 139 - the `node "..."` commands parse as valid shell.
QC-0.2 | FAIL | evidence: TC-063 lines 80-83 - the code blocks carry no language identifier.
QC-0.3 | PASS | evidence: TC-063 lines 80-140 - the snippets are complete.
QC-1.1 | PASS | evidence: TC-063 lines 82, 139 - no undefined name reference in the snippets.
QC-1.2 | PASS | evidence: TC-063 lines 80-140 - no invalid import.
QC-1.3 | PASS | evidence: TC-063 lines 80-140 - no deprecated API usage.
QC-1.4 | PASS | evidence: TC-063 lines 80-140 - no type mismatch.
QC-2.1 | PASS | evidence: TC-063 lines 80-140 - no file handle opened.
QC-2.2 | PASS | evidence: TC-063 lines 80-140 - no network connection opened.
QC-2.3 | PASS | evidence: TC-063 lines 80-140 - no unguarded high-risk operation shown.
QC-3.1 | PASS | evidence: TC-063 lines 80-140 - no unused import.
QC-3.2 | PASS | evidence: TC-063 lines 80-140 - no missing import.
QC-3.3 | PASS | evidence: TC-063 lines 80-140 - no hardcoded demo credential.

## Stage B - Cross-artifact inspection
Not Executed - fewer than two same-agent artifact types present (both provided artifacts are Skill).

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 4 unfixed Stage A P0 carried forward.
- G0-2: informational only - Stage B not executed.
- G0-3: satisfied - responsibility statements locatable (TC-063 lines 49-50, 99-100).
- G0-4: not applicable - no Tool Schema artifact present.
Gate-0 result: Passed.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed - incomplete artifact set (no System Prompt and no Tool Schema for the same agent).

## Stage E - Risk Explicit (EX)
Executed. 0 explicit risk items discovered. The Skills declare safety/confirmation boundaries (e.g. "wait for a yes before writing the file", TC-063 line 79), which are mitigations, not risk expressions. Risk Implicit was NOT run; dynamic exploitability is unverified.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-S-1.1 / QD-S-1.3 (resource/execution bound missing, P0) - candidate attack surface: AS-06; potential impact: Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-10.
- QD-S-5.4 (chained invocation permissions undeclared, P1) - candidate attack surface: AS-04, AS-05, AS-07; potential impact: D1, D2, D3; strength: Conditional, provisional (lite); FM: FM-05, FM-09.
- QD-S-3.2 / QD-S-1.2 (P1) - candidate attack surface: AS-01, AS-06; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite).
- QD-S-4.2 / QD-S-4.3 (failure expansion, P1) - candidate attack surface: AS-07; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-09.
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. Risk Implicit and Runtime Quality subsets were NOT run; per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent.

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(In-place self-correction: the non-English (Cyrillic) trigger phrases inside both front-matter descriptions were rendered as English paraphrases marked "(translated)", per the CJK/non-ASCII zero-tolerance rule.)

## Status board
Stage A (Single-artifact):  Executed - two Skill artifacts at L2 + embedded-snippet QC
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present
Stage C (Gate-0):           Passed
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 risk items
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
