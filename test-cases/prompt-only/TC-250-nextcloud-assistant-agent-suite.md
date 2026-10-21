# TC-250: Nextcloud Assistant - Enterprise Productivity Agent Suite

## Metadata
- **Source Project**: nextcloud/assistant
- **GitHub**: https://github.com/nextcloud/assistant
- **Commit SHA**: 0911bc12c9443c96574fe7cca0c030266c7e6cc2
- **License**: AGPL-3.0 (per-file SPDX headers state AGPL-3.0-or-later)
- **Artifact Type**: Business-embedded logical artifacts (prompt components)
- **Business Scenario**: Enterprise productivity assistant inside Nextcloud (chat, task processing, file context)
- **Collection Date**: 2026-10-21
- **Collection Method**: Shallow clone at the pinned commit; verbatim extraction of server-side prompt constants and prompt builders. No rewriting or completion; placeholders preserved as-is.
- **Unit of Analysis**: Prompt component (verbatim)
- **Local Clone (read-only)**: `d:\My Docunments\AI\artifacts-report\_archive\_clones\nc-assistant`

## Project Overview
Nextcloud Assistant is the server-side Nextcloud app that provides a chat UI, an OCS/API surface and a set of assistant-specific task types on top of Nextcloud's TaskProcessing framework, delegating all model work to providers shipped by other apps (for example the OpenAI/LocalAI integration, llm2, Whisper or Stable Diffusion apps). It registers reference providers for the smart picker, listeners for task success/failure notifications, and providers such as TextToSticker, AudioToAudioTranslate, AudioToAudioChat and ContextAgentAudioInteraction. Chat conversations are persisted as sessions plus ordered messages with the roles `human`, `assistant` and `system`; every new session begins with one system message that stores the assistant's instructions. When the plain chat path is used, that system message is read back and sent as the `system_prompt` input of a `TextToTextChat`, `MultimodalChatWithTools` or `AudioToAudioChat` task, together with a bounded message history encoded as JSON strings. When a `ContextAgentInteraction` task type is available, the app instead routes the user's message to the agency flow with a confirmation flag and a conversation token, and no system prompt from this app is forwarded. Sessions marked as remembered are summarized by a background job into "memories" that are optionally injected into later model calls, and scheduled assignments re-enter the same chat pipeline with a reset conversation context.

## Business Loop
A user opens the Assistant inside Nextcloud, selects a task type (chat, text generation, summarization, translation, image generation, speech-to-text, sticker generation) or types a message into a chat session created for that user. The message is stored against a chat session owned by the user; the session carries a title, an optional remembered flag, an optional summary and, for the agency path, a conversation token and pending actions. Task execution runs either synchronously or as a background job through Nextcloud TaskProcessing, and the result comes back as a new assistant message, a notification, and/or an output file in the user's Assistant folder. Language is handled implicitly: the chat system prompt asks the model to detect the user's language and answer in it, and the title prompt asks for a title in the conversation's language. For remembered sessions, the summarizer reads up to 150 messages, produces a compact memory, and up to 10 memories are attached to later chat or agency tasks; scheduled assignments reuse a dedicated chat session and deliberately discard prior context between runs.

## Logical Artifact Inventory

### 1. Chat session system prompt (`CHAT_USER_INSTRUCTIONS`)
- **Source**: `lib/AppInfo/Application.php`
- **Line Range**: L60-L60
- **Type**: System Prompt
- **Composability**: standalone (admin-overridable at runtime)
- **Parameterization**: The literal contains no placeholder. At runtime `str_replace('{user}', $user->getDisplayName(), $userInstructions)` is applied (ChatService L73), so an administrator-supplied override may use `{user}`; the shipped default is sent unchanged. The value can be replaced through the app config key `chat_user_instructions` (ChatService L67-L72, Admin settings L56).
- **Business Entities**: chat session, system message, user display name, answer language, markdown formatting

```text
This is a conversation in a specific language between the user and you, Nextcloud Assistant. You are a kind, polite and helpful AI that helps the user to the best of its abilities. If you do not understand something, you will ask for clarification. Detect the language that the user is using. Make sure to use the same language in your response. Do not mention the language explicitly. Format your answers properly in markdown.
```

### 2. Conversation title generation prompt (`CHAT_USER_INSTRUCTIONS_TITLE`)
- **Source**: `lib/AppInfo/Application.php`
- **Line Range**: L61-L61
- **Type**: System Prompt (title-generation instruction)
- **Composability**: runtime-parameterized (instruction is combined with conversation history at scheduling time)
- **Parameterization**: Same `{user}` substitution as artifact 1, applied in ChatService L613 and ChattyLLMController L801. Overridable via the app config key `chat_user_instructions_title`. The string is passed as both the task `input` and the task `system_prompt` (ChatService L627), with the recent messages as `history`. The controller removes the instruction text, double quotes and everything after the first newline from the model output (ChattyLLMController L794-L805).
- **Business Entities**: chat session, session title, conversation language, user display name

```text
This is a conversation between the user and Nextcloud Assistant. Generate a suitable title for the conversation that summarizes it. Detect the language of the conversation. The title that you output should be in the same language as the conversation. Output only the title in plain text, nothing else. Do not mention the language explicitly. For example, if the conversation is about trees in sweden but is written in Spanish, the title could be "Àrboles en Suecia", if it was in English, the title could be "Trees in Sweden". Do not write the title in e.g. Swedish just because Sweden is mentioned in the conversation.
```

*Language note: the prompt is English; it embeds a Spanish sample title ("Àrboles en Suecia") as an example, quoted as-is.*

### 3. Session summary prompt (remembered chats)
- **Source**: `lib/Service/SessionSummaryService.php`
- **Line Range**: L62-L62 (prompt literal); transcript appended at L64-L66
- **Type**: Task Prompt
- **Composability**: runtime-parameterized (fixed instruction prefix followed by the conversation transcript)
- **Parameterization**: The literal ends with two newline characters (PHP `"\n\n"`); after it, each message is appended as `role . ': ' . content . "\n\n"` (L64-L66) and the result is sent as the `input` of a `TextToText` task (L68-L71). The `system` message is dropped before the transcript is built (L58-L60), and at most `SUMMARY_MESSAGE_LIMIT = 150` messages are read. The task is scheduled as app `assistant:summary-service` for the session owner.
- **Business Entities**: chat session marked as remembered, message role, message content, session summary, summary freshness flag

```text
Summarize insights about the user's circumstances, preferences and choices from the following conversation. Be as concise as possible. Especially mention any facts or numbers stated by the user. Do not add an introductory sentence or any other remarks.

```

### 4. Raw chat history memory prefix
- **Source**: `lib/Service/SessionSummaryService.php`
- **Line Range**: L141-L141
- **Type**: Instruction Constant (prompt fragment used to build a "memory")
- **Composability**: runtime-parameterized (prefix concatenated with a JSON-encoded message list)
- **Parameterization**: Used when a remembered session has no summary yet. The prefix is concatenated with `json_encode($chatHistory)`, where the history is the last `chat_last_n_messages` messages (default `10`, L139-L140). The resulting string is placed in the `memories` list passed to chat/agency tasks. The literal ends with a single space before the JSON payload.
- **Business Entities**: remembered session without summary, chat history, injected memories, message count limit

```text
This is the raw chat history of a chat between the user and Assistant: 
```

### 5. Outdated summary memory prefix
- **Source**: `lib/Service/SessionSummaryService.php`
- **Line Range**: L135-L135
- **Type**: Instruction Constant (prompt fragment used to build a "memory")
- **Composability**: runtime-parameterized (appended to an existing summary, followed by a JSON-encoded message list)
- **Parameterization**: Used when a remembered session has a summary whose freshness flag is false. The prefix is appended to the stored summary and concatenated with `json_encode($chatHistory)` restricted to the last `chat_last_n_messages` messages (default `10`). The literal ends with a single space before the JSON payload.
- **Business Entities**: remembered session, stale summary, recent chat history, injected memories

```text
The summary is outdated. These are the last messages in the raw chat history: 
```

### 6. Sticker generation prompt template
- **Source**: `lib/TaskProcessing/TextToStickerProvider.php`
- **Line Range**: L97-L97
- **Type**: Task Prompt (templated)
- **Composability**: runtime-parameterized (one substitution slot)
- **Parameterization**: `%1$s` is replaced with the user's sticker description through `IL10N::t('cartoon, neutral background, sticker of %1$s', [$input])`; the resulting string becomes the `input` of a `TextToImage` task with `numberOfImages = 1`. Because it passes through `IL10N`, the msgid can be translated and the runtime form depends on the active language.
- **Business Entities**: sticker task input, user description, image generation task, output image

```text
cartoon, neutral background, sticker of %1$s
```

## Composition Notes
- **Where the chat constant is injected**: `ChatService::createChatSession()` resolves `chat_user_instructions` (falling back to `CHAT_USER_INSTRUCTIONS`), substitutes `{user}`, and inserts it as the content of the first message with role `system` for the new session (ChatService L67-L98). The instruction is therefore persisted per session rather than recomposed on every turn; later changes to the admin setting affect only newly created sessions.
- **What surrounds it**: On the classic chat path, `scheduleMessageGeneration()` loads the first system message as `$systemPrompt` (L459-L462) and the recent messages via `getRawLastMessages()` (L695-L703). The system message itself is removed from the history. The task input is `['input' => lastHumanMessage, 'system_prompt' => systemPrompt, 'history' => historyMessages]` (L747-L751) for `TextToTextChat`, with `input_attachments` and empty `tools` added for `MultimodalChatWithTools` (L789-L796), and with only `system_prompt` plus history for `AudioToAudioChat` (L929-L933).
- **History and language**: History depth is controlled by the app config key `chat_last_n_messages` (default `10`); each entry is a JSON object `{"role": ..., "content": ...}`, and in the multimodal case content becomes a list of file and text parts. No per-user language parameter is sent; language behaviour is delegated entirely to the instruction "Detect the language that the user is using" in artifact 1 and to the equivalent sentence in artifact 2.
- **Memories**: When the chosen task type exposes an optional `memories` input, `SessionSummaryService::getMemories()` returns up to `MAX_INJECTED_SUMMARIES = 10` strings, each either a summary, a summary plus artifact 5 plus recent raw messages, or artifact 4 plus raw messages. These are added to the task input in the chat, audio-chat, agency and multimodal-agency paths.
- **Agency path bypass**: If the `ContextAgentInteraction` task type is available, `scheduleMessageGeneration()` does not send any system prompt; it sends only `input`, `confirmation`, `conversation_token` (and optionally `memories`) to the context-agent task (L416-L456, L831-L847). The agent's own instructions are supplied by the provider app and are out of scope here.
- **Title generation**: A separate task uses artifact 2 as both `input` and `system_prompt`, with the same history builder, and a custom task id prefix `chatty-title:` (L743-L745, L627). Only one generation task per session is allowed by `checkIfSessionIsThinking()`.
- **Assignments**: Scheduled assignments write their stored prompt as a `human` message into a dedicated session and call the agency task with an empty conversation token (`EMPTY_CONVERSATION_TOKEN = '{}'`), so no memory of prior runs is carried over (L542-L580).

## Coverage and Exclusions
- **Extracted**: six distinct shipped prompt components — the chat system prompt, the title-generation instruction, the session-summary task prompt, the two memory-building prefixes and the sticker prompt template. All are server-side PHP literals quoted verbatim with source path and line range.
- **Excluded (UI and localization)**: `l10n/*` translation catalogs, task-type and shape descriptions (`ShapeDescriptor` names/descriptions such as "System prompt", "Prompt", "Memories"), notification strings, settings labels, error messages and API documentation strings.
- **Excluded (non-prompt output text)**: the watermark suffix `This was generated using Artificial Intelligence.` in `AudioToAudioTranslateProvider` (L283-L285) is appended to task output, not sent as an instruction, so it is not counted as a prompt.
- **Excluded (runtime user data)**: the assignment prompt (`Db/Assignment::$prompt`) is end-user content, not a shipped instruction; `runTaskProcessingTask` and `TaskProcessingService` contain no prompt text.
- **Note on localization**: artifact 6 (the sticker prompt) is an English msgid passed through `IL10N::t()`, so its runtime form depends on the active UI language. It is quoted as shipped. No other prompt in the repository is passed through the translation layer.
- **Note on truncation**: nothing was truncated or paraphrased. Placeholders (`%1$s`, and the potential `{user}` in admin overrides) are preserved exactly as they appear in source.
- **Language**: the output file is English. The only non-English text is the Spanish example title inside artifact 2, quoted as-is and flagged above.
