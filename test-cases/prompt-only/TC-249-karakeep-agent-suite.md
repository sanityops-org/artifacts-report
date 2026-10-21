# TC-249: Karakeep - Bookmark Tagging and Summary Agent Suite

## Metadata

- Source Project: karakeep-app/karakeep
- GitHub: https://github.com/karakeep-app/karakeep
- Commit SHA: 5c72fa95807df2d7dd96f0c9ac52a536b5bf3cfc
- License: AGPL-3.0
- Artifact Type: Business-embedded logical artifacts (prompt components)
- Business Scenario: Read-it-later / bookmarking; AI-assisted tagging and summarization
- Collection Date: 2026-10-21
- Collection Method: Shallow clone at the pinned commit; verbatim extraction from TypeScript prompt builders. No rewriting or completion; template placeholders preserved as-is.
- Unit of Analysis: Prompt component (verbatim)

## Project Overview

Karakeep (previously Hoarder) is a self-hostable "bookmark-everything" read-it-later application organized as a Turborepo monorepo, with a Next.js web app, a Hono/tRPC API, Drizzle ORM persistence, a browser extension, mobile and CLI clients, and a background worker process. Saved items are typed bookmarks: links, plain text notes, or assets (images and PDFs). Background workers run an inference pipeline that performs automatic tagging and summarization through a pluggable inference client (text and image models) and additionally produces embeddings for similarity search. Prompt construction is centralized in `packages/shared/prompts.ts`; per-user customization is stored in a `customPrompts` table whose `appliesTo` column scopes a prompt to `all_tagging`, `text`, `images`, or `summary`. Tagging behavior is further parameterized by a user-selected tag style (for example `lowercase-hyphens` or `camelCase`), a target language (`inferredTagLang`), and either a curated tag list or a set of potentially relevant tags retrieved from similar bookmarks. Summaries are stored on the bookmark record, while AI-generated tags are attached with provenance `attachedBy: "ai"`.

## Business Loop

1. **Save item** - a user saves a bookmark (link, text, image, or PDF); the application enqueues background inference jobs.
2. **Analyze item** - the inference worker selects a content path: plain-text extraction for links, raw text for notes, image bytes (base64) for images, or extracted asset content for PDFs. For images, an OCR preprocessing step can extract text first.
3. **Resolve tagging context** - the worker loads the user's `tagStyle`, `inferredTagLang`, and custom prompts. If `curatedTagIds` are configured, their tag names become the curated list; otherwise the worker looks up similar bookmarks in the vector store and collects their tags as potentially relevant tags.
4. **Generate tags** - a prompt is assembled from the base rules, curated/potential tag instructions, tag style instruction, and custom prompts, then sent to the text or image inference model, which must answer with a JSON object containing a `tags` array.
5. **Persist tags** - inferred tag names are normalized (leading `#` stripped, trimmed, lowercased and stripped of spaces/hyphens/underscores for matching), matched against existing tags, created when missing, and attached to the bookmark; prior AI tags are detached first.
6. **Generate summary** - a separate job summarizes the link title, description, content, publisher, author, and URL in 3-4 sentences in the configured language, and stores the result in the bookmark's `summary` field.
7. **Store for retrieval** - tags, summary, and embeddings feed the dashboard tag browsing, search, rules, and webhooks.

Concrete entities: bookmark, bookmark tag, tag style, language (`lang`), custom prompt, curated tags, potential relevant tags, summary, inference response.

## Logical Artifact Inventory

### 1. Image Tagging Prompt

- **Source:** `packages/shared/prompts.ts`
- **Line Range:** L15-L48 (function `buildImagePrompt`); prompt literal L28-L47
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized
- **Parameterization:** `lang` (target tag language), `customPrompts: string[]` (joined as `- ` bullet lines), `tagStyle: ZTagStyle` (rendered through `getTagStylePrompt`), `curatedTags?: string[]` (rendered through `getCuratedTagsPrompt`), `potentialRelevantTags?: string[]` (rendered through `getPotentialRelevantTagsPrompt`). The image itself is supplied out-of-band as a base64 attachment by the inference client, not interpolated into the string.
- **Business Entities:** bookmark image, tag, tag language, tag style, curated tags, potential relevant tags, custom prompts, failure/interstitial page detection

```text
You are an expert whose responsibility is to help with automatic tagging for a read-it-later/bookmarking app.
Analyze the attached image and suggest relevant tags that describe its key themes, topics, and main ideas. The rules are:
- Prefer concrete, durable tags: named products, technologies, projects, standards, subject areas, and important concepts.
- Include only retrieval-worthy tags that describe the saved item's intended content, not incidental UI or page chrome.
- The tags must be in ${lang}.
- Keep each tag short: ideally 1-3 words. Do not include parenthetical explanations, comma-separated examples, or long descriptive phrases inside a tag.
- Prefer durable subject tags over one-off facts, examples, source organizations, page sections, or implementation details unless they are central to the whole item.
- Do NOT generate any tags if the image is mainly:
    - A screenshot of an error, unavailable, forbidden, unauthorized, not found, DNS, timeout, or service failure page
    - A Cloudflare/security check, CAPTCHA, bot check, anti-DDoS challenge, browser verification, or access-blocked page
    - Boilerplate content such as cookie consent, login walls, GDPR notices, navigation menus, or a blank/empty image
  In these cases, return an empty tags array. Do not tag the failure/interstitial page itself.
- Aim for 10-15 tags.
- If there are no good tags, leave the array empty.
${curatedInstruction}
${potentialRelevantTagsInstruction}
${tagStyleInstruction}
${customPrompts && customPrompts.map((p) => `- ${p}`).join("\n")}
You must respond in valid JSON with the key "tags" and the value is list of tags. Don't wrap the response in a markdown code.
```

### 2. Text Tagging Prompt

- **Source:** `packages/shared/prompts.ts`
- **Line Range:** L53-L91 (function `constructTextTaggingPrompt`); prompt literal L67-L90
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized
- **Parameterization:** `lang`, `customPrompts: string[]`, `content: string` (interpolated inside `<TEXT_CONTENT>` tags), `tagStyle: ZTagStyle`, `curatedTags?: string[]`, `potentialRelevantTags?: string[]`. Callers may prepend structured metadata to `content` (for links: `URL:`, `Title:`, `Description:`, `Content:`) or prefix it with `Content:` for PDF assets.
- **Business Entities:** bookmark text/link/PDF content, tag, tag language, tag style, curated tags, potential relevant tags, custom prompts, boilerplate/failure content

```text
You are an expert whose responsibility is to help with automatic tagging for a read-it-later/bookmarking app.
Analyze the TEXT_CONTENT below and suggest relevant tags that describe its key themes, topics, and main ideas. The rules are:
- Prefer concrete, durable tags: named products, technologies, projects, standards, subject areas, and important concepts.
- Include only retrieval-worthy tags that describe the saved item's intended content, not incidental page chrome.
- The tags must be in ${lang}.
- Keep each tag short: ideally 1-3 words. Do not include parenthetical explanations, comma-separated examples, or long descriptive phrases inside a tag.
- Prefer durable subject tags over one-off facts, examples, source organizations, page sections, or implementation details unless they are central to the whole item.
- Ignore any part of the content that is:
    - An error, unavailable, forbidden, unauthorized, not found, DNS, timeout, or service failure page
    - A Cloudflare/security check, CAPTCHA, bot check, anti-DDoS challenge, browser verification, or access-blocked page
    - Boilerplate content such as cookie consent, login walls, GDPR notices, navigation menus, or empty pages
  If useful metadata or other legitimate content remains, generate tags using only that information. Otherwise, return an empty tags array. Never tag the failure, interstitial, or boilerplate content itself.
- Aim for 3-5 tags.
- If there are no good tags, leave the array empty.
${curatedInstruction}
${potentialRelevantTagsInstruction}
${tagStyleInstruction}
${customPrompts && customPrompts.map((p) => `- ${p}`).join("\n")}

<TEXT_CONTENT>
${content}
</TEXT_CONTENT>
You must respond in JSON with the key "tags" and the value is an array of string tags.
```

### 3. Summary Prompt

- **Source:** `packages/shared/prompts.ts`
- **Line Range:** L96-L107 (function `constructSummaryPrompt`); prompt literal L101-L106
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized
- **Parameterization:** `lang` (output language), `customPrompts: string[]` (joined as `- ` bullet lines), `content: string` (interpolated after the four-space indentation on the final line; callers pass a `Title:`/`Description:`/`Content:`/`Publisher:`/`Author:`/`URL:` block).
- **Business Entities:** bookmark summary, tag language, custom summary prompts, link metadata

```text
Summarize the following content responding ONLY with the summary. You MUST follow the following rules:
- Summary must be in 3-4 sentences.
- The summary must be in ${lang}.
${customPrompts && customPrompts.map((p) => `- ${p}`).join("\n")}
    ${content}
```

### 4. OCR Extraction Prompt

- **Source:** `packages/shared/prompts.ts`
- **Line Range:** L146-L157 (function `buildOCRPrompt`); prompt literal L147-L156
- **Type:** System Prompt
- **Composability:** Standalone (zero parameters)
- **Parameterization:** None. The image is attached by the caller; the prompt is a constant string.
- **Business Entities:** image asset, extracted text, OCR preprocessing

```text
You are an OCR (Optical Character Recognition) expert. Your task is to extract ALL text from this image.

Rules:
- Extract every piece of text visible in the image, including titles, body text, captions, labels, watermarks, and any other textual content.
- Preserve the original structure and formatting as much as possible (e.g., paragraphs, lists, headings).
- If text appears in multiple columns, read from left to right, top to bottom.
- If text is partially obscured or unclear, make your best attempt and indicate uncertainty with [unclear] if needed.
- Do not add any commentary, explanations, or descriptions of non-text elements.
- If there is no text in the image, respond with an empty string.
- Output ONLY the extracted text, nothing else.
```

### 5. Tag Style Instruction

- **Source:** `packages/shared/utils/tag.ts`
- **Line Range:** L12-L30 (function `getTagStylePrompt`)
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized (single enum switch)
- **Parameterization:** `style: TagStyle` where `TagStyle = ZTagStyle`, one of `lowercase-hyphens`, `lowercase-spaces`, `lowercase-underscores`, `titlecase-spaces`, `titlecase-hyphens`, `camelCase`, `as-generated`. Lines 1-6 of the block below correspond, in order, to those first six keys; `as-generated` and the `default` branch return an empty string, so no text is emitted for that style.
- **Business Entities:** tag style preference, tag naming convention

```text
- Use lowercase letters with hyphens between words (e.g., 'machine-learning', 'web-development')
- Use lowercase letters with spaces between words (e.g., 'machine learning', 'web development')
- Use lowercase letters with underscores between words (e.g., 'machine_learning', 'web_development')
- Use title case with spaces between words (e.g., 'Machine Learning', 'Web Development')
- Use title case with hyphens between words (e.g., 'Machine-Learning', 'Web-Development')
- Use camelCase format (e.g., 'machineLearning', 'webDevelopment')
```

### 6. Curated Tags Instruction

- **Source:** `packages/shared/utils/tag.ts`
- **Line Range:** L32-L37 (function `getCuratedTagsPrompt`)
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized
- **Parameterization:** `curatedTags?: string[]` joined with `", "`. When the list is absent or empty, the function returns an empty string and the line disappears from the composed prompt.
- **Business Entities:** curated tag list, tag vocabulary constraint

```text
- ONLY use tags from this predefined list: [${curatedTags.join(", ")}]. Do not create any new tags outside this list. If no tags fit, don't emit any.
```

### 7. Potential Relevant Tags Instruction

- **Source:** `packages/shared/utils/tag.ts`
- **Line Range:** L39-L46 (function `getPotentialRelevantTagsPrompt`)
- **Type:** Prompt Builder
- **Composability:** Runtime-parameterized
- **Parameterization:** `potentialRelevantTags?: string[]` joined with `", "`. When the list is absent or empty, the function returns an empty string and the line disappears from the composed prompt.
- **Business Entities:** similar bookmarks, existing tag vocabulary, embedding-based retrieval

```text
- Similar bookmarks were tagged with the following tags (reuse if possible, ignore if irrelevant): ${potentialRelevantTags.join(", ")}
```

## Composition Notes

All three tagging/summary literals in `packages/shared/prompts.ts` open with a newline immediately after the opening backtick; the quoted blocks start at the first non-empty line. `${...}` sequences are TypeScript template interpolations evaluated at call time and are preserved above exactly as written.

**Image prompt order.** `buildImagePrompt` computes `tagStyleInstruction`, `curatedInstruction`, and `potentialRelevantTagsInstruction` first, then concatenates, in this exact order: base role sentence and image analysis rules; the `${lang}` rule; tag length and durability rules; the image failure/boilerplate exclusion rule; the `10-15` tag target; `${curatedInstruction}`; `${potentialRelevantTagsInstruction}`; `${tagStyleInstruction}`; custom prompts rendered as `- <prompt>` lines joined by newlines; the JSON output contract requiring a `tags` key and forbidding a markdown code fence.

**Text prompt order.** `constructTextTaggingPrompt` follows the same order (base rules, `${curatedInstruction}`, `${potentialRelevantTagsInstruction}`, `${tagStyleInstruction}`, custom prompts), but adds a blank line and a `<TEXT_CONTENT>` ... `</TEXT_CONTENT>` wrapper around `${content}`, followed by a JSON output contract. The text prompt targets `3-5` tags versus `10-15` for images.

**Summary prompt order.** `constructSummaryPrompt` emits the fixed instruction line, the 3-4 sentence rule, the `${lang}` rule, the custom summary prompts as `- ` bullet lines, and finally the content indented by four spaces. It requests free-form text rather than JSON.

**Conditional segments.** `getTagStylePrompt` returns `""` for `as-generated` (the default when the user has no tag style). `getCuratedTagsPrompt` and `getPotentialRelevantTagsPrompt` return `""` for empty or missing lists. Because each helper output occupies its own template line, an empty return leaves a blank line in the final prompt rather than removing the line.

**Curated tags versus potential tags are mutually exclusive at runtime.** In `apps/workers/workers/inference/tagging.ts`, if `userSettings.curatedTagIds` is non-empty, tag names are resolved from the database and passed as `curatedTagNames`; only in the `else` branch does the worker call the vector store for potentially relevant tags from up to 10 similar bookmarks (ranking score threshold 0.75), collecting up to 100 distinct tag names and keeping the shortest ones until the joined name list reaches 1000 characters. Both are then passed to the image, text, and PDF tagging paths.

**Custom prompt scoping and placeholders.** `fetchCustomPrompts` selects rows whose `appliesTo` is either `all_tagging` or the current surface (`text` for links/notes/PDF, `images` for image bookmarks), while the summary job selects `appliesTo = "summary"`. Before insertion, `$tags`, `$aiTags`, and `$userTags` placeholders in a custom prompt are replaced with bracketed, comma-joined tag name lists (all tags, tags with human attachments defaulting to true, and human-only tags respectively). Custom prompts are appended after the built-in tag-style line and before the content/output contract, so user instructions sit closest to the content for tagging, and before the content for summaries.

**Token budgeting.** `packages/shared/prompts.server.ts` wraps the text and summary builders: it first renders the prompt with empty content to measure token cost using the `o200k_base` tokenizer, subtracts that from `serverConfig.inference.contextLength`, truncates the content to the remaining token budget, and re-renders. Content is also passed through `preprocessContent`, which collapses runs of ten or more whitespace characters into one.

## Coverage and Exclusions

**Extracted.** All prompt text in `packages/shared/prompts.ts`: `buildImagePrompt`, `constructTextTaggingPrompt`, `constructSummaryPrompt`, and `buildOCRPrompt`. All prompt text in `packages/shared/utils/tag.ts`: `getTagStylePrompt` (six non-empty style strings; `as-generated` returns empty), `getCuratedTagsPrompt`, and `getPotentialRelevantTagsPrompt`.

**Excluded (no new prompt text).** `buildTextPromptUntruncated` and `buildSummaryPromptUntruncated` in `prompts.ts` delegate to the builders above with `preprocessContent` applied. `buildTextPrompt` and `buildSummaryPrompt` in `packages/shared/prompts.server.ts` are token-budget wrappers around the same builders. `preprocessContent`, `parseJsonFromLLMResponse`, `tagNormalizer`, and `connectTags` are supporting logic, not prompt components. Also excluded: test files, UI strings and the AI settings prompt preview component (`apps/web/components/settings/AISettings.tsx`), landing-page privacy/terms content, API documentation, and database schema definitions. No prompt text outside the two source files was included, and no strings were paraphrased, reordered, or completed.
