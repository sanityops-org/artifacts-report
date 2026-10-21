# TC-159: Weizhena/Deep-Research-skills (Preliminary Research) - Skill Evaluation Case

## Metadata
- **Source Project**: Weizhena/Deep-Research-skills
- **License**: MIT (LICENSE file present; GitHub API reports `spdx_id: MIT`)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/Weizhena/Deep-Research-skills/master/skills/research-en/research/SKILL.md (default branch `master`). Repository README: https://raw.githubusercontent.com/Weizhena/Deep-Research-skills/master/README.md . License file: https://raw.githubusercontent.com/Weizhena/Deep-Research-skills/master/LICENSE . Repository tree (GitHub API): https://api.github.com/repos/Weizhena/Deep-Research-skills/git/trees/HEAD?recursive=1

## Original Artifact Content

````markdown
---
name: research
user-invocable: true
allowed-tools: Read, Write, Glob, WebSearch, Task, AskUserQuestion
description: Conduct preliminary research on a topic and generate research outline. For academic research, benchmark research, technology selection, etc.
---

# Research Skill - Preliminary Research

## Trigger
`/research <topic>`

## Workflow

### Step 1: Generate Initial Framework from Model Knowledge
Based on topic, use model's existing knowledge to generate:
- Main research objects/items list in this domain
- Suggested research field framework

Output {step1_output}, use AskUserQuestion to confirm:
- Need to add/remove items?
- Does field framework meet requirements?

### Step 2: Web Search Supplement
Use AskUserQuestion to ask for time range (e.g., last 6 months, since 2024, unlimited).

**Parameter Retrieval**:
- `{topic}`: User input research topic
- `{YYYY-MM-DD}`: Current date
- `{step1_output}`: Complete output from Step 1
- `{time_range}`: User specified time range

**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording.

Launch 1 web-search-agent (background), **Prompt Template**:
```python
prompt = f"""## Task
Research topic: {topic}
Current date: {YYYY-MM-DD}

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
{step1_output}

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for {topic} related items within {time_range} and supplement
4. Supplement new fields

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
"""
```

**One-shot Example** (assuming researching AI Coding History):
```
## Task
Research topic: AI Coding History
Current date: 2025-12-30

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
### Items List
1. GitHub Copilot: Developed by Microsoft/GitHub, first mainstream AI coding assistant
2. Cursor: AI-first IDE, based on VSCode
...

### Field Framework
- Basic Info: name, release_date, company
- Technical Features: underlying_model, context_window
...

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for AI Coding History related items within since 2024 and supplement
4. Supplement new fields

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
```

### Step 3: Ask User for Existing Fields
Use AskUserQuestion to ask if user has existing field definition file, if so read and merge.

### Step 4: Generate Outline (Separate Files)
Merge {step1_output}, {step2_output} and user's existing fields, generate two files:

**outline.yaml** (items + config):
- topic: Research topic
- items: Research objects list
- execution:
  - batch_size: Number of parallel agents (confirm with AskUserQuestion)
  - items_per_agent: Items per agent (confirm with AskUserQuestion)
  - output_dir: Results output directory (default: ./results)

**fields.yaml** (field definitions):
- Field categories and definitions
- Each field's name, description, detail_level
- detail_level hierarchy: brief -> moderate -> detailed
- uncertain: Uncertain fields list (reserved field, auto-filled in deep phase)

### Step 5: Output and Confirm
- Create directory: `./{topic_slug}/`
- Save: `outline.yaml` and `fields.yaml`
- Show to user for confirmation

## Output Path
```
{current_working_directory}/{topic_slug}/
  ├── outline.yaml    # items list + execution config
  └── fields.yaml     # field definitions
```

## Follow-up Commands
- `/research-add-items` - Supplement items
- `/research-add-fields` - Supplement fields
- `/research-deep` - Start deep research
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter has `name` (`research`), `user-invocable: true`, `allowed-tools`, and a `description`
- [ ] `allowed-tools` scopes the capability set (Read, Write, Glob, WebSearch, Task, AskUserQuestion)
- [ ] No in-file `license`, but the repository LICENSE is MIT

### 2. Trigger Condition Clarity
- [ ] An explicit "Trigger" section (`/research <topic>`)
- [ ] `description` states the use cases (academic, benchmark, technology selection)
- [ ] Follow-up commands extend the workflow (`/research-add-items`, `/research-add-fields`, `/research-deep`)

### 3. Instruction Structure
- [ ] Clear numbered workflow (Steps 1–5) with a defined output path
- [ ] Human-in-the-loop confirmations via `AskUserQuestion` at each stage
- [ ] A "Hard Constraint" that pins a verbatim sub-agent prompt template

### 4. Example / Output Quality
- [ ] A complete one-shot example (AI Coding History) showing the filled prompt and expected output shape
- [ ] Concrete artifact schema for `outline.yaml` and `fields.yaml`
- [ ] Parameter retrieval list (`{topic}`, `{YYYY-MM-DD}`, `{step1_output}`, `{time_range}`)

### 5. Maintainability
- [ ] Modular file outputs (`outline.yaml` + `fields.yaml`) that separate items from field definitions
- [ ] Companion skills extend the flow without editing this one
- [ ] Versioned workflow with reserved fields ("uncertain") for a later deep phase

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. `/research AI Coding History`; verify it generates an initial framework and asks the user to confirm items/fields
2. Provide a time range ("since 2024"); verify the sub-agent prompt is filled with that range and launched
3. Proceed to Step 4; verify `outline.yaml` and `fields.yaml` are written under `./{topic_slug}/`

### Boundary Test Cases
1. User provides an existing field-definition file; verify Step 3 reads and merges it
2. A very broad topic; verify it asks the user to narrow the item list before searching
3. No web access for the sub-agent; verify it reports the limitation rather than fabricating sources

### Negative Test Cases
1. Whether it alters the Hard Constraint prompt structure/wording (the skill forbids this)
2. Whether it invents sources/URLs in the "Sources" section
3. Whether it skips the human-in-the-loop confirmations and runs straight to output

## Notes
- End-user research artifact authored as a Markdown SKILL.md; the body is a research workflow with an embedded sub-agent prompt template, not executable code (the `python` code block is an illustrative f-string).
- MIT license permits verbatim reproduction.
- The repository targets multiple hosts (Claude Code / OpenCode / Codex) and ships English and Chinese variants (`skills/research-en/`, `skills/research-zh/`, `skills/research-codex-*`); this case captures the English Claude variant `skills/research-en/research/SKILL.md`.
- Distinct from TC-138/TC-158 (marketing) and TC-148 (persona research): this is a structured, human-in-the-loop deep-research outline skill.
