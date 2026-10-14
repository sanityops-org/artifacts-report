# TC-202: Exa MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: exa-labs/exa-mcp-server (official Exa MCP server)
- **License**: MIT (Copyright (c) 2025 Exa Labs)
- **Artifact Type**: Tool Schema (MCP tool definition for the `web_search_exa` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/webSearch.ts` — tool registration, description, parameter schema (`query`, `numResults`) and annotations
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool registration and schema (`src/tools/webSearch.ts`, fetched verbatim)

```typescript
import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { API_CONFIG, createExaClient, integrationHeaders } from "./config.js";
import { ExaSearchRequest, ExaSearchResponse } from "../types.js";
import { createRequestLogger } from "../utils/logger.js";
import { retryWithBackoff, formatToolError, withTimeout } from "../utils/errorHandler.js";
import { sanitizeSearchResponse } from "../utils/exaResponseSanitizer.js";
import { lenientString, lenientOptionalNumber } from "./validation.js";
import { checkpoint } from "agnost";

type WebSearchConfig = {
  exaApiKey?: string;
  userProvidedApiKey?: boolean;
  defaultSearchType?: "auto" | "fast" | "instant";
  exaSource?: string;
  mcpSessionId?: string;
};

export function registerWebSearchTool(
  server: McpServer,
  config?: WebSearchConfig,
  toolName?: string,
): void {
  server.tool(
    toolName || "web_search_exa",
    `Search the web for any topic and get clean, ready-to-use content.
      Best for: Finding current information, news, facts, people, companies, or answering questions about any topic.
      Returns: Clean text content from top search results.
      Query tips:
      describe the ideal page, not keywords. "blog post comparing React and Vue performance" not "React vs Vue".
      Use category:people / category:company to search through Linkedin profiles / companies respectively.
      If highlights are insufficient, follow up with web_fetch_exa on the best URLs.`,
    {
      query: lenientString().describe(
        "Natural language search query. Should be a semantically rich description of the ideal page, not just keywords. Optionally include category:<type> (company, people) to focus results — e.g. 'category:people John Doe software engineer'.",
      ),
      numResults: lenientOptionalNumber().describe(
        "Number of search results to return (default: 10).",
      ),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: true,
      idempotentHint: true,
    },
    async ({ query, numResults }) => {
      const toolId = toolName || "web_search_exa";
      const logger = createRequestLogger(toolId);

      // Extract category:<type> from query string if present
      const categoryMatch = query.match(
        /\bcategory:(company|publication|news|personal\s*site|people)\b/i,
      );
      const category = categoryMatch
        ? (categoryMatch[1].toLowerCase().replace(/\s+/g, " ") as
            | "company"
            | "publication"
            | "news"
            | "personal site"
            | "people")
        : undefined;
      const cleanedQuery = categoryMatch
        ? query.replace(categoryMatch[0], "").replace(/\s+/g, " ").trim()
        : query;

      logger.start(cleanedQuery);
      try {
        const exa = createExaClient(config);
        const searchRequest: ExaSearchRequest = {
          query: cleanedQuery,
          type: config?.defaultSearchType || "auto",
          numResults: numResults || API_CONFIG.DEFAULT_NUM_RESULTS,
          ...(category && { category }),
          contents: {
            highlights: true,
          },
        };
        checkpoint("web_search_request_prepared");
        logger.log("Sending request to Exa API");
        const response = await withTimeout(
          () =>
            retryWithBackoff(() =>
              exa.request<ExaSearchResponse>(
                API_CONFIG.ENDPOINTS.SEARCH,
                "POST",
                searchRequest,
                undefined,
                integrationHeaders("web-search-mcp", config),
              ),
            ),
          API_CONFIG.TOOL_TIMEOUTS.SEARCH_MS,
          toolId,
        );
        checkpoint("exa_search_response_received");
        logger.log("Received response from Exa API");

        if (!response || !response.results || response.results.length === 0) {
          logger.log("Warning: Empty or invalid response from Exa API");
          checkpoint("web_search_complete");
          return {
            content: [
              {
                type: "text" as const,
                text: "No search results found. Please try a different query.",
              },
            ],
          };
        }

        logger.log(`Received ${response.results.length} results with highlights`);
        const sanitized = sanitizeSearchResponse(response);
        const results = Array.isArray(sanitized.results) ? sanitized.results : [];
        const formattedResults = results
          .map((r) => {
            const lines = [
              `Title: ${r.title || "N/A"}`,
              `URL: ${r.url}`,
              `Published: ${r.publishedDate || "N/A"}`,
              `Author: ${r.author || "N/A"}`,
            ];
            if (Array.isArray(r.highlights) && r.highlights.length > 0) {
              lines.push(`Highlights:\n${r.highlights.join("\n")}`);
            } else if (r.text) {
              lines.push(`Text: ${r.text}`);
            }
            return lines.join("\n");
          })
          .join("\n\n---\n\n");

        const searchTime =
          typeof sanitized.searchTime === "number" ? sanitized.searchTime : undefined;

        const result = {
          content: [
            {
              type: "text" as const,
              text: formattedResults,
              _meta: {
                searchTime: searchTime,
              },
            },
          ],
        };
        checkpoint("web_search_complete");
        logger.complete();
        return result;
      } catch (error) {
        logger.error(error);
        return formatToolError(error, toolId, config?.userProvidedApiKey);
      }
    },
  );
}
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete parameter schema with two fields (`query`, `numResults`)
- [ ] Parameter types are inferable (`query` is a string; `numResults` is a number)
- [ ] Required vs optional is distinguishable (only `query` is effectively required; `numResults` is described as optional with a default)
- [ ] The schema is authored with the `lenientString` / `lenientOptionalNumber` helpers rather than a raw `z.object`, so coercion behaviour is centralized

### 2. Description Clarity
- [ ] The tool description states what the tool does ("Search the web for any topic and get clean, ready-to-use content")
- [ ] It states when to use the tool ("Best for: Finding current information, news, facts, people, companies...")
- [ ] It states the return shape ("Returns: Clean text content from top search results")
- [ ] It includes non-obvious query guidance ("describe the ideal page, not keywords") and a disambiguation rule for `category:` prefixes

### 3. Integration Compatibility
- [ ] Conforms to the MCP tool model (`server.tool(name, description, params, annotations, handler)`)
- [ ] Provides `ToolAnnotations` (`readOnlyHint`, `destructiveHint`, `openWorldHint`, `idempotentHint`) consumed by MCP clients for risk display
- [ ] Zod schema is transpiled to JSON Schema by the MCP SDK, so it is consumable by standard function-calling clients

### 4. Example Quality
- [ ] The description embeds a concrete contrastive example ("blog post comparing React and Vue performance" not "React vs Vue")
- [ ] The `query` description embeds a concrete `category:people` example
- [ ] The default result count (10) is documented inline on `numResults`

### 5. Extensibility
- [ ] Tool registration is a factory (`registerWebSearchTool(server, config, toolName?)`) so the tool name and defaults can be overridden per profile
- [ ] Behaviour is configurable (`defaultSearchType`, `exaApiKey`, `exaSource`) without changing the schema
- [ ] Cross-tool guidance ("follow up with web_fetch_exa") documents composition with a sibling tool

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Schema Completeness | 25% | | |
| Description Clarity | 20% | | |
| Integration Compatibility | 25% | | |
| Example Quality | 20% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what did Exa announce this week?"; verify the model selects `web_search_exa` with a semantically rich `query` and, optionally, `numResults`.
2. Issue "find software engineers named Jane Doe on LinkedIn"; verify the model emits a `query` containing a `category:people` prefix, matching the documented convention.
3. Issue "give me 3 sources about vector databases"; verify `numResults: 3`.

### Boundary Test Cases
1. Omit `numResults`; verify the server falls back to `API_CONFIG.DEFAULT_NUM_RESULTS` (documented as 10).
2. Pass `numResults: 0` or a non-integer via the lenient number helper; verify coercion/validation behaviour matches `lenientOptionalNumber`.
3. A `query` containing `category:company` inside a longer sentence; verify the category is stripped before the API call (`cleanedQuery`).

### Negative Test Cases
1. Call the tool without `query`; verify schema validation rejects the call.
2. Pass `numResults` as a string; verify the lenient helper either coerces it or the call is rejected (behaviour should be explicit, not silently ignored).
3. Ambiguous request ("find stuff"); verify the model asks for a refinement or rewrites into a semantically rich query rather than sending a bare keyword.

## Notes
- This case quotes the single `web_search_exa` tool verbatim from the official Exa MCP server. The parameter schema is authored with the `lenientString` / `lenientOptionalNumber` helpers (defined in `src/tools/validation.ts`) and converted to JSON Schema by the MCP TypeScript SDK at registration time, so the schema the LLM receives is generated from this source.
- The server exposes several other tools (e.g. `web_fetch_exa`, `company_research_exa`, `people_search_exa`, agent tools); only the web-search tool is quoted here (one logical artifact per case).
- License is MIT, so verbatim quotation is permissible.
