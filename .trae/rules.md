# SanityOps Artifacts Report — Folder Prompt

> **CRITICAL: READ THIS ENTIRE PROMPT BEFORE ANY ACTION**
>
> This prompt contains **mandatory rules** that must be followed for ALL operations in this folder. Failure to read and follow these rules will result in incorrect outputs.

---

## Mandatory Rules (Read First)

### Rule 0: Read This File First ⭐ MANDATORY AT SESSION START
**This file is auto-loaded whenever this folder is opened.** Before answering any
question or performing any action in this folder, you MUST treat its content as
already-loaded session context, and you MUST consult the sections below
(especially "Repository Ecosystem & Authority") before reading other repos.

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

## Repository Ecosystem & Authority

This folder (`artifacts-report`) is **one node** in the SanityOps project. It produces
neither the specification nor the tools — it stores **samples + verification reports**.
Its sibling directories under `d:\My Docunments\AI\` are:

| Directory | Role | Language | Form | When to use it |
|-----------|------|----------|------|----------------|
| `sanityops-framework-cn` | **Specification — Chinese mirror** of the SanityOps Framework (Inspect / Risk / Quality / Relevance / Core) | Chinese | VitePress-style docs | Chinese Q&A, reading path, DMC/sales material |
| `sanityops-inspect-lite` | **Lite Skill implementation** of the Inspect pillar — zero-install, detect-only, seven-stage flow, no repair | English | Claude Code plugin + standalone Skill | Run a lightweight inspection of a Prompt / Skill / Tool Schema |
| `inspect-cli` | **Full CLI implementation** (`sanityops-cli`) — L1/L2/L3 depth, `inspect repair`, P0-blocking, CI/CD ready | English | Python package + standalone binary | Production / pre-release full inspection |
| `SanityOps-Sider` | Flattened Chinese doc set snapshot for the Sider agent (includes DMC, which framework v1.0 does not) | Chinese | Flat single-layer files | Fast Chinese retrieval, earlier-generation compilation |
| `promotion` | Outbound promotion material | Mixed | Ad-hoc | Marketing / launch content |

### Default Aliases (Read This Before Interpreting User Requests)

| User says | Default meaning | Resolve to |
|-----------|-----------------|------------|
| **"the skill" / "skill"** | The SanityOps Inspect **lite** skill | `d:\My Docunments\AI\sanityops-inspect-lite\plugins\sanityops-inspect-lite\skills\sanityops-inspect-lite\SKILL.md` |
| **"the CLI" / "cli"** | The SanityOps Inspect **full** CLI | `d:\My Docunments\AI\inspect-cli\` (`sanityops-cli`) |

> These are the **default referents**. Do NOT reinterpret them as "a skill" or "a CLI"
> in the generic sense. Expand to another tool only when the user names it explicitly.

### Authority Chain (highest → lowest)

```
sanityops-framework       <- authoritative source specification (English, CC BY-SA 4.0)
  └── sanityops-framework-cn   <- Chinese mirror; on conflict, the English source governs
        ├── sanityops-inspect-lite  <- condensed extraction of Inspect; NON-normative, defines no new rules
        └── inspect-cli             <- full-fidelity implementation (Apache 2.0)
```
- If a rule conflict appears, always fall back to the authoritative sub-specification
  (`inspect/`, `risk/`, `quality/`, `framework/relevance.md`).
- `sanityops-inspect-lite` is executed by a **host model**; it never overrides the spec.

### Division of Labor — One Sentence

> **The framework defines *what to check*; inspect-lite / inspect-cli are *the checkers*;
> artifacts-report is the *result repository* produced by running those checkers.**

### Doc Router

A skill at `d:\My Docunments\AI\.trae\skills\sanityops-docs-router\SKILL.md` routes
SanityOps documentation questions to the correct directory/file. **Use it to locate the
right file first instead of reading every document.**

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

### Related References (absolute paths)

- Framework specification (CN mirror) → `d:\My Docunments\AI\sanityops-framework-cn\`
- Framework authoritative source (EN) → `sanityops-framework` (not present locally; governs on conflict)
- Skill tool (lite) → `d:\My Docunments\AI\sanityops-inspect-lite\`
- CLI tool (full) → `d:\My Docunments\AI\inspect-cli\`
- Doc router → `d:\My Docunments\AI\.trae\skills\sanityops-docs-router\SKILL.md`

---

## Session Start Checklist

When a new conversation begins in this folder, confirm in order:

1. ✅ This `rules.md` is loaded (auto-injected on folder open).
2. ✅ Output language = English (Rule 1).
3. ✅ Naming pattern for any file to be created (Rule 2).
4. ✅ Which sibling repo actually holds the answer — use the Doc Router before reading widely.

> If any of the above is unclear, state the assumption explicitly before proceeding.

---

## Quick Start

1. **Understand the framework**: Read `d:\My Docunments\AI\sanityops-framework-cn\README.md` (CN mirror; EN source governs on conflict)
2. **Quick experience**: Use `d:\My Docunments\AI\sanityops-inspect-lite\` for zero-install inspection
3. **Full inspection**: Install `d:\My Docunments\AI\inspect-cli\` for production-grade inspection
4. **Store reports**: Save verification reports to this folder, archived per naming conventions
