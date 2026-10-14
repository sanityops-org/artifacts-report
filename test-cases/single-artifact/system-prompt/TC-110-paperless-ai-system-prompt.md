# TC-110: Paperless-AI - System Prompt Evaluation Case

## Metadata
- **Source Project**: Paperless-AI (clusterzx/paperless-ai) — automated document analyzer for Paperless-ngx
- **License**: MIT (project `LICENSE` states "This project is licensed under the MIT License")
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the project's source repository (default branch `main`) on 2026-10-13. Exact URLs:
  - Raw (prompt): `https://cdn.jsdelivr.net/gh/clusterzx/paperless-ai@main/config/config.js` (mirror of `https://raw.githubusercontent.com/clusterzx/paperless-ai/main/config/config.js`)
  - Consuming code: `https://cdn.jsdelivr.net/gh/clusterzx/paperless-ai@main/services/openaiService.js`

## Original Artifact Content

The following are the verbatim system-prompt templates from `config/config.js`. They are the system messages sent to the model when analyzing an incoming document: `specialPromptPreDefinedTags` (used when tag-matching against a predefined tag list is enabled) and `mustHavePrompt` (the appended output-contract). `${process.env.PROMPT_TAGS}` is inlined at runtime.

```javascript
  specialPromptPreDefinedTags: `You are a document analysis AI. You will analyze the document. 
  You take the main information to associate tags with the document. 
  You will also find the correspondent of the document (Sender not receiver). Also you find a meaningful and short title for the document.
  You are given a list of tags: ${process.env.PROMPT_TAGS}
  Only use the tags from the list and try to find the best fitting tags.
  You do not ask for additional information, you only use the information given in the document.
  
  Return the result EXCLUSIVELY as a JSON object. The Tags and Title MUST be in the language that is used in the document.:
  {
    "title": "xxxxx",
    "correspondent": "xxxxxxxx",
    "tags": ["Tag1", "Tag2", "Tag3", "Tag4"],
    "document_date": "YYYY-MM-DD",
    "language": "en/de/es/..."
  }`,
  mustHavePrompt: `  Return the result EXCLUSIVELY as a JSON object. The Tags, Title and Document_Type MUST be in the language that is used in the document.:
  IMPORTANT: The custom_fields are optional and can be left out if not needed, only try to fill out the values if you find a matching information in the document.
  Do not change the value of field_name, only fill out the values. If the field is about money only add the number without currency and always use a . for decimal places.
  {
    "title": "xxxxx",
    "correspondent": "xxxxxxxx",
    "tags": ["Tag1", "Tag2", "Tag3", "Tag4"],
    "document_type": "Invoice/Contract/...",
    "document_date": "YYYY-MM-DD",
    "language": "en/de/es/...",
    %CUSTOMFIELDS%
  }`,
```

Verbatim usage from `services/openaiService.js` (shows how the templates are combined and how the tag-matching branch is selected):

```javascript
      if (process.env.USE_PROMPT_TAGS === 'yes') {
        promptTags = process.env.PROMPT_TAGS;
        systemPrompt = `
        Take these tags and try to match one or more to the document content.\n\n
        ` + config.specialPromptPreDefinedTags;
      }
      if (customPrompt) {
        console.log('[DEBUG] Replace system prompt with custom prompt via WebHook');
        systemPrompt = customPrompt + '\n\n' + config.mustHavePrompt;
      }
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Role is explicit ("You are a document analysis AI… analyze the document")
- [ ] Each output field is defined (title, correspondent, tags, document_date, language)
- [ ] Correspondent is disambiguated ("Sender not receiver")

### 2. Output-Contract / Structured Output
- [ ] "Return the result EXCLUSIVELY as a JSON object" is stated twice (reinforced)
- [ ] Exact JSON schema is provided
- [ ] Constraint that Tags/Title/Document_Type must match the document language

### 3. Grounding & Anti-Hallucination
- [ ] "You only use the information given in the document"
- [ ] "You do not ask for additional information" (no interactive fallback)
- [ ] Tag constraint: "Only use the tags from the list" when a predefined list is supplied

### 4. Data-Formatting Rules
- [ ] Money values: number only, no currency, `.` as decimal separator
- [ ] `field_name` values must not be changed; only values filled
- [ ] Optional custom_fields may be omitted when no matching information exists

### 5. Testability
- [ ] Output is machine-parseable (strict JSON) → automatable pass/fail
- [ ] Tag-list conformance is checkable (subset of `PROMPT_TAGS`)
- [ ] `%CUSTOMFIELDS%` placeholder substitution is mechanically verifiable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Output-Contract / Structured Output | 30% | | |
| Grounding & Anti-Hallucination | 20% | | |
| Data-Formatting Rules | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Run a real invoice; verify valid JSON with `tags`, `correspondent`, `title`, `document_date`, `language` populated.
2. Enable `USE_PROMPT_TAGS=yes` with a fixed tag list; verify every returned tag is from the list.
3. Provide a document with monetary values; verify numbers use `.` and omit currency symbols.

### Boundary Test Cases
1. Document with no clear correspondent — verify JSON validity is preserved and field handling is sane.
2. Non-English document — verify Tags/Title/Document_Type are emitted in the document's language.
3. Empty/very long document content (token truncation path) — verify JSON still parses.

### Negative Test Cases
1. Verify the model never returns prose outside the JSON object ("EXCLUSIVELY as a JSON object").
2. Verify it does not invent tags outside the predefined list when tag-matching is enabled.
3. Verify it does not alter `field_name` keys of custom_fields.

## Notes
- This is an end-user business document-processing agent (auto-tagging/archiving of Paperless-ngx documents), not a coding agent.
- The two templates are combined into a single system message at runtime (`customPrompt + '\n\n' + config.mustHavePrompt`, or the predefined-tags branch); tests should cover both branches.
- `%CUSTOMFIELDS%` and `${process.env.PROMPT_TAGS}` are runtime substitutions; treat them as required configuration in tests.
- MIT license permits full quotation and modification.
