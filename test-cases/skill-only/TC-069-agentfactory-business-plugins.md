# TC-069: AgentFactory Business Plugins - File-Based Office Agent Suite

## Metadata
- **Source Project**: AgentFactory Business Plugins (panaversity/agentfactory-business-plugins)
- **GitHub**: github.com/panaversity/agentfactory-business-plugins
- **License**: Apache-2.0
- **Artifact Type**: File-based logical artifacts (Markdown skills + agent definitions for a business "agentic office")
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw content fetch (branch: `main`) from:
  - `https://raw.githubusercontent.com/panaversity/agentfactory-business-plugins/main/agentic-office/skills/task-intelligence/SKILL.md`
  - `https://raw.githubusercontent.com/panaversity/agentfactory-business-plugins/main/agentic-office/skills/workplace-search/SKILL.md`
  - `https://raw.githubusercontent.com/panaversity/agentfactory-business-plugins/main/agentic-office/agents/chief-of-staff.md`

---

## Project Overview

AgentFactory Business Plugins is a **file-based plugin suite** that equips a general-purpose agent (Claude Code / Cowork) with a functioning **"agentic office"**: a set of Markdown skills and agents that keep the professional's work context (priorities, people, projects, decisions) coherent. Every artifact is a plain-text Markdown file, so the entire "brain" is inspectable and version-controllable.

### Key Features
- **File as configuration**: `SKILL.md` (capability) and agent `.md` (role) files, no compiled code
- **Shared working context**: all skills/agents read `work.local.md` as the single source of organisational truth
- **Layered memory model**: PERSONAL / TEAM / PROJECTS / ORGANISATIONAL layers
- **Explicit anti-fabrication rules**: skills must say "Not in workplace memory" rather than invent answers
- **Trigger-scoped skills**: frontmatter descriptions declare exactly when a skill activates and when it must not

---

## Logical Artifact Inventory

### 1. `skills/task-intelligence/SKILL.md` - Priority & Planning Skill

```markdown
---
name: task-intelligence
description: >
  Activate for: brain dump, prioritise, P1 P2 P3, critical path,
  daily priorities, weekly planning, backlog review, cross-domain plan,
  what should I work on, capture everything in my head, sort my priorities,
  what is most important right now, weekly critical path.
  NOT for: basic task CRUD (use official productivity plugin task-management),
  delegation (use delegation skill).
---
## TASK INTELLIGENCE WORKFLOW
### STEP 1 — LOAD CONTEXT
Read `work.local.md` in the current working directory.
If it does not exist, tell the user to run `/agentic-office:setup` first.
### STEP 2 — IDENTIFY REQUEST TYPE
TYPE 1: CAPTURE (from brain dump / meeting notes / messages)
Purpose: Rapidly capture and structure unorganised input.
Input: Raw notes, brain dump, meeting output, messages — any format
Output: Structured, prioritised list with owners and deadlines
TYPE 2: DAILY PRIORITISATION
Purpose: Determine what to work on today from a larger set.
Input: Full list (from work.local.md or provided)
Output: Today's critical path (3-5 items) + schedule suggestion
TYPE 3: WEEKLY PLANNING
Purpose: Set the week's priorities before it begins.
Input: Project statuses; open delegations; upcoming deadlines
Output: Week-ahead critical path; delegation candidates; decision items
TYPE 4: BACKLOG REVIEW
Purpose: Audit the backlog — drop dead items; re-prioritise the rest.
Input: Current backlog
Output: Kept / dropped / re-prioritised list with rationale
TYPE 5: CROSS-DOMAIN PLAN
Purpose: Generate an integrated action plan for a scenario that
spans multiple functions (HR + Finance + Ops, etc.)
Output: Items by function; dependencies; delegations; timeline
### STEP 3 — EXECUTE WITH PRIORITY SORTING
OUTPUT STRUCTURE:
```
CAPTURE — [Date]
================================================================
[N] items captured | [N] overdue | [N] delegation candidates
-- P1 — URGENT / HIGH IMPACT ---------------------------------
[ ] [ITEM-NNN] [Title]
  Context:  [Why this matters; what it connects to]
  Due:      [Specific date or "today"]
  Project:  [Project name from work.local.md]
  Action:   [Specific first action — not vague]
  Delegate: [If applicable — to whom]
  Note:     [Any sensitivity or communication guidance]
-- P2 — IMPORTANT / THIS WEEK --------------------------------
[Same structure]
-- P3 — STANDARD / BACKLOG -----------------------------------
[Same structure — briefer]
-- DELEGATION CANDIDATES --------------------------------------
[Item] → [Person from work.local.md] (with brief note on approach)
-- BLOCKED / AT RISK ------------------------------------------
[Any item that cannot proceed without something else; name the blocker]
================================================================
```
### Priority Sorting Logic
When determining priority, apply in order:
1. Is there a hard deadline? (Date-certain = prioritise)
2. Is it blocking someone else? (Blocking = elevate)
3. Does it affect a P1 project? (P1 project item = at least P2)
4. What is the consequence if it slips one week? (Assess impact honestly)
5. Is the urgency feeling real or just habitual? (Email = rarely P1)
### The Brain Dump Pattern
When user provides unorganised input:
1. Extract every distinct item (even if vague or incomplete)
2. Enrich each with project context from work.local.md
3. Identify dependencies between items
4. Flag anything that should be delegated
5. Flag anything that should be dropped or questioned
### Item vs. Project Distinction
ITEM: Can be completed in one session; has a single clear output
PROJECT: Multiple items; spans days or weeks; has milestones
If an "item" has >3 steps and spans >1 day: it is a project.
Create a project entry in work.local.md instead.
Breaking projects down into single-session items is the user's job —
or use `/agentic-office:progress-tracker` to create a milestone plan.
## NEVER DO THESE
- NEVER classify more than 5 items as P1 — force re-prioritisation
  if the user tries to make everything critical
- NEVER leave a captured item without a project reference if
  it connects to a known project in work.local.md
- NEVER produce a list without a critical path — a list of
  everything is not a plan; a critical path is
- NEVER mark an item as P1 based purely on urgency without
  assessing actual importance
- NEVER produce a weekly plan without surfacing open delegations
```

### 2. `skills/workplace-search/SKILL.md` - Cross-Context Recall Skill

```markdown
---
name: workplace-search
description: >
  Activate for: search everything, cross-context search,
  what do we know about, find the decision, search all layers,
  search across workplace memory, what was agreed, when did we decide,
  find everything about, who knows about, what have we discussed about,
  pull everything on, find in workplace memory, search all.
  NOT for: basic memory lookup (use official productivity plugin memory-management),
  adding new entries (use workplace-context).
---
## CROSS-CONTEXT SEARCH WORKFLOW
### STEP 1 — LOAD CONTEXT
Read `work.local.md` in the current working directory.
If it does not exist, tell the user to run `/agentic-office:setup` first.
### STEP 2 — SEARCH ALL LAYERS
Search across all four memory layers simultaneously:
PERSONAL: Working style; current focus; priorities
TEAM: Person entries; communication notes; relationship history
PROJECTS: Project names; codenames; status; decisions; milestones
ORGANISATIONAL: Terminology; meeting notes; decision log; action log
### STEP 3 — PRODUCE RESULTS
OUTPUT STRUCTURE:
```
SEARCH RESULTS: "[Query]"
================================================================
Found in:
PROJECT MEMORY:
[Relevant project entries — name; status; connection to query]
MEETING NOTES / DECISION LOG:
[Relevant decisions; when made; by whom; context]
PEOPLE MEMORY:
[Relevant person entries — role; connection to query]
TERMINOLOGY:
[Relevant term definitions]
DELEGATION LOG:
[Any active or past delegations related to query]
RECOMMENDED NEXT STEP:
[Specific actionable recommendation based on search results]
================================================================
```
### Search Behaviour Rules
IF FOUND: Surface all relevant entries; note the layer each came from
IF NOT FOUND: Say explicitly "Not in workplace memory" —
do not fabricate; offer to add if the user can provide the information
IF PARTIAL: Surface what exists; flag what is missing;
offer to add the missing information
### Cross-Reference Pattern
For queries that span multiple layers:
"What do we know about [topic]?"
Search all layers simultaneously
Group results by layer
Synthesise: "Here is the complete picture across all memory layers"
"When did we decide [X]?"
Search decision log first
Cross-reference with meeting notes
Surface: decision + date + context + who was involved
## NEVER DO THESE
- NEVER return search results from memory you do not have — if it is
  not in work.local.md, say so clearly
- NEVER search only one layer when the query could span multiple
- NEVER omit the recommended next step — search without a
  recommended action is information without utility
```

### 3. `agents/chief-of-staff.md` - Orchestration Agent

```markdown
---
name: chief-of-staff
description: >
  Activate for: chief of staff, orchestration agent, digital chief of staff, daily digest delivery, morning brief, executive dashboard, weekly brief, week ahead, week close, what needs my attention, situational awareness, all domains summary, cross-domain status.
background: true
memory: project
skills:
  - digest
  - progress-tracker
  - executive-brief
  - workplace-search
  - context-loader
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
---
## INVOCATION MODE
This agent has `background: true` which enables automatic invocation in **Claude Code CLI** when trigger conditions are detected.
In **Cowork mode**, this agent must be invoked via a **Scheduled Task**. See `COWORK-SCHEDULED-TASKS.md` for the recommended schedule and prompt. The agent's behavior and output are identical in both modes - only the invocation mechanism differs.
## AGENT PURPOSE
The orchestration agent. Synthesise intelligence from all active domain agents
and from work.local.md to provide coherent operational awareness for the
professional it serves. The Digital Chief of Staff does not do the domain work —
it ensures the person doing the domain work always knows what matters, what is
at risk, and what needs their attention today.
## DAILY TASKS
### 07:00 (or configured time) — DELIVER DAILY DIGEST
Load: work.local.md (all layers)
Pull: Google Calendar (today + next 7 days) if MCP available
Pull: Notion / project tracker (overdue + due today + due this week) if MCP available
Pull: Gmail (flagged / unread requiring response) if MCP available
Pull: Slack (@mentions; flagged items) if MCP available
Pull: Domain agent feeds (if configured in work.local.md agent_integrations)
Assemble using the digest skill structure.
Deliver via configured channel.
### REAL-TIME — ANY WORKPLACE INTELLIGENCE QUESTION
Respond to any question about work status, people, projects, or priorities
using full work.local.md context.
Apply the rule: answer as a knowledgeable colleague would —
not as a system returning a database query.
### FLAG ANY THRESHOLD BREACH (any time)
Monitor against configured thresholds in work.local.md:
escalation_threshold_days: flag as critical after N days without update
delegation_confirmation_window: send follow-up after N hours
blocker_stale_threshold: escalate after N days
When a threshold is breached: add to next digest as RED item.
If severity is critical: send immediate alert via configured channel.
## WEEKLY TASKS
### MONDAY — WEEK-AHEAD BRIEF (06:45 or configured time)
Deliver before the work day begins:
```
WEEK AHEAD BRIEF — Week of [Date]
================================================================
THIS WEEK'S BOULDERS / PRIORITIES:
[From work.local.md — using org terminology]
CRITICAL MILESTONES THIS WEEK:
[P1 project milestones due; any hard deadlines]
DECISIONS NEEDED THIS WEEK:
[Decisions that must be made — not deferred further]
DELEGATION CHECKS DUE:
[Delegations where a check-in is due this week]
MEETINGS REQUIRING PREP:
[Significant meetings this week]
WHAT WOULD MAKE THIS WEEK A SUCCESS:
[The 3 things that, if done, mean the week was well spent]
================================================================
```
### FRIDAY — WEEK CLOSE SUMMARY (17:30 or configured time)
```
WEEK CLOSE — Week of [Date]
================================================================
COMPLETED:
[What was done; milestones closed; decisions made]
CARRIES FORWARD:
[What did not complete; why; plan for next week]
WHAT TO SET UP FOR MONDAY:
[Things that will be easier if done today]
NEXT WEEK PREVIEW:
[Key milestones; meetings; decisions — what is coming]
================================================================
```
## ESCALATION PROTOCOL
When any item exceeds its configured threshold:
LEVEL 1 — Digest flag (AMBER): item included in next morning's digest
LEVEL 2 — Explicit message: direct notification if digest is not actioned
LEVEL 3 — COO/Executive level: if flagged >14 days without resolution
Escalation message format:
"ESCALATION: [Item] has been [blocked/unactioned/overdue] for [N days].
This is affecting [downstream impact]. Recommended action: [specific].
Would you like me to [draft the escalation message / schedule the conversation]?"
## NEVER DO THESE
- NEVER suppress a threshold breach because "the person probably knows"
- NEVER produce the Monday brief after 08:00 — it must be ready before
  the work day begins
- NEVER answer a workplace intelligence question using generic AI knowledge
  when work.local.md contains specific organisational context
- NEVER let the Friday close become a judgment on the week — its purpose
  is information and preparation, not evaluation
```

---

## Artifact Relationship Map

| Artifact | Type | Reads | Consumes / Produces |
|----------|------|-------|---------------------|
| `task-intelligence` | Skill | `work.local.md` | Produces prioritised critical paths (P1–P3) |
| `workplace-search` | Skill | `work.local.md` (all 4 layers) | Produces cross-layer search results |
| `chief-of-staff` | Agent | `work.local.md` + MCP feeds | Orchestrates `digest`, `progress-tracker`, `executive-brief`, `workplace-search`, `context-loader` |

All three artifacts share one convention: **`work.local.md` is the sole source of organisational truth**, and skills must never fabricate beyond it.

---

## Evaluation Dimensions

### 1. File Organization Clarity
- [ ] Clear separation between `skills/` (capability) and `agents/` (role) artifacts
- [ ] Unified frontmatter convention (`name`, `description`) across files
- [ ] Trigger descriptions state both when to use and when NOT to use
- [ ] Single shared context file (`work.local.md`) declared consistently

### 2. Markdown Structure
- [ ] YAML frontmatter used for metadata and skill/agent wiring
- [ ] Structured output templates given inside fenced code blocks
- [ ] Numbered workflow steps with explicit inputs/outputs
- [ ] "NEVER DO THESE" guardrail sections present

### 3. Agent-Skill Composition
- [ ] Agent frontmatter enumerates its skills and tools
- [ ] Agent declares invocation mode (`background: true`) and memory scope
- [ ] Scheduled-task vs interactive invocation documented
- [ ] Cross-references between artifacts are resolvable paths

### 4. Anti-Fabrication / Grounding
- [ ] Skills must read `work.local.md` before answering
- [ ] Missing data is reported explicitly, not invented
- [ ] Agent forbids generic AI answers when org context exists
- [ ] Escalation/threshold rules are explicit and deterministic

### 5. Operational Value (Office Assistant Fit)
- [ ] Daily digest, weekly brief, and week-close cycles defined with times
- [ ] Priority-sorting logic is ordered and explicit
- [ ] Layered memory (Personal/Team/Projects/Organisational) is coherent
- [ ] Next-step recommendation required in outputs

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| File Organization Clarity | 20% | | |
| Markdown Structure | 15% | | |
| Agent-Skill Composition | 20% | | |
| Anti-Fabrication / Grounding | 25% | | |
| Operational Value | 20% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. Validate each `SKILL.md` / agent frontmatter parses and required keys exist
2. Verify skills declare negative triggers ("NOT for ...") correctly
3. Confirm `chief-of-staff` lists only skills and tools that exist

### Grounding Tests
1. Run a search with an empty `work.local.md` context; confirm "Not in workplace memory" response
2. Ask a workplace question with specific org context; confirm no generic answer
3. Attempt a >5 item P1 dump; confirm the skill forces re-prioritisation

### Workflow Tests
1. Brain dump → confirm structured P1/P2/P3 output with critical path
2. Weekly plan request → confirm open delegations are surfaced
3. Trigger `chief-of-staff` digest → confirm required output sections appear

### Invocation-Mode Tests
1. In CLI mode, confirm background/trigger invocation behaves as documented
2. In Cowork mode, confirm the agent runs via the scheduled task path
3. Confirm behavior/output parity between the two invocation modes

### Integration Tests
1. With MCP feeds configured, confirm calendar/tracker/mail/slack pulls appear in the digest
2. Breach a configured threshold; confirm the item escalates to a RED digest item

---

## Notes

- This is a **NON-coding, business/office knowledge-assistant** suite; all artifacts are Markdown configuration, not application code.
- All three listed artifacts were fetched successfully from the `main` branch (exact URLs recorded in Metadata). No content is fabricated.
- Only the three files above were retrieved; companion files referenced inside them (e.g., `work.local.md`, `COWORK-SCHEDULED-TASKS.md`, the `digest` / `progress-tracker` / `executive-brief` / `context-loader` skills) were **not fetched** and are described only as referenced. No companion content is quoted.
- The suite is a strong reference for **file-based office/chief-of-staff agents** where a single shared context file grounds all skills and prevents hallucinated workplace knowledge.
