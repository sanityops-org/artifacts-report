# TC-184: Slack MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers-archived (reference server `src/slack`)
- **License**: MIT (Copyright (c) 2024 Anthropic, PBC)
- **Artifact Type**: Tool Schema (MCP tool definitions: `slack_list_channels`, `slack_post_message`, `slack_reply_to_thread`, `slack_add_reaction`, `slack_get_channel_history`, `slack_get_thread_replies`, `slack_get_users`, `slack_get_user_profile`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/slack/index.ts` — tool definitions and request handlers
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definitions (`src/slack/index.ts`, fetched verbatim)

```typescript
// Tool definitions
const listChannelsTool: Tool = {
  name: "slack_list_channels",
  description: "List public or pre-defined channels in the workspace with pagination",
  inputSchema: {
    type: "object",
    properties: {
      limit: {
        type: "number",
        description:
          "Maximum number of channels to return (default 100, max 200)",
        default: 100,
      },
      cursor: {
        type: "string",
        description: "Pagination cursor for next page of results",
      },
    },
  },
};

const postMessageTool: Tool = {
  name: "slack_post_message",
  description: "Post a new message to a Slack channel",
  inputSchema: {
    type: "object",
    properties: {
      channel_id: {
        type: "string",
        description: "The ID of the channel to post to",
      },
      text: {
        type: "string",
        description: "The message text to post",
      },
    },
    required: ["channel_id", "text"],
  },
};

const replyToThreadTool: Tool = {
  name: "slack_reply_to_thread",
  description: "Reply to a specific message thread in Slack",
  inputSchema: {
    type: "object",
    properties: {
      channel_id: {
        type: "string",
        description: "The ID of the channel containing the thread",
      },
      thread_ts: {
        type: "string",
        description: "The timestamp of the parent message in the format '1234567890.123456'. Timestamps in the format without the period can be converted by adding the period such that 6 numbers come after it.",
      },
      text: {
        type: "string",
        description: "The reply text",
      },
    },
    required: ["channel_id", "thread_ts", "text"],
  },
};

const addReactionTool: Tool = {
  name: "slack_add_reaction",
  description: "Add a reaction emoji to a message",
  inputSchema: {
    type: "object",
    properties: {
      channel_id: {
        type: "string",
        description: "The ID of the channel containing the message",
      },
      timestamp: {
        type: "string",
        description: "The timestamp of the message to react to",
      },
      reaction: {
        type: "string",
        description: "The name of the emoji reaction (without ::)",
      },
    },
    required: ["channel_id", "timestamp", "reaction"],
  },
};

const getChannelHistoryTool: Tool = {
  name: "slack_get_channel_history",
  description: "Get recent messages from a channel",
  inputSchema: {
    type: "object",
    properties: {
      channel_id: {
        type: "string",
        description: "The ID of the channel",
      },
      limit: {
        type: "number",
        description: "Number of messages to retrieve (default 10)",
        default: 10,
      },
    },
    required: ["channel_id"],
  },
};

const getThreadRepliesTool: Tool = {
  name: "slack_get_thread_replies",
  description: "Get all replies in a message thread",
  inputSchema: {
    type: "object",
    properties: {
      channel_id: {
        type: "string",
        description: "The ID of the channel containing the thread",
      },
      thread_ts: {
        type: "string",
        description: "The timestamp of the parent message in the format '1234567890.123456'. Timestamps in the format without the period can be converted by adding the period such that 6 numbers come after it.",
      },
    },
    required: ["channel_id", "thread_ts"],
  },
};

const getUsersTool: Tool = {
  name: "slack_get_users",
  description:
    "Get a list of all users in the workspace with their basic profile information",
  inputSchema: {
    type: "object",
    properties: {
      cursor: {
        type: "string",
        description: "Pagination cursor for next page of results",
      },
      limit: {
        type: "number",
        description: "Maximum number of users to return (default 100, max 200)",
        default: 100,
      },
    },
  },
};

const getUserProfileTool: Tool = {
  name: "slack_get_user_profile",
  description: "Get detailed profile information for a specific user",
  inputSchema: {
    type: "object",
    properties: {
      user_id: {
        type: "string",
        description: "The ID of the user",
      },
    },
    required: ["user_id"],
  },
};
```

### List-tools wiring (fetched verbatim, same file)

```typescript
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    console.error("Received ListToolsRequest");
    return {
      tools: [
        listChannelsTool,
        postMessageTool,
        replyToThreadTool,
        addReactionTool,
        getChannelHistoryTool,
        getThreadRepliesTool,
        getUsersTool,
        getUserProfileTool,
      ],
    };
  });
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Every tool declares `type: "object"` with `properties`
- [ ] Required vs optional parameters are marked (e.g. `limit`/`cursor` optional; `channel_id`/`text` required)
- [ ] Defaults are declared inline (`limit` default 100 / 10)
- [ ] Types are accurate (`string`, `number`)

### 2. Description Clarity
- [ ] Each tool has a concise functional description
- [ ] Parameters are individually described
- [ ] The unusual `thread_ts` timestamp format is explained, including a conversion rule

### 3. Integration Compatibility
- [ ] Declared via the MCP `Tool` type and returned by `ListToolsRequestSchema`
- [ ] JSON-Schema `inputSchema` is directly consumable by MCP clients and function-calling LLMs
- [ ] Read tools and write tools are both present, allowing a client to assess side effects

### 4. Example Quality
- [ ] Format examples embedded in descriptions (`'1234567890.123456'`, "without ::")
- [ ] Pagination pattern (`cursor` + `limit`) is consistent across list tools
- [ ] Tool names cover a complete messaging workflow (list → post → reply → react → read history)

### 5. Extensibility
- [ ] Tools are separate `const` definitions aggregated in the list handler
- [ ] Consistent naming prefix (`slack_`) and shared parameter names (`channel_id`)
- [ ] New tools can be added by following the same definition + handler pattern

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Schema Completeness | 25% | | |
| Description Clarity | 20% | | |
| Integration Compatibility | 25% | | |
| Example Quality | 20% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "post 'standup in 5' to the general channel"; verify `slack_post_message` is selected with `channel_id` and `text`.
2. Issue "what were the last 20 messages in #eng?"; verify `slack_get_channel_history` with `channel_id` and `limit: 20`.
3. Issue "reply in that thread saying we will ship Friday"; verify `slack_reply_to_thread` with `channel_id`, `thread_ts`, `text`.

### Boundary Test Cases
1. `limit` omitted on both list tools; verify defaults (100 for channels/users, 10 for history) are applied.
2. `limit` above the documented max (200); verify behavior is defined (server clamps with `Math.min`).
3. Pagination: fetch page 1, then call again with the returned `cursor`.
4. `slack_add_reaction` with an emoji name containing or omitting colons; verify guidance ("without ::").

### Negative Test Cases
1. `slack_post_message` without `text`; verify rejection (schema requires both `channel_id` and `text`).
2. `slack_get_user_profile` without `user_id`; verify rejection.
3. `slack_reply_to_thread` with a `thread_ts` that does not match the documented format; verify the model attempts to normalize it per the description.
4. Ambiguous request "message the team"; verify the model asks which channel instead of guessing a `channel_id`.

## Notes
- This is the archived MCP Slack reference server; the eight tools are quoted verbatim from `src/slack/index.ts` and constitute one tightly-related tool group from a single file.
- The `inputSchema` values are hand-written JSON Schema; the tool descriptions intentionally embed format guidance (timestamps, emoji names) that the LLM uses for argument formatting.
- License is MIT; long verbatim quotation is permissible.
