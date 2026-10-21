# TC-191: Shopify MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: GeLi2001/shopify-mcp (MCP Server for the Shopify GraphQL Admin API)
- **License**: MIT (Copyright (c) 2023 Shopify MCP Server Contributors)
- **Artifact Type**: Tool Schema (MCP tool definition for the `get-products` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/getProducts.ts` — the `GetProductsInputSchema` (Zod) and the `getProducts` tool object
  - `src/tools/registry.ts` — the tool registry that exports all tools
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Input schema (`src/tools/getProducts.ts`, fetched verbatim)

```typescript
import { z } from "zod";

// Input schema for getProducts
const GetProductsInputSchema = z.object({
  searchTitle: z.string().optional().describe("Search by title (convenience filter, wraps in title:*...*). Use 'query' for advanced filtering."),
  limit: z.number().default(10),
  after: z.string().optional().describe("Cursor for forward pagination"),
  before: z.string().optional().describe("Cursor for backward pagination"),
  sortKey: z.enum([
    "CREATED_AT", "ID", "INVENTORY_TOTAL", "PRODUCT_TYPE",
    "PUBLISHED_AT", "RELEVANCE", "TITLE", "UPDATED_AT", "VENDOR"
  ]).optional().describe("Sort key for products"),
  reverse: z.boolean().optional().describe("Reverse the sort order"),
  query: z.string().optional().describe("Raw query string for advanced filtering (e.g. 'status:active vendor:Nike tag:sale')")
});

type GetProductsInput = z.infer<typeof GetProductsInputSchema>;
```

### Tool object (`src/tools/getProducts.ts`, fetched verbatim)

```typescript
const getProducts = {
  name: "get-products",
  description: "Get all products or search by title",
  schema: GetProductsInputSchema,

  // Add initialize method to set up the GraphQL client
  initialize(client: GraphQLClient) {
    shopifyClient = client;
  },

  execute: async (input: GetProductsInput) => { /* ... */ }
};

export { getProducts };
```

### Registration (`src/index.ts`, fetched verbatim)

```typescript
// Register all tools with the MCP server
for (const tool of tools) {
  server.tool(
    tool.name,
    tool.schema.shape,
    async (args) => {
      const result = await tool.execute(args);
      return {
        content: [{ type: "text", text: JSON.stringify(result) }]
      };
    }
  );
}
```

### Tool registry excerpt (`src/tools/registry.ts`, fetched verbatim)

```typescript
export const tools: ShopifyTool[] = [
  // Products (8)
  getProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
  manageProductVariants,
  deleteProductVariants,
  manageProductOptions,
  // Orders (10)
  getOrders,
  // ... (Orders, Customers, Metafields, Config, Inventory groups)
];
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`GetProductsInputSchema`)
- [ ] Types are accurate (`string`, `number`, `boolean`, `enum`)
- [ ] Required vs optional parameters are distinguishable (only `limit` has a default; the rest are `.optional()`)
- [ ] A default is declared (`limit: z.number().default(10)`)

### 2. Description Clarity
- [ ] The tool has a description ("Get all products or search by title")
- [ ] Each optional parameter carries a `.describe(...)` string
- [ ] Field-level descriptions explain relationships (e.g. "Use 'query' for advanced filtering") and give query examples (`'status:active vendor:Nike tag:sale'`)

### 3. Integration Compatibility
- [ ] Registered through the MCP SDK (`McpServer.tool(name, schema.shape, handler)`)
- [ ] Zod schema is converted to JSON Schema by the SDK, consumable by MCP clients and function-calling LLMs
- [ ] Tool result is returned as a text content block containing JSON

### 4. Example Quality
- [ ] Parameter descriptions embed concrete query DSL examples
- [ ] The `sortKey` enum enumerates all valid values
- [ ] Pagination parameters (`after`/`before`) are documented as cursors

### 5. Extensibility
- [ ] Tools follow a uniform `ShopifyTool` interface (`name`, `description`, `schema`, `initialize`, `execute`) declared in `src/lib/toolUtils.ts`
- [ ] Tools are collected in a single `registry.ts` array, so adding a tool requires one import + one array entry
- [ ] The shared GraphQL client is injected via `initialize`, decoupling tools from transport/auth

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
1. Issue "show me the latest 5 products in the store"; verify `get-products` is called with `limit: 5` (and possibly `sortKey: "CREATED_AT"`, `reverse: true`).
2. Issue "find products named 'Hoodie'"; verify `searchTitle: "Hoodie"` (or an equivalent `query`).
3. Issue "list active Nike products on sale"; verify `query: "status:active vendor:Nike tag:sale"`.

### Boundary Test Cases
1. `limit` omitted; verify the default (10) is applied.
2. `sortKey` set to a valid enum value (e.g. `INVENTORY_TOTAL`) with `reverse: true`.
3. Forward pagination: pass `after` with a cursor returned by a previous call; then backward pagination with `before`.
4. `searchTitle` combined with a raw `query`; verify both are merged server-side (`title:*...*` + raw query).

### Negative Test Cases
1. `sortKey: "PRICE"` (not in the enum); verify rejection.
2. `limit` provided as a string; verify type validation rejects it.
3. An unknown tool name; verify the server does not register/route it.
4. Ambiguous request "show me stuff"; verify the model asks for a refinement (title, status, vendor) rather than issuing an unbounded query.

## Notes
- This is a community Shopify MCP server. The `get-products` tool and its Zod input schema are quoted verbatim from `src/tools/getProducts.ts`; the registry and registration code are quoted for context. The server also exposes order, customer, metafield, inventory and configuration tools (one logical artifact = this one product-query tool).
- The input schema is authored in Zod and converted to JSON Schema at registration (`tool.schema.shape`), so the schema the LLM receives is generated from this source.
- License is MIT; verbatim quotation is permissible.
