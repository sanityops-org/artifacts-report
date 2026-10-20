# SanityOps Inspect-Lite: Batch Inspection Summary (100 Reports)

**Summary version:** 1.0
**Generated:** 2026-10-15
**Host models used to author the underlying reports:** DeepSeek V4 Flash; GLM 5.3 Flash (per-report assignment not recorded)
**Framework under test:** SanityOps Framework v1.0 (September 2026)
**Inspector skill:** sanityops-inspect-lite v1.0.0
**Source corpus:** `test-cases/` (100 SanityOps super-skill reports, 4 categories x 25)

> Provenance. This document is a downstream aggregate of 100 independent inspection reports. Every number
> here is derived from the reports' own Executive-Summary counts; the derivation, the counting convention,
> the corrections applied, and the self-checks are stated in Sections 6 and 8. The working data cache and
> the verification logs are retained (Section 9). Companion machine-readable files: `summary-per-tc.csv`,
> `summary-rules.csv`, `summary-ex.csv`.

---

## 1. Scope and Corpus Construction

### 1.1 Object

This summary covers **100 inspection reports** produced by `sanityops-inspect-lite` v1.0.0 over a
four-category slice of a larger 200-case evaluation corpus. Each report inspects one test case (a single
AI-agent artifact or a whole agent suite) against the SanityOps quality-design (QD) rule families and the
embedded-code quality (QC) family, in the seven-stage flow A-G.

Report file pattern: `{name}.sanityops-skill-report.md`.

### 1.2 Categories and coverage

| Category | Directory | Reports | Artifact inspected | Stage B (cross-artifact) |
|---|---|---:|---|---|
| system-prompt (sp) | `single-artifact/system-prompt/` | 25 | a System Prompt | not applicable |
| skill (sk) | `single-artifact/skill/` | 25 | a Skill (SKILL.md) | not applicable |
| tool-schema (ts) | `single-artifact/tool-schema/` | 25 | one or more Tool Schemas | not applicable |
| agent-suite (as) | `agent-suite/` | 25 | Prompt + Skill + Tool Schema set | executed |

Test-case IDs by category:
- **sp:** TC-001, 018, 019, 044-048, 051, 052, 072-077, 078-080, 082, 083, 108-112.
- **sk:** TC-002, 047, 049, 053, 054, 081, 138-156.
- **ts:** TC-003, 050, 182-206.
- **as:** TC-004-006, 031-042, 055-064.

### 1.3 Construction of the underlying reports

Each of the 100 reports was produced by running the lite inspector over one test case. Reports were
authored in at least two layout generations (Section 6.3), which differ in wording and in whether the
Executive-Summary headline prints severities inline, but not in the underlying verdicts. The aggregate here
uses each report's own stated counts, normalised to a single convention (Section 2.1).

### 1.4 What is and is not measured

- **Measured:** per-test-case counts of FAIL verdicts by severity (P0/P1/P2), the set of failed rule IDs,
  Gate-0 admission outcome, risk-tier assignment, and Stage-E Risk-Explicit (EX) items.
- **Not measured / deferred:** the definitions catalogue and the rule-code dictionary are deferred to a
  future attachment (Section 7); no cross-artifact causal claims, no defect-chain analysis (out of the lite
  scope), and no inter-model comparison (per-report model attribution is not recorded).

## 2. Aggregate Results

### 2.1 Counting convention (single normalised metric)

For every test case the reported **P0/P1/P2** are the number of FAIL verdicts at each severity, summed over
all executed quality-design check families for that case (QD-P, QD-S, QD-T, and the cross-artifact families
QD-PT / QD-PS / QD-ST / QD-CYC) **plus** the embedded-code quality family (QC). Stage-E Risk-Explicit (EX)
items are **excluded** from P0/P1/P2 and reported separately (Section 2.4).

Reports are not uniform in how the Executive-Summary headline is composed. Some print a total that already
includes embedded-code QC; others print a QD-only count with a separate positive QC clause. The convention
above is applied uniformly, so a QD-only headline with a non-zero QC clause has its QC verdicts added back.
This normalisation affects exactly one test case materially (TC-046; see Section 8.2, correction C-1).

### 2.2 Totals by category

| Category | Reports | P0 | P1 | P2 | Total FAIL | Mean FAIL / report |
|---|---:|---:|---:|---:|---:|---:|
| system-prompt (sp) | 25 | 171 | 122 | 5 | 298 | 11.9 |
| skill (sk) | 25 | 76 | 101 | 8 | 185 | 7.4 |
| tool-schema (ts) | 25 | 26 | 51 | 52 | 129 | 5.2 |
| agent-suite (as) | 25 | 552 | 292 | 17 | 861 | 34.4 |
| **Total** | **100** | **825** | **566** | **82** | **1473** | **14.7** |

One further finding in the skill category is **unmarked** (no numeric P-count is emitted; TC-139) and is not
assigned to P0/P1/P2; it is carried as `+1 ungraded` in the per-category table (Section 4).

### 2.3 Severity distribution

| Severity | Count | Share of 1473 |
|---|---:|---:|
| P0 (blocking) | 825 | 56.0% |
| P1 (recommended) | 566 | 38.4% |
| P2 (advisory) | 82 | 5.6% |

P0 dominates overall, and is concentrated in the agent-suite category: 552 of the 825 P0 verdicts (66.9%)
come from 25 agent-suite reports. By contrast the tool-schema category is P2-heavy (52 of its 129 verdicts,
40.3% P2), reflecting that lone Tool Schemas most often miss optional parameter constraints rather than
blocking constraints.

### 2.4 Risk-Explicit (EX) items

13 EX items were recorded across **12 test cases** (12% of the corpus). No EX item is folded into the
P0/P1/P2 counts above.

| EX rule | Severity | Test case(s) |
|---|---|---|
| NL-A-1 | P1 | TC-111 |
| NL-A-2 | P2 | TC-034 |
| NL-A-3 | P0 | TC-018 |
| NL-A-3 | P1 | TC-031 |
| NL-A-7 | P0 | TC-033 |
| NL-A-7 | P2 | TC-019, TC-140 |
| NR-S-2 | P1 | TC-194 |
| NR-S-4 | P1 | TC-143 |
| NR-S-9 | P2 | TC-003, TC-032, TC-033, TC-061 |

EX severity mix: 2 x P0, 4 x P1, 7 x P2. The most frequent EX class is NR-S-9 (4 cases). TC-033 carries two
EX items (NL-A-7 and NR-S-9).

### 2.5 Gate-0 outcomes

| Category | Passed | Not passed | Dominant unsatisfied condition |
|---|---:|---:|---|
| system-prompt (sp) | 0 | 25 | G0-4 (no Tool Schema; per-Tool completeness unverifiable) |
| skill (sk) | 0 | 25 | G0-4 (same) |
| tool-schema (ts) | 0 | 25 | G0-3 (lone Tool Schema has no responsibility baseline) |
| agent-suite (as) | 11 | 14 | G0-4 (incomplete artifact set) |
| **Total** | **11** | **89** | |

Overall Gate-0 pass rate = 11/100 (11%). Only the agent-suite category can satisfy Gate-0, and only when the
full same-agent artifact set (Prompt + Skill + Tool Schema) is present; TC-037 and TC-040 additionally
record G0-3. Two Gate-0 labels appear across layout generations (G0-1..G0-4 vs G0-3/G0-4 wording); the
outcome, not the label, is aggregated (Section 6.3).

### 2.6 Risk-tier distribution

| Tier | sp | sk | ts | as | Total |
|---|---:|---:|---:|---:|---:|
| L1 (single-turn / read-only) | 11 | 4 | 21 | 1 | 37 |
| L2 (multi-turn / medium risk) | 6 | 18 | 1 | 11 | 36 |
| L3 (complex agent / high risk) | 8 | 2 | 1 | 13 | 24 |
| mixed (per-tool tiers differ) | 0 | 0 | 2 | 0 | 2 |
| undetermined | 0 | 1 | 0 | 0 | 1 |

Tier notes: tool-schema reports assign a tier per tool, so two reports (TC-184, TC-185) are marked *mixed*.
TC-139 (skill) carries no explicit tier determination. TC-037 (agent-suite) states an artifact-level L3 but
no suite-level determination; it is counted as L3 here (Section 6.3).

## 3. Rule-Level Findings

Across the 100 reports, **106 distinct rule IDs** produced at least one FAIL. The tables below give, per
rule family, the number of FAIL *mentions* in the reports for each rule ID, sorted by descending frequency.
Counts are the raw FAIL-line tally and are indicative frequencies, not exact verdict counts (see 6.3); the
rule IDs are exact. Rule semantics are defined in the deferred dictionary (Section 7).

### 3.1 QD-P family (System Prompt) - 36 rule IDs

| Rule | FAILs | Rule | FAILs | Rule | FAILs |
|---|---:|---|---:|---|---:|
| QD-P-2.7.3 | 41 | QD-P-1.3.3 | 20 | QD-P-1.6.6 | 9 |
| QD-P-2.3.4 | 38 | QD-P-2.6.1 | 19 | QD-P-2.4.1 | 9 |
| QD-P-2.7.2 | 38 | QD-P-2.6.2 | 18 | QD-P-2.6.3 | 7 |
| QD-P-2.5.2 | 37 | QD-P-2.3.2 | 17 | QD-P-1.6.1 | 7 |
| QD-P-2.7.1 | 33 | QD-P-2.5.1 | 16 | QD-P-1.4.1 | 4 |
| QD-P-2.2.4 | 32 | QD-P-2.4.2 | 13 | QD-P-1.6.3 | 3 |
| QD-P-2.2.2 | 25 | QD-P-2.5.4 | 12 | QD-P-1.1.1 | 2 |
| QD-P-2.3.3 | 24 | QD-P-1.5.2 | 12 | QD-P-1.1.3 | 2 |
| QD-P-1.3.2 | 22 | QD-P-2.3.1 | 11 | QD-P-1.6.7 | 2 |
| QD-P-2.5.5 | 22 | QD-P-2.2.1 | 11 | QD-P-1.1.2 | 1 |
| QD-P-2.5.3 | 22 | QD-P-1.6.2 | 10 | QD-P-1.5.1 | 1 |
| QD-P-2.4.3 | 22 | QD-P-1.6.4 | 9 | QD-P-2.1.2 | 1 |

(Some columns show a slightly out-of-order pair where it keeps the three-column layout balanced; the full
sorted order is available in `summary-rules.csv`.)

Top signal: QD-P-2.7.3, 2.3.4, 2.7.2, 2.5.2 and 2.7.1 (all in the 33-41 range) - boundary/termination and
data-handling sub-rules of the prompt family.

### 3.2 QD-S family (Skill) - 25 rule IDs

| Rule | FAILs | Rule | FAILs | Rule | FAILs |
|---|---:|---|---:|---|---:|
| QD-S-4.1 | 33 | QD-S-3.3 | 12 | QD-S-3.1 | 4 |
| QD-S-1.1 | 33 | QD-S-1.5 | 11 | QD-S-2.2 | 1 |
| QD-S-1.3 | 30 | QD-S-2.3 | 7 | QD-S-3.5 | 1 |
| QD-S-3.4 | 26 | QD-S-2.1 | 7 | QD-S-0.2 | 2 |
| QD-S-4.3 | 26 | QD-S-2.4 | 6 | QD-S-0.1 | 1 |
| QD-S-1.2 | 25 | QD-S-5.2 | 5 | QD-S-0.4 | 1 |
| QD-S-3.2 | 23 | | | QD-S-0.6 | 1 |
| QD-S-5.3 | 22 | | | | |
| QD-S-5.1 | 22 | | | | |
| QD-S-1.4 | 22 | | | | |
| QD-S-4.2 | 22 | | | | |
| QD-S-5.4 | 12 | | | | |

Top signal: QD-S-4.1 and 1.1 (33 each) - resource/input boundary declaration - followed by 1.3 (execution
boundary) and 3.4 (non-goals/scope). Note: the QD-S counts for batch-1 skill reports carry a higher
parser-artifact risk (Section 6.3).

### 3.3 QD-T family (Tool Schema) - 16 rule IDs

| Rule | FAILs | Rule | FAILs |
|---|---:|---|---:|
| QD-T-2.1 | 28 | QD-T-3.3 | 6 |
| QD-T-1.4 | 26 | QD-T-3.5 | 4 |
| QD-T-2.3 | 15 | QD-T-2.4 | 3 |
| QD-T-4.2 | 11 | QD-T-2.2 | 3 |
| QD-T-3.1 | 11 | QD-T-1.3 | 1 |
| QD-T-3.2 | 10 | QD-T-3.4 | 1 |
| QD-T-1.1 | 9 | QD-T-4.3 | 1 |
| QD-T-1.2 | 9 | | |
| QD-T-4.1 | 8 | | |

Top signal: QD-T-1.4 (uncontrolled `additionalProperties`) and QD-T-2.1 (parameter constraint missing) -
the two structural gaps reported in essentially every Tool Schema inspected. Tool-schema reports also
assign a severity inline per tool, which is why this family shows a P2-heavy profile (Section 2.3).

### 3.4 Cross-artifact families (agent-suite only) - 19 rule IDs

| Family | Rule: FAILs |
|---|---|
| QD-PT (Prompt-Tool) | 2.3:11, 2.6:10, 2.5:10, 2.2:9, 2.1:6, 2.4:5 |
| QD-PS (Prompt-Skill) | 1.2:7, 1.3:7, 1.4:7, 1.5:6, 1.6:6 |
| QD-ST (Skill-Tool) | 3.2:4, 3.3:4, 3.4:4, 3.5:4, 3.6:4, 3.7:4, 3.1:3 |
| QD-CYC (cycle) | 1.2:1 |

Top signal: QD-PT-2.3 (parameter-constraint consistency) and the PT termination/error-handling sub-rules -
the same boundary themes as the single-artifact families but measured across the prompt/tool contract seam.

### 3.5 QC family (embedded-code quality) - 10 rule IDs

| Rule | FAILs | Rule | FAILs |
|---|---:|---|---:|
| QC-0.3 | 19 | QC-3.1 | 2 |
| QC-1.1 | 10 | QC-1.3 | 1 |
| QC-3.2 | 9 | QC-2.1 | 1 |
| QC-3.3 | 5 | | |
| QC-0.1 | 4 | | |
| QC-0.2 | 3 | | |
| QC-2.3 | 2 | | |

Top signal: QC-0.3 (elided/incomplete code fragments) is the most frequent embedded-code problem, i.e. the
runbook snippets shipped inside the artifacts are most often not self-contained.

## 4. Per-Category Results

Legend: **Gate-0** `NP-G0-4` = Not passed, G0-4; `NP-G0-3` = Not passed, G0-3; `Pass` = Gate-0 Passed.
**EX** lists the Stage-E Risk-Explicit rule(s) recorded for that case (`-` = none). P0/P1/P2 follow the
convention in 2.1.

### 4.1 system-prompt (sp) - 25 reports | P0 171, P1 122, P2 5 (total 298)

| TC | Tier | Gate-0 | P0 | P1 | P2 | EX |
|---|---|---|---:|---:|---:|---|
| TC-001 | L1 | NP-G0-4 | 3 | 8 | 1 | - |
| TC-018 | L3 | NP-G0-4 | 5 | 1 | 1 | NL-A-3 (P0) |
| TC-019 | L1 | NP-G0-4 | 3 | 10 | 1 | NL-A-7 (P2) |
| TC-044 | L2 | NP-G0-4 | 3 | 3 | 0 | - |
| TC-045 | L2 | NP-G0-4 | 4 | 5 | 1 | - |
| TC-046 | L1 | NP-G0-4 | 2 | 10 | 1 | - |
| TC-048 | L2 | NP-G0-4 | 3 | 3 | 0 | - |
| TC-051 | L3 | NP-G0-4 | 11 | 2 | 0 | - |
| TC-052 | L2 | NP-G0-4 | 0 | 2 | 0 | - |
| TC-072 | L1 | NP-G0-4 | 2 | 8 | 0 | - |
| TC-073 | L1 | NP-G0-4 | 2 | 8 | 0 | - |
| TC-074 | L1 | NP-G0-4 | 3 | 7 | 0 | - |
| TC-075 | L1 | NP-G0-4 | 2 | 5 | 0 | - |
| TC-076 | L1 | NP-G0-4 | 2 | 5 | 0 | - |
| TC-077 | L1 | NP-G0-4 | 2 | 6 | 0 | - |
| TC-078 | L3 | NP-G0-4 | 18 | 1 | 0 | - |
| TC-079 | L3 | NP-G0-4 | 18 | 1 | 0 | - |
| TC-080 | L3 | NP-G0-4 | 18 | 1 | 0 | - |
| TC-082 | L3 | NP-G0-4 | 17 | 1 | 0 | - |
| TC-083 | L3 | NP-G0-4 | 18 | 1 | 0 | - |
| TC-108 | L2 | NP-G0-4 | 8 | 10 | 0 | - |
| TC-109 | L2 | NP-G0-4 | 8 | 9 | 0 | - |
| TC-110 | L1 | NP-G0-4 | 2 | 6 | 0 | - |
| TC-111 | L3 | NP-G0-4 | 15 | 3 | 0 | NL-A-1 (P1) |
| TC-112 | L1 | NP-G0-4 | 2 | 6 | 0 | - |

### 4.2 skill (sk) - 25 reports | P0 76, P1 101, P2 8 (total 185) | +1 ungraded (TC-139)

| TC | Tier | Gate-0 | P0 | P1 | P2 | EX |
|---|---|---|---:|---:|---:|---|
| TC-002 | L2 | NP-G0-4 | 5 | 13 | 1 | - |
| TC-047 | L2 | NP-G0-4 | 3 | 8 | 1 | - |
| TC-049 | L2 | NP-G0-4 | 4 | 9 | 0 | - |
| TC-053 | L2 | NP-G0-4 | 4 | 11 | 0 | - |
| TC-054 | L2 | NP-G0-4 | 3 | 6 | 0 | - |
| TC-081 | L2 | NP-G0-4 | 4 | 0 | 0 | - |
| TC-138 | L2 | NP-G0-4 | 3 | 0 | 0 | - |
| TC-139 | n/a | NP-G0-4 | 0 | 0 | 0 | - (+1 ungraded) |
| TC-140 | L2 | NP-G0-4 | 5 | 0 | 0 | NL-A-7 (P2) |
| TC-141 | L1 | NP-G0-4 | 1 | 3 | 0 | - |
| TC-142 | L2 | NP-G0-4 | 0 | 0 | 0 | - |
| TC-143 | L3 | NP-G0-4 | 14 | 1 | 1 | NR-S-4 (P1) |
| TC-144 | L3 | NP-G0-4 | 2 | 0 | 0 | - |
| TC-145 | L2 | NP-G0-4 | 3 | 0 | 0 | - |
| TC-146 | L2 | NP-G0-4 | 4 | 1 | 1 | - |
| TC-147 | L2 | NP-G0-4 | 5 | 10 | 0 | - |
| TC-148 | L2 | NP-G0-4 | 2 | 7 | 0 | - |
| TC-149 | L1 | NP-G0-4 | 0 | 2 | 1 | - |
| TC-150 | L2 | NP-G0-4 | 3 | 3 | 0 | - |
| TC-151 | L1 | NP-G0-4 | 1 | 3 | 0 | - |
| TC-152 | L1 | NP-G0-4 | 1 | 4 | 1 | - |
| TC-153 | L2 | NP-G0-4 | 4 | 9 | 0 | - |
| TC-154 | L2 | NP-G0-4 | 1 | 3 | 1 | - |
| TC-155 | L2 | NP-G0-4 | 2 | 3 | 1 | - |
| TC-156 | L2 | NP-G0-4 | 2 | 5 | 0 | - |

### 4.3 tool-schema (ts) - 25 reports | P0 26, P1 51, P2 52 (total 129)

| TC | Tier | Gate-0 | P0 | P1 | P2 | EX |
|---|---|---|---:|---:|---:|---|
| TC-003 | L3 | NP-G0-3 | 7 | 0 | 2 | NR-S-9 (P2) |
| TC-050 | L1 x2 | NP-G0-3 | 0 | 2 | 4 | - |
| TC-182 | L1 | NP-G0-3 | 0 | 0 | 0 | - |
| TC-183 | L1 | NP-G0-3 | 0 | 7 | 7 | - |
| TC-184 | mixed (L1 x5, L2 x3) | NP-G0-3 | 3 | 12 | 8 | - |
| TC-185 | mixed (L1 x3, L2 x3, L3 x3) | NP-G0-3 | 13 | 9 | 0 | - |
| TC-186 | L1 x2 | NP-G0-3 | 0 | 2 | 2 | - |
| TC-187 | L1 | NP-G0-3 | 0 | 1 | 1 | - |
| TC-188 | L1 x5 | NP-G0-3 | 0 | 5 | 8 | - |
| TC-189 | L1 | NP-G0-3 | 0 | 1 | 1 | - |
| TC-190 | L1 | NP-G0-3 | 0 | 1 | 1 | - |
| TC-191 | L1 | NP-G0-3 | 0 | 1 | 2 | - |
| TC-192 | L1 | NP-G0-3 | 0 | 1 | 2 | - |
| TC-193 | L1 | NP-G0-3 | 0 | 1 | 2 | - |
| TC-194 | L1 | NP-G0-3 | 0 | 1 | 2 | NR-S-2 (P1) |
| TC-195 | L1 | NP-G0-3 | 0 | 2 | 1 | - |
| TC-196 | L1 | NP-G0-3 | 0 | 0 | 2 | - |
| TC-197 | L2 | NP-G0-3 | 2 | 2 | 0 | - |
| TC-198 | L1 | NP-G0-3 | 0 | 0 | 0 | - |
| TC-199 | L1 | NP-G0-3 | 0 | 1 | 2 | - |
| TC-200 | L1 | NP-G0-3 | 0 | 0 | 0 | - |
| TC-201 | L1 | NP-G0-3 | 1 | 2 | 1 | - |
| TC-202 | L1 | NP-G0-3 | 0 | 0 | 2 | - |
| TC-205 | L1 | NP-G0-3 | 0 | 0 | 2 | - |
| TC-206 | L1 | NP-G0-3 | 0 | 0 | 0 | - |

### 4.4 agent-suite (as) - 25 reports | P0 552, P1 292, P2 17 (total 861)

| TC | Tier | Gate-0 | P0 | P1 | P2 | EX |
|---|---|---|---:|---:|---:|---|
| TC-004 | L3 | NP-G0-4 | 37 | 11 | 5 | - |
| TC-005 | L2 | Pass | 1 | 7 | 1 | - |
| TC-006 | L2 | Pass | 4 | 4 | 0 | - |
| TC-031 | L3 | NP-G0-4 | 50 | 35 | 4 | NL-A-3 (P1) |
| TC-032 | L3 | NP-G0-4 | 56 | 40 | 0 | NR-S-9 (P2) |
| TC-033 | L3 | NP-G0-4 | 62 | 37 | 0 | NL-A-7 (P0); NR-S-9 (P2) |
| TC-034 | L2 | NP-G0-4 | 38 | 49 | 0 | NL-A-2 (P2) |
| TC-035 | L3 | NP-G0-4 | 32 | 2 | 0 | - |
| TC-036 | L3 | NP-G0-4 | 33 | 2 | 0 | - |
| TC-037 | L3 (artifact-level) | NP-G0-4 (+G0-3) | 9 | 0 | 0 | - |
| TC-038 | L3 | Pass | 36 | 14 | 0 | - |
| TC-039 | L3 | NP-G0-4 | 36 | 2 | 0 | - |
| TC-040 | L1 | NP-G0-4 (+G0-3) | 3 | 7 | 0 | - |
| TC-041 | L3 | NP-G0-4 | 25 | 9 | 0 | - |
| TC-042 | L3 | NP-G0-4 | 34 | 1 | 0 | - |
| TC-055 | L2 | Pass | 2 | 0 | 0 | - |
| TC-056 | L2 | Pass | 3 | 10 | 0 | - |
| TC-057 | L2 | Pass | 18 | 6 | 0 | - |
| TC-058 | L2 | Pass | 5 | 11 | 1 | - |
| TC-059 | L2 | Pass | 4 | 8 | 0 | - |
| TC-060 | L3 | NP-G0-4 | 26 | 7 | 1 | - |
| TC-061 | L2 | Pass | 5 | 12 | 1 | NR-S-9 (P2) |
| TC-062 | L3 | Pass | 24 | 3 | 2 | - |
| TC-063 | L2 | Pass | 4 | 10 | 0 | - |
| TC-064 | L2 | NP-G0-4 | 5 | 5 | 2 | - |

## 5. Recurring Patterns and Notable Findings

**5.1 P0 is concentrated in agent-suite.** 552 of 825 P0 verdicts (66.9%) come from the 25 agent-suite
reports, whose median is far above the single-artifact categories (mean 34.4 FAIL/report vs 5.2-11.9).
Two mechanisms explain this: (a) a suite is inspected against the union of the Prompt, Skill, Tool Schema
*and* three cross-artifact families; (b) agent-suite reports apply an L3 severity-upgrade rule (Agent L3 ->
global P1->P0, P2->P1), so the same underlying gap is recorded one band higher.

**5.2 One boundary declaration failure recurs across all three single-artifact families.** The top rules in
each family are the boundary sub-rules: prompt (QD-P-2.5.x input/output bounds, 2.7.x termination/data
handling), skill (QD-S-1.1/1.3/4.x resource, execution and failure-handling bounds) and tool schema
(QD-T-2.1/2.2/2.3 parameter constraints). The shared failure mode is an artifact that declares its task but
not the *limits* of the task (inputs, quantities, termination, failure handling).

**5.3 Tool Schemas fail structurally, not incidentally.** QD-T-1.4 (uncontrolled `additionalProperties`)
and QD-T-2.1 (missing parameter constraints) appear in essentially every tool report, and the tool-schema
category is the only one that is P2-heavy (52/129, 40.3%). This is a clean, mechanical, high-recurrence
signature: schema authors overwhelmingly omit the negative-space declarations.

**5.4 Embedded code is most often not self-contained.** QC-0.3 (elided code fragments, 19 mentions) is the
single most frequent embedded-code problem - runbook snippets inside artifacts are frequently truncated or
pseudo-code and are not independently runnable.

**5.5 Determinism across reused source projects (reproducibility signal).** Where the same source project
appears in several cases, the counts are near-identical: the `claude-skills` prompt cases TC-078/079/080/083
all report 18/1/0, and TC-054/TC-046-fabric variants cluster tightly. Repeated inspection of comparable
artifacts under the same rule set yields stable counts, which supports the reproducibility of the
instrument.

**5.6 Gate-0 is a corpus-construction boundary, not a defect rate.** Single-artifact reports (75 of 100)
cannot satisfy Gate-0 by construction (a lone artifact has no responsibility baseline / no Tool Schema to
complete). Only agent-suite cases can pass (11/25). The 89 "Not passed" outcomes therefore measure the
*absence of a cross-artifact responsibility context*, not a quality failure of the artifact itself.

**5.7 Notable Risk-Explicit items.** NR-S-9 (explicit credential/secret exposure in the artifact text;
4 cases, incl. a `GITHUB_TOKEN` example in TC-003), NR-S-2 (an ignored `ignoreRobotsText` control in
TC-194), and NL-A-7 (reverse-constraint removal; 3 cases, one at P0 in TC-033).

## 6. Measurement Framing and Limitations

**6.1 Evaluand vs. unit of count.** P0/P1/P2 are *FAIL-verdict counts* produced by the inspector, not counts
of distinct defects. A single artefact defect can yield several rule verdicts (e.g. one missing boundary
triggers several sub-rules; one tool schema triggers the same rule once per tool). Counts therefore measure
the *rule-level verdict surface*, which is the right unit for rule-coverage analysis but should not be read
as an absolute defect census.

**6.2 Instrument.** One framework version (SanityOps v1.0, September 2026) and one inspector version
(sanityops-inspect-lite v1.0.0) produced all 100 reports; the counts are not comparable across other
framework or inspector versions.

**6.3 Layout heterogeneity and parser caveats.** The reports span at least two layout generations
(Section 1.3). Consequences: (a) the mechanical FAIL-line tally in Section 3 is an *indicative* frequency,
because batch-1 layouts omit the inline severity and some counts live only in headline lines; the
authoritative per-case numbers come from each report's own Executive-Summary counts (Section 2.1).
(b) Two Gate-0 label sets (G0-1..G0-4 vs G0-3/G0-4) occur; only the outcome is aggregated.

**6.4 No inter-model comparison.** The corpus was authored with two host models (DeepSeek V4 Flash,
GLM 5.3 Flash), but per-report model attribution is not recorded in the reports, so no model-to-model
comparison is possible from this data. This is a limitation to be closed in a future collection pass.

**6.5 Corpus scope.** The 100 reports are the 25-per-category inspected slice of a 200-case corpus; they
are not asserted to be a probability sample. Percentages describe this slice.

## 7. Definitions and Codes (deferred)

The full **rule-code dictionary** (every QD-*/QC-* ID with its plain-language definition, example, rationale
and remediation) and the **EX class catalogue** (NL-A-*, NR-S-* semantics) are deferred to a future
attachment. The user's instruction is to add them once the per-case reports are complete, to keep this
summary within a workable size. Until then, Sections 3 and 4 give the exact rule IDs, so every number in
this report is traceable to the rule level; only the human-readable gloss of each ID is outstanding.

**Plan for the attachment:** (1) enumerate all 106 rule IDs from `summary-rules.csv`; (2) for each, add
definition / phenomenon / rationale / example / remediation, grouped by family; (3) enumerate the 13 EX
items with their class semantics; (4) cross-link each entry to at least one source report line.

## 8. Aggregation Coverage and Self-Check

**8.1 Coverage.** All 100 source reports were aggregated: 25 per category, every test case appears exactly
once (verified). Two data sources are kept distinct: (i) the **curated per-case counts** used in this report
(each report's own stated counts), and (ii) the **mechanical FAIL-line tally** used only for the rule-level
frequencies in Section 3.

**8.2 Corrections applied to the working data.**

- **C-1 (new).** TC-046: the report's headline is QD-P only ("P0 = 2, P1 = 9, P2 = 0") with a separate
  additive line "Embedded-code QC added 2 FAIL (QC-0.3 P1, QC-1.3 P2)". Under the Section-2.1 convention the
  correct value is **2/10/1** (the two QC FAILs are confirmed at the report's lines 71 and 74). An earlier
  draft held 2/9/0, which was inconsistent with the identical handling of TC-143/TC-146. Effect on totals:
  sp 171/121/4 -> 171/122/5; grand total 825/565/81 -> 825/566/82.
- **C-2 (carried).** TC-140's EX item is NL-A-7 (Reverse Constraint Removal), severity P2, not NR-S-4.

**8.3 Self-checks (C1-C8).**

| # | Check | Result |
|---|---|---|
| C1 | Category totals re-summed by hand from the per-case table | PASS (825/566/82) |
| C2a | Independent re-derivation: mechanical extraction of each report's own counts vs. the curated table | PASS - 98/100 exact; 1 parser artifact (TC-050, curated correct); 1 curated correction (TC-046, applied) |
| C3 | (TC, rule) distinct pairs <= FAIL verdicts | PASS |
| C4 | Special-case review (TC-139 unmarked; TC-046; TC-050; mixed/undetermined tiers) | PASS |
| C5 | Zero non-ASCII in deliverables | PASS |
| C6 | Numeric read-back of Section 2/3 against Section 4 row sums | PASS |
| C7 | Structural validation (100 unique cases, 25/category) | PASS |
| C8 | Three-way consistency: cache == report tables == CSV exports | PASS |

All verification logs and the working data cache are retained (Section 9).

## 9. Data Availability

The following artifacts are retained for audit and reuse. The 100 source reports remain the ground truth;
every aggregate here is reproducible from them via the logs below.

| Artifact | Path | Role |
|---|---|---|
| 100 source reports | `test-cases/{...}/*.sanityops-skill-report.md` | ground truth |
| Working data cache | `summary-work/summary-data.md` | curated per-case + per-rule data, corrections, checks |
| C2a extractor | `summary-work/c2a-verify.ps1` | re-derivation script |
| C2a diff log | `summary-work/c2a-check.log` | per-case curated-vs-mechanical diff |
| Mechanical parse logs | `summary-work/raw-{sp,sk,ts,as}.log` | rule/TC tallies behind Section 3 |
| CSV exports | `test-cases/summary-per-tc.csv`, `summary-rules.csv`, `summary-ex.csv` | machine-readable companions |

**Appendix A. Data Dictionary** - deferred together with Section 7 (rule-code dictionary and EX catalogue).

