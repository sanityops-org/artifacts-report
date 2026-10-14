# TC-109: AnythingLLM - System Prompt Evaluation Case

## Metadata
- **Source Project**: AnythingLLM (Mintplex-Labs/anything-llm) — private, on-device/self-hosted document chat assistant
- **License**: MIT (`The MIT License`, Copyright (c) Mintplex Labs Inc.)
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the project's source repository (default branch `master`) on 2026-10-13. Exact URLs:
  - Raw (prompt): `https://raw.githubusercontent.com/Mintplex-Labs/anything-llm/master/server/models/systemSettings.js`
  - Raw (license): `https://raw.githubusercontent.com/Mintplex-Labs/anything-llm/master/LICENSE`

## Original Artifact Content

The following is the verbatim `saneDefaultSystemPrompt` definition from `server/models/systemSettings.js`. It is the default system prompt used whenever a workspace does not define its own `openAiPrompt`.

```javascript
const SystemSettings = {
  /** A default system prompt that is used when no other system prompt is set or available to the function caller. */
  saneDefaultSystemPrompt:
    "Given the following conversation, relevant context, and a follow up question, reply with an answer to the current question the user is asking. The current date and time is {datetime}. Return only your response to the question given the above information following the users instructions as needed.",
  protectedFields: ["multi_user_mode", "hub_api_key", "onboarding_complete"],
  publicFields: [
    "footer_data",
    "support_email",
    "text_splitter_chunk_size",
    // ...
  ],
  // ...
};
```

How the prompt is selected and prepared at runtime (verbatim from `server/utils/chats/index.js`), which defines the surrounding contract and the variable-substitution step:

```javascript
async function chatPrompt(workspace, user = null, opts = {}) {
  const { SystemSettings } = require("../../models/systemSettings");
  const { promptWithMemories } = require("../memories");
  const basePrompt =
    workspace?.openAiPrompt ?? SystemSettings.saneDefaultSystemPrompt;
  const systemPrompt = await SystemPromptVariables.expandSystemPromptVariables(
    basePrompt,
    user?.id,
    workspace?.id
  );
  // Memories are scoped per-user, but in single-user mode they are stored with a
  // null userId. Never inject them into anonymous/unauthenticated contexts.
  if (opts.skipMemories === true) return systemPrompt;
  return promptWithMemories({
    systemPrompt,
    userId: user?.id ?? null,
    workspaceId: workspace?.id,
    prompt: opts.prompt ?? "",
    rawHistory: opts.rawHistory ?? [],
  });
}
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Task is stated plainly (answer the current question from conversation + context + follow-up)
- [ ] Output constraint "Return only your response to the question" is explicit
- [ ] "following the users instructions as needed" precedence is stated

### 2. Context Grounding & RAG Alignment
- [ ] Explicitly references "relevant context" (RAG documents) as an input
- [ ] Explicitly references prior "conversation" and the "follow up question"
- [ ] Frame is suited to a retrieval-augmented chat assistant

### 3. Variable & Dynamic Injection Handling
- [ ] Uses a `{datetime}` template variable that is substituted at runtime
- [ ] Behavior is defined for the "no workspace prompt set" fallback case
- [ ] Memory injection is layered on top (and suppressed for unauthenticated contexts)

### 4. Safety / Scope Control
- [ ] Does not instruct the model to reveal hidden context or system internals
- [ ] Keeps scope to answering the user's current question
- [ ] Leaves room for the product to append memories/citations without contradiction

### 5. Testability
- [ ] `{datetime}` substitution is mechanically verifiable
- [ ] "Return only your response" is objectively checkable (no preamble/meta text)
- [ ] Fallback-vs-workspace-prompt behavior is directly testable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 25% | | |
| Context Grounding & RAG Alignment | 25% | | |
| Variable & Dynamic Injection Handling | 20% | | |
| Safety / Scope Control | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask a question answerable from the pinned/embedded workspace documents; verify the answer is grounded and free of preamble.
2. Send a multi-turn conversation with a follow-up question; verify continuity ("the following conversation… follow up question").
3. Configure a workspace `openAiPrompt` and verify it fully replaces the sane default.

### Boundary Test Cases
1. Empty retrieval context (no matching documents) — verify behavior is still coherent and non-hallucinatory.
2. Very long conversation history — verify the prompt still yields a single answer to the latest question.
3. Missing/odd `{datetime}` value — verify graceful handling of the substituted variable.

### Negative Test Cases
1. Verify the model does not output meta-commentary before/after the answer ("Return only your response…").
2. Verify it does not leak memory-injection scaffolding or system internals.
3. Anonymous/unauthenticated context — verify no per-user memory content is injected.

## Notes
- This is the default system prompt of an end-user-facing document chat product; it is deliberately short and relies on the app to prepend retrieved context and append memories.
- `{datetime}` is expanded by `SystemPromptVariables.expandSystemPromptVariables` before the call; treat it as a required runtime variable in tests.
- MIT license permits full quotation and modification.
