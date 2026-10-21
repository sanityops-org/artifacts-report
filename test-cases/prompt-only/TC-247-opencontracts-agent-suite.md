# TC-247: OpenContracts - Legal Contract Analysis Agent Suite

## Metadata

- Source Project: JSv4/OpenContracts
- GitHub: https://github.com/JSv4/OpenContracts
- Commit SHA: 8bc8254d0c03efcf3cdb7b383a675016fcb51351
- License: MIT
- Artifact Type: Business-embedded logical artifacts (prompt components)
- Business Scenario: Legal contract review and corpus analysis
- Collection Date: 2026-10-21
- Collection Method: Shallow clone at the pinned commit; verbatim extraction from product code paths. No rewriting or completion; runtime placeholders preserved as-is.
- Unit of Analysis: Prompt component (verbatim)

## Project Overview

OpenContracts is a self-hosted, MIT-licensed document-intelligence platform that turns a repository of documents into a programmable citation graph. Users create a corpus, upload documents, and the installed "intelligence bundle" has agents describe and summarize every document while statutory citations are detected, resolved, and drawn as edges. Annotation is a first-class data model: extracted text is located through character-level `TextSpan` offsets rather than free-form prose, so highlights, redactions, and citation anchors survive back to the source PDF. The platform exposes the same graph through three surfaces: a GraphQL + REST API, a Model Context Protocol (MCP) server, and a React UI. LLM work is split between Anthropic Claude analyzer tasks (`@doc_analyzer_task`), pydantic-ai agents created through a single factory chokepoint (`make_pydantic_ai_agent`), and corpus-scoped agents that may call tools to write descriptions, summaries, notes, and CAML articles. Corpus actions can be automated by agent configurations whose system instructions and task instructions are seeded from templates or supplied per action.

## Business Loop

1. **Ingest** - a user uploads contracts or filings into a corpus; PDF text and PAWLS layout data are extracted and stored per document.
2. **Analyze** - document analyzers run over the extracted text. The agentic highlighter turns a reviewer's free-text `instructions` into precise highlight spans; the PII highlighter returns offending snippets that become `TextSpan` annotations labelled `REDACTED`.
3. **Anchor** - model output is mapped back to character offsets (`start`/`end`) either through Anthropic's citation API or, as a fallback, exact substring search over the source text.
4. **Cite** - a sliding-window LLM extractor emits candidate citations with `raw_text`, character offsets, `jurisdiction`, `authority_type`, `normalized_citation`, and `confidence`; hallucinated candidates whose text is not present in the chunk are dropped.
5. **Resolve authority text** - for citations the library does not yet hold, an approval-gated provider searches the web and fetches only allowlisted public-domain government sources, refusing to fabricate text when no official source is confirmed.
6. **Automate corpus actions** - per-corpus actions (add-document, new-message triggers) run an agent with a generated system prompt, the action's `task_instructions`, and a tool allowlist; the agent loads document text and writes descriptions, summaries, notes, or thread replies.
7. **Publish collection intelligence** - a CAML Article Writer action and a corpus-branding service produce `Readme.CAML` articles that narrate the collection; a memory curator distills reusable patterns from past conversations into a corpus memory document for future agents.

Concrete entities: document, corpus, contract clause, annotation / `TextSpan`, annotation label (`REDACTED`), citation, jurisdiction, authority type, authority pack, corpus action, agent configuration, thread / message, CAML article (`Readme.CAML`), corpus memory document, deadline-free but obligation-bearing provisions (e.g. indemnification, risk allocations) surfaced through extraction.

## Logical Artifact Inventory

### 1. Agentic Contract Highlighter System Directive

- **Source:** `opencontractserver/tasks/doc_analysis_tasks.py`
- **Line Range:** L369-L377 (inside `agentic_highlighter_claude`, decorated at L232; instructions read at L297)
- **Type:** System Prompt
- **Composability:** Runtime-parameterized
- **Parameterization:** `instructions` - the user's natural-language highlighting goal, taken from `kwargs.get("instructions", "No instructions provided.")` and interpolated inside double quotes. It is a Python f-string element (L371): the literal braces/quotes of the f-string are preserved below. Chunk text is not interpolated into this string; it is supplied separately as a `document` content block with citations enabled (L385-L394).
- **Business Entities:** contract, document chunk, instruction, relevant excerpt, citation, `TextSpan`

```text
    system_directive = (
        "You are a contract interpretation expert. "
        f'You have received the following user instructions:\n\n"{instructions}"\n\n'
        "Your goal: Identify relevant text from the contract. Review the full document text if possible, "
        "or use the largest available chunks of text to find relevant excerpts.\n\n"
        "Use citations so we can locate the relevant text within each chunk. "
        "If you cannot find any relevant excerpts, respond with empty text. "
        "No extra commentary. Return only the relevant text, or nothing."
    )
```

### 2. PII / Confidential-Data Highlighter Prompt

- **Source:** `opencontractserver/tasks/doc_analysis_tasks.py`
- **Line Range:** L599-L612 (inside `pii_highlighter_claude`, defined at L524-L525)
- **Type:** Template (sent as the sole user-role message)
- **Composability:** Runtime-parameterized
- **Parameterization:** `pdf_text_extract` - the full document text, interpolated between `=====` fences. It is a Python f-string element (L611); the braces shown below are the literal f-string placeholders. The prompt is passed as `messages[0].content` with `max_tokens=8192` (L621-L630); the model comes from `ANALYZER_KWARGS["opencontractserver.tasks.doc_analysis_tasks.pii_highlighter_claude"]["ANTHROPIC_MODEL"]` or `CLAUDE_ANALYZER_DEFAULT_MODEL`.
- **Business Entities:** contract, confidential data, party name, transaction detail, offending snippet, `REDACTED` annotation label

```text
    prompt_text = (
        "You are an expert at interpreting contracts and, more importantly, inferring "
        "confidential data from the text of the document. We are going to give you a "
        "contract related to a document and want you to carefully review "
        "the document, thinking step-by-step whether any given section of text could reveal "
        "confidential details of the transaction or the names of the parties, or could do "
        "so in combination with other text. For all such text, return the offending text "
        "EXACTLY as it appears in the source text, with a few preceding works and a few trailing words,"
        " each snippet on its own line. Add nothing "
        "to the text — no formatting changes, punctuation, capitalization changes, commas, "
        "quotes, or additional commentary. Don't explain your work. Don't add commentary. "
        "No chatter. If you see no relevant material, simply return empty string.\n\n"
        f"Now, here's the document text:\n=====\n{pdf_text_extract}\n====="
    )
```

### 3. Legal Citation Extraction Instructions

- **Source:** `opencontractserver/enrichment/llm_citation_extractor.py`
- **Line Range:** L270-L289
- **Type:** System Prompt (pydantic-ai `instructions=`)
- **Composability:** Standalone
- **Parameterization:** None - a module-level constant with no interpolation. The chunk text is supplied at runtime as the agent's run input (`agent.run(chunk_text)`, L323) and structural output is enforced by `output_type=ChunkCitationExtraction` (L319).
- **Business Entities:** law, statute, regulation, case law, constitution, treaty, administrative rule, municipal ordinance, jurisdiction, authority type, normalized citation, confidence

```text
_INSTRUCTIONS = """\
You are a legal citation extraction engine. Your job is to identify every
explicit citation to a law, statute, regulation, case, constitution, treaty,
administrative rule, or municipal ordinance within the supplied text.

For each citation found:
- raw_text: copy the citation VERBATIM from the text — do not paraphrase.
- start/end: character offsets within this chunk (0-indexed, end is exclusive).
- jurisdiction: the governing jurisdiction (e.g. "Delaware", "Federal",
  "California"). Use "Federal" for US federal law.
- authority_type: one of "statute", "regulation", "case_law", "constitution",
  "ordinance", "administrative", "guidance", "treaty".
- normalized_citation: canonical form if recognisable (e.g. "dgcl:145" for
  DGCL Section 145, "securities-act:5" for Securities Act Section 5); leave ""
  if unsure.
- confidence: 0.0-1.0 self-rated confidence that this is a real citation.

Return ONLY citations you are confident about. Do NOT invent text that is not
in the provided excerpt.
"""
```

### 4. Document Corpus Action Agent System Prompt

- **Source:** `opencontractserver/tasks/agent_tasks.py`
- **Line Range:** L617-L678 (function `_build_document_action_system_prompt`, defined at L580)
- **Type:** System Prompt
- **Composability:** Runtime-parameterized
- **Parameterization:** Python f-string expressions throughout: `UNTRUSTED_CONTENT_NOTICE`, `action.name`, `fence_user_content(doc_title, ...)`, `document.id`, `fence_user_content(corpus_title, ...)`, `trigger_desc` (from `TRIGGER_DESCRIPTIONS`), `tool_list`, optional `fence_user_content(desc, ...)` truncated to `MAX_DESCRIPTION_PREVIEW_LENGTH`, `action.task_instructions`, and optional `action.agent_config.system_instructions`. Sections are joined with `"\n"` at L678. The optional "Additional Agent Guidance" block (L668-L676) is only appended when an agent config with system instructions exists.
- **Business Entities:** corpus action, document, corpus, trigger (add document / metadata change), agent tool, document description, document summary, note, task instructions

```text
    parts = [
        "You are an automated corpus action agent. You execute tasks on documents "
        "without human interaction.",
        f"\n{UNTRUSTED_CONTENT_NOTICE}",
        "",
        "## Execution Context",
        f'- Action: "{action.name}"',
        f"- Document: {fence_user_content(doc_title, label='document title')} (ID: {document.id})",
        f"- Corpus: {fence_user_content(corpus_title, label='corpus title')}",
        f"- Trigger: Document {trigger_desc} the corpus",
        f"- Available tools: {tool_list}",
    ]

    # Inject current document metadata so the agent doesn't waste tool calls
    if document.description:
        desc = document.description[:MAX_DESCRIPTION_PREVIEW_LENGTH]
        if len(document.description) > MAX_DESCRIPTION_PREVIEW_LENGTH:
            desc += "..."
        parts.append(
            f"- Current description: {fence_user_content(desc, label='document description')}"
        )

    parts.extend(
        [
            "",
            "## Rules",
            "1. You MUST use tools to accomplish your task. Describing what you "
            "would do is NOT sufficient — call the tools.",
            "2. Do NOT ask clarifying questions. Execute the task as described.",
            "3. Ground all answers and outputs in actual document content "
            "loaded via tools. NEVER guess or fabricate document content.",
            "4. When the task requires writing or updating something, use the "
            "appropriate tool (e.g., update_document_description, "
            "update_document_summary, add_document_note).",
            "5. After completing your task, respond with a brief summary of "
            "actions taken.",
            "",
            "## Guidelines",
            "- Start by loading the document text so you have real content "
            "to work with. Use chunked reads for large documents.",
            "- Be responsive to what the task instructions ask for — whether "
            "that is summarization, analysis, annotation, classification, "
            "or any other document operation.",
            "- Use only the tools available to you. If the task requires a "
            "capability you lack, say so rather than improvising.",
            "",
            "## Task Instructions",
            action.task_instructions,
        ]
    )

    # Append supplementary guidance from agent config if present
    if action.agent_config and action.agent_config.system_instructions:
        parts.extend(
            [
                "",
                "## Additional Agent Guidance",
                action.agent_config.system_instructions,
            ]
        )

    return "\n".join(parts)
```

### 5. Thread Corpus Action Agent System Prompt

- **Source:** `opencontractserver/tasks/agent_tasks.py`
- **Line Range:** L716-L800 (function `_build_thread_action_system_prompt`, defined at L681)
- **Type:** System Prompt
- **Composability:** Runtime-parameterized
- **Parameterization:** f-string expressions for `UNTRUSTED_CONTENT_NOTICE`, `thread_context` fields (`id`, fenced `title`, fenced `creator_username`, `message_count`, `is_locked`, `is_pinned`), optional fenced `corpus_title`, `tool_list`, optional triggering `message_id` / fenced author / fenced body, and up to five recent messages (`recent_messages[:5]`) whose bodies are truncated to `MAX_MESSAGE_PREVIEW_LENGTH`. Also interpolates `action.task_instructions` and optional `action.agent_config.system_instructions`; the parts are joined with `"\n"` at L800.
- **Business Entities:** discussion thread, message, author/username, corpus, lock/pin state, moderation action, automated reply, trigger (new message)

```text
    parts = [
        "You are an automated corpus action agent. You execute moderation and "
        "response tasks on discussion threads without human interaction.",
        f"\n{UNTRUSTED_CONTENT_NOTICE}",
        "",
        "## Thread Context",
        f"- Thread ID: {thread_context.get('id', 'unknown')}",
        f"- Title: {fence_user_content(thread_context.get('title', 'untitled'), label='thread title')}",
        f"- Creator: {fence_user_content(thread_context.get('creator_username', 'unknown'), label='username')}",
        f"- Message count: {thread_context.get('message_count', 0)}",
        f"- Is locked: {thread_context.get('is_locked', False)}",
        f"- Is pinned: {thread_context.get('is_pinned', False)}",
    ]

    if thread_context.get("corpus_title"):
        parts.append(
            f"- Corpus: {fence_user_content(thread_context['corpus_title'], label='corpus title')}"
        )

    parts.append(f"- Available tools: {tool_list}")

    # Inject triggering message for NEW_MESSAGE triggers
    if message_id and message_content:
        raw_content = message_content.get("content", "")
        warn_if_content_large(raw_content, context="triggering message")
        parts.extend(
            [
                "",
                f"## Triggering Message (ID: {message_id})",
                f"- Author: {fence_user_content(message_content.get('creator_username', 'unknown'), label='username')}",
                f"- Content:\n{fence_user_content(raw_content, label='message body')}",
            ]
        )

    # Inject recent thread messages for context
    if recent_messages:
        from opencontractserver.constants.corpus_actions import (
            MAX_MESSAGE_PREVIEW_LENGTH,
        )

        parts.append("")
        parts.append("## Recent Thread Messages (most recent first)")
        for msg in recent_messages[:5]:
            warn_if_content_large(msg["content"], context="recent message")
            content_preview = (
                msg["content"][:MAX_MESSAGE_PREVIEW_LENGTH] + "..."
                if len(msg["content"]) > MAX_MESSAGE_PREVIEW_LENGTH
                else msg["content"]
            )
            parts.append(
                f"- [{fence_user_content(msg['creator_username'], label='username')}] (ID: {msg['id']}): "
                f"{fence_user_content(content_preview, label='message')}"
            )

    parts.extend(
        [
            "",
            "## Rules",
            "1. You MUST use tools to accomplish your task. Describing what you "
            "would do is NOT sufficient — call the tools.",
            "2. Do NOT ask clarifying questions. Execute the task as described.",
            "3. Ground your actions in the actual thread content provided above. "
            "Do not fabricate messages or user identities.",
            "4. Be responsive to the task instructions — whether that is "
            "moderation, summarization, automated replies, or other thread "
            "operations.",
            "5. After completing your task, respond with a brief summary of "
            "actions taken.",
            "",
            "## Task Instructions",
            action.task_instructions,
        ]
    )

    # Append supplementary guidance from agent config if present
    if action.agent_config and action.agent_config.system_instructions:
        parts.extend(
            [
                "",
                "## Additional Agent Guidance",
                action.agent_config.system_instructions,
            ]
        )

    return "\n".join(parts)
```

### 6. Memory Curator System Prompt

- **Source:** `opencontractserver/agents/memory.py`
- **Line Range:** L370-L384
- **Type:** System Prompt
- **Composability:** Runtime-parameterized
- **Parameterization:** A `str.format` template with one named field, `{max_insights}`, filled from `MEMORY_MAX_INSIGHTS_PER_CURATION` (default `5`) by `build_curation_prompt` (L407-L427). Not an f-string. Backslash-newline continuations inside the literal are source-level line joins: the produced text has no newline at those points.
- **Business Entities:** corpus memory document, conversation, generalizable insight, collection pattern, query pattern, refinement

```text
_CURATION_SYSTEM_PROMPT = """\
You are a memory curator for a document analysis system. Your job is to review \
a completed conversation between a user and an AI agent about a document corpus, \
and extract GENERALIZABLE insights that would help future interactions.

RULES:
1. Extract PATTERNS, not specifics. Say "Users often ask about X" NOT "User John asked about X".
2. NEVER include personal information, specific user queries, or conversation details.
3. Focus on: document structure patterns, effective search strategies, common topics, \
domain-specific knowledge discovered during the conversation.
4. DEDUPLICATE: if an insight is already in the existing memory, skip it or refine it.
5. Be concise: each insight should be 1-2 sentences with a bold title prefix.
6. Maximum {max_insights} new insights per curation run.

Format each insight as: - **Title**: Description"""
```

### 7. CAML Writer Mission

- **Source:** `opencontractserver/corpuses/caml_authoring.py`
- **Line Range:** L298-L304
- **Type:** Sub-prompt (persona framing for an include-composed system prompt)
- **Composability:** Include-only
- **Parameterization:** None - a constant. It carries no placeholders and is never used alone: `CAML_ARTICLE_SYSTEM_INSTRUCTIONS = _CAML_WRITER_MISSION + CAML_AUTHORING_GUIDE` (L309) concatenates it directly with the shared CAML syntax/editorial guide. Not an f-string. Backslash-newline continuations are source-level line joins.
- **Business Entities:** document collection, CAML (Corpus Article Markup Language), CAML article, corpus home page

```text
_CAML_WRITER_MISSION = """\
You are an expert editorial writer and CAML (Corpus Article Markup Language) \
designer. Your mission is to research a document collection thoroughly and \
produce a compelling, beautifully formatted CAML article that tells the \
story of the collection in the most engaging way possible.

"""
```

### 8. Authority-Text Locator Instructions

- **Source:** `opencontractserver/pipeline/authority_source_providers/agentic_web_locator_provider.py`
- **Line Range:** L196-L207 (inside `AgenticWebLocatorProvider._run_agent`, defined at L121)
- **Type:** System Prompt (pydantic-ai `instructions=`)
- **Composability:** Runtime-parameterized
- **Parameterization:** f-string with `{citation}` and `{jurisdiction_clause}`. Both inputs are passed through `sanitize_for_prompt_strict` (L153-L154) before interpolation; `jurisdiction_clause` is either `""` or `" (jurisdiction: <value>)"` (L195). The run message is separately built as `f"Locate the official text of: {citation}"` (L220).
- **Business Entities:** legal citation, jurisdiction, official public-domain source, statute/regulation text, authority pack, `found` flag

```text
        instructions = (
            "You are an authority-text locator. Your job is to find the OFFICIAL, "
            "public-domain full text of a single legal citation: "
            f"{citation}{jurisdiction_clause}. "
            "Steps: (1) Use web_search to find candidate official .gov sources for "
            "this citation. (2) Use fetch_allowlisted_url to retrieve the text from "
            "the most promising official URL. "
            "RULES: ONLY return text from a public-domain government source "
            "(e.g. uscode.house.gov, ecfr.gov, federalregister.gov). "
            "If you cannot confirm an official source with the actual text, set "
            "found=false. Do NOT fabricate text or invent sources."
        )
```

### 9. Default Seeded Agent System Instructions

- **Source:** `opencontractserver/corpuses/template_seeds.py`
- **Line Range:** L313-L317 (inside `create_default_action_templates`, defined at L287)
- **Type:** Template (default value persisted onto seeded `AgentConfiguration` rows)
- **Composability:** Standalone
- **Parameterization:** None. It is the fallback used for every entry in `TEMPLATES` that does not declare its own `system_instructions` (`tmpl_def.get("system_instructions", default_system_instructions)`, L332-L334); the "CAML Article Writer" template overrides it with `CAML_ARTICLE_SYSTEM_INSTRUCTIONS` (L245).
- **Business Entities:** agent configuration, corpus action template, task instructions, tool allowlist, seeded superuser owner

```text
    default_system_instructions = (
        "You are an automated document processing agent. "
        "Execute the task described in your instructions precisely. "
        "Use only the tools provided. Do not ask questions."
    )
```

### 10. Corpus Branding System Prompt

- **Source:** `opencontractserver/corpuses/services/branding.py`
- **Line Range:** L381-L423 (inside `_build_branding_system_prompt`, defined at L353; joined and returned at L424)
- **Type:** System Prompt
- **Composability:** Runtime-parameterized
- **Parameterization:** f-string expressions for `UNTRUSTED_CONTENT_NOTICE`, `fence_user_content(title, ...)`, optional fenced `description`, and `tool_list`; the whole `CAML_AUTHORING_GUIDE` is interpolated by reference (L416), not as a field; title/description are fenced because they are user-generated. `parts` is joined with `"\n"` at L424 and passed as `system_prompt=` to `agents.for_corpus(...)` from `_generate_readme` (L129-L141).
- **Business Entities:** corpus, `Readme.CAML` article, corpus title, corpus description, web search result, `update_corpus_description` tool, corpus logo (separate image path)

```text
    parts = [
        "You are an automated corpus-branding agent. You write the "
        "``Readme.CAML`` article for a newly created document collection, "
        "without human interaction, following the CAML authoring guide below.",
        f"\n{UNTRUSTED_CONTENT_NOTICE}",
        "",
        "## Collection",
        f"- Title: {fence_user_content(title, label='corpus title')}",
    ]
    if description:
        parts.append(
            "- Description: "
            f"{fence_user_content(description, label='corpus description')}"
        )
    parts.append(f"- Available tools: {tool_list}")

    parts.extend(
        [
            "",
            "## Branding rules (override the guide where they conflict)",
            "1. You MUST use tools. Research the collection's subject with "
            "web_search, then call update_corpus_description with the raw CAML "
            "as ``new_content`` to SAVE the article. Merely printing it is NOT "
            "sufficient — the guide's 'output ONLY the raw CAML' rule refers to "
            "what you pass to that tool.",
            "2. You have NO document-analysis tools (only web_search + "
            "update_corpus_description). Wherever the guide says to use "
            "ask_document / load_document_text, substitute your web_search "
            "findings and the collection metadata above.",
            "3. Ground every claim in the title/description above and what you "
            "verify via web_search. Never fabricate documents, statistics, or "
            "quotes — the collection may be empty so far, so favour a concise "
            "article over invented data blocks (pills/maps/timelines).",
            "4. Do NOT ask clarifying questions. Execute the task.",
            "",
            CAML_AUTHORING_GUIDE,
            "",
            "## Task",
            "Produce and SAVE (via update_corpus_description) a CAML article "
            "that helps a new reader quickly understand what this collection is "
            "about.",
        ]
    )
```

## Composition Notes

- **Anthropic analyzer path (artifacts 1, 2).** Both functions in `opencontractserver/tasks/doc_analysis_tasks.py` are registered with `@doc_analyzer_task`, so the platform supplies `pdf_text_extract` and analyzer `kwargs`. Artifact 1 is passed as the `system=` argument of `client.messages.create`, while the chunk itself travels as a `{"type": "document", ... "citations": {"enabled": True}}` block plus the fixed user text `"Please extract the relevant text as specified."`. The document is pre-split into `MAX_CHARS_PER_CHUNK = 80000` character chunks. Artifact 2 is a single user message with the document inlined between `=====` fences. Model selection for both is resolved from `settings.ANALYZER_KWARGS[...]["ANTHROPIC_MODEL"]` with `CLAUDE_ANALYZER_DEFAULT_MODEL` as fallback; `temperature` is deliberately omitted.
- **Citation extractor path (artifact 3).** `_one_shot_structured` calls `make_pydantic_ai_agent(model, instructions=_INSTRUCTIONS, output_type=ChunkCitationExtraction, output_retries=C.LLM_STRUCTURED_RETRIES, model_settings={"temperature": 0})` and runs it on one chunk. `LLMCitationExtractor` slides a window (`C.LLM_CHUNK_WINDOW = 8000`) with `C.LLM_CHUNK_OVERLAP = 400`, bounds concurrency, and post-validates every candidate by exact substring lookup in the chunk before converting it to absolute offsets.
- **Corpus action path (artifacts 4, 5).** `_run_agent_corpus_action_async` resolves tools with `_resolve_action_tools(action, action.trigger)`, calls `_build_document_action_system_prompt(action, document, tools)` (L884), and hands the result to the agent as its system prompt; the thread runner calls `_build_thread_action_system_prompt(...)` at L1128. In both prompts, `action.task_instructions` is appended verbatim under `## Task Instructions`, and `agent_config.system_instructions` is appended as `## Additional Agent Guidance` when present - this is the per-install/per-action override seam. Untrusted user text (titles, descriptions, message bodies, usernames) is wrapped through `fence_user_content(...)` under a shared `UNTRUSTED_CONTENT_NOTICE`.
- **Memory curation path (artifact 6).** `build_curation_prompt(current_memory, conversation_text, max_insights)` formats the system prompt with `max_insights=MEMORY_MAX_INSIGHTS_PER_CURATION` and a separate user template containing the existing memory and the conversation summary, then returns the `(system, user)` pair. `opencontractserver/tasks/memory_tasks.py` (L234-L245) passes the system text as `instructions=` to `make_pydantic_ai_agent` and the user text to `agent.run`, expecting a JSON object with `collection_patterns`, `query_patterns`, and `refinements`.
- **CAML composition (artifacts 7, 10).** `_CAML_WRITER_MISSION` is a persona-only fragment that must be concatenated with `CAML_AUTHORING_GUIDE` (L27-L296 of the same module) to form `CAML_ARTICLE_SYSTEM_INSTRUCTIONS`; the seeded "CAML Article Writer" template stores that combined value as its agent system instructions (`template_seeds.py` L245), and the `agents` migration `0016_update_caml_article_writer_prompt.py` re-syncs existing rows to it. The branding service imports only the guide and layers its own framing plus higher-priority "Branding rules" on top, deliberately overriding guide steps that reference document tools the branding agent does not have.
- **Authority locator path (artifact 8).** Instructions are rebuilt per citation inside `_run_agent`, paired with `output_type=_LocatorOutput`, two LLM-facing tools (`web_search`, `fetch_allowlisted_url`), and `UsageLimits(request_limit=self.max_agent_requests)` (class default 10). Model choice follows the canonical chain: per-corpus `preferred_llm` -> live `PipelineSettings.default_llm` -> deployment defaults.
- **Seed path (artifact 9).** `create_default_action_templates` iterates `TEMPLATES`, creating one `AgentConfiguration` per template with the default system instructions unless the template declares its own, then a `CorpusActionTemplate` holding `task_instructions`, `pre_authorized_tools`, and the trigger. The same default text therefore reaches the model only indirectly, as the agent configuration's persisted `system_instructions`.
- **Shared sanitization.** `opencontractserver/utils/prompt_sanitization.py` supplies `UNTRUSTED_CONTENT_NOTICE`, `fence_user_content`, `warn_if_content_large`, `sanitize_for_prompt_strict`, and `sanitize_plaintext_for_prompt`; these are the only mechanisms by which user data enters the prompts above, apart from `action.task_instructions`, which is treated as trusted operator input.

## Coverage and Exclusions

**Extracted.** Ten verbatim prompt components covering the end-to-end legal-review loop: contract highlighting, PII/confidential-data redaction, citation extraction, document-level corpus automation, thread-level corpus automation, memory curation, CAML article authorship, authority-text location, default seeded agent instructions, and corpus branding. Every artifact is quoted from product code with its source path and exact line range; f-string and `str.format` placeholders are preserved character-for-character.

**Deliberately skipped.**
- `CAML_AUTHORING_GUIDE` (`caml_authoring.py` L27-L296, roughly 270 lines) - an include-only syntax and editorial reference, not a persona or task prompt; quoted only by reference inside artifacts 7 and 10 to avoid duplicating a large block that neither prompt owns.
- `_CURATION_USER_PROMPT` (`memory.py` L386-L404) - the user-role companion template; the task's unit list specifies the curator system prompt, and the user template is a data-carrying JSON instruction sheet rather than a system directive.
- `MEMORY_SUMMARISE_SYSTEM_PROMPT` / `MEMORY_SUMMARISE_USER_PROMPT` and the memory injection prefix - auxiliary memory plumbing outside the requested inventory.
- `pii_scanner_privacy_filter` and the privacy-filter prompt in `doc_analysis_tasks.py` - a separate opt-in privacy pipeline not in the requested list.
- `_build_logo_prompt` (`branding.py` L452-L496) - a text-to-image prompt, not a text-LLM prompt component.
- The `TEMPLATES` task-instruction bodies in `template_seeds.py` (e.g. the CAML Article Writer research/writing phase instructions) - task instructions rather than agent system prompts; they enter the model only through `action.task_instructions` at runtime.
- Unit tests (`opencontractserver/tests/`), migrations except where they document prompt re-sync, fixtures, `docs/`, and generated GraphQL schema files - excluded per scope rules.
