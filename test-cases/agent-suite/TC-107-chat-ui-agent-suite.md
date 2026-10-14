# TC-107: Chat UI (HuggingChat) - Agent Suite Evaluation Case

## Metadata
- **Source Project**: Chat UI (huggingface/chat-ui) — powers the HuggingChat app
- **Submodule**: `src/lib/buildPrompt.ts` (prompt assembly) + `src/lib/server/` (MCP tool integration, Omni LLM router, request processing) + environment-defined MCP tool schemas
- **License**: Apache-2.0
- **Artifact Type**: Single-Agent suite (AI chat assistant: prompt/preprompt assembly + MCP tool schemas + server-side LLM router policy + ML Intern mode)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source / file-tree retrieval, exact URLs:
  - `https://github.com/huggingface/chat-ui`
  - `https://raw.githubusercontent.com/huggingface/chat-ui/main/README.md`
  - `https://cdn.jsdelivr.net/gh/huggingface/chat-ui@main/src/lib/buildPrompt.ts`
  - `https://api.github.com/repos/huggingface/chat-ui/contents/src/lib/server` (directory listing)
  - `https://data.jsdelivr.com/v1/packages/gh/huggingface/chat-ui@main?structure=flat` (file-tree listing)
  - `https://api.github.com/repos/huggingface/chat-ui` (repository metadata, license = Apache-2.0)

---

## Project Overview

Chat UI is the open-source chat application that powers **HuggingChat**. It is an end-user-facing conversational assistant with MCP tool-calling, a server-side model router, and an experimental "ML Intern" task mode. It speaks to any OpenAI-compatible API.

From the project README (verbatim):

> "A chat interface for LLMs. It is a SvelteKit app and it powers the [HuggingChat app on hf.co/chat](https://huggingface.co/chat)."

> "Chat UI can call tools exposed by Model Context Protocol (MCP) servers and feed results back to the model using OpenAI function calling. You can preconfigure trusted servers via env, let users add their own, and optionally have the Omni router auto-select a tools-capable model."

> "**ML Intern** is an experimental mode that plans and runs machine-learning work on the Hugging Face Hub: reproducing papers, finetuning and evaluating models, building datasets, and deploying demos as Spaces. It reads papers, models and datasets, writes scripts, and runs them as [Hugging Face Jobs]..."

---

## Logical Artifact Inventory

### 1. Prompt Assembly (`src/lib/buildPrompt.ts`, verbatim)

```
import type { EndpointParameters } from "./server/endpoints/endpoints";
import type { BackendModel } from "./server/models";
import { toLegacyShape } from "./utils/messageShape";

type buildPromptOptions = Pick<EndpointParameters, "messages" | "preprompt"> & {
	model: BackendModel;
};

export async function buildPrompt({
	messages,
	model,
	preprompt,
}: buildPromptOptions): Promise<string> {
	const filteredMessages = messages.map(toLegacyShape);
	if (filteredMessages[0].from === "system" && preprompt) {
		filteredMessages[0].content = preprompt;
	}
	const prompt = model
		.chatPromptRender({
			messages: filteredMessages.map((m) => ({
				...m,
				role: m.from,
			})),
			preprompt,
		})
		// Not super precise, but it's truncated in the model's backend anyway
		.split(" ")
		.slice(-(model.parameters?.truncate ?? 0))
		.join(" ");
	return prompt;
}
```

### 2. MCP Tool Schemas (`MCP_SERVERS` env, from README verbatim)

```env
# JSON array of servers: name, url, optional headers
MCP_SERVERS=[
  {"name": "Web Search (Exa)", "url": "https://mcp.exa.ai/mcp"},
  {"name": "Hugging Face MCP Login", "url": "https://hf.co/mcp?login"}
]
# Forward the signed-in user's Hugging Face token to the official HF MCP login endpoint
# when no Authorization header is set on that server entry.
MCP_FORWARD_HF_USER_TOKEN=true
```

README (verbatim) on tool use:
> "Use tools in the UI: Open "MCP Servers" from the top-right menu or from the `+` menu in the chat input to add servers, toggle them on, and run Health Check. The server card lists available tools."
> "When a model calls a tool, the message shows a compact "tool" block with parameters, a progress bar while running, and the result (or error). Results are also provided back to the model for follow-up."

### 3. Server-side LLM Router policy (README, verbatim)

> "The UI exposes a virtual model alias called "Omni" (configurable) that, when selected, chooses the best route/model for each message: image inputs go to a `multimodal` route, MCP-tool-enabled requests go to an `agentic` route, and everything else goes to a `default` route."

> "Provide a routes policy JSON via `LLM_ROUTER_ROUTES_PATH`. ... Each route entry needs `name`, `description`, `primary_model`, and optional `fallback_models`. The router recognizes the route names `default`, `multimodal`, and `agentic`."

> "Multimodal: If `LLM_ROUTER_ENABLE_MULTIMODAL=true` and the user sends an image, the router bypasses the policy file and uses the model specified in `LLM_ROUTER_MULTIMODAL_MODEL`. Route name: `multimodal`."
> "Tools: If `LLM_ROUTER_ENABLE_TOOLS=true` and the user has at least one MCP server enabled, the router bypasses the policy file and uses `LLM_ROUTER_TOOLS_MODEL`. ... Route name: `agentic`."

### 4. Server Modules (`src/lib/server/` — directory listing, verbatim paths)

```
src/lib/server/askUserQuestion.ts       src/lib/server/config.ts
src/lib/server/api/                     src/lib/server/conversation.ts
src/lib/server/abortRegistry.ts         src/lib/server/abortedGenerations.ts
src/lib/server/adminToken.ts            src/lib/server/apiToken.ts
src/lib/server/auth.ts                  src/lib/server/billing*.ts
...
```

### 5. ML Intern Mode (README coverage, verbatim)

> "ML Intern is an experimental mode that plans and runs machine-learning work on the Hugging Face Hub... within a compute budget you set for each conversation."
> Local setup: `docs/source/ml-intern/getting-started.md`, `docs/source/ml-intern/local-development.md`.

---

## Evaluation Dimensions

### 1. Role & Capability Clarity
- [ ] System prompt ("preprompt") assembly is explicit and model-aware
- [ ] Tool-calling, multimodal, and default capabilities are distinguished as routes
- [ ] ML Intern is a clearly separated experimental mode

### 2. Workflow Completeness
- [ ] Message → prompt render (with truncation) → model → tool loop → answer
- [ ] MCP server health-check, enable/disable, and per-call result surfacing
- [ ] Router fallback chain (`fallback_models` → `LLM_ROUTER_FALLBACK_MODEL`)

### 3. Prompt Consistency
- [ ] Single prompt-assembly path for all models (`chatPromptRender`)
- [ ] Preprompt overrides the system message uniformly
- [ ] Per-model overrides (tool calling, multimodal) applied consistently

### 4. Tool Modularity
- [ ] Tools sourced from arbitrary MCP servers (preconfigured or user-added)
- [ ] Tools surfaced via OpenAI function calling
- [ ] Routed to a dedicated tools-capable model (`agentic` route)

### 5. Observability
- [ ] RouterMetadata emitted immediately (route + actual model used)
- [ ] Tool block shows parameters, progress and result/error
- [ ] Health Check per MCP server

### 6. Extensibility
- [ ] OpenAI-compatible backends only (llama.cpp, Ollama, OpenRouter, Poe, …)
- [ ] Users can add their own MCP servers
- [ ] MongoDB-backed history/users/settings

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
1. **MCP tool call**: enable an MCP server, ask a question requiring it, and verify the tool block renders with parameters and result.
2. **Omni routing**: select Omni with an image attached and confirm routing to the `multimodal` route/model.
3. **Preprompt override**: set a custom preprompt and verify it replaces the system message.

### Unit Tests
1. **buildPrompt**: assert the system message is replaced by `preprompt` and truncation is applied.
2. **Router policy**: given signals (image / MCP enabled / default), assert the selected route name.
3. **Fallback chain**: simulate a primary-model failure and verify fallback selection order.

### Stress Tests
1. **Many MCP servers**: enable several servers and confirm tool selection stays correct.
2. **Long conversations**: verify prompt truncation keeps requests within model limits.
3. **ML Intern budget**: confirm compute-budget enforcement halts runaway Jobs.

---

## Notes

- **License**: Apache-2.0 (verified via GitHub API `license.spdx_id = "apache-2.0"`). Verbatim quotation is permitted.
- **Scope**: chatting, MCP tool use and ML Intern are end-user assistant scenarios. ML Intern's "reproducing papers / finetuning models" is one optional mode; the core product is a general chat assistant, not a coding agent.
- **Collection note**: `PROMPTS.md` appeared in the jsDelivr file tree but was not retrievable via the raw/CDN endpoints at collection time; it is therefore not quoted. The verbatim prompt artifact used here is `src/lib/buildPrompt.ts`.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long README sections are excerpted.
