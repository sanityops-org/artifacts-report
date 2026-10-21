# TC-137: Kotaemon - System Prompt Evaluation Case

## Metadata
- **Source Project**: Cinnamon/kotaemon
- **License**: Apache-2.0
- **Artifact Type**: System Prompt (document-Q&A assistant; citation QA prompt templates)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `libs/kotaemon/kotaemon/indices/qa/citation_qa.py` (constants `DEFAULT_QA_TEXT_PROMPT`, `DEFAULT_QA_TABLE_PROMPT`, `DEFAULT_QA_CHATBOT_PROMPT`, `DEFAULT_QA_FIGURE_PROMPT`)
  - Repository confirmed at `https://github.com/Cinnamon/kotaemon`

## Original Artifact Content

The QA system prompt templates used by `AnswerWithContextPipeline` are reproduced verbatim below (the module also defines citation-format helpers and the pipeline class, not quoted here).

```python
DEFAULT_QA_TEXT_PROMPT = (
    "Use the following pieces of context to answer the question at the end in detail with clear explanation. "  # noqa: E501
    "If you don't know the answer, just say that you don't know, don't try to "
    "make up an answer. Give answer in "
    "{lang}.\n\n"
    "{context}\n"
    "Question: {question}\n"
    "Helpful Answer:"
)
DEFAULT_QA_TABLE_PROMPT = (
    "Use the given context: texts, tables, and figures below to answer the question, "
    "then provide answer with clear explanation."
    "If you don't know the answer, just say that you don't know, "
    "don't try to make up an answer. Give answer in {lang}.\n\n"
    "Context:\n"
    "{context}\n"
    "Question: {question}\n"
    "Helpful Answer:"
)  # noqa
DEFAULT_QA_CHATBOT_PROMPT = (
    "Pick the most suitable chatbot scenarios to answer the question at the end, "
    "output the provided answer text. If you don't know the answer, "
    "just say that you don't know. Keep the answer as concise as possible. "
    "Give answer in {lang}.\n\n"
    "Context:\n"
    "{context}\n"
    "Question: {question}\n"
    "Answer:"
)  # noqa
DEFAULT_QA_FIGURE_PROMPT = (
    "Use the given context: texts, tables, and figures below to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Give answer in {lang}.\n\n"
    "Context: \n"
    "{context}\n"
    "Question: {question}\n"
    "Answer: "
)  # noqa
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The task is grounded in "the following pieces of context" (text, tables, figures) supplied at runtime
- [ ] Four evidence-mode variants exist (text, table, chatbot, figure) with the same grounding intent
- [ ] Answer style differs by mode (detailed explanation vs. concise scenario output)

### 2. Anti-Fabrication / Grounding
- [ ] Repeated instruction: "If you don't know the answer, just say that you don't know"
- [ ] Repeated instruction: "don't try to make up an answer"
- [ ] Answers must be derived from `{context}`

### 3. Output-Format Determinism
- [ ] The completion scaffold (`Question:` / `Helpful Answer:` or `Answer:`) is fixed
- [ ] `{context}` and `{question}` placeholders pin the runtime injection points
- [ ] The table/chatbot/figure modes adjust the answer style but keep the scaffold

### 4. Localization
- [ ] "Give answer in {lang}" enforces the output language per mode
- [ ] The scaffold labels remain fixed while the answer language varies

### 5. Testability
- [ ] Placeholders (`{context}`, `{question}`, `{lang}`) are checkable for correct substitution
- [ ] The "say you don't know" behavior is a verifiable negative path
- [ ] Mode selection maps deterministically to the evidence type

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 20% | | |
| Anti-Fabrication / Grounding | 30% | | |
| Output-Format Determinism | 20% | | |
| Localization | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide text context that answers the question; verify a detailed "Helpful Answer" grounded in the context.
2. Provide a table/figure context; verify the table/figure variant is selected and the answer references the evidence.
3. Set `{lang}` to a non-English value; verify the answer is produced in that language.

### Boundary Test Cases
1. Provide context that does not contain the answer; verify the model says it does not know rather than fabricating.
2. Test the chatbot variant; verify the answer stays concise and picks a suitable scenario.
3. Provide an empty context; verify no invented content is produced.

### Negative Test Cases
1. Attempt to make the model answer from general knowledge outside `{context}`; verify it declines.
2. Verify the `{context}` / `{question}` placeholders are never echoed literally.
3. Verify the model does not add a bibliography or extra sections beyond the scaffold.

## Notes
- Kotaemon is an open-source, end-user RAG/document-Q&A application (with a tool/agent layer), not a coding agent; this case captures its core QA prompt templates.
- The pipeline selects one of the four templates based on evidence mode; evaluation should freeze the evidence mode for stable regression runs.
- The module also includes citation-formatting logic (`citation.py`, `citation_qa_inline.py`) that post-processes answers; the QA prompts themselves are the logical artifact captured here.
- Apache-2.0 license (per `Cinnamon/kotaemon`), which permits verbatim quotation.
