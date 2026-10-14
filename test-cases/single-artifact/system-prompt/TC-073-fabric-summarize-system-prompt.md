# TC-073: Fabric `summarize` Pattern - System Prompt Evaluation Case

## Metadata
- **Source Project**: danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from the raw file at https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/summarize/system.md (branch: `main`)

## Original Artifact Content

```text
# IDENTITY and PURPOSE

You are an expert content summarizer. You take content in and output a Markdown formatted summary using the format below.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:.

- Output the 10 most important points of the content as a list with no more than 16 words per point into a section called MAIN POINTS:.

- Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:.

# OUTPUT INSTRUCTIONS

- Create the output using the formatting above.
- You only output human readable Markdown.
- Output numbered lists, not bullets.
- Do not output warnings or notes—just the requested sections.
- Do not repeat items in the output sections.
- Do not start items with the same opening words.

# INPUT:

INPUT:
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Role and purpose are stated in a single clear sentence
- [ ] The summarization goal is expressed through explicit steps
- [ ] The prompting style ("take a deep breath and think step by step") is applied consistently

### 2. Input/Output Contract
- [ ] The input placeholder (`# INPUT:` / `INPUT:`) is clearly separated
- [ ] Each output section is named with a machine-parseable label (ONE SENTENCE SUMMARY:, MAIN POINTS:, TAKEAWAYS:)
- [ ] Element counts are constrained (20 words; 10 points; 5 takeaways)

### 3. Output Format Discipline
- [ ] Numbered lists are mandated instead of bullets
- [ ] Markdown-only, human-readable output is required
- [ ] Prohibitions are explicit (no warnings/notes, no duplicate items, no repeated opening words)

### 4. Reusability
- [ ] Works with any input content type without domain assumptions
- [ ] No residual example content that would leak into output
- [ ] Fixed output schema enables downstream automation/parsing

### 5. Robustness
- [ ] The "do not repeat / do not start with same words" rules guard against degenerate summaries
- [ ] Behavior on very short input (fewer than 5 takeaways) is predictable
- [ ] The prompt avoids inventing content beyond the provided text

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Input/Output Contract | 20% | | |
| Output Format Discipline | 25% | | |
| Reusability | 20% | | |
| Robustness | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Summarize a standard article; verify ONE SENTENCE SUMMARY (≤20 words), 10 MAIN POINTS (≤16 words each), and 5 TAKEAWAYS are produced.
2. Confirm the output is valid, human-readable Markdown with numbered lists.
3. Check that the three section labels match exactly (ONE SENTENCE SUMMARY:, MAIN POINTS:, TAKEAWAYS:).

### Boundary Test Cases
1. Very short input with fewer than 5 distinct takeaways; verify graceful handling.
2. Input already containing many near-duplicate points; verify the no-repeat rules hold.
3. Non-English or mixed-language content; verify the summary stays coherent.

### Negative Test Cases
1. Empty or near-empty input; verify no invented content.
2. Whether the model adds preamble, warnings, or notes (prohibited).
3. Whether two points start with the same opening words (violation).

## Notes
- Part of the `danielmiessler/fabric` prompt-pattern library, a set of reusable System Prompts for non-coding productivity tasks (summarizing, writing, analysis).
- `summarize` is one of the most widely reused Fabric patterns and exhibits the library's signature structure: identity → output sections → output instructions → input placeholder.
- MIT licensed; the full prompt can be quoted and reproduced.
