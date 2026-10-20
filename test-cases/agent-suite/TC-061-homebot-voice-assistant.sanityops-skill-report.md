# SanityOps Inspect-Lite Report - TC-061-homebot-voice-assistant.md

## Provenance
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)

## Artifact Inventory (Input preparation, not a Stage)
- Artifact 1: `mijia` skill manifest (`docs/skills/mijia.md` / generated `SKILL.md`) - type = Skill. Basis: markdown SKILL.md manifest with YAML frontmatter (metadata/requires/platforms/always) parsed by the loader (TC-061 lines 96-115); content is a translated summary (source doc is Chinese).
- Artifact 2: `weather` skill manifest (`docs/skills/weather.md`) - type = Skill. Basis: same; content is a translated summary (source doc is Chinese).
- The skills loader `homebot/agent/skills.py` is a Python source file -> treated as a referenced script, not a logic artifact (input-preparation rule).
- No JSON/function-calling Tool Schema and no standalone System Prompt file are provided; both provided manifest artifacts are Skill.
- Same-agent scope: both manifests belong to the same agent ("homebot").

## Executive Summary
- Stages executed: A (two Skills; L2 + L1; plus embedded-snippet QC), B (Not Executed), C (Gate-0), D (Not Executed), E (Risk Explicit), F (Impact outlook, advisory), G (self-verification).
- P0/P1/P2 counts (Stage A): P0 = 5, P1 = 12, P2 = 1.
- Gate-0 result: Passed (G0-3 satisfied; G0-4 not applicable - no Tool Schema). G0-1 informational (5 unfixed P0 carried forward).
- Risk-Explicit summary: Executed, 1 item - EX NR-S-9, Explicit-P2 (placeholder access-token field in a config example).
- Top findings:
  - QD-S-1.1 - no input-size/number bound declared (both Skills).
  - QD-S-3.4 - no `non_goals` declared in either Skill.
  - QD-S-5.1 - read/write/delete scopes not distinguished for a device-control skill.
  - QD-S-4.1 - no execution-failure behavior declared.
  - QD-S-1.3 - executor/home-assistant invocations with no retry count, invocation count, or timeout.
- What was NOT run: Risk Implicit and the runtime Quality subsets were not run.
- Upgrade pointer: for the full inspection use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Single-artifact inspection

### Artifact 1 - `mijia` smart-home Skill
Tier determination: L2 (Medium Risk) - basis: controls real home devices via Home Assistant (state-changing, recoverable) - resource access/write per skill-checklist risk levels.
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-061 lines 96-105 - the loader parses `SKILL.md` frontmatter (a `name` is required for the index).
QD-S-0.2 | PASS | evidence: TC-061 lines 78-92 - the summary index requires a non-empty `description`.
QD-S-0.3 | PASS | evidence: TC-061 lines 113-115 - frontmatter metadata is parsed successfully.
QD-S-0.4 | PASS | evidence: TC-061 lines 97-104 - `requires`/`platforms` typed as expected.
QD-S-0.5 | PASS | evidence: TC-061 lines 134-181 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-061 lines 134-160 - front matter + body present.
Baseline passed -> mandatory set (Q6):
QD-S-1.1 | FAIL | evidence: TC-061 lines 134-160 - no input-count/size upper bound declared.
QD-S-1.3 | FAIL | evidence: TC-061 lines 149-160 - device control is executed through a driver/Home Assistant; no retry count, invocation count, or timeout declared.
QD-S-2.1 | PASS | evidence: TC-061 lines 159-160 (translated) - "close all the curtains" is bounded by the device inventory; no unbounded processing declared.
QD-S-2.2 | PASS | evidence: TC-061 lines 134-160 - no unterminated-execution wording.
QD-S-3.4 | FAIL | evidence: TC-061 lines 134-160 - no `non_goals` statement.
QD-S-4.1 | FAIL | evidence: TC-061 lines 134-160 - no execution-failure behavior declared.
Recommended set (14, P1):
QD-S-1.2 | FAIL | evidence: TC-061 lines 134-160 - no output-size bound declared.
QD-S-1.4 | FAIL | evidence: TC-061 lines 134-160 - controls devices but read/write/delete permission types are not distinguished.
QD-S-1.5 | FAIL | evidence: TC-061 lines 134-160 - no permitted/prohibited data sources declared.
QD-S-2.3 | PASS | evidence: TC-061 lines 155-160 - the operation vocabulary is closed.
QD-S-2.4 | PASS | evidence: TC-061 lines 134-160 - control scope is bounded by the generated device inventory.
QD-S-3.1 | PASS | evidence: TC-061 lines 159-160 - concrete voice triggers given.
QD-S-3.2 | FAIL | evidence: TC-061 lines 134-160 - no deactivation conditions declared.
QD-S-3.3 | FAIL | evidence: TC-061 lines 134-160 - no ambiguous/incomplete input handling declared.
QD-S-3.6 | PASS | evidence: TC-061 lines 134-160 - name/description consistent with a device-control skill.
QD-S-4.2 | FAIL | evidence: TC-061 lines 134-160 - no `partial_result_allowed` declaration.
QD-S-4.3 | FAIL | evidence: TC-061 lines 134-160 - no post-failure prohibited behaviors declared.
QD-S-5.1 | FAIL | evidence: TC-061 lines 134-160 - the Skill operates on devices but read/modify/delete scopes are not distinguished.
QD-S-5.3 | FAIL | evidence: TC-061 lines 134-160 - no operational-environment declaration for the real home devices.
QD-S-5.4 | PASS | evidence: TC-061 lines 149-155 - uses a co-located driver, does not chain other Skills.

### Artifact 2 - `weather` Skill
Tier determination: L1 (Low Risk) - basis: read-only information lookup via a public endpoint; no state change (skill-checklist risk levels).
Baseline (QD-S-0, run first):
QD-S-0.1 | PASS | evidence: TC-061 lines 96-105 - loader-parsed `SKILL.md` frontmatter requires a `name`.
QD-S-0.2 | PASS | evidence: TC-061 lines 78-92 - non-empty `description` required by the index.
QD-S-0.3 | PASS | evidence: TC-061 lines 113-115 - frontmatter parses.
QD-S-0.4 | PASS | evidence: TC-061 lines 97-104 - `requires`/`platforms` typed as expected.
QD-S-0.5 | PASS | evidence: TC-061 lines 162-181 - no contradictory declarations found.
QD-S-0.6 | PASS | evidence: TC-061 lines 162-172 - front matter + body present.
Baseline passed -> mandatory set (L1, 6 items):
QD-S-1.1 | FAIL | evidence: TC-061 lines 169-180 - no input-count/size upper bound declared.
QD-S-1.2 | FAIL | evidence: TC-061 lines 169-180 - no output-size upper bound declared.
QD-S-2.1 | PASS | evidence: TC-061 lines 176-177 - the `curl` command is bounded by the requested city/time range.
QD-S-3.4 | FAIL | evidence: TC-061 lines 162-180 - no `non_goals` statement.
QD-S-4.1 | FAIL | evidence: TC-061 lines 162-180 - no execution-failure behavior declared (e.g. endpoint unreachable).
QD-S-3.6 | PASS | evidence: TC-061 lines 162-172 - name/description consistent.
Optional items (recommended, not required):
QD-S-3.1 | PASS | evidence: TC-061 lines 169 - concrete usage examples ("how's the weather today", etc., translated).
QD-S-3.2 | FAIL | evidence: TC-061 lines 162-180 - no deactivation conditions declared.
QD-S-3.3 | PASS | evidence: TC-061 line 170 (translated) - default city (Guangzhou) declared when no city is specified.

### Embedded code snippets (QC)
Snippet inspected: the weather `curl` block (TC-061 lines 174-177). The Python loader is a referenced script and is out of QC scope (QC inspects embedded snippets only, per code-contract-checklist Sec.1).
QC-0.1 | PASS | evidence: TC-061 lines 175-177 - the `curl` commands parse as valid shell.
QC-0.2 | PASS | evidence: TC-061 line 174 - code block carries the ```bash``` identifier.
QC-0.3 | PASS | evidence: TC-061 lines 174-177 - the snippet is complete.
QC-1.1 | PASS | evidence: TC-061 lines 175-177 - no undefined name reference.
QC-1.2 | PASS | evidence: TC-061 lines 175-177 - no invalid import.
QC-1.3 | PASS | evidence: TC-061 lines 175-177 - no deprecated API usage.
QC-1.4 | PASS | evidence: TC-061 lines 175-177 - no type mismatch.
QC-2.1 | PASS | evidence: TC-061 lines 174-177 - no file handle opened.
QC-2.2 | PASS | evidence: TC-061 lines 175-177 - one-shot `curl`; no unreleased connection.
QC-2.3 | PASS | evidence: TC-061 lines 175-177 - no unguarded high-risk operation in the snippet.
QC-3.1 | PASS | evidence: TC-061 lines 174-177 - no unused import.
QC-3.2 | PASS | evidence: TC-061 lines 174-177 - no missing import.
QC-3.3 | PASS | evidence: TC-061 lines 174-177 - no hardcoded demo credential.

## Stage B - Cross-artifact inspection
Not Executed - fewer than two same-agent artifact types present (both provided manifest artifacts are Skill).

## Stage C - Gate-0
- G0-1: informational only (non-blocking), 5 unfixed Stage A P0 carried forward.
- G0-2: informational only - Stage B not executed.
- G0-3: satisfied - responsibility statements locatable (TC-061 lines 134-160, 162-172).
- G0-4: not applicable - no Tool Schema artifact present.
Gate-0 result: Passed.

## Stage D - Permission (QD-PM Quick Mode)
Not Executed - incomplete artifact set (no System Prompt and no Tool Schema for the same agent).

## Stage E - Risk Explicit (EX)
Executed. 1 explicit risk item discovered (static-document risk, not a confirmed runtime exploit).

EX NR-S-9 | risk expression: `"access_token": "<long-lived access token>"` (placeholder access-token field in the Mi Home `config.json` example inside the skill doc, TC-061 lines 141-146) | impact type labels: D3 | Explicit-P2 | trigger: unconditional | disposition: record in risk ledger (placeholder value; the doc also warns the token must not be committed, which is a mitigation).

Risk Implicit was NOT run; dynamic exploitability is unverified. This is a Risk-Explicit grade, never a security conclusion.

## Stage F - Impact outlook (candidate mapping, advisory only)
Physically separated from the stage verdicts above. Single-defect mapping only.
- QD-S-1.1 / QD-S-1.3 (resource/execution bound missing, P0) - candidate attack surface: AS-06; potential impact: Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-10.
- QD-S-3.4 (task scope not defined, P0) - candidate attack surface: AS-01, AS-05; potential impact: D2, D3; strength: Medium, provisional (lite); FM: FM-02, FM-07, FM-09.
- QD-S-5.1 / QD-S-1.4 / QD-S-5.3 (permission/environment boundary missing, P1) - candidate attack surface: AS-04, AS-05; potential impact: D2, D3; strength: Conditional, provisional (lite); FM: FM-05, FM-09.
- QD-S-4.1 / QD-S-4.2 / QD-S-4.3 (failure expansion, P0/P1) - candidate attack surface: AS-07; potential impact: D1, D2, D3, Availability; strength: Conditional, provisional (lite); FM: FM-08, FM-09.
- Note: candidate associations only ("may", "needs dynamic verification"); no causal claim. NR-S-9 was detected statically; whether the token is exploitable at runtime is unverified (Risk Implicit NOT run). Per relevance.md Sec.1.4 no assumption is made that compensating controls outside the artifacts are absent.

## Stage G - Self-verification
Self-verification: ID back-closure OK - red-line wording OK - output contract OK.
(In-place self-correction: Chinese source text in both skill docs was rendered as English translations marked "(translated)" and the Chinese city-name examples were paraphrased, per the CJK zero-tolerance rule.)

## Status board
Stage A (Single-artifact):  Executed - two Skill artifacts (L2 and L1) + embedded-snippet QC
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present
Stage C (Gate-0):           Passed
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 1 item (Explicit-P2)
Stage F (Impact outlook):   Executed - mapped defects (advisory)
Stage G (Self-verification): Executed - report self-check passed
