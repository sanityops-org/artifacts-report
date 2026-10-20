# SanityOps Inspect-Lite Report - TC-018-browser-use-system-prompt.md

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label; Collection Date: 2026-10-12)

## 1. Executive Summary

- Executed stages: Stage A (single-artifact System Prompt inspection, QD-P, plus embedded-code QC on the JSON output template), Stage C (Gate-0 admission check), Stage E (Risk Explicit), Stage F (Impact outlook), Stage G (self-verification).
- Inspect defect findings (Stage A): P0 = 5, P1 = 1, P2 = 1 (7 FAIL verdicts over 47 applicable L3 rules).
- Gate-0 result: Not passed - G0-4.
- Risk-Explicit summary: Explicit-P0 = 1, Explicit-P1 = 0, Explicit-P2 = 0 (1 explicitly declared risk item).
- Top findings (up to five, rule ID - one-line defect):
  - QD-P-2.5.2 - No security boundary constraints (prohibited operations / sensitive-data boundaries) are declared.
  - QD-P-2.3.4 - No security/privacy filtering mechanism is declared.
  - QD-P-2.5.3 - No permission control boundaries are declared.
  - QD-P-2.5.5 - No resource invocation frequency limits are declared.
  - QD-P-2.2.4 - Handling of missing/anomalous input is undefined.
- What was NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran inside Stage A.
- Upgrade pointer: for the full inspect ruleset plus Risk and Quality, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md
- This report states no security conclusion and no quality conclusion; Inspect PASS is not Risk PASS and is not Quality PASS.

## 2. Stage A - System Prompt Inspection (QD-P)

Artifact inventory: one file, classified as a System Prompt by structural signature (prose/markdown agent instructions). Note: the case presents an upstream excerpt - the file's own note states the 24 KB upstream source also contains <language_settings>, <user_request>, the full <agent_history>, <browser_vision>, <action_rules>, <efficiency_guidelines>, <reasoning_rules>, <examples>, <error_recovery>, and the remaining <task_completion_rules> and <browser_rules> items. Verdicts below are made against the text as provided; where a declaration is known to live in an omitted upstream section, that is noted.

Tier determination: L3 (Complex Agent). Basis: 4 or more tool/action invocations (navigate, extract, read_file, done, plan_update, search_page, wait), a workflow longer than 5 steps (iterative agent loop), security-sensitive operation (automated browsing and form submission), and a requirement for exception/loop handling - 2 or more of the L3 criteria are satisfied. The L3 tier item set (47 items) is applied; the tier matrix is upward-compatible (L3 covers L2 and L1).

### Part 1 - Logic defects
- QD-P-1.1.1 | PASS | P0 | evidence: TC-018, <browser_rules> / <file_system>; no mutually exclusive directives on one object detected.
- QD-P-1.1.2 | PASS | P0 | evidence: TC-018, <critical_reminders> / <browser_rules>; no unarbitrated competing MUST-directives detected.
- QD-P-1.1.3 | PASS | P0 | evidence: TC-018, <browser_state> examples and <output> JSON; examples are consistent with the stated formats.
- QD-P-1.2.1 | PASS | P0 | evidence: TC-018, intro; role (browser automation agent) matches the stated responsibilities.
- QD-P-1.2.2 | PASS | P1 | evidence: TC-018, <output>; role and structured-JSON style are consistent.
- QD-P-1.2.3 | PASS | P0 | evidence: TC-018, <file_system> "DO NOT use the file system if the task is less than 10 steps!"; limits rather than prohibits the core responsibility.
- QD-P-1.3.1 | PASS | P1 | evidence: TC-018, <critical_reminders>; quantifiers are attached to concrete objects (every requirement, every URL).
- QD-P-1.3.2 | FAIL | P1 | evidence: TC-018, <browser_rules>; excerpt: "if you are on the same URL for 3+ steps without meaningful progress" - the term "meaningful progress" is undefined and governs a loop-break decision.
- QD-P-1.3.3 | PASS | P0 | evidence: TC-018; behavioral boundaries are stated via <browser_rules>.
- QD-P-1.4.1 | FAIL | P2 | evidence: TC-018, <critical_reminders>; the success-verification constraint is duplicated - "ALWAYS verify action success using the screenshot before proceeding" and "NEVER assume success - always verify from screenshot or browser state"; the CAPTCHA statement is also duplicated in <browser_rules> and <critical_reminders>.
- QD-P-1.4.2 | PASS | P2 | evidence: TC-018; no unreachable/dead rule detected in the shown text.
- QD-P-1.4.3 | PASS | P0 | evidence: TC-018; no invalid sub-skill definition detected in the shown text.
- QD-P-1.5.1 | PASS | P0 | evidence: TC-018; responsibilities are sufficient for the completion objective.
- QD-P-1.5.2 | PASS | P0 | evidence: TC-018; workflow-referenced actions are declared by name in <input>/<output>.
- QD-P-1.6.1 | PASS | P0 | evidence: TC-018; no vague term carrying a security/permission decision detected.
- QD-P-1.6.2 | PASS | P0 | evidence: TC-018, <planning>; planning criteria are bounded (1-3 actions / 3-10 items) rather than purely internal-state keyed.
- QD-P-1.6.3 | PASS | P0 | evidence: TC-018; no unarbitrated soft-rule interweaving detected.
- QD-P-1.6.4 | PASS | P1 | evidence: TC-018; no internal reasoning-method constraint imposed.
- QD-P-1.6.5 | PASS | P1 | evidence: TC-018; no self-referential/recursive constraint.
- QD-P-1.6.6 | PASS | P0 | evidence: TC-018; pre-done verification guards the main assumption.
- QD-P-1.6.7 | PASS | P0 | evidence: TC-018; per-step memory update provides a revision channel.

### Part 2 - Completeness/security defects
- QD-P-2.1.1 | PASS | P2 | evidence: TC-018; format is consistent (tagged sections plus JSON output).
- QD-P-2.1.2 | PASS | P1 | evidence: TC-018; referenced actions are named consistently.
- QD-P-2.1.3 | PASS | P2 | evidence: TC-018; section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | P2 | evidence: TC-018; language is reasonably concise.
- QD-P-2.2.1 | PASS | P0 | evidence: TC-018, <input>; six input sources are declared.
- QD-P-2.2.2 | PASS | P0 | evidence: TC-018, <input>/<browser_state>; input element format is described.
- QD-P-2.2.3 | PASS | P0 | evidence: TC-018, <input>; the conditional nature of <read_state> ("only if your previous action was extract or read_file") is distinguished.
- QD-P-2.2.4 | FAIL | P0 | evidence: TC-018; handling of a missing/empty/anomalous <user_request> is not declared (absence confirmed in the shown text).
- QD-P-2.3.1 | PASS | P0 | evidence: TC-018, <output>; output format declared (valid JSON with named fields).
- QD-P-2.3.2 | PASS | P0 | evidence: TC-018, <output>; output schema fields are enumerated.
- QD-P-2.3.3 | PASS | P0 | evidence: TC-018, <pre_done_verification> / <critical_reminders>; consistency-check behavior declared.
- QD-P-2.3.4 | FAIL | P0 | evidence: TC-018; no sensitive-data filtering, privacy handling, or security output constraint declared (absence confirmed).
- QD-P-2.4.1 | PASS | P0 | evidence: TC-018; task-completion and verification steps are defined.
- QD-P-2.4.2 | PASS | P0 | evidence: TC-018; referenced actions/resources are declared by name.
- QD-P-2.4.3 | PASS | P0 | evidence: TC-018, <output>; action invocation format is shown (action_rules exist upstream per the excerpt note).
- QD-P-2.5.1 | PASS | P0 | evidence: TC-018, <task_completion_rules>; termination declared ("reach the final allowed step (max_steps)").
- QD-P-2.5.2 | FAIL | P0 | evidence: TC-018; no prohibited operations, sensitive-data access boundary, or external-system access boundary declared (absence confirmed).
- QD-P-2.5.3 | FAIL | P0 | evidence: TC-018; no Agent permission scope, elevation conditions, or privilege-escalation handling declared (absence confirmed).
- QD-P-2.5.4 | PASS | P0 | evidence: TC-018; no explicit conflict among constraints requiring an arbitration rule was identified.
- QD-P-2.5.5 | FAIL | P0 | evidence: TC-018; no invocation/access frequency limit for browser actions or external systems declared (absence confirmed).
- QD-P-2.6.1 | PASS | P0 | evidence: TC-018; error recovery is addressed in the shown text and exists upstream (<error_recovery> per the excerpt note).
- QD-P-2.6.2 | PASS | P0 | evidence: TC-018; alternative-approach/loop-break guidance is present and <error_recovery> exists upstream.
- QD-P-2.6.3 | PASS | P1 | evidence: TC-018; "NEVER repeat the same failing action more than 2-3 times" bounds retries.
- QD-P-2.7.1 | PASS | P0 | evidence: TC-018; <examples> exists upstream per the excerpt note.
- QD-P-2.7.2 | PASS | P0 | evidence: TC-018; <examples> exists upstream per the excerpt note.
- QD-P-2.7.3 | PASS | P0 | evidence: TC-018; <examples> exists upstream per the excerpt note.

### QC - embedded code (JSON output template)
- QC-0.1 | PASS | P0 | evidence: TC-018, <output> JSON template is structurally valid.
- QC-0.2 | PASS | P1 | evidence: TC-018, the enclosing code block carries a language identifier (markdown).
- QC-0.3 | PASS | P1 | evidence: TC-018, the JSON template is complete (no truncation marker).
- QC-1.1 | PASS | P1 | evidence: TC-018; no undefined name reference in the template.
- QC-1.2 | PASS | P2 | evidence: TC-018; no invalid import.
- QC-1.3 | PASS | P2 | evidence: TC-018; no deprecated API.
- QC-1.4 | PASS | P2 | evidence: TC-018; no type incompatibility.
- QC-2.1 | PASS | P1 | evidence: TC-018; no file handle opened in the template.
- QC-2.2 | PASS | P2 | evidence: TC-018; no network connection opened in the template.
- QC-2.3 | PASS | P2 | evidence: TC-018; no high-risk call in the template.
- QC-3.1 | PASS | P2 | evidence: TC-018; no unused import.
- QC-3.2 | PASS | P1 | evidence: TC-018; no missing import.
- QC-3.3 | PASS | P2 | evidence: TC-018; no hardcoded demo credential/value.

Stage A summary: 47 applicable rules, 7 FAIL (5 P0, 1 P1, 1 P2). P0 findings are carried forward and do not halt the flow.

## 3. Stage B - Cross-Artifact Inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. No cross results are invented.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (no unfixed P0 in Stage A): informational only; 5 P0 findings recorded and carried forward (does not gate in this non-blocking flow).
- G0-2 (no unfixed P0 in Stage B): informational only; Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): the Prompt defines a role and behavioral responsibilities, so a responsibility baseline is locatable.
- G0-4 (each Tool Schema's name, description, and parameter descriptions are complete): unsatisfiable - the artifact set contains no Tool Schema, so no Tool-schema completeness can be verified.

Gate-0 result: Not passed - G0-4 (no Tool Schema present, so per-Tool completion of name/description/parameter descriptions cannot be verified).

## 5. Stage D - Permission Proportionality (QD-PM)

Not Executed - incomplete artifact set (Precondition: full set Prompt + Skill + all Tool Schemas required; only a System Prompt is present).

## 6. Stage E - Risk Explicit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above. It is not a defect verdict and not a security conclusion. Explicit-P0/P1/P2 is a Risk-Explicit assessment, not a confirmed runtime exploit.

Audit object: TC-018 System Prompt. Scan path: NL-A (sentence-by-sentence) -> NL-B (cross-sentence) -> NR-O (decode) -> NR-S (structure/field).

Risk Item Summary
- Total risk items: 1
- Explicit-P0 (Block release): 1 item
- Explicit-P1 (Fix / exemption): 0 items
- Explicit-P2 (Risk ledger): 0 items

Risk Item Details
- EX Classification: NL-A-3 (Intent Declaration)
- Risk Expression: "CAPTCHAs are automatically solved by the browser. If blocked by login/403, try alternative approaches."
- Severity Grade: Explicit-P0
- Reason: worst possible consequence is complete bypass of an access control (anti-bot CAPTCHA and login/403 denial) - matches the P0 criterion "security restrictions or permissions bypassed"; static text only.
- Impact Type Labels: D3
- Trigger Condition Label: unconditional (triggered by the environment the agent operates in; not system-mandated verification the attacker cannot satisfy).
- Disposition: Block release (fix or record approved exemption).
- Remediation Suggestion: restrict the declared bypass scope / add an explicit boundary on which access controls may not be circumvented.

Note: Risk Implicit (dynamic exploitability) was NOT run. This is a static-document risk item, not a confirmed exploit.

## 7. Stage F - Impact Outlook (candidate mapping, advisory only)

Advisory context only; this section does not change, soften, or escalate any Inspect verdict. Candidate language only; strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; only Stage E (Risk Explicit) and the Stage A lite embedded-code QC ran. Per relevance.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

| Defect ID (severity) | Candidate AS-* | Candidate FM-* | Candidate RAG metrics | Strength (provisional lite) |
|---|---|---|---|---|
| QD-P-1.3.2 (P1) | AS-01, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Conditional - undefined loop-break term |
| QD-P-1.4.1 (P2) | AS-05, AS-09 | FM-01, FM-02, FM-07, FM-09 | Correctness, Relevance, Consistency, Format Compliance | Conditional - redundant constraint |
| QD-P-2.2.4 (P0) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - missing-input path undefined |
| QD-P-2.3.4 (P0) | AS-03 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Medium - no privacy/sensitive-data output filtering |
| QD-P-2.5.2 (P0) | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Strong - no security boundary constraints declared on a web-acting agent |
| QD-P-2.5.3 (P0) | AS-04, AS-05 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no permission control boundaries declared |
| QD-P-2.5.5 (P0) | AS-06 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no resource invocation frequency limits |

Boundary reminders: candidate associations only ("may", "needs dynamic verification"); no causal claim is made. Single-defect mapping only (v1 scope); defect chains are out of scope.

## 8. Stage G - Self-Verification

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. All emitted QD-P / QC / EX IDs were confirmed against the reference files; no fabricated IDs; no causal wording in Stage F; no "secure"/"high quality" claim; no "Permission = ERROR/BLOCKED" wording. No in-place self-corrections were required.

## 9. Status Board

Stage A (Single-artifact):  Executed - System Prompt L3 inspection + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 1 risk item (Explicit-P0=1, Explicit-P1=0, Explicit-P2=0).
Stage F (Impact outlook):   Executed - candidate mapping for 7 Stage A FAILs (advisory only).
Stage G (Self-verification): Executed - ID back-closure OK, red-line wording OK, output contract OK.
