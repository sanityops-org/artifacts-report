# agent-suite 测试用例「可直接运行逻辑工件」统计

> 统计范围：本目录下全部 51 个测试用例（TC-004 ~ TC-107），以及第七节联网补充的 10 个用例（TC-108 ~ TC-117）
> 分析日期：2026-10-21
> 统计对象：仅测试用例文件中**实际出现、且可直接加载运行**的文本，不追溯原始仓库、不检查后端程序

---

## 一、统计口径

**只有能直接运行起来的，才被算作工件并计入数字。**

| 处理方式 | 内容 |
|---|---|
| **计入统计** | 可直接作为 system message 加载的完整 Prompt；带 `name` + `description` frontmatter 且正文完整的 SKILL.md；符合 OpenAI / Anthropic / MCP 结构的完整 Tool Schema |
| **不计入任何数字** | 摘要、节选、被 `...` / `[...]` 截断的文本；只有名称或一句话职责的清单；缺 frontmatter 的 skill；Python 装饰器、Zod/TypeBox、LangChain `Tool(...)` 等非标准工具定义；后端代码、配置、状态定义 |

说明：

- 本报告**没有"候选工件"这一层**。不能运行的内容不是工件，只在"未达标原因"里用文字说明，不参与计数。
- 因此每个用例只有两个结果：**有可直接运行工件**，或**没有**。
- 汇总数字 = 可直接运行工件的数量，不代表文件中出现过多少段文字。

### 判定标准

| 类型 | 可直接运行的标准 |
|---|---|
| **System Prompt** | 角色 + 任务 + 约束/输出格式齐全，可整段粘贴为 system message；模板变量 `{context}`、`{{query}}` 可接受，`...` 省略不可接受 |
| **Skill** | `---` frontmatter 同时含 `name` 与 `description`，正文含完整可执行指令，可直接放入 `skills/<name>/SKILL.md` |
| **Tool Schema** | 单个工具定义，且为以下三种结构之一，参数体含 `type: object`、`properties`、`required` |

```json
// (a) OpenAI function calling
{"type":"function","function":{"name":"...","description":"...","parameters":{"type":"object","properties":{},"required":[]}}}
// (b) Anthropic tools
{"name":"...","description":"...","input_schema":{"type":"object","properties":{},"required":[]}}
// (c) MCP tools
{"name":"...","description":"...","inputSchema":{"type":"object","properties":{},"required":[]}}
```

---

## 二、总体结果

| 指标 | 数值 |
|---|---:|
| 用例总数 | 51 |
| **可直接运行工件总数** | **74** |
| — System Prompt | 33 |
| — Skill | 41 |
| — Tool Schema | 0 |
| 有可运行工件的用例 | 27（52.9%） |
| 无可运行工件的用例 | 24（47.1%） |

**结论：**

1. **Tool Schema 可直接运行的为 0 个**。所有工具要么是 Python 装饰器、TypeBox/Zod 源码、LangChain `Tool(...)`，要么只是名称/注册表，没有任何一个能直接注册给模型调用。
2. **Skill 是唯一可批量直接运行的类型**：41 个，全部具备标准 frontmatter。
3. **System Prompt 只有 33 个可运行**：大量用例给的是摘要、节选或截断文本。
4. 51 个用例中近一半（24 个）**一个可运行工件都没有**。

---

## 三、逐用例结果

> P = System Prompt，S = Skill，T = Tool Schema；数字均为**可直接运行**的数量，0 即没有。

| 用例 | 项目 | P | S | T | 合计 | 结果 | 未达标原因 | 可直接运行工件 |
|---|---|---|---:|---:|---:|---|---|---|
| [TC-004](TC-004-gpt-researcher-multi-agent-suite.md) | gpt-researcher | 0 | 0 | 0 | 0 | 无 | 8 段 prompt 为文档摘要；工具无 JSON Schema | — |
| [TC-005](TC-005-openclaw-file-based-agents.md) | OpenClaw | 0 | 0 | 0 | 0 | 无 | frontmatter 缺 name/description；正文是模板 | — |
| [TC-006](TC-006-agency-agents-marketing-suite.md) | agency-agents | 0 | 6 | 0 | 6 | 有 | — | content-creator 等 6 个角色定义 |
| [TC-007](TC-007-openclaw-three-layer-suite.md) | OpenClaw 三层 | 0 | 1 | 0 | 1 | 有 | SOUL 仅人格边界；工具为 TypeBox 源码 | browser-automation |
| [TC-031](TC-031-nanobot-file-based-agents.md) | nanobot | 0 | 4 | 0 | 4 | 有 | 提示均为 Jinja 片段；工具为 Python DSL | memory / github / cron / weather |
| [TC-032](TC-032-hermes-agent-file-based-agents.md) | hermes-agent | 0 | 4 | 0 | 4 | 有 | SOUL 仅文风；AGENTS 为开发文档 | computer-use / notion / obsidian / excalidraw |
| [TC-033](TC-033-openagent-file-based-agents.md) | openagent | 0 | 5 | 0 | 5 | 有 | 无 prompt/工具层 | github / coding-agent / notion / weather / obsidian |
| [TC-034](TC-034-mem0-file-based-agents.md) | mem0 | 0 | 6 | 0 | 6 | 有 | TS 常量仅为工具描述 | remember / search / forget / pause / resume / status |
| [TC-035](TC-035-autogpt-classic-autonomous-agent.md) | AutoGPT Classic | 0 | 0 | 0 | 0 | 无 | 模板片段含 `{constraints}` 等占位，缺角色 | — |
| [TC-036](TC-036-openmanus-general-agent.md) | OpenManus | 0 | 0 | 0 | 0 | 无 | 缺输出格式；含 `{directory}` 占位 | — |
| [TC-037](TC-037-babyagi-task-driven-agent.md) | BabyAGI | 0 | 0 | 0 | 0 | 无 | 全文为框架代码与目录树 | — |
| [TC-038](TC-038-anythingllm-agent-rag-suite.md) | AnythingLLM | 0 | 0 | 0 | 0 | 无 | 仅一句角色；工具为 Aibitat 自定义包装 | — |
| [TC-039](TC-039-wrenai-genbi-suite.md) | WrenAI GenBI | 0 | 1 | 0 | 1 | 有 | AGENTS.md 无 frontmatter，仅指针 | genbi |
| [TC-040](TC-040-leon-personal-assistant.md) | Leon | 0 | 0 | 0 | 0 | 无 | 模板正文被 `...` 截断 | — |
| [TC-041](TC-041-buzz-hive-mind-platform.md) | Buzz | 0 | 1 | 0 | 1 | 有 | AGENTS.md 为贡献指南，无 frontmatter | desktop-screenshot |
| [TC-042](TC-042-openamer-self-improving-agent.md) | OpenAmer | 0 | 0 | 0 | 0 | 无 | 均为运行时拼装片段，无角色/任务 | — |
| [TC-055](TC-055-ai-marketing-claude-file-based-agents.md) | ai-marketing-claude | 0 | 0 | 0 | 0 | 无 | 两段 SKILL.md 均无 YAML frontmatter | — |
| [TC-056](TC-056-claude-blog-file-based-agents.md) | claude-blog | 0 | 2 | 0 | 2 | 有 | — | blog / blog-write |
| [TC-057](TC-057-baoyu-skills-file-based-agents.md) | baoyu-skills | 0 | 2 | 0 | 2 | 有 | — | baoyu-cover-image / baoyu-post-to-wechat |
| [TC-058](TC-058-i18nstack-file-based-agents.md) | i18nstack | 0 | 2 | 0 | 2 | 有 | — | i18nstack / localize-ja |
| [TC-059](TC-059-writing-agent-file-based-agents.md) | writing-agent | 0 | 2 | 0 | 2 | 有 | — | workflow-producer / style-modeler |
| [TC-060](TC-060-cowagent-general-assistant.md) | CowAgent | 0 | 0 | 0 | 0 | 无 | Python 拼接片段；仅工具基类契约 | — |
| [TC-061](TC-061-homebot-voice-assistant.md) | homebot | 0 | 0 | 0 | 0 | 无 | 英文摘要转述，无 frontmatter | — |
| [TC-062](TC-062-smartflat-ai-property-advisor.md) | smartflat-ai | 0 | 0 | 0 | 0 | 无 | 占位模板；`@tool` 无入参 Schema | — |
| [TC-063](TC-063-claude-gym-coach-file-based-agents.md) | Claude Gym Coach | 0 | 0 | 0 | 0 | 无 | 正文为分节引用节选，非完整 SKILL.md | — |
| [TC-064](TC-064-anthropic-customer-support-agent.md) | Anthropic 客服 | 1 | 0 | 0 | 1 | 有 | 工具侧仅 Zod/分类清单 | 客服 system prompt |
| [TC-065](TC-065-microsoft-ufo-office-agent.md) | Microsoft UFO | 2 | 0 | 0 | 2 | 有 | `{apis}` 为占位；无工具入参 Schema | filter.yaml 判定 / prefill.yaml 规划 |
| [TC-066](TC-066-finrobot-financial-agents.md) | FinRobot | 3 | 0 | 0 | 3 | 有 | `.md` 无 frontmatter，只能作 Prompt | analysis_agent / report_agent / bull_agent |
| [TC-067](TC-067-chatwoot-captain-support-agent.md) | Chatwoot Captain | 1 | 0 | 0 | 1 | 有 | tools.yml 仅 id/描述，无 parameters | assistant.liquid |
| [TC-068](TC-068-onyx-enterprise-assistant.md) | Onyx | 0 | 1 | 0 | 1 | 有 | — | feature-map |
| [TC-069](TC-069-agentfactory-business-plugins.md) | AgentFactory | 0 | 3 | 0 | 3 | 有 | — | task-intelligence / workplace-search / chief-of-staff |
| [TC-070](TC-070-claude-skills-business-roles.md) | claude-skills | 0 | 1 | 0 | 1 | 有 | 另 2 份正文为 abridged/摘要 | cs-financial-analyst |
| [TC-071](TC-071-fabric-pattern-library.md) | Fabric | 4 | 0 | 0 | 4 | 有 | — | analyze_bill / summarize / extract_wisdom / create_prd |
| [TC-084](TC-084-tradingagents-multi-agent-suite.md) | TradingAgents | 0 | 0 | 0 | 0 | 无 | 9 条 prompt 均被 `[...]` 截断 | — |
| [TC-090](TC-090-finrobot-multi-agent-suite.md) | FinRobot 多智能体 | 1 | 0 | 0 | 1 | 有 | 另 5 个为占位骨架或职责概述 | leader_system_message |
| [TC-091](TC-091-mobileagent-multi-agent-suite.md) | Mobile-Agent-v2 | 1 | 0 | 0 | 1 | 有 | 其余提示截断或仅一句角色 | init_action_chat |
| [TC-092](TC-092-openai-customer-service-multi-agent-suite.md) | OpenAI 客服 Demo | 6 | 0 | 0 | 6 | 有 | 2 条指令截断；工具为 `@function_tool` | Seat / Refunds / FAQ / Triage + 2 条 Guardrail |
| [TC-094](TC-094-ai-hedge-fund-multi-agent-suite.md) | AI Hedge Fund | 3 | 0 | 0 | 3 | 有 | — | Buffett / Graham / Druckenmiller |
| [TC-095](TC-095-customer-service-ai-agent-multi-agent-suite.md) | 客服多智能体 | 5 | 0 | 0 | 5 | 有 | — | 综合/账单/投诉/产品/技术支持 5 个模板 |
| [TC-096](TC-096-multi-agent-medical-assistant-multi-agent-suite.md) | 医疗助手 | 1 | 0 | 0 | 1 | 有 | — | RAG Agent prompt |
| [TC-097](TC-097-lavern-multi-agent-suite.md) | Lavern | 0 | 0 | 0 | 0 | 无 | 两段提示含 `...` 截断；工具仅名称 | — |
| [TC-098](TC-098-travel-planner-multi-agent-suite.md) | Travel Planner | 0 | 0 | 0 | 0 | 无 | flights.md 正文含 `...` 截断 | — |
| [TC-099](TC-099-e-commerce-agents-multi-agent-suite.md) | E-Commerce Agents | 0 | 0 | 0 | 0 | 无 | YAML base 多处 `...` 截断 | — |
| [TC-100](TC-100-salesgpt-agent-suite.md) | SalesGPT | 0 | 0 | 0 | 0 | 无 | 三段提示截断；Tool 无参数 Schema | — |
| [TC-101](TC-101-kotaemon-agent-suite.md) | kotaemon | 5 | 0 | 0 | 5 | 有 | — | QA_TEXT/TABLE/CHATBOT/FIGURE、REWRITE |
| [TC-102](TC-102-vane-agent-suite.md) | Vane | 0 | 0 | 0 | 0 | 无 | 两模式提示均 `...` 截断 | — |
| [TC-103](TC-103-morphic-agent-suite.md) | Morphic | 0 | 0 | 0 | 0 | 无 | Quick 模式提示截断 | — |
| [TC-104](TC-104-xagent-agent-suite.md) | XAgent | 0 | 0 | 0 | 0 | 无 | Planner `SYSTEM_PROMPT` 截断 | — |
| [TC-105](TC-105-open-notebook-agent-suite.md) | Open Notebook | 0 | 0 | 0 | 0 | 无 | Jinja 模板 + `...` 截断 | — |
| [TC-106](TC-106-private-gpt-agent-suite.md) | PrivateGPT | 0 | 0 | 0 | 0 | 无 | 仅能力表、目录清单与 Python 函数 | — |
| [TC-107](TC-107-chat-ui-agent-suite.md) | Chat UI | 0 | 0 | 0 | 0 | 无 | 仅 TS 构建函数、env 配置与路由说明 | — |

**核对**：P 列合计 33，S 列合计 41，T 列合计 0，总数 74；"有"27 个，"无"24 个，共 51 个。

---

## 四、结果分布

### 4.1 有可直接运行工件的用例（27 个）

- **只有 Skill 可运行（15 个）**：TC-006、TC-007、TC-031、TC-032、TC-033、TC-034、TC-039、TC-041、TC-056、TC-057、TC-058、TC-059、TC-068、TC-069、TC-070。
- **只有 Prompt 可运行（12 个）**：TC-064、TC-065、TC-066、TC-067、TC-071、TC-090、TC-091、TC-092、TC-094、TC-095、TC-096、TC-101。
- **没有任何用例同时具备可运行的 Prompt、Skill 与 Tool Schema**，也没有任何用例存在可运行的 Tool Schema。

### 4.2 无可直接运行工件的用例（24 个）

| 类型 | 用例 | 共同特征 |
|---|---|---|
| 摘要 / 节选 / 截断 | TC-004、TC-084、TC-097、TC-098、TC-099、TC-100、TC-102、TC-103、TC-104、TC-105、TC-040、TC-042 | 正文自带 `...`、`[...]`、"verbatim excerpt"，无法拼回可加载文本 |
| 缺标准头部 | TC-005、TC-055、TC-061、TC-063 | skill 缺 `name`/`description` frontmatter，或正文不是完整文件 |
| 只有后端代码 / 配置 | TC-035、TC-036、TC-037、TC-038、TC-060、TC-062、TC-106、TC-107 | 类、函数、env、目录树，不构成三类工件 |

### 4.3 Tool Schema 为什么一个都不能用

| 形式 | 涉及用例 | 缺失点 |
|---|---|---|
| Python 装饰器 `@tool` / `@function_tool` | TC-084、TC-092、TC-062 | 无 JSON Schema，依赖运行时反射 |
| LangChain `Tool(name, func, description)` | TC-100 | 无 parameters |
| TypeBox / Zod 源码 | TC-007、TC-038、TC-064 | 是 TS 代码，不是 schema 文本 |
| 自定义 `{"tools":[...]}` 集合 | TC-004 | 工具项无 `input_schema/parameters` |
| `id/title/description/icon` 注册表 | TC-067 | 无参数定义 |
| 仅工具名清单 | TC-031、TC-097~TC-099、TC-102~TC-104 | 连定义都不存在 |

---

## 五、典型样例

### 5.1 可直接运行（正例）

- [TC-056](TC-056-claude-blog-file-based-agents.md#L85-L137)：`skills/blog/SKILL.md`，frontmatter 含 `name: blog` 与多行 `description`，正文有硬性质量门与评分阈值。
- [TC-071](TC-071-fabric-pattern-library.md#L34-L133)：4 个 pattern 均为 `IDENTITY / STEPS / OUTPUT / INPUT` 全文，可直接作为 system message。
- [TC-094](TC-094-ai-hedge-fund-multi-agent-suite.md#L53-L181)：角色 + 检查清单 + signal 规则 + JSON 输出 Schema。
- [TC-101](TC-101-kotaemon-agent-suite.md#L40-L97)：5 段完整指令模板，`{context}` 仅为模板变量。
- [TC-006](TC-006-agency-agents-marketing-suite.md#L28-L34)：frontmatter 含 `name` + `description`，正文为完整工作契约。

### 5.2 不能运行（反例）

- [TC-004](TC-004-gpt-researcher-multi-agent-suite.md#L36-L230)：8 段 `system_message` 实为文档摘要，无输出契约。
- [TC-004](TC-004-gpt-researcher-multi-agent-suite.md#L236-L304)：`"parameters": {"content":"string"}` 是属性简写，不是 JSON Schema。
- [TC-067](TC-067-chatwoot-captain-support-agent.md#L135-L170)：7 个工具只有 `id/title/description/icon`，模型无法生成调用参数。
- [TC-063](TC-063-claude-gym-coach-file-based-agents.md#L42-L141)：frontmatter 完整但正文按 § 分节引用，缺段无法部署。
- [TC-105](TC-105-open-notebook-agent-suite.md#L39-L91)：Jinja 模板中多处 `...`，未渲染也无法复原。
- [TC-037](TC-037-babyagi-task-driven-agent.md#L31-L151)：通篇 Python 框架代码，无三类工件。

---

## 六、说明

1. 本报告只回答一个问题：**这个用例里有没有能直接加载运行的工件，有几个**。不评价业务逻辑、提示词质量或 Agent 设计。
2. 计数以测试用例文件中**实际粘贴的文本**为准；文件未取到正文、只提到文件名的不算有工件。
3. 模板变量（`{context}`、`{{query}}`）不影响运行，计为可运行；`...`、"abridged"、"excerpt" 属于信息缺失，不计。
4. 节选型 Skill（TC-063、TC-070、TC-098）按"不可直接运行"处理；若补回原文全文，数字会上升。

---

## 七、联网补充：10 个含可直接运行 Tool Schema 的 Agent Suite

> 查询时间：2026-10-21；编号 TC-108 ~ TC-117
> 入选条件：**至少含 1 个可直接运行的 Tool Schema**（这是与前面 51 个用例最大的差别）
> 分析方式：GitHub 目录树定位 + `raw.githubusercontent.com` 原文核验，不运行后端

### 7.1 补充口径

在原有标准上明确四种可直接注册的 Tool Schema 形态：

1. OpenAI Chat Completions：`{"type":"function","function":{"name","description","parameters"}}`
2. OpenAI Responses：`{"type":"function","name","description","parameters"}`
3. Anthropic：`{"name","description","input_schema"}`
4. MCP：`{"name","description","inputSchema"}`，以及官方 MCP Python SDK 的字面构造 `types.Tool(name=..., description=..., inputSchema={...})`

仍排除：`@tool` / `@mcp.tool()` 装饰器、Pydantic/Zod/TypeBox、函数签名反射、schema 值来自变量引用。
计数规则：**同一套件内同名工具只计一次**；Prompt 与 Skill 同样去重。

### 7.2 逐用例结果

| 编号 | 套件 / 仓库 | 分析范围 | P | S | T | 合计 | 典型可运行工件 |
|---|---|---|---:|---:|---:|---:|---|
| TC-108 | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | `claude_agent_sdk/site_reliability_agent/` | 2 | 0 | 19 | 21 | 12 个基础 MCP 工具 + 7 个 PagerDuty/Confluence 工具；2 条 SRE 系统提示 |
| TC-109 | [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | `04-tool-use/` + `.agents/skills/` | 1 | 6 | 1 | 8 | `get_current_time`（OpenAI）；6 个课程 Skill；TravelAgent 提示 |
| TC-110 | [kortix-ai/suna](https://github.com/kortix-ai/suna) | `SUNA-LEGACY-cutoff` 分支 `backend/core/` | 2 | 0 | 1 | 3 | `calculate`（OpenAI）；CORE_SYSTEM_PROMPT；记忆抽取提示 |
| TC-111 | [ed-donner/agents](https://github.com/ed-donner/agents) | `1_foundations` 数字孪生 Agent | 2 | 2 | 3 | 7 | `record_user_details` / `record_unknown_question` / `search_faq`（Anthropic） |
| TC-112 | [CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext) | `tool_definitions.py` + `prompts.py` + `.cursor/skills/` | 1 | 1 | 13 | 15 | 13 个 MCP 工具（check_job_status 等）；代码图谱系统提示 |
| TC-113 | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | `s01_agent_loop` ~ `s17_goal_loop` | 22 | 4 | 28 | 54 | 28 个去重后的 Anthropic 工具（bash/read_file/task 等）；17 章 Agent 提示 |
| TC-114 | [YaoApp/yao](https://github.com/YaoApp/yao) | `tools/` + `yao/assistants/` | 14 | 15 | 53 | 82 | 53 个 `*_schema.json`（MCP）；15 个 SKILL.md；14 条 prompts.yml |
| TC-115 | [awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples) | `device-management-agent` | 1 | 0 | 7 | 8 | 7 个 inlinePayload MCP 工具（list_devices 等） |
| TC-116 | [Klavis-AI/klavis](https://github.com/Klavis-AI/klavis) | `mcp_servers/context7` + `mcp_servers/exa` | 2 | 1 | 5 | 8 | `exa_search` 等 5 个 MCP 工具；documentation-lookup Skill |
| TC-117 | [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) | `app/backend/approaches/` | 2 | 0 | 1 | 3 | `search_sources`（OpenAI Responses）；chat_answer / query_rewrite 系统提示 |

### 7.3 汇总

| 类型 | 数量 |
|---|---:|
| 可运行 System Prompt | 49 |
| 可运行 Skill | 29 |
| 可运行 Tool Schema | **131** |
| **合计** | **209** |

- 10 个用例**全部**含可直接运行的 Tool Schema（10/10）。
- 与前面 51 个用例（Tool Schema 0 个）对比，差距不在"有没有工具"，而在**是否以字面 schema 形式交付**。

### 7.4 结果解读

1. **Tool Schema 可运行的项目，都是字面量/配置驱动**：Yao（53）、learn-claude-code（28）、claude-cookbooks（19）、CodeGraphContext（13）、agentcore（7）。
2. **SDK 生成派仍然是 0**：codex、continue、mcp-for-beginners、IBM watsonx ADK 都用装饰器或类型反射，schema 在运行时才存在，无法直接复制上线。
3. **Prompt / Skill / Tool 往往不同源**：claude-cookbooks 有 19 个工具但没有 SKILL.md；lobehub 有 54 个 Skill 但没有可运行工具。
4. 工具数量不等于可复用度：`learn-claude-code` 原始出现 142 次工具定义，按名称去重后只有 28 个。

### 7.5 曾核验但未入选（Tool Schema 为 0）

| 仓库 | 可运行 P / S | Tool Schema 为 0 的原因 |
|---|---|---|
| microsoft/mcp-for-beginners | 0 / 0 | `@mcp.tool()` 装饰器生成 schema；prompt 仅一句 |
| IBM/ibm-watsonx-orchestrate-adk | 2 / 1 | `@tool` + Pydantic 或 OpenAPI YAML，无字面 JSON |
| lobehub/lobehub | 0 / 54 | `input_schema` 由 TS/Zod 运行时拼装 |
| camel-ai/camel | 1 / 3 | `@tool()` / FunctionTool 从函数签名生成 |
| continuedev/continue | 3 / 2 | 工具 `name` 为枚举引用，对象含函数值，不可序列化 |
| openai/codex | 10 / 5 | `ResponsesApiTool` + `JsonSchema` 运行时构造，无字面 schema |

### 7.6 关键证据

- TC-108：[sre_mcp_server.py](https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/claude_agent_sdk/site_reliability_agent/sre_mcp_server.py)（`TOOLS` 列表，L58–371）
- TC-109：[04-tool-use/README.md](https://raw.githubusercontent.com/microsoft/ai-agents-for-beginners/main/04-tool-use/README.md)（`get_current_time`，L86–104）
- TC-110：[agentpress/example/agent.py](https://raw.githubusercontent.com/kortix-ai/suna/SUNA-LEGACY-cutoff/backend/core/agentpress/example/agent.py)（`calculate`）
- TC-111：[modules/tools.py](https://raw.githubusercontent.com/ed-donner/agents/main/1_foundations/community_contributions/claude_based_chatbot_tc/modules/tools.py)（3 个 Anthropic 工具）
- TC-112：[tool_definitions.py](https://raw.githubusercontent.com/CodeGraphContext/CodeGraphContext/main/src/codegraphcontext/tool_definitions.py)（13 个字面 MCP 工具）
- TC-113：[s15_integrated_harness/code.py](https://raw.githubusercontent.com/shareAI-lab/learn-claude-code/main/s15_integrated_harness/code.py)（`BUILTIN_TOOLS`）
- TC-114：[tools/agent/call_schema.json](https://raw.githubusercontent.com/YaoApp/yao/main/tools/agent/call_schema.json)（MCP schema）
- TC-115：[gateway/device-management-target.py](https://raw.githubusercontent.com/awslabs/agentcore-samples/main/02-use-cases/01-conversational-agents/device-management-agent/gateway/device-management-target.py)（L74–171）
- TC-116：[mcp_servers/exa/server.py](https://raw.githubusercontent.com/Klavis-AI/klavis/main/mcp_servers/exa/server.py)（5 个 `types.Tool`）
- TC-117：[chat_query_rewrite_tools.json](https://raw.githubusercontent.com/Azure-Samples/azure-search-openai-demo/main/app/backend/approaches/prompts/chat_query_rewrite_tools.json)
