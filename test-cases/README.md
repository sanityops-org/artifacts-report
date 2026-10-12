# SanityOps Agent 逻辑工件评估用例集

## 项目概述

本文件夹包含用于评估开源 Agent 项目中**逻辑工件**（System Prompt / Skill / Tool Schema）的测试用例。

- **目标规模**: 30~50 个 Agent，不低于 300 个逻辑工件
- **当前进度**: 6 个评估用例（覆盖 3 种类型 × 4 种组织形式）
- **采集标准**: 非代码开发类 Agent、Apache-2.0/MIT 优先、结构完整可审计

---

## 文件夹结构

```
test-cases/
├── README.md                          # 本文件
├── single-artifact/                   # 单工件用例（基础）
│   ├── TC-001-gpt-researcher-system-prompt.md
│   ├── TC-002-anthropics-pdf-skill.md
│   └── TC-003-mcp-tool-schema.json
├── multi-agent-suite/                 # 多 Agent 协作套件
│   └── TC-004-gpt-researcher-multi-agent-suite.md
├── file-based/                        # 文件式配置 Agent
│   └── TC-005-openclaw-file-based-agents.md
└── role-library/                      # 专门化角色库
    └── TC-006-agency-agents-marketing-suite.md
```

---

## 用例文件清单

### 📁 single-artifact/ - 单工件用例（基础）

| 编号 | 文件名 | 来源项目 | 工件类型 | 许可证 | 状态 |
|------|--------|----------|----------|--------|------|
| TC-001 | [TC-001-gpt-researcher-system-prompt.md](./single-artifact/TC-001-gpt-researcher-system-prompt.md) | gpt-researcher | System Prompt | Apache-2.0 | ✅ 已完成 |
| TC-002 | [TC-002-anthropics-pdf-skill.md](./single-artifact/TC-002-anthropics-pdf-skill.md) | anthropics/skills | Skill | Proprietary | ✅ 已完成 |
| TC-003 | [TC-003-mcp-tool-schema.json](./single-artifact/TC-003-mcp-tool-schema.json) | gpt-researcher | Tool Schema | Apache-2.0 | ✅ 已完成 |

### 📁 multi-agent-suite/ - 多 Agent 协作套件

| 编号 | 文件名 | 来源项目 | 套件类型 | 工件数量 | 许可证 | 状态 |
|------|--------|----------|----------|----------|--------|------|
| TC-004 | [TC-004-gpt-researcher-multi-agent-suite.md](./multi-agent-suite/TC-004-gpt-researcher-multi-agent-suite.md) | gpt-researcher | 多 Agent 协作系统 | 13 | Apache-2.0 | ✅ 已完成 |

**特点**: 8 个角色通过 LangGraph 状态机协作完成研究任务（Planning → Research → Review → Write → Publish）

### 📁 file-based/ - 文件式配置 Agent

| 编号 | 文件名 | 来源项目 | 套件类型 | 工件数量 | 许可证 | 状态 |
|------|--------|----------|----------|----------|--------|------|
| TC-005 | [TC-005-openclaw-file-based-agents.md](./file-based/TC-005-openclaw-file-based-agents.md) | OpenClaw | 文件式多 Agent | 6 | MIT | ✅ 已完成 |

**特点**: Markdown 文件即配置（SOUL.md/AGENTS.md/USER.md/IDENTITY.md/HEARTBEAT.md/MEMORY.md），无需编写代码

### 📁 role-library/ - 专门化角色库

| 编号 | 文件名 | 来源项目 | 套件类型 | 工件数量 | 许可证 | 状态 |
|------|--------|----------|----------|----------|--------|------|
| TC-006 | [TC-006-agency-agents-marketing-suite.md](./role-library/TC-006-agency-agents-marketing-suite.md) | agency-agents | 专门化角色套件 | 6 | MIT | ✅ 已完成 |

**特点**: Marketing 部门 6 个角色（Content Creator/Reddit Community Builder/Growth Hacker/Social Media Strategist/SEO Specialist/LinkedIn Content Creator）

---

## 分类说明

### 为什么这样分类？

| 分类 | 适用场景 | 评估重点 | 典型用户 |
|------|---------|---------|---------|
| **single-artifact** | 评估单个 Prompt/Skill/Tool 的质量 | 指令清晰度、Schema 完整性、示例质量 | Agent 开发者 |
| **multi-agent-suite** | 评估多 Agent 协作系统的设计 | 角色分工、协作流程、状态管理 | 系统架构师 |
| **file-based** | 评估文件式配置的灵活性 | 文件组织、配置维护、可审计性 | 运维/配置管理者 |
| **role-library** | 评估专门化角色的实用性 | 角色定义、工作流程、成功指标 | 业务运营人员 |

### 分类 vs 非分类的对比

```
未分类（扁平）              分类（层级）
    │                         │
TC-001.md                    single-artifact/
TC-002.md                    ├── TC-001.md
TC-003.md                    ├── TC-002.md
TC-004.md                    └── TC-003.md
TC-005.md                    
TC-006.md                    multi-agent-suite/
                             └── TC-004.md
                             
                             file-based/
                             └── TC-005.md
                             
                             role-library/
                             └── TC-006.md
```

**分类优势**:
- 按使用场景快速定位
- 同类用例便于对比分析
- 支持批量评估（如只评估 file-based 类型）
- 清晰的评估维度映射

---

## 评估维度对照表

### 单工件评估维度（single-artifact/）

| 工件类型 | 核心评估维度 | 权重分配 |
|----------|-------------|----------|
| **System Prompt** | 指令清晰度、结构化程度、引用处理、质量控制、可测试性 | 25%/20%/25%/20%/10% |
| **Skill** | 元数据完整性、触发条件、指令结构化、代码示例质量、可维护性 | 15%/20%/25%/25%/15% |
| **Tool Schema** | Schema 完整性、描述清晰度、集成兼容性、示例质量、可扩展性 | 25%/20%/25%/20%/10% |

### 多工件套件评估维度

#### multi-agent-suite/

| 维度 | 说明 | 权重 |
|------|------|------|
| 角色分工清晰度 | 8 个 Agent 职责边界清晰，无重叠 | 20% |
| 协作流程完整性 | 5 阶段流程覆盖完整，质量门控健全 | 25% |
| Prompt 一致性 | 跨角色术语、格式、标准统一 | 15% |
| Tool Schema 模块化 | 工具按功能域分组，参数定义完整 | 20% |
| 可观测性 | ResearchState 包含完整上下文，错误追踪 | 10% |
| 扩展性 | 新 Agent/Tool 接入成本低 | 10% |

#### file-based/

| 维度 | 说明 | 权重 |
|------|------|------|
| 文件组织清晰度 | 4 类核心文件职责边界清晰 | 20% |
| Markdown 结构化程度 | YAML frontmatter 规范，标题层级清晰 | 15% |
| 配置可维护性 | 关键配置集中，版本控制友好 | 20% |
| 多 Agent 隔离性 | 每个 Agent 独立 workspace 和状态 | 20% |
| 可审计性 | 纯 Markdown 可读可编辑，变更可追溯 | 15% |
| 扩展性 | 新 Agent 创建成本低，渠道接入配置驱动 | 10% |

#### role-library/

| 维度 | 说明 | 权重 |
|------|------|------|
| 角色定义完整性 | Identity、Mission、Rules 清晰可衡量 | 20% |
| 工作流程可操作性 | 分阶段流程清晰，交付物模板完整 | 25% |
| 成功指标可量化 | 3-5 个核心 KPI，有基准值和目标值 | 20% |
| 输出模板实用性 | 提供可直接使用的模板，有 ✅/❌ 示例 | 15% |
| 跨角色协作性 | 角色间职责边界清晰，有 handoff 机制 | 10% |
| 非编码定位清晰度 | 所有交付物为内容/策略/运营，不涉及代码 | 10% |

---

## 推荐扩展项目（按分类）

### single-artifact/
- [ ] anthropics/skills - docx/xlsx/pptx Skill
- [ ] dontriskit/awesome-ai-system-prompts - System Prompt 合集
- [ ] MCP 官方仓库 - Tool Schema 标准参考

### multi-agent-suite/
- [ ] AG2 (AutoGen) - 多 Agent 协作框架
- [ ] CrewAI - 角色扮演多 Agent 系统
- [ ] LangGraph 官方示例 - 状态机模式

### file-based/
- [ ] OpenClaw 其他文件 - HEARTBEAT.md/MEMORY.md 详细用例
- [ ] ClawHub Skills - 社区贡献的 Skill 文件

### role-library/
- [ ] agency-agents Sales 部门 - Outbound Strategist/Deal Strategist
- [ ] agency-agents Community 部门 - Reddit/Twitter/Discord 运营角色
- [ ] agency-agents Product 部门 - PM/UX Researcher 角色

---

## 使用指南

### 快速定位

1. **评估单个 Prompt 质量** → `single-artifact/TC-001`
2. **评估多 Agent 协作设计** → `multi-agent-suite/TC-004`
3. **评估文件式配置方案** → `file-based/TC-005`
4. **评估业务角色定义** → `role-library/TC-006`

### 批量评估

```bash
# 评估所有 file-based 用例
ls file-based/*.md

# 对比同类用例
diff single-artifact/TC-001.md single-artifact/TC-002.md

# 统计各类用例数量
find . -name "TC-*.md" | wc -l
```

### 新增用例流程

1. 确定用例类型 → 选择对应文件夹
2. 复制模板结构 → 保持评估维度一致
3. 填写元信息 → 来源/许可/采集方式
4. 调整评估维度 → 根据具体类型微调权重
5. 更新 README → 添加到对应表格

---

## 许可说明

- **Apache-2.0 / MIT**: 可完整引用和修改
- **Proprietary**: 仅做结构大纲 + ≤10 行短引
- **泄露/逆向内容**: 仅内部测试，不宜对外发布

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-10-10 | 初始化，添加 3 个基础用例（System Prompt / Skill / Tool Schema 各一） |
| 2026-10-10 | 新增 3 个多工件套件用例（TC-004/005/006），覆盖多 Agent 协作、文件式 Agent、专门化角色套件 |
| 2026-10-10 | 重构文件夹结构，按类型二次分类（single-artifact/multi-agent-suite/file-based/role-library） |

---

*Generated for SanityOps Artifacts Report*
