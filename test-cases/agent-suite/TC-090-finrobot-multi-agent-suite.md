# TC-090: FinRobot - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: AI4Finance-Foundation/FinRobot (the AutoGen generation, known as V0)
- **GitHub URL**: https://github.com/AI4Finance-Foundation/FinRobot
- **License**: Apache-2.0 (stated in the repository README; the V0 code shown here lives under `finrobot_autogen/`)
- **Artifact Type**: Multi-Agent suite (role library + leader/role prompt templates + GroupChat / leader-based orchestration)
- **Collection Date**: 2026-10-13
- **Collection Method**: Direct raw-file fetches of the public source. Exact URLs used:
  - https://raw.githubusercontent.com/AI4Finance-Foundation/FinRobot/master/finrobot_autogen/finrobot/agents/prompts.py
  - https://raw.githubusercontent.com/AI4Finance-Foundation/FinRobot/master/finrobot_autogen/finrobot/agents/agent_library.py
  - https://raw.githubusercontent.com/AI4Finance-Foundation/FinRobot/master/finrobot_autogen/finrobot/agents/workflow.py
  - https://github.com/AI4Finance-Foundation/FinRobot (README, for overview and license)

> **Note on uncertainty / repository shape**: FinRobot has been reorganised into three sub-projects (`finrobot_autogen/` = V0, `finrobot_equity/` = V1, `finrobot_desktop/` = V2). The classic multi-agent library shown below is the **V0 AutoGen generation**, which is the codebase behind the FinRobot whitepaper. The default branch is `master`, and the V0 package was moved into the `finrobot_autogen/` directory (the import name `finrobot` is unchanged).

---

## Project Overview

FinRobot (V0) is an open-source **agentic AI framework for financial analysis** built on Microsoft AutoGen. Instead of a single financial assistant, it ships a **role library** of specialised financial agents and two concrete multi-agent topologies (a peer GroupChat and a hierarchical leader-based workflow). It therefore represents an **end-user financial-analysis application** (equity research, report generation, market/fundamental analysis) rather than a developer toolchain.

### Agent Roles (from `agent_library.py`)

| Role (`name`) | Responsibility | Toolkits attached |
|------|------|-------------|
| **Software_Developer** | Collaborative coding for tasks assigned by a leader/colleague | none |
| **Data_Analyst** | Data analysis using Python, group-chat problem solving | none |
| **Programmer** | Python programming within a group chat | none |
| **Accountant** | Accounting principles + limited Python coding | none |
| **Statistician** | Statistics / mathematics + Python data analysis | none |
| **IT_Specialist** | IT problem-solving within a group chat | none |
| **Artificial_Intelligence_Engineer** | Python + collaborative problem solving | none |
| **Financial_Analyst** | Analytical / problem-solving for financial data | none |
| **Market_Analyst** | Collect & aggregate financial information per client requirement | `FinnHubUtils.get_company_profile`, `FinnHubUtils.get_company_news`, `FinnHubUtils.get_basic_financials`, `YFinanceUtils.get_stock_data` |
| **Expert_Investor** | Generation of customised financial analysis reports (annual report) | `FMPUtils.get_sec_report`, `IPythonUtils.display_image`, `TextUtils.check_text_length`, `ReportLabUtils.build_annual_report`, `ReportAnalysisUtils`, `ReportChartUtils` |

### Orchestration topologies (from `workflow.py`)

- **`MultiAssistant`** — a peer **GroupChat**; all agents cooperate in one shared conversation space with a custom speaker-selection function.
- **`MultiAssistantWithLeader`** — a **hub-and-spoke** topology where a single leader agent issues orders to subordinates through AutoGen nested chats.
- A `User_Proxy` (AutoGen `UserProxyAgent`) executes code and terminates the loop when an agent emits `TERMINATE`.

---

## Logical Artifact Inventory

### 1. System Prompt Templates (3)

Verbatim from `finrobot_autogen/finrobot/agents/prompts.py`:

#### 1.1 Leader system message
```python
leader_system_message = dedent(
    """
    You are the leader of the following group members:

    {group_desc}

    As a group leader, you are responsible for coordinating the team's efforts to achieve the project's objectives. You must ensure that the team is working together effectively and efficiently.
    - Summarize the status of the whole project progess each time you respond.
    - End your response with an order to one of your team members to progress the project, if the objective has not been achieved yet.
    - Orders should be follow the format: \"[<name of staff>] <order>\".
    - Orders need to be detailed, including necessary time period information, stock information or instruction from higher level leaders.
    - Make only one order at a time.
    - After receiving feedback from a team member, check the results of the task, and make sure it has been well completed before proceding to th next order.
    Reply "TERMINATE" in the end when everything is done.
    """
)
```

#### 1.2 Role (subordinate) system message
```python
role_system_message = dedent(
    """
    As a {title}, your reponsibilities are as follows:
    {responsibilities}
    Reply "TERMINATE" in the end when everything is done.
    """
)
```

#### 1.3 Order template (used inside nested chats)
```python
order_template = dedent(
    """
    Follow leader's order and complete the following task with your group members:
    {order}
    For coding tasks, provide python scripts and executor will run it for you.
    Save your results or any intermediate data locally and let group leader know how to read them.
    DO NOT include "TERMINATE" in your response until you have received the results from the execution of the Python scripts.
    If the task cannot be done currently or need assistance from other members, report the reasons or requirements to group leader ended with TERMINATE.
"""
)
```

### 2. Role / Agent Definitions (verbatim from `agent_library.py`, 3 representative excerpts)

The library is edited as a Python list here in the document for readability; in the source it is a Python list literal (`library = [ {...}, {...} ]`), later converted to a dict (`library = {d["name"]: d for d in library}`).

#### 2.1 `Data_Analyst`
```python
{
    "name": "Data_Analyst",
    "profile": "As a Data Analyst for this position, you must be adept at analyzing data using Python, completing tasks assigned by leaders or colleagues, and collaboratively solving problems in a group chat setting with professionals of various roles. Reply 'TERMINATE' when everything is done.",
}
```

#### 2.2 `Market_Analyst` (role with tools)
```python
{
    "name": "Market_Analyst",
    "profile": "As a Market Analyst, one must possess strong analytical and problem-solving abilities, collect necessary financial information and aggregate them based on client's requirement. For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    "toolkits": [
        FinnHubUtils.get_company_profile,
        FinnHubUtils.get_company_news,
        FinnHubUtils.get_basic_financials,
        YFinanceUtils.get_stock_data,
    ],
}
```

#### 2.3 `Expert_Investor` (longest, report-producing role)
```python
{
    "name": "Expert_Investor",
    "profile": dedent(
        f"""
        Role: Expert Investor
        Department: Finance
        Primary Responsibility: Generation of Customized Financial Analysis Reports
        Role Description:
        As an Expert Investor within the finance domain, your expertise is harnessed to develop bespoke Financial Analysis Reports ... Engaging directly with clients to gather essential information and continuously refining the report with their feedback ensures the final product precisely meets their needs and expectations.
        Key Objectives:
        Analytical Precision: ...
        Effective Communication: ...
        Client Focus: ...
        Adherence to Excellence: ...
        Performance Indicators:
        ...
        Reply TERMINATE when everything is settled.
        """
    ),
    "toolkits": [
        FMPUtils.get_sec_report,  # Retrieve SEC report url and filing date
        IPythonUtils.display_image,  # Display image in IPython
        TextUtils.check_text_length,  # Check text length
        ReportLabUtils.build_annual_report,  # Build annual report in designed pdf format
        ReportAnalysisUtils,  # Expert Knowledge for Report Analysis
        ReportChartUtils,  # Expert Knowledge for Report Chart Plotting
    ],
}
```

### 3. Orchestration / Config Artifacts (verbatim from `workflow.py`)

#### 3.1 The `FinRobot` agent class — profile assembly in `_preprocess_config`
```python
def _preprocess_config(self, config):
    role_prompt, leader_prompt, responsibilities = "", "", ""
    if "responsibilities" in config:
        title = config["title"] if "title" in config else config.get("name", "")
        if "name" not in config:
            config["name"] = config["title"]
        responsibilities = config["responsibilities"]
        responsibilities = (
            "\n".join([f" - {r}" for r in responsibilities])
            if isinstance(responsibilities, list)
            else responsibilities
        )
        role_prompt = role_system_message.format(
            title=title,
            responsibilities=responsibilities,
        )
    name = config.get("name", "")
    description = (
        f"Name: {name}\nResponsibility:\n{responsibilities}"
        if responsibilities
        else f"Name: {name}"
    )
    config["description"] = description.strip()
    if "group_desc" in config:
        group_desc = config["group_desc"]
        leader_prompt = leader_system_message.format(group_desc=group_desc)
    config["profile"] = (
        (role_prompt + "\n\n").strip()
        + (leader_prompt + "\n\n").strip()
        + config.get("profile", "")
    ).strip()
    return config
```

#### 3.2 Group-chat speaker-selection function (`MultiAssistant._get_representative`)
```python
def custom_speaker_selection_func(
    last_speaker: autogen.Agent, groupchat: autogen.GroupChat
):
    messages = groupchat.messages
    if len(messages) <= 1:
        return groupchat.agents[0]
    if last_speaker is self.user_proxy:
        return groupchat.agent_by_name(messages[-2]["name"])
    elif "tool_calls" in messages[-1] or messages[-1]["content"].endswith(
        "TERMINATE"
    ):
        return self.user_proxy
    else:
        return groupchat.next_agent(last_speaker, groupchat.agents[:-1])
```

#### 3.3 Leader-based group config contract (`MultiAssistantWithLeader` docstring)
```python
"""
Leader based Workflow with multiple agents connected to a leader agent through nested chats.
Group config has to follow the following structure:
{
    "leader": {
        "title": "Leader Title",
        "responsibilities": ["responsibility 1", "responsibility 2"]
    },
    "agents": [
        {
            "title": "Employee Title",
            "responsibilities": ["responsibility 1", "responsibility 2"]
        }, ...
    ]
}
"""
```

#### 3.4 Trigger / routing for subordinate orders
```python
for agent in self.agents:
    self.user_proxy.register_nested_chats(
        [
            {
                "sender": self.user_proxy,
                "recipient": agent,
                "message": partial(order_message, agent.name),
                "summary_method": "reflection_with_llm",
                "max_turns": 10,
                "max_consecutive_auto_reply": 3,
            }
        ],
        trigger=partial(
            order_trigger, name=leader.name, pattern=f"[{agent.name}]"
        ),
    )
```
The leader's order format (`[<name of staff>] <order>`) defined in the leader prompt is parsed by `order_trigger` / `order_message` in `finrobot/agents/utils.py` (referenced by `workflow.py`, not quoted here).

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Are the 10 library roles distinct, or do several (Software_Developer / Programmer / AI_Engineer) overlap significantly?
- [ ] Does each role's `profile` alone define positioning, or does it depend on leader/role templates concatenation?

### 2. Workflow Completeness
- [ ] Do both topologies (peer GroupChat + leader hierarchy) cover the financial analysis lifecycle?
- [ ] Is `TERMINATE` propagation (`is_termination_msg`) robust against agents that forget to emit it?

### 3. Prompt Consistency
- [ ] Terminology and `TERMINATE` convention consistent across roles and templates?
- [ ] `{title}` / `{responsibilities}` / `{group_desc}` placeholders filled deterministically?

### 4. Tool Schema Modularity
- [ ] Toolkits attached per-role via `toolkits` list; registration via `register_toolkits(self.toolkits, self, proxy)`.
- [ ] Are toolkit descriptions (from function docstrings) quality-controlled?

### 5. Observability
- [ ] Group chat messages / nested chat summaries available for tracing?
- [ ] No explicit state schema; state is implicit in AutoGen conversation history.

### 6. Extensibility
- [ ] Adding a new financial role = one dict entry in `library`.
- [ ] New tools = append to a role's `toolkits`.

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 20% | | |
| Prompt Consistency | 15% | | |
| Tool Schema Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Positive Tests
1. **Leader-based equity report**: run `MultiAssistantWithLeader` with a leader + `Market_Analyst` + `Expert_Investor` and verify the leader emits correctly formatted `[<name>] <order>`.
2. **Group-chat report generation**: run `MultiAssistant` and confirm the speaker-selection function round-robins and stops on `TERMINATE`.
3. **Tool-bound role**: verify `Market_Analyst` can call `FinnHubUtils.get_company_news` and that the result is consumed by `Expert_Investor`.

### Boundary Tests
1. **Single-member group**: group with only one agent (the `need_suffix` / duplicate-name path).
2. **Duplicate role names**: two agents with the same title → the `_init_agents` index-suffixing path (`{name}_{idx+1}`).
3. **Max turns**: leader task that exceeds `max_turns=10` in a nested chat.

### Negative Tests
1. **Unknown role**: instantiate `FinRobot("Non_Existent_Role")` → expect the `assert name in library` failure.
2. **Missing config**: `FinRobot(agent_config={})` → expect `assert agent_config` failure.
3. **Order with no matching subordinate**: leader emits `[Ghost_Agent] do X` → verify `order_trigger` does not fire.

---

## Notes

- FinRobot is licensed **Apache-2.0**; the README explicitly permits quotation and modification of the code and documents (the repository also carries a separate `TRADEMARK_POLICY.md`).
- All prompts, role profiles, and orchestration snippets above are **quoted verbatim** from the FinRobot source at the URLs listed in Metadata. Long profiles (`Expert_Investor`) are abbreviated with `...` to avoid pasting the whole file; no wording was altered.
- The `ReportAnalysisUtils` / `ReportChartUtils` toolkit entries are **Expert-Knowledge placeholders** (classes), not plain functions — a real ambiguity worth noting when inspecting tool-schema modularity.
