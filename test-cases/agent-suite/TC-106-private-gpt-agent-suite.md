# TC-106: PrivateGPT - Chat Prompt Template Suite

## Metadata
- **Source Project**: PrivateGPT (zylon-ai/private-gpt)
- **License**: Apache-2.0
- **Artifact Type**: System prompt / prompt template suite (Jinja2 templates loaded by the chat pipeline)
- **Collection Date**: 2026-10-20
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `private_gpt/components/prompts/templates/chat/system/base.j2`
  - `private_gpt/components/prompts/templates/chat/condense/condense.j2`
  - `private_gpt/components/prompts/templates/context/context.j2`
  - `private_gpt/components/prompts/prompt_builder.py`
  - `private_gpt/components/prompts/prompt_template.py`
- **Re-scope note**: The previous version of this case quoted README tables and directory listings instead of prompt text. It has been replaced with the actual templates.

---

## Original Artifact Content

### 1. Chat system prompt (`chat/system/base.j2`, verbatim in full)

```jinja
You are {{ assistant_name }}, an AI assistant.
{% if assistant_description is defined and assistant_description != "" %}
{{ assistant_description }}
{% endif %}
{% if system_prompt is defined and system_prompt != "" %}
{{ system_prompt }}
{% endif %}
{% if current_date is defined and current_date != "" %}
Current date: {{ current_date }}.
{% endif %}
{% block guidelines_block %}
{% endblock %}
{% block context_block %}
{% endblock %}
```

### 2. Follow-up condensing prompt (`chat/condense/condense.j2`, verbatim in full)

```jinja
Your task is to rewrite follow-up questions into clear, standalone questions that can be understood without chat history context.
Given a chat history and a follow-up question, create a self-contained question that:
1. Can be understood without any chat history
2. Captures all relevant information from both history and follow-up
3. Is optimized for semantic search
4. Contains only the question itself (no explanations or additional text)
5. Stays as-is if the follow-up is unrelated to chat history
{% if max_words is defined and max_words != "0" %}
6. Uses no more than {{ max_words }} words
{% endif %}
Guidelines:
- Replace pronouns (it, they, he, she) with their actual references from chat history
- Replace comparative references ("better", "worse") with specific items being compared
- Include quoted content from chat history when referenced
- Keep the question as-is if it's already self-contained
- Output only the rewritten question - no additional text
{% if max_words is defined and max_words != "0" %}
- Stay within {{ max_words }} words
{% endif %}
{% if few_shots == "True" %}
Examples:
Chat History: User asked about best practices for React component lifecycle methods.
Follow-up: "How do I implement these in my code?"
Standalone Question: How do I implement React component lifecycle methods in my code?
Chat History: User asked about MongoDB and SQL performance.
Follow-up: "Which one is better for high traffic?"
Standalone Question: Which database is better between MongoDB and SQL for high traffic?
Chat History: User discussed React hooks and their benefits in functional components.
Follow-up: "Can these solve the problems we talked about with those?"
Standalone Question: Can React hooks solve state management problems in functional components?
Chat History: User asked about Tesla's newest car model.
Follow-up: "What is the capital of Germany?"
Standalone Question: What is the capital of Germany?
{% endif %}
{% if chat_history is defined and chat_history != "" %}
Chat History:
{{ chat_history }}
{% endif %}
Follow-up Question: {{ question }}
Standalone Question:
```

### 3. Retrieval context block (`context/context.j2`, verbatim in full)

```jinja
{% if included_in_system_prompt is defined and included_in_system_prompt %}
**Context Information**:
Below is important information to help you provide the most accurate and relevant responses.
=====================
{% endif %}
{{ context_str }}
{% if included_in_system_prompt %}
=====================
{% endif %}
```

### 4. Prompt assembly (`prompt_builder.py`, verbatim excerpt)

```python
    def create_chat_system_prompt(
        self,
        assistant_name: str | None = None,
        assistant_description: str | None = None,
        system_prompt: str | None = None,
        current_date: datetime | None = None,
    ) -> BasePromptTemplate:
        if not current_date:
            current_date = datetime.now()
        return self.template_service.create_prompt_template(
            "chat/system/base.j2",
            system_prompt=None,
            assistant_name=assistant_name or settings().chat.assistant_name,
            assistant_description=assistant_description
            or settings().chat.assistant_description,
            # ... (date and remaining kwargs elided at the excerpt boundary)
            current_date=current_date.astimezone().date().isoformat(),
        )
```

```python
    def create_chat_condense_prompt(
        self,
        question: str,
        chat_history: list[ChatMessage],
        max_words: int = 0,
        few_shots: bool = True,
    ) -> BasePromptTemplate:
        return self.template_service.create_prompt_template(
            "chat/condense/condense.j2",
            question=question,
            chat_history=chat_history,
            max_words=max_words,
```

### 5. Template loader (`prompt_template.py`, verbatim excerpt)

```python
@singleton
class PromptTemplateService:
    def __init__(self, templates_dir: Path = prompt_templates_path) -> None:
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=["jinja2.ext.do"],
        )
```

---

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Assistant identity and description are parameterized, not hardcoded
- [ ] Date is injected once and formatted unambiguously
- [ ] Optional blocks degrade cleanly when empty

### 2. Grounding and Context
- [ ] Retrieved context is delimited from instructions
- [ ] Context can be embedded in the system prompt or sent separately
- [ ] No instruction inside retrieved text can override the system prompt boundary

### 3. Condensing Behavior
- [ ] Follow-up rewriting preserves entities from history
- [ ] Unrelated questions are left unchanged
- [ ] Word limits are honored when configured

### 4. Template Extensibility
- [ ] Blocks (`guidelines_block`, `context_block`) allow overrides
- [ ] Templates are loaded by path, not concatenated in code
- [ ] New prompts follow the same `.j2` convention

### 5. Testability
- [ ] Rendered prompts can be snapshotted
- [ ] Empty and missing variables produce deterministic output
- [ ] Condensing can be evaluated with paired history/question cases

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|---|---|---|---|
| Instruction Clarity | 20% | | |
| Grounding and Context | 25% | | |
| Condensing Behavior | 20% | | |
| Template Extensibility | 20% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

1. Render `base.j2` with an empty `assistant_description` and `system_prompt`; verify no blank labeled sections remain.
2. Provide retrieved context and verify the `=====================` delimiters appear only when the context is embedded.
3. Submit a follow-up containing pronouns and verify `condense.j2` replaces them with the referenced entities.
4. Submit an unrelated follow-up and verify it is returned unchanged.
5. Set `max_words` and verify both the instruction and the output respect it.
6. Override `context_block` and verify the base template still renders.

---

## Notes

- These templates are loaded by `PromptTemplateService` from `private_gpt/components/prompts/templates`, the path resolved in `private_gpt/paths.py`.
- The previous version of this case contained no prompt text. It has been replaced with the upstream templates above.
