# SanityOps Agent Logical Artifact Evaluation Test Case Set

## Project Overview

This folder contains test cases for evaluating the **logical artifacts** (System Prompt / Skill / Tool Schema) within open-source Agent projects.

- **Target Scale**: 30~50 Agents, no fewer than 300 logical artifacts
- **Current Progress**: 6 evaluation cases (covering 3 types × 4 organizational forms)
- **Collection Criteria**: Non-code-development Agents, Apache-2.0/MIT preferred, structurally complete and auditable

---

## Folder Structure

```
test-cases/
├── README.md                          # This file
├── single-artifact/                   # Single-artifact cases (basic)
│   ├── TC-001-gpt-researcher-system-prompt.md
│   ├── TC-002-anthropics-pdf-skill.md
│   └── TC-003-mcp-tool-schema.json
├── multi-agent-suite/                 # Multi-Agent collaboration suite
│   └── TC-004-gpt-researcher-multi-agent-suite.md
├── file-based/                        # File-configured Agents
│   └── TC-005-openclaw-file-based-agents.md
└── role-library/                      # Specialized role library
    └── TC-006-agency-agents-marketing-suite.md
```

---

## Test Case File List

### 📁 single-artifact/ - Single-artifact cases (basic)

| # | File Name | Source Project | Artifact Type | License | Status |
|------|--------|----------|----------|--------|------|
| TC-001 | [TC-001-gpt-researcher-system-prompt.md](./single-artifact/TC-001-gpt-researcher-system-prompt.md) | gpt-researcher | System Prompt | Apache-2.0 | ✅ Complete |
| TC-002 | [TC-002-anthropics-pdf-skill.md](./single-artifact/TC-002-anthropics-pdf-skill.md) | anthropics/skills | Skill | Proprietary | ✅ Complete |
| TC-003 | [TC-003-mcp-tool-schema.json](./single-artifact/TC-003-mcp-tool-schema.json) | gpt-researcher | Tool Schema | Apache-2.0 | ✅ Complete |

### 📁 multi-agent-suite/ - Multi-Agent collaboration suite

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-004 | [TC-004-gpt-researcher-multi-agent-suite.md](./multi-agent-suite/TC-004-gpt-researcher-multi-agent-suite.md) | gpt-researcher | Multi-Agent collaboration system | 13 | Apache-2.0 | ✅ Complete |

**Characteristics**: 8 roles collaborate through a LangGraph state machine to complete research tasks (Planning → Research → Review → Write → Publish)

### 📁 file-based/ - File-configured Agents

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-005 | [TC-005-openclaw-file-based-agents.md](./file-based/TC-005-openclaw-file-based-agents.md) | OpenClaw | File-based multi-Agent | 6 | MIT | ✅ Complete |

**Characteristics**: Markdown files are the configuration (SOUL.md/AGENTS.md/USER.md/IDENTITY.md/HEARTBEAT.md/MEMORY.md), no code writing required

### 📁 role-library/ - Specialized role library

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-006 | [TC-006-agency-agents-marketing-suite.md](./role-library/TC-006-agency-agents-marketing-suite.md) | agency-agents | Specialized role suite | 6 | MIT | ✅ Complete |

**Characteristics**: 6 Marketing department roles (Content Creator/Reddit Community Builder/Growth Hacker/Social Media Strategist/SEO Specialist/LinkedIn Content Creator)

---

## Classification Notes

### Why classify this way?

| Classification | Applicable Scenario | Evaluation Focus | Typical User |
|------|---------|---------|---------|
| **single-artifact** | Evaluate the quality of a single Prompt/Skill/Tool | Instruction clarity, Schema completeness, example quality | Agent developer |
| **multi-agent-suite** | Evaluate the design of a multi-Agent collaboration system | Role division, collaboration workflow, state management | System architect |
| **file-based** | Evaluate the flexibility of file-based configuration | File organization, configuration maintenance, auditability | Ops/config manager |
| **role-library** | Evaluate the practicality of specialized roles | Role definition, workflow, success metrics | Business operations staff |

### Classified vs Unclassified Comparison

```
Unclassified (flat)        Classified (hierarchical)
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

**Classification Advantages**:
- Quick location by usage scenario
- Easier comparison of same-type cases
- Supports batch evaluation (e.g., evaluate only the file-based type)
- Clear mapping to evaluation dimensions

---

## Evaluation Dimension Reference Table

### Single-artifact evaluation dimensions (single-artifact/)

| Artifact Type | Core Evaluation Dimensions | Weight Distribution |
|----------|-------------|----------|
| **System Prompt** | Instruction clarity, structure, citation handling, quality control, testability | 25%/20%/25%/20%/10% |
| **Skill** | Metadata completeness, trigger conditions, instruction structure, code example quality, maintainability | 15%/20%/25%/25%/15% |
| **Tool Schema** | Schema completeness, description clarity, integration compatibility, example quality, extensibility | 25%/20%/25%/20%/10% |

### Multi-artifact suite evaluation dimensions

#### multi-agent-suite/

| Dimension | Description | Weight |
|------|------|------|
| Role division clarity | 8 Agents with clear responsibility boundaries, no overlap | 20% |
| Workflow completeness | 5-stage workflow fully covered, sound quality gating | 25% |
| Prompt consistency | Unified terminology, format, and standards across roles | 15% |
| Tool Schema modularity | Tools grouped by functional domain, complete parameter definitions | 20% |
| Observability | ResearchState contains complete context, error tracking | 10% |
| Extensibility | Low cost to integrate new Agents/Tools | 10% |

#### file-based/

| Dimension | Description | Weight |
|------|------|------|
| File organization clarity | Clear responsibility boundaries across the 4 core file types | 20% |
| Markdown structure | Standard YAML frontmatter, clear heading hierarchy | 15% |
| Configuration maintainability | Centralized key configuration, version-control friendly | 20% |
| Multi-Agent isolation | Independent workspace and state for each Agent | 20% |
| Auditability | Pure Markdown readable and editable, traceable changes | 15% |
| Extensibility | Low cost to create new Agents, config-driven channel onboarding | 10% |

#### role-library/

| Dimension | Description | Weight |
|------|------|------|
| Role definition completeness | Identity, Mission, Rules clear and measurable | 20% |
| Workflow actionability | Clear phased workflow, complete deliverable templates | 25% |
| Quantifiable success metrics | 3-5 core KPIs with baseline and target values | 20% |
| Output template utility | Ready-to-use templates with ✅/❌ examples | 15% |
| Cross-role collaboration | Clear responsibility boundaries with handoff mechanism | 10% |
| Non-coding positioning clarity | All deliverables are content/strategy/operations, no code | 10% |

---

## Recommended Projects for Expansion (by classification)

### single-artifact/
- [ ] anthropics/skills - docx/xlsx/pptx Skill
- [ ] dontriskit/awesome-ai-system-prompts - System Prompt collection
- [ ] MCP official repositories - Tool Schema standard reference

### multi-agent-suite/
- [ ] AG2 (AutoGen) - multi-Agent collaboration framework
- [ ] CrewAI - role-playing multi-Agent system
- [ ] LangGraph official examples - state machine pattern

### file-based/
- [ ] Other OpenClaw files - HEARTBEAT.md/MEMORY.md detailed cases
- [ ] ClawHub Skills - community-contributed Skill files

### role-library/
- [ ] agency-agents Sales department - Outbound Strategist/Deal Strategist
- [ ] agency-agents Community department - Reddit/Twitter/Discord operations roles
- [ ] agency-agents Product department - PM/UX Researcher roles

---

## Usage Guide

### Quick Location

1. **Evaluate a single Prompt's quality** → `single-artifact/TC-001`
2. **Evaluate multi-Agent collaboration design** → `multi-agent-suite/TC-004`
3. **Evaluate file-based configuration approach** → `file-based/TC-005`
4. **Evaluate business role definitions** → `role-library/TC-006`

### Batch Evaluation

```bash
# Evaluate all file-based cases
ls file-based/*.md

# Compare same-type cases
diff single-artifact/TC-001.md single-artifact/TC-002.md

# Count cases of each type
find . -name "TC-*.md" | wc -l
```

### New Case Workflow

1. Determine case type → choose the corresponding folder
2. Copy the template structure → keep evaluation dimensions consistent
3. Fill in meta information → source/license/collection method
4. Adjust evaluation dimensions → fine-tune weights by specific type
5. Update README → add to the corresponding table

---

## License Notes

- **Apache-2.0 / MIT**: May be fully quoted and modified
- **Proprietary**: Structure outline only + ≤10-line short quotes
- **Leaked/reverse-engineered content**: Internal testing only, not for public release

---

## Changelog

| Date | Update |
|------|----------|
| 2026-10-10 | Initialized, added 3 basic cases (one each of System Prompt / Skill / Tool Schema) |
| 2026-10-10 | Added 3 multi-artifact suite cases (TC-004/005/006), covering multi-Agent collaboration, file-based Agents, and specialized role suites |
| 2026-10-10 | Restructured folder layout, secondary classification by type (single-artifact/multi-agent-suite/file-based/role-library) |

---

*Generated for SanityOps Artifacts Report*
