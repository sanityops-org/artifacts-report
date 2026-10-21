# TC-004: GPT Researcher Multi-Agent - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: gpt-researcher (assafelovic/gpt-researcher)
- **Submodule**: multi_agents/ (LangGraph version)
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent suite (8 roles × 3 artifact types)
- **Collection Date**: 2026-10-10
- **Collection Method**: Documentation summary + code structure analysis

---

## Project Overview

GPT Researcher Multi-Agent is a **complete Agent collaboration system** containing 8 specialized Agent roles, orchestrated through a LangGraph state machine to complete the full flow from research planning to report publication.

### 8 Agent Roles

| Role | Responsibility | Primary Artifact Type |
|------|------|-------------|
| **Chief Editor** | Main coordinator, manages the LangGraph state machine | System Prompt + Tool Schema |
| **Editor** | Plans the report outline and structure | System Prompt |
| **Researcher** | Executes deep research (wraps GPTResearcher) | System Prompt + Tool Schema |
| **Reviewer** | Validates the correctness of research results | System Prompt + evaluation criteria |
| **Revisor** | Revises drafts based on feedback | System Prompt |
| **Writer** | Compiles and writes the final report | System Prompt |
| **Publisher** | Publishes multi-format reports | System Prompt + Tool Schema |
| **Human** | Human review node (human-in-the-loop) | Interaction configuration |

---

## Logical Artifact Inventory

### 1. System Prompts (8)

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

### 2. Tool Schemas (3 core tool sets)

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

### 3. Configuration Artifacts (2)

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

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 8 Agents with clear responsibility boundaries, no overlap
- [ ] Each role's System Prompt clearly defines its unique positioning
- [ ] Inter-role dependencies (input/output) are clearly defined

### 2. Workflow Completeness
- [ ] 5-stage workflow covers the complete research lifecycle
- [ ] State machine transitions (LangGraph) clearly defined
- [ ] Quality gating (Reviewer → Revisor loop) mechanism is sound

### 3. Prompt Consistency
- [ ] Terminology usage is consistent across roles
- [ ] Output format specifications are unified (JSON Schema)
- [ ] Global configurations (citation format, quality standards) are shared

### 4. Tool Modularity
- [ ] Tools grouped by functional domain (Research/Review/Publish)
- [ ] Parameter definitions complete, including types/constraints/defaults
- [ ] Tool-to-role mapping is clear

### 5. Observability
- [ ] ResearchState contains complete context
- [ ] Error logging and stage tracking
- [ ] Human intervention point (Human Agent) reasonably designed

### 6. Extensibility
- [ ] Cost of onboarding new Agent roles
- [ ] Schema compatibility for new Tools
- [ ] Flexibility of configuration-driven approach (task.json)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: from query input to multi-format report output
2. **Human intervention**: insert feedback at the planning/review stages
3. **Error recovery**: simulate Researcher failure and verify retry mechanism

### Unit Tests
1. **Per-Agent independence**: test the Editor's outline generation separately
2. **Tool invocation**: verify Tool Schema parameter validation
3. **State transitions**: state passing between LangGraph nodes

### Stress Tests
1. **Parallel research**: concurrent processing at max_sections=10
2. **Long reports**: performance of generating 50+ page reports
3. **Multi-source mixing**: Web + Local + MCP retrieval simultaneously

---

## Relationship to Other Test Cases

| Component of This Case | Corresponding Standalone Case | Relationship |
|-----------|-------------|------|
| Researcher System Prompt | TC-001 | TC-001 is the single-Agent version; this case is the role within multi-Agent collaboration |
| MCP Tool Schema | TC-003 | TC-003 is a generic MCP configuration; this case is the instance integrated into multi-Agent |
| PDF Publication | TC-002 | TC-002 is a Skill implementation; this case is the invocation target of the Publisher Agent |

---

## Notes

- The **Apache-2.0 license** allows full quotation and modification
- This suite demonstrates **best practices for multi-Agent systems**: role specialization + state machine orchestration + quality iteration
- Can serve as an evaluation baseline for **complex Agent systems** (vs the simple single-Agent scenario)
- The actual code resides in the `multi_agents/` directory; this case is a summary based on documentation and code structure
