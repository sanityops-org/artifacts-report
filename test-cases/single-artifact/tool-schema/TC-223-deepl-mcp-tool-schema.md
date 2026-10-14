# TC-223: DeepL MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: DeepL/deepl-mcp-server (official DeepL MCP server)
- **License**: MIT (Copyright (c) 2022 DeepL SE, https://www.deepl.com)
- **Artifact Type**: Tool Schema (MCP tool definition for the `translate-text` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools.mjs` — tool registration, descriptions and input schemas for all tools
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Shared description helpers and the `translate-text` tool (`src/tools.mjs`, fetched verbatim)

```javascript
import { z } from "zod";
import { writingStyles, writingTones } from "./writing.mjs";

// Descriptive text for reuse in our tools
const languageCodeDescription =
  "language code, in standard ISO-639-1 format (e.g. 'en-US', 'de', 'fr')";
const sourceLanguageCodeDescription =
  "language code, in standard ISO-639-1 format (e.g. 'en', 'de', 'fr')";
const glossaryLanguageCodeDescription =
  "language code, in standard ISO-639-1 format without a regional variant (e.g. 'en', 'de', 'fr')";
const glossaryEntriesGuidance =
  "This does not fetch any glossary entries. Use the get-glossary-dictionary-entries tool to fetch entries.";
const styleRuleDescription =
  "Style rule ID to apply. Use the list-style-rules tool to discover available style rules.";

const formalityTypes = /** @type {const} */ ([
  "less",
  "more",
  "default",
  "prefer_less",
  "prefer_more",
]);

/**
 * Text inputs take a single string or an array of strings, each handled independently
 * @param {string} verb
 */
function textInput(verb) {
  return z
    .union([z.string(), z.array(z.string())])
    .describe(`Text to ${verb}, as a single string or an array of strings handled independently`);
}

export function registerTools(server, handlers) {
  server.tool(
    "translate-text",
    "Translate text to a target language using DeepL API. Review all available optional parameters and use those applicable to your scenario for best results. When the translation includes a glossary, you must specify the source language as well as the target language. If the user requests a glossary by name instead of by id, you can use the list-glossaries tool to get a name for each id.",
    {
      text: textInput("translate"),
      sourceLangCode: z
        .string()
        .optional()
        .describe(`source ${sourceLanguageCodeDescription}, or leave empty for auto-detection`),
      targetLangCode: z.string().describe("target " + languageCodeDescription),
      formality: z
        .enum(formalityTypes)
        .optional()
        .describe(
          "Controls formality: 'less' for informal, 'more' for formal/polite, 'prefer_less'/'prefer_more' to prefer but fall back to default",
        ),
      glossaryId: z
        .string()
        .optional()
        .describe("Glossary ID to ensure consistent terminology translation"),
      styleId: z.string().optional().describe(styleRuleDescription),
      context: z
        .string()
        .optional()
        .describe(
          "Recommended: describe what this text is about (e.g., 'Technical documentation for a software API'). Improves translation accuracy but is not itself translated.",
        ),
      preserveFormatting: z
        .boolean()
        .optional()
        .describe(
          "Set to true to preserve original formatting - recommended for markdown, code blocks, HTML, or any structured text",
        ),
      splitSentences: z
        .enum(["0", "1", "nonewlines"])
        .optional()
        .describe(
          "Sentence splitting: '0' disables, '1' (default) splits on punctuation and newlines, 'nonewlines' preserves line breaks",
        ),
      customInstructions: z
        .array(z.string())
        .optional()
        .describe(
          "Array of custom instructions to guide translation style (max 10 instructions, 300 chars each)",
        ),
    },
    handlers.translateText,
  );
```

> The same file registers `get-source-languages`, `get-target-languages`, `get-writing-styles`, `get-writing-tones`, `rephrase-text`, `translate-document`, `list-glossaries`, `get-glossary-info`, `get-glossary-dictionary-entries`, `list-style-rules`, `get-style-rule` and `get-custom-instruction` using the same `server.tool(name, description, schema, handler)` pattern; only the single `translate-text` tool is quoted here (one logical artifact per case).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states what the tool does (translate text to a target language)
- [ ] Cross-tool dependencies are explained (glossary requires source language; discover glossaries via `list-glossaries`)
- [ ] Guidance encourages reviewing optional parameters

### 2. Schema Correctness
- [ ] The tool exposes a concrete input schema (Zod object converted to JSON Schema by the MCP SDK)
- [ ] Types are accurate (`string`, `string|string[]`, `boolean`, `enum`, `array`)
- [ ] Required vs optional parameters are distinguishable (`text`, `targetLangCode` required; rest optional)
- [ ] `enum` domains are declared (`formality`, `splitSentences`)

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Formats are documented inline (ISO 639-1 language codes, `max 10 instructions, 300 chars each`)
- [ ] Conditional behavior is explained (`sourceLangCode` optional for auto-detection; required when a glossary is used)

### 4. Integration Compatibility
- [ ] Conforms to the MCP tool model (`server.tool(name, description, schema, handler)`)
- [ ] Zod schema is transpiled to JSON Schema, consumable by standard function-calling clients
- [ ] Handlers are injected (`registerTools(server, handlers)`), separating registration from execution

### 5. Extensibility & Maintainability
- [ ] Shared description constants (`languageCodeDescription`, `styleRuleDescription`) keep wording consistent
- [ ] The `textInput(verb)` factory produces a reusable single-string-or-array schema
- [ ] Enum vocabularies are centralized (`formalityTypes`, `writingStyles`, `writingTones`)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "translate 'Good morning' into German"; verify `translate-text` with `text` and `targetLangCode: "de"`.
2. Issue "rephrase this paragraph more formally" (no language change); verify the correct tool selection between `translate-text` and `rephrase-text`.
3. Issue "translate these three sentences into French, one at a time"; verify `text` accepts an array.

### Boundary Test Cases
1. `text` as a single string vs an array of strings; verify both are accepted.
2. `formality` at each enum value (`less`, `more`, `default`, `prefer_less`, `prefer_more`).
3. `glossaryId` provided without `sourceLangCode`; verify the documented requirement is surfaced.
4. `splitSentences: "nonewlines"` with multi-line input; verify line breaks are preserved.

### Negative Test Cases
1. Call without `targetLangCode`; verify schema validation rejects the call.
2. `formality: "polite"` (not in enum); verify rejection.
3. `customInstructions` with more than 10 items; verify the documented limit is enforced or warned.
4. Ambiguous request ("make this better") that conflates rephrasing and translation; verify the model clarifies intent.

## Notes
- DeepL is a commercial machine-translation service; this case quotes a single tool (`translate-text`) from the official DeepL MCP server.
- The schema is authored in Zod and converted to JSON Schema by the MCP SDK at registration time.
- License is MIT; long verbatim quotation is permissible.
