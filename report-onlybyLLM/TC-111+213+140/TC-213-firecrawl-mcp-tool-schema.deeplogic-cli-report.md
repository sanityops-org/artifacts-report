# TC-213: Firecrawl MCP Tool Schema - deeplogic-cli Evaluation Report

## Execution Record

| Item | Value |
|---|---|
| Source case | `test-cases/single-artifact/tool-schema/TC-213-firecrawl-mcp-tool-schema.md` |
| Evaluated artifact | `artifacts/TC-213-firecrawl-mcp-tool-schema.deeplogic.tool.json` |
| Artifact extraction | `firecrawl_agent` value from the frozen MCP snapshot |
| Compatibility adapter | MCP `inputSchema` renamed to the CLI-recognized `input_schema`; all schema content was retained |
| Tool | `deeplogic-cli 1.18.0` |
| Defect-check SDK | `defect-check 1.2.8` |
| Model | `anthropic / test-assistant` |
| Check level | **L1 completed** |
| Generated | 2026-10-20 19:19:57 |
| Inspection duration | 765.39s |
| Registered artifact | 0 Prompts, 1 Tool, 0 Skills |
| QD-T input length | 6,087 characters |

## Result

| Metric | Result |
|---|---:|
| Total defects | **0** |
| Severity | **P0: 0 / P1: 0 / P2: 0** |
| Score | **100.0 / 100** |
| Grade | **A** |
| Quality gate | **PASS** |
| QC lint | **PASS** (0 defects) |
| Permission inspection | **Skipped** (`GATE0_BLOCKED`) |

The CLI found no QD-T defects and awarded the tool schema a perfect L1 score. The result is supported by the tool's clear trigger and sibling-tool disambiguation, a valid Draft-07 object schema, a single required `prompt` field, constrained enums, and detailed parameter descriptions.

## Defects

No defects found.

## QC Lint

No QC lint defects were reported.

## Interpretation

**Strengths**

- The description explains when to use `firecrawl_agent` and when to prefer `firecrawl_scrape`, `firecrawl_search`, or `firecrawl_agent_status`.
- The asynchronous contract, expected latency, thread continuation, and provider-approval flow are documented.
- The input schema has `additionalProperties: false`, a single required field, bounded numeric fields, and constrained enums.
- Risk annotations such as `readOnlyHint`, `openWorldHint`, and `destructiveHint` are present.

**Reviewer notes beyond the CLI result**

- The captured object has no `outputSchema`; the test case's checklist claim that an output schema is present is not supported by the quoted artifact.
- The `schema` input is declared as an object with `additionalProperties: false` but no named properties. Under a strict Draft-07 validator, this would reject non-empty schema objects, which appears inconsistent with the parameter's documented purpose.
- These observations are independent review notes, not additional QD-T defects emitted by the CLI.

## Execution Caveats

- The CLI did not recognize the camel-case MCP `inputSchema` key in its structured-tool path. The first L2 attempt therefore evaluated empty parameters and produced three false P0 findings; that run is not used as evidence.
- After the equivalent `input_schema` adapter was applied, L2 ended in a model response timeout. A complete L1 run then finished with 0 defects and a 100/100 score.
- The final run skipped automatic corpus upload (`API key not configured`).
- Permission inspection was skipped because Gate-0 reported a missing responsibility-boundary statement.

## Evidence

- [Raw deeplogic-cli report](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.inspect-raw.md)
- [CLI console log](./TC-213-firecrawl-mcp-tool-schema.deeplogic-cli.console.log)
- [Run configuration](./runs/TC-213/inspect_config.yaml)
- [Original extracted MCP object](./artifacts/TC-213-firecrawl-mcp-tool-schema.tool.json)
