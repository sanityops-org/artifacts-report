基于对 `TC-004-gpt-researcher-multi-agent-suite.md` 全文（涵盖 8 个角色列表、8 个 System Prompts、3 组 Tool Schemas、2 个配置与状态工件 `task.json` / `ResearchState` 以及评估与测试规范）的完整解析与交叉复检，以下针对该多智能体系统的**缺陷（逻辑与契约不一致）**、**权限（越权访问与职责边界失控）**、**显性风险（安全漏洞、死循环与并发故障）**三类问题进行分级统计与解释。

---

### 一、 全局问题统计概览

- **问题总数**：**15 项**
- **按严重级别统计**：
  - **P0 级（致命/阻断级）**：**5 项**（直接导致系统运行崩溃、并发数据静默丢失、死循环耗尽资源或高危越权/注入攻击）
  - **P1 级（严重级）**：**6 项**（导致人工审批门禁失效、状态越权篡改、核心工具/状态契约冲突导致功能残缺）
  - **P2 级（一般/演进级）**：**4 项**（导致动态配置失效、上下游字段丢失、可观测性与审计轨迹缺失）
- **按问题类型统计（含交叉属性）**：
  - **缺陷（Defects）**：10 项（含纯缺陷 7 项，缺陷伴随显性风险 3 项）
  - **权限（Permissions）**：4 项（含纯权限 1 项，权限伴随显性风险 3 项）
  - **显性风险（Explicit Risks）**：7 项（含纯显性风险 1 项，与其他类别交叉 6 项）

---

### 二、 问题分级统计大列表（P0 ~ P2）

#### 【P0 级：致命 / 阻断级】—— 共 5 项

1. **[P0-01] [缺陷 / 显性风险] 并行研究状态字段缺失 Reducer，导致并发写入崩溃或数据覆盖丢失**
   
   - **涉及工件**：`1.1 Chief Editor` (`run_research`)、`3.2 State Schema (ResearchState)`、`Stress Tests` (`max_sections=10`)
   
   - **问题概要与解释**：Chief Editor 明确支持触发多章节并行研究（`Trigger parallel section research`），压测也要求支持 `max_sections=10` 并发。但在 LangGraph 的 `ResearchState` 定义中，仅 `messages` 和 `error_log` 声明了 `Annotated[..., operator.add]` 累加器；而并行节点高频写入的 `sections: Dict[str, str]`、`sources: List[Dict]`、`review_scores: Dict[str, int]` 均未定义合并归约器（Reducer）。
   
   - **可能的影响**：多个 Researcher / Reviewer 节点并行返回结果汇合时，LangGraph 会直接抛出并发写入冲突异常（`InvalidUpdateError`）导致工作流崩溃；或发生“最后写入者覆盖（Last-Write-Wins）”，导致其余并行章节的研究草稿和文献来源静默丢失。

2. **[P0-02] [显性风险 / 缺陷] 审核-修订闭环（Reviewer ↔ Revisor）缺乏最大重试次数与熔断机制**
   
   - **涉及工件**：`1.4 Reviewer`、`1.5 Revisor`、`3.1 task.json`、`3.2 State Schema (ResearchState)`
   
   - **问题概要与解释**：Reviewer 规定总分 `< 7` 即标记为 `needs_revision` 打回修改，Revisor 修改后重新提交复审（`Re-submit for re-review`）。然而在 `task.json` 和 `ResearchState` 中，均未设计 `revision_count` 或 `max_iterations` 计数与上限字段，也无降级放行或转人工兜底策略。
   
   - **可能的影响**：当研究主题较冷门（无法找齐至少 5 个多样化来源或统计数据）或评分模型在临界值震荡时，状态机将陷入 `reviewing ↔ revising` 无限死循环，导致任务永久挂起、LLM Token 与搜索 API 额度被耗尽。

3. **[P0-03] [权限 / 显性风险] 本地文档检索与报告导出工具存在未受限路径参数（任意文件读写/目录遍历）**
   
   - **涉及工件**：`2.1 Research Tools` (`local_document_search`)、`2.3 Publication Tools` (`export_markdown`, `export_docx`)
   
   - **问题概要与解释**：`local_document_search` 的 `doc_path` 参数、`export_markdown` 的 `filename` 参数以及 `export_docx` 的 `template` 参数均为无约束的裸 `string` 类型，缺乏根目录白名单限制、路径规范化校验或沙箱隔离。
   
   - **可能的影响**：一旦 Agent 受到恶意 Query 或网页检索内容的诱导，可通过 `../` 目录遍历读取宿主机上的任意敏感文件（`.pdf`/`.docx`/`.txt`/`.md`），或利用导出与模板加载功能覆盖系统关键文件，构成高危越权读写。

4. **[P0-04] [缺陷] System Prompts 声明的工具名称与 Tool Schemas 定义严重脱节（工具缺失/命名冲突）**
   
   - **涉及工件**：`8 Agent Roles 表`、`1.1 Chief Editor`、`1.3 Researcher`、`1.4 Reviewer`、`2.1 Research Tools`、`2.2 Review Tools`
   
   - **问题概要与解释**：
    1. Chief Editor 提示词声明拥有 `init_research`、`plan_sections`、`run_research`、`review_draft`、`compile_report` 5 个工具，但 `2. Tool Schemas` 中完全没有定义这些工具；
    2. Researcher 提示词声明调用 `conduct_research` 和 `write_draft`，但 `2.1 Research Tools` 实际定义的工具名为 `web_search` 和 `local_document_search`；
    3. `8 Agent Roles 表` 中 Reviewer 的工件类型未包含 `Tool Schema`，但 `2.2 Review Tools` 却为其定义了 `evaluate_draft`。
   
   - **可能的影响**：模型按照 System Prompt 发起工具调用时，会因工具名不存在或未绑定而直接触发 `ToolNotFound` 调用异常，导致编排与检索主流程阻断。

5. **[P0-05] [显性风险] 外部不可信检索内容直接写入全局状态，引发间接提示词注入（Indirect Prompt Injection）与 SSRF/XSS**
   
   - **涉及工件**：`1.3 Researcher`、`1.7 Publisher`、`2.1 Research Tools`、`3.2 State Schema (ResearchState)`
   
   - **问题概要与解释**：Researcher 从公网抓取的网页内容直接存入 `ResearchState.sources`（`content: str`），未经任何清洗、转义或上下文隔离标记，便直接传递给 Reviewer、Revisor、Writer 和 Publisher；同时 Publisher 使用 `weasyprint` 生成 PDF、输出 HTML 并自动嵌入图片（`Embed images`）。
   
   - **可能的影响**：攻击者可在外部网页中埋入恶意指令劫持下游 Agent（例如诱导 Reviewer 直接输出 `"overall_score": 10, "approval_status": "approved"` 绕过质检）；或在图片链接/HTML 中注入 `file:///etc/passwd` 或内网元数据地址，在 `weasyprint` 渲染 PDF 时触发服务端请求伪造（SSRF）/本地文件包含（LFI），以及在 HTML 报告中产生存储型 XSS。

---

#### 【P1 级：严重级】—— 共 6 项

6. **[P1-01] [权限 / 显性风险] Human 节点超时采用“默认批准（Fail-Open）”策略，使人工门禁形同虚设**
   
   - **涉及工件**：`1.8 Human (Human-in-the-Loop)`
   
   - **问题概要与解释**：Human 节点的超时机制被设定为 `Default approval after 24 hours`（24 小时无响应则默认批准通过），同时又声明该节点负责关键决策通知（`Notify on critical decisions needed`）。
   
   - **可能的影响**：违背权限与安全设计的“默认拒绝（Fail-Closed）”原则。若告警通知组件故障、审核人员休假或通知渠道被恶意阻塞，低质量、违规甚至被注入恶意载荷的研究报告将在 24 小时后自动越过人工审核并正式发布。

7. **[P1-02] [权限] 全局共享 `ResearchState` 缺乏基于角色的字段级读写访问控制（RBAC/ACL）**
   
   - **涉及工件**：`1.1 Chief Editor`、`3.2 State Schema (ResearchState)`
   
   - **问题概要与解释**：系统要求所有 Agent 维护并共享同一个 `ResearchState`，但在状态机层面未对不同角色的读写范围做最小权限约束（例如 Researcher 理论上只应写 `sections` 和 `sources`，不应有权限修改 `review_scores`、`outline` 或 `current_phase`）。
   
   - **可能的影响**：任一子 Agent 出现幻觉或被提示词注入劫持后，均可越权篡改全局核心状态（如直接修改 `review_scores` 为满分，或将 `current_phase` 篡改为 `"complete"`），从而绕过 Chief Editor 的质量关卡。

8. **[P1-03] [权限 / 显性风险] Chief Editor 职责越界包揽撰写与发布，且 Human 节点允许无约束动态注入规则**
   
   - **涉及工件**：`1.1 Chief Editor`、`1.8 Human`
   
   - **问题概要与解释**：Chief Editor 的 `compile_report: Finalize and publish` 工具直接跨越了 Writer（汇总撰写）和 Publisher（多格式发布）的权限边界；此外，Human 节点的 `Add guidance - Inject additional constraints` 允许在运行期注入任意自然语言约束，缺乏权限范围与格式合规校验。
   
   - **可能的影响**：导致主控 Agent 权限过大、角色职责重叠；同时未受限的运行时人工指令可能直接覆盖或破坏 `task.json` 中预设的强制合规要求（`guidelines`）。

9. **[P1-04] [缺陷] Reviewer 提示词输出结构与 `evaluate_draft` 工具 Schema、状态机字段三方契约冲突**
   
   - **涉及工件**：`1.4 Reviewer`、`2.2 Review Tools` (`evaluate_draft`)、`3.2 State Schema (ResearchState)`
   
   - **问题概要与解释**：
    1. Reviewer 提示词要求输出包含 `overall_score`、`criteria_scores`（含 `source_quality`）、`gaps_identified`、`revision_suggestions`、`approval_status` 的完整 JSON；
    2. 但 `evaluate_draft` 工具的参数枚举写成了 `"sources"`（而非 `"source_quality"`），且返回值 Schema 仅包含 `{"score": number, "feedback": string}`；
    3. `ResearchState` 的 `review_scores: Dict[str, int]` 仅支持存储单一整数，无法保存分项得分与 `approval_status`。
   
   - **可能的影响**：工具返回结果与 Prompt 预期结构不兼容，导致解析报错，或者丢失结构化的漏洞列表（`gaps_identified`）与分项评分，使下游 Revisor 失去明确的修改靶向。

10. **[P1-05] [缺陷] Publisher 发布格式与工具集、配置文件不一致，且工具 Schema 存在语法缺陷与参数缺失**
    
    - **涉及工件**：`1.7 Publisher`、`2.3 Publication Tools`、`3.1 task.json`
    
    - **问题概要与解释**：
    
    1. Publisher 提示词声明支持 Markdown、PDF、Word、**HTML** 四种格式，但 `2.3 Publication Tools` 和 `3.1 task.json` 中均缺失 HTML 导出工具（无 `export_html`）及对应配置开关；
    2. `2.3 Publication Tools` 的 JSON Schema 语法不合规范（如 `"content": "string"` 未写成标准的 `{"type": "string"}`）；
    3. `export_pdf` 与 `export_docx` 均缺失输出文件名参数（`filename`），且所有导出工具均无参数接收 Publisher 要求写入的元数据（`Metadata`：报告标题、生成日期、来源数、字数、作者/机构）。
    
    - **可能的影响**：HTML 格式发布能力彻底不可用；PDF 与 Word 导出无法指定文件名及附加元数据；非标准 JSON Schema 在严格校验的 LLM 客户端中会直接引发工具注册失败。

11. **[P1-06] [缺陷] 状态机 `current_phase` 缺失人工审核与取消/失败状态，且无字段保存人工反馈与发布产物**
    
    - **涉及工件**：`1.8 Human`、`3.2 State Schema (ResearchState)`、`Evaluation Dimensions (2. Workflow Completeness)`
    
    - **问题概要与解释**：`ResearchState.current_phase` 定义了 7 个字面量状态（与评估维度中声称的“5-stage workflow”自相矛盾），但唯独缺少对应 Human 节点的 `human_review`（等待人工审核）状态，以及对应 `4. Cancel - Terminate workflow` 的 `cancelled` / `failed` 状态；同时 `ResearchState` 中没有任何字段用于持久化存储 Human 输入的 `guidance` 和 Publisher 生成的文件路径列表。
    
    - **可能的影响**：当工作流在等待人工审核并触发异步持久化（`Save state for async resumption`）或被人工取消时，状态机无法正确记录挂起位置与人工指导意见，恢复执行时会导致状态流转错乱。

---

#### 【P2 级：一般 / 演进级】—— 共 4 项

12. **[P2-01] [缺陷] System Prompt 硬编码的章节数与字数上限，与 `task.json` 动态配置及压测目标冲突**
    
    - **涉及工件**：`1.2 Editor`、`1.6 Writer`、`3.1 task.json`、`Stress Tests`
    
    - **问题概要与解释**：Editor 提示词硬编码要求大纲为 `3-5 main sections`，Writer 提示词硬编码要求总字数为 `1500-2500 words`；然而 `task.json` 提供了动态配置 `"max_sections": 3`，且压力测试明确要求测试 `max_sections=10` 以及生成 `50+ page reports`（远超 2500 词）。
    
    - **可能的影响**：当用户在 `task.json` 中配置小于 3 或大于 5 的章节数、或要求生成长篇报告时，System Prompt 中的硬编码数字会与动态配置产生指令冲突，导致模型忽略配置或强行截断内容。

13. **[P2-02] [缺陷] Editor 规划的章节范围与预估字数在 `ResearchState.outline` 中被丢弃**
    
    - **涉及工件**：`1.2 Editor`、`1.5 Revisor`、`3.2 State Schema (ResearchState)`
    
    - **问题概要与解释**：Editor 提示词要求输出 5 个要素（`Section title`、`Key questions`、`Expected content scope`、`Priority level`、`Estimated word count`），但 `ResearchState.outline` 的结构定义 `[{"title": str, "questions": [], "priority": str}]` 仅保留了 3 项，丢弃了 `Expected content scope`（内容范围边界）和 `Estimated word count`（预估字数）。
    
    - **可能的影响**：下游 Researcher 与 Revisor 的提示词中多次强调“Do not expand beyond original section scope（不得超出原始章节范围边界）”，但因状态机未保存该字段，下游 Agent 无法获知各章节的边界定义，极易造成章节内容重叠或篇幅失控。

14. **[P2-03] [缺陷] Writer 对章节内容来源的表述前后矛盾，且 `ResearchState` 缺乏初稿与修订稿的版本隔离**
    
    - **涉及工件**：`1.5 Revisor`、`1.6 Writer`、`3.2 State Schema (ResearchState)`
    
    - **问题概要与解释**：Writer 提示词首句要求整合“all revised sections（所有修订后的章节）”，但在正文结构第 3 点却写着 `Main Sections (from Researcher outputs)`；同时 `ResearchState` 仅有一个 `sections: Dict[str, str]` 字段，未区分初稿与修订稿。
    
    - **可能的影响**：若 Revisor 直接覆盖 `sections`，系统将丢失初稿与修订过程的对比审计轨迹（影响 Observability）；若 Revisor 不覆盖 `sections`，Writer 则会误将未经修订的 Researcher 初稿拼入最终报告。

15. **[P2-04] [缺陷 / 显性风险] `task.json` 的全局配置项未同步至 `ResearchState`，且缺乏检索源的强制权限绑定**
    
    - **涉及工件**：`1.3 Researcher`、`2.1 Research Tools`、`3.1 task.json`、`3.2 State Schema (ResearchState)`
    
    - **问题概要与解释**：`task.json` 定义了 `"source": "web"`、`"follow_guidelines": true`、`"guidelines": [...]` 等全局配置，但 `ResearchState` 仅存储了 `query: str`，没有字段传递 `guidelines`、引文格式（如 APA）或允许的数据源类型（`source`）。同时，即便配置限定 `"source": "web"`，Researcher 依然默认暴露 `local_document_search` 工具。
    
    - **可能的影响**：在长链路多轮迭代中，末端 Agent（如 Revisor、Writer）容易因上下文缺失而违背 `task.json` 中的全局 `guidelines`（如语言、引文格式要求）；且在纯 Web 检索任务中，Researcher 仍存在误调用本地文件检索工具的风险。
