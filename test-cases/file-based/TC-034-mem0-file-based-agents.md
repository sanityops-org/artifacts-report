# TC-034: Mem0 - File-Based Memory Layer for AI Agents

## Metadata
- **Source Project**: mem0ai/mem0
- **GitHub**: https://github.com/mem0ai/mem0
- **Commit SHA**: b7ad69afda6b6ed030347c66d48a13e4de9dec08
- **License**: Apache-2.0
- **Artifact Type**: File-based logical artifacts (Agent Plugin Skills)
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API retrieval via `gh api`

---

## Project Overview

Mem0 is a **memory layer for AI agents** that provides persistent, searchable memory across sessions. It integrates with coding agents and AI assistants to capture, store, and retrieve memories from earlier work. The agent-plugin-core provides skill modules that expose memory operations to agent harnesses (skills live as `integrations/agent-plugin-core/skills/<name>/SKILL.md.tmpl` Jinja-style templates, rendered per plugin under `integrations/<harness>-plugin/skills/<name>/SKILL.md`; this case scopes itself to agent-plugin-core — repo-wide, mem0 also ships skills in 10 harness plugins plus 6 top-level `skills/mem0-*` skills).

### Key Features
- **Persistent memory**: Memories survive across sessions and compaction
- **Semantic search**: Find relevant memories from earlier work
- **Repository-scoped**: Memories are scoped to repositories for relevance
- **Automatic capture**: Sessions automatically capture important information
- **Simple skill interface**: 6 skills for memory operations

---

## Logical Artifact Inventory

### 1. Prompts (TypeScript)

```typescript
export const SEARCH_WHEN =
  "before repeating investigation or when earlier decisions, fixes, commands, or results may help";

export const SEARCH_TOOL_DESCRIPTION = `Search memories from earlier work in this repository. Use it ${SEARCH_WHEN}.`;
export const SEARCH_QUERY_DESCRIPTION = "A direct question about earlier work in this repository.";
export const RECALL_HEADING = "Mem0 found these relevant memories from earlier work in this repository:";

export const USER_SEARCH_TOOL_DESCRIPTION = `Search memories from earlier work. Use it ${SEARCH_WHEN}.`;
export const USER_SEARCH_QUERY_DESCRIPTION = "A direct question about earlier work.";
export const USER_RECALL_HEADING = "Mem0 found these relevant memories from earlier work:";
```

---

## Skills

### 1. Remember Skill

```markdown
---
name: remember
description: Acknowledge a "remember this" request and make sure it is captured well. Use when the user explicitly asks to remember, note, or save something for future sessions.
disable-model-invocation: true
---

# Remember something for future sessions

Mem0 creates memories from the session automatically — there is no separate
write command. When the user asks to remember something:

1. Restate the fact clearly and completely in your reply, in one or two
   sentences, including any names, values, or paths it depends on. Your visible
   reply is what memory extraction reads, so a precise restatement is what gets
   remembered.

2. Tell the user it will be saved with this session's memories when the session
   ends or compacts, and that it will surface in future sessions in this
   repository (they can check later with /mem0:search).

Do not invent a storage confirmation or a memory ID — creation happens in the
background after the session.
```

### 2. Search Skill

```markdown
---
name: search
description: Search memories from earlier {{HARNESS_NAME}} sessions in this repository. Use it when earlier work may already explain the code, error, decision, or command you need, so you can avoid repeating file reads, searches, or experiments.
argument-hint: "[question] [--top-k number] [--category category-name] [--scope repo|dir|mine] [--run-id session-id]"
disable-model-invocation: true
---

# Search memories

Call `search_memories` with the user's question. Treat `--top-k`, `--category`,
`--scope`, and `--run-id` as tool arguments instead of including them in the
query.

Omit `top_k` to use Mem0's configured default. Omit `category` to search every
category. Omit `scope` to use the configured default, normally `repo`: this
repository's shared memory, which everyone who works in it contributes to,
plus your own preferences.

Pass `scope` when the question needs something else: `dir` to narrow the
shared memory to the directory you are working in (a package inside a
monorepo), `mine` for your own preferences alone.

Pass `run_id` with any scope to retrieve memories saved in a specific coding-agent
session. Omit `run_id` to search across sessions. It filters the memories returned;
it does not identify the session making the search request. Use a known session ID,
never invent one. Return the tool's result directly.
```

### 3. Forget Skill

```markdown
---
name: forget
description: Delete the Mem0 memories stored for this repository and this user. Use when the user asks to forget, clear, wipe, or delete memories.
disable-model-invocation: true
---

# Forget this repository's memories

This permanently deletes remote memories. Before running anything, tell the
user exactly what will be deleted: their own memories for this repository
only. The repository's project memory is shared by everyone who works in it,
so it stays unless the user explicitly asks to delete that too.

After the user confirms, run:

```bash
python3 "{{PLUGIN_ROOT}}/core/memory_cli.py" --harness "{{HARNESS_ID}}" {{PLUGIN_DATA_ARG}} forget --remote --yes
```

If the user also asked to delete the repository's shared project memory, add
`--include-project-memory` and say that this removes it for every teammate.

Report what the command output says was deleted. If the user only wants local
data cleared (evidence log, pending queue), run the same command without
`--remote`. Never pass `--yes` before the user has confirmed in this
conversation.
```

### 4. Pause Skill

```markdown
---
name: pause
description: Pause Mem0 memory capture on this machine. Use when the user wants to stop memories being recorded, for example for private work or experiments.
disable-model-invocation: true
---

# Pause memory capture

To pause (hooks stop capturing and sending session content; a minimal
telemetry ping still fires at session start, under your Mem0 account email,
unless `MEM0_TELEMETRY=false`):

```bash
python3 "{{PLUGIN_ROOT}}/core/memory_cli.py" --harness "{{HARNESS_ID}}" {{PLUGIN_DATA_ARG}} pause
```

Confirm the new state back to the user, and remind them that already-created
memories still exist and remain searchable. Pending unsent packets are held
while paused, not expired, and are delivered after resuming. To turn capture
back on, use `/mem0:resume`.
```

### 5. Resume Skill

```markdown
# integrations/agent-plugin-core/skills/resume/SKILL.md.tmpl

---
name: resume
description: Resume Mem0 memory capture after it was paused with /mem0:pause.
disable-model-invocation: true
---

# Resume memory capture

Resume memory capture for this machine.

Run:

```bash
python3 "{{PLUGIN_ROOT}}/core/memory_cli.py" --harness "{{HARNESS_ID}}" {{PLUGIN_DATA_ARG}} resume
```

Confirm to the user that capture is active again. New sessions record evidence and
create memories as normal; nothing that happened while paused is retroactively
captured.
```

### 6. Status Skill

```markdown
---
name: status
description: Show whether Mem0 memory is working in this repository, covering configuration, capture state, pending flushes, and whether the Mem0 API key is valid. Use when the user asks whether memory is on, why a memory is missing, or anything looks broken.
disable-model-invocation: false
---

# Memory status

Run both commands and report the combined result in plain language:

```bash
python3 "{{PLUGIN_ROOT}}/core/memory_cli.py" --harness "{{HARNESS_ID}}" {{PLUGIN_DATA_ARG}} status --json
python3 "{{PLUGIN_ROOT}}/core/memory_cli.py" --harness "{{HARNESS_ID}}" {{PLUGIN_DATA_ARG}} doctor
```

Summarize, using only fields the JSON actually reports: whether capture is
active or paused, the user ID and repository scope (`repo_id`), whether an
API key is configured, the event/flush/retrieval counts (`flushes` is the
number of completed flushes, not a pending count), and the doctor check
results. If doctor reports an authentication failure (401 / invalid key), say
clearly that the Mem0 API key is invalid or expired and that memories are NOT
being created. Never report an auth failure as "no memories found". Suggest
reinstalling with `--config api_key=...` in that case.
```

---

## Evaluation Dimensions

### 1. Skill Interface Design
- [ ] Skills follow consistent SKILL.md format with YAML frontmatter
- [ ] Each skill has clear name, description, and usage guidance
- [ ] `disable-model-invocation` flag correctly set per skill

### 2. Memory Operations
- [ ] Remember: Automatic capture with explicit acknowledgment
- [ ] Search: Repository-scoped with configurable scope (repo/dir/mine)
- [ ] Forget: User confirmation required for destructive operations
- [ ] Pause/Resume: Toggle capture state without losing existing memories
- [ ] Status: Diagnostic output for debugging memory issues

### 3. Template System
- [ ] Jinja2-like template variables: `{{PLUGIN_ROOT}}`, `{{HARNESS_ID}}`, `{{HARNESS_NAME}}`
- [ ] `{{PLUGIN_DATA_ARG}}` for plugin-specific data arguments
- [ ] Templates resolved at skill loading time

### 4. Safety and Privacy
- [ ] Forget requires user confirmation
- [ ] Pause allows private work without recording
- [ ] Repository-scoped memory isolation
- [ ] No storage confirmation or memory IDs invented

### 5. Integration Patterns
- [ ] Skills designed for agent harness integration
- [ ] CLI-based operations for transparency
- [ ] No separate write command (automatic capture)
- [ ] Session-based memory extraction

### 6. Extensibility
- [ ] Template variables enable harness-specific customization
- [ ] Skills can be extended with additional parameters
- [ ] Category filtering for organized memory retrieval

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Interface Design | 20% | | |
| Memory Operations | 25% | | |
| Template System | 15% | | |
| Safety and Privacy | 20% | | |
| Integration Patterns | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Skill Interface Tests
1. **Frontmatter parsing**: Verify YAML frontmatter is correctly parsed
2. **Template resolution**: Test `{{PLUGIN_ROOT}}` and other variables resolve correctly
3. **Disable-model-invocation**: Verify flag is respected by agent harness

### Memory Operations Tests
1. **Remember workflow**: Verify restatement is captured for memory extraction
2. **Search scopes**: Test repo/dir/mine scope filtering
3. **Forget confirmation**: Verify destructive operation requires confirmation
4. **Pause/Resume toggle**: Test capture state transitions
5. **Status diagnostics**: Verify status command reports accurate state

### Integration Tests
1. **Harness integration**: Test skills work with different agent harnesses
2. **CLI execution**: Verify memory_cli.py commands execute correctly
3. **Session extraction**: Test memory extraction at session end

### Safety Tests
1. **Forget safety**: Verify confirmation required before deletion
2. **Privacy mode**: Verify pause stops recording
3. **Scope isolation**: Verify memories are scoped to correct repository

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- Demonstrates **minimal skill interface** pattern for agent plugins
- **6 skills** provide complete memory lifecycle management
- **Template system** enables harness-specific customization
- **No separate write command** simplifies memory capture
- **Repository scoping** provides context-relevant memory retrieval

---

## Comparison with Other File-Based Agents

| Feature | TC-031 (Nanobot) | TC-032 (Hermes) | TC-033 (OpenAgent) | TC-034 (Mem0) |
|---------|-----------------|-----------------|--------------------|--------------|
| **Primary Focus** | Personal assistant framework | Multi-surface assistant | Single-binary assistant | Memory layer |
| **Skills Count** | 11 | 58 built-in / 200+ total | 54 | 6 |
| **Template System** | Jinja2 | Jinja2 | None | Jinja2-like |
| **Backend Language** | Python | Python | Go | Python |
| **Key Innovation** | SOUL.md personality | Prompt caching invariant | Single-binary deploy | Auto memory capture |
| **Agent Architecture** | AgentLoop + Subagent | Multi-surface facade | Beego MVC | Plugin skills |
| **Memory Support** | JSONL history log | Memory plugins | RAG knowledge base | Core feature |