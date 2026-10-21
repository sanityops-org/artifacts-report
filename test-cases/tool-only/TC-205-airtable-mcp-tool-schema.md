# TC-205: Airtable MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: domdomegg/airtable-mcp-server (MCP server for the Airtable Web API)
- **License**: MIT (Copyright (c) 2024 Adam Jones (domdomegg))
- **Artifact Type**: Tool Schema (MCP tool definition for the `list_records` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `master`:
  - `src/tools/list-records.ts` — the `list_records` tool registration, input schema and output schema
  - `src/tools/schemas.ts` — the shared `baseId` / `tableId` / `recordId` input-schema fragments
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool registration (`src/tools/list-records.ts`, fetched verbatim)

```typescript
import type {McpServer} from '@modelcontextprotocol/sdk/server/mcp.js';
import {z} from 'zod';
import type {ToolContext} from './types.js';
import {tableId} from './schemas.js';
import {jsonResult} from '../utils/response.js';

const outputSchema = z.object({
	records: z.array(z.object({
		id: z.string(),
		fields: z.record(z.string(), z.unknown()),
	})),
});

export function registerListRecords(server: McpServer, ctx: ToolContext): void {
	server.registerTool(
		'list_records',
		{
			title: 'List Records',
			description: 'List records from a table',
			inputSchema: {
				...tableId,
				view: z.string().optional().describe('The name or ID of a view in the table'),
				maxRecords: z.number().optional().describe('The maximum total number of records that will be returned'),
				filterByFormula: z.string().optional().describe('A formula used to filter records'),
				sort: z.array(z.object({
					field: z.string(),
					direction: z.enum(['asc', 'desc']).optional(),
				})).optional().describe('A list of sort objects that specifies how the records will be ordered'),
				fields: z.array(z.string()).optional().describe('An array of field names or IDs to include in the response. Omit this to return all fields, which is usually what you want. Only set it if the table has many fields and you don\'t need most of them, AND you already know the exact field names or IDs (e.g. from describe_table) - guessing them will silently return the wrong data.'),
			},
			outputSchema,
			annotations: {
				readOnlyHint: true,
			},
		},
		async (args) => {
			const records = await ctx.airtableService.listRecords(
				args.baseId,
				args.tableId,
				{
					view: args.view,
					maxRecords: args.maxRecords,
					filterByFormula: args.filterByFormula,
					sort: args.sort,
					fields: args.fields,
				},
			);
			return jsonResult(outputSchema.parse({records}));
		},
	);
}
```

### Shared input-schema fragments (`src/tools/schemas.ts`, fetched verbatim)

```typescript
import {z} from 'zod';

// Shared input schema fields for tools that operate on bases
export const baseId = {
	baseId: z.string().describe('The ID of the base'),
};

// Shared input schema fields for tools that operate on tables
export const tableId = {
	...baseId,
	tableId: z.string().describe('The ID or name of the table'),
};
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` built by spreading the shared `tableId` fragment (`baseId` + `tableId`)
- [ ] A typed `outputSchema` is declared and enforced (`outputSchema.parse({records})`)
- [ ] Types are accurate (`string`, `number`, `array`, nested `object` with an `enum` for sort direction)
- [ ] Required vs optional is clear (only `baseId` and `tableId` from the fragment are required; all others use `.optional()`)

### 2. Description Clarity
- [ ] The tool has a title (`List Records`) and description (`List records from a table`)
- [ ] Every optional parameter carries a `.describe(...)` string
- [ ] The `fields` description explains when NOT to use the parameter and warns about silent-wrong-data failure modes

### 3. Integration Compatibility
- [ ] Registered through the MCP SDK (`server.registerTool(name, config, handler)`)
- [ ] Declares annotations (`readOnlyHint: true`) for client-side risk display
- [ ] Zod schemas are converted to JSON Schema by the SDK, so they are consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] The `fields` description embeds a concrete example workflow ("e.g. from describe_table")
- [ ] The `sort` parameter documents its nested object shape (a list of `{field, direction}` objects)
- [ ] The `filterByFormula` parameter names the Airtable concept it maps to

### 5. Extensibility
- [ ] Shared schema fragments (`baseId`, `tableId`, `recordId`) live in one module and are spread into multiple tools, keeping identifiers consistent
- [ ] Tools follow a `registerX(server, ctx)` convention, so tools are added by importing and invoking a register function
- [ ] The `outputSchema` doubles as a runtime validator via `parse`, keeping output shape and validation in sync

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
1. Issue "list the records in the 'Projects' table"; verify `list_records` is called with `baseId` and `tableId: "Projects"`.
2. Issue "show me the 5 most recent records"; verify `maxRecords: 5` (and, if the model sorts, a `sort` array with a `direction`).
3. Issue "list records sorted by name descending"; verify `sort: [{ field: "name", direction: "desc" }]`.

### Boundary Test Cases
1. `sort` omitted; verify the schema accepts it and the request returns the default Airtable ordering.
2. `filterByFormula` set to a valid Airtable formula; verify it is passed through unchanged.
3. `maxRecords` set to 1; verify the schema accepts the minimum sensible value.
4. `fields` omitted (the recommended default); verify all fields are returned.

### Negative Test Cases
1. Call `list_records` without `baseId` or `tableId`; verify schema validation rejects the call.
2. `sort[].direction` set to an out-of-enum value such as `"ascending"`; verify rejection.
3. `maxRecords` passed as a string; verify type validation rejects it.
4. `fields` set to guessed field names that do not exist; verify the documented failure mode (silently wrong data) is treated as a known risk, and the model is steered to call `describe_table` first.

## Notes
- This case quotes the single `list_records` tool verbatim from `src/tools/list-records.ts`, plus the shared `baseId`/`tableId` fragments it depends on from `src/tools/schemas.ts`. The input and output schemas are authored in Zod and converted to JSON Schema by the MCP TypeScript SDK, so the schema the LLM receives is generated from this source.
- The server exposes a full set of base/table/record tools (e.g. `list_bases`, `list_tables`, `describe_table`, `create_record`, `update_records`, `delete_records`, `upload_attachment`); only `list_records` is quoted here (one logical artifact per case).
- License is MIT; verbatim quotation is permissible.
