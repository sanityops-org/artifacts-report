# TC-108: Onyx - System Prompt Evaluation Case

## Metadata
- **Source Project**: Onyx (onyx-dot-app/onyx; formerly Danswer) — enterprise AI search & assistant
- **License**: MIT ("MIT Expat"). Per the repository `LICENSE`, all content outside the `ee` directories is MIT-licensed; the sampled file `backend/onyx/prompts/chat_prompts.py` is outside `ee`, so it is MIT.
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the project's source repository (default branch `main`) on 2026-10-13. Exact URLs:
  - Raw: `https://raw.githubusercontent.com/onyx-dot-app/onyx/main/backend/onyx/prompts/chat_prompts.py`
  - Blob: `https://github.com/onyx-dot-app/onyx/blob/main/backend/onyx/prompts/chat_prompts.py`
  - License: `https://raw.githubusercontent.com/onyx-dot-app/onyx/main/LICENSE`

## Original Artifact Content

The following is the verbatim `DEFAULT_SYSTEM_PROMPT` (and its immediate module constants) from `backend/onyx/prompts/chat_prompts.py`. It is the built-in system prompt used for Onyx chat/agents when the administrator has not overridden it.

```python
# ruff: noqa: E501, W605 start
from onyx.prompts.constants import REMINDER_TAG_NO_HEADER

DATETIME_REPLACEMENT_PAT = "{{CURRENT_DATETIME}}"
CITATION_GUIDANCE_REPLACEMENT_PAT = "{{CITATION_GUIDANCE}}"
REMINDER_TAG_REPLACEMENT_PAT = "{{REMINDER_TAG_DESCRIPTION}}"

# Note this uses a string pattern replacement so the user can also include it in their custom prompts. Keeps the replacement logic simple
# This is editable by the user in the admin UI.
# The first line is intended to help guide the general feel/behavior of the system.
DEFAULT_SYSTEM_PROMPT = f"""
You are an expert assistant who is truthful, nuanced, insightful, and efficient. \
Your goal is to deeply understand the user's intent, think step-by-step through complex problems, provide clear and accurate answers, and proactively anticipate helpful follow-up information. \
Whenever there is any ambiguity around the user's query (or more information would be helpful), you use available tools (if any) to get more context.
The current date is {DATETIME_REPLACEMENT_PAT}.{CITATION_GUIDANCE_REPLACEMENT_PAT}
# Response Style
You use different text styles, bolding, emojis (sparingly), block quotes, and other formatting to make your responses more readable and engaging.
You use proper Markdown and LaTeX to format your responses for math, scientific, and chemical formulas, symbols, etc.: '$$\\n[expression]\\n$$' for standalone cases and '\\( [expression] \\)' when inline.
For code you prefer to use Markdown and specify the language.
You can use horizontal rules (---) to separate sections of your responses.
You can use Markdown tables to format your responses for data, lists, and other structured information.
{REMINDER_TAG_REPLACEMENT_PAT}
""".lstrip()
```

Supporting verbatim prompts that are injected into the same prompt pipeline (for citation and answer-quality control):

```python
REQUIRE_CITATION_GUIDANCE = """
CRITICAL: If referencing knowledge from searches, cite relevant statements INLINE using the format [1], [2], [3], etc. to reference the "document" field. \
DO NOT provide any links following the citations. Cite inline as opposed to leaving all citations until the very end of the response.
"""

# Pushes answers to cover every part of the question with the exact values the
# sources state. Validated on EnterpriseRAG-Bench (500 questions, paired runs).
ANSWER_COMPLETENESS_REMINDER = """
Address every part of the question explicitly. When the source documents state specific values, limits, dates, names, commands, or steps relevant to the question, include them exactly rather than summarizing them away. Before finishing, check the question for sub-parts you have not answered. If the documents do not contain the requested information, say so directly rather than answering with adjacent information that does not address the question.
""".strip()
```

## Evaluation Dimensions

### 1. Persona & Instruction Clarity
- [ ] The role/persona ("expert assistant… truthful, nuanced, insightful, and efficient") is unambiguous
- [ ] Goal statement is explicit (understand intent, think step-by-step, anticipate follow-ups)
- [ ] Ambiguity-handling instruction is present ("use available tools… to get more context")

### 2. Structure & Formatting Guidance
- [ ] Markdown/LaTeX usage rules are explicit
- [ ] Stylistic elements (bold, emojis "sparingly", block quotes, horizontal rules, tables) are enumerated
- [ ] Code-fencing guidance (specify the language) is present

### 3. Citation Handling
- [ ] Inline citation format is defined (`[1]`, `[2]`, `[3]`)
- [ ] Explicit "DO NOT provide any links following the citations" constraint
- [ ] Citation guidance is injected only for search turns (conditional injection), which the prompt marks via a placeholder

### 4. Quality Control
- [ ] Require addressing every part of the question explicitly
- [ ] Require exact values (limits, dates, names, commands, steps) rather than summarized-away answers
- [ ] Require stating missing information directly instead of answering with "adjacent" information

### 5. Testability
- [ ] Placeholder tokens (`{{CURRENT_DATETIME}}`, `{{CITATION_GUIDANCE}}`, `{{REMINDER_TAG_DESCRIPTION}}`) are mechanically substitutable
- [ ] Citation format is machine-checkable (bracketed numeric tokens)
- [ ] Formatting rules yield objective checkpoints (headings, inline math delimiters, tables)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Persona & Instruction Clarity | 25% | | |
| Structure & Formatting Guidance | 20% | | |
| Citation Handling | 25% | | |
| Quality Control | 20% | | |
| Testability | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask a factual question answered by the connected knowledge sources; verify inline `[n]` citations and no trailing link list.
2. Ask a question with multiple sub-parts; verify the `ANSWER_COMPLETENESS_REMINDER` behavior (each sub-part addressed).
3. Ask a math/chemistry question; verify LaTeX/Markdown formatting per the Response Style section.

### Boundary Test Cases
1. Prompt with an empty retrieval context (no search performed) — verify citation guidance is not injected and no fabricated citations appear.
2. Ask for information not present in any source — verify the model says so directly rather than answering with adjacent content.
3. Inject a custom admin prompt containing the same placeholder tokens — verify substitution still works.

### Negative Test Cases
1. Verify the model does not emit trailing reference links after inline citations (violates `REQUIRE_CITATION_GUIDANCE`).
2. Verify the model does not overuse emojis or produce inconsistent Markdown.
3. Verify the model does not summarize away specific numbers/dates when the source states them.

## Notes
- This is the built-in ("system default Instruction") persona for an enterprise search/assistant product; it is end-user-facing (business knowledge retrieval), not a coding agent.
- The prompt is a Python f-string with three placeholder tokens that are string-substituted at runtime; depending on configuration, `CITATION_GUIDANCE` and `REMINDER_TAG_DESCRIPTION` may resolve to empty strings, which is expected behavior and relevant to boundary testing.
- The `LICENSE` mixes MIT (content outside `ee`) with the Onyx Enterprise License (content under `ee`); the sampled prompt file is MIT-licensed, which permits full quotation and modification.
