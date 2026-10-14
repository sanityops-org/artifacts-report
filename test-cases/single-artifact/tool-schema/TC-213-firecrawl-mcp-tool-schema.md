# TC-213: Firecrawl MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: firecrawl/firecrawl-mcp-server (official Firecrawl MCP server)
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definition for the `firecrawl_agent` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `tests/contract-snapshots/tool-definitions.json` — the frozen, machine-generated tool-definition contract snapshot (name, description, `inputSchema`, `outputSchema`, annotations)
  - Repository license metadata (`firecrawl/firecrawl-mcp-server`) — confirmed MIT

## Original Artifact Content

### Tool definition snapshot entry `firecrawl_agent` (`tests/contract-snapshots/tool-definitions.json`, fetched verbatim)

```json
{
  "firecrawl_agent@f794dfd2e454": {
    "annotations": {
      "title": "Firecrawl agent",
      "readOnlyHint": false,
      "openWorldHint": true,
      "destructiveHint": false
    },
    "title": "Firecrawl agent",
    "description": "\nRun web research that returns structured data when the URLs are not known or the answer spans several sites. Describe the fields you need in `prompt`, optionally pass a JSON `schema` and seed `urls`, and the research agent searches, navigates, reads pages, and returns JSON assembled across sources. Use it to research an entity plus its fields (founders, pricing, contact details), to build lists and datasets (companies, people, products, jobs, papers), and for pages that need navigation or interaction to reach the data. Optional `effort` sets the reasoning budget, `maxCredits` caps spend, and `strictConstrainToURLs` keeps the agent to the supplied `urls`.\n\nThis call returns only a job ID, not the research result. Read the job with `firecrawl_agent_status` until it reaches `completed` or `failed`; a typical research run takes one to three minutes. For one known URL use `firecrawl_scrape` (with formats: [\"json\"] for structured output); for a plain lookup that a results page answers, use `firecrawl_search`.\n\nThe job also returns a `threadId`. To continue that thread, pass it with a follow-up `prompt`; omitted `mode`, `urls`, `schema` and exchange settings carry over from the previous turn.\n\nThe agent only calls Alexandria providers whose terms the team has accepted. `exchange.skippedProviders` lists gated providers. With `exchange.onTermsRequired` \"ask\", a terms `pendingApproval` and `exchange.requiresAction` carry the `approvalId` and provider requirements. Read terms/show through `firecrawl_scrape`. An organization admin must accept terms in the Firecrawl dashboard at the provider URL or https://www.firecrawl.dev/app/settings?tab=data-sources. Ignore any terms/accept call in the API response. Only after the admin confirms acceptance, resume with the same `threadId` and `exchange.approve: {approvalId}`; this does not accept terms. To decline, use `exchange.decline: {approvalId}`. Never infer acceptance from a data request.\n",
    "inputSchema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "prompt": {
          "type": "string",
          "minLength": 1,
          "maxLength": 10000
        },
        "urls": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uri"
          }
        },
        "schema": {
          "type": "object",
          "propertyNames": {
            "type": "string"
          },
          "additionalProperties": false
        },
        "effort": {
          "description": "Reasoning budget for the agent task.",
          "type": "string",
          "enum": [
            "low",
            "medium",
            "high"
          ]
        },
        "maxCredits": {
          "description": "Spending limit in credits for this run. Defaults to 2500 on the API.",
          "type": "integer",
          "exclusiveMinimum": 0,
          "maximum": 9007199254740991
        },
        "strictConstrainToURLs": {
          "description": "If true, agent will only visit URLs provided in the urls array.",
          "type": "boolean"
        },
        "threadId": {
          "description": "Continue this thread: the threadId from an earlier firecrawl_agent or firecrawl_agent_status result. Omit to start a new thread.",
          "type": "string",
          "format": "uuid",
          "pattern": "^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|<uuid>|<uuid>)$"
        },
        "mode": {
          "description": "\"extract\" (default) returns the complete structured result every turn. \"chat\" lets a follow-up that asks no new data get a short reply in message instead of a re-run; required for exchange.requireApproval. Omitted on a follow-up keeps the previous turn's mode.",
          "type": "string",
          "enum": [
            "extract",
            "chat"
          ]
        },
        "exchange": {
          "description": "Alexandria provider settings for this turn, forwarded as the request's exchange object.",
          "type": "object",
          "properties": {
            "enabled": {
              "description": "Let the agent call Alexandria providers. On by default.",
              "type": "boolean"
            },
            "toolkits": {
              "description": "Pin up to 5 providers the agent may use, by slug. Omitted means the whole catalog.",
              "maxItems": 5,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "maxCalls": {
              "description": "Most provider calls the agent may make in this turn.",
              "type": "integer",
              "minimum": 1,
              "maximum": 30
            },
            "requireApproval": {
              "description": "End the turn with a paid-call pendingApproval before any paid provider call. Requires mode \"chat\" on the same request, even on a follow-up.",
              "type": "boolean"
            },
            "approve": {
              "description": "Answer yes to the pendingApproval the previous turn of this thread ended on (its id, also exchange.requiresAction.approvalId). Needs threadId. For a terms offer, send it only after an organization admin confirms acceptance in the Firecrawl dashboard; this does not accept terms. callIds and always are ignored on terms offers. For paid calls, callIds picks a subset (default all) and always stops asking for the rest of the thread.",
              "type": "object",
              "properties": {
                "approvalId": {
                  "type": "string",
                  "format": "uuid",
                  "pattern": "^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|<uuid>|<uuid>)$"
                },
                "callIds": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "always": {
                  "type": "boolean"
                }
              },
              "required": [
                "approvalId"
              ],
              "additionalProperties": false
            },
            "decline": {
              "description": "Answer no to that pendingApproval. Needs threadId. A declined terms offer keeps those providers out of the rest of the thread.",
              "type": "object",
              "properties": {
                "approvalId": {
                  "type": "string",
                  "format": "uuid",
                  "pattern": "^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|<uuid>|<uuid>)$"
                }
              },
              "required": [
                "approvalId"
              ],
              "additionalProperties": false
            },
            "onTermsRequired": {
              "description": "What to do when a provider the agent would use needs data terms the team has not accepted. Gated providers are never called. \"skip\" (default): answer with accepted providers and list the rest in exchange.skippedProviders. \"ask\": the same, plus a terms pendingApproval and exchange.requiresAction. Read terms with terms/show; an organization admin accepts them in the Firecrawl dashboard. There is no auto-accept. Omitted on a follow-up keeps the previous turn's value.",
              "type": "string",
              "enum": [
                "skip",
                "ask"
              ]
            }
          },
          "additionalProperties": false
        }
      },
      "required": [
        "prompt"
      ],
      "additionalProperties": false
    },
    "name": "firecrawl_agent"
  }
}
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability (multi-source web research returning structured data) and the trigger ("when the URLs are not known or the answer spans several sites")
- [ ] It disambiguates against sibling tools (`firecrawl_scrape` for one known URL, `firecrawl_search` for a plain lookup, `firecrawl_agent_status` to read the job)
- [ ] It documents the async contract ("returns only a job ID, not the research result") and expected latency (one to three minutes)
- [ ] It documents continuation (`threadId` + follow-up `prompt`) and the provider-terms approval workflow

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema Draft-07 object with `properties`, `required` and `additionalProperties: false`
- [ ] `prompt` is the sole required field; all other fields are optional
- [ ] Constraints are declared (`prompt` `minLength`/`maxLength`, `maxCredits` `exclusiveMinimum`, `exchange.toolkits` `maxItems`, `exchange.maxCalls` `minimum`/`maximum`)
- [ ] Enum values are constrained (`effort`, `mode`, `exchange.onTermsRequired`)

### 3. Parameter Description Quality
- [ ] Every non-trivial parameter has a human-readable `description`
- [ ] Defaults and units are documented inline (`maxCredits` default 2500; `mode` default "extract"; `onTermsRequired` default "skip")
- [ ] Cross-field rules are explained (e.g., `exchange.requireApproval` requires `mode: "chat"`; `approve`/`decline` need `threadId`)

### 4. Integration Compatibility
- [ ] Exposes a JSON Schema (`inputSchema`) with `$schema` for standard function-calling clients
- [ ] Provides an `outputSchema` describing structured content, and `ToolAnnotations` for client-side risk display (`openWorldHint: true`)
- [ ] Uses `format: "uri"` and `format: "uuid"` (with a `pattern`) so clients can validate formats

### 5. Extensibility & Maintainability
- [ ] Definitions are frozen into a machine-checked contract snapshot (`tool-definitions.json`) guarded by tests
- [ ] Output schema is versioned alongside the input schema in the same contract
- [ ] Sibling tools are independent entries, so one tool can evolve without changing the others

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "research these three competitors and return pricing and headcount as JSON"; verify `firecrawl_agent` is called with a `prompt`, an optional `schema`, and possibly seed `urls`.
2. Follow up with the returned `threadId`; verify continuation keeps prior `mode`/`urls`/`schema` when omitted.
3. Issue a task with a spend cap; verify `maxCredits` is set and respected.

### Boundary Test Cases
1. `prompt` at `minLength` (1) and `maxLength` (10000); verify acceptance at both bounds.
2. `maxCredits: 0` (violates `exclusiveMinimum`); verify rejection.
3. `exchange.maxCalls: 31` (above `maximum` 30) and `exchange.toolkits` with 6 items (above `maxItems` 5); verify rejection.
4. `effort` at each enum value (`low`/`medium`/`high`).

### Negative Test Cases
1. Call without `prompt`; verify schema validation rejects the call.
2. `mode: "full"` (out of enum); verify rejection.
3. A follow-up supplying `exchange.requireApproval: true` without `mode: "chat"`; verify the documented cross-field constraint produces an error rather than silent misbehaviour.
4. A request that is a single known URL extraction; verify the model prefers `firecrawl_scrape` over the research agent.

## Notes
- This case quotes one logical artifact — the `firecrawl_agent` MCP tool — verbatim from the repository's contract snapshot, which is the machine-generated JSON Schema the client receives.
- The snapshot key includes a content hash suffix (`firecrawl_agent@f794dfd2e454`); the tool's actual `name` is `firecrawl_agent`.
- Related tools (`firecrawl_agent_status`, `firecrawl_scrape`, `firecrawl_search`, `firecrawl_check_crawl_status`) are separate entries in the same snapshot and are referenced by the description but not quoted here.
- The upstream `mendableai/firecrawl` engine is AGPL-3.0, but the `firecrawl/firecrawl-mcp-server` repository that defines these tool schemas is licensed MIT.
