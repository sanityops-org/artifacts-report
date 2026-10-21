# TC-248: Mealie - Recipe Import Agent Suite

## Metadata

- Source Project: mealie-recipes/mealie
- GitHub: https://github.com/mealie-recipes/mealie
- Commit SHA: 9f9ef5f0bb594a7ebdcfb6365aa6e2de97496713
- License: AGPL-3.0
- Artifact Type: Business-embedded logical artifacts (prompt components)
- Business Scenario: Self-hosted recipe management; AI-assisted recipe import and normalization
- Collection Date: 2026-10-21
- Collection Method: Shallow clone at the pinned commit; verbatim extraction of the 7 shipped prompt templates. No rewriting or completion; template placeholders preserved as-is.
- Unit of Analysis: Prompt component (verbatim)

## Project Overview

Mealie is a self-hosted recipe manager, meal planner, and shopping list with a FastAPI backend (Python 3.14) and a Nuxt 4 / Vue 3 frontend, persisted through SQLAlchemy on SQLite or PostgreSQL. Recipes are added by importing a URL, pasting text, uploading images or video, or entering data manually, and the collection is scoped per group and household. The AI features are configured per group as OpenAI-compatible providers, each with its own `base_url`, `api_key`, `model`, `timeout`, and optional headers/params, and providers are assigned to three roles: default, image, and audio. All shipped prompt templates are plain `.txt` files under `mealie/services/openai/prompts/`, addressed in dot notation (for example `recipes.build-recipe`) by `OpenAIService.get_prompt`, which may apply group-level overrides before returning the text. Every model call goes through `OpenAIService.get_response`, which sends the prompt as the `system` message, the caller's data as the `user` message, and a Pydantic model as the `response_format` schema. Recipe imports are orchestrated by `RecipeImportWorkflow`, used by the `/recipes/create/ai` route and by `RecipeScraperOpenAI`, the fallback strategy for `/recipes/create/url`; the workflow returns a draft recipe and never persists it.

## Business Loop

The suite implements an import-and-normalization loop in which each stage hands a progressively more structured artifact to the next:

1. **Transcribe / compile** -- raw source material (fetched webpage text, schema.org JSON, plain text, uploaded images, or a downloaded video's audio) becomes one faithful markdown *Compiled Source Document*. `system/compile-source` performs this for pages and images; `system/transcribe-audio` supplies the transcript when a video has no usable subtitles.
2. **Build** -- the compiled document becomes a draft *recipe*: `name`, `description`, `recipe_yield` (servings), `total_time` / `prep_time` / `perform_time`, an ordered list of *ingredients* kept as single lines of text, an ordered list of *instructions* with optional section titles, *notes*, and *nutrition*.
3. **Parse ingredients** -- each ingredient line is split into `quantity`, `unit`, `food`, `note`, and `substitutes`, so ingredients can be linked to the group's *food* and *unit* records and aggregated onto shopping lists.
4. **Resolve organizers** -- the recipe is assigned *tags*, *categories*, and *tools*, preferring names that already exist in the group's collection and optionally creating missing ones.
5. **Translate** -- the structured recipe is rewritten into the caller's target language with every field, ingredient, instruction, and note kept in place.

At runtime the workflow executes compile -> build -> translate -> resolve-organizers; ingredient parsing is not a workflow step but a separate parser path (`RegisteredParser.openai`) reached when the caller parses or saves ingredient lines, and `recipes.parse-recipe-video` belongs to a separate video-URL scraper strategy rather than to the workflow.

## Logical Artifact Inventory

### 1. build-recipe

- Source: `mealie/services/openai/prompts/recipes/build-recipe.txt`
- Line Range: L1-L19
- Type: Task Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. The compiled source document is appended by the caller as the user message, prefixed with `Below is the transcribed recipe source.`; group-level overrides and appended data injections may be concatenated after the template at runtime.
- Business Entities: recipe, ingredient (single-line text), instruction step, section title, notes, nutrition, total_time / prep_time / perform_time, source-supplied user text.

```text
You convert a transcribed recipe source document into structured recipe data.

The user message contains the transcribed source. Everything you return must come from it. Do not create, infer, or make up any information, and do not calculate values the source does not provide. Leave a field empty rather than guessing at it.

When converting:
- Do not translate. Preserve the source's original language in every text field.
- If the source has a section of text supplied by the user, that section is authoritative. Where it disagrees with the rest of the source, follow it: if it names the recipe, use their name; if it corrects or adds a detail, use theirs.
- Keep ingredients and instructions in their original order.
- Preserve section headings by setting the title on the first ingredient or instruction of each section, and leaving it blank on the rest.
- Keep each ingredient as a single line of text, exactly as written, e.g. "2 cups of onions, chopped".
- If a recipe does not contain an explicit list of ingredients, collect and extract the ingredients directly from the instructions.
- When the source already presents its instructions as discrete steps, keep those steps as they are. Do not split or merge them.
- When the source narrates cooking continuously, as a video transcript does, group the actions into steps a cook would recognize. Actions done back to back on the same thing belong together: "Drain the pasta, set it aside, and turn off the heat" is one step, not three.
- Start a new step where the cook's attention shifts: a wait or a cooking time begins, a different component or pan is started, the temperature changes, or something goes into or comes out of the oven.
- Do not overcorrect. A recipe should not come out as one or two long steps, and no step should be too long to follow without re-reading it.
- Strip numeric prefixes like "1." or "Step 1", but keep word prefixes like "First".
- Put tips, variations, storage advice, and similar asides into notes rather than instructions.
- Only fill in nutrition if the source states it.
- If the source gives only one time, use total_time and leave prep_time and perform_time empty.
```

### 2. parse-recipe-ingredients

- Source: `mealie/services/openai/prompts/recipes/parse-recipe-ingredients.txt`
- Line Range: L1-L14
- Type: Task Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. The caller supplies a JSON array of ingredient strings as the user message and may append a `###` data-injection section listing unit names from the group's units database.
- Business Entities: ingredient, quantity, unit, food, note, substitutes, recipe (implicit owner of the ingredient list).

```text
Parse ingredient strings into components. You will receive a list of one or more ingredients. It is critical that you return the same number of ingredients as given and in the same order.

When parsing:
- If uncertain about quantity, unit, or food, put the entire string in the note field
- Respect grammar rules for multiple languages
- Do not translate. Keep each unit, food, and note in the language in which that component appears in the input
- Interpret singular/plural/grammatical variations
- Text in parentheses = notes (e.g., "3 potatoes (roughly chopped)" → note: "roughly chopped"), unless it names an alternative food
- Alternative foods the text explicitly offers go in substitutes, not the note (e.g., "1 cup chicken stock (or broth)" → food: "chicken stock", substitutes: ["broth"]). Only record alternatives stated in the text; never suggest your own
- Correct common typos (e.g., "potatos" → "potatoes")
- Recognize units: tablespoon, teaspoon, gram, tsp, tbsp, oz, sprig, can, bundle, bunch, unit, cube, package, pinch
- For ranges (e.g., "3-5", "1 to 2"), use the lower number
- All text must appear somewhere, or otherwise be accounted for; if converting "2 dozen" → "24", don't put "dozen" elsewhere. If you're unsure, put extra text in the notes. Text captured in substitutes is already accounted for and must not be repeated in the note
- When a single input ingredient contains multiple quantities or phrases such as "plus", "and", or commas, do not split it into multiple ingredients. Return exactly one parsed ingredient for that input and keep the secondary quantity or preparation detail in the note field. For example, "1 tablespoon fresh lemon juice, plus 2 teaspoons zest" must be returned as one ingredient, not two.
```

### 3. parse-recipe-video

- Source: `mealie/services/openai/prompts/recipes/parse-recipe-video.txt`
- Line Range: L1-L7
- Type: Task Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. The caller injects `Title:`, `Description:` (the video's caption text), and `Transcription:` lines as the user message, and binds the response to the recipe schema.
- Business Entities: recipe (schema.org Recipe), video transcript, caption text, ingredient list, instruction steps.

```text
You will receive a video transcript and the video's original caption text. Analyze BOTH inputs to generate a single, accurate recipe in schema.org Recipe format. Reference: https://schema.org/Recipe

Do not create or make up any information. If insufficient data is found, return an empty object.

- The video transcript is the primary source for instructions.
- The caption text is the primary source for the ingredient list and title.
- If there is a conflict (e.g., caption says "1 cup" but transcript says "1.5 cups"), trust the video transcript.
```

### 4. resolve-organizers

- Source: `mealie/services/openai/prompts/recipes/resolve-organizers.txt`
- Line Range: L1-L13
- Type: Task Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. The recipe is supplied as the user message (truncated compiled source when available, otherwise name / description / ingredient notes / instruction text), and up to three `###` data injections list the group's existing tags (capped at 200), categories, and tools.
- Business Entities: recipe, tags, categories, tools, user's existing collection (group organizer names).

```text
You assign tags, categories, and tools to a recipe, so it can be organized alongside the rest of a user's collection.

The user message contains the recipe. You may also be given the tags, categories, and tools that already exist in the user's collection.

Tags describe what the recipe is like: dietary information, occasion, season, cuisine, effort. Categories are the broader groups a recipe belongs to, such as the course or meal. Tools are the equipment needed to make it.

Rules:
- Only assign an organizer the recipe itself refers to. The recipe has to say it.
- Do not infer. Do not derive a cuisine from the ingredients, a course or meal from the kind of dish, an occasion or season from the style, or a diet from what the recipe happens to leave out.
- Only assign a tool when the recipe says that tool is used to make it.
- Returning empty lists is the correct answer for most recipes. A plain list of ingredients and steps, with nothing else said about it, has no organizers at all.
- When the recipe does refer to something that matches a name already in the user's collection, return that name exactly as it is written there, matching its spelling and capitalization.
- Do not invent names to fill out the lists, and do not repeat a name across tags, categories, and tools.
```

### 5. translate-recipe

- Source: `mealie/services/openai/prompts/recipes/translate-recipe.txt`
- Line Range: L1-L12
- Type: Task Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. The caller supplies `Translate the recipe below into <target language>.` followed by the draft recipe serialized as JSON in the recipe schema (nutrition omitted), and expects the same schema back.
- Business Entities: recipe, name, description, recipe_yield (servings), times, ingredients, instructions, notes, section titles, measurement units, target language.

```text
You translate a structured recipe into another language.

The user message names the target language and contains the recipe as JSON. Return the same structure, with every piece of text in it translated.

Rules:
- Translate every text field: the name, description, yield, times, every ingredient, every instruction, every note, and every section title.
- Return the same number of ingredients, instructions, and notes, in the same order. Do not merge, split, add, or drop entries.
- Keep each section title on the entry it arrived on, and leave it blank on the rest.
- Translate the recipe as it is written. Do not rewrite, improve, correct, summarize, or expand it, and do not add anything the recipe does not say.
- Do not convert between measurement systems and do not recalculate anything. Keep every number as it is and translate only the words around it, so "2 cups of flour" becomes "2 tasses de farine", not "480 ml de farine".
- Leave proper nouns and brand names alone, along with the names of dishes and ingredients that have no established translation in the target language.
- Return any field that is already written in the target language unchanged.
```

### 6. compile-source

- Source: `mealie/services/openai/prompts/system/compile-source.txt`
- Line Range: L1-L29
- Type: System Prompt
- Composability: runtime-parameterized
- Parameterization: No in-template placeholders. For web pages the caller supplies an extraction preamble plus the truncated page text (and the page's primary image URL when found); for images the caller supplies a sentence describing the attached images and passes them as image attachments. Group-wide instructions are not applied to this prompt because it lives in the `system` category.
- Business Entities: recipe, title, description/headnote, yield/servings, prep/cook/total time, ingredients with section headings, instruction steps, notes, storage advice, equipment, nutrition, attribution, recipe image URL, illegible text marker, `contains_recipe` flag.

```text
You transcribe recipe source material into a single plain-text document. You are not writing a recipe, you are making a faithful record of what the source says, so that a later step can turn it into structured data.

The user message contains the source material. It may be text extracted from a webpage, a schema.org JSON object, plain text, a video transcript, one or more images, or some combination. Assume everything you receive describes exactly one recipe.

Capture at least the following, when the source contains them:
- The recipe title
- The description, introduction, or headnote
- Yield or servings
- Prep time, cook time, and total time
- Every ingredient, in order, including any section headings such as "For the sauce"
- Every instruction step, in order, including any section headings
- Notes, tips, variations, and substitutions
- Storage, make-ahead, and reheating advice
- Equipment or tools mentioned
- Nutrition information
- Attribution, such as the author, publication, or source URL
- The URL of the recipe's image, if one appears in the source

Rules:
- Transcribe, do not summarize. If you are unsure whether something belongs, include it.
- The list above is a minimum, not a limit. Transcribe anything else the source says about the recipe, even when it doesn't fit one of the categories above. Serving suggestions, drink pairings, difficulty, cost, allergen information, dietary labels, ingredient substitutions, temperature or measurement conversions, and cultural or historical notes all belong in the document.
- Leave out anything on the page that isn't about the recipe, such as navigation, advertisements, cookie and subscription notices, reader comments, and links to other recipes.
- Do not create, infer, or make up any information that is not in the source.
- Do not translate. Preserve the original wording and language.
- Preserve the original ordering of ingredients and steps.
- Use markdown headings to separate sections so the content stays easy to read.
- If the source is one or more images, they may be photographs of a page, printed text, or handwriting. They may be rotated or poorly cropped. Work out which part of the image is the recipe and transcribe that. Multiple images are pages of the same recipe, in the order given.
- Mark any text you cannot read as [illegible] rather than guessing at it.
- If the source contains no recipe at all, set contains_recipe to false and leave the content empty.
```

### 7. transcribe-audio

- Source: `mealie/services/openai/prompts/system/transcribe-audio.txt`
- Line Range: L1-L1
- Type: System Prompt
- Composability: standalone
- Parameterization: None inside the template; the audio is supplied as a base64 audio attachment in the user message, and the caller pairs it with the fixed sentence `Attached is the audio data.`
- Business Entities: audio data, transcript (later treated as recipe source material).

```text
Transcribe any audio data provided to you. You should respond only with the audio transcription and nothing else.
```

## Composition Notes

**Prompt loading and naming.** `OpenAIService.get_prompt` resolves a dot-notation name to `prompts/<category>/<name>.txt`; the path is checked so it cannot escape the prompts directory. Names are enumerated by walking the directory, which is why the seven files above are exactly the user-customizable prompt surface. The templates are never concatenated with one another in a single request; each call uses exactly one template as the system message.

**Runtime assembly.** After the template is loaded, `_apply_prompt_overrides` may replace it (mode `override`) or append to it (mode `append`) with a group's saved customization, and any group-wide `global` instructions are appended for every prompt except those in the `system` category. Appended text is joined after the template with a `###` marker, the line `Additional instructions. These take priority over any instructions above that conflict with them.`, and a `---` separator. `data_injections` are appended in the same `###` / `---` shape with a description and a value (lists are JSON-encoded). Overrides are limited to 20,000 characters and store a hash of the built-in prompt so the UI can flag a template that changed after customization.

**Call sites.**

| Prompt | Call site | Path |
| --- | --- | --- |
| `system.compile-source` | `WebPageCompiler.compile` (web page text) and `ImageCompiler.compile` (uploaded images, vision provider) inside `CompileSourceStep` | `mealie/services/recipe/import_workflow/compilers/web_page.py`, `image.py` |
| `recipes.build-recipe` | `BuildRecipeStep.run` | `mealie/services/recipe/import_workflow/steps/build_recipe.py` |
| `recipes.translate-recipe` | `TranslateRecipeStep.run`, only when a target language differs from the source language | `mealie/services/recipe/import_workflow/steps/translate_recipe.py` |
| `recipes.resolve-organizers` | `ResolveOrganizersStep.run` | `mealie/services/recipe/import_workflow/steps/resolve_organizers.py` |
| `recipes.parse-recipe-ingredients` | `OpenAIParser._parse` in the ingredient parser service | `mealie/services/parser_services/openai/parser.py` |
| `recipes.parse-recipe-video` | `RecipeScraperOpenAITranscription.parse` (video-URL import) | `mealie/services/scraper/scraper_strategies.py` |
| `system.transcribe-audio` | `OpenAIService.transcribe_audio`, chat-completion fallback after the native transcription endpoint fails | `mealie/services/openai/openai.py` |

**Model configuration.** Each group stores `AIProvider` rows (`base_url`, `api_key`, `model`, `timeout` defaulting to 300 seconds, plus request headers and params) and assigns them to `default_provider_id`, `image_provider_id`, and `audio_provider_id`. `_get_provider` picks the image provider when any image attachment is present, the audio provider when audio is attached, and the default provider otherwise; a request carrying both image and audio is rejected. The model identifier is provider-defined, not hard-coded in the prompts. `transcribe_audio` first calls the provider's native `audio.transcriptions.create`; only if that fails does it fall back to the chat model with `system.transcribe-audio` and a base64 audio attachment.

**Request shape.** `_get_raw_response` sends `[{"role": "system", "content": prompt}, {"role": "user", "content": content}]` with `response_format=response_schema`, reads the raw body, strips `service_tier`, and raises on `length` or `content_filter` finish reasons before parsing the message content.

**Output schema coupling.** Prompts and schemas are tightly paired and must be changed together:

- `recipes.build-recipe` and `recipes.translate-recipe` both bind to `OpenAIRecipe` (`name`, `description`, `recipe_yield`, `total_time`, `prep_time`, `perform_time`, `ingredients[]` with `title`/`text`, `instructions[]` with `title`/`text`, `notes[]`, `nutrition`). The translate step round-trips the draft through the same schema, carrying nutrition and parsed time/serving values over unchanged.
- `system.compile-source` binds to `OpenAICompiledSource` (`contains_recipe`, `content`, `language`, `image_url`); `contains_recipe` is the only place the template's flag rule is realized, and `language` is what lets the translate step skip a same-language import.
- `recipes.parse-recipe-ingredients` binds to `OpenAIIngredients` (`ingredients[]` of `quantity`, `unit`, `food`, `note`, `substitutes[]`). The caller enforces the template's count requirement by raising when the returned list length differs from the input length.
- `recipes.resolve-organizers` binds to `OpenAIOrganizers` (`tags`, `categories`, `tools`); the resolver matches returned names case-insensitively against existing records and optionally creates missing ones.
- `recipes.parse-recipe-video` binds to `OpenAIRecipe` as well, but its response is converted directly into a `Recipe` by the scraper strategy instead of going through the workflow.
- `system.transcribe-audio` binds to `OpenAIText` (`text`).

**Workflow ordering and failure policy.** `DEFAULT_WORKFLOW_STEPS` is `CompileSourceStep`, `BuildRecipeStep`, `TranslateRecipeStep`, `ResolveOrganizersStep`. Compile and build are required and raise; translate and resolve-organizers are marked `required = False`, so a failed or skipped step is logged and the import continues with the untranslated or unorganized draft. `ResolveOrganizersStep` can run either from the compiled source or from the draft recipe, and skips the model call when there is neither an existing organizer to match nor permission to create new ones. Translation skips when target and source language codes match.

**Multi-source merging.** When several sources are compiled, `CompileSourceStep` merges them into one document with per-source `##` labels and a preamble stating that the sections describe the same recipe and that user-supplied content wins on conflict; the user's own pasted content is appended last. Source text is capped at 100,000 characters, with the budget split across parts and a `[content truncated]` marker appended.

**Legacy prompt paths.** The prompt-override migration maps legacy custom prompt file locations to prompt names, including `recipes/compile-source.txt` -> `system.compile-source` and `general/transcribe-audio.txt` -> `system.transcribe-audio`, reflecting an earlier directory layout. Importing a custom prompt directory is a one-time migration into per-group overrides.

## Coverage and Exclusions

- Extracted: all 7 shipped prompt templates under `mealie/services/openai/prompts/` -- `recipes/build-recipe.txt`, `recipes/parse-recipe-ingredients.txt`, `recipes/parse-recipe-video.txt`, `recipes/resolve-organizers.txt`, `recipes/translate-recipe.txt`, `system/compile-source.txt`, `system/transcribe-audio.txt`. Each is quoted verbatim with its source path and line range; no text was reordered, truncated, completed, or paraphrased.
- Template formats: all seven are plain text with no `{placeholder}` slots and no templating syntax. Parameterization happens entirely through the user message, appended data-injection sections, and per-group overrides, so no placeholder substitution was performed during extraction.
- Deliberately excluded: `mealie/services/openai/testing/debug.txt` (a test fixture outside `prompts/`, not enumerated by `get_prompt_names`), the data-injection description strings and response schema field descriptions (constructed in code, not shipped as prompt templates), and the non-AI import paths (`StructuredDataCompiler`, the NLP and brute-force ingredient parsers, the scraper's local cleaner) which use no prompt.
- Note on prompt category: `system/compile-source.txt` and `system/transcribe-audio.txt` are classified as System Prompts because they are sent in the system role from the `system` prompt category, which also exempts them from group-wide instructions; operationally they are transcription tasks that feed later prompts rather than conversational system prompts.
