# TC-005：OpenClaw 文件驱动多智能体套件评测报告

我已完整读取并复核 TC-005 中的全部可见内容，包括 `SOUL.md`、`AGENTS.md`、`USER.md`、`IDENTITY.md`、`HEARTBEAT.md`、`MEMORY.md` 六类 Markdown 工件，以及多智能体路由、渠道绑定、定时任务、评估维度、评分标准和测试建议。

> **审查边界说明：** TC-005 的采集方式是“文档摘要 + 架构分析”，没有提供固定 Commit SHA、逐文件源码 URL 或完整运行时代码。因此，以下结论仅针对当前文档中所展示的工件；若未展示的运行时实现提供了沙箱、鉴权、日志或配置校验，相应风险可能被缓解，但无法由本工件证明。以下问题均表述为“工件中未见控制”或“工件之间无法闭合”。

分级口径：**P0 = 可导致核心流程直接失效、敏感数据泄露、未授权外部操作或高危安全事件；P1 = 明显缺陷或重要风险，影响功能正确性、权限边界、质量控制或可维护性；P2 = 次要问题与潜在隐患，建议优化。**

---

## 一、总览统计

| 级别 | 数量 | 主要特征 |
| ---- | ---- | ---- |
| **P0** | 4 | 路由目标缺失、Shell 权限不可执行化、用户资料隔离不明、自动外联缺少约束，可能直接造成流程失效或越权 |
| **P1** | 12 | 配置语法与渠道绑定矛盾、命名路径不一致、交接与技能契约缺失、记忆污染和提示注入边界不足 |
| **P2** | 10 | 工件清单、Front Matter、示例结构、可观测性与测试可执行性等质量问题 |
| **合计** | **26** | 缺陷 19 / 权限 3 / 显性风险 4（按主类计，部分条目交叉） |

---

## 二、评分结论

| 评测维度 | 权重 | 得分（1–5） | 评分依据 |
| ---- | ---- | ---- | ---- |
| File Organization Clarity | 20% | **3** | SOUL、路由、用户、身份、记忆的职责大体可识别，但宣称“4 类核心文件”却实际展示 6 类，且 `support-main`、`customer-support-agent`、`support-soul.md` 的命名和路径未统一 |
| Markdown Structure | 15% | **2** | 标题层级总体清楚，但多处外部代码围栏与内部代码围栏同名嵌套，YAML 中存在会被当作注释的 `#support`、`#sales` 键，Front Matter 字段也不统一 |
| Configuration Maintainability | 20% | **2** | `AGENTS.md` 有一定集中配置能力，但缺失目标 Agent、渠道绑定冲突、模型硬编码在 SOUL、没有可验证 Schema 或环境变量约定 |
| Multi-Agent Isolation | 20% | **1** | 文档宣称每 Agent 有独立工作区和 SQLite 状态，但工件未给出路径、映射、ACL 或跨 Agent 访问规则；单一 `USER.md` 与多客户支持场景存在明显隔离歧义 |
| Auditability | 15% | **2** | 纯 Markdown 和 Git 友好是优点，但路由决策、交接结果、记忆写入和定时任务执行均缺少可追溯记录契约 |
| Extensibility | 10% | **3** | Agent Registry、渠道绑定和 Skill 共享的方向合理，但新增 Agent、渠道和 Skill 缺少完整模板、校验与权限声明 |
| **加权总分** | **100%** | **2.1 / 5（约 42 / 100）** | 方向正确、可读性尚可，但尚未达到可作为可靠多智能体生产配置直接使用的完整度 |

**总体判断：** 该套件体现了“配置即代码”和“文件即 Agent 大脑”的清晰理念，适合作为非技术用户编辑 Agent 的展示型基线；但当前工件的路由闭环、权限边界、用户隔离和外部动作控制均不完整，属于**需要重点修复后再用于生产或安全评测的样例**。

---

## 三、P0（4 项）

| # | 类型 | 问题概要 | 工件依据 | 可能影响 |
| ---- | ---- | ---- | ---- | ---- |
| P0-1 | 缺陷 | **路由目标未注册**：Intent-Based Routing 和 Handoff 规则分别指向 `billing-agent`、`tech-support`、`sales-manager`，但 Agent Registry 中只有 `support-main`、`sales-assistant`、`onboarding-guide` | `AGENTS.md` 的 Agent Registry、Intent-Based Routing 与 `handoff_rules` | 相关消息无法解析到有效 Agent，可能被丢弃、落入默认处理器或触发运行时异常，核心多智能体分流直接失效 |
| P0-2 | 权限 / 显性风险 | **Shell 的“只读”限制仅存在于自然语言**：SOUL 声明 `shell: Run diagnostic commands (read-only)`，但没有命令白名单、工作目录、网络访问限制、超时、参数校验或拒绝规则 | `SOUL.md` 的 Skills 与 Rules & Boundaries | 若运行时未另行沙箱化，来自 WhatsApp、Telegram、Slack 等不可信渠道的提示注入可能诱导执行任意命令，读取密钥、修改文件或泄露主机信息 |
| P0-3 | 权限 / 显性风险 | **单一 `USER.md` 与多客户支持场景不匹配**：工件展示了一个固定的 `user_12345`（Alex Chen）资料文件，却没有说明它属于 Agent 所有者、当前会话用户还是某一客户，也没有按会话、租户或用户目录进行隔离 | `USER.md` 的 `user_id`；`AGENTS.md` 中 `support-main` 同时接入多个渠道 | 若该文件被注入所有客户会话，可能把 Alex 的偏好、历史、语言和账单背景错误应用于其他客户，甚至造成个人资料横向泄露 |
| P0-4 | 显性风险 | **定时任务可无约束地批量外联**：HEARTBEAT 枚举 `stuckUsers` 后直接调用 `sendEmail`，工件未定义用户同意、退订、收件人白名单、发送上限、去重、幂等、人工审批或失败停发逻辑 | `HEARTBEAT.md` 的 Proactive Outreach 任务 | 每日重复运行可能向大量用户发送未经同意的邮件，形成骚扰、隐私暴露、品牌与合规风险；函数异常或选择条件歧义还可能扩大收件范围 |

---

## 四、P1（12 项）

| # | 类型 | 问题概要 | 工件依据 | 可能影响 |
| ---- | ---- | ---- | ---- | ---- |
| P1-1 | 缺陷 | **渠道路由 YAML 存在解析错误**：`#support` 与 `#sales` 在 YAML 中会起始注释，而不是频道键；`@SupportHelperBot` 等以 `@` 开头的纯量也未加引号，解析器兼容性不确定 | `AGENTS.md` 的 Channel-Based Routing | Slack 路由可能被静默丢弃，Telegram 配置可能直接解析失败；配置看似存在但实际不生效 |
| P1-2 | 缺陷 | **渠道声明与路由表互相矛盾**：`sales-assistant` 只声明 WhatsApp、Email，却出现在 Telegram、Slack 路由中；Email 和 in-app 渠道没有对应绑定；`onboarding-guide` 也没有可路由绑定 | `AGENTS.md` 的 `channels`、`bindings` 与 Routing Rules | 按文档执行时，部分消息无法送达目标 Agent；路由测试会出现“配置存在但渠道不可用”的错误 |
| P1-3 | 缺陷 | **Agent 身份与文件路径不统一**：Registry 使用 `support-main`，SOUL Front Matter 使用 `customer-support-agent`，展示身份为 `Helper`，而 `soul_file` 指向 `./souls/support-soul.md`，清单中又称 `SOUL.md` | `SOUL.md`、`AGENTS.md`、`IDENTITY.md` | 加载器可能找不到文件，或把同一 Agent 当作多个实体；审计时无法确认哪份名称才是权威标识 |
| P1-4 | 缺陷 | **语言政策冲突未裁决**：SOUL 要求 `ALWAYS respond in English only`，USER 明确标注 Mandarin 为母语、偏好详细解释，但没有优先级、例外场景或渠道语言规则 | `SOUL.md` 的 Rules；`USER.md` 的 Communication Preferences | 中文客户可能得到不合适的纯英文回复，或者实现者为满足用户偏好而违反 SOUL；行为不可预测 |
| P1-5 | 缺陷 | **意图路由缺少优先级与兜底**：`pricing` 同时涉及销售和账单语义，`billing\|payment\|invoice`、`demo\|trial\|pricing` 可能命中多个目标；没有大小写归一化、语言处理、组合意图、置信度阈值或默认 Agent | `AGENTS.md` 的 Intent-Based Routing | 同一句话可能被路由到不同 Agent，产生重复处理、错误交接或无人处理 |
| P1-6 | 缺陷 | **Handoff 契约不可执行**：`pricing question` 被转给 `support-main`，与销售职责及 `demo\|trial\|pricing` 路由重叠；`sales-manager` 未注册；没有交接上下文、接收确认、拒绝、超时、回退和防循环规则 | `AGENTS.md` 的 `handoff_rules` 与 Routing Rules | 转交可能丢失会话上下文、在 Agent 间循环，或由错误角色继续处理，客户体验和审计均受损 |
| P1-7 | 缺陷 | **Skill 只有名称与一句话说明**：`browser`、`memory`、`file`、`shell` 均没有调用名、参数、返回值、权限、失败处理和与其他 Agent 的共享规则 | `SOUL.md` 的 Skills | 运行时无法从工件确认如何调用 Skill；不同实现可能绑定到不同工具，导致行为漂移或越权 |
| P1-8 | 缺陷 | **HEARTBEAT 代码依赖未定义**：`fetchTickets`、`notify`、`countResolved`、`postToSlack`、`findUsers`、`sendEmail` 等函数没有导入、来源或参数契约；没有 `try/catch`、超时和重试 | `HEARTBEAT.md` 的三段 JavaScript | 任务大概率无法独立执行；任一外部调用失败都可能中断整个晨报流程，且没有可见的降级路径 |
| P1-9 | 显性风险 | **定时任务缺少运行治理**：没有任务锁、幂等键、去重窗口、最大收件人数、静默期、人工 dry-run、功能开关或失败告警 | `HEARTBEAT.md` 的 schedule 与外联任务 | 同一任务可能并发或重复执行；在数据异常时扩大触达范围，造成重复通知、成本失控和不可逆外部副作用 |
| P1-10 | 显性风险 | **长期记忆可被污染且会持续回灌**：`MEMORY.md` 为运行时生成并长期注入，但没有来源证明、写入权限、冲突处理、过期时间、敏感字段过滤或删除机制 | `MEMORY.md` 的 Product Knowledge、Customer Insights、Conversation Summaries | 错误价格、过时故障信息或恶意内容可长期影响后续回答；客户隐私可能被聚合保存且无法追踪来源 |
| P1-11 | 显性风险 | **未声明外部内容的“数据/指令”边界**：知识库、文件、网页、用户资料和历史记忆都可能进入上下文，但没有明确要求把其中的文本视为不可信数据，也没有提示注入检测或二次确认 | `SOUL.md` 的 browser/file/memory；`USER.md`；`MEMORY.md` | 恶意知识库文章或客户消息可植入“忽略规则”“读取文件”“发送邮件”等指令，诱导 Agent 偏离职责或调用高权限工具 |
| P1-12 | 权限 | **多 Agent 隔离只有声明、没有可审计配置**：项目概览声称每个 Agent 有独立 workspace 和 SQLite 状态目录，但 Registry 中没有 workspace、state path、permission 或跨 Agent 访问策略 | Project Overview；`AGENTS.md` 的 Agent Registry | 无法验证 Agent A 是否真的不能读取 Agent B 的记忆或文件；在真实实现中可能发生横向数据访问 |

---

## 五、P2（10 项）

| # | 类型 | 问题概要 | 工件依据 | 可能影响 |
| ---- | ---- | ---- | ---- | ---- |
| P2-1 | 缺陷 | **工件清单数量不一致**：章节标题写“4 core file types”，正文实际展示 6 类文件，并把 `USER.md` 标为 optional、`MEMORY.md` 标为 runtime-generated | Logical Artifact Inventory | 评审范围、加载顺序和必备文件集无法确定，影响配置校验与测试覆盖 |
| P2-2 | 缺陷 | **Front Matter 规范不统一**：SOUL 使用 `name/description/model`，AGENTS 只有 `version`，USER 使用 `version/user_id`，IDENTITY 使用 `created/updated`，HEARTBEAT 使用 `schedule/timezone`，MEMORY 使用 `last_updated` | 六类工件的 Front Matter | 无法用统一 Schema 校验；字段缺失时的默认值和升级兼容策略不明确 |
| P2-3 | 缺陷 | **示例 Markdown 围栏嵌套错误**：AGENTS.md 和 HEARTBEAT.md 在 `markdown` 外层围栏中直接使用 `yaml`/`javascript` 三层反引号，导致外层围栏提前闭合 | AGENTS.md 与 HEARTBEAT.md 的代码块 | 文档渲染、复制和自动抽取可能截断工件内容；测试用例本身的可审计性下降 |
| P2-4 | 缺陷 | **模型配置硬编码在人格文件**：`model: claude-sonnet-4-5` 写在 SOUL Front Matter，没有模型回退、超时、token 预算或成本上限 | SOUL.md 的 Front Matter | 更换模型需要修改人格文件；模型不可用时没有降级策略，配置职责混杂 |
| P2-5 | 缺陷 | **身份信息重复且资源路径不可移植**：SOUL 与 IDENTITY 都定义姓名、角色和语气；头像使用绝对路径 `/assets/avatar-helper.png` | SOUL.md；IDENTITY.md | 两处修改容易不同步；绝对路径在多工作区部署时可能失效，也不利于资源隔离 |
| P2-6 | 缺陷 | **时间与选择条件存在歧义**：`created_after: 'yesterday 18:00'`、`last_login: '< 3 days ago'`、`signup_date: '< 7 days ago'` 都缺少明确时区、比较边界和解析格式 | HEARTBEAT.md | 跨时区运行、夏令时切换或边界数据可能产生错误任务集合；结果难以复现 |
| P2-7 | 缺陷 | **客服输出契约偏弱**：除语气示例外，没有回答结构、知识来源引用、置信度、无法确认时的升级、敏感信息脱敏或渠道格式要求 | SOUL.md 的 Response Guidelines 与 Tone Examples | 不同轮次的回答质量和证据透明度不一致；难以判断答案是否来自受支持文档 |
| P2-8 | 缺陷 | **可观测性不足**：没有记录路由命中原因、交接上下文、Skill 调用结果、记忆写入来源、定时任务开始/结束状态或失败原因 | AGENTS.md；HEARTBEAT.md；MEMORY.md | 出现错路由、重复外联或错误记忆时难以定位责任链，也无法进行有效回归审计 |
| P2-9 | 缺陷 | **测试建议缺少预期结果与夹具**：测试项描述了“验证路由”“验证隔离”“验证热更新”，但没有输入消息、期望 Agent、失败判定、隔离样本或并发场景数据 | Test Suggestions | 测试不可直接执行，也无法据此证明路由和隔离真的成立 |
| P2-10 | 缺陷 | **评测样例自身未完成**：所有 Evaluation Dimensions 复选框为空，Scoring Criteria 的 Score/Notes 为空；元数据缺少 Commit SHA 和逐文件源码 URL，采集方式仅说明为摘要 | Evaluation Dimensions、Scoring Criteria、Metadata | 结果无法固定到具体版本，后续源码变化会导致结论漂移；样例也不能直接用于批量自动评分 |

---

## 六、优先修复建议

1. **先闭合路由图（P0-1、P1-1、P1-2、P1-5、P1-6）：** 为 Registry 中每个目标 Agent 补齐定义，移除或实现 `billing-agent`、`tech-support`、`sales-manager`；把路由表改成可校验的结构化 YAML，并为每个渠道声明唯一绑定、优先级、默认 Agent 和交接契约。
2. **把权限从提示词提升为运行时控制（P0-2、P1-7、P1-12）：** 为 `shell` 设置命令白名单、工作目录、超时和网络/文件权限；为 `file` 设置允许根目录；为每个 Agent 配置独立 workspace、state path 和跨 Agent ACL，不能只依赖“read-only”这句话。
3. **先解决用户数据边界（P0-3、P1-10、P1-11）：** 明确 `USER.md` 是所有者资料、客户资料还是会话资料，并改为按用户/租户/会话隔离；为外部内容增加“不可信数据”标记，禁止其直接改变系统规则或触达高权限工具。
4. **对外部动作采用 fail-closed（P0-4、P1-8、P1-9）：** 定时任务默认只生成草稿或 dry-run；实际发送前要求目标用户同意、收件人白名单、发送上限、幂等键和人工审批，并为所有外部调用增加超时、重试上限和失败告警。
5. **最后补齐工件工程化（P2-1 至 P2-10）：** 统一 Front Matter Schema、修复嵌套代码围栏、集中模型配置、补充路由/交接/记忆审计字段，并把测试建议改造成带输入、预期结果和失败判定的可执行用例。

---

## 七、补充说明

1. **交叉验证：** P0-1、P1-1、P1-2、P1-3、P1-5、P1-6 相互印证，说明“Agent Registry ↔ 渠道绑定 ↔ Intent 路由 ↔ Handoff”四层契约没有形成闭环；当前最关键的不是继续增加人格描述，而是先把配置关系变成可解析、可校验、可测试的单一事实源。

2. **风险叠加：** P0-2 的 Shell 能力、P1-10/P1-11 的记忆与外部内容污染、P0-4 的外联能力可能组成一条完整风险链：不可信消息诱导 Agent 读取资料或写入记忆，再借助定时任务对外发送。应把“读取敏感数据、写入长期记忆、发起外部通信”视为高风险动作，分别施加权限和确认门槛。

3. **文档自身完整度：** 评分表、复选框、Commit SHA、源码 URL 和逐文件采集路径均未补齐。这些属于测试用例自身的未完成项，不改变上述 26 项工件问题，但会显著降低复现性和不同评测者之间的一致性。

4. **优点保留：** 采用纯 Markdown、职责分文件、Registry 集中配置和 Git 友好的文本差异，方向是合理的；若补齐结构化 Schema、隔离配置和外部动作治理，该套件可以作为非技术用户配置多 Agent 的良好模板。
