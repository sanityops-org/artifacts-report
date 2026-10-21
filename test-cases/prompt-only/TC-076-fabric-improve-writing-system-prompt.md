# TC-076: Fabric `improve_writing` Pattern - System Prompt Evaluation Case

## Metadata
- **Source Project**: danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from the raw file at https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/improve_writing/system.md (branch: `main`)

## Original Artifact Content

```text
# IDENTITY and PURPOSE

You are a writing expert. You refine the input text to enhance clarity, coherence, grammar, and style.

# Steps

- Analyze the input text for grammatical errors, stylistic inconsistencies, clarity issues, and coherence.
- Apply corrections and improvements directly to the text.
- Maintain the original meaning and intent of the user's text, ensuring that the improvements are made within the context of the input language's grammatical norms and stylistic conventions.

# OUTPUT INSTRUCTIONS

- Refined and improved text that has no grammar mistakes.
- Return in the same language as the input.
- Include NO additional commentary or explanation in the response.

# INPUT:

INPUT:
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] The role (writing expert) and the improvement targets (clarity, coherence, grammar, style) are explicit
- [ ] The three steps are ordered and actionable
- [ ] The "preserve original meaning/intent" boundary is stated

### 2. Input/Output Contract
- [ ] The input placeholder (`# INPUT:` / `INPUT:`) is clearly marked
- [ ] The output is defined as the refined text only
- [ ] The output language is pinned to the input language

### 3. Output Discipline
- [ ] "NO additional commentary or explanation" enforces a clean, drop-in replacement
- [ ] The result is expected to be grammar-correct
- [ ] No formatting meta-text leaks into the output

### 4. Reusability
- [ ] Language-agnostic by design (returns in the input's language)
- [ ] Works for emails, articles, docs, and arbitrary prose
- [ ] No domain-specific assumptions that limit reuse

### 5. Robustness
- [ ] Preserves meaning even when rewriting for style
- [ ] Behaves predictably for already-clean input (minimal change)
- [ ] Handles very short or very long inputs without truncation guidance issues

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Input/Output Contract | 20% | | |
| Output Discipline | 25% | | |
| Reusability | 20% | | |
| Robustness | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide text with grammar and clarity issues; verify corrected text with the original meaning intact.
2. Provide text in a non-English language; verify the returned text is in the same language.
3. Verify no commentary or explanation is appended.

### Boundary Test Cases
1. Already well-written text; verify changes are minimal and meaning is unchanged.
2. Ambiguous sentences where edits could alter intent; verify original intent is preserved.
3. Very long text; verify full coverage without truncation.

### Negative Test Cases
1. Whether the model adds explanations or notes (prohibited).
2. Whether it translates the text into another language (prohibited).
3. Whether it changes the meaning or adds new content.

## Notes
- Part of the `danielmiessler/fabric` prompt-pattern library, a set of reusable System Prompts for non-coding productivity tasks (writing, editing, summarizing).
- `improve_writing` is a minimal, high-reuse pattern whose compact design makes it a good baseline for evaluating instruction-following precision.
- MIT licensed; the full prompt can be quoted and reproduced.
