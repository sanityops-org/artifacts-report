# deeplogic-cli Evaluation Summary - TC-111, TC-213, TC-140

## Scope

This folder contains three isolated `deeplogic-cli` evaluations of artifacts embedded in the requested test cases. Evaluation dimensions, test suggestions, and notes from the surrounding test-case documents were excluded from the model input.

| Case | Artifact type | Completed level | Defects | Score | Grade | CLI gate | QC lint | Permission |
|---|---|---:|---:|---:|---|---|---|---|
| TC-111 SalesGPT | System Prompt | L1 | 3 (P0 1; P1 2; P2 0) | 89.22 | B | FAIL | PASS (2 P1) | Skipped |
| TC-213 Firecrawl | Tool Schema | L1 | 0 (P0 0; P1 0; P2 0) | 100.0 | A | PASS | PASS | Skipped |
| TC-140 CSV Summarizer | Skill | L2 | 16 (P0 5; P1 11; P2 0) | 20.55 | D | FAIL | PASS | Skipped |

## Conclusions

1. **TC-213 is the strongest artifact in the CLI run.** Its L1 check reports no QD-T defects and a perfect score. The description and input schema are unusually detailed. Independent review still found a missing `outputSchema` and a potentially over-constrained `schema` parameter.
2. **TC-111 is structurally useful but internally inconsistent.** The direct conflict between the greeting-only first turn and the requirement to introduce the company and purpose is a real production behavior risk. The output terminator also needs an unambiguous format.
3. **TC-140 needs redesign before production use.** The strongest findings concern unbounded input/output, an instruction to run all analyses without upper bounds, and no failure-handling policy. Several lower-severity permission findings are more debatable, but the five P0 defects form a coherent risk cluster.

## Method and Reproducibility

- **CLI:** `deeplogic-cli 1.18.0`
- **Defect-check SDK:** `defect-check 1.2.8`
- **Model endpoint:** `anthropic / test-assistant` through the configured local-compatible gateway
- **Run date:** 2026-10-20 (Asia/Shanghai)
- **Prompt input:** exact value of `SALES_AGENT_TOOLS_PROMPT`
- **Tool input:** exact `firecrawl_agent` object with only the field name adapted from `inputSchema` to `input_schema`
- **Skill input:** exact quoted `SKILL.md` content, including frontmatter
- **Upload behavior:** final successful runs reported `API key not configured, skip auto upload`
- **Permission checks:** all skipped by Gate-0
- **Compatibility shim:** accepts CLI `force_permission`, ignores an unsupported SDK timeout constructor argument, and awaits a synchronous `close()`; it does not alter content, defect rules, or scores

## Level Consistency

TC-140 completed at the default L2 level. TC-111 and TC-213 produced no usable L2 result after repeated model response timeouts. Their completed L1 results are retained because they are valid CLI inspections, but they are shallower and should not be treated as directly interchangeable with the L2 score.

## Evidence Inventory

| Case | Report | Raw report | Console log | Extracted input |
|---|---|---|---|---|
| TC-111 | [Report](./TC-111-salesgpt-system-prompt.deeplogic-cli-report.md) | [Raw](./TC-111-salesgpt-system-prompt.deeplogic-cli.inspect-raw.md) | [Log](./TC-111-salesgpt-system-prompt.deeplogic-cli.console.log) | [Prompt](./artifacts/TC-111-salesgpt-system-prompt.prompt.txt) |
| TC-213 | [Report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md) | [Raw](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.inspect-raw.md) | [Log](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.console.log) | [Tool JSON](./artifacts/TC-213-firecrawl-mcp-tool-schema.deeplogic.tool.json) |
| TC-140 | [Report](./TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md) | [Raw](./TC-140-csv-data-summarizer-skill.deeplogic-cli.inspect-raw.md) | [Log](./TC-140-csv-data-summarizer-skill.deeplogic-cli.console.log) | [Skill](./artifacts/TC-140-csv-data-summarizer-skill.SKILL.md) |

Failed or superseded L2 attempts are retained under `runs/<case>/attempts/` for auditability.

## Cross-Method Comparison

See [Direct-model vs deeplogic-cli comparison](./comparison-direct-model-vs-deeplogic-cli-tc-111-213-140-2026-10-20.md) for score deltas, defect-level agreement, coverage gaps, and the recommended adjudication.
