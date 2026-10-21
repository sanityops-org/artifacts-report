# Comparison - TC-004 Inspection Reports Across Skill Versions (2026-10-20)

Comparison date: 2026-10-20
Input artifact: `TC-004-gpt-researcher-multi-agent-suite.md` (SHA256 `849CE90C9919C9A9B1940ACE142350CC3B398191DD1F31CEDFD4365886B49904`, identical in `report-onlybyLLM/` and `test-cases/agent-suite/`)
Report A (previous skill version): [TC-004 ... sanityops-skill-report.md](file:///d:/My%20Docunments/AI/artifacts-report/report-onlybyLLM/TC-004-gpt-researcher-multi-agent-suite.sanityops-skill-report.md) - 2026-10-14
Report B (current skill version): [TC-004 ... sanityops-skill-report-2026-10-20.md](file:///d:/My%20Docunments/AI/artifacts-report/report-onlybyLLM/TC-004-gpt-researcher-multi-agent-suite.sanityops-skill-report-2026-10-20.md) - 2026-10-20

Because the inspected file is byte-identical in both runs, every difference below is attributable to the skill package, not to an artifact change.

---

## 1. Bottom line

| Item | Report A (previous) | Report B (current) | Delta |
|---|---|---|---|
| Fidelity gate | Not applied (no tier declared) | `summary` per object; absence-based rules skipped | New gate |
| Inspect findings | 53 (P0 37 / P1 11 / P2 5) | 3 (P0 2 / P1 1 / P2 0) | -50 |
| Retained findings | - | 3 (two P0, one P1) | See section 4.1 |
| Risk Explicit items | 0 | 1 (`Explicit·P1`) | +1 |
| Gate-0 | Not passed - G0-4 | Not passed - G0-4 | Same |
| Stage D Permission | Not Executed | Not Executed | Same |
| Stage A prompt scope | L3, 47 items claimed | AC-L3, contradiction-based subset | Narrowed |
| Stage B severity model | AC-L3 used to upgrade P1 to P0 | OR-L used for severity; no OR-L3 exists | Corrected |
| Stage G depth | One-line statement | ID back-closure, tier audit, N/A basis, upgrade audit, reconciliation | Expanded |
| Numeric score | Not emitted | Not emitted | Same |

The headline is not "fewer defects were found". The artifact did not change. Report B applies the new fidelity gate: the case self-declares itself as a documentation summary, so only contradiction-based findings are in scope. Most of Report A's findings are absence-based and were correctly withheld.

---

## 2. Method differences that drive the delta

| Method element | Report A | Report B |
|---|---|---|
| Fidelity classification (Step 0) | Absent; summary objects treated as full artifacts | `summary` under S1 + S2 + S3; scope consequence applied |
| Rule scope | Full tier matrices (L1/L2/L3) regardless of object fidelity | Contradiction-based rules only |
| Agent tier | "L3 Complex Agent", "47 items" | AC-L3; suite morphology AC-L4 inspected as AC-L3; 44-item tier cited |
| Tool tier | OR-L1 / OR-L1 / OR-L2; cited "7/7/12-item" sets | OR-L1 / OR-L1 / OR-L2; cites the actual 20/20/25-item sets |
| Severity binding | Mixed AC-L into severity ("Agent L3 -> global P1-to-P0") | AC-L for applicability, OR-L for severity; no OR-L3 element, no upgrade |
| Non-blocking flow | P0 carried forward (already non-blocking) | Same, plus explicit Gate-0 informational handling for G0-1/G0-2 |
| Risk Explicit | Ran, 0 items | Ran, 1 item |
| QC | Ran baseline + pattern rules | Ran baseline; absence rules skipped; QC-1.2/1.3 Not Executed for missing inputs |
| Self-verification | One line | In-line plus closing reconciliation and tier audit |

---

## 3. Stage-by-stage comparison

| Stage | Report A | Report B | Assessment |
|---|---|---|---|
| A - Prompt | 26 FAILs (including 3 ungraded items, 1 deleted ID, 1 deprecated ID) | 1 FAIL (`QD-P-1.1.3`); 9 contradiction rules verdicts; absence rules listed as not run | B is method-correct for a summary object; A over-inspected |
| A - Tools | 19 FAILs across 3 sets (`QD-T-1.1/1.2/1.4/2.1/2.3/3.1/3.2/4.1/4.2`) | 0 FAILs on internal-consistency items (`QD-T-1.3/1.5/1.6/3.4/3.6`); absence rules not run | A's findings are true gaps in the excerpt but out of scope at summary fidelity |
| A - QC | 2 FAILs (`QC-0.3`, `QC-3.2`) | Both skipped (absence-based and illustrative-snippet exemption) | B applies the illustrative-snippet rule; A did not |
| B - Cross | 6 FAILs; severity upgraded by AC-L3 | 2 FAILs (`QD-PT-2.1` P0, `QD-CYC-1.2` P1) | Same core contract breach; severity model corrected |
| C - Gate-0 | G0-3 pass, G0-4 fail | G0-3 pass, G0-4 fail | Agreement |
| D - Permission | Not Executed | Not Executed (only the normative block emitted) | Agreement; B keeps the output to the required block |
| E - Risk Explicit | 0 items | 1 item (`NL-A-4`, `Explicit·P1`) | B detects what A missed on identical text |
| F - Impact | One large table; some rows map IDs without a dedicated source row | Three condensed Impact Cards with strength, status, and mandatory not-run statements | B follows the current Stage F contract |
| G - Self-verification | One-line statement | Full closing checks plus reconciliation notes | Expanded per current skill |

---

## 4. Finding-level comparison

### 4.1 Findings retained in both reports

| Rule | Report A | Report B | Note |
|---|---|---|---|
| `QD-P-1.1.3` | FAIL P0 | FAIL P0 | Same Reviewer threshold/example conflict |
| `QD-PT-2.1` | FAIL P0 (Chief Editor tools only) | FAIL P0 (Chief Editor + Researcher + Publisher HTML) | B widens the evidence within the same fact |
| `QD-CYC-1.2` | FAIL P0 (upgraded via AC-L3) | FAIL P1 (conditional loop, no OR-L3) | Existence agreed; severity corrected |
| Gate-0 `G0-4` | Fail | Fail | Same reason: tool/parameter descriptions incomplete |
| Stage D | Not Executed | Not Executed | Same structural outcome |

### 4.2 Findings withheld in Report B (50 findings)

| Class | Representative IDs | Count (approx.) | Why withheld |
|---|---|---|---|
| Absence-based | `QD-P-2.5.2`, `QD-P-2.6.1`, `QD-T-1.1`, `QD-T-2.1`, `QD-T-3.2`, `QD-PT-2.5`, `QC-0.3` | 42 | The excerpt does not claim the declaration exists; summary fidelity skips absence findings |
| Ambiguity-based, not contradiction | `QD-P-1.3.2`, `QD-P-1.6.1`, `QD-P-2.1.2` | 3 | Vague wording, not a written conflict |
| Ungraded recommendation items | `QD-P-2.7.1`, `QD-P-2.7.2`, `QD-P-2.7.3` | 3 | Recommendation items carry no P grade and are never scored |
| Deleted ID | `QD-P-2.3.3` | 1 | Removed from the current checklist |
| Deprecated ID | `QD-P-2.5.5` | 1 | Deprecated; folded into cross `QD-PT-2.6` / `QD-ST-3.4` |
| Tombstone duplicate | `QD-T-4.2` | 1 | Merged into `QD-T-3.1`; charging both double-counts one fact |

Classes overlap (for example `QD-P-2.3.3` is both deleted and absence-based), so the counts are not additive. No withheld finding asserts a contradiction inside the excerpt.

### 4.3 Findings added in Report B

- `EX` `NL-A-4`: Human prompt "Default approval after 24 hours", corroborated by `"include_human_feedback": false` in section 3.1, graded `Explicit·P1·unconditional` (D2, D3).
- `QD-PT-2.1` evidence expanded to the Researcher tool names (`conduct_research`, `write_draft`) and the Publisher HTML export.
- Stage G reconciliation notes: fidelity scope decision, ID-hygiene decision, and reference-governance note.

---

## 5. Defects in Report A that are independent of the fidelity question

These are method errors, not merely scope differences:

1. Item-count errors: "L3 scope = 47 items" (the prompt checklist states 44); tool sets described as "7/7/12-item" minimal sets (actual `OR-L1` = 20, `OR-L2` = 25).
2. Deleted or deprecated IDs emitted as live verdicts: `QD-P-2.1.1`, `QD-P-2.1.3`, `QD-P-2.1.4`, `QD-P-1.4.2`, `QD-P-2.3.3`, `QD-P-2.5.5`, `QD-T-4.2`.
3. Ungraded recommendation items graded as defects: `QD-P-2.7.1`-`QD-P-2.7.3`.
4. Tombstone double charge: `QD-T-3.1` and `QD-T-4.2` both FAIL on the same undeclared write side effect.
5. Severity model mix: an AC-L3-keyed "global P1-to-P0, P2-to-P1" upgrade. AC-L determines applicability; severity must follow OR-L. With no OR-L3 element, `QD-CYC-1.2` stays P1, `QD-PT-2.3` stays P1, `QD-PT-2.6` stays P2.
6. Risk Explicit false negative: 0 items on the same text that explicitly declares a timeout default approval and disables human feedback.
7. Grade-prefix formatting: `Explicit.P0` instead of the mandated `Explicit·P0` domain prefix.
8. Header incompleteness: no fidelity tier; baseline labeled "September 2026" instead of the package's "2026-10 revision".

---

## 6. What both reports agree on

- The only concrete cross-artifact contract breach is the declared tool surface versus the provided tool schemas.
- The Reviewer output example conflicts with its own threshold rule.
- Gate-0 fails at G0-4; Permission therefore did not execute.
- The suite has no Skill artifact, so Prompt-Skill, Skill-Tool, and Skill-Skill checks are N/A.
- Tool risk tiers are `OR-L1`, `OR-L1`, `OR-L2`; no OR-L3 upgrade applies.
- Risk Implicit, runtime Quality, and permission enforcement were not evaluated.
- No numeric score was requested or emitted.

---

## 7. Which report to use

- Use Report B as the compliance verdict for TC-004 in its current `summary` form. It is scope-correct, ID-correct, and severity-correct.
- Keep Report A as a gap inventory, not as a defect verdict. Its absence findings point at what the excerpt does not prove (tool descriptions, input/output contracts, termination, permission boundaries, error handling). They are useful as a collection checklist for the upstream `multi_agents/` source.
- To turn any Report A absence finding into a valid finding, re-collect the artifact at `full` fidelity (verbatim files from the upstream repository) and re-run; the fidelity gate, not a re-reading of the same summary, is what unlocks those rules.

---

## 8. Residual caveats

- Report B's PASS verdicts mean "no contradiction is visible in the excerpt", not "the artifact is complete or correct".
- The delta of -50 findings measures method strictness, not a quality improvement of the artifact.
- Report A's 53 findings should not be quoted as the TC-004 defect count without the fidelity qualifier.
- The current skill package still has one internal inconsistency: `references/relevance-map.md` says Risk Explicit was not run, while `SKILL.md` Stage E/F runs it. Report B follows `SKILL.md` and records the conflict in Stage G.
