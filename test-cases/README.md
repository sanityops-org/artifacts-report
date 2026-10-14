# SanityOps Agent Logical Artifact Evaluation Test Case Set

## Project Overview

This folder collects open-source Agent **logical artifact samples** (System Prompt / Skill / Tool Schema) for the SanityOps project, used to run static defect inspection and store the verification reports.

- **Inclusion Criteria** (a case qualifies when ALL hold):
  1. Real open-source project with a clear license (Apache-2.0 / MIT preferred)
  2. End-user-facing scenario (excludes code-development agents, dev toolchains, IDE plugins, development frameworks, and research simulations/benchmarks)
  3. Contains auditable logic artifacts (System Prompt / Skill / Tool Schema)

## Current Progress — 200 cases

| Object kind | Folder | Count | Meaning |
|---|---|---|---|
| Single logical artifact | `single-artifact/system-prompt/` | **50** | One System Prompt |
| Single logical artifact | `single-artifact/skill/` | **50** | One Skill (`SKILL.md`) |
| Single logical artifact | `single-artifact/tool-schema/` | **50** | One Tool Schema |
| Complete Agent / group of Agents | `agent-suite/` | **50** | One Agent bundling multiple logical artifacts |
| | **TOTAL** | **200** | |

---

## Classification: two kinds of evaluation object

Only two kinds of object are actually evaluated:

| Category | What it is | Reusable? |
|---|---|---|
| **single-artifact** | One logical artifact (System Prompt / Skill / Tool Schema); may be reused across multiple Agents, so it has standalone value | Yes, by many Agents |
| **agent-suite** | A complete Agent, or a group of Agents, bundling multiple logical artifacts into one business expression | No, it is the whole |

`single-artifact/` is further split by artifact type into `system-prompt/`, `skill/`, and `tool-schema/`.

> The earlier four-way split (`single-artifact` / `multi-agent-suite` / `file-based` / `role-library`) mixed *evaluation object* with *implementation shape* (file storage, role content, collaboration topology) and has been retired.

---

## Folder Structure

```
test-cases/
├── README.md
├── single-artifact/
│   ├── system-prompt/        # 50 System Prompt cases
│   ├── skill/                # 50 Skill cases
│   └── tool-schema/          # 50 Tool Schema cases
└── agent-suite/              # 50 complete-Agent / group-of-Agents cases
```

Each `TC-*` file is self-describing: its `## Metadata` block records the source project, GitHub URL, license, artifact type, collection date, and the exact source URLs used to quote the artifact verbatim.

---

## Evaluation Dimensions

### single-artifact — per artifact type

| Artifact Type | Core Evaluation Dimensions | Weight Distribution |
|----------|-------------|----------|
| **System Prompt** | Instruction clarity, structure, citation handling, quality control, testability | 25%/20%/25%/20%/10% |
| **Skill** | Metadata completeness, trigger conditions, instruction structure, code example quality, maintainability | 15%/20%/25%/25%/15% |
| **Tool Schema** | Schema completeness, description clarity, integration compatibility, example quality, extensibility | 25%/20%/25%/20%/10% |

### agent-suite — complete Agent / group of Agents

| Dimension | Description | Weight |
|------|------|------|
| Role / responsibility division | Clear boundaries between roles/artifacts, no overlap | 20% |
| Workflow / lifecycle completeness | Full lifecycle coverage, sound quality gating | 25% |
| Artifact consistency | Unified terminology, format, and standards across artifacts | 15% |
| Tool / artifact modularity | Artifacts grouped by domain, complete parameters | 20% |
| Auditability / observability | Readable structure, traceable changes, error tracking | 10% |
| Extensibility | Low cost to add new roles/artifacts | 10% |

---

## Domain Coverage (indicative)

- **single-artifact / system-prompt** — research & report, customer service, travel, finance/investing, legal, healthcare, education, e-commerce, productivity, CRM, data analysis, multilingual, real-estate.
- **single-artifact / skill** — marketing, HR/recruiting, legal, finance/trading, design, education, media/journalism, product management, real estate, travel, health billing, negotiation.
- **single-artifact / tool-schema** — search, maps/geocoding, messaging, memory, time, finance/crypto, weather, cloud files, e-commerce, music, books, news, transit, sports, translation, movies/TV, calendar, documents, public health.
- **agent-suite** — multi-role agents across customer service, travel, finance, legal, healthcare, e-commerce, sales, research, personal assistant, and content generation.

---

## Usage Guide

### Quick Location

1. **Evaluate a single System Prompt** → `single-artifact/system-prompt/`
2. **Evaluate a single Skill** → `single-artifact/skill/`
3. **Evaluate a single Tool Schema** → `single-artifact/tool-schema/`
4. **Evaluate a complete Agent / group of Agents** → `agent-suite/`

### Batch Evaluation

```bash
find test-cases/single-artifact/system-prompt -name "TC-*" | wc -l
find test-cases/single-artifact/skill         -name "TC-*" | wc -l
find test-cases/single-artifact/tool-schema   -name "TC-*" | wc -l
find test-cases/agent-suite                   -name "TC-*" | wc -l
```

### New Case Workflow

1. Decide the object type → `single-artifact/{system-prompt|skill|tool-schema}/` or `agent-suite/`
2. Copy the structure of an existing case in that folder
3. Fill in meta information → source / license / collection method (exact URLs)
4. Quote the artifact **verbatim**; never fabricate
5. Keep the evaluation dimensions consistent with the artifact type

---

## License Notes

- **Apache-2.0 / MIT**: May be fully quoted and modified
- **Proprietary**: Structure outline only + ≤10-line short quotes
- **Split-licensed repos** (e.g. chatwoot `enterprise/`, Onyx `ee/`): quote only the permissive-licensed parts; flag the rest
- A few cases use other OSI licenses (e.g. AGPL-3.0); each flags its license explicitly in its own `## Metadata` / `## Notes`

---

## Changelog

| Date | Update |
|------|----------|
| 2026-10-13 | Restructured to two evaluation-object kinds and expanded to **200 cases**: `single-artifact/` split into `system-prompt/` (50), `skill/` (50), `tool-schema/` (50); `agent-suite/` expanded to 50. Removed duplicate-project cases found during collection. |
| 2026-10-13 | Merged the former `multi-agent-suite`, `file-based`, and `role-library` folders into `agent-suite/`. |
| 2026-10-12 | Migrated 37 TC files from demo-agent. |
| 2026-10-10 | Initialized with 6 original cases (TC-001 to TC-006). |

---

*SanityOps Agent Logical Artifact Test Case Set*
