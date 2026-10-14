# TC-105: Open Notebook - Agent Suite Evaluation Case

## Metadata
- **Source Project**: Open Notebook (lfnovo/open-notebook)
- **Submodule**: `prompts/` (Jinja prompt library: `ask/`, `chat/`, `pattern/`, `podcast/`, `source_chat/`, `transformation/`) + `open_notebook/graphs/` (LangGraph agents) + `open_notebook/podcasts/`
- **License**: MIT
- **Artifact Type**: Single-Agent suite (research/notebook assistant: chat system prompt + source-chat + podcast outline/transcript prompts + transformation prompts + LangGraph agents)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/lfnovo/open-notebook`
  - `https://raw.githubusercontent.com/lfnovo/open-notebook/main/README.md`
  - `https://raw.githubusercontent.com/lfnovo/open-notebook/main/prompts/chat/system.jinja`
  - `https://raw.githubusercontent.com/lfnovo/open-notebook/main/prompts/podcast/outline.jinja`
  - `https://raw.githubusercontent.com/lfnovo/open-notebook/main/open_notebook/graphs/chat.py`
  - `https://github.com/lfnovo/open-notebook/tree/main/prompts` (directory listing)
  - `https://api.github.com/repos/lfnovo/open-notebook` (repository metadata, license = MIT)

---

## Project Overview

Open Notebook is a self-hosted, privacy-focused **alternative to Google NotebookLM**. It is an end-user-facing research and knowledge-work application: it ingests multi-modal sources, answers questions with citations, and generates multi-speaker podcasts.

From the project README (verbatim):

> "An open source, privacy-focused alternative to Google's Notebook LM!"

> - "📚 **Organize multi-modal content** - PDFs, videos, audio, web pages, and more"
> - "🎙️ **Generate professional podcasts** - Advanced multi-speaker podcast generation"
> - "🔍 **Search intelligently** - Full-text and vector search across all your content"
> - "💬 **Chat with context** - AI conversations powered by your research"

> "## A private, multi-model, 100% local, full-featured alternative to Notebook LM"

---

## Logical Artifact Inventory

### 1. Chat System Prompt (`prompts/chat/system.jinja`, verbatim)

```
# SYSTEM ROLE
You are a cognitive study assistant that helps users research and learn by engaging in focused discussions about documents in their workspace. You have access to project context and can analyze documents in detail using specialized tools.
# CAPABILITIES
- Access to project information and selected documents (CONTEXT)
- Can engage in natural dialogue while maintaining academic rigor
# YOUR OPERATING METHOD
Whenever a user asks you a question, you need to identify the query context and the user intent. ...
{% if notebook %}
# PROJECT INFORMATION
**Name:** {{notebook.name}}
**Description:** {{notebook.description}}
{% endif %}
{% if context %}
# CONTEXT
The user has selected this context to help you with your response:
{{context}}
{% endif %}
# MATH FORMATTING
When showing math, write display math as $$...$$ and inline math as $...$ so formulas render properly. ...
# CITING INSTRUCTIONS
If your answer is based off of any item in the context, it's very important that your response contains references to the searched documents...
## IMPORTANT
- Do not make up documents or document ids. Only use the ids of the documents that you have access through the query you made.
- The ID is composed of the type of document and a random string, such as "source:randomstring", "note:randomstring", or "insight:randomstring". ...
```

### 2. Podcast Outline Prompt (`prompts/podcast/outline.jinja`, verbatim excerpt)

```
You are an AI assistant specialized in creating podcast outlines. Your task is to create a detailed outline for a podcast episode based on a provided briefing. The outline you will create will be used to generate the podcast transcript.
Here is the briefing for the podcast episode:
<briefing>
{{ briefing }}
</briefing>
...
The podcast will feature the following speakers:
<speakers>
{% for speaker in speakers %}
- **{{ speaker.name }}**: {{ speaker.backstory }}
  Personality: {{ speaker.personality }}
{% endfor %}
</speakers>
{% if language %}
IMPORTANT LANGUAGE INSTRUCTION: You MUST generate ALL content in {{ language }}. ...
{% endif %}
...
Return exactly one JSON object with a single root key "segments" whose value is a list of exactly {{ num_segments }} entries. Each entry has exactly three keys: "name" and "description" (strings) and "size".
...
   - Never emit placeholder or elided content: no "..." or "…", no "[like this]", no "<like this>", no "TODO", no empty strings, no trailing commas.
```

### 3. Prompt Library Structure (`prompts/` — directory listing, verbatim)

```
prompts/
  ask/
  chat/
  pattern/
  podcast/
  source_chat/
  transformation/
```

Each group maps to a distinct agent capability: `chat` (document chat), `source_chat` (single-source chat), `podcast` (outline + transcript + TTS), `transformation` (summarize/extract), `pattern` and `ask` (structured ask/query patterns).

### 4. Agent Graphs (`open_notebook/graphs/chat.py`, verbatim excerpt)

```
def call_model_with_messages(state: ThreadState, config: RunnableConfig) -> dict:
    try:
        system_prompt = Prompter(prompt_template="chat/system").render(data=state)
        payload = [SystemMessage(content=system_prompt)] + state.get("messages", [])
        model_id = config.get("configurable", {}).get("model_id") or state.get("model_override")
        ...
        ai_message = model.invoke(payload)
        content = extract_text_content(ai_message.content)
        cleaned_content = clean_thinking_content(content)
        if not cleaned_content.strip():
            raise IncompleteGenerationError(
                "The model returned an empty response. Try again, or pick a different model if this keeps happening."
            )
```

The graph binds the `chat/system` template (via the `ai_prompter` `Prompter`), a configurable `model_id`, `IncompleteGenerationError` guard, and thinking-content cleaning.

### 5. Podcast Episode Profiles (`open_notebook/podcasts/models.py`, verbatim excerpt)

```
class EpisodeProfile(ObjectModel):
    """
    Episode Profile - Simplified podcast configuration.
    Replaces complex 15+ field configuration with user-friendly profiles.
    """
    table_name: ClassVar[str] = "episode_profile"
```

---

## Evaluation Dimensions

### 1. Role & Capability Clarity
- [ ] Chat, source-chat, podcast, transformation, ask/pattern capabilities are split into separate prompt groups
- [ ] Chat system prompt declares role ("cognitive study assistant") and capabilities
- [ ] Podcast outline prompt declares the specialised role ("AI assistant specialized in creating podcast outlines")

### 2. Workflow Completeness
- [ ] Chat LangGraph node → model invocation → content cleaning → error guard
- [ ] Podcast pipeline: briefing → outline → transcript → TTS (multi-speaker)
- [ ] Content transformations as discrete actions

### 3. Prompt Consistency
- [ ] Jinja templating with consistent variable names (`{{context}}`, `{{ language }}`, `{{ speakers }}`)
- [ ] Consistent strict-output rules (no placeholders, no elided content, exact JSON contract)
- [ ] Universal citation-integrity rule (never invent document IDs)

### 4. Tool / Component Modularity
- [ ] Prompt library separated from code (`prompts/` vs `open_notebook/`)
- [ ] Model provisioning abstracted (`provision_langchain_model`, multi-provider)
- [ ] Episode profiles decouple podcast configuration from logic

### 5. Observability
- [ ] Answers cite source/note/insight IDs
- [ ] `IncompleteGenerationError` surfaces empty model responses to the user
- [ ] Error classification (`classify_error`) maps failures to user messages

### 6. Extensibility
- [ ] 20+ AI providers (OpenAI, Anthropic, Google, Mistral, Ollama, LM Studio, …)
- [ ] Full REST API and MCP integration
- [ ] New prompt templates drop into the `prompts/` tree

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Capability Clarity | 15% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 20% | | |
| Tool / Component Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Grounded chat**: add a source, ask a question, and verify the answer cites the correct document ID.
2. **Podcast generation**: configure 1–4 speakers and generate an outline + transcript, verifying segment counts match `num_segments`.
3. **Multi-language**: set `language` and confirm all generated content is in that language while JSON keys stay English.

### Unit Tests
1. **Template rendering**: render `chat/system` with/without `notebook` and `context` and assert conditional blocks.
2. **Citation rule**: attempt to reference a fabricated document ID and verify the prompt's constraint.
3. **Error guard**: force an empty model response and assert `IncompleteGenerationError`.

### Stress Tests
1. **Large context**: many sources ingested, verify context control limits what is shared.
2. **Provider swap**: change provider/model and confirm prompt behavior is unchanged.
3. **Long podcast**: 4 speakers × many segments without truncation or placeholder leakage.

---

## Notes

- **License**: MIT (verified via GitHub API `license.spdx_id = "MIT"`). Verbatim quotation is permitted.
- **Scope**: research, note-taking and podcasting are end-user knowledge-work scenarios; no code generation.
- **Naming**: "Open Notebook" (README) / repository `lfnovo/open-notebook`; not to be confused with the unrelated `openagent`/`openmanus` cases.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long prompts are excerpted.
