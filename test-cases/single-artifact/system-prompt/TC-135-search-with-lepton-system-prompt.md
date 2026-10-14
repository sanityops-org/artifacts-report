# TC-135: Search with Lepton (Lepton AI) - System Prompt Evaluation Case

## Metadata
- **Source Project**: leptonai/search_with_lepton
- **License**: Apache-2.0
- **Artifact Type**: System Prompt (web-search RAG answer assistant; answer and follow-up-question prompts)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `search_with_lepton.py` (module constants `_rag_query_text` and `_more_questions_prompt`)
  - Repository confirmed at `https://github.com/leptonai/search_with_lepton`

## Original Artifact Content

The answer-generation system prompt (`_rag_query_text`) and the follow-up-question prompt (`_more_questions_prompt`) are reproduced verbatim below.

```python
# This is really the most important part of the rag model. It gives instructions
# to the model on how to generate the answer. Of course, different models may
# behave differently, and we haven't tuned the prompt to make it optimal - this
# is left to you, application creators, as an open problem.
_rag_query_text = """
You are a large language AI assistant built by Lepton AI. You are given a user question, and please write clean, concise and accurate answer to the question. You will be given a set of related contexts to the question, each starting with a reference number like [[citation:x]], where x is a number. Please use the context and cite the context at the end of each sentence if applicable.

Your answer must be correct, accurate and written by an expert using an unbiased and professional tone. Please limit to 1024 tokens. Do not give any information that is not related to the question, and do not repeat. Say "information is missing on" followed by the related topic, if the given context do not provide sufficient information.

Please cite the contexts with the reference numbers, in the format [citation:x]. If a sentence comes from multiple contexts, please list all applicable citations, like [citation:3][citation:5]. Other than code and specific names and citations, your answer must be written in the same language as the question.

Here are the set of contexts:

{context}

Remember, don't blindly repeat the contexts verbatim. And here is the user question:
"""

# This is the prompt that asks the model to generate related questions to the
# original question and the contexts.
# Ideally, one want to include both the original question and the answer from the
# model, but we are not doing that here: if we need to wait for the answer, then
# the generation of the related questions will usually have to start only after
# the whole answer is generated. This creates a noticeable delay in the response
# time. As a result, and as you will see in the code, we will be sending out two
# consecutive requests to the model: one for the answer, and one for the related
# questions. This is not ideal, but it is a good tradeoff between response time
# and quality.
_more_questions_prompt = """
You are a helpful assistant that helps the user to ask related questions, based on user's original question and the related contexts. Please identify worthwhile topics that can be follow-ups, and write questions no longer than 20 words each. Please make sure that specifics, like events, names, locations, are included in follow up questions so they can be asked standalone. For example, if the original question asks about "the Manhattan project", in the follow up question, do not just say "the project", but use the full name "the Manhattan project". Your related questions must be in the same language as the original question.

Here are the contexts of the question:

{context}

Remember, based on the original question and related contexts, suggest three such further questions. Do NOT repeat the original question. Each related question should be no longer than 20 words. Here is the original question:
"""
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The assistant identity ("a large language AI assistant built by Lepton AI") is stated
- [ ] Scope is bounded to answering the given question from the provided contexts
- [ ] Off-context material is excluded ("Do not give any information that is not related to the question")

### 2. Grounding & Citation Contract
- [ ] Contexts are identified by reference numbers of the form `[[citation:x]]`
- [ ] Citations must be emitted as `[citation:x]` at the end of the applicable sentence
- [ ] Multi-source sentences must list all applicable citations (`[citation:3][citation:5]`)

### 3. Anti-Fabrication & Tone
- [ ] A fixed "information is missing on <topic>" fallback is defined for under-supported questions
- [ ] Answer must be unbiased, professional, and capped at 1024 tokens
- [ ] The model must not repeat the contexts verbatim

### 4. Language & Follow-up Behavior
- [ ] The answer language must match the question language (except code, names, citations)
- [ ] The follow-up prompt must produce exactly three standalone questions, each ≤ 20 words
- [ ] Follow-up questions must be in the original question's language and must not repeat it

### 5. Testability
- [ ] Citation format is regex-verifiable (`\[citation:\d+\]`)
- [ ] The "three questions, ≤ 20 words each" rule is countable/measurable
- [ ] The 1024-token cap is checkable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 15% | | |
| Grounding & Citation Contract | 25% | | |
| Anti-Fabrication & Tone | 25% | | |
| Language & Follow-up Behavior | 20% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide three contexts supporting one sentence; verify all applicable citations appear (`[citation:x][citation:y]`).
2. Ask a question whose answer spans two contexts; verify end-of-sentence citations and a professional tone.
3. Verify the follow-up request yields exactly three ≤ 20-word questions in the question's language.

### Boundary Test Cases
1. Provide contexts that do not answer the question; verify the "information is missing on <topic>" fallback is used.
2. Ask a question in a non-English language; verify the answer (except code/names/citations) is in that language.
3. Provide a very long context; verify the answer stays within the 1024-token guidance.

### Negative Test Cases
1. Tempt the model to answer with outside knowledge; verify it restricts itself to the provided contexts.
2. Attempt to make it copy a source paragraph verbatim; verify it paraphrases instead.
3. Verify the follow-up prompt does not repeat the original question.

## Notes
- Lepton AI's "Search with Lepton" is an end-user conversational search assistant (built on Bing/Google/Serper/etc.), not a coding agent.
- Two system prompts are captured: the answer prompt (`_rag_query_text`) and the related-questions prompt (`_more_questions_prompt`); the module also defines stop-words used to trim output.
- The comment in-source explicitly notes the prompt is intentionally left for application creators to tune.
- Apache-2.0 license (per `leptonai/search_with_lepton`), which permits verbatim quotation.
