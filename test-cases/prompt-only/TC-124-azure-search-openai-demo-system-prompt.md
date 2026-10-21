# TC-124: Azure Search OpenAI Demo - System Prompt Evaluation Case

## Metadata
- **Source Project**: Azure-Samples/azure-search-openai-demo
- **License**: MIT
- **Artifact Type**: System Prompt (Retrieval-augmented internal-document Q&A assistant)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the raw source file `app/backend/approaches/prompts/chat_answer.system.jinja2` on the `main` branch:
  `https://raw.githubusercontent.com/Azure-Samples/azure-search-openai-demo/main/app/backend/approaches/prompts/chat_answer.system.jinja2`
  The prompt file's existence and path were confirmed from the repo git tree (GitHub API `git/trees/main?recursive=1`), and the repo is `https://github.com/Azure-Samples/azure-search-openai-demo`. Sibling templates in the same directory include `chat_answer.user.jinja2` and `query_rewrite.system.jinja2`.

## Original Artifact Content

A Jinja2 template (`.jinja2`). Conditionals are driven by the approach configuration; `override_prompt`, `image_sources`, `citations`, `injected_prompt`, and `include_follow_up_questions` are injected at runtime.

```jinja2
{% if override_prompt %}
{{ override_prompt }}
{% else %}
Assistant helps the company employees with their questions about internal documents. Be brief in your answers.
Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below.
If asking a clarifying question to the user would help, ask the question.
If the question is not in English, answer in the language used in the question.
Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, for example [info1.txt]. Don't combine sources, list each source separately, for example [info1.txt][info2.pdf].
{% if image_sources %}
Each image source has the document file name in the top left corner of the image with coordinates (10,10) pixels with format <filename.ext#page=N>,
and the image figure name is right-aligned in the top right corner of the image.
The filename of the actual image is in the top right corner of the image and is in the format <figureN_N.png>.
Each text source starts in a new line and has the file name followed by colon and the actual information
Always include the source document filename for each fact you use in the response in the format: [document_name.ext#page=N].
If you are referencing an image, add the image filename in the format: [document_name.ext#page=N(image_name.png)].
{% endif %}
Possible citations for current question: {% for citation in citations %} [{{ citation }}] {% endfor %}
{{ injected_prompt }}
{% endif %}
{% if include_follow_up_questions %}
Generate 3 very brief follow-up questions that the user would likely ask next.
Enclose the follow-up questions in double angle brackets. Example:
<<Are there exclusions for prescriptions?>>
<<Which pharmacies can be ordered from?>>
<<What is the limit for over-the-counter medication?>>
Do not repeat questions that have already been asked.
Make sure the last question ends with ">>".
{% endif %}
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Scope is fixed ("questions about internal documents"), tone constrained ("Be brief")
- [ ] Language policy defined (mirror the question's language)
- [ ] Follow-up-question format is defined with examples

### 2. Grounding & Anti-Hallucination
- [ ] "Answer ONLY with the facts listed in the list of sources" is the primary constraint
- [ ] Explicit "if there isn't enough information, say you don't know" fallback
- [ ] "Do not generate answers that don't use the sources below" forbids parametric-knowledge answers

### 3. Citation Handling
- [ ] Inline citation syntax specified with examples (`[info1.txt]`)
- [ ] "Don't combine sources" rule (one bracket per source)
- [ ] Multimodal citation format is defined (`[document.ext#page=N]`, image variant)

### 4. Configurability
- [ ] `override_prompt` allows full replacement (testable branch)
- [ ] `injected_prompt` allows additive safety language (e.g., prompt-injection defense) without editing the core
- [ ] `citations` list is materialized by the template

### 5. Testability
- [ ] Citation brackets are regex-checkable
- [ ] The `<<...>>` follow-up format is machine-parseable
- [ ] "I don't know" on empty sources is a verifiable negative case

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Grounding & Anti-Hallucination | 30% | | |
| Citation Handling | 20% | | |
| Configurability | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Query answered by one retrieved source; verify a single `[source]` citation per fact
2. Query answerable from two sources; verify sources are listed separately (`[a][b]`), not combined
3. Query with `include_follow_up_questions` on; verify exactly 3 `<<...>>` questions, none repeated

### Boundary Test Cases
1. Empty source list; verify the assistant says it does not know rather than answering from memory
2. Non-English question; verify the answer mirrors the question's language
3. Image-source mode on; verify `[document.ext#page=N]` and image filename formats appear

### Negative Test Cases
1. Query whose answer exists only in the model's parametric knowledge; verify it is not answered
2. Inject an instruction inside a source document; verify it is treated as content, not instruction (this depends on `injected_prompt`)
3. Verify follow-up questions do not duplicate earlier questions

## Notes
- This is a Microsoft **sample application** ("RAG chat app with Azure OpenAI and Azure AI Search (Python)"); sibling language ports (JavaScript, .NET, Java) exist. It is end-user-facing (an employee knowledge assistant), not a coding agent, though it is a reference/sample codebase rather than a shipped product.
- The actual system message is this template rendered by `promptmanager.py`; the retrieval logic and citation pipeline live in the surrounding `app/backend/approaches/` modules.
- A related Microsoft repo (`microsoft/sample-app-aoai-chatGPT`) carried a similar pattern but was **archived** on 2026-10-14 (Azure OpenAI "On Your Data" retirement) and is therefore excluded in favour of this one.
- MIT license; quotation from raw file only.
