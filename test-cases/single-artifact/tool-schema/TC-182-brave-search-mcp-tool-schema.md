# TC-182: Brave Search MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: brave/brave-search-mcp-server (official Brave Search MCP server)
- **License**: MIT (Copyright (c) 2024 Anthropic, PBC; Copyright (c) 2025 Brave Software, Inc)
- **Artifact Type**: Tool Schema (MCP tool definition for the `brave_web_search` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/web/index.ts` — tool identity, description, annotations and registration
  - `src/tools/web/params.ts` — input parameters as a Zod object (`params`)
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### 1. Tool identity, description and registration (`src/tools/web/index.ts`, fetched)

```typescript
export const name = 'brave_web_search';

export const annotations: ToolAnnotations = {
  title: 'Brave Web Search',
  openWorldHint: true,
};

export const description = `
    Performs web searches using the Brave Search API and returns comprehensive search results with rich metadata.

    When to use:
        - General web searches for information, facts, or current topics
        - Location-based queries (restaurants, businesses, points of interest)
        - News searches for recent events or breaking stories
        - Finding videos, discussions, or FAQ content
        - Research requiring diverse result types (web pages, images, reviews, etc.)

    Returns a JSON list of web results with title, description, and URL.
    
    When the "results_filter" parameter is empty, JSON results may also contain FAQ, Discussions, News, and Video results.
`.trim();
```

```typescript
export const register = (mcpServer: McpServer) => {
  mcpServer.registerTool(
    name,
    {
      title: name,
      description: description,
      inputSchema: params,
      annotations: annotations,
    },
    execute
  );
};
```

```typescript
export default {
  name,
  description,
  annotations,
  inputSchema: params.shape,
  execute,
  register,
};
```

### 2. Input schema (`src/tools/web/params.ts`, fetched verbatim)

```typescript
import { z } from 'zod';

export const params = z.object({
  query: z
    .string()
    .max(400)
    .refine((str) => str.split(/\s+/).length <= 50, 'Query cannot exceed 50 words')
    .describe('Search query (max 400 chars, 50 words)'),
  country: z
    .enum([
      'ALL',
      'AR',
      'AU',
      'AT',
      'BE',
      'BR',
      'CA',
      'CL',
      'DK',
      'FI',
      'FR',
      'DE',
      'HK',
      'IN',
      'ID',
      'IT',
      'JP',
      'KR',
      'MY',
      'MX',
      'NL',
      'NZ',
      'NO',
      'CN',
      'PL',
      'PT',
      'PH',
      'RU',
      'SA',
      'ZA',
      'ES',
      'SE',
      'CH',
      'TW',
      'TR',
      'GB',
      'US',
    ])
    .default('US')
    .describe(
      'Search query country, where the results come from. The country string is limited to 2 character country codes of supported countries.'
    )
    .optional(),
  search_lang: z
    .enum([
      'ar',
      'eu',
      'bn',
      'bg',
      'ca',
      'zh-hans',
      'zh-hant',
      'hr',
      'cs',
      'da',
      'nl',
      'en',
      'en-gb',
      'et',
      'fi',
      'fr',
      'gl',
      'de',
      'gu',
      'he',
      'hi',
      'hu',
      'is',
      'it',
      'jp',
      'kn',
      'ko',
      'lv',
      'lt',
      'ms',
      'ml',
      'mr',
      'nb',
      'pl',
      'pt-br',
      'pt-pt',
      'pa',
      'ro',
      'ru',
      'sr',
      'sk',
      'sl',
      'es',
      'sv',
      'ta',
      'te',
      'th',
      'tr',
      'uk',
      'vi',
    ])
    .default('en')
    .describe(
      'Search language preference. The 2 or more character language code for which the search results are provided.'
    )
    .optional(),
  ui_lang: z
    .enum([
      'es-AR',
      'en-AU',
      'de-AT',
      'nl-BE',
      'fr-BE',
      'pt-BR',
      'en-CA',
      'fr-CA',
      'es-CL',
      'da-DK',
      'fi-FI',
      'fr-FR',
      'de-DE',
      'zh-HK',
      'en-IN',
      'en-ID',
      'it-IT',
      'ja-JP',
      'ko-KR',
      'en-MY',
      'es-MX',
      'nl-NL',
      'en-NZ',
      'no-NO',
      'zh-CN',
      'pl-PL',
      'en-PH',
      'ru-RU',
      'en-ZA',
      'es-ES',
      'sv-SE',
      'fr-CH',
      'de-CH',
      'zh-TW',
      'tr-TR',
      'en-GB',
      'en-US',
      'es-US',
    ])
    .default('en-US')
    .describe(
      'The language of the UI. The 2 or more character language code for which the search results are provided.'
    )
    .optional(),
  count: z
    .int()
    .min(1)
    .max(20)
    .default(10)
    .describe(
      'Number of results (1-20, default 10). Applies only to web search results (i.e., has no effect on locations, news, videos, etc.)'
    )
    .optional(),
  offset: z
    .int()
    .min(0)
    .max(9)
    .default(0)
    .describe('Pagination offset (max 9, default 0)')
    .optional(),
  safesearch: z
    .enum(['off', 'moderate', 'strict'])
    .default('moderate')
    .describe(
      "Filters search results for adult content. The following values are supported: 'off' - No filtering. 'moderate' - Filters explicit content (e.g., images and videos), but allows adult domains in search results. 'strict' - Drops all adult content from search results. The default value is 'moderate'."
    )
    .optional(),
  freshness: z
    .union([
      z.enum(['pd', 'pw', 'pm', 'py']),
      z
        .string()
        .regex(
          /^\d{4}-\d{2}-\d{2}to\d{4}-\d{2}-\d{2}$/,
          "Use 'pd', 'pw', 'pm', or 'py' for a relative discovery window, or a custom range as YYYY-MM-DDtoYYYY-MM-DD (e.g. 2022-04-01to2022-07-30)."
        ),
    ])
    .describe(
      "Filters search results by when they were discovered. The following values are supported: 'pd' - Discovered within the last 24 hours. 'pw' - Discovered within the last 7 days. 'pm' - Discovered within the last 31 days. 'py' - Discovered within the last 365 days. 'YYYY-MM-DDtoYYYY-MM-DD' - Timeframe is also supported by specifying the date range e.g. 2022-04-01to2022-07-30."
    )
    .optional(),
  text_decorations: z
    .boolean()
    .default(true)
    .describe(
      'Whether display strings (e.g. result snippets) should include decoration markers (e.g. highlighting characters).'
    )
    .optional(),
  spellcheck: z
    .boolean()
    .default(true)
    .describe('Whether to spellcheck the provided query.')
    .optional(),
  result_filter: z
    .array(
      z.enum([
        'discussions',
        'faq',
        'infobox',
        'news',
        'query',
        'summarizer',
        'videos',
        'web',
        'locations',
        'rich',
      ])
    )
    .default(['web', 'query'])
    .describe("Result filter (default ['web', 'query'])")
    .optional(),
  goggles: z
    .union([z.string(), z.array(z.string())])
    .describe(
      "Goggles act as a custom re-ranking on top of Brave's search index. The parameter supports both a url where the Goggle is hosted or the definition of the Goggle. Multiple goggle URLs and/or definitions can be provided in an array. For more details, refer to the Goggles repository (i.e., https://github.com/brave/goggles-quickstart)."
    )
    .optional(),
  units: z
    .union([z.literal('metric'), z.literal('imperial')])
    .describe('The measurement units. If not provided, units are derived from search country.')
    .optional(),
  extra_snippets: z
    .boolean()
    .describe(
      'A snippet is an excerpt from a page you get as a result of the query, and extra_snippets allow you to get up to 5 additional, alternative excerpts. Only available under Free AI, Base AI, Pro AI, Base Data, Pro Data and Custom plans.'
    )
    .optional(),
  summary: z
    .boolean()
    .describe(
      'This parameter enables summary key generation in web search results. This is required for summarizer to be enabled.'
    )
    .optional(),
});

export type QueryParams = z.infer<typeof params>;

export default params;
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete input schema (here a Zod object converted to JSON Schema at registration; `inputSchema: params.shape`)
- [ ] Parameter types are accurate (`string`, `int`, `boolean`, `enum`, `array`, `union`)
- [ ] Required vs optional parameters are distinguishable (only `query` is effectively required; the rest are `.optional()` with `.default(...)`)
- [ ] Constraints (`max(400)`, 50-word refine, `min(1)/max(20)`, `max(9)`) are declared

### 2. Description Clarity
- [ ] The tool description states what it does and enumerates "When to use" scenarios
- [ ] Every parameter carries an inline human-readable description
- [ ] Enum semantics are explained (e.g. `safesearch`, `freshness`, `result_filter`)

### 3. Integration Compatibility
- [ ] Conforms to the MCP tool model (`registerTool(name, {title, description, inputSchema, annotations}, execute)`)
- [ ] Provides `ToolAnnotations` (`title`, `openWorldHint: true`) for client-side risk display
- [ ] Zod schema is transpiled to JSON Schema by the SDK, so it is consumable by standard function-calling clients

### 4. Example Quality
- [ ] Tool description embeds usage guidance and result-shape notes ("Returns a JSON list of web results with title, description, and URL")
- [ ] Parameter descriptions include concrete formats (e.g. `YYYY-MM-DDtoYYYY-MM-DD`, `2022-04-01to2022-07-30`)
- [ ] Plan tiers and limitations are documented inline (`extra_snippets` availability)

### 5. Extensibility
- [ ] Tool parameters are isolated in a dedicated `params.ts` module, reusable across profiles
- [ ] Default export exposes `inputSchema: params.shape` for reuse/testing
- [ ] Result filtering (`result_filter`) allows mixing web/FAQ/news/video/discussion result types without schema changes

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
1. Issue "search the web for the latest AI research news"; verify the model selects `brave_web_search` with a `query` and, if it wants fresh results, a valid `freshness` value (`pd`/`pw`/`pm`/`py` or `YYYY-MM-DDtoYYYY-MM-DD`).
2. Issue "find Italian restaurants near me"; verify `query` is populated and `result_filter` may include `locations`.
3. Issue "give me 5 results, only the last week"; verify `count: 5` and `freshness: "pw"`.

### Boundary Test Cases
1. `query` at exactly 400 characters / 50 words; verify it passes, and that 51 words or 401 characters are rejected.
2. `count` at floor (1) and ceiling (20); `offset` at ceiling (9).
3. `result_filter` set to a multi-value array such as `["web", "news", "videos"]`.
4. `country` default behavior when omitted (should default to `US`).

### Negative Test Cases
1. Call without `query`; verify schema validation rejects the call.
2. `safesearch: "high"` (out of enum); verify rejection.
3. `freshness: "2022-13-40to2022-01-01"`; verify the regex constraint rejects it.
4. `count: 50` (above `max(20)`); verify rejection.

## Notes
- This case quotes the tool definition verbatim from the official Brave Search MCP server. The input schema is authored in Zod (`params.ts`) and converted to JSON Schema by the MCP TypeScript SDK at registration time (`inputSchema: params.shape`), so the schema the LLM receives is generated from this source rather than hand-written.
- `brave_web_search` is one of several tools in the server; only this single tool and its parameters are quoted here (one logical artifact per case).
- License is MIT, so verbatim quotation is permissible.
