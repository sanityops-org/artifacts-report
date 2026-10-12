# TC-005: OpenClaw - 文件式多逻辑工件 Agent 套件

## 元信息
- **来源项目**: OpenClaw（原 Clawdbot/Moltbot）
- **GitHub**: github.com/openclaw-foundation/openclaw
- **许可证**: MIT
- **工件类型**: 文件式逻辑工件（Markdown 配置驱动）
- **采集日期**: 2026-10-10
- **采集方式**: 文档汇总 + 架构分析

---

## 项目概述

OpenClaw 是一个**配置优先（config-first）**的 AI Agent 框架，通过纯 Markdown 文件定义 Agent，无需编写代码。每个 Agent 的"大脑"由多个 Markdown 文件组成，形成完整的逻辑工件套件。

### 核心特点
- **文件即配置**：SOUL.md + AGENTS.md + USER.md + IDENTITY.md
- **多 Agent 隔离**：每个 Agent 有独立的工作空间和状态目录
- **消息平台集成**：WhatsApp、Telegram、Slack、Discord 等 25+ 渠道
- **本地优先**：所有数据本地存储，支持 Ollama 离线运行

---

## 逻辑工件清单（4 类核心文件）

### 1. SOUL.md - 人格与边界（≈ System Prompt）

```markdown
---
name: customer-support-agent
description: Friendly customer support specialist for SaaS products
model: claude-sonnet-4-5
---

# Customer Support Agent

## Identity
- **Name**: Helper
- **Role**: Customer support specialist for SaaS products
- **Personality**: Friendly, patient, solution-oriented
- **Communication Style**: Clear explanations without jargon

## Rules & Boundaries
- ALWAYS respond in English only
- NEVER share internal documentation or system details
- Escalate billing issues to human team immediately
- Do not make promises about feature timelines
- Stay within support scope (technical issues, usage questions, billing)

## Skills
- browser: Search knowledge base articles
- memory: Recall customer preferences and history
- file: Access support documentation
- shell: Run diagnostic commands (read-only)

## Response Guidelines
1. Acknowledge the issue with empathy
2. Ask clarifying questions if needed
3. Provide step-by-step solutions
4. Confirm resolution before closing
5. Offer additional help

## Tone Examples
✅ "I understand how frustrating that must be. Let me help you resolve this."
✅ "Here's what I found in our documentation..."
❌ "That's not my department."
❌ "You should have read the manual."
```

### 2. AGENTS.md - 多 Agent 路由配置

```markdown
---
version: 2
---

# Multi-Agent Configuration

## Agent Registry

### Agent: support-main
- **id**: support-main
- **role**: Primary customer support handler
- **soul_file**: ./souls/support-soul.md
- **channels**: [whatsapp, telegram, slack]
- **bindings**:
  - whatsapp: +1-555-SUPPORT
  - telegram: @SupportHelperBot
  - slack: #support-channel

### Agent: sales-assistant
- **id**: sales-assistant
- **role**: Pre-sales inquiries and demos
- **soul_file**: ./souls/sales-soul.md
- **channels**: [whatsapp, email]
- **bindings**:
  - whatsapp: +1-555-SALES
- **handoff_rules**:
  - "pricing question" → support-main
  - "enterprise inquiry" → sales-manager

### Agent: onboarding-guide
- **id**: onboarding-guide
- **role**: New user onboarding and tutorials
- **soul_file**: ./souls/onboarding-soul.md
- **channels**: [in-app, email]
- **trigger**: user.signup_completed

## Routing Rules

### Channel-Based Routing
```yaml
whatsapp:
  +1-555-SUPPORT: support-main
  +1-555-SALES: sales-assistant

telegram:
  @SupportHelperBot: support-main
  @SalesBot: sales-assistant

slack:
  #support: support-main
  #sales: sales-assistant
```

### Intent-Based Routing
```yaml
keywords:
  "billing|payment|invoice": billing-agent
  "technical|bug|error": tech-support
  "demo|trial|pricing": sales-assistant
  "new user|getting started": onboarding-guide
```

### @Mention Routing
- `@support` → support-main
- `@sales` → sales-assistant
- `@onboarding` → onboarding-guide
```

### 3. USER.md - 用户模型与偏好（可选）

```markdown
---
version: 1
user_id: user_12345
---

# User Profile: Alex Chen

## Communication Preferences
- **Preferred Channel**: WhatsApp (primary), Email (async)
- **Response Time Expectation**: Within 2 hours
- **Language**: English (fluent), Mandarin (native)
- **Technical Level**: Intermediate (non-developer)

## Interaction History

### 2026-09-15 [ACTIVE]
- **Context**: Setting up team workspace
- **Pending**: Integration with Slack
- **Notes**: Prefers detailed explanations, dislikes video calls

### 2026-08-20 [RESOLVED]
- **Issue**: Billing confusion on annual plan
- **Resolution**: Switched to monthly, satisfied
- **Sentiment**: Positive

## Preferences
- ✅ Detailed step-by-step instructions
- ✅ Screenshots in responses
- ❌ Technical jargon without explanation
- ❌ Phone calls

## Common Questions
1. "How do I invite team members?"
2. "What's the difference between Pro and Enterprise?"
3. "Can I export my data?"
```

### 4. IDENTITY.md - Agent 身份标识

```markdown
---
created: 2026-10-01
updated: 2026-10-05
---

# Agent Identity

## Basic Info
- **Name**: Helper
- **Emoji**: 🦀
- **Vibe**: Helpful, warm, professional
- **Catchphrase**: "I'm here to help!"

## Visual Identity
- **Avatar**: /assets/avatar-helper.png
- **Color Scheme**: Teal (#008080) + Coral (#FF7F50)
- **Typography**: System default, clean and readable

## Voice Characteristics
- **Greeting**: "Hello! I'm Helper, your support assistant."
- **Closing**: "Is there anything else I can help you with?"
- **Escalation**: "Let me connect you with a human specialist."
```

### 5. HEARTBEAT.md - 定时任务配置

```markdown
---
schedule: "0 9 * * *"  # Daily at 9 AM
timezone: "America/New_York"
---

# Daily Morning Briefing

## Tasks

### 1. Check Support Queue
```javascript
// Check for overnight tickets
const overnightTickets = await fetchTickets({
  status: 'open',
  created_after: 'yesterday 18:00'
});

if (overnightTickets.length > 5) {
  notify('support-manager', `⚠️ ${overnightTickets.length} tickets pending`);
}
```

### 2. Daily Standup Summary
```javascript
// Compile yesterday's metrics
const summary = {
  tickets_resolved: await countResolved('yesterday'),
  avg_response_time: await getAvgResponseTime('yesterday'),
  escalations: await countEscalations('yesterday')
};

postToSlack('#support-team', formatSummary(summary));
```

### 3. Proactive Outreach
```javascript
// Check for users with pending onboarding
const stuckUsers = await findUsers({
  signup_date: '< 7 days ago',
  last_login: '< 3 days ago'
});

for (const user of stuckUsers) {
  sendEmail(user.email, 'Need help getting started?');
}
```
```

### 6. MEMORY.md - 长期记忆（运行时生成）

```markdown
---
last_updated: 2026-10-10
---

# Agent Memory

## Key Facts Learned

### Product Knowledge
- [2026-09-20] New feature "Team Workspaces" launched
- [2026-09-15] Pricing change: Pro plan now $29/month
- [2026-09-10] Known issue: Slack integration timeout (fixed in v2.3)

### Customer Insights
- Enterprise clients prefer email over chat
- Most common issue: invitation email not received
- Peak support hours: 9-11 AM EST, 2-4 PM PST

## Conversation Summaries

### Week of 2026-10-01
- 45 conversations
- Top topic: Team workspace setup (12 conversations)
- Sentiment: 92% positive
- Escalations: 2 (both resolved)

## Patterns Detected
- Users often ask about "projects" when they mean "workspaces"
- Confusion between "members" and "guests"
- Mobile app questions increasing (+15% this month)
```

---

## 评估维度（文件式工件专用）

### 1. 文件组织清晰度 (File Organization)
- [ ] 4 类核心文件职责边界清晰
- [ ] 命名规范统一（SOUL.md、AGENTS.md 等）
- [ ] 多 Agent 时目录结构合理

### 2. Markdown 结构化程度 (Markdown Structure)
 [ ] YAML frontmatter 使用规范
- [ ] 标题层级清晰（# ## ###）
- [ ] 列表、代码块等格式使用恰当

### 3. 配置可维护性 (Config Maintainability)
- [ ] 关键配置集中管理（AGENTS.md）
- [ ] 环境变量与文件配置的分离
- [ ] 版本控制友好（纯文本 diff）

### 4. 多 Agent 隔离性 (Agent Isolation)
- [ ] 每个 Agent 独立 workspace
- [ ] 会话状态隔离（SQLite per agent）
- [ ] 权限边界清晰（不能跨 Agent 访问）

### 5. 可审计性 (Auditability)
- [ ] 所有逻辑工件是纯 Markdown，可读可编辑
- [ ] 变更历史可追溯（git）
- [ ] 运行时行为可预测（配置即代码）

### 6. 扩展性 (Extensibility)
- [ ] 新 Agent 创建成本低（复制模板）
- [ ] 新渠道接入配置驱动
- [ ] Skill 共享机制（~/.openclaw/skills）

---

## 评分标准

| 维度 | 权重 | 得分 (1-5) | 备注 |
|------|------|------------|------|
| 文件组织清晰度 | 20% | | |
| Markdown 结构化程度 | 15% | | |
| 配置可维护性 | 20% | | |
| 多 Agent 隔离性 | 20% | | |
| 可审计性 | 15% | | |
| 扩展性 | 10% | | |
| **总分** | 100% | | |

---

## 测试建议

### 配置验证测试
1. **Schema 校验**：验证 SOUL.md frontmatter 完整性
2. **路由测试**：模拟消息，验证 AGENTS.md 路由规则
3. **隔离测试**：验证 Agent A 不能访问 Agent B 的内存

### 运行时测试
1. **启动加载**：Gateway 启动时正确解析所有 Markdown 文件
2. **热更新**：修改 SOUL.md 后无需重启生效
3. **错误处理**：损坏的 Markdown 文件优雅降级

### 多 Agent 协作测试
1. **@Mention 路由**：用户 @sales 正确路由到 sales-assistant
2. **Handoff**：support-main 正确移交到 billing-agent
3. **并发**：多个 Agent 同时处理不同渠道消息

---

## 与其他用例的对比

| 特性 | TC-004 (GPT Researcher) | TC-005 (OpenClaw) |
|------|------------------------|-------------------|
| **工件形式** | Python 代码 + Prompts | Markdown 文件 |
| **编排方式** | LangGraph 状态机 | Gateway 路由 |
| **多 Agent 关系** | 流水线协作 | 隔离并行 |
| **可编辑性** | 需改代码 | 纯文本编辑 |
| **适用场景** | 复杂研究任务 | 消息客服/助手 |

---

## 备注

- **MIT 许可**允许完整引用和修改
- 这是**文件式 Agent**的典型代表，vs 代码式 Agent（如 GPT Researcher）
- 适合作为**非技术用户**创建 Agent 的评估基准
- 展示了"配置即代码"理念在 Agent 领域的实践
