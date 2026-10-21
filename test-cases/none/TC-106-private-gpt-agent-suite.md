# TC-106: PrivateGPT - Agent Suite Evaluation Case

## Metadata
- **Source Project**: PrivateGPT (zylon-ai/private-gpt)
- **Submodule**: `private_gpt/components/prompts/` (prompt components) + `private_gpt/components/llm/prompt_helper.py` (prompt-style/tokenizer dispatch) + built-in tool components (`code_execution/`, `database/`, `multimodality/`, `files/`) + `private_gpt/components/chat/`
- **License**: Apache-2.0
- **Artifact Type**: Single-Agent suite (private AI application layer: messages API + retrieval-with-citations + built-in tools + custom tools + MCP connectors + skills)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source / file-tree retrieval, exact URLs:
  - `https://github.com/zylon-ai/private-gpt`
  - `https://raw.githubusercontent.com/zylon-ai/private-gpt/main/README.md`
  - `https://raw.githubusercontent.com/zylon-ai/private-gpt/main/private_gpt/components/llm/prompt_helper.py`
  - `https://api.github.com/repos/zylon-ai/private-gpt/contents/private_gpt/components` (directory listing)
  - `https://api.github.com/repos/zylon-ai/private-gpt/contents/private_gpt/components/chat` (directory listing)
  - `https://data.jsdelivr.com/v1/packages/gh/zylon-ai/private-gpt@main` (file-tree listing)
  - `https://api.github.com/repos/zylon-ai/private-gpt` (repository metadata, license = Apache-2.0)

---

## Project Overview

PrivateGPT is an open-source **API layer that turns locally-run models into production AI applications**. It is an end-user-facing private assistant: it ships a workbench chat UI, document ingestion with citations, agentic RAG, and a tool/skill surface — while connecting to any OpenAI-compatible inference server.

From the project README (verbatim):

> "**PrivateGPT is the open-source API layer that turns local models into production AI applications.**"

> "PrivateGPT ships a built-in workbench UI for testing and demos, available at `/ui`. The API is the actual product."

> "## What PrivateGPT gives you
> - Standard messages API (streaming, async, token counting)
> - File and artifact ingestion
> - Retrieval with citations and agentic RAG
> - Built-in tools mirroring the Claude API (web search, web fetch, code execution)
> - Custom tools and MCP connectors
> - Structured access to databases and CSVs
> - Embeddings and orchestration"

> "PrivateGPT started as a proof of concept in 2023: a script that let you chat with your documents, fully offline, with no data leaving your machine. It went viral on GitHub, crossed 50K stars..."

---

## Logical Artifact Inventory

### 1. Tool / Skill Surface (from README, verbatim — Claude-API compatibility table)

| Area | Capability | PrivateGPT |
|---|---|---|
| Tools | Tool use | ✅ |
| Tools | Tools in streaming | ✅ |
| Tools | Built-in web search | ✅ |
| Tools | Web extraction / fetch | ✅ |
| Tools | Custom tools | ✅ |
| Data | Database querying | ✅ built-in |
| Data | CSV / tabular analysis | ✅ built-in |
| Agents | MCP in the API | ✅ |
| Agents | Remote MCP servers | ✅ |
| Agents | Skills | ⚙️ basic |

### 2. Prompt Components (`private_gpt/components/prompts/`, directory verification)

The repository ships a dedicated prompt component package (verified as a directory under `private_gpt/components/` via the GitHub contents API and the jsDelivr file tree). Prompt-style dispatch is wired through the LLM component:

```
private_gpt/components/prompts/               (prompt components)
private_gpt/components/llm/prompt_helper.py   (prompt style + tokenizer dispatch)
```

### 3. Prompt-style dispatch (`private_gpt/components/llm/prompt_helper.py`, verbatim)

```
def get_prompt_style(
    prompt_style: str,
    *args: Any,
    **kwargs: Any,
) -> PromptStyleBase:
    """Get a tokenizer formatter by name."""
    from private_gpt.components.llm.prompt_styles.registry import PromptStyleRegistry
    return PromptStyleRegistry.get_prompt_style(
        prompt_style,
        *args,
        **kwargs,
    )
```

### 4. Component Inventory (`private_gpt/components/` — directory listing, verbatim, abbreviated)

```
chat/            (models/, processors/ — request/response processing)
code_execution/  (code execution tool)
context/         database/       embedding/      engines/
files/           filesystems/    ingest/         ingestion/
llm/             (prompt_helper.py, prompt_styles/, tokenizers/)
markdown/        memory/         migrations/     model_discovery/
multimodality/   node_store/     persistence/    postgres/
postprocessor/   prompts/        ...
```

### 5. Integrations (README, verbatim)

> "PrivateGPT works natively as the local backend for the tools developers and end users already use."
> - Claude Code · Claude Desktop / Cowork · Claude for Microsoft 365 · OpenCode
> - Also: n8n, OpenClaw, Hermes Agent, VS Code, Cline

---

## Evaluation Dimensions

### 1. Role & Capability Clarity
- [ ] Assistant role and system prompt are configurable per chat
- [ ] Built-in tools (web search, web fetch, code execution) are distinctly declared
- [ ] Skills and custom tools are separated from built-in tools

### 2. Workflow Completeness
- [ ] Messages API (streaming, async, token counting) → retrieval (citations) → tool use → answer
- [ ] Agentic RAG path distinct from plain retrieval
- [ ] Request/response processors normalise model I/O

### 3. Prompt Consistency
- [ ] Prompt styles dispatched by name via `PromptStyleRegistry`
- [ ] Tokenizer/prompt-style abstraction keeps prompts model-agnostic
- [ ] Prompt components centralised under `private_gpt/components/prompts/`

### 4. Tool Modularity
- [ ] Each tool is its own component directory (code_execution, database, multimodality, files)
- [ ] Custom tools and MCP connectors pluggable
- [ ] Built-in tools mirror the Claude API surface

### 5. Observability
- [ ] API Debugger in the workbench UI (inspect requests/responses)
- [ ] Token-based auth; structured outputs
- [ ] Retrieval with citations

### 6. Extensibility
- [ ] Any OpenAI-compatible inference server (Ollama, llama.cpp, vLLM)
- [ ] MCP (local + remote) connectors
- [ ] Skills system (basic, in progress)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Capability Clarity | 15% | | |
| Workflow Completeness | 20% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 25% | | |
| Observability | 15% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Document RAG**: ingest a PDF, ask a question, and verify a cited answer via the workbench UI.
2. **Built-in tool**: ask a question requiring web search and confirm the built-in web-search tool is invoked.
3. **Custom tool / MCP**: register a custom tool (or MCP connector) and verify it is callable and surfaces in the UI.

### Unit Tests
1. **Prompt style dispatch**: `get_prompt_style(...)` returns the registered style; unknown names raise.
2. **Tool registry**: assert built-in tools are individually addressable components.
3. **Streaming tool use**: verify tools work in streaming mode.

### Stress Tests
1. **Large ingestion**: many documents through the ingestion component.
2. **Concurrent requests**: token-based auth under load.
3. **Model swap**: point `OPENAI_API_BASE` at different servers and confirm prompt-styles adapt.

---

## Notes

- **License**: Apache-2.0 (verified via GitHub API `license.spdx_id = "apache-2.0"`). Verbatim quotation is permitted.
- **Scope**: PrivateGPT is positioned as an "API layer", but it ships a full end-user workbench application (document chat, tools, skills) and is maintained by Zylon as the open-source application layer. This positioning should be weighed as a baseline; compared with pure developer frameworks, its artifact surface is the end-user assistant (tools + prompt components + skills), not a coding agent.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13.
