# TC-004: GPT Researcher Multi-Agent - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: gpt-researcher (assafelovic/gpt-researcher)
- **Submodule**: `multi_agents/` (LangGraph implementation)
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent suite (role prompts + graph state + task configuration)
- **Collection Date**: 2026-10-20
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `master`:
  - `multi_agents/agents/orchestrator.py`
  - `multi_agents/agents/editor.py`
  - `multi_agents/agents/researcher.py`
  - `multi_agents/agents/reviewer.py`
  - `multi_agents/agents/reviser.py`
  - `multi_agents/agents/writer.py`
  - `multi_agents/agents/publisher.py`
  - `multi_agents/agents/human.py`
  - `multi_agents/memory/research.py`
  - `multi_agents/task.json`
- **Artifact coverage**: 4 of the 8 roles carry LLM prompt text; 4 do not (Chief Editor, Researcher, Publisher, Human).

---

## Project Structure (verbatim facts)

`ChiefEditorAgent._create_workflow` registers these LangGraph nodes:

```python
workflow.add_node("browser", agents["research"].run_initial_research)
workflow.add_node("planner", agents["editor"].plan_research)
workflow.add_node("researcher", agents["editor"].run_parallel_research)
workflow.add_node("writer", agents["writer"].run)
workflow.add_node("publisher", agents["publisher"].run)
workflow.add_node("human", agents["human"].review_plan)
```

Edges:

```python
workflow.add_edge('browser', 'planner')
workflow.add_edge('planner', 'human')
workflow.add_edge('researcher', 'writer')
workflow.add_edge('writer', 'publisher')
workflow.set_entry_point("browser")
workflow.add_edge('publisher', END)
workflow.add_conditional_edges(
    'human',
    lambda review: "accept" if review['human_feedback'] is None else "revise",
    {"accept": "researcher", "revise": "planner"}
)
```

Reviewer and Reviser are **not** top-level nodes. They form a nested loop inside `EditorAgent._create_workflow`, applied per section:

```python
workflow.add_node("researcher", agents["research"].run_depth_research)
workflow.add_node("reviewer", agents["reviewer"].run)
workflow.add_node("reviser", agents["reviser"].run)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "reviewer")
workflow.add_edge("reviser", "reviewer")
workflow.add_conditional_edges(
    "reviewer",
    lambda draft: "accept" if draft["review"] is None else "revise",
    {"accept": END, "revise": "reviser"},
)
```

---

## Logical Artifact Inventory

### 1. Editor system prompt (`multi_agents/agents/editor.py`, verbatim)

```python
{
    "role": "system",
    "content": "You are a research editor. Your goal is to oversee the research project "
               "from inception to completion. Your main task is to plan the article section "
               "layout based on an initial research summary.\n ",
}
```

The user message is assembled by `_format_planning_instructions`:

```python
return f"""Today's date is {today}
           Research summary report: '{initial_research}'
           {feedback_instruction}
           \nYour task is to generate an outline of sections headers for the research project
           based on the research summary report above.
           You must generate a maximum of {max_sections} section headers.
           You must focus ONLY on related research topics for subheaders and do NOT include introduction, conclusion and references.
           You must return nothing but a JSON with the fields 'title' (str) and 
           'sections' (maximum {max_sections} section headers) with the following structure:
           '{{title: string research title, date: today's date, 
           sections: ['section header 1', 'section header 2', 'section header 3' ...]}}'."""
```

### 2. Reviewer prompt (`multi_agents/agents/reviewer.py`, verbatim)

```python
TEMPLATE = """You are an expert research article reviewer. \
Your goal is to review research drafts and provide feedback to the reviser only based on specific guidelines. \
"""
```

```python
review_prompt = f"""You have been tasked with reviewing the draft which was written by a non-expert based on specific guidelines.
Please accept the draft if it is good enough to publish, or send it for revision, along with your notes to guide the revision.
If not all of the guideline criteria are met, you should send appropriate revision notes.
If the draft meets all the guidelines, please return None.
{revise_prompt if revision_notes else ""}
Guidelines: {guidelines}\nDraft: {draft_state.get("draft")}\n
"""
```

The reviewer returns `None` for acceptance or free-form revision notes; there is **no** numeric scoring schema.

### 3. Reviser prompt (`multi_agents/agents/reviser.py`, verbatim)

```python
{
    "role": "system",
    "content": "You are an expert writer. Your goal is to revise drafts based on reviewer notes.",
}
```

```python
"content": f"""Draft:\n{draft_report}" + "Reviewer's notes:\n{review}\n\n
You have been tasked by your reviewer with revising the following draft, which was written by a non-expert.
If you decide to follow the reviewer's notes, please write a new draft and make sure to address all of the points they raised.
Please keep all other aspects of the draft the same.
You MUST return nothing but a JSON in the following format:
{sample_revision_notes}
"""
```

```python
sample_revision_notes = """
{
  "draft": { 
    draft title: The revised draft that you are submitting for review 
  },
  "revision_notes": Your message to the reviewer about the changes you made to the draft based on their feedback
}
"""
```

### 4. Writer prompt (`multi_agents/agents/writer.py`, verbatim)

```python
{
    "role": "system",
    "content": "You are a research writer. Your sole purpose is to write a well-written "
    "research reports about a "
    "topic based on research findings and information.\n ",
}
```

The writer is asked for introduction, conclusion, table of contents, and sources only:

```python
sample_json = """
{
  "table_of_contents": A table of contents in markdown syntax (using '-') based on the research headers and subheaders,
  "introduction": An indepth introduction to the topic in markdown syntax and hyperlink references to relevant sources,
  "conclusion": A conclusion to the entire research based on all research data in markdown syntax and hyperlink references to relevant sources,
  "sources": A list with strings of all used source links in the entire research data in markdown syntax and apa citation format. For example: ['-  Title, year, Author [source url](source)', ...]
}
"""
```

### 5. Roles with no prompt artifact

- **Chief Editor** (`orchestrator.py`): `ChiefEditorAgent` only wires the LangGraph workflow; it contains no LLM call and no prompt.
- **Researcher** (`researcher.py`): wraps `GPTResearcher` and calls `conduct_research()` / `write_report()`; no system message is sent by this file.
- **Publisher** (`publisher.py`): assembles a Markdown layout and calls `write_md_to_pdf`, `write_md_to_word`, `write_text_to_md`; no prompt.
- **Human** (`human.py`): reads feedback from websocket or `input()`; no prompt.

### 6. State schema (`multi_agents/memory/research.py`, verbatim in full)

```python
from typing import TypedDict, List, Annotated
import operator
class ResearchState(TypedDict):
    task: dict
    initial_research: str
    sections: List[str]
    research_data: List[dict]
    human_feedback: str
    # Report layout
    title: str
    headers: dict
    date: str
    table_of_contents: str
    introduction: str
    conclusion: str
    sources: List[str]
    report: str
```

### 7. Task configuration (`multi_agents/task.json`, verbatim in full)

```json
{
  "query": "Is AI in a hype cycle?",
  "max_sections": 3,
  "publish_formats": {
    "markdown": true,
    "pdf": true,
    "docx": true
  },
  "include_human_feedback": false,
  "follow_guidelines": false,
  "model": "gpt-4o",
  "guidelines": [
    "The report MUST be written in APA format",
    "Each sub section MUST include supporting sources using hyperlinks. If none exist, erase the sub section or rewrite it to be a part of the previous section",
    "The report MUST be written in spanish"
  ],
  "verbose": true
}
```

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 8 classes exist with distinct responsibilities
- [ ] Only 4 roles carry prompt text; the other 4 are code-only roles
- [ ] Input/output between nodes is defined by `ResearchState`

### 2. Workflow Completeness
- [ ] Top-level graph covers browser → planner → human → researcher → writer → publisher
- [ ] Reviewer/Reviser loop exists per section, not globally
- [ ] Human feedback can loop back to the planner

### 3. Prompt Consistency
- [ ] Citation and guideline constraints are passed via `task.json`, not repeated in prompts
- [ ] Output formats differ by role (JSON for planner/reviser/writer, free text or None for reviewer)
- [ ] Reviewer has no numeric score; quality gating depends on guideline text

### 4. Tool Modularity
- [ ] Tools are Python methods, not function-calling schemas
- [ ] `MCPClientManager` supplies external MCP tools at runtime
- [ ] Tool-to-role mapping is implicit in each class

### 5. Observability
- [ ] `ResearchState` carries task, research data, drafts, human feedback, and final report
- [ ] Errors are printed or logged; there is no structured error field
- [ ] Human intervention is a graph node guarded by `include_human_feedback`

### 6. Extensibility
- [ ] New roles require a class plus graph wiring
- [ ] New tools require a retriever or MCP server, not a schema entry
- [ ] Configuration is file-driven through `task.json`

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|---|---|---|---|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

1. Run the full graph with `include_human_feedback=false` and verify the human node passes through.
2. Set `follow_guidelines=true` and verify the reviewer returns revision notes until the draft meets `guidelines`.
3. Force a reviewer rejection and verify the reviser loop terminates when the reviewer returns `None`.
4. Fail `GPTResearcher.conduct_research()` and verify the graph surfaces the failure.
5. Replace a section draft with an empty string and verify writer/reviewer behavior.

---

## Notes

- The upstream repository has no tool/function schema; tool use is Python method calls plus `MultiServerMCPClient.get_tools()`.
- `multi_agents/agents/` contains 8 agent modules, but only `editor.py`, `reviewer.py`, `reviser.py`, and `writer.py` send system messages.
- The previous version of this case was a documentation summary with invented prompts and tool schemas. It has been replaced with the quoted upstream text above.
