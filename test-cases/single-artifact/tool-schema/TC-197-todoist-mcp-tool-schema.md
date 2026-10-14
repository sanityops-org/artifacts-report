# TC-197: todoist-mcp-server (abhiz123) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: abhiz123/todoist-mcp-server (MCP server for natural-language Todoist task management)
- **License**: MIT (Copyright (c) 2024 Abhiram Nair)
- **Artifact Type**: Tool Schema (MCP tool definition for the `todoist_create_task` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/index.ts` — the `CREATE_TASK_TOOL: Tool` object (raw JSON Schema `inputSchema`) and the server bootstrap
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### The `todoist_create_task` tool (`src/index.ts`, fetched verbatim)

```typescript
// Define tools
const CREATE_TASK_TOOL: Tool = {
  name: "todoist_create_task",
  description: "Create a new task in Todoist with optional description, due date, and priority",
  inputSchema: {
    type: "object",
    properties: {
      content: {
        type: "string",
        description: "The content/title of the task"
      },
      description: {
        type: "string",
        description: "Detailed description of the task (optional)"
      },
      due_string: {
        type: "string",
        description: "Natural language due date like 'tomorrow', 'next Monday', 'Jan 23' (optional)"
      },
      priority: {
        type: "number",
        description: "Task priority from 1 (normal) to 4 (urgent) (optional)",
        enum: [1, 2, 3, 4]
      }
    },
    required: ["content"]
  }
};
```

### Server bootstrap (`src/index.ts`, fetched verbatim)

```typescript
// Server implementation
const server = new Server(
  {
    name: "todoist-mcp-server",
    version: "0.1.0",
```

### Sibling tools in the same array (fetched verbatim, headers only)

```typescript
const GET_TASKS_TOOL: Tool = { name: "todoist_get_tasks", ... };
const UPDATE_TASK_TOOL: Tool = { name: "todoist_update_task", ... };
const DELETE_TASK_TOOL: Tool = { name: "todoist_delete_task", ... };
const COMPLETE_TASK_TOOL: Tool = { name: "todoist_complete_task", ... };
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete raw JSON Schema (`type: object`, `properties`, `required`)
- [ ] Types are accurate (`string`, `string`, `string`, `number`)
- [ ] Required vs optional parameters are distinguishable (`content` required; the rest optional)
- [ ] A constrained field is modelled with `enum` (`priority: [1, 2, 3, 4]`)

### 2. Description Clarity
- [ ] The tool description states the capability ("Create a new task in Todoist ...")
- [ ] Every parameter has a human-readable `description`
- [ ] Optionality is stated inline ("(optional)")

### 3. Integration Compatibility
- [ ] Built with the official `@modelcontextprotocol/sdk` `Server` class
- [ ] The raw JSON Schema is standards-compliant and consumable by MCP clients and function-calling LLMs
- [ ] Uses the official `@doist/todoist-api-typescript` client for execution

### 4. Example Quality
- [ ] The `due_string` description embeds natural-language examples (`'tomorrow'`, `'next Monday'`, `'Jan 23'`)
- [ ] The `priority` description maps numeric values to meaning ("1 (normal) to 4 (urgent)")
- [ ] The `enum` on `priority` is machine-checkable, not just prose

### 5. Extensibility
- [ ] Tools are declared as discrete `Tool` constants (create/get/update/delete/complete), so each is independently testable
- [ ] The Todoist API token is read from an environment variable (`TODOIST_API_TOKEN`), keeping the tool surface credential-free
- [ ] The create/get/update siblings share the same field vocabulary (`content`, `description`, `due_string`, `priority`)

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
1. Issue "create a task to buy groceries tomorrow"; verify `todoist_create_task` is called with `content: "Buy groceries"` and `due_string: "tomorrow"`.
2. Issue "add an urgent task: 'Team Meeting' with description 'Weekly sync'"; verify `content: "Team Meeting"`, `description: "Weekly sync"`, `priority: 4`.
3. Issue "remind me to call the dentist next Monday"; verify `due_string: "next Monday"`.

### Boundary Test Cases
1. `priority` at each enum value (1, 2, 3, 4); verify all are accepted and lower/upper bounds hold.
2. A long `content` string near Todoist's length limit; verify behavior.
3. `due_string` with a relative date near a month/year boundary (e.g. "Dec 31"); verify parsing.
4. Only `content` supplied (all optional fields omitted); verify the task is still created.

### Negative Test Cases
1. `todoist_create_task` without the required `content`; verify validation rejects the call.
2. `priority: 5` (not in the enum); verify rejection.
3. `priority` provided as a string (e.g. `"high"`); verify type validation rejects it.
4. Missing `TODOIST_API_TOKEN`; verify an authentication error is surfaced rather than a silent no-op.

## Notes
- This is one logical artifact: the `todoist_create_task` tool. The server also exposes `todoist_get_tasks`, `todoist_update_task`, `todoist_delete_task`, and `todoist_complete_task`.
- The `inputSchema` is an author-written raw JSON Schema, quoted verbatim from `src/index.ts`.
- A useful quality discussion point: `update`/`delete`/`complete` locate a task by fuzzy `task_name` string rather than by immutable ID, a design tension between natural-language ergonomics and determinism.
- License is MIT; verbatim quotation is permissible.
