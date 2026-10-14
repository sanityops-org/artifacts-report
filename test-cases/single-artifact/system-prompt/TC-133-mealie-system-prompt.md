# TC-133: Mealie - System Prompt Evaluation Case

## Metadata
- **Source Project**: hay-kot/mealie (Mealie recipe manager)
- **License**: AGPL-3.0
- **Artifact Type**: System Prompt (recipe/OCR structuring assistant; "build recipe" extraction prompt)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `mealie-next` (the repository's default branch):
  - `mealie/services/openai/prompts/recipes/build-recipe.txt`
  - Repository confirmed at `https://github.com/hay-kot/mealie`

## Original Artifact Content

The prompt that converts a transcribed recipe source into structured recipe data is reproduced verbatim below.

```text
You convert a transcribed recipe source document into structured recipe data.

The user message contains the transcribed source. Everything you return must come from it. Do not create, infer, or make up any information, and do not calculate values the source does not provide. Leave a field empty rather than guessing at it.

When converting:
- Do not translate. Preserve the source's original language in every text field.
- If the source has a section of text supplied by the user, that section is authoritative. Where it disagrees with the rest of the source, follow it: if it names the recipe, use their name; if it corrects or adds a detail, use theirs.
- Keep ingredients and instructions in their original order.
- Preserve section headings by setting the title on the first ingredient or instruction of each section, and leaving it blank on the rest.
- Keep each ingredient as a single line of text, exactly as written, e.g. "2 cups of onions, chopped".
- When the source already presents its instructions as discrete steps, keep those steps as they are. Do not split or merge them.
- When the source narrates cooking continuously, as a video transcript does, group the actions into steps a cook would recognize. Actions done back to back on the same thing belong together: "Drain the pasta, set it aside, and turn off the heat" is one step, not three.
- Start a new step where the cook's attention shifts: a wait or a cooking time begins, a different component or pan is started, the temperature changes, or something goes into or comes out of the oven.
- Do not overcorrect. A recipe should not come out as one or two long steps, and no step should be too long to follow without re-reading it.
- Strip numeric prefixes like "1." or "Step 1", but keep word prefixes like "First".
- Put tips, variations, storage advice, and similar asides into notes rather than instructions.
- Only fill in nutrition if the source states it.
- If the source gives only one time, use total_time and leave prep_time and perform_time empty.
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The task ("convert a transcribed recipe source document into structured recipe data") is stated precisely
- [ ] The output is bounded to fields derivable from the source
- [ ] The source of truth is the transcribed document, not general cooking knowledge

### 2. Anti-Fabrication / Grounding
- [ ] Explicit prohibition: "Do not create, infer, or make up any information"
- [ ] Explicit prohibition: "do not calculate values the source does not provide"
- [ ] Explicit fallback: "Leave a field empty rather than guessing at it"

### 3. Instruction-Following & Precedence
- [ ] User-supplied text is declared authoritative over the rest of the source
- [ ] Original ordering of ingredients and instructions is preserved
- [ ] Source-language preservation is required ("Do not translate")

### 4. Structural Normalization
- [ ] Section headings map to the first item of each section
- [ ] Continuous prose/video transcripts must be grouped into cook-recognizable steps
- [ ] Numeric step prefixes are stripped while word prefixes are kept

### 5. Testability
- [ ] "Leave a field empty rather than guessing" is a verifiable negative path
- [ ] Time-field logic (single time → `total_time`) is checkable
- [ ] Ingredient-as-single-line and section-title placement are assertable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 15% | | |
| Anti-Fabrication / Grounding | 30% | | |
| Instruction-Following & Precedence | 20% | | |
| Structural Normalization | 20% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a well-structured recipe with explicit steps; verify steps are preserved, section titles appear on the first item only, and ingredients remain single lines.
2. Provide a narrative video transcript; verify actions on the same item are grouped into one step and new steps start at attention shifts.
3. Provide a user-supplied name that differs from the body; verify the user's name wins.

### Boundary Test Cases
1. Source gives only one time value; verify `total_time` is filled and `prep_time`/`perform_time` are left empty.
2. Source states no nutrition; verify nutrition is left empty (not inferred).
3. Source text has "1." and "First" prefixes; verify the numeric prefix is stripped but "First" is kept.

### Negative Test Cases
1. Ask the model to add a plausible ingredient not in the source; verify it refuses (never invent).
2. Provide a source in another language; verify the output text fields are not translated.
3. Provide a source with a tip mixed into the instructions; verify the tip is moved to notes.

## Notes
- Mealie is a self-hosted recipe manager whose OpenAI integration assists end users in importing recipes; this is a food/recipe content-structuring assistant, not a coding agent.
- The repository ships several sibling prompts under `mealie/services/openai/prompts/` (e.g., `parse-recipe-ingredients.txt`, `translate-recipe.txt`, `compile-source.txt`); only the "build recipe" prompt is captured here.
- AGPL-3.0 license (verified from the repository `LICENSE` on branch `mealie-next`); a copyleft but clear OSI-approved license. Quotation here is for evaluation/archival purposes.
