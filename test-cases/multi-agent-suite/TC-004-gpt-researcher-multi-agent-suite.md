# TC-004: GPT Researcher Multi-Agent - 多逻辑工件套件评估用例

## 元信息
- **来源项目**: gpt-researcher (assafelovic/gpt-researcher)
- **子模块**: multi_agents/ (LangGraph 版本)
- **许可证**: Apache-2.0
- **工件类型**: 多 Agent 套件（8 个角色 × 3 类工件）
- **采集日期**: 2026-10-10
- **采集方式**: 文档汇总 + 代码结构分析

---

## 项目概述

GPT Researcher Multi-Agent 是一个**完整的 Agent 协作系统**，包含 8 个专门化的 Agent 角色，通过 LangGraph 状态机编排完成从研究规划到报告发布的全流程。

### 8 个 Agent 角色

| 角色 | 职责 | 主要工件类型 |
|------|------|-------------|
| **Chief Editor** | 主协调器，管理 LangGraph 状态机 | System Prompt + Tool Schema |
| **Editor** | 规划报告大纲和结构 | System Prompt |
| **Researcher** | 执行深度研究（封装 GPTResearcher） | System Prompt + Tool Schema |
| **Reviewer** | 验证研究结果的正确性 | System Prompt + 评估标准 |
| **Revisor** | 根据反馈修订草稿 | System Prompt |
| **Writer** | 编译并撰写最终报告 | System Prompt |
| **Publisher** | 发布多格式报告 | System Prompt + Tool Schema |
| **Human** | 人工审核节点（人在回路） | 交互配置 |

---

## 逻辑工件清单

### 1. System Prompts（8 个）

#### 1.1 Chief Editor (Orchestrator)
```python
# multi_agents/agents/orchestrator.py
system_message = """You are the Chief Editor of a research team. Your role is to:
1. Coordinate the multi-agent research workflow
2. Manage state transitions in the LangGraph pipeline
3. Delegate tasks to specialized agents (Editor, Researcher, Reviewer, etc.)
4. Ensure quality gates are passed before proceeding to next stage
5. Handle errors and edge cases gracefully

You have access to the following tools:
- init_research: Initialize research with query and configuration
- plan_sections: Delegate outline creation to Editor
- run_research: Trigger parallel section research
- review_draft: Validate research quality
- compile_report: Finalize and publish

Always maintain the shared ResearchState across all operations."""
```

#### 1.2 Editor (Planner)
```python
# multi_agents/agents/editor.py
system_message = """You are a senior research editor. Given a research query and initial findings:

1. Analyze the research question to identify key themes
2. Create a structured outline with 3-5 main sections
3. Assign priorities to each section (high/medium/low)
4. Define clear scope boundaries for each section
5. Ensure sections collectively answer the original question

Output format:
- Section title
- Key questions to address
- Expected content scope
- Priority level
- Estimated word count

Guidelines:
- Avoid overlapping content between sections
- Ensure logical flow from introduction to conclusion
- Consider counter-arguments and alternative perspectives"""
```

#### 1.3 Researcher
```python
# multi_agents/agents/researcher.py
system_message = """You are a specialized research agent. For each assigned section:

1. Conduct comprehensive web/local research using available retrievers
2. Gather diverse sources (minimum 5 per section)
3. Extract key facts, statistics, and expert opinions
4. Synthesize findings into a coherent draft
5. Cite all sources using the specified format (APA/MLA/etc.)

Tools available:
- conduct_research: Execute search and data collection
- write_draft: Generate section content from findings

Quality criteria:
- Factual accuracy (verify claims with multiple sources)
- Source diversity (avoid over-reliance on single source)
- Currency (prioritize recent information)
- Objectivity (present multiple perspectives)"""
```

#### 1.4 Reviewer
```python
# multi_agents/agents/reviewer.py
system_message = """You are a critical research reviewer. Evaluate each section draft against:

**Quality Criteria (Score 1-10):**
1. Factual accuracy - Are claims supported by evidence?
2. Completeness - Does it address all key questions?
3. Logical coherence - Is the argument structure sound?
4. Source quality - Are citations from credible sources?
5. Objectivity - Is the presentation balanced?

**Output format:**
{
  "overall_score": 7,
  "criteria_scores": {
    "accuracy": 8,
    "completeness": 6,
    "coherence": 7,
    "source_quality": 8,
    "objectivity": 7
  },
  "gaps_identified": ["missing counter-arguments", "insufficient data on X"],
  "revision_suggestions": ["Add statistics from Y source", "Clarify Z concept"],
  "approval_status": "needs_revision"  # or "approved"
}

Be thorough but constructive. If score < 7, provide specific revision guidance."""
```

#### 1.5 Revisor
```python
# multi_agents/agents/reviser.py
system_message = """You are a research reviser. Based on reviewer feedback:

1. Address each identified gap systematically
2. Incorporate suggested sources and data
3. Clarify ambiguous or unclear points
4. Strengthen weak arguments with additional evidence
5. Maintain original section scope while improving depth

**Process:**
- Review feedback item by item
- Prioritize high-impact revisions
- Preserve accurate content from original draft
- Update citations for new sources added
- Re-submit for re-review if major changes made

**Constraints:**
- Do not expand beyond original section scope
- Maintain consistent tone with other sections
- Ensure all new claims are properly sourced"""
```

#### 1.6 Writer
```python
# multi_agents/agents/writer.py
system_message = """You are the lead writer. Compile all revised sections into a cohesive report:

**Structure:**
1. Executive Summary (150-200 words)
2. Introduction (context + research question)
3. Main Sections (from Researcher outputs)
4. Conclusion (key findings + implications)
5. References (consolidated bibliography)

**Writing guidelines:**
- Ensure smooth transitions between sections
- Maintain consistent terminology throughout
- Write for target audience (technical vs general)
- Follow specified style guide (APA/MLA/etc.)
- Total length: 1500-2500 words

**Quality checks:**
- No orphan headings
- Proper citation format
- Table of contents alignment
- Cross-reference accuracy"""
```

#### 1.7 Publisher
```python
# multi_agents/agents/publisher.py
system_message = """You are a document publisher. Convert the final report to requested formats:

**Supported formats:**
- Markdown (.md) - default
- PDF (.pdf) - using reportlab/weasyprint
- Word (.docx) - using python-docx
- HTML (.html) - styled for web viewing

**Process:**
1. Apply format-specific styling
2. Generate table of contents (if requested)
3. Add header/footer with metadata
4. Embed images with proper captions
5. Validate output file integrity

**Metadata to include:**
- Report title
- Generation date
- Source count
- Word count
- Author/Organization"""
```

#### 1.8 Human (Human-in-the-Loop)
```python
# multi_agents/agents/human.py
system_message = """You are the human oversight interface. Present research findings for human review:

**Presentation format:**
- Research question summary
- Proposed outline (if at planning stage)
- Section drafts with quality scores
- Reviewer feedback summary
- Estimated completion time

**Interaction modes:**
1. Approve - Continue to next stage
2. Request revision - Loop back with feedback
3. Add guidance - Inject additional constraints
4. Cancel - Terminate workflow with summary

**Timeout handling:**
- Default approval after 24 hours
- Save state for async resumption
- Notify on critical decisions needed"""
```

---

### 2. Tool Schemas（3 个核心工具集）

#### 2.1 Research Tools
```json
{
  "name": "research_tools",
  "description": "Web and local document research capabilities",
  "tools": [
    {
      "name": "web_search",
      "parameters": {
        "query": {"type": "string", "description": "Search query"},
        "max_results": {"type": "integer", "default": 10},
        "source": {"type": "string", "enum": ["tavily", "google", "bing"]}
      }
    },
    {
      "name": "local_document_search",
      "parameters": {
        "query": {"type": "string"},
        "doc_path": {"type": "string"},
        "file_types": {"type": "array", "items": {"enum": ["pdf", "docx", "txt", "md"]}}
      }
    }
  ]
}
```

#### 2.2 Review Tools
```json
{
  "name": "review_tools",
  "description": "Quality validation and scoring",
  "tools": [
    {
      "name": "evaluate_draft",
      "parameters": {
        "draft_content": {"type": "string"},
        "criteria": {"type": "array", "items": {"enum": ["accuracy", "completeness", "coherence", "sources", "objectivity"]}},
        "guidelines": {"type": "array", "items": {"type": "string"}}
      },
      "returns": {
        "score": {"type": "number", "minimum": 1, "maximum": 10},
        "feedback": {"type": "string"}
      }
    }
  ]
}
```

#### 2.3 Publication Tools
```json
{
  "name": "publication_tools",
  "description": "Multi-format report generation",
  "tools": [
    {
      "name": "export_markdown",
      "parameters": {"content": "string", "filename": "string"}
    },
    {
      "name": "export_pdf",
      "parameters": {"content": "string", "style": {"type": "string", "enum": ["academic", "business"]}}
    },
    {
      "name": "export_docx",
      "parameters": {"content": "string", "template": "string"}
    }
  ]
}
```

---

### 3. Configuration Artifacts（2 个）

#### 3.1 Task Configuration (task.json)
```json
{
  "query": "Is AI in a hype cycle?",
  "model": "gpt-4o",
  "max_sections": 3,
  "publish_formats": {
    "markdown": true,
    "pdf": true,
    "docx": true
  },
  "include_human_feedback": false,
  "source": "web",
  "follow_guidelines": true,
  "guidelines": [
    "The report MUST fully answer the original question",
    "The report MUST be written in apa format",
    "The report MUST be written in english"
  ],
  "verbose": true
}
```

#### 3.2 State Schema (LangGraph)
```python
# multi_agents/memory/research.py
class ResearchState(TypedDict):
    # Core
    query: str
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Planning
    outline: List[Dict]  # [{"title": str, "questions": [], "priority": str}]
    
    # Research
    sections: Dict[str, str]  # section_id -> draft content
    sources: List[Dict]  # [{"url": str, "title": str, "content": str}]
    
    # Review
    review_scores: Dict[str, int]  # section_id -> score
    revision_notes: Dict[str, List[str]]
    
    # Writing
    final_report: str
    
    # Status
    current_phase: Literal["planning", "researching", "reviewing", "revising", "writing", "publishing", "complete"]
    error_log: Annotated[List[str], operator.add]
```

---

## 评估维度（多工件套件专用）

### 1. 角色分工清晰度 (Role Clarity)
- [ ] 8 个 Agent 职责边界清晰，无重叠
- [ ] 每个角色的 System Prompt 明确其独特定位
- [ ] 角色间依赖关系（输入/输出）定义清楚

### 2. 协作流程完整性 (Workflow Completeness)
- [ ] 5 阶段流程覆盖完整研究生命周期
- [ ] 状态机转换（LangGraph）定义明确
- [ ] 质量门控（Reviewer → Revisor 循环）机制健全

### 3. Prompt 一致性 (Prompt Consistency)
- [ ] 跨角色术语使用一致
- [ ] 输出格式规范统一（JSON Schema）
- [ ] 引用格式、质量标准等全局配置共享

### 4. Tool Schema 模块化 (Tool Modularity)
- [ ] 工具按功能域分组（Research/Review/Publish）
- [ ] 参数定义完整，包含类型/约束/默认值
- [ ] 工具与角色的映射关系清晰

### 5. 可观测性 (Observability)
- [ ] ResearchState 包含完整上下文
- [ ] 错误日志和阶段追踪
- [ ] 人工介入点（Human Agent）设计合理

### 6. 扩展性 (Extensibility)
- [ ] 新 Agent 角色的接入成本
- [ ] 新 Tool 的 Schema 兼容性
- [ ] 配置驱动（task.json）的灵活性

---

## 评分标准

| 维度 | 权重 | 得分 (1-5) | 备注 |
|------|------|------------|------|
| 角色分工清晰度 | 20% | | |
| 协作流程完整性 | 25% | | |
| Prompt 一致性 | 15% | | |
| Tool Schema 模块化 | 20% | | |
| 可观测性 | 10% | | |
| 扩展性 | 10% | | |
| **总分** | 100% | | |

---

## 测试建议

### 端到端测试
1. **完整流程**: 从 query 输入到多格式报告输出
2. **人工介入**: 在 planning/review 阶段插入反馈
3. **错误恢复**: 模拟 Researcher 失败，验证重试机制

### 单元测试
1. **各 Agent 独立**: 单独测试 Editor 的大纲生成
2. **Tool 调用**: 验证 Tool Schema 的参数校验
3. **状态转换**: LangGraph 节点间的状态传递

### 压力测试
1. **并行研究**: max_sections=10 时的并发处理
2. **长报告**: 生成 50+ 页报告的性能
3. **多源混合**: Web + Local + MCP 同时检索

---

## 与其他用例的关系

| 本用例组件 | 对应独立用例 | 关系 |
|-----------|-------------|------|
| Researcher System Prompt | TC-001 | TC-001 是单 Agent 版本，本用例是多 Agent 协作中的角色 |
| MCP Tool Schema | TC-003 | TC-003 是通用 MCP 配置，本用例是集成到多 Agent 中的实例 |
| PDF Publication | TC-002 | TC-002 是 Skill 实现，本用例是 Publisher Agent 的调用目标 |

---

## 备注

- **Apache-2.0 许可**允许完整引用和修改
- 该套件展示了**多 Agent 系统的最佳实践**：角色专业化 + 状态机编排 + 质量迭代
- 可作为**复杂 Agent 系统**的评估基准（vs 单 Agent 的简单场景）
- 实际代码位于 `multi_agents/` 目录，本用例基于文档和代码结构汇总
