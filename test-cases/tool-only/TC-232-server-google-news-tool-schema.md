# TC-232: server-google-news Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: ChanMeng666/server-google-news
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definition: name, description, JSON-Schema `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/index.ts` (tool registration via `ListToolsRequestSchema`) — `https://raw.githubusercontent.com/ChanMeng666/server-google-news/HEAD/src/index.ts`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/ChanMeng666/server-google-news/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/ChanMeng666/server-google-news/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/index.ts` (the `google_news_search` tool definition):

```typescript
  private setupHandlers(): void {
    // 注册可用工具
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'google_news_search',
          description: 'Search Google News for articles and news content. Results will be automatically categorized by topic.',
          inputSchema: {
            type: 'object',
            properties: {
              q: {
                type: 'string',
                description: 'Search query',
              },
              gl: {
                type: 'string',
                description: 'Country code (e.g., us, uk)',
                default: 'us'
              },
              hl: {
                type: 'string',
                description: 'Language code (e.g., en)',
                default: 'en'
              },
              topic_token: {
                type: 'string',
                description: 'Topic token for specific news topics',
              },
              publication_token: {
                type: 'string',
                description: 'Publication token for specific publishers',
              },
              story_token: {
                type: 'string',
                description: 'Story token for full coverage of a story',
              },
              section_token: {
                type: 'string',
                description: 'Section token for specific sections',
              },
            },
          },
        },
      ],
    }));
```

Verbatim argument validation and default handling for the same tool (same file):

```typescript
      if (name === 'google_news_search') {
        if (!isValidGoogleNewsSearchArgs(args)) {
          throw new McpError(
            ErrorCode.InvalidParams,
            'Invalid arguments for google_news_search'
          );
        }

        const params = {
          ...args,
          engine: 'google_news',
          api_key: SERP_API_KEY,
          gl: args.gl || 'us',
          hl: args.hl === 'zh' ? 'en' : (args.hl || 'en')
        };
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Description states what the tool does (search Google News) and the result shape (auto-categorized by topic)
- [ ] Description gives a hint that results are grouped into categories
- [ ] No marketing-only text that omits functional capability

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`)
- [ ] `default` values (`us`, `en`) are declared for `gl` and `hl`
- [ ] Note whether any parameters are actually required (schema declares none; the tool accepts an empty argument object)

### 3. Parameter Description Quality
- [ ] Every parameter has a `description`
- [ ] `gl`/`hl` document expected format and example values (`us`, `uk` / `en`)
- [ ] The four `*_token` parameters explain what a token represents and where it comes from (currently only one-line descriptions)
- [ ] `q` is described as a search query but not marked as required

### 4. Configuration / Runtime Consistency
- [ ] Schema defaults (`gl: 'us'`, `hl: 'en'`) match the runtime defaults in the handler
- [ ] The `hl === 'zh' → 'en'` override in the handler is reflected (or at least not contradicted) in the schema description
- [ ] The `SERP_API_KEY` requirement is documented in the server's configuration surface

### 5. Extensibility & Maintainability
- [ ] Tool declaration is centralized in `setupHandlers()`
- [ ] Argument types are mirrored by an `isValidGoogleNewsSearchArgs` type guard in `types.ts`
- [ ] Tool `name` (`google_news_search`) is unique and stable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Configuration / Runtime Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what's the latest news about AI?"; verify `google_news_search` is selected with a populated `q`.
2. Issue "show me UK news in English"; verify `gl: "uk"`, `hl: "en"`.
3. Ask for full coverage of a developing story; verify `story_token` is used when available.

### Boundary Test Cases
1. Call with only `q`; verify the server applies default `gl: "us"` and `hl: "en"`.
2. `hl: "zh"`; verify the runtime override forces `en` and the model is not surprised by the substitution.
3. Provide `topic_token`, `publication_token`, `section_token` together; verify all are accepted.

### Negative Test Cases
1. Call with empty arguments `{}`; verify behavior is defined (the schema marks nothing required) and does not silently return arbitrary default news.
2. Pass a non-string `gl` (e.g. number); verify the type guard rejects it.
3. Ambiguous "news?" request; verify the model supplies a meaningful `q` or asks a clarifying question instead of firing an empty query.

## Notes
- This artifact is the surface an LLM sees when choosing the single Google News tool exposed by this server (SerpAPI-backed).
- The schema declares no `required` field, which is a notable risk: a model can call the tool with no arguments at all.
- License is MIT; verbatim quotation of the tool schema is permissible.
