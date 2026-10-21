# TC-190: Google Drive MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers-archived (reference server `src/gdrive`)
- **License**: MIT (Copyright (c) 2024 Anthropic, PBC)
- **Artifact Type**: Tool Schema (MCP tool definition for the `search` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/gdrive/index.ts` — the `search` tool definition, list/resources handlers and server setup
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definition (`src/gdrive/index.ts`, fetched verbatim)

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search",
        description: "Search for files in Google Drive",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});
```

### Call-tool handler (`src/gdrive/index.ts`, fetched verbatim)

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "search") {
    const userQuery = request.params.arguments?.query as string;
    const escapedQuery = userQuery.replace(/\\/g, "\\\\").replace(/'/g, "\\'");
    const formattedQuery = `fullText contains '${escapedQuery}'`;

    const res = await drive.files.list({
      q: formattedQuery,
      pageSize: 10,
      fields: "files(id, name, mimeType, modifiedTime, size)",
    });

    const fileList = res.data.files
      ?.map((file: any) => `${file.name} (${file.mimeType})`)
      .join("\n");
    return {
      content: [
        {
          type: "text",
          text: `Found ${res.data.files?.length ?? 0} files:\n${fileList}`,
        },
      ],
      isError: false,
    };
  }
  throw new Error("Tool not found");
});
```

### Server / resource wiring (`src/gdrive/index.ts`, fetched verbatim)

```typescript
const server = new Server(
  {
    name: "example-servers/gdrive",
    version: "0.1.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  },
);
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool declares `type: "object"`, `properties` and `required`
- [ ] The parameter `query` is typed as `string`
- [ ] `query` is correctly marked required
- [ ] A companion resource capability (`resources: {}`) exposes file listing/reading separately from the tool

### 2. Description Clarity
- [ ] The tool has a functional description ("Search for files in Google Drive")
- [ ] The single parameter has a description ("Search query")
- [ ] The response text is human-readable ("Found N files: ...")

### 3. Integration Compatibility
- [ ] Uses the MCP `Server` with standard `ListToolsRequestSchema` / `CallToolRequestSchema` handlers
- [ ] JSON-Schema `inputSchema` is directly consumable by MCP clients and function-calling LLMs
- [ ] Runs `google.drive("v3")` with an OAuth credential loaded from a local file

### 4. Example Quality
- [ ] The handler demonstrates the query-translation pattern (free-text → Drive `fullText contains` query)
- [ ] Input is escaped to reduce query-injection risk
- [ ] Handles the empty-result case gracefully

### 5. Extensibility
- [ ] Read-only scope (`drive.readonly`) is requested during auth
- [ ] File listing is also exposed as a subscribable-style resource, so search and enumeration are separated
- [ ] Credential paths are configurable via environment variables (`GDRIVE_CREDENTIALS_PATH`, `GDRIVE_OAUTH_PATH`)

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
1. Issue "find the quarterly report in my Drive"; verify `search` is called with a `query` string.
2. Issue "look for anything mentioning 'invoice'"; verify the free-text query is translated to `fullText contains 'invoice'`.
3. After a search, list resources to confirm file enumeration works alongside the tool.

### Boundary Test Cases
1. A query containing a single quote or backslash; verify escaping prevents a malformed Drive query.
2. A query with zero matches; verify "Found 0 files:" is returned without error.
3. A very broad query matching many files; verify the `pageSize: 10` cap is reflected in the response.
4. A non-string `query` value; verify validation rejects it.

### Negative Test Cases
1. `search` without `query`; verify schema validation rejects the call.
2. An unknown tool name; verify the handler throws "Tool not found".
3. Missing credentials file; verify the server refuses to start with a clear message.
4. Ambiguous request "get the file"; verify the model asks which file / performs a search rather than blindly guessing an ID.

## Notes
- This is the archived MCP Google Drive reference server. The single `search` tool is documented here as one logical artifact; file reading/enumeration lives in the resource handlers, which are quoted for context.
- The `inputSchema` is hand-written JSON Schema; note that the tool intentionally exposes a single free-text `query` and performs Drive-query translation server-side.
- License is MIT; verbatim quotation is permissible.
