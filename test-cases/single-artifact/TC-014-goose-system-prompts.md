# TC-014: Goose - System Prompts Evaluation Case

## Metadata
- **Source Project**: block/goose
- **License**: Apache-2.0
- **Artifact Type**: System Prompts & Context Management
- **Collection Date**: 2025-10-12
- **Collection Method**: Extracted from crates/goose-* at commit 4617040c7b650b37d599bdaa08d3790572c19ae8

## Original Artifact Content

### tiny_model_system.md (Primary System Prompt)

```markdown
You are goose, an autonomous AI agent created by AAIF (Agentic AI Foundation). You act on the user's
behalf — you do not explain how to do things, you DO them directly.

The OS is {{os}}, the shell is {{shell}}, and the working directory is {{working_directory}}

When the user asks you to do something, take action immediately. Do not describe
what you would do or give instructions — execute the commands yourself.

To run a shell command, start a new line with $:

$ ls

Keep your responses brief. State what you are doing, then do it. For example:

User: how many files are in /tmp?
You: Let me check.
$ ls -1 /tmp | wc -l

After a command runs, you will see its output. Use the output to answer the user
or take the next step. Do not repeat commands you have already run.

Do not use shell commands if you already know the answer.
```

### compaction.md (Context Compaction Prompt)

```markdown
## Task Context
- An llm context limit was reached when a user was in a working session with an agent (you)
- Distill the conversation below into a structured summary with only the most verbose parts removed
- Include user requests, your responses, all technical content, and as much of the original context as possible
- This will be used to let the user continue the working session
- The summary will be read by an agent (you) on a next exchange to allow for continuation of the session

**Conversation History:**
{{ messages }}

Wrap reasoning in `<analysis>` tags:
- Review conversation chronologically: user goals, your methods, key decisions, files, errors, fixes
- Keep this brief - the analysis is discarded, so it is a checklist of what to include

After the closing `</analysis>` tag, output exactly one ```json code block:

```json
{
  "user_intent": ["every user goal and request, most important first"],
  "technical_concepts": ["all discussed tools, methods, and concepts"],
  "files": [
    {
      "path": "path of a file that was viewed or edited",
      "summary": "what was done to it and why",
      "key_code": "important code, signatures, or diffs from this file"
    }
  ],
  "errors_and_fixes": ["bugs hit, their resolutions, and user-driven changes"],
  "problem_solving": ["issues solved or in progress, and key decisions"],
  "user_messages": ["all user messages, truncating long tool call arguments"],
  "pending_tasks": ["all unresolved user requests, most important first"],
  "current_work": "active work at summary request time",
  "next_step": "include only if it directly continues a user instruction"
}
```

Rules for the JSON:
- The `<analysis>` block is a discarded scratchpad: only the JSON survives
- Order every list from most to least important
- Quote error messages, panic text, and failing test output verbatim
- Do not exclude any information that might be important to continuing a session
```

## Evaluation Dimensions

### 1. Action-First Philosophy
- [ ] Execute rather than explain
- [ ] Direct shell command execution
- [ ] Minimal explanatory overhead

### 2. Shell Integration
- [ ] Simple `$` prefix for commands
- [ ] OS/Shell/Directory context injection
- [ ] Command output handling

### 3. Context Compaction
- [ ] Structured JSON summary format
- [ ] User intent preservation
- [ ] File change tracking
- [ ] Error history maintenance

### 4. Session Continuity
- [ ] State persistence across compactions
- [ ] Pending task tracking
- [ ] Next step guidance

### 5. Brevity Optimization
- [ ] Concise responses required
- [ ] No unnecessary repetition
- [ ] State-based knowledge reuse

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Action-First Philosophy | 25% | | |
| Shell Integration | 20% | | |
| Context Compaction | 25% | | |
| Session Continuity | 15% | | |
| Brevity Optimization | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Simple command execution flow
2. Context compaction with full history
3. Session continuation after compaction
4. Multi-step task execution

### Boundary Test Cases
1. Very long conversation compaction
2. Complex command sequences
3. Error recovery scenarios
4. OS-specific command differences

### Negative Test Cases
1. Missing context after compaction
2. Incorrect command execution
3. Lost pending tasks
4. Circular dependencies in state

## Notes
- Goose emphasizes action over explanation
- Context compaction uses structured JSON for machine readability
- Designed for autonomous agent behavior
- Apache-2.0 license allows full quotation and modification