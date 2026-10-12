# TC-005: OpenClaw - File-Based Multi-Logical-Artifact Agent Suite

## Metadata
- **Source Project**: OpenClaw (formerly Clawdbot/Moltbot)
- **GitHub**: github.com/openclaw-foundation/openclaw
- **License**: MIT
- **Artifact Type**: File-based logical artifacts (Markdown config-driven)
- **Collection Date**: 2026-10-10
- **Collection Method**: Documentation summary + architecture analysis

---

## Project Overview

OpenClaw is a **config-first** AI Agent framework that defines Agents through pure Markdown files, with no code writing required. Each Agent's "brain" is composed of multiple Markdown files, forming a complete logical artifact suite.

### Key Features
- **File as configuration**: SOUL.md + AGENTS.md + USER.md + IDENTITY.md
- **Multi-Agent isolation**: each Agent has an independent workspace and state directory
- **Messaging platform integration**: 25+ channels including WhatsApp, Telegram, Slack, Discord
- **Local-first**: all data stored locally, supports offline operation with Ollama

---

## Logical Artifact Inventory (4 core file types)

### 1. SOUL.md - Personality & Boundaries (≈ System Prompt)

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

### 2. AGENTS.md - Multi-Agent Routing Configuration

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

### 3. USER.md - User Model & Preferences (optional)

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

### 4. IDENTITY.md - Agent Identity

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

### 5. HEARTBEAT.md - Scheduled Task Configuration

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

### 6. MEMORY.md - Long-Term Memory (runtime-generated)

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

## Evaluation Dimensions (file-based artifacts specific)

### 1. File Organization Clarity
- [ ] Clear responsibility boundaries across the 4 core file types
- [ ] Unified naming conventions (SOUL.md, AGENTS.md, etc.)
- [ ] Reasonable directory structure for multi-Agent scenarios

### 2. Markdown Structure
- [ ] YAML frontmatter used properly
- [ ] Clear heading hierarchy (# ## ###)
- [ ] Appropriate use of lists, code blocks, and other formats

### 3. Configuration Maintainability
- [ ] Key configuration centrally managed (AGENTS.md)
- [ ] Separation of environment variables from file configuration
- [ ] Version-control friendly (plain-text diff)

### 4. Multi-Agent Isolation
- [ ] Independent workspace for each Agent
- [ ] Session state isolation (SQLite per agent)
- [ ] Clear permission boundaries (no cross-Agent access)

### 5. Auditability
- [ ] All logical artifacts are pure Markdown, readable and editable
- [ ] Change history traceable (git)
- [ ] Runtime behavior predictable (configuration as code)

### 6. Extensibility
- [ ] Low cost to create new Agents (copy template)
- [ ] Config-driven onboarding of new channels
- [ ] Skill sharing mechanism (~/.openclaw/skills)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| File Organization Clarity | 20% | | |
| Markdown Structure | 15% | | |
| Configuration Maintainability | 20% | | |
| Multi-Agent Isolation | 20% | | |
| Auditability | 15% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. **Schema validation**: verify SOUL.md frontmatter completeness
2. **Routing tests**: simulate messages and verify AGENTS.md routing rules
3. **Isolation tests**: verify that Agent A cannot access Agent B's memory

### Runtime Tests
1. **Startup loading**: Gateway correctly parses all Markdown files on startup
2. **Hot reload**: modifying SOUL.md takes effect without restart
3. **Error handling**: corrupted Markdown files degrade gracefully

### Multi-Agent Collaboration Tests
1. **@Mention routing**: user @sales is correctly routed to sales-assistant
2. **Handoff**: support-main correctly hands off to billing-agent
3. **Concurrency**: multiple Agents simultaneously handle messages from different channels

---

## Comparison with Other Test Cases

| Feature | TC-004 (GPT Researcher) | TC-005 (OpenClaw) |
|------|------------------------|-------------------|
| **Artifact Form** | Python code + Prompts | Markdown files |
| **Orchestration** | LangGraph state machine | Gateway routing |
| **Multi-Agent Relationship** | Pipeline collaboration | Isolated parallelism |
| **Editability** | Requires code changes | Plain-text editing |
| **Applicable Scenario** | Complex research tasks | Messaging customer service/assistant |

---

## Notes

- The **MIT license** allows full quotation and modification
- This is a typical representative of **file-based Agents**, vs code-based Agents (such as GPT Researcher)
- Suitable as an evaluation baseline for **non-technical users** creating Agents
- Demonstrates the "configuration as code" philosophy applied in the Agent domain
