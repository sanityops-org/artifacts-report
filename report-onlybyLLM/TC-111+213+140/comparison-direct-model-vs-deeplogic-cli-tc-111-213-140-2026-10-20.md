# Direct-Model vs deeplogic-cli Evaluation Comparison - TC-111, TC-213, TC-140

## Scope

This report compares two independent evaluations of the same three verbatim artifacts:

- **Direct model evaluation:** the pre-existing `综合评测报告.md`, which applies case-specific dimensions, 1-5 rubric scores, weighted scores, and manual boundary checks.
- **deeplogic-cli evaluation:** the three isolated L1/L2 inspections generated in this folder, using the CLI's QDP/QDT/QDS rule taxonomy, QC lint, quality gate, and raw-report evidence.

The comparison does not merge the two scores into a single authoritative score. Their rating scales, defect taxonomies, and evidence methods are different.

## Executive Summary

The two methods agree on the relative order of artifact quality:

1. TC-213 Firecrawl Tool Schema
2. TC-111 SalesGPT System Prompt
3. TC-140 CSV Data Summarizer Skill

They disagree sharply on magnitude, severity, and coverage:

- The direct-model report gives an average of **60.5/100** and records **28 defects**: P0 1, P1 17, P2 10.
- `deeplogic-cli` gives an unweighted average of **69.92/100** and records **19 defects**: P0 6, P1 13, P2 0.
- The CLI is much more permissive on TC-213, awarding **100/A/PASS** while the direct review found seven contract-level defects, including schema behavior confirmed with executable validation.
- The CLI is much harsher on TC-140, awarding **20.55/D/FAIL** and elevating resource, scope, and failure-boundary issues to P0.
- Both methods find the TC-111 first-turn conflict, but the CLI assigns it P0 while the direct review assigns it P1.
- The direct review finds a compliance P0 in TC-111 (`public records` disclosure) that the CLI misses completely.

**Bottom line:** the direct-model evaluation is stronger on semantic compliance and JSON Schema correctness; `deeplogic-cli` is stronger on repeatable rule application, structural reporting, resource/security policy coverage, and evidence traceability. The methods are complementary, but neither should be used alone for release decisions.

## Score Comparison

| Case | Direct score | Direct 5-point score | CLI score | CLI grade / gate | CLI minus direct |
|---|---:|---:|---:|---|---:|
| TC-111 SalesGPT Prompt | 59.0 | 3.0 | 89.22 | B / FAIL | +30.22 |
| TC-213 Firecrawl Tool | 64.5 | 3.2 | 100.00 | A / PASS | +35.50 |
| TC-140 CSV Skill | 58.0 | 2.9 | 20.55 | D / FAIL | -37.45 |
| **Unweighted mean** | **60.5** | **3.0** | **69.92** | Mixed | **+9.42** |

The averages are for orientation only. The direct report uses case-specific weighted dimensions, while the CLI applies module-level automated scoring and gates. A higher CLI score does not necessarily mean broader coverage, and a lower CLI score does not necessarily mean the direct review was more severe.

## Defect Count Comparison

| Case | Direct P0/P1/P2 | Direct total | CLI P0/P1/P2 | CLI total | Difference |
|---|---:|---:|---:|---:|---:|
| TC-111 | 1 / 7 / 3 | 11 | 1 / 2 / 0 | 3 | -8 |
| TC-213 | 0 / 4 / 3 | 7 | 0 / 0 / 0 | 0 | -7 |
| TC-140 | 0 / 6 / 4 | 10 | 5 / 11 / 0 | 16 | +6 |
| **Total** | **1 / 17 / 10** | **28** | **6 / 13 / 0** | **19** | **-9** |

The largest structural difference is that the CLI produced **no P2 findings** and used P0 much more aggressively for TC-140. The direct review spread findings across all three severities and treated some TC-140 permission issues as risks rather than immediate blockers.

## Per-Case Comparison

### TC-111: SalesGPT System Prompt

**Agreement**

- Both evaluations identify the conflict between the first-turn “greeting only, no pitch” instruction and the Introduction-stage requirement to introduce the company and explain the call.
- Both flag the vague response-length instruction and the unclear `<END_OF_CALL>` output contract.

**Differences**

| Finding | Direct model | deeplogic-cli | Assessment |
|---|---|---|---|
| First-turn greeting conflict | P1 | QDP-1.1.1, P0 | Same issue; severity calibration differs |
| Vague “short length” | P2 | QDP-1.3.2, P1 | Both detect it; CLI is stricter |
| `<END_OF_CALL>` format | P2 | QDP-2.3.1, P1 | Both detect it; CLI is stricter |
| Unconditional “public records” source claim | P0 | Not detected | Major direct-model advantage |
| Missing stage state machine and transition rules | P1 | Not detected | Direct review has broader workflow coverage |
| Tool input forced to one simple string | P1 | Not detected | Direct review has deeper tool-contract analysis |
| Missing tool failure/retry policy | P1 | Not detected | CLI focuses on prompt rule structure, not runtime failure behavior |
| Prompt-injection isolation for user input/observations | P1 | Not detected | Direct review has stronger safety analysis |
| Consent, opt-out, AI disclosure, recording notice | P1 | Not detected | Permission inspection was skipped and safety coverage is incomplete |
| Evidence/testimonial verifiability | P1 | Not detected | Direct review captures marketing-risk constraints |
| Internal `Thought:` exposure | P2 | Not detected | Direct review has additional privacy/architecture concern |

**Judgment:** Both reports are directionally correct, but the direct review is more complete. The CLI gives a relatively high 89.22/B score while missing several safety and compliance concerns and produces a FAIL only from one P0 conflict. For production review, the direct report should drive remediation, while the CLI finding provides an additional standardized gate result.

### TC-213: Firecrawl MCP Tool Schema

**Agreement**

- Both recognize the description as strong: clear capability, when-to-use guidance, sibling-tool disambiguation, asynchronous job flow, continuation, spend controls, and provider-approval workflow.
- Both note the absence of `outputSchema` or otherwise flag missing output-contract coverage.

**Differences**

| Finding | Direct model | deeplogic-cli | Assessment |
|---|---|---|---|
| `schema` accepts only an empty object under `additionalProperties: false` | P1, verified with Draft-07 instance tests | Not detected | Direct-model advantage; likely functional defect |
| Cross-field constraints absent from JSON Schema | P1, multiple invalid instances pass | Not detected | Direct-model advantage |
| `threadId` regex accepts literal `<uuid>` placeholders | P1, verified | Not detected | Direct-model advantage |
| Missing `outputSchema` | P1 | Not emitted as a QD-T defect | Direct-model advantage |
| Parameter descriptions and collection bounds incomplete | P2 | Not detected | Direct-model advantage in depth |
| Cancellation, polling, and terminal-timeout contract missing | P2 | Not detected | Direct-model advantage in runtime integration analysis |

**Judgment:** This is the clearest disagreement. The CLI reports **0 defects and 100/A/PASS**, while the direct review provides executable evidence for several contract defects. At minimum, the empty `schema` object and cross-field validation gaps should be treated as real defects until disproved. The CLI's L1 result is not sufficient evidence that the schema is production-ready.

The CLI also had a tooling limitation: it did not recognize the MCP camel-case `inputSchema` key in its structured-tool parser. Mapping the key to `input_schema` was necessary before meaningful evaluation. That adapter preserved the schema content, but it also shows that the CLI pipeline needs an MCP-aware ingestion layer.

### TC-140: CSV Data Summarizer Skill

**Agreement**

- Both identify over-triggering and the lack of safe clarification behavior.
- Both identify unbounded resource use and excessive “run everything” instructions.
- Both identify the visualization-rule contradiction.
- Both treat the Skill as unsuitable for direct production use.

**Differences**

| Finding | Direct model | deeplogic-cli | Assessment |
|---|---|---|---|
| No input-size or row/column boundary | P1 | QDS-1.1, P0 | Same issue; CLI is stricter |
| No timeout, retry, or tool-call boundary | P1 | QDS-1.3, P0 | Same issue; CLI is stricter |
| Unbounded comprehensive analysis | P1 | QDS-2.1, P0 | Same issue; CLI maps it directly to resource risk |
| No failure-handling policy | P1 | QDS-4.1, P0 | Same issue; CLI is stricter |
| Over-triggering and no negative routing | P1/P2 | QDS-3.2, P1 | Broad agreement |
| No ambiguous-input clarification policy | P1 | QDS-3.3, P1 | Broad agreement |
| Visualization-rule contradiction | P1 | QDS-3.6, P1 | Broad agreement; CLI's recommended fix is contextually wrong |
| Missing non-goals | Not separate | QDS-3.4, P0 | CLI adds a broad scope-boundary finding |
| Read/write/delete permission matrix | Partial path-access finding | QDS-1.4, QDS-5.1, P1 | CLI is more systematic |
| Data-source and environment boundaries | Partial path-access finding | QDS-1.5, QDS-5.3, P1 | CLI is more systematic |
| Chained-invocation permissions | Not explicit | QDS-5.4, P1 | CLI adds a policy-level finding |
| Execution contract for `analyze.py` | P1 | Not directly detected | Direct-model advantage |
| Dependency failure and artifact completeness | P2 | Not detected | Direct-model advantage |
| Example-output and statistical-causality quality | P2 | Not directly detected | Direct-model advantage |

**Judgment:** The two reviews are complementary. The CLI gives a clearer policy-based P0 cluster for unsafe autonomy and missing boundaries. The direct review gives a better implementation-contract review. The 20.55/D score is useful as a release warning, but it should not replace the direct report's more specific execution and documentation findings.

## Methodological Differences

| Dimension | Direct model report | deeplogic-cli report |
|---|---|---|
| Primary method | Holistic semantic review plus targeted manual tests | Fixed defect rule engine, LLM inspectors, QC lint, and quality gates |
| Rating | Case-specific 1-5 dimensions and weighted 100-point score | Module score, letter grade, severity counts, and gate |
| Case-specific adaptation | High | Medium; rules are standardized across artifacts |
| Repeatability | Lower without a saved prompt/model trace | Higher; config, console log, raw report, and extracted input are retained |
| Schema validation | Can execute Draft-07 meta-schema and instance tests | QC lint is mostly syntax/structure; LLM may miss semantic schema defects |
| Safety/compliance coverage | Stronger in the TC-111 review | Stronger TC-140 permission policy coverage, but QD-PM was skipped |
| Severity consistency | More conservative; only one P0 | More aggressive; six P0 findings |
| Evidence traceability | Strong narrative examples, but no model/version/run trace in the report | Strong: raw report, console log, configuration, and artifact copies |
| Failure handling | Not a runtime dependency | Model timeouts and SDK incompatibilities affected L2 completion |

## Agreement Matrix

| Area | Agreement level | Notes |
|---|---|---|
| Relative ranking | High | Both rank TC-213 first, TC-111 second, TC-140 third |
| TC-111 main behavior conflict | High | Same conflict; P1 vs P0 |
| TC-213 schema correctness | Low | Direct review finds multiple concrete defects; CLI finds none |
| TC-213 description quality | High | Both treat the description as strong |
| TC-140 autonomy and resource risk | High | Both flag unbounded execution and missing limits |
| TC-140 permission/environment policy | Medium | CLI is broader and more structured |
| TC-140 execution/documentation contract | Low | Direct review is materially deeper |
| Overall severity calibration | Low | CLI has more P0s and no P2s; direct review is more granular |

## Which Evaluation Should Be Trusted?

There is no universal winner.

**Use the direct-model report when:**

- Reviewing semantic compliance and user-facing safety.
- Evaluating JSON Schema behavior with concrete instances.
- Checking implementation contracts, documentation completeness, and testability.
- Comparing artifact quality against the case-specific evaluation dimensions.

**Use `deeplogic-cli` when:**

- A repeatable release gate and standardized rule taxonomy are required.
- You need severity counts, QC lint, configuration, and raw execution evidence.
- You want systematic policy coverage for resources, permissions, failure modes, and output contracts.
- You need a consistent baseline across a larger artifact corpus.

## Recommended Adjudication

| Case | Recommended decision | Reason |
|---|---|---|
| TC-111 | **FAIL / remediation required** | Accept the direct report's compliance P0 and the CLI's conflict finding. Add measurable length limits and a machine-readable end-of-call contract. |
| TC-213 | **FAIL / conditional remediation** | Do not accept the CLI's 100/A as a release approval in isolation. Resolve the directly verified `schema`, cross-field, UUID, and `outputSchema` issues, then rerun both methods. |
| TC-140 | **FAIL / redesign required** | Accept the CLI's resource and failure-boundary P0 cluster, and add the direct report's execution-contract, visualization, and documentation findings. |

## Final Conclusion

The two evaluation methods are not substitutes:

- The **direct model evaluation** has better semantic depth and catches high-value compliance and schema-contract defects.
- The **CLI evaluation** has better repeatability, explicit severity policy, and audit evidence, but it can miss concrete contract defects and overstate or understate severity because its result depends on the model, check level, and parser ingestion.
- The appropriate production workflow is **CLI as a repeatable gate plus direct review as a semantic and adversarial test layer**, followed by human adjudication of disagreements.

For the current corpus, the combined evidence supports treating all three artifacts as not production-ready. TC-213 remains the strongest artifact, but its perfect CLI score should not be interpreted as a clean contract.

## Evidence

- [Direct-model report](./综合评测报告.md)
- [deeplogic-cli summary](./deeplogic-cli-evaluation-summary.md)
- [TC-111 CLI report](./TC-111-salesgpt-system-prompt.deeplogic-cli-report.md)
- [TC-213 CLI report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md)
- [TC-140 CLI report](./TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md)
- [TC-111 raw CLI report](./TC-111-salesgpt-system-prompt.deeplogic-cli.inspect-raw.md)
- [TC-213 raw CLI report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.inspect-raw.md)
- [TC-140 raw CLI report](./TC-140-csv-data-summarizer-skill.deeplogic-cli.inspect-raw.md)
