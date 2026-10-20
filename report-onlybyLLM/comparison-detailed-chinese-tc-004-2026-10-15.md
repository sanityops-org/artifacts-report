# TC-004 双源检查结果详细对比报告（中文·逐条版）

> 本报告由宿主模型生成，用于对同一工件（TC-004）的两类检查结果做**逐条、逐维度**对比。
> 其中"技能报告"为 `sanityops-inspect-lite` 规则包执行结果，**非官方 SanityOps 引擎结论**；本对比报告亦非官方引擎结论。完整权威检查请使用 `sanityops-cli`。
> 说明：本文件按用户明确要求以中文撰写（覆盖文件夹默认英文策略）。

---

## 0. 对比对象与数据来源

| 代号 | 文件 | 性质 | 产出方式 |
|------|------|------|----------|
| **A** | `test-cases/agent-suite/TC-004-gpt-researcher-multi-agent-suite.sanityops-skill-report.md` | 官方规则包检查报告（inspect-lite v1.0.0） | 规则 ID + PASS/FAIL/N/A + 证据引用，分阶段执行 |
| **B** | `report-onlybyLLM/` 下 6 份 LLM 报告（Claude Fable 5.1 / DeepSeek-V4-Pro / GLM-5 / GPT-5.6 Terra / Gemini 4 Argon / sonnet-5.5） | 自由式缺陷/权限/风险审计 | 叙事式 P0/P1/P2 清单 |
| 共同工件 | `TC-004-gpt-researcher-multi-agent-suite.md` | 8 角色系统提示词 + 3 组工具 Schema + 2 个配置工件 | — |

---

## 1. 总量与严重度对比

### 1.1 总量

| 指标 | A 技能报告 | B 六份 LLM 报告 |
|------|:----------:|:---------------:|
| 判定项总数 | 94（FAIL 53 / PASS 34 / N/A 7） | — |
| 缺陷/问题总数 | **53（FAIL）** | **127 条**（均值 21.2 / 份，范围 15~30） |
| P0 | **37（69.8%）** | 23（均值 3.83） |
| P1 | **11（20.8%）** | 61（均值 10.17） |
| P2 | **5（9.4%）** | 43（均值 7.17） |
| 显性风险条目 | **0（Stage E）** | 六份均设为一等类别 |

**结论：严重度分布相反。** A 因 Agent-L3 升级（P1→P0、P2→P1）而**近乎全 P0（70%）**；B 由分析者判断，**P0 仅约 18%**。

### 1.2 各份数量一览

| 报告 | 条目 | P0 | P1 | P2 | P0 占比 |
|------|:----:|:--:|:--:|:--:|:-------:|
| A 技能报告 | 53 | 37 | 11 | 5 | 69.8% |
| R1 Claude Fable 5.1 | 30 | 4 | 13 | 13 | 13.3% |
| R2 DeepSeek-V4-Pro | 19 | 3 | 9 | 7 | 15.8% |
| R3 GLM-5 | 25 | 5 | 14 | 6 | 20.0% |
| R4 GPT-5.6 Terra | 16 | 2 | 9 | 5 | 12.5% |
| R5 Gemini 4 Argon | 15 | 5 | 6 | 4 | 33.3% |
| R6 sonnet-5.5 | 22 | 4 | 10 | 8 | 18.2% |

### 1.3 A 报告内部结构

| 阶段 / 工件 | 判定项 | FAIL |
|-------------|:------:|:----:|
| A.1 系统提示词（L3） | 47 | 26 |
| A.2 `research_tools`（L1 只读） | 7 | 6 |
| A.3 `review_tools`（L1） | 7 | 5 |
| A.4 `publication_tools`（L2） | 12 | 8 |
| A.5 内嵌代码 QC | 13 | 2 |
| B 跨工件（`QD-PT` / `QD-CYC`） | 8 | 6 |
| **合计** | **94** | **53** |

- 阶段执行：A/B/C/E/F/G 已执行，**D（Permission）未执行**（Gate-0 的 G0-4 未满足）。
- Gate-0：**未通过**（G0-1/G0-2 为信息性；G0-4 未满足）。
- Stage E 显性风险：**0 条**（无自包含外泄、身份/权限声明、约束移除、危险标志、硬编码凭据、异常回调等显式表达）。

---

## 2. A 技能报告逐条明细（全 94 项）

> 说明：`判定`为 A 报告原始判定；`对应 B 主题`为与第 4 节 LLM 主题（T1~T24）的映射，"—"表示 B 未覆盖。

### 2.1 A.1 系统提示词（47 项）

| 规则 ID | 判定 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|-------------|:-----------:|
| QD-P-1.1.1 | PASS | 1.1-1.8 无互斥属性 | — |
| QD-P-1.1.2 | PASS | task.json guidelines 三者不冲突 | — |
| QD-P-1.1.3 | **FAIL** | 1.4 Reviewer 示例 `overall_score:7` + `needs_revision` 与"score<7"规则冲突 | T8 |
| QD-P-1.2.1 | PASS | 1.1-1.8 角色身份与职责相符 | — |
| QD-P-1.2.2 | PASS | 无输出风格错配 | — |
| QD-P-1.2.3 | PASS | 约束未禁止核心职责 | — |
| QD-P-1.3.1 | PASS | 1.3 "minimum 5 per section" 有界 | — |
| QD-P-1.3.2 | **FAIL** | 1.4 "Be thorough but constructive" 模糊限定 | — |
| QD-P-1.3.3 | **FAIL** | 1.1-1.8 无禁止范围/交接条件 | — |
| QD-P-1.4.1 | PASS | 无重复约束 | — |
| QD-P-1.4.2 | PASS | 1.8 交互模式可达 | — |
| QD-P-1.4.3 | PASS | 非 Skill 定义（空真） | — |
| QD-P-1.5.1 | PASS | 职责支撑目标 | — |
| QD-P-1.5.2 | **FAIL** | 1.1 列工具 `init_research/plan_sections/run_research/review_draft/compile_report` 无资源定义 | T5 |
| QD-P-1.6.1 | **FAIL** | 1.1 "Handle errors ... gracefully" 关键决策标准未定义 | T20 |
| QD-P-1.6.2 | **FAIL** | 1.5 "Re-submit for re-review if major changes" 依赖不可观测判断 | T4 |
| QD-P-1.6.3 | **FAIL** | 1.6 "consistent terminology" 与 "smooth transitions" 无仲裁 | — |
| QD-P-1.6.4 | PASS | 无内部推理方法约束 | — |
| QD-P-1.6.5 | PASS | 无自引用/递归约束 | — |
| QD-P-1.6.6 | **FAIL** | 1.6 假设 sections/sources 已存在，无前置校验 | — |
| QD-P-1.6.7 | **FAIL** | 1.5 无信息更新时的结论修订机制 | — |
| QD-P-2.1.1 | PASS | 格式可读 | — |
| QD-P-2.1.2 | **FAIL** | 1.3 "using the specified format (APA/MLA/etc.)" 模糊交叉引用 | T22 |
| QD-P-2.1.3 | PASS | 标题层级合理 | — |
| QD-P-2.1.4 | PASS | 行文简洁 | — |
| QD-P-2.2.1 | PASS | 各角色声明输入 | — |
| QD-P-2.2.2 | **FAIL** | 1.2 输入无格式/编码声明 | — |
| QD-P-2.2.3 | **FAIL** | 无必填/选填标记 | — |
| QD-P-2.2.4 | **FAIL** | 无缺失输入处理 | — |
| QD-P-2.3.1 | PASS | 声明输出格式 | — |
| QD-P-2.3.2 | PASS | 1.4 输出字段已枚举 | — |
| QD-P-2.3.3 | **FAIL** | 无输出稳定性/一致性保证 | — |
| QD-P-2.3.4 | **FAIL** | 无敏感数据过滤/隐私处理 | T23 |
| QD-P-2.4.1 | PASS | 1.5-1.7 流程步骤完整 | — |
| QD-P-2.4.2 | PASS | 1.1/1.3 声明工具 | — |
| QD-P-2.4.3 | **FAIL** | 1.1 仅列工具名，无参数/顺序/失败规格 | T5 |
| QD-P-2.5.1 | **FAIL** | 1.8 "Loop back" 无最大迭代数 | T4 |
| QD-P-2.5.2 | **FAIL** | 1.1-1.8 无禁止操作/访问边界 | T7 |
| QD-P-2.5.3 | **FAIL** | 1.1-1.8 无权限控制边界 | T7 |
| QD-P-2.5.4 | **FAIL** | 1.3/1.6 软约束（来源多样性 vs 时效性）无优先级仲裁 | T16 |
| QD-P-2.5.5 | **FAIL** | 1.1-1.8 无调用频率限制 | T14 |
| QD-P-2.6.1 | **FAIL** | 1.1 "Handle errors" 未覆盖工具/解析/外部异常 | T20 |
| QD-P-2.6.2 | **FAIL** | 无降级/恢复策略 | T20 |
| QD-P-2.6.3 | PASS | 未声明重试机制（未触发） | — |
| QD-P-2.7.1 | **FAIL** | 多数角色（Editor/Writer/Publisher）无正例 | — |
| QD-P-2.7.2 | **FAIL** | 无反例 | — |
| QD-P-2.7.3 | **FAIL** | 无边界用例 | — |

> A.1 小计：47 项，FAIL 26。

### 2.2 A.2 `research_tools`（7 项，L1 只读）

| 规则 ID | 判定 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|-------------|:-----------:|
| QD-T-1.1 | **FAIL** | 2.1 `web_search` 无 `description`、无 `inputSchema` | — |
| QD-T-1.2 | **FAIL** | 2.1 无 `required` 数组；`query` 未列必填 | — |
| QD-T-1.3 | PASS | 枚举 `["tavily","google","bing"]` 无重复/空值 | — |
| QD-T-1.4 | **FAIL** | 参数对象无 `"additionalProperties": false` | — |
| QD-T-2.1 | **FAIL** | `query` 无 `maxLength`/`minLength` | T18 |
| QD-T-2.3 | **FAIL** | `max_results` 无 `minimum`/`maximum` | T18 |
| QD-T-4.1 | **FAIL** | `web_search` 无描述文本 | — |

> **关键：`local_document_search.doc_path` 的路径安全问题未出现在本层级规则中**——L1 只读最小集不含路径安全规则（见 §4 差异 T1）。

### 2.3 A.3 `review_tools`（7 项，L1）

| 规则 ID | 判定 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|-------------|:-----------:|
| QD-T-1.1 | **FAIL** | 2.2 `evaluate_draft` 无 `description`/`inputSchema` | — |
| QD-T-1.2 | **FAIL** | 2.2 无 `required` 数组；`draft_content` 未列必填 | — |
| QD-T-1.3 | PASS | 枚举 `["accuracy","completeness","coherence","sources","objectivity"]` 合法 | — |
| QD-T-1.4 | **FAIL** | 参数对象无 `additionalProperties` | — |
| QD-T-2.1 | **FAIL** | `draft_content` 无长度界 | T8 |
| QD-T-2.3 | PASS | `returns.score` 有 `minimum:1/maximum:10` | — |
| QD-T-4.1 | **FAIL** | `evaluate_draft` 无描述文本 | — |

### 2.4 A.4 `publication_tools`（12 项，L2）

| 规则 ID | 判定 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|-------------|:-----------:|
| QD-T-1.1 | **FAIL** | 2.3 `export_*` 无 `description`/`inputSchema` | — |
| QD-T-1.2 | **FAIL** | 2.3 无 `required` 数组；`content` 未列必填 | T17 |
| QD-T-1.3 | PASS | 枚举 `["academic","business"]` 合法 | — |
| QD-T-1.4 | **FAIL** | 参数对象无 `additionalProperties` | — |
| QD-T-2.1 | **FAIL** | `"content": "string"` 无长度界 | T12 |
| QD-T-2.2 | PASS | 无需要特定格式的字符串参数 | — |
| QD-T-2.3 | N/A | 无数值参数 | — |
| QD-T-2.4 | N/A | 无数组参数 | — |
| QD-T-3.1 | **FAIL** | 导出函数改文件系统，描述（缺）无写操作提示 | T2 |
| QD-T-3.2 | **FAIL** | `"content":"string"` 原始自由输入直通输出生成 | T2/T6 |
| QD-T-4.1 | **FAIL** | `export_*` 无描述文本 | — |
| QD-T-4.2 | **FAIL** | 文件创建副作用未在任何描述中声明 | T2 |

### 2.5 A.5 内嵌代码 QC（13 项）

| 规则 ID | 判定 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|-------------|:-----------:|
| QC-0.1 | PASS | 1.1-1.8 与 3.2 片段语法可解析 | — |
| QC-0.2 | PASS | 代码块标注 `python`/`json` | — |
| QC-0.3 | **FAIL** | 3.2 `class ResearchState(TypedDict)` 使用 `BaseMessage` 等无 import（片段） | — |
| QC-1.1 | PASS | 无未定义名（除未导入符号） | — |
| QC-1.2 | PASS | 无不可用模块导入 | — |
| QC-1.3 | PASS | 无弃用 API | — |
| QC-1.4 | PASS | 无类型不匹配调用 | — |
| QC-2.1 | N/A | 无文件句柄模式 | — |
| QC-2.2 | N/A | 无网络连接构造 | — |
| QC-2.3 | N/A | 无高危文件/网络/DB 调用 | — |
| QC-3.1 | PASS | 无未使用导入 | — |
| QC-3.2 | **FAIL** | 3.2 引用 `TypedDict`/`BaseMessage` 无 import 语句 | — |
| QC-3.3 | PASS | 无硬编码演示凭据 | — |

### 2.6 B 跨工件（8 项）

| 规则 ID | 判定 | 级别 | 证据 / 内容 | 对应 B 主题 |
|---------|:----:|:----:|-------------|:-----------:|
| QD-PT-2.1 | **FAIL** | **P0** | 1.1 声明 `run_research`，Schema 仅 `web_search/local_document_search/evaluate_draft/export_*`，工具不存在 | T5 |
| QD-PT-2.2 | **FAIL** | **P0** | 1.1 仅列工具名；Schema 定义 `parameters`——调用方式与 Schema 不符 | T5 |
| QD-PT-2.3 | **FAIL** | **P0**（原 P1，L3 升级） | 1.1 未声明参数约束；Schema 2.1 定义 `query/max_results/source` | T5 |
| QD-PT-2.4 | N/A | — | 无 RS-3 高危工具 | — |
| QD-PT-2.5 | **FAIL** | **P0**（原 P1，L3 升级） | 1.1 "Handle errors gracefully"；Schema 2.1 未定义错误类型 | T20 |
| QD-PT-2.6 | **FAIL** | **P1**（原 P2，L3 升级） | 无频率限制声明；Schema 仅 `max_results` 一个数量限制 | T14 |
| QD-CYC-1.1 | N/A | — | 无 Skill，无 Prompt/Skill/Tool 循环 | — |
| QD-CYC-1.2 | **FAIL** | **P0**（原 P1，L3 升级） | 1.4 `needs_revision` + 1.5 "Re-submit for re-review" 构成无终止条件的 Reviewer↔Revisor 环 | T4 |

> **A 报告 Top-5 发现**：① `QD-PT-2.1` 声明工具不存在；② `QD-P-2.5.2` 角色提示词无安全边界；③ `QD-P-2.4.3` 无工具调用规格；④ `QD-T-3.2` publication 原始内容直通；⑤ `QD-P-2.5.1` Reviewer↔Revisor 循环无终止。

---

## 3. B 六份 LLM 报告逐条明细（全 127 项）

> `对应 A 规则`列给出可对应的 A 报告规则 ID；"—"表示 A 未覆盖。

### 3.1 R1 Claude Fable 5.1（30 项：P0 4 / P1 13 / P2 13）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| P0-1 | P0 | 权限 | `local_document_search.doc_path` 自由字符串，无白名单/规范化/沙箱 | —（A 未覆盖） |
| P0-2 | P0 | 权限 | `export_markdown.filename` 自由；`export_pdf/docx` 无输出路径 | QD-T-3.1/4.2（部分） |
| P0-3 | P0 | 风险 | Human 节点 24h 默认批准（fail-open） | — |
| P0-4 | P0 | 缺陷 | Reviewer→Revisor 循环无最大轮次/兜底 | QD-P-2.5.1、QD-CYC-1.2 |
| P1-1 | P1 | 风险 | `include_human_feedback:false` + publish_formats 全开 | — |
| P1-2 | P1 | 风险 | 检索内容当可信指令源（间接注入） | — |
| P1-3 | P1 | 权限 | 工具-角色映射缺失；Chief Editor/Researcher 工具不在 Schema | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1/2.2 |
| P1-4 | P1 | 权限 | Publisher embed images + weasyprint SSRF/本地文件读取 | — |
| P1-5 | P1 | 风险 | 本地文档内容存 `sources` 并送第三方模型 | QD-P-2.3.4（部分） |
| P1-6 | P1 | 缺陷 | Human 节点以 LLM 提示词形式编写 | — |
| P1-7 | P1 | 缺陷 | Reviewer 阈值自相矛盾 + JSON 内嵌 Python 注释 | QD-P-1.1.3 |
| P1-8 | P1 | 缺陷 | 三处评审契约不一致 | QD-PT-2.2/2.3（部分） |
| P1-9 | P1 | 缺陷 | `sections/sources/review_scores` 无 reducer | — |
| P1-10 | P1 | 缺陷 | `current_phase` 缺 `cancelled/failed/awaiting_human` | — |
| P1-11 | P1 | 缺陷 | `publication_tools` `"content":"string"` 非 JSON Schema | QD-T-2.1、QD-T-3.2 |
| P1-12 | P1 | 风险 | "minimum 5 sources" 无不足出口 | QD-P-1.3.1（相关） |
| P1-13 | P1 | 权限 | `export_docx.template` 任意路径 | QD-T-3.1/4.2（部分） |
| P2-1 | P2 | 缺陷 | 评审维度命名 `sources` vs `source_quality` | — |
| P2-2 | P2 | 缺陷 | 章节数冲突（3-5 / max_sections 3 / 压测 10） | — |
| P2-3 | P2 | 缺陷 | Writer 1500-2500 词 vs 压测 50+ 页 | — |
| P2-4 | P2 | 缺陷/风险 | Publisher HTML 无 `export_html` + 未转义 | — |
| P2-5 | P2 | 缺陷 | `web_search.max_results` 无上下界 | QD-T-2.1、QD-T-2.3 |
| P2-6 | P2 | 缺陷 | `sources[].content` 全文无去重 | — |
| P2-7 | P2 | 缺陷 | 职责重叠（Chief Editor review_draft/compile_report） | — |
| P2-8 | P2 | 缺陷 | "Handle errors" 无重试/退避/降级 | QD-P-1.6.1、QD-P-2.6.1/2.6.2、QD-PT-2.5 |
| P2-9 | P2 | 缺陷 | 引用格式配置分散 | QD-P-2.1.2 |
| P2-10 | P2 | 风险 | Author/Org 未定义；save state 无加密；verbose 泄密 | QD-P-2.3.4（部分） |
| P2-11 | P2 | 风险 | embed images 无版权校验 | — |
| P2-12 | P2 | 缺陷 | Human 多处未定义（loop back 目标/Notify/ETA/Add guidance） | — |
| P2-13 | P2 | 缺陷 | 文档保真 `reviser.py` vs Revisor | — |

### 3.2 R2 DeepSeek-V4-Pro（19 项：P0 3 / P1 9 / P2 7）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| P0-1 | P0 | 缺陷 | 工具名完全不一致 | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1 |
| P0-2 | P0 | 权限 | 本地文件检索无路径白名单 | — |
| P0-3 | P0 | 风险 | 修订循环无上限 | QD-P-2.5.1、QD-CYC-1.2 |
| P1-1 | P1 | 风险/缺陷 | 人工关卡默认绕过 | — |
| P1-2 | P1 | 权限 | 导出文件名无路径校验 | QD-T-3.1/4.2（部分） |
| P1-3 | P1 | 缺陷 | Reviewer 阈值逻辑不一致 | QD-P-1.1.3 |
| P1-4 | P1 | 缺陷 | Revisor 能力与职责不匹配（无检索工具） | — |
| P1-5 | P1 | 缺陷 | 状态机枚举缺 `human_review` | — |
| P1-6 | P1 | 缺陷 | Publisher HTML 但无 `export_html` | — |
| P1-7 | P1 | 风险 | 共享状态无并发保护 | — |
| P1-8 | P1 | 风险 | 事实核查缺失 | QD-P-2.5.4（相关） |
| P1-9 | P1 | 缺陷 | 评审契约命名/结构不一致 | QD-PT-2.2/2.3（部分） |
| P2-1 | P2 | 风险 | `max_sections` 无上限 | — |
| P2-2 | P2 | 权限/配置 | 外部搜索 API key 管理未说明 | — |
| P2-3 | P2 | 缺陷 | MCP retrieval 提及但未定义 | — |
| P2-4 | P2 | 缺陷 | 引用格式无全局强制 | QD-P-2.1.2 |
| P2-5 | P2 | 缺陷 | 错误恢复机制未定义 | QD-P-2.6.1/2.6.2 |
| P2-6 | P2 | 缺陷/权限 | Tool-to-role 映射缺失 | QD-P-2.5.2/2.5.3 |
| P2-7 | P2 | 缺陷 | 篇幅目标与配置冲突 | — |

### 3.3 R3 GLM-5（25 项：P0 5 / P1 14 / P2 6）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| 1 | P0 | 风险 | Prompt 注入漏洞（外部网页直入上下文） | — |
| 2 | P0 | 权限 | `local_document_search` 无路径沙箱 | — |
| 3 | P0 | 权限 | Publisher 无文件写入目录限制 | QD-T-3.1/4.2（部分） |
| 4 | P0 | 风险 | 无内容安全过滤/DLP | QD-P-2.3.4（部分） |
| 5 | P0 | 缺陷 | Human 24h 超时自动批准 | — |
| 6 | P1 | 权限 | 共享 State 无 RBAC | QD-P-2.5.2/2.5.3 |
| 7 | P1 | 缺陷 | 循环无最大迭代次数 | QD-P-2.5.1、QD-CYC-1.2 |
| 8 | P1 | 缺陷 | 工具失败无错误处理 | QD-P-2.6.1/2.6.2、QD-PT-2.5 |
| 9 | P1 | 缺陷 | 配置矛盾 `include_human_feedback` | — |
| 10 | P1 | 缺陷 | Outline 与 Section 映射缺失 | — |
| 11 | P1 | 权限 | 搜索 API 密钥管理未定义 | — |
| 12 | P1 | 权限 | Chief Editor 超级权限角色 | — |
| 13 | P1 | 权限 | Human guidance 注入无校验 | — |
| 14 | P1 | 风险 | 无 Web 搜索速率限制 | QD-P-2.5.5、QD-PT-2.6 |
| 15 | P1 | 风险 | 异步恢复状态持久化无加密 | QD-P-2.3.4（部分） |
| 16 | P1 | 风险 | 来源可信度无自动化验证 | QD-P-2.5.4（相关） |
| 17 | P1 | 风险 | 无完整审计日志 | — |
| 18 | P1 | 风险 | 并行研究无并发控制 | — |
| 19 | P1 | 风险 | Token 消耗无预算上限 | — |
| 20 | P2 | 缺陷 | "最少 5 来源"未程序化强制 | QD-P-1.3.1（相关） |
| 21 | P2 | 缺陷 | 字数限制未程序化强制 | — |
| 22 | P2 | 缺陷 | Reviewer 评分边界值未定义（=7） | QD-P-1.1.3 |
| 23 | P2 | 缺陷 | 导出工具参数不一致 | QD-T-1.2 |
| 24 | P2 | 缺陷 | 搜索源故障无降级 | QD-P-2.6.2 |
| 25 | P2 | 风险 | Publisher 元数据无脱敏选项 | QD-P-2.3.4（部分） |

### 3.4 R4 GPT-5.6 Terra（16 项：P0 2 / P1 9 / P2 5）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| P0-1 | P0 | 权限/风险 | `local_document_search.doc_path` 任意（路径遍历/越权读） | — |
| P0-2 | P0 | 权限/风险 | Human 24h 默认批准 + `include_human_feedback:false` | — |
| P1-1 | P1 | 权限 | 未定义角色→工具强制授权矩阵（ACL/RBAC） | QD-P-2.5.2/2.5.3 |
| P1-2 | P1 | 风险 | 检索结果直接入上下文（无隔离/注入检测） | — |
| P1-3 | P1 | 缺陷/权限 | 共享 State 无字段级读写权限 | QD-P-2.3.4（部分） |
| P1-4 | P1 | 风险 | 并行 + 共享状态无版本/事务 | — |
| P1-5 | P1 | 风险 | 无资源上限/速率/超时/预算 | QD-P-2.5.5、QD-PT-2.6 |
| P1-6 | P1 | 风险 | `filename`/`template` 自由字符串 | QD-T-3.1/4.2（部分） |
| P1-7 | P1 | 风险 | Publisher HTML 无清洗（XSS） | — |
| P1-8 | P1 | 缺陷/权限 | 审批身份/授权/审计未定义 | — |
| P1-9 | P1 | 缺陷 | 质量门禁规则不闭合 | QD-P-1.6.2 |
| P2-1 | P2 | 缺陷 | 工具与提示词命名不一致 | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1 |
| P2-2 | P2 | 缺陷 | 审核数据模型不一致 | QD-PT-2.2/2.3（部分） |
| P2-3 | P2 | 缺陷 | 发布能力定义不一致（HTML） | — |
| P2-4 | P2 | 缺陷/可观测性 | `messages/sources/error_log` 无限膨胀 | — |
| P2-5 | P2 | 缺陷 | `current_phase` 缺 `cancelled/failed/awaiting/retrying` | — |

### 3.5 R5 Gemini 4 Argon（15 项：P0 5 / P1 6 / P2 4）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| P0-01 | P0 | 缺陷/风险 | 并行研究状态字段缺 Reducer | — |
| P0-02 | P0 | 风险/缺陷 | 审核-修订闭环无最大重试/熔断 | QD-P-2.5.1、QD-CYC-1.2 |
| P0-03 | P0 | 权限/风险 | 本地检索与导出工具路径参数未受限 | QD-T-3.1/4.2（部分） |
| P0-04 | P0 | 缺陷 | prompts 工具名与 Schema 脱节 | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1 |
| P0-05 | P0 | 风险 | 不可信检索内容入全局状态（注入+SSRF/XSS） | — |
| P1-01 | P1 | 权限/风险 | Human 节点 fail-open 默认批准 | — |
| P1-02 | P1 | 权限 | 共享 State 无 RBAC | QD-P-2.5.2/2.5.3 |
| P1-03 | P1 | 权限/风险 | Chief Editor 职责越界 + Human 无约束注入 | — |
| P1-04 | P1 | 缺陷 | Reviewer 输出 vs `evaluate_draft` vs State 三方冲突 | QD-P-1.1.3、QD-PT-2.2/2.3 |
| P1-05 | P1 | 缺陷 | Publisher 格式与工具/配置不一致 + Schema 语法缺陷 + 参数缺失 | QD-T-1.2、QD-T-2.1、QD-T-3.2 |
| P1-06 | P1 | 缺陷 | `current_phase` 缺 human/cancel/fail；无 guidance/产物字段 | — |
| P2-01 | P2 | 缺陷 | 硬编码章节/字数 vs task.json vs 压测 | — |
| P2-02 | P2 | 缺陷 | outline 的范围/字数被丢弃 | — |
| P2-03 | P2 | 缺陷 | Writer 章节来源矛盾 + 无版本隔离 | — |
| P2-04 | P2 | 缺陷 | task.json 配置未同步 State + 检索源权限绑定 | — |

### 3.6 R6 sonnet-5.5（22 项：P0 4 / P1 10 / P2 8）

| 编号 | 级别 | 类别 | 问题 | 对应 A 规则 |
|------|:----:|------|------|:-----------:|
| 1 | P0 | 权限/风险 | Human 24h 默认批准 | — |
| 2 | P0 | 缺陷 | 循环无最大迭代次数 | QD-P-2.5.1、QD-CYC-1.2 |
| 3 | P0 | 权限 | `doc_path` 任意字符串 | — |
| 4 | P0 | 风险 | 无提示注入防护 | — |
| 5 | P1 | 缺陷 | 阶段数不一致（5-stage vs 7 值 vs 5 工具） | — |
| 6 | P1 | 缺陷 | Chief Editor 工具无 Schema | QD-P-1.5.2、QD-PT-2.1 |
| 7 | P1 | 缺陷 | Researcher 工具名对不上 | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1 |
| 8 | P1 | 缺陷 | Reviewer 输出两种格式 + 命名不一致 | QD-P-1.1.3、QD-PT-2.2/2.3 |
| 9 | P1 | 缺陷 | 评分类型不一致 + 阈值写死 | QD-P-1.1.3 |
| 10 | P1 | 缺陷 | `max_sections` 配置冲突 | — |
| 11 | P1 | 缺陷 | Writer 长度冲突 | — |
| 12 | P1 | 权限 | 共享 State 无字段级权限 | QD-P-2.5.2/2.5.3 |
| 13 | P1 | 权限 | Publisher `filename`/`template` 自由 | QD-T-3.1/4.2（部分） |
| 14 | P1 | 风险 | 来源核验靠 Prompt；sources 无可信度字段 | QD-P-2.5.4（相关） |
| 15 | P2 | 缺陷 | 命名/路径不一致 `reviser.py` | — |
| 16 | P2 | 缺陷 | "8 roles × 3 artifact types" 统计有误 | — |
| 17 | P2 | 缺陷 | 无 HTML 导出 + Schema 参数无类型 | QD-T-2.1（部分） |
| 18 | P2 | 缺陷 | `web_search.source` 枚举 vs task.json `source:"web"`；MCP 无 Schema | QD-T-1.3（相关） |
| 19 | P2 | 风险 | 错误处理无重试/降级；无 failed/cancelled | QD-P-2.6.1/2.6.2 |
| 20 | P2 | 风险 | 无成本/token/速率/并发限制 | QD-P-2.5.5、QD-PT-2.6 |
| 21 | P2 | 风险 | 无审计与隐私要求 | QD-P-2.3.4（部分） |
| 22 | P2 | 缺陷 | 文档不严谨（空白评分表 + 最佳实践矛盾） | — |

---

## 4. 正向映射：A 的 53 个 FAIL → B 是否覆盖

| A 规则 ID | 对应 B 主题 | B 覆盖模型数 | 判定 |
|-----------|:-----------:|:------------:|------|
| QD-P-1.1.3 | T8 | R1,R2,R4,R5,R6 | ✅ 覆盖 |
| QD-P-1.3.2 | — | 0 | ✗ A 独有 |
| QD-P-1.3.3 | — | 0 | ✗ A 独有 |
| QD-P-1.5.2 | T5 | R1,R2,R4,R5,R6 | ✅ 覆盖 |
| QD-P-1.6.1 | T20 | R1,R2,R3,R6 | ✅ 覆盖 |
| QD-P-1.6.2 | T4 | R1,R2,R3,R4,R5,R6 | ✅ 覆盖 |
| QD-P-1.6.3 | — | 0 | ✗ A 独有 |
| QD-P-1.6.6 | — | 0 | ✗ A 独有 |
| QD-P-1.6.7 | — | 0 | ✗ A 独有 |
| QD-P-2.1.2 | T22 | R1,R2 | ✅ 覆盖 |
| QD-P-2.2.2 | — | 0 | ✗ A 独有 |
| QD-P-2.2.3 | — | 0 | ✗ A 独有 |
| QD-P-2.2.4 | — | 0 | ✗ A 独有 |
| QD-P-2.3.3 | — | 0 | ✗ A 独有 |
| QD-P-2.3.4 | T23 | R1,R3,R4,R6 | ✅ 覆盖 |
| QD-P-2.4.3 | T5 | R1,R2,R4,R5,R6 | ✅ 覆盖 |
| QD-P-2.5.1 | T4 | 全部 6 | ✅ 覆盖 |
| QD-P-2.5.2 | T7 | R1,R2,R3,R4,R5,R6 | ✅ 覆盖 |
| QD-P-2.5.3 | T7 | R1,R2,R3,R4,R5,R6 | ✅ 覆盖 |
| QD-P-2.5.4 | T16 | R1,R2,R3,R6（相关） | ◐ 部分 |
| QD-P-2.5.5 | T14 | R3,R4,R6 | ✅ 覆盖 |
| QD-P-2.6.1 | T20 | R1,R2,R3,R6 | ✅ 覆盖 |
| QD-P-2.6.2 | T20 | R1,R2,R3,R6 | ✅ 覆盖 |
| QD-P-2.7.1 | — | 0 | ✗ A 独有 |
| QD-P-2.7.2 | — | 0 | ✗ A 独有 |
| QD-P-2.7.3 | — | 0 | ✗ A 独有 |
| QD-T-1.1（research） | — | 0 | ✗ A 独有 |
| QD-T-1.2（research） | — | 0 | ✗ A 独有 |
| QD-T-1.4（research） | — | 0 | ✗ A 独有 |
| QD-T-2.1（research） | T18 | R1,R2,R3,R6 | ✅ 覆盖 |
| QD-T-2.3（research） | T18 | R1,R2,R3,R6 | ✅ 覆盖 |
| QD-T-4.1（research） | — | 0 | ✗ A 独有 |
| QD-T-1.1（review） | — | 0 | ✗ A 独有 |
| QD-T-1.2（review） | — | 0 | ✗ A 独有 |
| QD-T-1.4（review） | — | 0 | ✗ A 独有 |
| QD-T-2.1（review） | T8 | R1,R5（相关） | ◐ 部分 |
| QD-T-4.1（review） | — | 0 | ✗ A 独有 |
| QD-T-1.1（pub） | — | 0 | ✗ A 独有 |
| QD-T-1.2（pub） | T17 | R1,R3,R5 | ✅ 覆盖 |
| QD-T-1.4（pub） | — | 0 | ✗ A 独有 |
| QD-T-2.1（pub） | T12 | R1,R5,R6 | ✅ 覆盖 |
| QD-T-3.1（pub） | T2 | 全部 6 | ✅ 覆盖 |
| QD-T-3.2（pub） | T2/T6 | 全部 6 | ✅ 覆盖 |
| QD-T-4.1（pub） | — | 0 | ✗ A 独有 |
| QD-T-4.2（pub） | T2 | 全部 6 | ✅ 覆盖 |
| QC-0.3 | — | 0 | ✗ A 独有 |
| QC-3.2 | — | 0 | ✗ A 独有 |
| QD-PT-2.1 | T5 | R1,R2,R4,R5,R6 | ✅ 覆盖 |
| QD-PT-2.2 | T5/T8 | R1,R4,R5,R6 | ✅ 覆盖 |
| QD-PT-2.3 | T5 | R1,R4,R5,R6 | ✅ 覆盖 |
| QD-PT-2.5 | T20 | R1,R3,R6 | ✅ 覆盖 |
| QD-PT-2.6 | T14 | R3,R4,R6 | ✅ 覆盖 |
| QD-CYC-1.2 | T4 | 全部 6 | ✅ 覆盖 |

**统计**：A 的 53 个 FAIL 中，**28 个被 B 覆盖**（✅/◐），**25 个为 A 独有**（✗）。A 独有项集中在两类：① **提示词/工具的"文档卫生"规则**（描述缺失、required 缺失、additionalProperties、示例缺失、输入格式/必填标注）——自由式审计几乎不枚举；② 少量语义细节（结论修订机制、前置校验、术语仲裁）。

---

## 5. 反向映射：B 的 24 个主题 → A 是否覆盖

| 主题 | 说明 | B 覆盖模型数 | A 覆盖 | A 对应规则 |
|:----:|------|:------------:|:------:|------------|
| T1 | 路径穿越 `local_document_search.doc_path` | 6/6（全 P0） | **✗** | —（research_tools 归 L1 只读，无路径安全规则） |
| T2 | 任意文件写 `export_*` | 6/6 | ◐ | QD-T-3.1/4.2（写副作用未声明；无输出路径白名单规则） |
| T3 | HITL fail-open（24h 默认批准） | 6/6 | **✗** | — |
| T4 | 循环无最大迭代 | 6/6 | ✅ | QD-P-2.5.1、QD-CYC-1.2（P0） |
| T5 | 工具名不匹配 | 5/6 | ✅ | QD-P-1.5.2、QD-P-2.4.3、QD-PT-2.1/2.2/2.3 |
| T6 | 间接提示注入 | 5/6 | **✗** | —（Stage E 显性风险 = 0） |
| T7 | 缺 RBAC/访问边界 | 6/6 | ✅ | QD-P-2.5.2、QD-P-2.5.3 |
| T8 | 评审契约不一致 | 6/6 | ◐ | QD-P-1.1.3（阈值）；返回结构/命名未单独覆盖 |
| T9 | 并发/缺 reducer | 5/6 | **✗** | — |
| T10 | `current_phase` 枚举不完整 | 5/6 | **✗** | — |
| T11 | Publisher HTML 能力不符 | 5/6 | **✗** | — |
| T12 | publication 参数类型缺陷 | 3/6 | ◐ | QD-T-2.1、QD-T-3.2 |
| T13 | Chief Editor 超级角色/重叠 | 3/6 | **✗** | — |
| T14 | 无速率/频率限制 | 3/6 | ✅ | QD-P-2.5.5、QD-PT-2.6（仅频率） |
| T15 | 无审计日志/可观测性 | 3/6 | **✗** | — |
| T16 | 来源可信度/幻觉/事实核查 | 4/6 | **✗** | — |
| T17 | 导出参数缺失（filename/metadata） | 3/6 | ✗ | —（QD-T-1.2 仅覆盖 required 缺失） |
| T18 | `web_search` 参数无界/密钥管理 | 4/6 | ✅ | QD-T-2.1、QD-T-2.3（仅参数） |
| T19 | 配置冲突（章节/字数/压测） | 5/6 | **✗** | —（配置工件视为 out-of-type） |
| T20 | 错误处理/重试未定义 | 4/6 | ✅ | QD-P-1.6.1、QD-P-2.6.1/2.6.2、QD-PT-2.5（P0） |
| T21 | Human 节点细节未定义/注入 | 4/6 | **✗** | — |
| T22 | 引用格式未全局强制 | 2/6 | ✅ | QD-P-2.1.2 |
| T23 | 状态持久化无加密/脱敏 | 4/6 | ◐ | QD-P-2.3.4 |
| T24 | 文档保真（命名/统计/量表） | 3/6 | **✗** | —（设计上超出范围） |

**统计**：24 个主题中，**A 完全覆盖 7 个**（T4/T5/T7/T14/T18/T20/T22）、**部分覆盖 4 个**（T2/T8/T12/T23）、**完全未覆盖 13 个**（T1/T3/T6/T9/T10/T11/T13/T15/T16/T17/T19/T21/T24）。

---

## 6. 差异维度总结（逐维度）

### 6.1 差异一：方法学

| 维度 | A | B |
|------|---|---|
| 输出单元 | 规则 ID + PASS/FAIL + 证据 | 叙事式问题 + 严重度 |
| 规则集 | 固定枚举 | 无 |
| 可复现性 | 高 | 低 |
| 严重度来源 | 规则层级 + L3 升级 | 分析者判断 |
| 范围控制 | 严格（配置 out-of-type） | 宽泛 |
| 结论纪律 | 拒绝下安全/质量结论 | 自由下安全结论 |
| 阶段 | 7 阶段（D 未跑） | 单遍叙事 |
| 风险审计 | Stage E = 0 条 | 风险为主导关注 |

### 6.2 差异二：数量与严重度

- A：53 FAIL，**P0 占 70%**（因 L3 升级近乎全 P0）。
- B：127 条，**P0 占 ~18%**。
- 表观"53 vs 21"是**粒度差异**（规则标签 vs 问题条目），不可直接比大小。

### 6.3 差异三：范围（A 静默、B 高亮）

B 主导的**安全/运维/配置**类在 A 中**无规则或超范围**：T1 路径穿越、T6 注入、T9 并发、T10 枚举、T11 HTML、T15 审计、T16 可信度、T19 配置、T21 Human 细节、T23 加密、T24 文档保真。**根本原因**：A 为 lite、静态、仅 Inspect 规则包，且将 `research_tools` 定为 L1 只读，最小集不含路径安全规则。

### 6.4 差异四：严重度校准（同一缺陷，级别可差两级）

| 共同缺陷 | A | B 区间 |
|----------|:-:|:------:|
| 工具存在性不匹配 | P0 | P0–P2 |
| 循环终止 | P0 | P0–P1 |
| 原始内容直通 | P0 级（L2 写） | P1–P2 |

### 6.5 差异五：证据纪律

- A：每条判定引用精确小节/规则证据，并声明"PASS 不等于 Risk PASS"。
- B：参差。R4/R6 显式声明"文档≠源码"边界；R3 从文本较强断言运行时风险。

### 6.6 差异六：A 独有的"卫生类"规则（25 项，B 几乎不枚举）

包括 `QD-T-1.1/1.2/1.4/4.1`（描述/required/additionalProperties/描述文本）、`QD-P-2.7.1/2.7.2/2.7.3`（示例缺失）、`QD-P-2.2.2/2.2.3`（输入格式/必填标注）、`QC-0.3/QC-3.2`（片段 import 缺失）。这类**规范化/文档完整性**问题自由式审计普遍不覆盖。

---

## 7. 结论与联合使用建议

### 7.1 两者关系

**互补，而非竞争。**

- **A 技能报告** = **可复现、规则锚定、范围克制、按构造偏 P0** 的权威结构视图；强于结构/契约缺陷，明确拒绝过度断言；局限是 lite 规则集的**覆盖盲区**（尤其 L1 只读层不含路径安全）。
- **B 多模型分析** = **广谱的安全/运维**视图；独有地给出 T1/T3/T6 等**全部或多数模型独立判为 P0** 的类别；但无统一规则 ID、严重度分歧大、证据纪律参差。

### 7.2 修复建议（联合排序）

| 优先级 | 动作 | 来源 |
|:------:|------|------|
| 必须（阻断） | 修复工具存在性/调用契约 FAIL（`QD-PT-2.1`~`2.5`）、循环终止（`QD-CYC-1.2`）、Schema 完整性（`QD-T-1.1/1.2/1.4`）、错误处理（`QD-P-2.6.*`） | A（权威） |
| 必须（阻断） | 沙箱化 `local_document_search`；限制 `export_*` 输出目录；Human 超时改 **fail-closed**；补抗注入处理 | B（T1/T2/T3/T6），须用 `sanityops-cli` Risk 复核 |
| 高 | 以 Tool Schema 为单一事实源反向校正 8 个提示词 + 状态/配置；建立角色→工具授权矩阵 | A `QD-PT/2.5.2`、B T5/T7 |
| 中 | 运维/质量：限流、成本预算、审计日志、状态加密、保留期限 | B T14/T15/T23 |
| 中 | 解决配置冲突（章节/字数/压测）与引用格式全局强制 | B T19/T22 |

### 7.3 最高置信缺陷

**两者都命中**的缺陷置信度最高：**工具契约（A `QD-PT-*` ≈ B T5）** 与 **循环终止（A `QD-CYC-1.2` ≈ B T4）**。
**仅 B 命中的高危项**（T1 路径穿越、T3 fail-open、T6 注入）应视为"**未验证但紧急**"，用完整版 `sanityops-cli` 的 Risk 阶段据实确认——这正是 A 报告自身给出的升级路径。

---

## 附录 A：术语与规则族对照

| A 规则族 | 含义 | 判定项数 | FAIL |
|----------|------|:--------:|:----:|
| `QD-P-*` | 系统提示词规则（1.x 结构/身份，2.x 清晰度/输入输出/工具/错误/示例） | 47 | 26 |
| `QD-T-*` | 工具 Schema 规则（research L1 / review L1 / publication L2） | 26 | 19 |
| `QD-PT-*` | 跨工件 Prompt↔Tool 规则 | 6 | 5 |
| `QD-CYC-*` | 循环调用规则 | 2 | 1 |
| `QC-*` | 内嵌代码质量检查 | 13 | 2 |

## 附录 B：三份报告的关系

| 报告 | 位置 | 作用 |
|------|------|------|
| 多模型元分析 | `report-onlybyLLM/comparison-multi-llm-analysis-tc-004-2026-10-15.md` | 横向对比 6 份 LLM 报告，建立主题 T1~T24 |
| 技能 vs LLM 对比（英文） | `report-onlybyLLM/comparison-sanityops-skill-report-vs-multi-llm-analysis-tc-004-2026-10-15.md` | A 与 B 的宏观/覆盖对比 |
| **本报告（中文·逐条）** | `report-onlybyLLM/comparison-detailed-chinese-tc-004-2026-10-15.md` | A 94 项 + B 127 项逐条明细 + 双向映射 |
