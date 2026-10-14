# TC-236: mcp-local-translate Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: damoqiongqiu/mcp-local-translate
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions: name, description, JSON-Schema `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/server/types.ts` (tool definitions) — `https://raw.githubusercontent.com/damoqiongqiu/mcp-local-translate/HEAD/src/server/types.ts`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/damoqiongqiu/mcp-local-translate/HEAD/LICENSE`
  - Contributor guide / structure reference — `https://raw.githubusercontent.com/damoqiongqiu/mcp-local-translate/HEAD/CONTRIBUTING.md`

## Original Artifact Content

Verbatim excerpt from `src/server/types.ts` (the `translate` tool):

```typescript
export const TRANSLATE_TOOL: Tool = {
  name: 'translate',
  description:
    'Translate text between 200+ languages using the NLLB-200 model, running entirely on your local CPU. No cloud APIs, no data leaves your machine.',
  inputSchema: {
    type: 'object' as const,
    properties: {
      text: {
        type: 'string',
        description: 'The text to translate',
      },
      source_lang: {
        type: 'string',
        description:
          'Source language code (FLORES-200, ISO 639-1, or language name). Examples: "eng_Latn", "en", "English", "zho_Hans", "zh", "中文". Use list_languages to see all supported codes.',
      },
      target_lang: {
        type: 'string',
        description:
          'Target language code (FLORES-200, ISO 639-1, or language name). Examples: "zho_Hans", "zh", "中文", "eng_Latn", "en", "English".',
      },
      glossary: {
        type: 'object',
        description:
          'Optional term mapping for consistent translation of domain-specific vocabulary. Keys are source terms, values are their fixed translations. Example: {"Transformer": "transformer", "embedding": "嵌入"}. Terms are replaced with placeholders before translation and restored afterwards.',
      },
    },
    required: ['text', 'source_lang', 'target_lang'],
  },
}
```

Verbatim excerpt from `src/server/types.ts` (the `translate_batch` tool):

```typescript
export const TRANSLATE_BATCH_TOOL: Tool = {
  name: 'translate_batch',
  description:
    'Translate multiple texts at once with a single model pipeline invocation. Much faster than calling translate repeatedly for batch workloads. All texts must share the same source and target languages.',
  inputSchema: {
    type: 'object' as const,
    properties: {
      texts: {
        type: 'array',
        items: { type: 'string' },
        description: 'Array of text strings to translate',
      },
      source_lang: {
        type: 'string',
        description:
          'Source language code (same format as translate tool). All texts share this source language.',
      },
      target_lang: {
        type: 'string',
        description:
          'Target language code (same format as translate tool). All texts share this target language.',
      },
      glossary: {
        type: 'object',
        description: 'Optional term mapping applied to all texts in the batch.',
      },
    },
    required: ['texts', 'source_lang', 'target_lang'],
  },
}
```

Verbatim excerpt from `src/server/types.ts` (the `status` and `list_languages` tools):

```typescript
export const STATUS_TOOL: Tool = {
  name: 'status',
  description:
    'Check the current status of the translation engine. Returns model readiness, download progress, and endpoint connectivity info. Useful before calling translate to avoid timeouts during model download.',
  inputSchema: {
    type: 'object' as const,
    properties: {},
  },
}

export const LIST_LANGUAGES_TOOL: Tool = {
  name: 'list_languages',
  description:
    'List all 200+ languages supported by the NLLB-200 translation model. Optionally filter/search by keyword.',
  inputSchema: {
    type: 'object' as const,
    properties: {
      query: {
        type: 'string',
        description:
          'Optional search term to filter languages by name, code, or language family. Leave empty to list all.',
      },
    },
  },
}
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool does and when to use it
- [ ] `translate` vs `translate_batch` are clearly disambiguated (single vs bulk)
- [ ] `status` explains a non-obvious benefit (avoiding model-download timeouts)

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`, `required`) for each tool
- [ ] `translate_batch.texts` is a correctly typed array with `items: { type: 'string' }`
- [ ] `status` uses an empty-properties object correctly (no arguments)

### 3. Parameter Description Quality
- [ ] Every parameter has a `description`
- [ ] `source_lang`/`target_lang` document the accepted code systems (FLORES-200, ISO 639-1, or names) with examples
- [ ] `glossary` documents its shape, purpose, and placeholder behavior
- [ ] `list_languages.query` explains what fields it matches

### 4. Tool Identity & Cross-tool Consistency
- [ ] Tool `name` values are unique (snake_case)
- [ ] Language-parameter descriptions cross-reference each other consistently
- [ ] `translate` and `translate_batch` share the same `source_lang`/`target_lang` semantics

### 5. Extensibility & Maintainability
- [ ] Tools are exported constants (`TRANSLATE_TOOL`, …) for reuse and testing
- [ ] Handlers (`server/index.ts`) are separated from tool definitions (`types.ts`)
- [ ] Language-code resolution is centralized (`translator/language-codes.ts`)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Tool Identity & Cross-tool Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "translate 'good morning' into Japanese"; verify `translate` with `text`, `source_lang: "en"`, `target_lang: "ja"` (or a valid alias).
2. Issue "translate these 5 product descriptions into German"; verify `translate_batch` with a `texts` array sharing one language pair.
3. Issue "what languages can you translate?"; verify `list_languages` is selected.

### Boundary Test Cases
1. `source_lang` given as a FLORES-200 code (`eng_Latn`) vs a name (`English`) vs `en`; verify all three accepted forms work.
2. `glossary` with multiple entries; verify the term mapping is accepted and applied.
3. Call `translate` before the model has downloaded; verify `status` is the suggested pre-check.

### Negative Test Cases
1. Call `translate` without `target_lang`; verify the required field is enforced.
2. `translate_batch` with a non-array `texts` (single string); verify type validation rejects it.
3. Ask to translate between two languages with no source text; verify the model requests the text rather than fabricating it.

## Notes
- This artifact is the tool-selection surface an LLM sees for a fully local, offline translation server (NLLB-200; no cloud API).
- The language-parameter descriptions are a strong example of documenting multiple accepted input formats with multilingual examples.
- License is MIT; verbatim quotation of the tool schemas is permissible.
