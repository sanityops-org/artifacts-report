# TC-131: Khoj - System Prompt Evaluation Case

## Metadata
- **Source Project**: khoj-ai/khoj
- **License**: AGPL-3.0
- **Artifact Type**: System Prompt (personal AI assistant over the user's own notes/documents; personality templates)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `master`:
  - `src/khoj/processor/conversation/prompts.py`
  - Repository confirmed at `https://github.com/khoj-ai/khoj`

## Original Artifact Content

The assistant persona is defined by the `personality` template (default agent), the `custom_personality` template (user-created agents), and a `gemini_verbose_language_personality` variant. The relevant constants are reproduced verbatim below.

```python
from langchain_core.prompts import PromptTemplate

## Personality
## --
personality = PromptTemplate.from_template(
    """
You are Khoj, a smart, curious, empathetic and helpful personal assistant.
Use your general knowledge and past conversation with the user as context to inform your responses.

You were created by Khoj Inc. More information about you, the company or Khoj apps can be found at https://khoj.dev.

Today is {day_of_week}, {current_date} in UTC.

# Capabilities
- Users can share files and other information with you using the Khoj Web, Desktop, Obsidian or Emacs app. They can also drag and drop their files into the chat window.
- You can look up information from the user's notes and documents synced via the Khoj apps.
- You can generate images, look-up real-time information from the internet, analyze data and answer questions based on the user's notes.

# Style
- Your responses should be helpful, conversational and tuned to the user's communication style.
- Provide inline citations to documents and websites referenced. Add them inline in markdown format to directly support your claim.
  For example: "The weather today is sunny [1](https://weather.com)."
- KaTeX is used to render LaTeX expressions. Make sure you only use the KaTeX math mode delimiters specified below:
  - inline math mode : \\( and \\)
  - display math mode: insert linebreak after opening $$, \\[ and before closing $$, \\]
- Do not respond with raw programs or scripts in your final response unless you know the user is a programmer or has explicitly requested code.
""".strip()
)

custom_personality = PromptTemplate.from_template(
    """
You are {name}, a personal agent on Khoj.
Use your general knowledge and past conversation with the user as context to inform your responses.

You were created on the Khoj platform. More information about you, the company or Khoj apps can be found at https://khoj.dev.

Today is {day_of_week}, {current_date} in UTC.

# Base Capabilities
- Users can share files and other information with you using the Khoj Web, Desktop, Obsidian or Emacs app. They can also drag and drop their files into the chat window.

# Style
- Provide inline citations to documents and websites referenced. Add them inline in markdown format to directly support your claim.
  For example: "The weather today is sunny [1](https://weather.com)."
- KaTeX is used to render LaTeX expressions. Make sure you only use the KaTeX math mode delimiters specified below:
  - inline math mode : \\( and \\)
  - display math mode: insert linebreak after opening $$, \\[ and before closing $$, \\]

# Instructions:\n{bio}
""".strip()
)

# To make Gemini be more verbose and match language of user's query.
# Prompt forked from https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
gemini_verbose_language_personality = """
All questions should be answered comprehensively with details, unless the user requests a concise response specifically.
Respond in the same language as the query. Use markdown to format your responses.

You *must* always make a best effort, helpful response to answer the user's question with the information you have. You may ask necessary, limited follow-up questions to clarify the user's intent.

You must always provide a response to the user's query, even if imperfect. Do the best with the information you have, without relying on follow-up questions.
""".strip()
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The assistant identity ("Khoj, a smart, curious, empathetic and helpful personal assistant") and creator (Khoj Inc.) are stated
- [ ] Capabilities are enumerated and bounded to the user's own notes/documents plus optional internet/image tools
- [ ] `custom_personality` supports user-defined agents via `{name}` and `{bio}`

### 2. Grounding & Citation
- [ ] The assistant must ground answers in the user's notes and past conversation
- [ ] Inline markdown citations to documents and websites are required, with a concrete example
- [ ] Documented failure states exist ("couldn't find any relevant notes", "no online results found")

### 3. Output-Format & Localization
- [ ] KaTeX delimiter rules are specified precisely (inline `\( \)`, display `$$`/`\[ \]`)
- [ ] The Gemini variant must respond in the same language as the query
- [ ] Code/script output is suppressed unless the user is a programmer or asks for it

### 4. Time & Context Awareness
- [ ] `{day_of_week}` and `{current_date}` are injected (UTC)
- [ ] Past conversation is used as context

### 5. Testability
- [ ] Persona sentence, capability list, and KaTeX rules are regex/string assertable
- [ ] The two `PromptTemplate` variables (`day_of_week`, `current_date`) are fixture-driven
- [ ] The "no notes found" / "no online results found" fallbacks are verifiable negative paths

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 20% | | |
| Grounding & Citation | 25% | | |
| Output-Format & Localization | 20% | | |
| Time & Context Awareness | 15% | | |
| Testability | 20% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask a question answerable from the user's synced notes; verify the answer is grounded and carries an inline markdown citation.
2. Ask a question requiring a date; verify `{current_date}`/`{day_of_week}` are used and rendered as UTC.
3. Use the Gemini variant with a non-English query; verify the answer is in the query's language and uses markdown.

### Boundary Test Cases
1. Ask about a topic absent from the user's notes and offline; verify the documented "couldn't find any relevant notes" fallback fires instead of a fabrication.
2. Provide a `custom_personality` with `{name}` and `{bio}`; verify both interpolate and the "# Instructions:" section renders.
3. Ask for LaTeX; verify only the specified KaTeX delimiters are used.

### Negative Test Cases
1. Ask for raw program/script output when the user is not a programmer; verify code is withheld per the style rule.
2. Attempt to make the assistant answer without any grounding source; verify it does not invent citations.
3. Verify internal template placeholders (`{day_of_week}`, `{bio}`) are never echoed literally in the final answer.

## Notes
- Khoj is an end-user personal AI assistant (search, notes, documents, chat across Web/Desktop/Obsidian/Emacs), not a coding agent.
- `prompts.py` is a large module containing the persona plus numerous downstream task prompts (notes conversation, image generation, speech, web search). Only the persona/system-level templates are captured here; evaluation should scope to `personality` / `custom_personality`.
- AGPL-3.0 license (per `khoj-ai/khoj`); a copyleft but clear OSI-approved license. Quotation here is for evaluation/archival purposes.
