# SanityOps Agent Logical Artifact Evaluation Test Case Set

## Project Overview

This folder contains test cases for evaluating the **logical artifacts** (System Prompt / Skill / Tool Schema) within open-source Agent projects.

- **Target Scale**: 30~50 Agents, no fewer than 300 logical artifacts
- **Current Progress**: 44 evaluation cases (6 original + 37 migrated + 1 index)
- **Collection Criteria**: Non-code-development Agents, Apache-2.0/MIT preferred, structurally complete and auditable

---

## Folder Structure

```
test-cases/
├── README.md                          # This file
├── single-artifact/                   # Single-artifact cases (basic)
│   ├── TC-001-gpt-researcher-system-prompt.md
│   ├── TC-002-anthropics-pdf-skill.md
│   ├── TC-003-mcp-tool-schema.json
│   ├── TC-007-aider-system-prompts.md
│   ├── TC-008-cline-system-prompts.md
│   ├── TC-009-gemini-cli-system-prompts.md
│   ├── TC-010-opencode-system-prompts.md
│   ├── TC-011-mini-swe-agent-system-prompt.md
│   ├── TC-012-openhands-sdk-system-prompts.md
│   ├── TC-013-openai-codex-system-prompt.md
│   ├── TC-014-goose-system-prompts.md
│   ├── TC-015-qwen-code-skills.md
│   ├── TC-016-swe-agent-tool-schemas.md
│   ├── TC-017-smolagents-system-prompt.md
│   ├── TC-018-browser-use-system-prompt.md
│   ├── TC-019-deep-research-system-prompt.md
│   └── TC-020-smol-developer-system-prompt.md
├── multi-agent-suite/                 # Multi-Agent collaboration suite
│   ├── TC-004-gpt-researcher-multi-agent-suite.md
│   ├── TC-021-autogen-multi-agent-suite.md
│   ├── TC-022-ag2-multi-agent-suite.md
│   ├── TC-023-crewai-multi-agent-suite.md
│   ├── TC-024-camel-multi-agent-suite.md
│   ├── TC-025-openhands-multi-agent-suite.md
│   ├── TC-026-metagpt-multi-agent-suite.md
│   ├── TC-027-phidata-multi-agent-suite.md
│   ├── TC-028-superagi-multi-agent-suite.md
│   ├── TC-029-e2b-multi-agent-suite.md
│   └── TC-030-openinterpreter-multi-agent-suite.md
├── file-based/                        # File-configured Agents
│   ├── TC-005-openclaw-file-based-agents.md
│   ├── TC-031-nanobot-file-based-agents.md
│   ├── TC-032-hermes-agent-file-based-agents.md
│   ├── TC-033-openagent-file-based-agents.md
│   └── TC-034-mem0-file-based-agents.md
└── role-library/                      # Specialized role library
    ├── TC-006-agency-agents-marketing-suite.md
    ├── TC-035-autogpt-classic-autonomous-agent.md
    ├── TC-036-openmanus-general-agent.md
    ├── TC-037-babyagi-task-driven-agent.md
    ├── TC-038-anythingllm-agent-rag-suite.md
    ├── TC-039-wrenai-genbi-suite.md
    ├── TC-040-leon-personal-assistant.md
    ├── TC-041-buzz-hive-mind-platform.md
    ├── TC-042-openamer-self-improving-agent.md
    └── TC-043-openbitfun-code-agent.md
```

---

## Test Case File List

### 📁 single-artifact/ - Single-artifact cases (basic)

| # | File Name | Source Project | Artifact Type | License | Status |
|------|--------|----------|----------|--------|------|
| TC-001 | [TC-001-gpt-researcher-system-prompt.md](./single-artifact/TC-001-gpt-researcher-system-prompt.md) | gpt-researcher | System Prompt | Apache-2.0 | ✅ Complete |
| TC-002 | [TC-002-anthropics-pdf-skill.md](./single-artifact/TC-002-anthropics-pdf-skill.md) | anthropics/skills | Skill | Proprietary | ✅ Complete |
| TC-003 | [TC-003-mcp-tool-schema.json](./single-artifact/TC-003-mcp-tool-schema.json) | gpt-researcher | Tool Schema | Apache-2.0 | ✅ Complete |
| TC-007 | [TC-007-aider-system-prompts.md](./single-artifact/TC-007-aider-system-prompts.md) | aider | System Prompts | Apache-2.0 | ✅ Complete |
| TC-008 | [TC-008-cline-system-prompts.md](./single-artifact/TC-008-cline-system-prompts.md) | cline | System Prompts + Tools | Apache-2.0 | ✅ Complete |
| TC-009 | [TC-009-gemini-cli-system-prompts.md](./single-artifact/TC-009-gemini-cli-system-prompts.md) | gemini-cli | System Prompts + Tools + Skills | Apache-2.0 | ✅ Complete |
| TC-010 | [TC-010-opencode-system-prompts.md](./single-artifact/TC-010-opencode-system-prompts.md) | opencode | System Prompts + Tools | Apache-2.0 | ✅ Complete |
| TC-011 | [TC-011-mini-swe-agent-system-prompt.md](./single-artifact/TC-011-mini-swe-agent-system-prompt.md) | mini-swe-agent | System Prompts + Tools | MIT | ✅ Complete |
| TC-012 | [TC-012-openhands-sdk-system-prompts.md](./single-artifact/TC-012-openhands-sdk-system-prompts.md) | openhands-sdk | System Prompts + Tools | MIT | ✅ Complete |
| TC-013 | [TC-013-openai-codex-system-prompt.md](./single-artifact/TC-013-openai-codex-system-prompt.md) | openai/codex | System Prompts + Tools | Apache-2.0 | ✅ Complete |
| TC-014 | [TC-014-goose-system-prompts.md](./single-artifact/TC-014-goose-system-prompts.md) | goose | System Prompts + Tools | Apache-2.0 | ✅ Complete |
| TC-015 | [TC-015-qwen-code-skills.md](./single-artifact/TC-015-qwen-code-skills.md) | qwen-code | Skills | Apache-2.0 | ✅ Complete |
| TC-016 | [TC-016-swe-agent-tool-schemas.md](./single-artifact/TC-016-swe-agent-tool-schemas.md) | swe-agent | Tool Schemas | MIT | ✅ Complete |
| TC-017 | [TC-017-smolagents-system-prompt.md](./single-artifact/TC-017-smolagents-system-prompt.md) | smolagents | System Prompts + Tools | Apache-2.0 | ✅ Complete |
| TC-018 | [TC-018-browser-use-system-prompt.md](./single-artifact/TC-018-browser-use-system-prompt.md) | browser-use | System Prompts + Tools | MIT | ✅ Complete |
| TC-019 | [TC-019-deep-research-system-prompt.md](./single-artifact/TC-019-deep-research-system-prompt.md) | deep-research | System Prompt | MIT | ✅ Complete |
| TC-020 | [TC-020-smol-developer-system-prompt.md](./single-artifact/TC-020-smol-developer-system-prompt.md) | smol-developer | System Prompt + Tool | MIT | ✅ Complete |

### 📁 multi-agent-suite/ - Multi-Agent collaboration suite

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-004 | [TC-004-gpt-researcher-multi-agent-suite.md](./multi-agent-suite/TC-004-gpt-researcher-multi-agent-suite.md) | gpt-researcher | Multi-Agent collaboration system | 13 | Apache-2.0 | ✅ Complete |
| TC-021 | [TC-021-autogen-multi-agent-suite.md](./multi-agent-suite/TC-021-autogen-multi-agent-suite.md) | Microsoft AutoGen | Multi-Agent framework | 4 | CC-BY-4.0 | ✅ Complete |
| TC-022 | [TC-022-ag2-multi-agent-suite.md](./multi-agent-suite/TC-022-ag2-multi-agent-suite.md) | AG2 (AutoGen) | Multi-Agent framework | 6 | Apache-2.0 | ✅ Complete |
| TC-023 | [TC-023-crewai-multi-agent-suite.md](./multi-agent-suite/TC-023-crewai-multi-agent-suite.md) | CrewAI | Role-play multi-Agent | 4 | MIT | ✅ Complete |
| TC-024 | [TC-024-camel-multi-agent-suite.md](./multi-agent-suite/TC-024-camel-multi-agent-suite.md) | CAMEL | Multi-Agent framework | 14 | Apache-2.0 | ✅ Complete |
| TC-025 | [TC-025-openhands-multi-agent-suite.md](./multi-agent-suite/TC-025-openhands-multi-agent-suite.md) | OpenHands | Multi-Agent framework | 8 | MIT | ✅ Complete |
| TC-026 | [TC-026-metagpt-multi-agent-suite.md](./multi-agent-suite/TC-026-metagpt-multi-agent-suite.md) | MetaGPT | Software engineering pipeline | 7 | MIT | ✅ Complete |
| TC-027 | [TC-027-phidata-multi-agent-suite.md](./multi-agent-suite/TC-027-phidata-multi-agent-suite.md) | Phidata | Multi-Agent platform | 5 | Apache-2.0 | ✅ Complete |
| TC-028 | [TC-028-superagi-multi-agent-suite.md](./multi-agent-suite/TC-028-superagi-multi-agent-suite.md) | SuperAGI | Autonomous Agent framework | 9 | MIT | ✅ Complete |
| TC-029 | [TC-029-e2b-multi-agent-suite.md](./multi-agent-suite/TC-029-e2b-multi-agent-suite.md) | E2B | Sandbox runtime | 2 | Apache-2.0 | ✅ Complete |
| TC-030 | [TC-030-openinterpreter-multi-agent-suite.md](./multi-agent-suite/TC-030-openinterpreter-multi-agent-suite.md) | Open Interpreter | Code execution Agent | 5 | Apache-2.0 | ✅ Complete |

### 📁 file-based/ - File-configured Agents

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-005 | [TC-005-openclaw-file-based-agents.md](./file-based/TC-005-openclaw-file-based-agents.md) | OpenClaw | File-based multi-Agent | 6 | MIT | ✅ Complete |
| TC-031 | [TC-031-nanobot-file-based-agents.md](./file-based/TC-031-nanobot-file-based-agents.md) | nanobot | SOUL.md-driven Agent | 35 | MIT | ✅ Complete |
| TC-032 | [TC-032-hermes-agent-file-based-agents.md](./file-based/TC-032-hermes-agent-file-based-agents.md) | hermes-agent | Personal assistant framework | 24 | MIT | ✅ Complete |
| TC-033 | [TC-033-openagent-file-based-agents.md](./file-based/TC-033-openagent-file-based-agents.md) | openagent | MCP-based Agent | 21 | Apache-2.0 | ✅ Complete |
| TC-034 | [TC-034-mem0-file-based-agents.md](./file-based/TC-034-mem0-file-based-agents.md) | mem0 | Memory layer skills | 7 | Apache-2.0 | ✅ Complete |

### 📁 role-library/ - Specialized role library

| # | File Name | Source Project | Suite Type | Artifact Count | License | Status |
|------|--------|----------|----------|----------|--------|------|
| TC-006 | [TC-006-agency-agents-marketing-suite.md](./role-library/TC-006-agency-agents-marketing-suite.md) | agency-agents | Specialized role suite | 6 | MIT | ✅ Complete |
| TC-035 | [TC-035-autogpt-classic-autonomous-agent.md](./role-library/TC-035-autogpt-classic-autonomous-agent.md) | AutoGPT Classic | Autonomous task Agent | 30 | MIT | ✅ Complete |
| TC-036 | [TC-036-openmanus-general-agent.md](./role-library/TC-036-openmanus-general-agent.md) | OpenManus | General purpose Agent | 6 | MIT | ✅ Complete |
| TC-037 | [TC-037-babyagi-task-driven-agent.md](./role-library/TC-037-babyagi-task-driven-agent.md) | BabyAGI | Task-driven autonomous | 2 | MIT | ✅ Complete |
| TC-038 | [TC-038-anythingllm-agent-rag-suite.md](./role-library/TC-038-anythingllm-agent-rag-suite.md) | AnythingLLM Agent | Knowledge base/RAG | 13 | MIT | ✅ Complete |
| TC-039 | [TC-039-wrenai-genbi-suite.md](./role-library/TC-039-wrenai-genbi-suite.md) | WrenAI | GenBI text-to-SQL | 11 | Apache-2.0 | ✅ Complete |
| TC-040 | [TC-040-leon-personal-assistant.md](./role-library/TC-040-leon-personal-assistant.md) | Leon | Personal assistant | 6 | MIT | ✅ Complete |
| TC-041 | [TC-041-buzz-hive-mind-platform.md](./role-library/TC-041-buzz-hive-mind-platform.md) | Buzz | Hive mind platform | 15 | Apache-2.0 | ✅ Complete |
| TC-042 | [TC-042-openamer-self-improving-agent.md](./role-library/TC-042-openamer-self-improving-agent.md) | OpenAmer | Self-improving Agent | 14 | Apache-2.0 | ✅ Complete |
| TC-043 | [TC-043-openbitfun-code-agent.md](./role-library/TC-043-openbitfun-code-agent.md) | OpenBitFun | Code Agent with Rust | 13 | MIT | ✅ Complete |

---

## Classification Notes

### Why classify this way?

| Classification | Applicable Scenario | Evaluation Focus | Typical User |
|------|---------|---------|---------|
| **single-artifact** | Evaluate the quality of a single Prompt/Skill/Tool | Instruction clarity, Schema completeness, example quality | Agent developer |
| **multi-agent-suite** | Evaluate the design of a multi-Agent collaboration system | Role division, collaboration workflow, state management | System architect |
| **file-based** | Evaluate the flexibility of file-based configuration | File organization, configuration maintenance, auditability | Ops/config manager |
| **role-library** | Evaluate the practicality of specialized roles | Role definition, workflow, success metrics | Business operations staff |

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
| Role division clarity | Clear responsibility boundaries, no overlap | 20% |
| Workflow completeness | Full lifecycle coverage, sound quality gating | 25% |
| Prompt consistency | Unified terminology, format, and standards | 15% |
| Tool Schema modularity | Tools grouped by domain, complete parameters | 20% |
| Observability | Complete context, error tracking | 10% |
| Extensibility | Low cost to integrate new Agents/Tools | 10% |

#### file-based/

| Dimension | Description | Weight |
|------|------|------|
| File organization clarity | Clear responsibility boundaries | 20% |
| Markdown structure | Standard YAML frontmatter, clear hierarchy | 15% |
| Configuration maintainability | Centralized config, version-control friendly | 20% |
| Multi-Agent isolation | Independent workspace and state | 20% |
| Auditability | Pure Markdown readable, traceable changes | 15% |
| Extensibility | Low cost to create new Agents | 10% |

#### role-library/

| Dimension | Description | Weight |
|------|------|------|
| Role definition completeness | Identity, Mission, Rules clear | 20% |
| Workflow actionability | Clear phased workflow, complete templates | 25% |
| Quantifiable success metrics | 3-5 core KPIs with targets | 20% |
| Output template utility | Ready-to-use templates with examples | 15% |
| Cross-role collaboration | Clear boundaries with handoff mechanism | 10% |
| Non-coding positioning clarity | All deliverables are content/strategy | 10% |

---

## Task Domain Distribution

| Task Domain | Test Cases |
|-------------|------------|
| **Coding / Software Engineering CLI** | aider, cline, gemini-cli, opencode, mini-swe-agent, openhands-sdk, codex, goose, qwen-code, swe-agent, smolagents |
| **Autonomous Task / General Agent** | autogpt-classic, openmanus, babyagi, autogen, ag2, openamer, openbitfun |
| **Browser Automation** | browser-use, openinterpreter |
| **Deep Research** | gpt-researcher, deep-research |
| **Personal Assistant / Multi-channel** | nanobot, leon, mem0, hermes-agent, openagent, buzz |
| **Knowledge Base / RAG Agent** | anythingllm-agent, wrenai |
| **Code Generation** | smol-developer, agency-agents |
| **Multi-Agent Framework** | crewai, camel, openhands, phidata, metagpt, superagi, e2b |

---

## Usage Guide

### Quick Location

1. **Evaluate a single Prompt's quality** → `single-artifact/TC-007` (aider)
2. **Evaluate multi-Agent collaboration design** → `multi-agent-suite/TC-021` (autogen)
3. **Evaluate file-based configuration approach** → `file-based/TC-031` (nanobot)
4. **Evaluate business role definitions** → `role-library/TC-035` (autogpt-classic)

### Batch Evaluation

```bash
# Evaluate all single-artifact cases
ls test-cases/single-artifact/TC-*.md

# Compare same-type cases
diff test-cases/multi-agent-suite/TC-021-autogen-multi-agent-suite.md test-cases/multi-agent-suite/TC-022-ag2-multi-agent-suite.md

# Count cases of each type
find test-cases -name "TC-*.md" | grep -v sanityops | wc -l
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
| 2025-10-12 | Migrated 37 TC files from demo-agent: 14 single-artifact, 10 multi-agent-suite, 4 file-based, 9 role-library |
| 2025-10-10 | Initialized with 6 original cases (TC-001 to TC-006) |

---

*Generated for SanityOps Artifacts Report*