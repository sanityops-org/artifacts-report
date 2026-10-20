# SanityOps Inspect-Lite Report - TC-057-baoyu-skills-file-based-agents.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: `skills/baoyu-cover-image/SKILL.md` - type = Skill. Basis: markdown SKILL.md with YAML front matter (`name: baoyu-cover-image`, `description:`, `version:`) (TC-057 lines 54-62).
- Artifact 2: `skills/baoyu-post-to-wechat/SKILL.md` - type = Skill. Basis: markdown SKILL.md with YAML front matter (`name: baoyu-post-to-wechat`, `description:`, `version:`, `metadata.requires`) (TC-057 lines 107-119).
- TypeScript helper files under `scripts/` are referenced scripts, not logic artifacts (treated as referenced files).
- No JSON/function-calling Tool Schema and no standalone System Prompt file are provided; both provided files are Skill.
- Same-agent scope: both files belong to the same agent suite ("baoyu-skills").

## Executive Summary
- Stages executed: A (two Skills; L2 + L3), B (Not Executed), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts (Stage A): P0 = 18, P1 = 6, P2 = 0.
- Gate-0 result: Passed (G0-3 satisfied; G0-4 not applicable - no Tool Schema). G0-1 informational (18 unfixed P0 carried forward).
- Risk-Explicit summary: Executed, 0 explicit risk items.
- Top findings:
  - QD-S-5.2 - no high-risk confirmation declared for an irreversible external publish (`baoyu-post-to-wechat`).
  - QD-S-5.1 - read/write/delete scopes not distinguished though the Skill writes to an external platform.
  - QD-S-3.4 - no `non_goals` declared in either Skill.
  - QD-S-4.1 - no execution-failure behavior declared.
  - QD-S-1.1 - no input-count/size bound declared.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - `skills/baoyu-cover-image/SKILL.md` (Skill)
Tier determination: L2 (Medium Risk) - basis: external image-generation backend call and file writes (recoverable).
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-057 line 56 - `name: baoyu-cover-image`.
QD-S-0.2 | PASS | evidence: TC-057 line 57 - `description` non-empty.
QD-S-0.3 | PASS | evidence: TC-057 lines 55-62 - YAML parses.
QD-S-0.4 | PASS | evidence: TC-057 lines 58-61 - `version`/`metadata` typed as expected.
QD-S-0.5 | PASS | evidence: TC-057 lines 55-103 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-057 lines 55-62 - front matter + body present.
Baseline passed -> mandatory set (Q6):
QD-S-1.1 | FAIL | evidence: TC-057 lines 63-103 - no `max_items`/input-size upper bound declared.
QD-S-1.3 | FAIL | evidence: TC-057 lines 82-103 - Step 4 "Generate image" invokes a backend tool; no retry count, invocation count, or timeout declared.
QD-S-2.1 | PASS | evidence: TC-057 lines 72-81 - dimensions are closed enumerations; no unbounded processing.
QD-S-2.2 | PASS | evidence: TC-057 lines 63-103 - no "keep trying"/"until success" wording.
QD-S-3.4 | FAIL | evidence: TC-057 lines 63-103 - no `non_goals` statement of what the Skill does not do.
QD-S-4.1 | FAIL | evidence: TC-057 lines 65-70 - the only fallback is for a missing user-input tool, not for execution failure; no failure behavior declared for generation.
Recommended set (14, P1):
QD-S-1.2 | FAIL | evidence: TC-057 lines 82-103 - no output-size bound declared.
QD-S-1.4 | PASS | evidence: TC-057 lines 82-103 - no destructive scope; writes image files only.
QD-S-1.5 | PASS | evidence: TC-057 lines 94-103 - inputs limited to content/preferences declarations.
QD-S-2.3 | PASS | evidence: TC-057 lines 72-81 - dimension tables are closed.
QD-S-2.4 | PASS | evidence: TC-057 lines 63-103 - no un-excluded broad verb.
QD-S-3.1 | PASS | evidence: TC-057 line 57 - trigger phrases: "generate cover image", "create article cover", "make cover".
QD-S-3.2 | FAIL | evidence: TC-057 lines 55-103 - no deactivation / do-not-trigger conditions.
QD-S-3.3 | PASS | evidence: TC-057 lines 65-70 - if no user-input tool exists, a numbered plain-text prompt is used.
QD-S-3.6 | PASS | evidence: TC-057 lines 56-57 - name/description consistent.
QD-S-4.2 | FAIL | evidence: TC-057 lines 82-103 - no `partial_result_allowed` declaration.
QD-S-4.3 | FAIL | evidence: TC-057 lines 82-103 - no post-failure prohibited behaviors declared.
QD-S-5.1 | PASS | evidence: TC-057 lines 82-103 - no data read/modify/delete scope.
QD-S-5.3 | PASS | evidence: TC-057 lines 82-103 - no production environment operations.
QD-S-5.4 | FAIL | evidence: TC-057 lines 60-61, 101-103 - backend resolution chains to a non-native backend skill (`baoyu-image-gen`) with no declared downstream-skill whitelist.

### Artifact 2 - `skills/baoyu-post-to-wechat/SKILL.md` (Skill)
Tier determination: L3 (High Risk) - basis: external publishing to a public platform (irreversible external publish) with API credentials; per skill-checklist risk-level semantics.
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-057 line 109 - `name: baoyu-post-to-wechat`.
QD-S-0.2 | PASS | evidence: TC-057 line 110 - `description` non-empty.
QD-S-0.3 | PASS | evidence: TC-057 lines 108-119 - YAML parses.
QD-S-0.4 | PASS | evidence: TC-057 lines 111-119 - `version`/`metadata.requires` typed as expected.
QD-S-0.5 | PASS | evidence: TC-057 lines 108-156 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-057 lines 108-119 - front matter + body present.
Baseline passed -> mandatory set (21, L3):
QD-S-1.1 | FAIL | evidence: TC-057 lines 120-143 - no input-count/size upper bound declared.
QD-S-1.2 | FAIL | evidence: TC-057 lines 145-156 - no output-size bound declared.
QD-S-1.3 | FAIL | evidence: TC-057 lines 124-143 - multiple script invocations; no retry count, invocation count, or timeout declared.
QD-S-1.4 | FAIL | evidence: TC-057 lines 120-143 - write/publish scope declared but read/write/delete permission types are not distinguished.
QD-S-1.5 | FAIL | evidence: TC-057 lines 120-143 - no permitted/prohibited data sources declared.
QD-S-2.1 | PASS | evidence: TC-057 lines 120-156 - enumerations are closed; no unbounded quantity wording.
QD-S-2.2 | PASS | evidence: TC-057 lines 120-156 - no unterminated-execution wording.
QD-S-2.3 | PASS | evidence: TC-057 lines 145-156 - feature table is closed.
QD-S-2.4 | FAIL | evidence: TC-057 line 110 - broad verb "Posts content ... with HTML, markdown, or plain text" with no `non_goals` exclusion.
QD-S-3.1 | PASS | evidence: TC-057 line 110 - concrete trigger phrases ("post to wechat", plus translated Chinese triggers "(translated)").
QD-S-3.2 | FAIL | evidence: TC-057 lines 108-156 - no deactivation / do-not-trigger conditions.
QD-S-3.4 | FAIL | evidence: TC-057 lines 120-156 - no `non_goals` statement.
QD-S-3.5 | FAIL | evidence: TC-057 lines 120-143 - no declared default handling for empty input / format error / insufficient data branches.
QD-S-3.6 | PASS | evidence: TC-057 lines 109-110 - name/description consistent.
QD-S-4.1 | FAIL | evidence: TC-057 lines 120-156 - no execution-failure behavior declared.
QD-S-4.2 | FAIL | evidence: TC-057 lines 120-156 - no `partial_result_allowed` declaration.
QD-S-4.3 | FAIL | evidence: TC-057 lines 120-156 - no post-failure prohibited behaviors declared.
QD-S-5.1 | FAIL | evidence: TC-057 lines 145-156 - the Skill operates on data (publishes/writes) but read/modify/delete permission scopes are not distinguished.
QD-S-5.2 | FAIL | evidence: TC-057 lines 134-143 - article publishing (irreversible external publish) has no declared confirmation mechanism in the quoted workflow.
QD-S-5.3 | FAIL | evidence: TC-057 lines 120-156 - no operational-environment declaration / production-account boundary.
QD-S-5.4 | PASS | evidence: TC-057 lines 124-132 - invokes co-located scripts, not other Skills; no downstream-skill chaining declared.

### Embedded code snippets (QC)
Not applicable - no executable code snippet is embedded in the inspected excerpts (the ```markdown``` blocks are skill text, not code).

## Stage B - Cross-artifact inspection
Not Executed - fewer than two same-agent artifact types present (both provided artifacts are Skill).

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 18 unfixed Stage A P0 carried forward.
- G0-2: informational only - Stage B not executed.
- G0-3: satisfied - responsibility statements locatable (TC-057 lines 56-57, 109-110).
- G0-4: not applicable - no Tool Schema artifact present.
Gate-0 result: Passed.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed - incomplete artifact set (no System Prompt and no Tool Schema for the same agent).

## Stage E - Risk Explicit (EX)
Executed. 0 explicit risk items discovered. Credentials are declared as handled outside the skill file (TC-057 lines 182-183), which is a mitigation, not a risk expression. Risk Implicit was NOT run; dynamic exploitability is unverified.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-S-5.2 (high-risk confirmation missing, P0) - candidate attack surface: AS-05 Tool Misuse and High-Risk Side Effects (relevance-map.md A.2); potential impact: D2, D3; strength: Strong, provisional (lite); FM: FM-05, FM-09 (category "Skill permission and environment boundary defects").
- QD-S-5.1 / QD-S-5.3 (P0) - candidate attack surface: AS-04, AS-05; potential impact: D2, D3; strength: Medium, provisional (lite); FM: FM-05, FM-09.
- QD-S-1.1 / QD-S-1.3 (P0) - candidate attack surface: AS-06; potential impact: Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-10 ("Skill resource or unbounded declaration defects").
- QD-S-3.4 / QD-S-2.4 (P0) - candidate attack surface: AS-01, AS-05; potential impact: D2, D3; strength: Medium, provisional (lite); FM: FM-02, FM-07, FM-09.
- QD-S-4.1 / QD-S-4.2 / QD-S-4.3 (P0/P1) - candidate attack surface: AS-07; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-09.
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. Risk Implicit (runtime) and Runtime Quality subsets were NOT run; per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent.

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(In-place self-correction: the two Chinese trigger phrases in the `baoyu-post-to-wechat` description were rendered as an English translation marked "(translated)", per the CJK zero-tolerance rule.)

## Status board
Stage A (Single-artifact):  Executed - two Skill artifacts (L2 and L3)
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present
Stage C (Gate-0):           Passed
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 risk items
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
