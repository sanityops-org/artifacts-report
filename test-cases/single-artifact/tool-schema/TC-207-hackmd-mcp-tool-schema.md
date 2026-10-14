# TC-207: HackMD MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: yuna0x0/hackmd-mcp (MCP server for the HackMD collaborative-note API)
- **License**: MIT (Copyright (c) 2025 yuna0x0)
- **Artifact Type**: Tool Schema (MCP tool definition for the `create_note` tool; companion note tools `list_user_notes`, `get_note`, `update_note`, `delete_note`)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `tools/userNotes.ts` — the user-note tool registrations (`server.tool(...)`)
  - `utils/schemas.ts` — the `CreateNoteOptionsSchema` / `UpdateNoteOptionsSchema` payload schemas
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool registrations (`tools/userNotes.ts`, fetched verbatim)

```typescript
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { API } from "@hackmd/api";
import { z } from "zod";
import {
  CreateNoteOptionsSchema,
  UpdateNoteOptionsSchema,
} from "../utils/schemas.js";

export function registerUserNotesApiTools(server: McpServer, client: API) {
  // Tool: List user's notes
  server.tool(
    "list_user_notes",
    "List all notes owned by the user",
    {},
    {
      title: "Get a list of notes in the user's workspace",
      readOnlyHint: true,
      openWorldHint: true,
    },
    async () => {
      try {
        const notes = await client.getNoteList();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(notes, null, 2),
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error: ${error.message}` }],
          isError: true,
        };
      }
    },
  );

  // Tool: Get note by ID
  server.tool(
    "get_note",
    "Get a note by its ID",
    {
      noteId: z.string().describe("Note ID"),
    },
    {
      title: "Get a note",
      readOnlyHint: true,
      openWorldHint: true,
    },
    async ({ noteId }) => {
      try {
        const note = await client.getNote(noteId);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(note, null, 2),
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error: ${error.message}` }],
          isError: true,
        };
      }
    },
  );

  // Tool: Create a new note
  server.tool(
    "create_note",
    "Create a new note",
    {
      payload: CreateNoteOptionsSchema.describe("Create note options"),
    },
    {
      title: "Create a note",
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true,
    },
    async ({ payload }) => {
      try {
        const note = await client.createNote(payload);
        return {
          content: [
            {
              type: "text",
              text: `Note created successfully:\n${JSON.stringify(note, null, 2)}`,
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error: ${error.message}` }],
          isError: true,
        };
      }
    },
  );

  // Tool: Update a note
  server.tool(
    "update_note",
    "Update an existing note",
    {
      noteId: z.string().describe("Note ID"),
      payload: UpdateNoteOptionsSchema.describe("Update note options"),
    },
    {
      title: "Update a note",
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: true,
    },
    async ({ noteId, payload }) => {
      try {
        const result = await client.updateNote(noteId, payload);
        return {
          content: [
            {
              type: "text",
              text: `Note ${noteId} updated successfully:\n${JSON.stringify(result, null, 2)}`,
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error: ${error.message}` }],
          isError: true,
        };
      }
    },
  );

  // Tool: Delete a note
  server.tool(
    "delete_note",
    "Delete a note",
    {
      noteId: z.string().describe("Note ID"),
    },
    {
      title: "Delete a note",
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
      openWorldHint: true,
    },
    async ({ noteId }) => {
      try {
        const result = await client.deleteNote(noteId);
        return {
          content: [
            {
              type: "text",
              text: `Note ${noteId} deleted successfully:\n${JSON.stringify(result, null, 2)}`,
            },
          ],
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error: ${error.message}` }],
          isError: true,
        };
      }
    },
  );
}
```

### Payload schemas (`utils/schemas.ts`, fetched verbatim)

```typescript
// Local type definitions to match HackMD API types
enum NotePermissionRole {
  OWNER = "owner",
  SIGNED_IN = "signed_in",
  GUEST = "guest",
}

enum CommentPermissionType {
  DISABLED = "disabled",
  FORBIDDEN = "forbidden",
  OWNERS = "owners",
  SIGNED_IN_USERS = "signed_in_users",
  EVERYONE = "everyone",
}

export const CreateNoteOptionsSchema = z.object({
  title: z.string().optional().describe("Note title"),
  content: z.string().optional().describe("Note content"),
  readPermission: z
    .enum([
      NotePermissionRole.OWNER,
      NotePermissionRole.SIGNED_IN,
      NotePermissionRole.GUEST,
    ])
    .optional()
    .describe("Read permission"),
  writePermission: z
    .enum([
      NotePermissionRole.OWNER,
      NotePermissionRole.SIGNED_IN,
      NotePermissionRole.GUEST,
    ])
    .optional()
    .describe("Write permission"),
  commentPermission: z
    .enum([
      CommentPermissionType.DISABLED,
      CommentPermissionType.FORBIDDEN,
      CommentPermissionType.OWNERS,
      CommentPermissionType.SIGNED_IN_USERS,
      CommentPermissionType.EVERYONE,
    ])
    .optional()
    .describe("Comment permission"),
  permalink: z.string().optional().describe("Custom permalink"),
});
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Each tool exposes a concrete Zod input schema (an empty object for `list_user_notes`; `{noteId}`; or `{payload}`)
- [ ] Types are accurate (`string`, nested object with `enum` fields)
- [ ] Required vs optional is distinguishable (`noteId` is required for get/delete; all `CreateNoteOptionsSchema` fields are `.optional()`)
- [ ] Nested schemas are reused (`CreateNoteOptionsSchema`, `UpdateNoteOptionsSchema`) rather than inlined

### 2. Description Clarity
- [ ] Every tool has a short human description ("Create a new note", "Get a note by its ID") and a `title`
- [ ] Every parameter and enum value carries a `.describe(...)` string
- [ ] The `payload` parameter is annotated ("Create note options" / "Update note options")

### 3. Integration Compatibility
- [ ] Conforms to the MCP tool model (`server.tool(name, description, params, annotations, handler)`)
- [ ] Declares `ToolAnnotations` with correct mutation flags (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)
- [ ] Zod schemas are converted to JSON Schema by the SDK, so they are consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] Enum values are self-describing (`owner`/`signed_in`/`guest`; `everyone`/`owners`/...)
- [ ] The write-permission and read-permission enums share a consistent role vocabulary
- [ ] Mutation semantics differ correctly between tools (create = not destructive; update/delete = destructive; delete = idempotent)

### 5. Extensibility
- [ ] Note payload schemas are factored into `utils/schemas.ts`, so create/update share validation and remain independently extensible
- [ ] Tools are grouped by resource (`userNotes.ts`, plus team-note/team/profile/history modules) behind a single `register...ApiTools` entrypoint
- [ ] The shared HackMD `API` client is injected into each register function, decoupling tools from transport/auth

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
1. Issue "create a HackMD note titled 'Meeting Notes' with the agenda"; verify `create_note` is called with `payload.title` and `payload.content`.
2. Issue "list my HackMD notes"; verify `list_user_notes` is selected (no parameters).
3. Issue "read note abc123"; verify `get_note` with `noteId: "abc123"`.

### Boundary Test Cases
1. `create_note` with only `title` (no `content`); verify the schema accepts it since all fields are optional.
2. `readPermission: "guest"` combined with `writePermission: "owner"`; verify distinct enums for read vs write are both accepted.
3. `commentPermission` set to each of the five valid enum values; verify all pass.
4. `update_note` with a `payload` that changes only `readPermission`; verify partial updates are accepted.

### Negative Test Cases
1. `get_note` called without `noteId`; verify schema validation rejects the call.
2. `readPermission: "admin"` (out of enum); verify rejection.
3. A request to permanently remove a team-owned note using the personal delete tool; verify the model does not conflate `delete_note` with team-note deletion.
4. `create_note` with `payload` supplied as a flat string instead of an object; verify schema validation rejects it.

## Notes
- This case quotes the user-note tool set verbatim from `tools/userNotes.ts` and the supporting payload schemas from `utils/schemas.ts`. The `create_note` tool is the representative focus; the companion note tools are quoted because they share the same file and the same `CreateNoteOptionsSchema`/`UpdateNoteOptionsSchema` dependency.
- Input schemas are authored in Zod and converted to JSON Schema by the MCP TypeScript SDK at registration time, so the schema the LLM receives is generated from this source. The `ToolAnnotations` blocks are part of the tool definition surface.
- License is MIT; verbatim quotation is permissible.
