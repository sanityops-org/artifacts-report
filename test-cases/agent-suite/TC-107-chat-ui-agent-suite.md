# TC-107: Chat UI (HuggingChat) - Prompt Assembly and Preprompt Configuration

## Metadata
- **Source Project**: Chat UI (huggingface/chat-ui) — powers the HuggingChat app
- **License**: Apache-2.0
- **Artifact Type**: Prompt assembly contract + `preprompt` model configuration (the repository ships **no** system prompt text)
- **Collection Date**: 2026-10-20
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/lib/buildPrompt.ts`
  - `src/lib/server/models.ts`
  - `src/lib/server/endpoints/preprocessMessages.ts`
- **Re-type note**: The previous version of this case claimed a shipped system prompt. Chat UI has none: `preprompt` is a model-config field with default `""`, and the final system message is whatever the deployment supplies. This case therefore evaluates the real prompt-assembly contract instead of a non-existent prompt.

---

## Original Artifact Content

### 1. Prompt assembly (`src/lib/buildPrompt.ts`, verbatim in full)

```typescript
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

### 2. `preprompt` model configuration (`src/lib/server/models.ts`, verbatim excerpt)

```typescript
const modelConfig = z.object({
	/** Used as an identifier in DB */
	id: z.string().optional(),
	/** Used to link to the model page, and for inference */
	name: z.string().default(""),
	displayName: z.string().min(1).optional(),
	description: z.string().min(1).optional(),
	logoUrl: z.string().url().optional(),
	websiteUrl: z.string().url().optional(),
	modelUrl: z.string().url().optional(),
	tokenizer: z.never().optional(),
	datasetName: z.string().min(1).optional(),
	datasetUrl: z.string().url().optional(),
	preprompt: z.string().default(""),
	prepromptUrl: z.string().url().optional(),
	chatPromptTemplate: z.never().optional(),
	promptExamples: z
		.array(
			z.object({
				title: z.string().min(1),
				prompt: z.string().min(1),
			})
		)
		.optional(),
```

### 3. Message preprocessing (`src/lib/server/endpoints/preprocessMessages.ts`, verbatim in full)

```typescript
import type { Message } from "$lib/types/Message";
import type { EndpointMessage } from "./endpoints";
import { downloadFile } from "../files/downloadFile";
import type { ObjectId } from "mongodb";
import { withTrackioViewContext } from "$lib/utils/trackioView";
import { plainMentions } from "$lib/utils/mentionTokens";

export async function preprocessMessages(
	messages: Message[],
	convId: ObjectId
): Promise<EndpointMessage[]> {
	return Promise.resolve(messages)
		.then((msgs) => downloadFiles(msgs, convId))
		.then(injectTrackioViews)
		.then(stripEmptyInitialSystemMessage);
}

/** pasted text stays a file, the prompt builder inlines it within the attachment budget */
async function downloadFiles(messages: Message[], convId: ObjectId): Promise<EndpointMessage[]> {
	return Promise.all(
		messages.map<Promise<EndpointMessage>>((message) =>
			Promise.all(
				(message.files ?? []).map(async (file) => {
					const downloaded = await downloadFile(file.value, convId);
					// the bucket names a file by conversation id and hash, the message keeps the uploaded name
					return { ...downloaded, name: file.name || downloaded.name };
				})
			).then((files) => ({ ...message, files }))
		)
	);
}

function injectTrackioViews(messages: EndpointMessage[]): EndpointMessage[] {
	return messages.map((message) => {
		if (message.from !== "user") return message;
		const content = withTrackioViewContext(
			plainMentions(message.content),
			message.dashboardViews ?? []
		);
		return content === message.content ? message : { ...message, content };
	});
}

/**
 * Remove an initial system message if its content is empty/whitespace only.
 * This prevents sending an empty system prompt to any provider.
 */
function stripEmptyInitialSystemMessage(messages: EndpointMessage[]): EndpointMessage[] {
	if (!messages?.length) return messages;
	const first = messages[0];
	if (first?.from !== "system") return messages;
	const content = first?.content as unknown;
	const isEmpty = typeof content === "string" ? content.trim().length === 0 : false;
	if (isEmpty) {
		return messages.slice(1);
	}
	return messages;
}
```

---

## Evaluation Dimensions

### 1. Prompt Assembly Correctness
- [ ] `preprompt` replaces the first system message only when present
- [ ] Message roles are preserved when converted to the chat template
- [ ] Truncation is applied after rendering and is bounded

### 2. Preprompt Contract
- [ ] `preprompt` is optional and defaults to an empty string
- [ ] `prepromptUrl` is validated as a URL when supplied
- [ ] `promptExamples` entries require both a title and a prompt

### 3. Message Preprocessing
- [ ] Uploaded files are resolved before rendering
- [ ] Empty initial system messages are removed
- [ ] User mentions and dashboard views are injected deterministically

### 4. Provider Compatibility
- [ ] The rendered prompt works with OpenAI-compatible chat and completion endpoints
- [ ] No prompt is invented when the deployment supplies none
- [ ] Multi-provider fallback does not change the prompt semantics

### 5. Observability
- [ ] The final prompt can be snapshotted before the provider call
- [ ] Missing `preprompt` is distinguishable from an empty one
- [ ] Truncation is observable from the rendered prompt length

### 6. Extensibility
- [ ] New prompt sources can be added via `prepromptUrl`
- [ ] New models can declare their own preprompt without code changes
- [ ] Prompt examples are data, not code

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|---|---|---|---|
| Prompt Assembly Correctness | 25% | | |
| Preprompt Contract | 20% | | |
| Message Preprocessing | 20% | | |
| Provider Compatibility | 15% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

1. Configure a model with `preprompt` and verify it replaces the first system message.
2. Configure a model without `preprompt` and verify no system message is fabricated.
3. Send an empty initial system message and verify it is stripped before rendering.
4. Attach a file and verify it is downloaded and passed to the prompt builder within the attachment budget.
5. Set `truncate` and verify the rendered prompt is truncated to that many words.
6. Supply `promptExamples` and verify each entry renders with its title.

---

## Notes

- Chat UI deliberately ships no default system prompt. The `preprompt` slot is deployment- and model-specific.
- The previous version of this case treated `buildPrompt.ts` and README configuration prose as a system prompt. It has been replaced with the actual assembly code and the preprompt schema.
