# TC-103: Morphic - Agent Suite Evaluation Case

## Metadata
- **Source Project**: Morphic (miurla/morphic)
- **Submodule**: `lib/agents/prompts/search-mode-prompts.ts` (mode-specific system prompts) + `lib/agents/researcher.ts` (agent) + `lib/agents/title-generator.ts`
- **License**: Apache-2.0
- **Artifact Type**: Single-Agent suite (AI answer engine: identity + source-direction guidance + Quick/Adaptive mode system prompts + tool-calling research agent)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/miurla/morphic`
  - `https://raw.githubusercontent.com/miurla/morphic/main/README.md`
  - `https://raw.githubusercontent.com/miurla/morphic/main/lib/agents/prompts/search-mode-prompts.ts`
  - `https://raw.githubusercontent.com/miurla/morphic/main/lib/agents/researcher.ts`
  - `https://api.github.com/repos/miurla/morphic/contents/lib/agents/prompts` (directory listing)
  - `https://api.github.com/repos/miurla/morphic` (repository metadata, license = Apache-2.0)

---

## Project Overview

Morphic is an **AI-powered search engine with a generative UI**. It is an end-user-facing information-query application that produces grounded, cited answers and renders rich inline UI components.

From the project README (verbatim):

> "An AI-powered search engine with a generative UI."

> - "AI-powered search with grounded, cited answers"
> - "Generative UI — answers render rich inline components (source-credited images, grids, headings) live from a streamed JSON spec, beyond plain markdown"
> - "Search modes: Quick and Adaptive"
> - "Model selector with dynamic provider detection (OpenAI, Anthropic, Google, Ollama, Vercel AI Gateway, OpenAI-compatible providers)"
> - "Multiple search providers (Tavily, SearXNG, Brave, Exa)"

> "This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details."

---

## Logical Artifact Inventory

### 1. System Prompts (`lib/agents/prompts/search-mode-prompts.ts`)

#### 1.1 Identity guidance (verbatim)

```
function getIdentityGuidance(): string {
  return `Identity:
- You are Morphic, an AI-powered answer engine.
- When asked who or what you are, identify yourself as Morphic. Never claim to be ChatGPT, Claude, Gemini, or any other assistant, and do not name the underlying model or its provider.`
}
```

#### 1.2 Source-direction guidance (verbatim)

```
Source direction (include/exclude domains):
- When the user signals a source preference, pass it to the search tool via `include_domains` / `exclude_domains`:
  - Specific site(s): "search reddit", "from x.com", "on github" → `include_domains: ["reddit.com"]`
  - Authoritative-only: "official sources", "peer-reviewed", "primary sources" → include the relevant authoritative domains (e.g. `["pubmed.ncbi.nlm.nih.gov","nature.com"]` for medical, `["worldbank.org","oecd.org"]` for economic data)
  - Avoid a source: "not pinterest", "exclude forums" → `exclude_domains: ["pinterest.com"]`
- Only apply domain filters when the user's intent clearly points to a source. Do NOT invent restrictions for ordinary queries.
- Fallback: if a domain-restricted search returns too few or no results, ...
```

#### 1.3 Quick-mode system prompt (verbatim excerpt)

```
export function getQuickModePrompt(): string {
  const hasGeneralProvider = isGeneralSearchProviderAvailable()
  return `
Instructions:
${getIdentityGuidance()}
You are a fast, efficient AI assistant optimized for quick responses. You have access to web search and content retrieval.
**EFFICIENCY GUIDELINES:**
- **Use exactly one search tool call for informational questions without URLs**
- Combine the essential concepts into one focused query; d...
```

### 2. Agent & Auxiliary Artifacts (`lib/agents/`)

- `researcher.ts` (5863 bytes) — constructs the tool-calling research agent (`createResearcher`), wiring the mode prompt into the model with `search`/`retrieve` tools.
- `title-generator.ts` (2902 bytes) — generates conversation titles.
- Imported helpers referenced by the prompts: `getImageSpecPrompt`, `getRelatedQuestionsSpecPrompt` (from `lib/render/prompt`) and `getContentTypesGuidance` (from `lib/utils/search-config`).

### 3. Tool Surface (referenced in prompts, verbatim)

- `search` tool with `include_domains` / `exclude_domains` parameters.
- `retrieve` / content retrieval for URLs.
- Render spec tools: `getImageSpecPrompt`, `getRelatedQuestionsSpecPrompt` (generative-UI JSON spec).

---

## Evaluation Dimensions

### 1. Role & Mode Clarity
- [ ] Identity is fixed ("You are Morphic") and explicitly forbids claiming to be another assistant
- [ ] Distinct Quick vs Adaptive mode prompts with different efficiency budgets
- [ ] Domain-restriction guidance is a dedicated, reusable block

### 2. Workflow Completeness
- [ ] Search → retrieve → answer → generative-UI spec pipeline
- [ ] Fallback behavior defined when a domain-restricted search under-returns
- [ ] Related-questions and image-spec generation are explicit steps

### 3. Prompt Consistency
- [ ] Shared guidance functions composed into each mode prompt (identity, source direction)
- [ ] Uniform parameter naming (`include_domains` / `exclude_domains`) across guidance and tools
- [ ] Consistent "do not invent restrictions" guardrail

### 4. Tool Modularity
- [ ] Multiple interchangeable search providers (Tavily, SearXNG, Brave, Exa)
- [ ] Provider-agnostic model selector
- [ ] `hasGeneralProvider` conditionally adjusts prompt behavior

### 5. Observability
- [ ] Grounded, cited answers
- [ ] Shareable result URLs and chat history (PostgreSQL)
- [ ] Privacy documentation (`docs/PRIVACY.md`) describing outbound calls

### 6. Extensibility
- [ ] OpenAI-compatible provider support
- [ ] Docker/Compose deployment with bundled SearXNG
- [ ] File upload support

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
1. **Cited answer**: run a factual query in Quick mode and verify one focused search call plus citations.
2. **Source direction**: query "search reddit for X" and assert `include_domains: ["reddit.com"]` is passed to the search tool.
3. **Adaptive mode**: verify deeper multi-step retrieval and richer generative-UI output.

### Unit Tests
1. **Identity**: assert the identity block is present in every mode prompt.
2. **Fallback logic**: simulate an under-returning domain-restricted search and verify the fallback branch text.
3. **Tool wiring**: assert `researcher.ts` attaches the mode prompt and the expected tools.

### Stress Tests
1. **Ambiguous queries**: ensure no spurious domain filters are invented.
2. **Provider assortment**: rotate providers and search backends without prompt drift.
3. **Generative-UI streaming**: validate streamed JSON spec renders without breaking the answer.

---

## Notes

- **License**: Apache-2.0 (verified via GitHub API `license.spdx_id = "apache-2.0"`). Verbatim quotation is permitted.
- **Scope**: AI search / answer generation is an end-user information-query scenario; no code generation.
- **Overlap**: like Vane (TC-102), Morphic is an AI search engine, but the two have distinct, independently retrieved prompt systems and tool surfaces.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
