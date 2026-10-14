# TC-074: Fabric `extract_wisdom` Pattern - System Prompt Evaluation Case

## Metadata
- **Source Project**: danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from the raw file at https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/extract_wisdom/system.md (branch: `main`)

## Original Artifact Content

```text
# IDENTITY and PURPOSE

You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

# STEPS

- Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.

- Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.

- Extract 10 to 20 of the best insights from the input and from a combination of the raw input and the IDEAS above into a section called INSIGHTS. These INSIGHTS should be fewer, more refined, more insightful, and more abstracted versions of the best ideas in the content. 

- Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input. Include the name of the speaker of the quote at the end.

- Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the content into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things they always do, things they always avoid, productivity tips, diet, exercise, etc.

- Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.

- Extract all mentions of writing, art, tools, projects and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speaker mentioned.

- Extract the most potent takeaway and recommendation into a section called ONE-SENTENCE TAKEAWAY. This should be a 15-word sentence that captures the most important essence of the content.

- Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.

# OUTPUT INSTRUCTIONS

- Only output Markdown.

- Write the IDEAS bullets as exactly 16 words.

- Write the RECOMMENDATIONS bullets as exactly 16 words.

- Write the HABITS bullets as exactly 16 words.

- Write the FACTS bullets as exactly 16 words.

- Write the INSIGHTS bullets as exactly 16 words.

- Extract at least 25 IDEAS from the content.

- Extract at least 10 INSIGHTS from the content.

- Extract at least 20 items for the other output sections.

- Do not give warnings or notes; only output the requested sections.

- You use bulleted lists for output, not numbered lists.

- Do not repeat ideas, insights, quotes, habits, facts, or references.

- Do not start items with the same opening words.

- Ensure you follow ALL these instructions when creating your output.

# INPUT

INPUT:
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] The identity defines the extraction target (surprising/insightful/interesting information)
- [ ] The topical interest domain is scoped (meaning of life, technology, learning, etc.)
- [ ] Each STEPS bullet maps to exactly one named output section

### 2. Input/Output Contract
- [ ] The input placeholder (`# INPUT` / `INPUT:`) is clearly marked
- [ ] All output sections are named (SUMMARY, IDEAS, INSIGHTS, QUOTES, HABITS, FACTS, REFERENCES, ONE-SENTENCE TAKEAWAY, RECOMMENDATIONS)
- [ ] Per-section quantity constraints are specified (word counts and item ranges)

### 3. Output Format Discipline
- [ ] Bulleted lists are required (not numbered)
- [ ] Markdown-only output is mandated
- [ ] Anti-repetition rules are stated (no repeats, no shared opening words)

### 4. Reusability
- [ ] Applicable to podcasts, articles, talks, and transcripts of any length
- [ ] Example categories (sleep, diet, exercise) are illustrative rather than prescriptive
- [ ] Fixed schema supports downstream aggregation

### 5. Robustness & Constraint Satisfaction
- [ ] "Exactly 16 words" rules are testable and unambiguous
- [ ] Minimum-extraction floors (≥25 IDEAS, ≥10 INSIGHTS) are enforced
- [ ] Fallback guidance exists when fewer items are available ("collect all of them")

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Input/Output Contract | 20% | | |
| Output Format Discipline | 20% | | |
| Reusability | 15% | | |
| Robustness & Constraint Satisfaction | 25% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Feed a long interview transcript; verify all nine sections are produced.
2. Check that IDEAS/INSIGHTS/HABITS/FACTS/RECOMMENDATIONS bullets are each exactly 16 words.
3. Verify QUOTES preserve exact source text and attribute the speaker.

### Boundary Test Cases
1. A short clip with very few ideas; verify the "collect all of them" fallback triggers instead of outputting <20 items.
2. Content with no facts or habits; verify empty sections are handled without fabrication.
3. Very long content where the ≥25 IDEAS floor is hard to meet; verify behavior.

### Negative Test Cases
1. Whether numbered lists are used instead of bullets (prohibited).
2. Whether duplicate insights appear across IDEAS and INSIGHTS (prohibited).
3. Whether any bullets violate the exact 16-word constraint.

## Notes
- Part of the `danielmiessler/fabric` prompt-pattern library, a set of reusable System Prompts for non-coding productivity tasks (extracting, summarizing, analyzing).
- `extract_wisdom` is a flagship Fabric pattern that introduced the original "wisdom extraction" concept for transcripts and long-form content.
- MIT licensed; the full prompt can be quoted and reproduced.
