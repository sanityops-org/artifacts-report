# TC-239: RSS MCP Server (veithly/rss-mcp) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: veithly/rss-mcp (MCP server that fetches and parses any RSS/Atom feed, with RSSHub support)
- **License**: Apache License 2.0 (README "License" section; `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `get_feed` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/index.ts` — the `server.registerTool("get_feed", { description, inputSchema }, handler)` call, whose `inputSchema` is a Zod object
  - `README.md` — confirmed the single `get_feed` tool and Apache-2.0 license

## Original Artifact Content

### Tool registration (`src/index.ts`, fetched verbatim)

```typescript
// Register the get_feed tool using the modern McpServer API
server.registerTool(
    "get_feed",
    {
        description: "Get RSS feed from any URL, including RSSHub feeds.",
        inputSchema: {
            url: z.string().describe("URL of the RSS feed. For RSSHub, you can use 'rsshub://' protocol (e.g., 'rsshub://bilibili/user/dynamic/208259')."),
            count: z.number().optional().describe("Number of RSS feed items to retrieve. Defaults to 1. Set to 0 to retrieve all items.")
        }
    },
    async ({ url, count }) => {
        try {
            console.error(`Tool called with URL: ${url} and count: ${count}`);
            const feedResult = await get_feed({ url, count });
            console.error(`Tool completed successfully for URL: ${url}`);
            return {
                content: [{ type: "text", text: JSON.stringify(feedResult, null, 2) }]
            };
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
            console.error(`Tool error for URL ${url}: ${errorMessage}`);
            // Always return a valid response, never throw
            return {
                content: [{ type: "text", text: `Error fetching RSS feed: ${errorMessage}` }],
                isError: true
            };
        }
    }
);
```

### The `get_feed` implementation signature (`src/index.ts`, fetched verbatim)

```typescript
export async function get_feed(params: { url: string, count?: number }): Promise<RssFeed> {
```

> The `inputSchema` is authored as a Zod object literal (`z.string()`, `z.number().optional()`) and converted to JSON Schema by the MCP SDK. The `RssFeed` output shape (title, link, description, items[]) is described in `README.md`.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Get RSS feed from any URL") and the RSSHub extension ("including RSSHub feeds")
- [ ] The description implies supported inputs (any standard RSS/Atom URL, or an `rsshub://` URL)
- [ ] No marketing-only text that omits functional capability

### 2. JSON Schema Correctness
- [ ] The Zod schema converts to a valid JSON Schema object (`type: "object"`, `properties`)
- [ ] Types are accurate (`url`: string; `count`: number, optional)
- [ ] `url` is effectively required (declared without `.optional()`); `count` is optional
- [ ] No spurious constraints that contradict runtime behavior

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] The default is documented inline (`count` defaults to 1)
- [ ] The sentinel value is explained (`count: 0` retrieves all items)
- [ ] The `rsshub://` protocol form is shown with a concrete example

### 4. Integration Compatibility
- [ ] Conforms to the modern MCP SDK `registerTool(name, { description, inputSchema }, handler)` API
- [ ] Runs over the stdio transport (`StdioServerTransport`)
- [ ] Errors are returned as `isError` tool results rather than thrown, so the model can react
- [ ] Supports optional `PRIORITY_RSSHUB_INSTANCE` configuration without changing the schema

### 5. Extensibility & Maintainability
- [ ] A single exported `get_feed` function backs the tool registration, so logic and schema stay colocated
- [ ] RSSHub instances are held in one list with polling/failover, isolating transport concerns from the schema
- [ ] Consistent single-verb naming (`get_feed`)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 20% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 25% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "fetch the latest posts from https://news.ycombinator.com/rss"; verify `get_feed` is called with that `url`.
2. Issue "get the latest Bilibili dynamics for user 208259"; verify `url: "rsshub://bilibili/user/dynamic/208259"` or a full RSSHub URL.
3. Issue "get the 5 most recent items from this feed"; verify `count: 5`.

### Boundary Test Cases
1. `count` omitted; verify the documented default of 1 item.
2. `count: 0`; verify all items are requested (the documented sentinel).
3. A URL given without a scheme; verify the documented auto-prefix to `rsshub://`.
4. A primary RSSHub instance down; verify the polling mechanic falls through to the next instance without a schema change.

### Negative Test Cases
1. `get_feed` without the required `url`; verify schema validation rejects the call.
2. `url` provided as a number/object; verify type validation rejects it.
3. An unreachable feed URL; verify an `isError: true` text result ("Error fetching RSS feed: ...") is returned rather than an exception.
4. A non-feed HTML page; verify the parse failure is surfaced as a tool error, not a fabricated feed.

## Notes
- This is one logical artifact: the `get_feed` tool. The server exposes exactly this one tool.
- The verbatim `inputSchema` is authored as Zod (`z.string().describe(...)`, `z.number().optional().describe(...)`); the MCP SDK generates the JSON Schema that clients see, so the code is quoted as the schema source per the rule for generated schemas.
- License is Apache-2.0; long verbatim quotation is permissible.
