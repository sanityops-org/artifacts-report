# TC-102: Vane (formerly Perplexica) - Agent Suite Evaluation Case

## Metadata
- **Source Project**: Vane (ItzCrazyKns/Vane) — previously named Perplexica
- **Submodule**: `src/lib/prompts/search/` (search prompts: `researcher.ts`, `writer.ts`, `classifier.ts`) + `src/lib/prompts/suggestions/` + `src/lib/prompts/media/`
- **License**: MIT
- **Artifact Type**: Single-Agent suite (AI answering engine: research-orchestrator prompts × search modes + writer prompt + classifier prompt + tool surface)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/ItzCrazyKns/Vane`
  - `https://raw.githubusercontent.com/ItzCrazyKns/Vane/master/README.md`
  - `https://raw.githubusercontent.com/ItzCrazyKns/Vane/master/src/lib/prompts/search/researcher.ts`
  - `https://raw.githubusercontent.com/ItzCrazyKns/Vane/master/src/lib/prompts/search/writer.ts`
  - `https://raw.githubusercontent.com/ItzCrazyKns/Vane/master/src/lib/prompts/search/classifier.ts`
  - `https://api.github.com/repos/ItzCrazyKns/Vane/contents/src/lib/prompts/search` (directory listing)
  - `https://api.github.com/repos/ItzCrazyKns/Vane` (repository metadata, license = MIT)

---

## Project Overview

Vane is a **privacy-focused AI answering engine** (an end-user search/research assistant) that runs on the user's own hardware with local or cloud LLMs and returns cited answers. It is a web application with selectable search modes and sources.

From the project README (verbatim):

> "Vane is a **privacy-focused AI answering engine** that runs entirely on your own hardware. It combines knowledge from the vast internet with support for **local LLMs** (Ollama) and cloud providers (OpenAI, Claude, Groq), delivering accurate answers with **cited sources** while keeping your searches completely private."

> "⚡ **Smart search modes** - Choose Speed Mode when you need quick answers, Balanced Mode for everyday searches, or Quality Mode for deep research."

> "🧭 **Pick your sources** - Search the web, discussions, or academic papers. More sources and integrations are in progress."

> "🧩 **Widgets** - Helpful UI cards that show up when relevant, like weather, calculations, stock prices, and other quick lookups."

---

## Logical Artifact Inventory

### 1. Search Prompts (`src/lib/prompts/search/`)

#### 1.1 `researcher.ts` — Speed-mode orchestrator prompt (verbatim excerpt)

```
Assistant is an action orchestrator. Your job is to fulfill user requests by selecting and executing the available tools—no free-form replies.
...
When you are finished, you must call the `done` tool. Never output text directly.
<goal>
Fulfill the user's request as quickly as possible using the available tools.
...
<core_principle>
Your knowledge is outdated; if you have web search, use it to ground answers even for seemingly basic facts.
</core_principle>
<examples>
## Example 1: Unknown Subject
User: "What is Kimi K2?"
Action: web_search ["Kimi K2", "Kimi K2 AI"] then done.
...
<mistakes_to_avoid>
1. **Over-assuming**: Don't assume things exist or don't exist - just look them up
2. **Verification obsession**: Don't waste tool calls "verifying existence" - just search for the thing directly
3. **Endless loops**: If 2-3 tool calls don't fi...
```

#### 1.2 `researcher.ts` — Quality-mode orchestrator prompt (verbatim excerpt)

```
Assistant is a deep-research orchestrator. Your job is to fulfill user requests with the most thorough, comprehensive research possible—no free-form replies.
...
<core_principle>
Your knowledge is outdated; always use the available tools to ground answers.
This is DEEP RESEARCH mode—be exhaustive. Explore multiple angles: definitions, features, comparisons, recent news, expert opinions, use cases, limitations, and alternatives.
You can call up to 10 tools total per turn. Use an iterative loop: __reasoning_preamble → tool call(s) → ... → done.
</core_principle>
<response_protocol>
- NEVER output normal text to the user. ONLY call tools.
- Start with __reasoning_preamble and call __reasoning_preamble before every tool call (including done)...
- Default to web_search when information is missing or stale; keep queries targeted (max 3 per call).
- Do not invent tools. Do not return JSON.
</response_protocol>
```

#### 1.3 `writer.ts` (4853 bytes) — final-answer composition prompt
- Referenced in the same directory; composes the cited prose answer from gathered evidence.

#### 1.4 `classifier.ts` (6012 bytes) — query/source classification prompt
- Referenced in the same directory; classifies the query and selects source/widget behavior.

### 2. Sibling Prompt Groups (directory listing, verbatim paths)

- `src/lib/prompts/suggestions/` — search-suggestion prompts ("Smart suggestions ... as you type").
- `src/lib/prompts/media/` — image/video search prompts ("Image and video search").

### 3. Tool Surface (from orchestrator prompts + README, verbatim tokens)

Referenced tools in the researcher prompts (verbatim): `web_search`, `__reasoning_preamble`, `done`, plus an uploaded-files search tool:

```
<user_uploaded_files>
The user has uploaded the following files which may be relevant to their request:
${fileDesc}
You can use the uploaded files search tool to look for information within these documents if needed.
</user_uploaded_files>
```

---

## Evaluation Dimensions

### 1. Role & Mode Clarity
- [ ] Distinct supervisor prompts per search mode (Speed / Balanced / Quality)
- [ ] Answer-writing is separated from research orchestration (`researcher.ts` vs `writer.ts`)
- [ ] Query classification is isolated (`classifier.ts`)

### 2. Workflow Completeness
- [ ] Reason-act loop enforced via mandatory `__reasoning_preamble` before each tool call
- [ ] Explicit termination contract (`done` tool required; no free-form replies)
- [ ] Iteration/tool budget declared per mode (Speed ~6 calls, Quality ~10 calls)

### 3. Prompt Consistency
- [ ] Consistent XML sectioning (`<goal/>`, `<core_principle/>`, `<examples/>`, `<mistakes_to_avoid/>`, `<response_protocol/>`)
- [ ] Uniform "ground answers, don't rely on stale knowledge" principle across modes
- [ ] Shared anti-loop guidance ("If 2-3 tool calls don't find something... move on")

### 4. Tool Modularity
- [ ] Tools injected dynamically via `${actionDesc}` placeholder
- [ ] Guardrail: "Do not invent tools. Do not return JSON."
- [ ] File-search tool scoped to user uploads

### 5. Observability
- [ ] "Today's date" and "iteration i of maxIteration" injected for traceability
- [ ] Cited sources required in final answers
- [ ] Local search history persisted

### 6. Extensibility
- [ ] Multi-provider (Ollama, OpenAI, Anthropic, Gemini, Groq)
- [ ] Multiple search backends (SearxNG now; Tavily/Exa planned); custom widgets/sources on roadmap

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Mode Clarity | 20% | | |
| Workflow Completeness | 20% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 15% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Cited answer**: run a factual query in each mode and verify `web_search` is called and citations accompany the answer.
2. **Mode divergence**: compare Speed vs Quality on the same query to confirm different iteration budgets and depth.
3. **File grounding**: upload a PDF and confirm the uploaded-files search tool is used.

### Unit Tests
1. **Preamble enforcement**: omit `__reasoning_preamble` and verify the tool call is rejected/ignored per the prompt contract.
2. **Termination**: verify the agent always ends with `done` and never emits free-form text.
3. **Classification**: assert `classifier.ts` routes queries to the expected source set.

### Stress Tests
1. **No-result queries**: confirm the "move on after 2-3 calls" rule prevents loops.
2. **Prompt injection via web content**: verify the orchestrator does not abandon its tool-only contract.
3. **Provider failover**: switch providers and confirm prompt behavior is unchanged.

---

## Notes

- **License**: MIT (verified via GitHub API `license.spdx_id = "MIT"`). Verbatim quotation is permitted.
- **Naming**: the repository was renamed from **Perplexica** to **Vane** (source repo `ItzCrazyKns/Vane`); topics still include `perplexica`.
- **Scope**: web search / answer generation is an end-user information-query scenario; no code generation.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
