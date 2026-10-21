# TC-246: CDC Health MCP Server (cyanheads/cdc-health-mcp-server) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: cyanheads/cdc-health-mcp-server (TypeScript MCP server wrapping the CDC Open Data portal — ~1,080 datasets — via the Socrata SODA API v2.1; public-health / end-user data domain)
- **License**: Apache License 2.0 (Copyright 2026 Casey Hand @cyanheads; `LICENSE` and `package.json` `"license": "Apache-2.0"`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `cdc_discover_datasets` tool, authored as a Zod schema via the `@cyanheads/mcp-ts-core` `tool(name, {...})` builder)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `HEAD` (resolved at fetch time to commit `9ebab18bab062a8e1bfe51a996c74410dc948356`):
  - `https://raw.githubusercontent.com/cyanheads/cdc-health-mcp-server/HEAD/src/mcp-server/tools/definitions/discover-datasets.tool.ts` — the full `tool('cdc_discover_datasets', { description, annotations, errors, input, output, enrichment, enrichmentTrailer, handler })` definition
  - `https://raw.githubusercontent.com/cyanheads/cdc-health-mcp-server/HEAD/LICENSE` — confirmed Apache-2.0 ("Copyright 2026 Casey Hand @cyanheads")
  - `https://raw.githubusercontent.com/cyanheads/cdc-health-mcp-server/HEAD/package.json` — confirmed `"license": "Apache-2.0"`, `"name": "@cyanheads/cdc-health-mcp-server"`
  - `https://raw.githubusercontent.com/cyanheads/cdc-health-mcp-server/HEAD/CLAUDE.md` — server protocol / domain notes (tool list, Socrata endpoints, quirks)
  - Directory listing via `https://github.com/cyanheads/cdc-health-mcp-server/tree/HEAD/src/mcp-server/tools/definitions`

## Original Artifact Content

### Schema constants referenced by the tool (`discover-datasets.tool.ts`, fetched verbatim)

```typescript
/**
 * Max characters of a dataset description carried in discovery output before truncation.
 * The budget is spent on visible text: markup comes off first, so a description that opens
 * with a styled block does not hand its whole allowance to tags and inline CSS.
 */
const DESCRIPTION_MAX = 300;
/** Max column field names listed in the discovery sample. */
const COLUMN_SAMPLE_MAX = 8;
/**
 * Socrata's Discovery API rejects a request with a nonzero `offset` whose `offset + limit`
 * exceeds this ceiling, with a 400 pointing at its deep-scrolling API; at `offset=0` it
 * answers any `limit` (measured live: `limit=50000` returns 200). Both CDC portals hold far
 * fewer entries than this, so the ceiling is unreachable by legitimate paging and every
 * request that crosses it is a caller error worth catching before the round trip. It also
 * bounds `limit`, which no page can usefully exceed.
 */
const CATALOG_PAGE_WINDOW_MAX = 10_000;
/**
 * Most entries one call returns. `limit` sizes the Discovery API `limit`, so it is a workload
 * cap: a full page of 100 already serializes to about 158,000 characters, and a larger
 * `limit` is clamped to it and the clamp disclosed, rather than the call rejected.
 */
const MAX_LIMIT = 100;
```

### Shared enrichment sub-schema (`discover-datasets.tool.ts`, fetched verbatim)

```typescript
const AppliedFiltersSchema = z.object({
  query: z.string().optional().describe('Search query used.'),
  category: z.string().optional().describe('Category filter used.'),
  tags: z
    .array(z.string())
    .optional()
    .describe('Tag filters used — a dataset matched when it carried any one of them.'),
});
```

### Tool definition — `cdc_discover_datasets` (`discover-datasets.tool.ts`, fetched verbatim; `handler` body omitted with a pointer)

```typescript
export const discoverDatasets = tool('cdc_discover_datasets', {
  description:
    'Search the CDC dataset catalog by keyword, category, or tag. Returns IDs, names, truncated descriptions, asset types, column counts, and update timestamps. The catalog also holds charts, maps, stories, files, and links; an entry whose columnCount is 0 is one of those and yields no data from the other tools. Use cdc_get_dataset_schema for the full column list of a chosen dataset.',
  annotations: { readOnlyHint: true },
  errors: [
    {
      reason: 'rate_limited',
      code: JsonRpcErrorCode.RateLimited,
      when: 'Socrata API returns 429 Too Many Requests.',
      retryable: true,
      recovery: 'Retry after a brief delay; the request was rate-limited.',
    },
    {
      reason: 'dataset_not_found',
      code: JsonRpcErrorCode.NotFound,
      when: 'Socrata returned 404 for the catalog endpoint itself — the Discovery API address is wrong or the service moved.',
      recovery:
        'Check that CDC_CATALOG_URL still points at the Socrata Discovery API; the default is https://api.us.socrata.com/api/catalog/v1.',
    },
    {
      reason: 'access_denied',
      code: JsonRpcErrorCode.Forbidden,
      when: 'Socrata returned 403 — the catalog refused this request rather than failing to serve it.',
      recovery:
        'Do not retry the same request; drop any category or tag filters and search with query alone.',
    },
    {
      reason: 'upstream_error',
      code: JsonRpcErrorCode.ServiceUnavailable,
      when: 'Socrata catalog API returned a 5xx server error.',
      retryable: true,
      recovery: 'Retry after a brief delay; the catalog may be temporarily unavailable.',
    },
    {
      reason: 'page_out_of_range',
      code: JsonRpcErrorCode.ValidationError,
      when: `offset is above 0 and offset plus limit, after the ${MAX_LIMIT}-entry cap, exceeds ${CATALOG_PAGE_WINDOW_MAX}, which Socrata's catalog rejects outright.`,
      recovery: `Lower offset so it plus the capped limit is at most ${CATALOG_PAGE_WINDOW_MAX}; a limit above ${MAX_LIMIT} already counts as ${MAX_LIMIT}, so only a limit below that shrinks the sum. Each portal holds well under two thousand entries, so a much smaller offset already reaches the end.`,
    },
    {
      reason: 'invalid_query',
      code: JsonRpcErrorCode.ValidationError,
      when: 'Catalog API returned 400 — typically a malformed query or invalid filter value.',
      recovery:
        'Check that category names and tag values match what the catalog accepts; try removing filters to confirm basic discovery works.',
    },
  ],
  input: z.object({
    domain: z
      .enum(CDC_SOCRATA_DOMAINS)
      .default('data.cdc.gov')
      .describe(
        'CDC Socrata host to search. "data.cdc.gov" (default) and "chronicdata.cdc.gov" front the same catalog and return the same entries, so switching hosts neither widens nor narrows a search — chronic-disease and small-area collections such as PLACES, the Heart Disease & Stroke Atlas, and Environmental Public Health Tracking are found from either.',
      ),
    query: z
      .string()
      .optional()
      .describe(
        'Full-text search across dataset names and descriptions (e.g., "diabetes mortality", "lead exposure children").',
      ),
    category: z
      .string()
      .optional()
      .describe(
        'Filter by domain category (e.g., "NNDSS", "Vaccinations", "Behavioral Risk Factors"). Values come from the catalog\'s own vocabulary and are matched exactly, including case — "Vaccinations" matches 89 entries while "Vaccination" matches none. Call cdc_list_catalog_vocabulary for every value with its entry count rather than guessing at one.',
      ),
    tags: z
      .array(z.string().describe('Tag value'))
      .optional()
      .describe(
        'Filter by domain tags (e.g., ["covid19", "surveillance"]). Tags widen the search instead of narrowing it — a dataset matches when it carries any one of them, so every tag added returns more results, and an unrecognized tag matches nothing and leaves the result set unchanged. Values match the catalog\'s own tag vocabulary, case-insensitively; call cdc_list_catalog_vocabulary for the values in use with their entry counts, or read the tags field on any result. To narrow, combine tags with query or category, which intersect with the tag set.',
      ),
    limit: z
      .number()
      .int()
      .min(1)
      .max(CATALOG_PAGE_WINDOW_MAX)
      .default(10)
      .describe(
        `Results to return (default 10). One call returns at most ${MAX_LIMIT}: a larger limit, up to ${CATALOG_PAGE_WINDOW_MAX.toLocaleString('en-US')}, is capped at ${MAX_LIMIT}, and the response says so and gives the offset to continue from while more datasets match. offset plus limit must not exceed ${CATALOG_PAGE_WINDOW_MAX} once limit is capped.`,
      ),
    offset: z
      .number()
      .int()
      .min(0)
      .max(9999)
      .default(0)
      .describe(
        `Pagination offset for browsing beyond first page (max 9999). offset plus limit must not exceed ${CATALOG_PAGE_WINDOW_MAX} once limit is capped; both CDC portals hold well under two thousand entries, so offsets near that ceiling page past the end of the catalog.`,
      ),
    order: z
      .enum(['dataset_id', 'relevance'])
      .default('dataset_id')
      .describe(
        'Result ordering. "dataset_id" (default) sorts deterministically by each dataset\'s unique catalog ID — required for stable offset pagination, since consecutive pages form a gap-free, duplicate-free traversal. "relevance" returns best-match ranking for keyword search but is not stably paginable across pages, so walking offsets can skip or repeat datasets.',
      ),
  }),
  output: z.object({
    datasets: z
      .array(
        z
          .object({
            id: z.string().describe('Four-by-four dataset identifier (e.g., "bi63-dtpu").'),
            name: z
              .string()
              .describe(
                'Dataset display name from the catalog (e.g., "Provisional COVID-19 Deaths by Sex and Age").',
              ),
            description: z
              .string()
              .optional()
              .describe(
                `Dataset description when provided by the catalog, as plain text — markup stripped and entity references decoded — then truncated to ${DESCRIPTION_MAX} characters, so the limit bounds visible text. Fetch the full text via cdc_get_dataset_schema with full_description: true; without it, that tool caps the description at ${DATASET_DESCRIPTION_CAP_TEXT} characters.`,
              ),
            assetType: z
              .string()
              .optional()
              .describe(
                'Catalog asset type as Socrata reports it — "dataset", "filter", "chart", "map", "story", "file", or "href". Descriptive only: "filter" entries carry real columns and query normally, while "chart" and "map" entries do not. Read columnCount, not this field, to decide whether an entry is queryable.',
              ),
            category: z.string().optional().describe('Domain category when provided.'),
            tags: z.array(z.string()).optional().describe('Domain tags when provided.'),
            columnCount: z
              .number()
              .optional()
              .describe(
                'Number of columns in the dataset when reported by the catalog. A count of 0 means the entry is not tabular — cdc_get_dataset_schema and cdc_query_dataset return no usable data for it.',
              ),
            columnSample: z
              .array(z.string())
              .optional()
              .describe(
                `First ${COLUMN_SAMPLE_MAX} column field names as a preview. Call cdc_get_dataset_schema for the full column list with data types.`,
              ),
            updatedAt: z.string().optional().describe('Last data update timestamp when provided.'),
            pageViews: z.number().optional().describe('Total page views when provided.'),
          })
          .describe('A single dataset catalog entry.'),
      )
      .describe('Matching datasets.'),
  }),
  // Agent-facing result-set context: total for pagination, the filters as the server
  // applied them, and a recovery notice when nothing matched. Reaches structuredContent
  // AND content[] automatically — no format() entry needed or allowed.
  enrichment: {
    totalCount: z.number().describe('Total matching datasets in the catalog (for pagination).'),
    appliedFilters: AppliedFiltersSchema.describe(
      'Filters applied to this query; absent fields indicate no filter on that dimension. Query, category, and tags intersect with each other, but multiple tags union.',
    ),
    notice: z
      .string()
      .optional()
      .describe(
        'Guidance when the page came back empty — the catalog values closest to a category or tag filter that matched nothing, each with its entry count; how to broaden a search when no value is close; or the size of the result set when the offset ran past its end.',
      ),
  },
  enrichmentTrailer: {
    totalCount: { label: 'Total Matching' },
    appliedFilters: {
      render: (f) => {
        const parts: string[] = [];
        if (f.query) parts.push(`- **Query:** "${escapeMarkdownText(f.query)}"`);
        if (f.category) parts.push(`- **Category:** "${escapeMarkdownText(f.category)}"`);
        if (f.tags?.length) {
          parts.push(`- **Tags (any of):** ${f.tags.map((t) => escapeMarkdownText(t)).join(', ')}`);
        }
        return parts.length > 0
          ? `**Applied Filters:**\n${parts.join('\n')}`
          : '**Applied Filters:** none';
      },
    },
    notice: { render: markdownBlockquote },
  },
  async handler(input, ctx) {
    /* ... body omitted: clamps limit to MAX_LIMIT, rejects page_out_of_range when
       offset + capped limit > CATALOG_PAGE_WINDOW_MAX, drops blank filters, calls
       getSocrataService().discover(filters, ctx.signal), and re-dispatches on err.data.reason ... */
  },
});
```

> The `input`, `output` and `enrichment` schemas are quoted in full. Only the `handler` function body (starting at `async handler(input, ctx) {`) is elided — it contains runtime logic (clamping, the page-window guard, whitespace-filter normalization, the Socrata service call) rather than schema surface. `CDC_SOCRATA_DOMAINS` resolves to `['data.cdc.gov', 'chronicdata.cdc.gov']` and `DATASET_DESCRIPTION_CAP_TEXT` is a separate constant imported from `@/utils/text.js` (see `CLAUDE.md`), both referenced but defined outside this file.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Search the CDC dataset catalog by keyword, category, or tag")
- [ ] It enumerates the return surface ("IDs, names, truncated descriptions, asset types, column counts, and update timestamps")
- [ ] It warns about non-tabular catalog assets and gives the queryability signal ("an entry whose columnCount is 0 ... yields no data from the other tools")
- [ ] It chains to the next tool in the workflow ("Use cdc_get_dataset_schema for the full column list")

### 2. Schema Correctness
- [ ] Valid JSON Schema generated from Zod (`type: object`, `properties`, `required` inferred from non-optional fields)
- [ ] `domain` constrained with `z.enum(CDC_SOCRATA_DOMAINS)` (allowlist acting as an SSRF guard), `order` with an `enum`
- [ ] Numeric bounds present and internally consistent (`limit` `.min(1).max(10000)` default 10 while the tool caps at `MAX_LIMIT=100`; `offset` `.min(0).max(9999)`)
- [ ] `input` is a plain object schema with no `refine`/`superRefine` (relational checks — e.g. `offset + limit > CATALOG_PAGE_WINDOW_MAX` — are enforced in the handler and surfaced as the declared `page_out_of_range` reason)

### 3. Parameter Description Quality
- [ ] Every parameter has a `.describe(...)`, several with concrete examples ("diabetes mortality", `["covid19", "surveillance"]`, `"bi63-dtpu"`)
- [ ] Non-obvious semantics are documented (tags *widen* rather than narrow and union; `category` matches exactly including case, `"Vaccination"` → 0)
- [ ] Defaults stated inline (`limit` default 10, `offset` default 0, `order` default `dataset_id`)
- [ ] The declared cap is explained rather than merely asserted ("a larger limit ... is capped at 100, and the response says so")

### 4. Output / Enrichment Contract
- [ ] Every `output.datasets[]` field is described, including the meaning of `columnCount === 0`
- [ ] `enrichment` supplies pagination and recovery context (`totalCount`, `appliedFilters`, `notice`) mapping to `structuredContent` and `content[]`
- [ ] Documented errors (`errors[]`) carry `reason`, JSON-RPC `code`, `when`, `retryable`, and `recovery`
- [ ] The empty-page `notice` behavior is documented and resolvable against the catalog vocabulary

### 5. Extensibility & Maintainability
- [ ] Built on the shared `@cyanheads/mcp-ts-core` `tool(name, {...})` API; one tool per file under `src/mcp-server/tools/definitions/`
- [ ] Consistent `cdc_<verb>_<noun>` naming across the tool set (`cdc_discover_datasets`, `cdc_get_dataset_schema`, `cdc_list_catalog_vocabulary`, `cdc_query_dataset`, `cdc_query_wonder`)
- [ ] Read-only tool advertises `readOnlyHint`; shared `AppliedFiltersSchema` reused between enrichment and the trailer renderer
- [ ] Domain limits (`MAX_LIMIT`, `CATALOG_PAGE_WINDOW_MAX`, `DESCRIPTION_MAX`, `COLUMN_SAMPLE_MAX`) are named constants with rationale, not inline literals

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Output / Enrichment Contract | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "find CDC datasets about diabetes mortality"; verify `cdc_discover_datasets` is called with `query: "diabetes mortality"` and that results carry four-by-four `id`s such as `bi63-dtpu`.
2. Issue "show me CDC vaccination datasets, 25 at a time"; verify `category: "Vaccinations"` with `limit: 25`.
3. Issue "page past the first 10 COVID surveillance datasets"; verify `tags: ["covid19", "surveillance"]` with `offset: 10`, and that `totalCount`/`appliedFilters` appear in the enrichment.
4. Issue a keyword search expected to return many matches; verify `order` defaults to `dataset_id` so consecutive pages form a gap-free traversal.

### Boundary Test Cases
1. `limit` at its floor (1) and above the tool cap (e.g. 500); verify a full page of 100 is returned with the clamp disclosed and a continuation `offset` given.
2. `limit` at its declared schema ceiling (`10000`) or `offset` at its declared ceiling (`9999`); verify the intended `page_out_of_range` rejection rather than a Socrata 400.
3. `offset: 0` with a large `limit` (covers the documented "at offset=0 it answers any limit" case); verify it is accepted.
4. Empty result set (e.g. `category: "Vaccination"` — singular); verify the `notice` names the closest vocabulary values with their entry counts instead of a bare empty page.

### Negative Test Cases
1. `domain` set to a non-allowlisted host (e.g. `"data.gov"`); verify the `z.enum` rejects it before any network call (SSRF guard).
2. `order: "name"`; verify rejection against the `['dataset_id', 'relevance']` enum.
3. `limit: 0` or a negative `offset`; verify the `.min()` bounds reject them.
4. A request whose `offset + min(limit, 100) > 10000`; verify the documented `page_out_of_range` validation error, with the `recovery` text.
5. An ambiguous prompt ("show me health stuff") — verify the model does not hallucinate a specific `category`/`tags` value it has not seen and instead queries broadly or calls `cdc_list_catalog_vocabulary`.

## Notes
- This is one logical artifact: the `cdc_discover_datasets` tool — the entry point of the CDC Health MCP Server's discover → inspect → query workflow. The same server also exposes `cdc_get_dataset_schema`, `cdc_list_catalog_vocabulary`, `cdc_query_dataset`, and `cdc_query_wonder` tools, two `cdc://datasets…` resources, and one `analyze_health_trend` prompt (per `CLAUDE.md`).
- The `input`/`output`/`enrichment` are authored as Zod schemas and converted to JSON Schema by `@cyanheads/mcp-ts-core`; the verbatim Zod source is quoted as the schema source per the rule for generated schemas.
- `Collection Date` is recorded as 2026-10-13 per the task brief. The repo's `HEAD` at fetch time resolved to commit `9ebab18bab062a8e1bfe51a996c74410dc948356`; `CLAUDE.md` self-reports server version `0.9.3` while `package.json` reports `0.10.0` (the two files lag each other), and the `README.md` badge reports `5 Tools • 2 Resources • 1 Prompt`.
- The `description` string is unusually long (a full sentence-per-capability paragraph) — deliberately, so the model can distinguish this discovery tool from `cdc_get_dataset_schema` and the query tools without extra prompting.
- No API key is required (CDC Open Data / Socrata are public; an optional app token raises rate limits), so no `authConfig` surface is involved.
- License is Apache-2.0 (`LICENSE`: "Copyright 2026 Casey Hand @cyanheads"); long verbatim quotation is permissible.
