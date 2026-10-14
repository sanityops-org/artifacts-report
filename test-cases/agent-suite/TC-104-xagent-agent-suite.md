# TC-104: XAgent - Agent Suite Evaluation Case

## Metadata
- **Source Project**: XAgent (OpenBMB/XAgent)
- **Submodule**: `XAgent/agent/` (multi-role agents: dispatcher, plan_generate, plan_refine, reflect, tool agents) + `XAgent/agent/plan_generate_agent/prompt.py` (planner system prompt) + `XAgent/ai_functions/` (tool/function schemas) + `ToolServer/`
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent suite (autonomous agent: Dispatcher + Planner + Actor roles with per-role prompts + tool schemas)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/OpenBMB/XAgent`
  - `https://raw.githubusercontent.com/OpenBMB/XAgent/main/README.md`
  - `https://raw.githubusercontent.com/OpenBMB/XAgent/main/XAgent/agent/plan_generate_agent/prompt.py`
  - `https://api.github.com/repos/OpenBMB/XAgent/contents/XAgent/agent` (directory listing)
  - `https://api.github.com/repos/OpenBMB/XAgent` (repository metadata, license = Apache-2.0)

---

## Project Overview

XAgent is an **autonomous, general-purpose LLM agent** that solves open-ended tasks by decomposing them into subtasks and executing them with a ToolServer. It exposes a web GUI and CLI, and is applicable to end-user knowledge and workflow tasks (search & report, data analysis, life assistant, etc.).

From the project README (verbatim):

> "XAgent is an open-source experimental Large Language Model (LLM) driven autonomous agent that can automatically solve various tasks. It is designed to be a general-purpose agent that can be applied to a wide range of tasks."

> "XAgent is composed of three parts:
> - **🤖 Dispatcher** is responsible for dynamically instantiating and dispatching tasks to different agents...
> - **🧐 Planner** is responsible for generating and rectifying plans for tasks. It divides tasks into subtasks and generates milestones for them...
> - **🦾 Actor** is responsible for conducting actions to achieve goals and finish subtasks..."

> "ToolServer is the server that provides XAgent with powerful and safe tools to solve tasks... it provides:
> - **📝 File Editor** provides a text editing tool to write, read, and modify files.
> - **📘 Python Notebook** provides an interactive Python notebook...
> - **🌏 Web Browser** provides a web browser to search and visit webpages.
> - **🖥️ Shell** provides a bash shell tool...
> - **🧩 Rapid API** provides a tool to retrieve APIs from Rapid API and call them..."

---

## Logical Artifact Inventory

### 1. Planner System Prompt (`XAgent/agent/plan_generate_agent/prompt.py`, verbatim)

```
SYSTEM_PROMPT = '''You are an efficient plan-generation agent, your task is to decompose a query into several subtasks that describe must achieved goals for the query.
--- Background Information ---
PLAN AND SUBTASK:
A plan has a tree manner of subtasks: task 1 contatins subtasks task 1.1, task 1.2, task 1.3, ... and task 1.2 contains subtasks 1.2.1, 1.2.2, ...
A subtask-structure has the following json component:
{
"subtask name": string, name of the subtask
"goal.goal": string, the main purpose of the subtask, and what will you do to reach this goal?
"goal.criticism": string, what potential problems may the current subtask and goal have?
"milestones": list[string]. what milestones should be achieved to ensure the subtask is done? Make it detailed and specific.
}
SUBTASK HANDLE:
A task-handling agent will handle all the subtasks as the inorder-traversal. ...
RESOURCES:
1. Internet access for searches and information gathering, search engine and web browsing.
2. A FileSystemEnv to read and write files (txt, code, markdown, latex...)
3. A python notebook to execute python code. Always follow python coding rules.
4. A ShellEnv to execute bash or zsh command to further achieve complex goals.
--- Task Description ---
Generate the plan for query with operation SUBTASK_SPLIT, make sure all must reach goals are included in the plan.
*** Important Notice ***
- Always make feasible and efficient plans that can lead to successful task solving. Never create new subtasks that similar or same as the existing subtasks.
- For subtasks with similar goals, try to do them together in one subtask with a list of subgoals, rather than split them into multiple subtasks.
...
'''
```

### 2. Planner User Prompt (`prompt.py`, verbatim)

```
USER_PROMPT = '''This is not the first time you are handling the task, so you should give a initial plan. Here is the query:
"""
{{query}}
"""
You will use operation SUBTASK_SPLIT to split the query into 2-4 subtasks and then commit.'''
```

### 3. Agent Role Inventory (`XAgent/agent/` — directory listing, verbatim paths)

```
XAgent/agent/base_agent.py
XAgent/agent/dispatcher.py
XAgent/agent/dispatcher_agent/        (dir)
XAgent/agent/plan_generate_agent/     (dir: agent.py, prompt.py)
XAgent/agent/plan_refine_agent/       (dir)
XAgent/agent/reflect_agent/           (dir)
XAgent/agent/summarize.py
XAgent/agent/tool_agent/              (dir)
XAgent/agent/utils.py
```

### 4. Tool / Function Surface (`XAgent/ai_functions/`, README verbatim)

- `XAgent/ai_functions/` holds the function manager and tool definitions.
- ToolServer tools (README): **File Editor**, **Python Notebook**, **Web Browser**, **Shell**, **Rapid API**.
- Examples referenced in README: `AskForHumanHelp` tool (human-in-the-loop).

### 5. Dual-Loop Mechanism (README verbatim)

> "Demonstrating the Effectiveness of Dual-Loop Mechanism" — outer loop (planning) + inner loop (task execution), with `inner_loop_search_algorithms/` implementing action search.

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Dispatcher, Planner, Actor, Reflect, Tool-agents have separate prompt modules
- [ ] Planner output schema is strictly specified (subtask name / goal / criticism / milestones)
- [ ] Human-in-the-loop role (`AskForHumanHelp`) is explicit

### 2. Workflow Completeness
- [ ] Dual-loop mechanism (plan generation → refinement → execution → reflection)
- [ ] In-order subtask traversal with recursive splitting on failure
- [ ] Running records capture task statuses and LLM I/O for replay

### 3. Prompt Consistency
- [ ] JSON subtask contract enforced across planner prompts
- [ ] Shared resource description (Internet / FileSystemEnv / Notebook / ShellEnv) reused
- [ ] Anti-redundancy rule against creating duplicate subtasks

### 4. Tool Modularity
- [ ] ToolServer isolates tools in a sandboxed Docker container
- [ ] Functions registered through `ai_functions/`
- [ ] Extensible: new tools/agents can be added

### 5. Observability
- [ ] System-level record (query, code statuses, errors, server behavior) per run
- [ ] Sensitive info stripped from records for safe sharing
- [ ] GUI + CLI interaction modes

### 6. Extensibility
- [ ] Provider/model configuration via `assets/config.yml`
- [ ] New agents and tools pluggable
- [ ] Upload-files support for task seeding

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Task decomposition**: run "generate a plan for a data-analysis task" and verify a valid subtask tree is produced.
2. **Human-in-the-loop**: trigger `AskForHumanHelp` and confirm the agent pauses for input.
3. **Sandbox execution**: verify File Editor / Python Notebook / Shell operations run inside ToolServer.

### Unit Tests
1. **Planner schema**: assert output JSON contains `subtask name`, `goal.goal`, `goal.criticism`, `milestones`.
2. **Dispatcher routing**: confirm the dispatcher instantiates the correct agent per subtask type.
3. **Reflect agent**: verify a failed subtask triggers plan refinement.

### Stress Tests
1. **Deep recursion**: force repeated failures and confirm recursive splitting terminates efficiently.
2. **Duplicate-subtask pressure**: verify the anti-redundancy rule prevents duplicate subtasks.
3. **Long tasks**: multi-hour tasks with many LLM calls under the record/replay system.

---

## Notes

- **License**: Apache-2.0 (verified via GitHub API `license.spdx_id = "apache-2.0"`). Verbatim quotation is permitted.
- **Scope**: XAgent is a general-purpose assistant applicable to end-user tasks; it is not a code-review or IDE tool. The README explicitly labels it "experimental", which should be weighed when using it as a baseline.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long prompts are excerpted.
