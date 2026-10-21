# Direct-Model vs deeplogic-cli Evaluation Comparison - TC-111, TC-213, TC-140

> **Revision:** 2026-10-21
> This revision replaces the earlier comparison based on the previous direct-model report. The updated direct-model source is now a combined defect, permission, and risk inspection for the three artifacts, not a per-case checklist with the earlier 59.0 / 64.5 / 58.0 scores.

## Scope and Method

This report compares two evaluations of the same three verbatim artifacts:

- **Direct-model evaluation:** the revised `综合评测报告.md`, which uses case-specific dimension scores, Draft-07 metadata validation, representative invalid-instance tests, a permission matrix, and cross-artifact threat modeling.
- **deeplogic-cli evaluation:** three isolated QDP/QDT/QDS inspections with QC lint and quality gates. The final levels are L1 for TC-111, L1 for TC-213, and L2 for TC-140.

The two evaluations answer different questions:

- The direct report asks whether the three artifacts can be safely combined into a sales-agent workflow.
- `deeplogic-cli` asks whether each artifact contains defects under its standardized single-artifact rules.

That difference explains most of the disagreement. Scores and counts below are compared for orientation, not merged into a new authoritative score.

## Executive Summary

The revised reports agree that the corpus is not production-ready, but they disagree strongly about the individual artifacts and the reasons:

- The direct report ranks the artifacts **TC-111 > TC-140 > TC-213** by case-specific weighted score.
- `deeplogic-cli` ranks them **TC-213 > TC-111 > TC-140** by automated score and gate.
- The direct report assigns TC-213 the lowest relative score because it provides concrete evidence that the `schema`, cross-field constraints, URL handling, and output contract are defective.
- `deeplogic-cli` gives TC-213 **100/A/PASS** and reports no QD-T defects. Its single-artifact L1 check does not exercise those schema semantics.
- Both identify TC-140 as unsafe because it reads and analyzes data automatically without sufficient size, failure, or permission boundaries.
- The direct report adds a combined data-flow risk that the CLI cannot see: CSV → prompt/history → Firecrawl → third-party provider creates a plausible local-data exfiltration and prompt-injection chain.
- The CLI contributes several TC-111 and TC-140 single-artifact findings that the revised direct report does not enumerate, including the first-turn greeting conflict and missing output-size/failure policies.

**Bottom line:** the revised direct report is materially stronger for combined deployment risk, JSON Schema semantics, permissions, and adversarial data flow. `deeplogic-cli` remains stronger for repeatable single-artifact rule application, severity gates, QC lint, and run evidence. TC-213's perfect CLI score should not be accepted without the direct report's schema evidence.

## Score Comparison

| Case | Direct weighted score | Direct percentage | CLI score | CLI grade / gate | CLI minus direct |
|---|---:|---:|---:|---|---:|
| TC-111 SalesGPT Prompt | 3.55 / 5 | 71% | 89.22 | B / FAIL | +18.22 |
| TC-213 Firecrawl Schema | 2.65 / 5 | 53% | 100.00 | A / PASS | +47.00 |
| TC-140 CSV Skill | 2.80 / 5 | 56% | 20.55 | D / FAIL | -35.45 |
| **Unweighted mean** | **3.00 / 5** | **60.0%** | **69.92** | Mixed | **+9.92** |

Direct-model dimension scores:

| Case | Dimension 1 | Dimension 2 | Dimension 3 | Dimension 4 | Dimension 5 |
|---|---:|---:|---:|---:|---:|
| TC-111 | 5 | 4 | 3 | 1 | 4 |
| TC-213 | 4 | 2 | 2 | 2 | 3 |
| TC-140 | 4 | 2 | 3 | 3 | 2 |

The direct percentages and CLI scores use different weighting and rule systems. The CLI mean being approximately 9.92 points higher does not mean it found a better product; it mainly reflects weaker coverage of TC-213 contract behavior and a different severity model.

## Finding Counts

The revised direct report uses a different structure from its previous version. It does not publish one merged P0/P1/P2 count.

### Direct-model confirmed findings

| Severity in direct report | Count | IDs |
|---|---:|---|
| Severe | 1 | F-01 |
| High | 6 | F-02, F-03, F-04, F-05, F-06, F-07 |
| Medium | 2 | F-08, F-09 |
| **Total confirmed findings** | **9** | F-01 through F-09 |

### Direct-model combination risks

| Severity in direct report | Count | IDs |
|---|---:|---|
| Severe | 2 | R-01, R-02 |
| High | 3 | R-03, R-04, R-05 |
| Medium | 1 | R-06 |
| **Total combination risks** | **6** | R-01 through R-06 |

The confirmed findings and combination risks overlap in places. For example, source-authenticity concerns appear in both the confirmed-risk and combination-risk sections. They should not be added together as 15 independent defects.

### deeplogic-cli findings

| Case | P0 | P1 | P2 | Total |
|---|---:|---:|---:|---:|
| TC-111 | 1 | 2 | 0 | 3 |
| TC-213 | 0 | 0 | 0 | 0 |
| TC-140 | 5 | 11 | 0 | 16 |
| **Total** | **6** | **13** | **0** | **19** |

`deeplogic-cli` therefore detects more artifact-local defects overall, but most of that difference comes from its aggressive TC-140 resource and permission rules. It misses nearly all of the direct report's TC-213 contract findings and does not evaluate the three-artifact composition.

## Cross-Artifact Finding Map

| Direct-model finding | Direct severity | CLI equivalent | Assessment |
|---|---|---|---|
| F-01 Firecrawl `schema` accepts only an empty object | Severe | Not detected | Direct-model advantage; confirmed with invalid-instance tests |
| F-02 Cross-field constraints are not executable | High | Not detected | Direct-model advantage |
| F-03 Claimed `outputSchema` is absent | High | Not emitted as QD-T defect | Direct-model advantage |
| F-04 String `Action Input` conflicts with object-shaped Firecrawl input | High | Not detected | Cross-artifact issue outside CLI's isolated checks |
| F-05 Async job ID conflicts with one-shot Observation flow | High | Not detected | Cross-artifact state-machine issue |
| F-06 URL scope lacks protocol, count, and destination controls | High | Not detected | Direct-model advantage; SSRF/minimum-privilege analysis |
| F-07 CSV auto-execution lacks sensitive-data and size gates | High | QDS-1.1, QDS-1.3, QDS-2.1, QDS-3.3, P0/P1 | Strong overlap; CLI gives a more explicit gate |
| F-08 Date inference and graceful-missing-data claims lack evidence | Medium | Not directly detected | Direct-model advantage |
| F-09 Firecrawl parameter descriptions and `maxCredits` bound are weak | Medium | Not detected | Direct-model advantage |
| R-01 CSV → model → Firecrawl data exfiltration chain | Severe | Not evaluated | Requires the combined threat model |
| R-02 CSV/web content prompt-injection chain | Severe | Not evaluated | Requires cross-artifact composition |
| R-03 Sales-source and contact compliance risk | High | Not detected | Direct-model advantage |
| R-04 Cost and approval controls can be bypassed | High | Not detected | Direct-model advantage |
| R-05 Automated analysis can misrepresent statistics and business conclusions | High | Not directly detected | Direct-model advantage |
| R-06 Incorrect sources can be presented as public records | Medium | Not detected | Direct-model advantage |

## CLI-Only Findings

The following material findings appear in the CLI reports but are not clearly enumerated in the revised direct report:

| Case | CLI finding | Severity | Relevance |
|---|---|---|---|
| TC-111 | First-turn greeting conflict | P0 | Remains a credible instruction-consistency defect |
| TC-111 | “Short length” is not measurable | P1 | Useful prompt-quality finding |
| TC-111 | `<END_OF_CALL>` format is ambiguous | P1 | Useful output-contract finding |
| TC-140 | Missing output-size limit | P1 | Complements the direct resource-risk analysis |
| TC-140 | Missing non-activation conditions | P1 | Complements the direct over-triggering analysis |
| TC-140 | Missing non-goals | P0 | Useful scope-boundary finding |
| TC-140 | Partial completion and post-failure behavior are undefined | P1 | Complements the direct failure-path analysis |
| TC-140 | Permission, environment, and chained-invocation matrices are absent | P1 | Useful policy-level findings, though some are stricter than the direct review |

These CLI-only findings should not be discarded merely because the direct report has broader combined-risk coverage.

## Per-Case Assessment

### TC-111 SalesGPT Prompt

**Direct-model view:** 3.55/5 (71%). The persona and sales flow are understandable, but compliance, consent, opt-out, source authenticity, and tool-call compatibility are insufficient.

**CLI view:** 89.22/B, gate FAIL. The CLI reports one P0 greeting conflict plus two P1 clarity/output-format findings.

**Comparison:** The direct report looks beyond prompt wording and finds higher-value tool-chain and compliance problems. The CLI is better at enforcing measurable prompt-consistency rules. Both results support remediation, but neither alone covers both views.

### TC-213 Firecrawl Tool Schema

**Direct-model view:** 2.65/5 (53%). The description is good, but Draft-07 validation and representative instances expose real input/output contract defects.

**CLI view:** 100/A, gate PASS, zero QD-T defects.

**Comparison:** This is the largest disagreement and the strongest warning against relying on the CLI score alone. The direct report's concrete instance tests should carry more weight for schema release decisions. The CLI result is best treated as evidence that the description and basic structure look complete, not that the contract behaves correctly.

The CLI pipeline also required a compatibility adapter from MCP `inputSchema` to its recognized `input_schema` key. This adapter preserved schema content, but the need for it reinforces that MCP contract evaluation requires a dedicated ingestion and validation path.

### TC-140 CSV Skill

**Direct-model view:** 2.80/5 (56%). The Skill auto-triggers, lacks sensitive-data and resource boundaries, and participates in a plausible cross-artifact exfiltration path.

**CLI view:** 20.55/D, gate FAIL, with five P0 and eleven P1 findings.

**Comparison:** The two methods agree on the central danger but use different severity and scope. The CLI gives a clear single-artifact blocker cluster for unbounded autonomy, resources, permissions, and failure handling. The direct report better explains why that autonomy becomes dangerous when combined with external tools and sales communications.

## Methodological Comparison

| Dimension | Revised direct-model report | deeplogic-cli |
|---|---|---|
| Primary unit | Three-artifact composition and individual implications | One isolated artifact per CLI run |
| Scoring | Case-specific dimensions, weighted 5-point percentages | Module score, letter grade, gate |
| JSON Schema analysis | Draft-07 meta-validation plus representative instances | QC structure/syntax plus LLM inspection |
| Permission analysis | Explicit capability matrix and data-flow threat model | QD-PM attempted, skipped by Gate-0 |
| Cross-artifact analysis | Central to the report | Not effective because each run contains one artifact |
| Severity model | Severe / High / Medium in narrative findings | P0 / P1 / P2 |
| Repeatability | Manual and model-assisted; no full run trace in the report | Config, console log, extracted input, and raw report retained |
| Strength | Semantic depth, adversarial reasoning, combined risk | Standardization, repeatability, gates, and artifact-local coverage |
| Weakness | Less standardized and harder to reproduce exactly | False confidence on TC-213 and blind to composition risk |

## Agreement Matrix

| Area | Agreement | Notes |
|---|---|---|
| Overall production readiness | High | Both reject the corpus for direct production use |
| TC-111 remediation need | High | Different findings; both see significant gaps |
| TC-213 contract quality | Very low | Direct review finds serious defects; CLI finds none |
| TC-140 autonomy/risk | High | Both identify the automatic execution path as unsafe |
| TC-140 specific severity | Low | CLI uses five P0s; direct report uses one severe confirmed finding plus combined risks |
| Cross-artifact data flow | None | Only the direct report evaluates the composition |
| Relative artifact ranking | None | Direct: TC-111 > TC-140 > TC-213; CLI: TC-213 > TC-111 > TC-140 |

## Recommended Use

Use the revised direct-model report as the **deployment and composition review**. It is the only one that evaluates the sales-agent workflow as a system and provides concrete JSON Schema counterexamples.

Use `deeplogic-cli` as the **repeatable single-artifact gate**. It provides consistent P0/P1/P2 classification, QC lint, run artifacts, and resource/permission checks, but it must not be treated as sufficient for cross-artifact safety or contract correctness.

## Adjudication

| Case | Recommended decision | Basis |
|---|---|---|
| TC-111 | **FAIL / remediate before use** | Direct compliance and tool-chain risks plus CLI greeting/output-contract findings |
| TC-213 | **FAIL / contract remediation required** | Direct Draft-07 counterexamples outweigh the CLI's 100/A L1 result |
| TC-140 | **FAIL / redesign required** | Both methods identify unsafe automatic analysis; combine direct composition risk with CLI resource/permission findings |
| Combined workflow | **Do not deploy as-is** | Local file access, untrusted text, external network calls, third-party data transfer, paid calls, and automated outreach form an unsafe chain |

## Final Conclusion

The revised direct-model report changes the comparison materially:

- It is no longer a simple 28-defect checklist.
- It now emphasizes combined execution paths and confirms schema defects with test instances.
- The relative ranking no longer matches the CLI.
- The CLI's most serious weakness is its TC-213 false-negative result; the direct report's most serious limitation is that it is less standardized and does not provide the same raw execution trace.

The practical answer is not to choose one method. Use `deeplogic-cli` as a repeatable artifact gate, use the direct report as an adversarial and composition-level review, and require human adjudication whenever their severity or pass/fail decisions diverge.

## Evidence

- [Revised direct-model report](./综合评测报告.md)
- [deeplogic-cli summary](./deeplogic-cli-evaluation-summary.md)
- [TC-111 CLI report](./TC-111-salesgpt-system-prompt.deeplogic-cli-report.md)
- [TC-213 CLI report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md)
- [TC-140 CLI report](./TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md)
- [TC-111 raw CLI report](./TC-111-salesgpt-system-prompt.deeplogic-cli.inspect-raw.md)
- [TC-213 raw CLI report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.inspect-raw.md)
- [TC-140 raw CLI report](./TC-140-csv-data-summarizer-skill.deeplogic-cli.inspect-raw.md)
