# TC-005 OpenClaw 组合工件审查报告

- **审查对象**：`TC-005-openclaw-file-based-agents.md`
- **审查日期**：2026-10-21
- **审查类型**：静态缺陷审查、权限审查、安全与合规风险审查
- **审查结论**：**不通过。不可直接作为部署模板、Agent 安全基线或评测评分基线。**
- **综合评分**：**1.5 / 5（高风险）**
- **上线建议**：先修复全部 P0 和 P1，再补充可执行配置、权限矩阵、数据流与验证证据。

---

## 1. 执行摘要

该工件较好地展示了文件型 Agent 的概念形态，但示例与 OpenClaw 当前官方架构存在关键偏差，且缺少真正生效的权限、租户隔离、数据治理和审计设计。

### 1.1 阻断级问题

1. **文件职责写错**：把 `AGENTS.md` 描述为多 Agent 路由配置。官方定义中，`AGENTS.md` 是工作区操作约定；多 Agent 路由应放在 OpenClaw 配置的 `agents.entries` 与 `bindings` 中。
2. **使用已退役机制**：`HEARTBEAT.md` 已被官方标记为退役文件，新工作区不再创建，运行时也不再读取。
3. **权限边界不是权限边界**：“shell: read-only” 只是自然语言描述，不能阻止读取密钥、访问宿主文件或执行破坏性命令。
4. **客户数据隔离缺失**：单个 `USER.md` 和 `MEMORY.md` 被用于多通道客服 Agent，可能导致不同客户之间的画像、历史与记忆串线。
5. **间接提示注入路径完整**：浏览器、文件、记忆、消息发送同时存在，却没有不可信内容隔离、工具降权、出站审批或域名白名单。

### 1.2 风险分布

| 等级 | 数量 | 含义 |
|---|---:|---|
| P0 阻断 | 4 | 会导致架构失真、越权、数据泄漏或安全事故 |
| P1 高 | 10 | 上线前必须修复 |
| P2 中 | 9 | 应在发布前修复或明确接受风险 |
| P3 低 | 1 | 文档质量与评分方法问题 |
| **合计** | **24** | |

---

## 2. 审查范围与方法

### 2.1 审查范围

- 仅一个工件：`TC-005-openclaw-file-based-agents.md`，共 381 行。
- 包含 6 个示例文件段落、1 套评估维度、1 套评分表、若干测试建议。
- 未发现可执行的 OpenClaw 配置、测试代码、运行日志或部署产物。

### 2.2 审查方法

1. 逐行检查文档结构、围栏、引用、路由定义和内部一致性。
2. 对 Markdown 做实际解析，确认渲染层级与代码块边界。
3. 对照 OpenClaw 官方仓库和官方文档核验文件职责、权限模型、心跳机制、记忆与安全控制。
4. 按“症状 → 来源 → 后果 → 修复”形成可执行结论。
5. 以 P0/P1/P2/P3 分级，不使用单纯的“看起来安全/不安全”判断。

### 2.3 外部核验依据

| 主题 | 官方依据 |
|---|---|
| 官方仓库 | <https://github.com/openclaw/openclaw> |
| Agent 工作区文件地图 | <https://docs.openclaw.ai/concepts/agent-workspace> |
| SOUL 定义 | <https://docs.openclaw.ai/concepts/soul> |
| AGENTS 模板 | <https://docs.openclaw.ai/reference/templates/AGENTS> |
| HEARTBEAT 退役说明 | <https://docs.openclaw.ai/reference/templates/HEARTBEAT> |
| 多 Agent 路由与 `bindings` | <https://docs.openclaw.ai/gateway/config-agents/entries-and-multi-agent> |
| 多 Agent 沙箱与工具限制 | <https://docs.openclaw.ai/tools/multi-agent-sandbox-tools> |
| 工具与 Agent 权限 | <https://docs.openclaw.ai/gateway/security/tool-permissions> |
| 安全加固基线 | <https://docs.openclaw.ai/gateway/security/hardened-baseline> |
| 提示注入防护 | <https://docs.openclaw.ai/gateway/security/prompt-injection> |
| 访问控制与 DM 隔离 | <https://docs.openclaw.ai/gateway/security/access-control> |
| 记忆来源与删除 | <https://docs.openclaw.ai/concepts/memory-provenance> |
| 密钥与本地存储 | <https://docs.openclaw.ai/gateway/security/secrets-and-storage> |
| 速率限制 | <https://docs.openclaw.ai/gateway/security/rate-limiting> |

> 说明：本次审查为静态审查，未部署 OpenClaw，也未执行工件中的伪代码。因此，文中“缺少控制”均指工件未提供控制设计或可验证配置，不代表底层 OpenClaw 缺乏相应能力。

---

## 3. 缺陷、权限与风险清单

| ID | 等级 | 维度 | 位置 | 问题 | 主要影响 |
|---|---|---|---|---|---|
| P0-01 | P0 | 架构事实 | 71-140, 209-258 | `AGENTS.md` 被误作路由配置，`HEARTBEAT.md` 已退役 | 工件无法按官方架构落地 |
| P0-02 | P0 | 权限 | 51-55, 314-318 | “只读 shell”依赖提示词，不是强制权限 | 宿主文件、密钥和命令执行风险 |
| P0-03 | P0 | 隐私 | 82-108, 142-180, 260-293 | 单用户画像和记忆用于多用户、多通道客服 | 跨客户数据泄漏与记忆污染 |
| P0-04 | P0 | AI 安全 | 52-55, 224-256, 260-293 | 不可信内容可影响带外发能力的 Agent | 间接提示注入与数据外传 |
| P1-01 | P1 | 路由 | 82-139, 229-255 | 未定义 Agent、角色冲突、通道目标不一致 | 消息误路由、丢失或越权 |
| P1-02 | P1 | 隔离 | 19, 314-318, 327 | 宣称隔离，但无 workspace、sandbox、session 与 Agent 间限制 | Agent 间越权与信息混合 |
| P1-03 | P1 | 出站操作 | 229-255 | 自动通知与批量邮件无审批、同意、限流、幂等 | 垃圾邮件、误发、合规风险 |
| P1-04 | P1 | 访问控制 | 82-108, 142-180 | 未设计 Gateway 认证、DM 配对、allowlist、群组门控 | 未授权用户可触发 Agent |
| P1-05 | P1 | 数据治理 | 21, 147-179, 260-293 | PII、对话摘要与记忆缺少分类、加密、保留和删除策略 | 隐私与合规风险 |
| P1-06 | P1 | 配置完整性 | 353-355 | 热重载无签名、审批、原子发布和回滚 | 未授权或误操作改变 Agent 行为 |
| P1-07 | P1 | 模型配置 | 29-34, 224-256 | 模型写在 SOUL frontmatter，未体现官方 Agent 模型配置 | 模型选择失效，安全与成本失控 |
| P1-08 | P1 | 供应链 | 324-327 | 共享 `~/.openclaw/skills` 无来源、签名和 Agent 白名单 | 恶意 Skill 进入所有 Agent |
| P1-09 | P1 | 审计 | 260-293, 319-322 | “纯 Markdown”不等于审计，缺少操作与来源证据 | 无法追责、取证和回滚 |
| P1-10 | P1 | 可追溯性 | 3-9 | GitHub 地址不存在，缺少提交哈希与文档版本 | 工件不可复核，易基于过期信息 |
| P2-01 | P2 | Markdown | 71-180, 209-293 | 嵌套围栏破坏渲染，`USER.md`/`MEMORY.md` 被吞入代码块 | 文档结构失真，规则难以阅读 |
| P2-02 | P2 | 一致性 | 18, 25, 260, 297-327 | 标题称 4 类核心文件，实际列 6 类 | 分类与评分口径不一致 |
| P2-03 | P2 | 一致性 | 15, 209-258, 319-322 | 宣称“纯 Markdown、无代码”，示例却含 JS | “可审计纯文本”结论失真 |
| P2-04 | P2 | 配置语法 | 88-124, 199 | 电话标识、Slack 键、Agent 名和头像路径不符合示例语义 | 配置解析失败或目标错配 |
| P2-05 | P2 | 失效模式 | 352-355 | “损坏配置优雅降级”可能让安全规则静默消失 | 失败开放，安全边界失效 |
| P2-06 | P2 | 评估设计 | 297-341 | 评估维度无权限、安全、隐私、审计硬门槛，评分表为空 | 高风险工件可能获得高分 |
| P2-07 | P2 | 测试 | 345-360 | 只有测试建议，无安全、越权、注入和删除测试 | 无法证明控制有效 |
| P2-08 | P2 | 可靠性 | 224-256 | 外部调用无超时、重试、幂等、死信和失败告警 | 重复发送、漏发和任务卡死 |
| P2-09 | P2 | 隐私表述 | 20-21 | “所有数据本地存储”容易被理解为数据不离开设备 | 用户对数据流向产生错误预期 |
| P3-01 | P3 | 评分方法 | 331-341 | 权重缺乏依据，安全项完全缺席 | 评测结果不可比较、不可审计 |

---

## 4. P0 阻断项详述

### P0-01：核心文件职责与生命周期写错

**症状**

- 第 71-140 行把 `AGENTS.md` 定义为多 Agent 路由注册表，并使用 `soul_file`、`channels`、`bindings`、关键词路由等字段。
- 第 209-258 行把 `HEARTBEAT.md` 作为定时任务配置。
- 官方 `AGENTS.md` 是工作区操作约定，不控制工具可用性，也不承担全局多 Agent 路由。
- 官方多 Agent 路由使用配置中的 `agents.entries` 和 `bindings`，按 `channel`、`accountId`、`peer` 等字段匹配。
- 官方已明确 `HEARTBEAT.md` 退役，不再被新工作区创建，也不再在运行时读取。

**来源**

- `TC-005-openclaw-file-based-agents.md:71-140`
- `TC-005-openclaw-file-based-agents.md:209-258`
- <https://docs.openclaw.ai/reference/templates/AGENTS>
- <https://docs.openclaw.ai/gateway/config-agents/entries-and-multi-agent>
- <https://docs.openclaw.ai/reference/templates/HEARTBEAT>

**后果**

- 按工件实现时，路由不会生效，定时任务不会被当前运行时读取。
- 整个“多 Agent 文件套件”的核心架构说明失真。
- 后续评分、测试和比较均建立在错误前提上。

**修复**

1. 将多 Agent 路由迁移到真实的 Gateway 配置，使用 `agents.entries`、`bindings`、`accountId`、`peer`。
2. 将 `AGENTS.md` 改为工作区操作规则，不承担路由注册。
3. 删除 `HEARTBEAT.md` 作为当前配置的表述，改用官方 automation/monitor scratch 或 cron 机制。
4. 在 Metadata 中记录所依据的 OpenClaw 提交哈希与文档日期。

---

### P0-02：“只读 shell”不是可执行的权限控制

**症状**

- 第 55 行写有 `shell: Run diagnostic commands (read-only)`。
- 第 314-318 行只把“权限边界”作为评估项，没有给出强制策略。
- 工件没有 `tools.allow`、`tools.deny`、`sandbox`、`workspaceAccess`、`fs.workspaceOnly`、`exec.security` 等实际控制。

**来源**

- `TC-005-openclaw-file-based-agents.md:51-55`
- `TC-005-openclaw-file-based-agents.md:314-318`
- <https://docs.openclaw.ai/gateway/security/tool-permissions>
- <https://docs.openclaw.ai/concepts/agent-workspace>

**后果**

- 自然语言中的“只读”不能约束命令行为。读取环境变量、SSH 密钥、`.env`、配置和日志仍可能发生。
- 工作区只是默认工作目录，不是硬沙箱；未启用沙箱时，绝对路径仍可能访问宿主。
- 若 Agent 同时具备消息、浏览器或文件工具，可将读取到的数据外传。

**修复**

1. 默认拒绝 `exec`、`process`、`write`、`edit`、`apply_patch`、`browser`。
2. 需要工具时使用 Agent 级 `tools.allow` 与 `tools.deny`，不要用提示词声明。
3. 需要文件读取时启用 sandbox，设置 `scope: "agent"` 和 `workspaceAccess: "ro"` 或 `"none"`。
4. 配置 `tools.fs.workspaceOnly: true`，并明确允许目录，拒绝符号链接逃逸。
5. 将 `exec.security` 设为 `deny`，或至少使用严格命令白名单与人工审批。

---

### P0-03：客户画像与长期记忆存在跨用户串线

**症状**

- 一个客服 Agent 同时绑定 WhatsApp、Telegram、Slack，并列出“回忆客户偏好和历史”的 memory 能力。
- `USER.md` 仅包含一个固定用户 `Alex Chen` 和 `user_12345`。
- `MEMORY.md` 是 Agent 级长期记忆，并包含对话摘要、客户洞察和模式统计。
- 工件没有说明客户级租户、会话级作用域、记忆命名空间或数据访问校验。

**来源**

- `TC-005-openclaw-file-based-agents.md:82-108`
- `TC-005-openclaw-file-based-agents.md:142-180`
- `TC-005-openclaw-file-based-agents.md:260-293`
- <https://docs.openclaw.ai/concepts/agent-workspace>
- <https://docs.openclaw.ai/gateway/security/access-control>

**后果**

- 如果同一 Agent 处理多个客户，`USER.md` 和 `MEMORY.md` 的上下文可能被错误地注入到其他客户会话。
- 计费、邮箱、语言偏好、历史问题等敏感信息可能泄漏。
- 恶意用户可向共享记忆写入错误事实，污染后续客服判断。

**修复**

1. 明确部署模式：单用户 Agent 还是多租户客服系统。
2. 多租户场景必须实现 `tenant_id`、`customer_id`、`session_id` 三段式命名空间。
3. 客户画像不得放在 Agent 级共享 `USER.md`，应放入按租户隔离的受控数据层。
4. `MEMORY.md` 仅用于主私有会话，不对共享群聊或不同客户注入。
5. 增加跨租户访问测试、记忆写入来源校验和删除验证。

---

### P0-04：间接提示注入可触达外发工具

**症状**

- Agent 可搜索知识库、读文件、读记忆。
- Agent 还具备客服回复、Slack 发布和邮件发送能力。
- 工件没有区分可信系统指令、客户输入、知识库网页、文件和记忆内容。
- 没有 Reader Agent、内容来源标记、外发审批、域名白名单或发送范围限制。

**来源**

- `TC-005-openclaw-file-based-agents.md:52-55`
- `TC-005-openclaw-file-based-agents.md:224-256`
- `TC-005-openclaw-file-based-agents.md:260-293`
- <https://docs.openclaw.ai/gateway/security/prompt-injection>

**后果**

- 被投毒的知识库页面或客户消息可诱导 Agent 读取敏感文件并发送到外部渠道。
- 若消息工具允许跨上下文发送，默认策略可能扩大到跨会话或跨渠道。
- 提示词中的“NEVER share internal documentation”无法构成硬边界。

**修复**

1. 将知识库阅读交给只读 Reader Agent，禁止其使用 shell、浏览器任意导航和外发工具。
2. 对网页、邮件、附件、记忆内容使用来源标记和不可信内容包装。
3. 主 Agent 只接收结构化摘要，不直接接收未经处理的整页内容。
4. 设置 `tools.message.crossContext.allowWithinProvider: false` 和 `allowAcrossProviders: false`。
5. 对邮箱发送、Slack 发布和跨渠道通知采用草稿或人工审批。
6. 浏览器配置域名白名单，禁用任意 URL 和任意方法。

---

## 5. P1 高风险项

### P1-01：路由目标未定义且规则互相冲突

第 99-101 行把 “pricing question” 交给 `support-main`，但第 132 行把 “pricing” 交给 `sales-assistant`。第 130-131 行引用未注册的 `billing-agent`、`tech-support`，第 101 行引用 `sales-manager`，第 230 行引用 `support-manager`。第 120、124 行还引用了未在对应 Agent 通道中声明的 `@SalesBot`、`#sales`。

**后果**：路由结果依赖实现细节，可能出现误路由、无限转交、消息丢失或进入不存在目标。

**修复**：建立闭集 Agent 注册表；所有目标必须存在于注册表；增加启动期引用完整性校验；定义无匹配、冲突、超时和人工兜底规则。

### P1-02：多 Agent 隔离声明没有对应控制

第 19 行和 314-318 行直接宣称“独立工作区、状态隔离、无跨 Agent 访问”，但示例没有 workspace、sandbox、session visibility、Agent 间消息白名单，也没有共享 Skill 访问控制。

官方安全文档指出：Agent 间消息默认开启，会话可见性和沙箱范围需要显式配置；未沙箱 Agent 可能读取其他 Agent 的会话。共享 Skill 也可能成为跨 Agent 扩散路径。

**修复**：为每个 Agent 明确 `workspace`、`sandbox.scope: "agent"`、`tools.sessions.visibility`、`tools.agentToAgent.enabled` 或 allowlist；将 Skill 按 Agent 白名单加载；把隔离声明改为可执行配置。

### P1-03：自动外发缺少授权与业务保护

第 229-255 行会通知负责人、发布 Slack 摘要并向停滞用户批量发送邮件。工件没有收件人授权、退订、发送频率、内容模板审核、幂等键、失败重试、黑名单或人工审批。

**后果**：重复邮件、骚扰用户、品牌受损、邮件域名信誉下降，甚至在错误对象上泄露账户状态。

**修复**：默认生成草稿或审批任务；按发件人、租户和收件人设置配额；增加 suppression list、幂等键、冷却期和审计记录；禁止在无明确同意时自动营销触达。

### P1-04：缺少外部访问的认证与授权设计

工件覆盖 WhatsApp、Telegram、Slack、邮件和 in-app，但没有 Gateway 认证、DM 配对、allowlist、群组 mention 门控、`session.dmScope` 或命令授权。

**后果**：未授权用户可能触发 Agent、读取共享会话上下文或调用命令；多用户 DM 默认可能共享主会话。

**修复**：启用 Gateway token 或更强认证；DM 使用 pairing/allowlist；群组使用 mention gating 和 context visibility；共享收件箱设置 `session.dmScope: "per-channel-peer"`；配置冷却、限额和失败锁止。

### P1-05：PII 和敏感信息缺少生命周期管理

第 150-179 行包含姓名、语言、交互历史、计费问题、渠道偏好等个人信息。第 260-293 行包含客户洞察和对话摘要。工件未定义敏感级别、加密、访问者、保留期限、导出、更正、删除和备份清理。

**后果**：无法满足数据最小化、访问审计、删除请求和保留期限要求；本地存储也可能被宿主用户、备份或日志读取。

**修复**：建立数据分级；PII 不入公开仓库；限制 Agent 级读取范围；启用静态加密和目录权限；定义保留期；使用官方记忆来源与删除机制；日志和诊断默认脱敏。

### P1-06：热重载会成为高权限配置变更入口

第 355 行把“修改 SOUL.md 后无需重启生效”视为优点，但未设计签名、变更审批、原子替换、语义校验、回滚和告警。

**后果**：错误或恶意修改可立即改变人格、边界、路由提示和工具使用倾向；缺失旧的边界规则时可能直接影响线上行为。

**修复**：配置变更走代码审查和审批；校验 Schema 与引用完整性；使用原子写入和版本化发布；保留上一个稳定版本；检测非预期变更并触发告警。

### P1-07：模型配置位置与 Agent 安全等级不清

第 33 行将 `model` 放入 SOUL frontmatter。官方示例将模型配置放在 `agents.entries.<agentId>.model`。工件没有说明该字段是否生效，也没有回退模型、成本上限、上下文限制和模型权限。

**后果**：可能实际使用默认模型；若默认模型较弱，会增加提示注入和工具误用风险；成本和可用性不可预测。

**修复**：在真实 Agent 配置中声明主模型与回退模型；选择适合工具型 Agent 的安全等级；设置调用预算、上下文限制和失败策略；在工件中标注该配置不是 SOUL 的自然语言内容。

### P1-08：共享 Skill 目录缺少供应链防护

第 327 行把 `~/.openclaw/skills` 作为共享扩展机制，但没有版本固定、来源验证、签名、审查和 Agent 级白名单。

**后果**：一个被篡改的 Skill 可影响所有复用它的 Agent，形成横向扩散。

**修复**：仅从受信来源安装；固定版本和哈希；安装前审查脚本与网络访问；按 Agent 配置 `skills` allowlist；定期扫描和更新。

### P1-09：缺少真正的审计与来源证据

“纯 Markdown、可读、Git 可追溯”只能说明静态文件可追踪，不能证明 Agent 在运行时的工具调用、外发动作、审批、记忆来源和权限拒绝都有记录。

**修复**：记录 Agent ID、租户、会话、操作者、工具名、参数摘要、结果、审批人和时间；对记忆写入保留来源；对外发操作生成不可篡改事件；使用日志脱敏、保留策略和导出接口。

### P1-10：来源元数据不可复核

第 5 行给出的 `github.com/openclaw-foundation/openclaw` 在 GitHub API 返回 404。公开官方仓库为 `github.com/openclaw/openclaw`。工件还缺少 commit SHA、版本号、文档抓取时间和许可证文件路径。

**后果**：读者无法确认工件依据的是哪一版行为，后续审查和复现会失效。

**修复**：更正仓库地址；记录 commit SHA、OpenClaw 版本、抓取日期；为关键结论逐条附官方文档链接；区分官方事实、设计建议和示例假设。

---

## 6. P2 与 P3 问题

### P2-01：Markdown 围栏层级错误

实际 Markdown 解析结果显示：

- `USER.md` 标题落在无标签代码块中，从第 139 行延伸到第 180 行。
- `MEMORY.md` 标题及其示例被一个无标签代码块吞入，影响第 257-293 行。

根因是多个同深度三反引号嵌套。修复方式是外层使用四反引号，内层使用三反引号，或缩进内层示例并统一代码块闭合。

### P2-02：文件分类数量前后不一致

第 25 行写“4 core file types”，但实际列出 SOUL、AGENTS、USER、IDENTITY、HEARTBEAT、MEMORY 六类。官方工作区还包含 BOOT、BOOTSTRAP、daily memory、skills 等文件。应改为“6 类示例文件”或明确“4 个核心 + 2 个扩展”。

### P2-03：“纯 Markdown、无代码”与示例矛盾

第 15 行称无代码，HEARTBEAT 示例却包含 JavaScript。应改为“主体为 Markdown，自动化与路由由结构化配置或脚本承担”，并删除对“所有逻辑工件都是纯 Markdown”的绝对表述。

### P2-04：示例标识语法不可直接使用

- `+1-555-SUPPORT`、`+1-555-SALES` 不是有效 E.164 号码。
- YAML 中未加引号的 `#support`、`#sales` 会被解析为注释。
- `@SalesBot` 未在 Agent 注册中声明。
- 头像 `/assets/avatar-helper.png` 不是官方建议的 workspace 相对路径、HTTP(S) URL 或 data URI。
- `user_id`、`soul_file` 等字段未证明属于官方 Schema。

### P2-05：损坏配置不应“优雅降级”

第 355 行建议损坏 Markdown 时优雅降级。对于人格文件可以降级，对于权限、路由、安全边界和客户数据配置应失败关闭。建议区分“非安全配置降级”和“安全配置阻断”，并在缺失关键边界时禁止工具调用。

### P2-06：评分体系会奖励不安全设计

评估维度只有文件组织、Markdown、可维护性、隔离、可审计性、扩展性，缺少认证、授权、最小权限、提示注入、数据分类、出站审批、速率限制、密钥管理、供应链和删除机制。评分表也没有实际分数与证据列。

建议新增硬门槛：

- 任一项 P0 未关闭，总分直接判为不通过。
- 安全与隐私维度合计不低于 40%。
- 每项评分必须附测试或配置证据。

### P2-07：测试建议不足以证明安全

现有测试仅覆盖 schema、路由、隔离、启动、热重载、损坏文件和并发。缺少以下测试：

1. 未注册路由目标导致启动失败。
2. 跨租户读取 `USER.md`、`MEMORY.md` 和会话失败。
3. 提示注入无法触发文件读取和外发。
4. 禁止工具返回明确拒绝。
5. 外发邮件需要审批且不会重复发送。
6. 记忆删除后索引、缓存和摘要同步清理。
7. 配置回滚后旧权限立即失效。
8. 速率限制、配额和失败锁止生效。

### P2-08：自动化缺少可靠性控制

第 224-256 行的外部调用没有超时、重试、退避、幂等键、死信、告警和部分失败处理。建议每一项外部副作用定义唯一业务键，采用至少一次投递加幂等接收，并在失败时停止后续高风险步骤。

### P2-09：本地优先表述会误导数据流向

“所有数据存储本地”只描述存储位置，不等于数据不离开设备。消息会进入 WhatsApp、Telegram、Slack 等平台，提示会发送给模型提供方。应在文档中明确数据流、第三方处理者、诊断数据和遥测开关。

### P3-01：评分权重缺少依据

20%/15%/20%/20%/15%/10% 的权重没有说明来源，也没有区分“可展示性”和“生产安全性”。建议引入威胁模型和业务影响作为权重依据，并公开每个维度的评分证据。

---

## 7. 建议的最小权限矩阵

以下矩阵可作为修复后的默认基线。原则是默认拒绝、按 Agent 最小授权、外发操作默认审批。

| 能力 | support-main | sales-assistant | onboarding-guide | 强制条件 |
|---|---|---|---|---|
| 读取当前会话消息 | 允许 | 允许 | 允许 | 仅当前租户/会话 |
| 读取知识库 | 允许 | 允许 | 允许 | 只读、域名或目录白名单 |
| 读取 `USER.md` | 禁止共享 | 禁止共享 | 禁止共享 | 改为租户隔离存储 |
| 读取 `MEMORY.md` | 仅私有主会话 | 仅私有主会话 | 仅私有主会话 | 不注入共享群聊 |
| 写入长期记忆 | 受控 | 受控 | 受控 | 来源、租户、审批和去重 |
| 文件工具 | 禁止 | 禁止 | 禁止 | 如必需，sandbox 只读且限定目录 |
| `exec` / shell | 禁止 | 禁止 | 禁止 | 不建议为客服 Agent 开启 |
| 任意浏览器 | 禁止 | 禁止 | 禁止 | 仅允许白名单域名与只读方法 |
| 当前会话回复 | 允许 | 允许 | 允许 | 绑定来源渠道 |
| 跨会话消息 | 禁止 | 禁止 | 禁止 | `allowWithinProvider: false` |
| 跨渠道消息 | 禁止 | 禁止 | 禁止 | `allowAcrossProviders: false` |
| 邮件发送 | 仅草稿或审批 | 仅草稿或审批 | 仅草稿或审批 | 有同意、配额和退订 |
| Slack 发布 | 仅审批 | 仅审批 | 仅审批 | 绑定频道、限频、可撤销 |
| 读取密钥 | 禁止 | 禁止 | 禁止 | 密钥移出工作区 |
| 安装或更新 Skill | 禁止 | 禁止 | 禁止 | 管理员审批与版本固定 |

---

## 8. 数据分类与保护建议

| 数据级别 | 示例 | 最低控制 |
|---|---|---|
| L1 公开 | 公开知识库文章 | 只读、可缓存、来源可追溯 |
| L2 内部 | 产品规则、运营指标 | 内部访问控制、禁止公网分享 |
| L3 机密 | 客户画像、会话历史、计费信息、邮箱 | 租户隔离、加密、最小化、保留期、删除机制 |
| L4 受限 | 渠道 token、模型 API key、OAuth 凭据 | 移出 workspace、SecretRef、最小范围、轮换、禁止日志输出 |

建议默认规则：

1. `USER.md`、`MEMORY.md` 和会话历史按 L3 处理。
2. 任何 L3 数据进入模型上下文前必须通过租户和用途校验。
3. 外发内容进行敏感字段扫描，至少覆盖邮箱、电话号、内部 URL、token 和订单号。
4. 删除请求同时清理主文件、索引、缓存、摘要和派生记忆。
5. 日志与诊断默认脱敏，原始日志仅安全管理员可读。

---

## 9. 关键威胁模型

| 威胁 | 攻击路径 | 当前工件缺口 | 建议控制 |
|---|---|---|---|
| 身份伪造 | 用户通过 WhatsApp、Telegram、邮件冒充客户 | 无 sender identity、pairing、allowlist | 渠道身份绑定、配对、跨渠道 identity link 校验 |
| 配置篡改 | 修改 SOUL/AGENTS 或共享 Skill | 无签名、审批、回滚 | 代码审查、Schema 校验、原子发布、哈希固定 |
| 数据泄漏 | 浏览器/文件读取后经消息或邮件外传 | 工具组合过强，无外发审批 | Reader Agent、sandbox、域名白名单、外发 DLP |
| 跨租户串线 | 共享 USER/MEMORY 和默认主会话 | 无租户命名空间与 DM 隔离 | tenant scope、per-channel-peer、独立 workspace |
| 权限提升 | shell、文件、Skill 或 Agent 间消息 | “只读”仅靠提示词 | 默认 deny、Agent 级 allowlist、禁 Agent 间消息 |
| 滥用与成本 | 群聊或 DM 大量触发模型与外部 API | 无速率限制、配额、预算 | 入站限流、模型预算、每日额度、失败锁止 |
| 不可追责 | 无操作日志、记忆来源和审批记录 | 只有 Git 可追溯 | 结构化审计日志、记忆 provenance、不可篡改导出 |
| 供应链 | 恶意 Skill 或配置更新 | 共享 Skill 无来源要求 | 签名、版本固定、隔离测试、按 Agent 白名单 |

---

## 10. 修复优先级与验收门槛

### 10.1 建议修复顺序

1. **先修正事实与结构**：P0-01、P1-10、P2-01、P2-02、P2-03。
2. **再收紧权限与数据边界**：P0-02、P0-03、P0-04、P1-02、P1-04。
3. **补齐运行时保护**：P1-03、P1-05、P1-06、P1-07、P1-08。
4. **补齐审计与验证**：P1-09、P2-05、P2-06、P2-07、P2-08。
5. **最后修正表达与评分方法**：P2-09、P3-01。

### 10.2 发布前必须具备的证据

- [ ] 正确的官方仓库地址、commit SHA 与文档日期。
- [ ] 可解析、可校验的 OpenClaw 配置，而非 Markdown 伪配置。
- [ ] Agent 注册表闭集校验，所有路由目标存在且无冲突。
- [ ] 每个 Agent 的 workspace、sandbox、tools、skills、session visibility 配置。
- [ ] 租户隔离、DM 隔离和记忆命名空间设计。
- [ ] 不可信内容处理流程与 Reader Agent 边界。
- [ ] 外发审批、速率限制、幂等、退订和审计证据。
- [ ] PII 数据分类、保留、导出、删除和备份清理流程。
- [ ] 密钥管理方案，确保密钥不在 workspace 和提示词中。
- [ ] 提示注入、跨租户读取、工具拒绝、重复发送、删除和回滚测试结果。
- [ ] Markdown 渲染检查，确保所有示例文件结构正确。
- [ ] 安全维度占主导的评分规则，以及每项评分的证据链接。

### 10.3 最终判定

**当前工件不能进入生产，也不应作为安全 Agent 的正面样本。** 在修复 P0/P1 之前，最多可作为“待验证的概念草稿”，不能作为“OpenClaw 文件型 Agent 最佳实践基线”。

---

## 11. 结论

该工件的主要问题不是文案细节，而是**把自然语言描述误当成运行时权限，把共享文件误当成租户隔离，把旧机制误当成当前架构**。这三类问题叠加后，会给多通道客服 Agent 带来跨客户泄漏、提示注入、外发失控和不可审计风险。

建议按以下顺序推进：

1. 重写架构事实与配置示例。
2. 建立默认拒绝的 Agent 权限矩阵。
3. 实现租户与会话隔离。
4. 增加不可信内容处理和外发审批。
5. 用可执行测试和审计证据替换现有测试建议。

完成后应重新进行一轮独立安全审查，不以文档自评分替代验证。

---

## 附录 A：P0/P1 风险矩阵

| 风险 | 可能性 | 影响 | 等级 |
|---|---|---|---|
| 跨客户画像/记忆泄漏 | 高 | 高 | 极高 |
| 任意文件或命令访问 | 中 | 高 | 极高 |
| 提示注入触发外发 | 高 | 高 | 极高 |
| 未授权用户触发 Agent | 中 | 高 | 高 |
| 自动邮件误发或重复发送 | 中 | 高 | 高 |
| 路由到未定义 Agent | 高 | 中 | 高 |
| 共享 Skill 供应链污染 | 中 | 高 | 高 |
| 配置热重载被篡改 | 中 | 高 | 高 |
| 记忆删除不完整 | 高 | 中 | 高 |
| 审计证据缺失 | 高 | 中 | 中高 |

## 附录 B：本次未执行的项目

- 未启动 OpenClaw Gateway。
- 未运行工件中的 JavaScript 伪代码。
- 未进行真实 WhatsApp、Telegram、Slack 或邮件通道联调。
- 未验证第三方平台条款、数据跨境和具体司法辖区合规义务。
- 未对 OpenClaw 源码本身做全面安全审计，本报告只审查该组合工件的设计与表述。
