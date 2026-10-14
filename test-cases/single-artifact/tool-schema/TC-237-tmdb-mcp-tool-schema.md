# TC-237: tmdb-mcp Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: Grinv/tmdb-mcp
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions using Zod `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/tools/tmdb/search.ts` (name/id resolver tool definitions) — `https://raw.githubusercontent.com/Grinv/tmdb-mcp/HEAD/src/tools/tmdb/search.ts`
  - `src/tools/tmdb/details.ts` (detail lookup tool definitions) — `https://raw.githubusercontent.com/Grinv/tmdb-mcp/HEAD/src/tools/tmdb/details.ts`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/Grinv/tmdb-mcp/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/Grinv/tmdb-mcp/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/tools/tmdb/search.ts` (the `search_movies` tool):

```typescript
  server.registerTool(
    "search_movies",
    {
      title: "Search movies",
      description:
        "Search TMDB movies by title; returns compact summaries with the TMDB id that the other " +
        "movie tools (get_movie, get_movie_credits, …) require, plus pagination info. Use this over " +
        "search_multi when you already know the result is a movie. `region` here only picks which " +
        "country's release_date is shown per result (e.g. a title's US vs. India theatrical date) — " +
        "verified live, it does not filter which movies match or reorder them; for actual " +
        "region-based availability use get_watch_providers instead.",
      inputSchema: z.strictObject({
        query: z.string().min(1).describe("Movie title to search for."),
        year: yearFilter(
          "Bias results toward this release year — TMDB's search 'year' filter is soft: some " +
            "results outside this year can still appear (unlike discover_movies' year filter, a " +
            "hard primary_release_year match). For an exact-year filter, use discover_movies instead.",
        ),
        include_adult: includeAdult,
        language,
        region,
        page: page.optional(),
      }),
      outputSchema: pageSchema(movieSummarySchema),
      annotations: READ_ONLY,
    },
    (args, ctx) => requireTmdb(() => tmdb.searchMovies(args, ctx.mcpReq.signal), ctx.mcpReq.signal),
  );
```

Verbatim excerpt from `src/tools/tmdb/search.ts` (the `search_tv` and `search_multi` tools):

```typescript
  server.registerTool(
    "search_tv",
    {
      title: "Search TV shows",
      description:
        "Search TMDB TV shows by name; returns compact summaries with the TMDB id that get_tv and " +
        "the other TV tools require. Use this over search_multi when you already know the result is " +
        "a TV show.",
      inputSchema: z.strictObject({
        query: z.string().min(1).describe("TV show name to search for."),
        year: yearFilter(
          "Filter by first-air-date year. Unlike search_movies' soft year filter, this is a hard " +
            "first-air-year match (verified live). For a first-air-date range, use discover_tv.",
        ),
        include_adult: includeAdult,
        language,
        page: page.optional(),
      }),
      outputSchema: pageSchema(tvSummarySchema),
      annotations: READ_ONLY,
    },
    (args, ctx) => requireTmdb(() => tmdb.searchTv(args, ctx.mcpReq.signal), ctx.mcpReq.signal),
  );

  server.registerTool(
    "search_multi",
    {
      title: "Search everything",
      description:
        "Search movies, TV shows and people in one call. Each result carries a media_type " +
        "('movie' | 'tv' | 'person') so you can route to the right get_* tool. Use when the user's " +
        "query could be any of these; if you already know the type, search_movies/search_tv/" +
        "search_people are more precise.",
      inputSchema: z.strictObject({
        query: z.string().min(1).describe("Free-text query."),
        include_adult: includeAdult,
        language,
        page: page.optional(),
      }),
      outputSchema: pageSchema(multiItemSchema),
      annotations: READ_ONLY,
    },
    (args, ctx) => requireTmdb(() => tmdb.searchMulti(args, ctx.mcpReq.signal), ctx.mcpReq.signal),
  );
```

Verbatim excerpt from `src/tools/tmdb/details.ts` (the `get_movie` tool):

```typescript
  server.registerTool(
    "get_movie",
    {
      title: "Get movie details",
      description:
        "Get full details for one movie by TMDB id: overview, genres, runtime, budget/revenue, " +
        "vote average, the age/content rating (certification) for `region` — falling back to the " +
        "US rating, then any available country, when `region` has none; check `certification_region` " +
        "to see which one was used — and links (TMDB + IMDb). " +
        "By default also includes IMDb/Rotten Tomatoes/Metacritic ratings and an awards summary " +
        "(see include_ratings), plus OMDb's own age rating " +
        "(`ratings.rated` — separate from this tool's own `certification` above; the two can differ) " +
        "from OMDb (set include_ratings=false to skip); if unavailable (no OMDB_API_KEY, no imdb_id, or the " +
        "OMDb lookup fails), `ratings` degrades to `{found:false, reason}` instead of failing the " +
        "call. If you only need the headline info (title/year/genres/vote average) — for one id or " +
        "several — use get_movies instead; it's trimmed on purpose and skips the rest of this " +
        "payload. Get the id from search_movies.",
      inputSchema: z.strictObject({
        id: tmdbId,
        region,
        language,
        include_ratings: includeRatings,
      }),
      outputSchema: movieDetailEnrichedSchema,
      annotations: READ_ONLY,
    },
    ({ id, region: r, language: lang, include_ratings }, ctx) => {
      return requireTmdbCached(
        (onStale) =>
          getEnrichedDetail(
            "movie",
            id,
            r,
            lang,
            include_ratings ?? true,
            tmdb,
            omdb,
            false,
            onStale,
          ),
        ctx.mcpReq.signal,
      );
    },
  );
```

Additional tools declared across the same modules (names): `search_people`, `search_keywords`, `search_companies`, `search_watch_providers` (in `search.ts`); `get_tv`, `get_movies`, `get_tv_shows`, `get_person`, `get_person_credits`, `get_tv_season`, and `discover_movies`/`discover_tv` (in `details.ts`/`discover.ts`/`lookups.ts`).

Note: `year`, `include_adult`, `language`, `region`, `page`, `tmdbId`, `include_ratings` are shared reusable field schemas defined in `src/tools/tmdb/fields.ts`; their internal definitions were not fetched, so they are referenced here by name rather than quoted.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool returns and when to use it
- [ ] Descriptions explicitly disambiguate similar tools (e.g. `search_movies` vs `search_multi`, `get_movie` vs `get_movies`)
- [ ] Descriptions document non-obvious semantics (soft vs hard `year` filter, `region` behavior)

### 2. JSON Schema Correctness
- [ ] Each inputSchema is a Zod `strictObject`, surfacing as JSON Schema `additionalProperties: false`
- [ ] Required vs optional fields are expressed per tool (`query` required; `page` optional)
- [ ] Each tool declares an `outputSchema`, adding structure beyond inputs

### 3. Parameter Description Quality
- [ ] Every field has a `.describe()` (or a shared descriptor)
- [ ] Shared field schemas (`language`, `region`, `page`) are documented once and reused
- [ ] Quality caveats are stated (e.g. TMDB search `year` is "soft")

### 4. Tool Identity & Annotation Consistency
- [ ] Tool `name` values are unique snake_case and hierarchically named (`search_*`, `get_*`, `discover_*`)
- [ ] `annotations: READ_ONLY` is applied consistently to read-only tools
- [ ] Titles are human-readable and parallel

### 5. Extensibility & Maintainability
- [ ] Tools are grouped by concern (`search.ts`, `details.ts`, `discover.ts`, `lookups.ts`)
- [ ] Reusable field schemas live in `fields.ts`; output schemas in `format.schemas.ts`
- [ ] The "id from search, then details" chaining contract is stated in descriptions

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Tool Identity & Annotation Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "find the movie Inception"; verify `search_movies` with `query: "Inception"` then `get_movie` with the returned id.
2. Issue "search for anything about Pedro Pascal"; verify `search_multi` (or `search_people`) and correct `media_type` routing.
3. Issue "which streaming services have Netflix titles?"; verify `search_watch_providers` → `discover_movies` chaining with `watch_region`.

### Boundary Test Cases
1. `query: ""` (empty); verify `.min(1)` rejects it.
2. Unknown field under `strictObject` (e.g. `sort`); verify `additionalProperties: false` rejects it.
3. `year` on `search_movies` (soft) vs `search_tv` (hard); verify the model understands the difference from the descriptions.

### Negative Test Cases
1. `get_movie` with a missing `id`; verify the required field is enforced.
2. Pass a movie title where `id` is expected; verify the type expectation fails and the model falls back to `search_movies`.
3. Ambiguous "show me that show"; verify the model calls a `search_*` tool first rather than guessing an id.

## Notes
- This artifact is the tool-selection surface an LLM sees for a TMDB (movies/TV/people) server that also enriches results with OMDb ratings.
- The descriptions are unusually explicit about tool boundaries and chaining contracts, making this a strong example of description-driven disambiguation.
- License is MIT; verbatim quotation of the tool schemas is permissible.
