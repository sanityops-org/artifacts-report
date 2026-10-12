# SanityOps Artifacts Report — Folder Prompt

> **CRITICAL: READ THIS ENTIRE PROMPT BEFORE ANY ACTION**
>
> This prompt contains **mandatory rules** that must be followed for ALL operations in this folder. Failure to read and follow these rules will result in incorrect outputs.

---

## Mandatory Rules (Read First)

### Rule 1: Language Policy ⭐ HIGHEST PRIORITY
**ALL files in this folder MUST be written in English**, including:
- All generated reports
- All documentation
- All code comments
- All file names (except original test case content)

**The ONLY exception**: Content originally in other languages within test case artifacts.

**Violation examples to AVOID:**
- ❌ Writing reports in Chinese
- ❌ Mixing Chinese and English in output files
- ❌ Using Chinese file names

### Rule 2: Naming Conventions ⭐ HIGH PRIORITY
**MUST follow the exact naming patterns** defined in "Naming Conventions" section below.

**Violation examples to AVOID:**
- ❌ Using different naming patterns than specified
- ❌ Missing `.sanityops-{tool}-report.md` suffix
- ❌ Replacing original extensions instead of appending

### Rule 3: Read Before Action ⭐ HIGH PRIORITY
**ALWAYS read this entire prompt** before:
- Generating any files
- Running any inspections
- Creating any reports

---

> **Language Policy**: All files in this folder, including this prompt, must be written in English. The only exception is content originally in other languages within test cases. Unless explicitly specified, all disk-written content should be in English.

---

## Folder Purpose

This folder serves as the **Internet Use Case Defect Verification Report Repository** for the **SanityOps Project**. It is primarily used for collecting, storing, and managing Agent logical artifact samples from multiple open-source GitHub projects, along with their defect verification reports.

---

## What is SanityOps?

SanityOps is a **vendor-neutral, enterprise-grade AI Agent quality and safety governance framework** covering the complete lifecycle of AI Agents.

### Core Pillars

- **Inspect** — Static defect inspection of System Prompts, Skills, and Tool Schemas
- **Risk** — Explicit risk auditing + dynamic implicit runtime vulnerability validation
- **Quality** — Service quality evaluation for RAG-Agents and Tool-Agents
- **Relevance** — Diagnostic mapping between defects and risk/quality failure modes

### Key Concepts

| Term | Description |
|------|-------------|
| **Logic Artifacts** | Logical artifacts: System Prompt, Skill, Tool Schema, Permission |
| **Shadow Sandbox** | Production-equivalent shadow environment for dynamic validation |
| **Ratchet Mechanism** | Version-synchronized ratchet mechanism to prevent quality regression |
| **Gate** | Release admission decision based on baseline and ratchet mechanism |

> For complete framework documentation, refer to `../sanityops-framework/README.md`

---

## Related Tools

This folder's sibling directories contain two SanityOps Inspect tools:

### 1. sanityops-inspect-lite (Skill Version)

- **Positioning**: Lightweight Skill implementation of the `sanityops-inspect` collection
- **Features**:
  - Zero-install, detect-only
  - Covers minimal rule subset of Inspect only
  - **No repair functionality**
  - **Does not block on P0 defects** during inspection, continues subsequent tasks
- **Use Cases**: Quick understanding of Inspect functionality without CLI installation

### 2. inspect-cli (CLI Version)

- **Positioning**: Full-featured CLI implementation of the `sanityops-inspect` collection
- **Features**:
  - Complete Inspect specification implementation
  - Supports L1/L2/L3 three-level inspection depth
  - **Has repair functionality** (`sanityops-cli inspect repair`)
  - **Blocks execution on P0 defects**, does not continue subsequent tasks
  - CI/CD integration support
- **Use Cases**: Production environments, pre-release comprehensive inspection

### Skill vs CLI Comparison

| Feature | Skill (sanityops-inspect-lite) | CLI (inspect-cli) |
|---------|-------------------------------|-------------------|
| Repair | ❌ Not supported | ✅ Supported |
| P0 Defect Handling | Non-blocking, continues | Blocking, stops execution |
| Rule Coverage | Condensed subset | Full specification |
| Installation | Zero-install / Plugin | pip / curl / Source |

---

## Folder Working Guidelines

### Scope Constraints

> **Important: This folder only collects end-user facing internet application Agent use cases**

**Excluded Types:**
- ❌ Code development Agents (code generation, code review, programming assistance, etc.)
- ❌ Software development toolchain related logical artifacts
- ❌ IDE plugins, development frameworks, technical tools

**Included Examples:**
- ✅ Information query Agents (research assistants, data analysis assistants)
- ✅ Business processing Agents (customer service, booking, approval assistance)
- ✅ Content generation Agents (document writing, report generation)
- ✅ Multi-domain tool-calling Agents (travel planning, health management)

### Storage Content

1. **Agent Logical Artifact Samples** — System Prompts, Skills, Tool Schemas from GitHub open-source projects
2. **Defect Verification Reports** — Inspection reports generated using SanityOps Inspect tools
3. **Comparative Analysis Documents** — Comparison of inspection results across different tools/versions

### Naming Conventions

#### 1. Use Case Artifacts (Test Cases)

Pattern: `TC-{NNN}-{project-name}-{artifact-type}.{ext}`

| Component | Description | Examples |
|-----------|-------------|----------|
| `TC-{NNN}` | Test case serial number (001-999) | `TC-001`, `TC-002` |
| `{project-name}` | Source project name (kebab-case) | `gpt-researcher`, `anthropics-pdf` |
| `{artifact-type}` | Artifact type descriptor | `system-prompt`, `skill`, `tool-schema`, `multi-agent-suite` |
| `.{ext}` | File extension | `.md`, `.json`, `.yaml` |

**Examples:**
- `TC-001-gpt-researcher-system-prompt.md`
- `TC-002-anthropics-pdf-skill.md`
- `TC-003-mcp-tool-schema.json`
- `TC-004-gpt-researcher-multi-agent-suite.md`

#### 2. Inspection Reports

Pattern: `{original-filename}.sanityops-{tool}-{report-type}.md`

| Tool | Report Type | Pattern | Example |
|------|-------------|---------|---------|
| **Skill** (sanityops-inspect-lite) | Inspection report | `{artifact}.sanityops-skill-report.md` | `TC-001-gpt-researcher-system-prompt.sanityops-skill-report.md` |
| **Skill** (sanityops-inspect-lite) | Summary report | `sanityops-skill-inspection-summary.md` | `sanityops-skill-inspection-summary.md` |
| **CLI** (sanityops-cli) | Inspection report | `{artifact}.sanityops-cli-report.md` | `TC-001-gpt-researcher-system-prompt.sanityops-cli-report.md` |
| **CLI** (sanityops-cli) | Summary report | `sanityops-cli-inspection-summary.md` | `sanityops-cli-inspection-summary.md` |

**Key Rules:**
1. Always append `.sanityops-{tool}-{report-type}.md` to the original artifact filename
2. Do NOT replace the original extension; append after it
3. For single-artifact reports: use `-report.md` suffix
4. For summary reports: use `sanityops-{tool}-inspection-summary.md`

#### 3. Comparative Analysis

Pattern: `comparison-{tool-a}-vs-{tool-b}-{topic}-{date}.md`

**Examples:**
- `comparison-skill-vs-cli-inspection-results-2026-10-10.md`
- `comparison-l1-vs-l2-vs-l3-check-levels-2026-10-10.md`

#### 4. Directory Structure

```
test-cases/
├── {category}/                    # single-artifact, multi-agent-suite, file-based, role-library
│   ├── TC-{NNN}-{name}.{ext}       # Original artifact
│   ├── TC-{NNN}-{name}.sanityops-skill-report.md
│   └── TC-{NNN}-{name}.sanityops-cli-report.md
├── sanityops-skill-inspection-summary.md
└── sanityops-cli-inspection-summary.md
```

### Related References

- Framework docs → `../sanityops-framework/`
- Skill tool → `../sanityops-inspect-lite/`
- CLI tool → `../inspect-cli/`

---

## Quick Start

1. **Understand the framework**: Read `../sanityops-framework/README.md`
2. **Quick experience**: Use `../sanityops-inspect-lite/` for zero-install inspection
3. **Full inspection**: Install `../inspect-cli/` for production-grade inspection
4. **Store reports**: Save verification reports to this folder, archived per naming conventions
