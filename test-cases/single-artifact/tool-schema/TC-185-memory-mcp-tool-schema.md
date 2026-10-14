# TC-185: Memory MCP Server (Knowledge Graph) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers (reference server `src/memory`)
- **License**: MIT / Apache-2.0 (this repository is transitioning from MIT to Apache-2.0; see `LICENSE` — "Apache License 2.0 for new contributions, with existing code under MIT")
- **Artifact Type**: Tool Schema (MCP tool definitions for a knowledge-graph memory server: nine tools)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/memory/index.ts` — zod input schemas, tool registration blocks and the knowledge-graph resource
  - `LICENSE` — confirmed MIT/Apache-2.0 dual-license transition

## Original Artifact Content

### Shared zod schemas (`src/memory/index.ts`, fetched verbatim)

```typescript
// Zod schemas for entities and relations
const EntitySchema = z.object({
  name: z.string().describe("The name of the entity"),
  entityType: z.string().describe("The type of the entity"),
  observations: z
    .array(z.string())
    .describe("An array of observation contents associated with the entity"),
});

const RelationSchema = z.object({
  from: z.string().describe("The name of the entity where the relation starts"),
  to: z.string().describe("The name of the entity where the relation ends"),
  relationType: z.string().describe("The type of the relation"),
});

const RESOURCE_URI = "memory://knowledge-graph";

export const SEARCH_QUERY_MAX_LENGTH = 2048;

export const SearchNodesQuerySchema = z
  .string()
  .max(SEARCH_QUERY_MAX_LENGTH)
  .describe(
    "The search query to match against entity names, types, and observation content",
  );
```

### Tool registration blocks (`src/memory/index.ts`, fetched verbatim)

```typescript
  // Register create_entities tool
  server.registerTool(
    "create_entities",
    {
      title: "Create Entities",
      description:
        "Create multiple new entities in the knowledge graph. An entity whose name already exists, or repeats an earlier entity in the same call, is skipped and its observations are not added; the result lists the skipped names in `skipped`. Use add_observations to add observations to an existing entity.",
      inputSchema: {
        entities: z.array(EntitySchema),
      },
      outputSchema: {
        entities: z.array(EntitySchema),
        // Present only when at least one requested entity was skipped.
        skipped: z.array(z.string()).optional(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ entities }) => { /* ... */ },
  );

  // Register create_relations tool
  server.registerTool(
    "create_relations",
    {
      title: "Create Relations",
      description:
        "Create multiple new relations between entities in the knowledge graph. Relations should be in active voice",
      inputSchema: {
        relations: z.array(RelationSchema),
      },
      outputSchema: {
        relations: z.array(RelationSchema),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ relations }) => { /* ... */ },
  );

  // Register add_observations tool
  server.registerTool(
    "add_observations",
    {
      title: "Add Observations",
      description:
        "Add new observations to existing entities in the knowledge graph",
      inputSchema: {
        observations: z.array(
          z.object({
            entityName: z
              .string()
              .describe("The name of the entity to add the observations to"),
            contents: z
              .array(z.string())
              .describe("An array of observation contents to add"),
          }),
        ),
      },
      outputSchema: {
        results: z.array(
          z.object({
            entityName: z.string(),
            addedObservations: z.array(z.string()),
          }),
        ),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ observations }) => { /* ... */ },
  );

  // Register delete_entities tool
  server.registerTool(
    "delete_entities",
    {
      title: "Delete Entities",
      description:
        "Delete multiple entities and their associated relations from the knowledge graph",
      inputSchema: {
        entityNames: z
          .array(z.string())
          .describe("An array of entity names to delete"),
      },
      outputSchema: {
        success: z.boolean(),
        message: z.string(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ entityNames }) => { /* ... */ },
  );

  // Register delete_observations tool
  server.registerTool(
    "delete_observations",
    {
      title: "Delete Observations",
      description:
        "Delete specific observations from entities in the knowledge graph",
      inputSchema: {
        deletions: z.array(
          z.object({
            entityName: z
              .string()
              .describe("The name of the entity containing the observations"),
            observations: z
              .array(z.string())
              .describe("An array of observations to delete"),
          }),
        ),
      },
      outputSchema: {
        success: z.boolean(),
        message: z.string(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ deletions }) => { /* ... */ },
  );

  // Register delete_relations tool
  server.registerTool(
    "delete_relations",
    {
      title: "Delete Relations",
      description: "Delete multiple relations from the knowledge graph",
      inputSchema: {
        relations: z
          .array(RelationSchema)
          .describe("An array of relations to delete"),
      },
      outputSchema: {
        success: z.boolean(),
        message: z.string(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ relations }) => { /* ... */ },
  );

  // Register read_graph tool
  server.registerTool(
    "read_graph",
    {
      title: "Read Graph",
      description: "Read the entire knowledge graph",
      inputSchema: {},
      outputSchema: {
        entities: z.array(EntitySchema),
        relations: z.array(RelationSchema),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async () => { /* ... */ },
  );

  // Register search_nodes tool
  server.registerTool(
    "search_nodes",
    {
      title: "Search Nodes",
      description: "Search for nodes in the knowledge graph based on a query",
      inputSchema: {
        query: SearchNodesQuerySchema,
      },
      outputSchema: {
        entities: z.array(EntitySchema),
        relations: z.array(RelationSchema),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ query }) => { /* ... */ },
  );

  // Register open_nodes tool
  server.registerTool(
    "open_nodes",
    {
      title: "Open Nodes",
      description: "Open specific nodes in the knowledge graph by their names",
      inputSchema: {
        names: z
          .array(z.string())
          .describe("An array of entity names to retrieve"),
      },
      outputSchema: {
        entities: z.array(EntitySchema),
        relations: z.array(RelationSchema),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ names }) => { /* ... */ },
  );
```

> Note: the `async (...) => { ... }` handler bodies are elided above with `/* ... */`; the tool names, titles, descriptions, `inputSchema`, `outputSchema` and `annotations` are quoted verbatim from the fetched source.

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Nine tools each declare an `inputSchema` (or an empty `{}` for `read_graph`, which takes no arguments)
- [ ] Input and `outputSchema` are both declared, giving the model typed expectations
- [ ] Nested/array structures (`entities[]`, `relations[]`, `observations[]`, `deletions[]`, `names[]`) are fully typed
- [ ] Constraints are present (`SearchNodesQuerySchema` with `.max(2048)`)

### 2. Description Clarity
- [ ] Each tool has a title and a description stating its purpose
- [ ] `create_entities` description documents skip semantics and points to `add_observations` for existing entities
- [ ] Field-level `.describe(...)` texts explain each sub-parameter

### 3. Integration Compatibility
- [ ] Registered through the MCP `McpServer.registerTool` API with zod schemas → JSON Schema
- [ ] `annotations` expose `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint` for client risk assessment
- [ ] A companion subscribable resource (`memory://knowledge-graph`) is registered alongside the tools

### 4. Example Quality
- [ ] Descriptions embed usage rules, e.g. relations "should be in active voice"
- [ ] The `skipped` output field is documented as "Present only when at least one requested entity was skipped"
- [ ] Delete tools return a human-readable `message` describing partial success

### 5. Extensibility
- [ ] Shared `EntitySchema` / `RelationSchema` are reused across tools
- [ ] The graph is persisted as JSONL with a documented file-path override (`MEMORY_FILE_PATH`)
- [ ] New tools can reuse the same zod building blocks and annotation convention

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
1. Issue "remember that Alice works at Acme as an engineer"; verify `create_entities` (Alice, Acme) and/or `create_relations` (Alice → works_at → Acme) are called with well-formed objects.
2. Issue "what do you know about Alice?"; verify `search_nodes` with a `query` or `open_nodes` with `names`.
3. Issue "Alice left Acme"; verify `delete_relations` and/or `add_observations` are used rather than `create_entities`.

### Boundary Test Cases
1. `create_entities` with an entity whose name already exists; verify the `skipped` output and the notice text are returned.
2. `search_nodes` with a query at the 2048-character limit; verify acceptance, and rejection above it.
3. `read_graph` called with `{}`; verify no-argument invocation succeeds.
4. A batch of entities with one duplicate inside the same call.

### Negative Test Cases
1. `open_nodes` without `names`; verify schema validation rejects the call.
2. An entity object missing `entityType`; verify rejection against `EntitySchema`.
3. A relation using passive phrasing that yields an ambiguous direction; verify the model normalizes per "active voice" guidance.
4. Destructive tools (`delete_entities`) on a non-existent name; verify the tool reports "not found" instead of failing silently.

## Notes
- This is the official MCP Memory reference server; the nine tools together are one tightly-related tool group from a single file and are documented as one logical artifact.
- The schemas are authored in Zod and converted to JSON Schema by the MCP TypeScript SDK; `inputSchema: {}` for `read_graph` is quoted exactly as in the source.
- License is MIT/Apache-2.0 (repository is mid-transition); verbatim quotation is permissible.
