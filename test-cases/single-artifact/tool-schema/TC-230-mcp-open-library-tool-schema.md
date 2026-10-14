# TC-230: mcp-open-library Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: 8enSmith/mcp-open-library
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definition: name, description, Zod/JSON-Schema parameters)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/tools/search-books/index.ts` — `https://raw.githubusercontent.com/8enSmith/mcp-open-library/HEAD/src/tools/search-books/index.ts`
  - `LICENSE.md` (license verification) — `https://raw.githubusercontent.com/8enSmith/mcp-open-library/HEAD/LICENSE.md`
  - Repository file listing — `https://api.github.com/repos/8enSmith/mcp-open-library/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/tools/search-books/index.ts` (the `search_books` tool definition and its argument schema):

```typescript
import { z } from "zod";

import { parseArgs, toErrorResult } from "../../utils/errors.js";
import { jsonResult, textResult } from "../../utils/results.js";
import {
  OpenLibrarySearchResponse,
  SEARCH_FIELDS,
  searchLimitSchema,
  searchOffsetSchema,
  toSearchResults,
} from "../../utils/search.js";
import { READ_ONLY_LOOKUP, ToolDefinition, ToolHandler } from "../types.js";

export const SEARCH_CRITERIA = [
  "q",
  "title",
  "author",
  "subject",
  "place",
  "person",
  "publisher",
  "isbn",
] as const;

export const SORT_VALUES = [
  "new",
  "old",
  "random",
  "key",
  "rating",
  "readinglog",
  "want_to_read",
  "currently_reading",
  "already_read",
  "title",
] as const;

const CRITERIA_MESSAGE = `Provide at least one search criterion: ${SEARCH_CRITERIA.join(", ")}`;

export const SearchBooksArgsSchema = z
  .object({
    q: z
      .string()
      .min(1)
      .optional()
      .describe(
        "Free-form query searched across all fields. Supports Solr syntax, e.g. `subject:cyberpunk AND first_publish_year:[1980 TO 1990]`.",
      ),
    title: z.string().min(1).optional().describe("Search by book title."),
    author: z.string().min(1).optional().describe("Search by author name."),
    subject: z.string().min(1).optional().describe("Search by subject."),
    place: z
      .string()
      .min(1)
      .optional()
      .describe("Search by a place the book is about."),
    person: z
      .string()
      .min(1)
      .optional()
      .describe("Search by a person the book is about."),
    publisher: z.string().min(1).optional().describe("Search by publisher."),
    isbn: z
      .string()
      .min(1)
      .optional()
      .describe("Search by ISBN-10 or ISBN-13."),
    language: z
      .string()
      .regex(/^[a-z]{3}$/, {
        message:
          "language must be a lowercase 3-letter MARC code, e.g. eng, fre, spa",
      })
      .optional()
      .describe(
        "Restrict results to a language, as a 3-letter MARC code (e.g. eng, fre, spa).",
      ),
    sort: z
      .enum(SORT_VALUES)
      .optional()
      .describe(
        "Result ordering. Omit for relevance. `new`/`old` order by first publication date, `rating` by average rating.",
      ),
    limit: searchLimitSchema,
    offset: searchOffsetSchema,
  })
  .refine((value) => SEARCH_CRITERIA.some((key) => Boolean(value[key])), {
    message: CRITERIA_MESSAGE,
  });
```

```typescript
export const searchBooksTool: ToolDefinition = {
  name: "search_books",
  title: "Search books",
  description: `Search Open Library across titles, authors, subjects, places, people, publishers and ISBNs. ${CRITERIA_MESSAGE}; combining several narrows the search. Returns at most \`limit\` results (default 10) together with \`num_found\`, the total number of matches; page through them with \`offset\`. Each result carries \`best_edition\` — one edition of the work, with its \`isbn_13\`/\`isbn_10\` where Open Library has them, and its \`edition_key\`, which can be passed to \`get_book_by_id\` as \`{ idType: "olid" }\` for that edition's full record.`,
  schema: SearchBooksArgsSchema,
  annotations: READ_ONLY_LOOKUP,
  handler: handleSearchBooks,
};
```

Sibling tools in the same server (names only, from `src/tools/registry.ts` and the `src/tools/*` directories): `search_books`, `get_book_by_id`, `get_book_by_title`, `get_book_cover`, `get_author_info`, `get_authors_by_name`, `get_author_photo`.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Description states what the tool does (search Open Library) and when to use it
- [ ] `title` ("Search books") is human-readable and distinct from sibling tools
- [ ] Description explains the relationship to other tools (`edition_key` → `get_book_by_id`)

### 2. JSON Schema Correctness
- [ ] The Zod schema compiles to a valid JSON Schema (`type: object`, `properties`, `required`)
- [ ] The `.refine()` "at least one criterion" constraint is representable/enforced at validation time
- [ ] `limit`/`offset` reference shared schemas with documented bounds

### 3. Parameter Description Quality
- [ ] Every parameter has a `.describe()` string
- [ ] `limit` default (10) and the `offset` paging semantics are documented
- [ ] `language` documents the exact format (lowercase 3-letter MARC code) and gives examples
- [ ] `q` documents the advanced Solr syntax it accepts

### 4. Tool Identity & Annotation Consistency
- [ ] Tool `name` (`search_books`) is unique and stable (snake_case)
- [ ] Read-only annotation (`READ_ONLY_LOOKUP`) matches the tool's non-mutating behavior
- [ ] Description does not overstate capabilities (no data returned beyond the schema)

### 5. Extensibility & Maintainability
- [ ] Schema is exported (`SearchBooksArgsSchema`) for reuse and testing
- [ ] Enumerations are single-sourced (`SEARCH_CRITERIA`, `SORT_VALUES`)
- [ ] Tool definition is separated from the handler implementation

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
1. Issue "find books by Ursula K. Le Guin about anarchism"; verify `search_books` is selected and `author`/`subject` arguments are populated correctly.
2. Issue "search for the ISBN 9780441013593"; verify `search_books` is called with `isbn` and no other criteria.
3. Ask for results in French; verify `language: "fre"` (3-letter MARC) is used rather than a 2-letter code.

### Boundary Test Cases
1. Call with zero criteria; verify the `.refine()` rule rejects the call with the `CRITERIA_MESSAGE`.
2. `limit` at its maximum; verify the shared `searchLimitSchema` bound is respected.
3. `sort` set to each enum value (e.g. `rating`, `new`); verify all are accepted.

### Negative Test Cases
1. `language: "fr"` (2-letter code); verify the `^[a-z]{3}$` regex rejects it.
2. Unknown argument (e.g. `genre`) under a strict schema; verify rejection.
3. Ambiguous query "get me that book"; verify the model asks for a criterion instead of emitting an empty-argument call that violates the refine rule.

## Notes
- This artifact is the tool-selection surface an LLM sees for the Open Library MCP server; the Zod schema is published to the client as JSON Schema via the MCP SDK.
- The `search_books` description is unusually explicit about downstream affordances (`best_edition`, `edition_key`, `get_book_by_id`), which is useful for multi-step tool chaining.
- License is MIT; verbatim quotation of the tool schema is permissible.
