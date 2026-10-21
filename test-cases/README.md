# SanityOps Test Case Set — Organized by Logic-Artifact Combination

> Corpus of open-source Agent logic artifacts, organized by **which artifact types are actually loadable** in each case.
> Restructured 2026-10-21. Case files are unchanged; only the folder layout changed.

---

## 1. Why organize by combination

The three artifact types (System Prompt / Skill / Tool Schema) are not interchangeable, and a case that ships only one of them cannot exercise the cross-artifact checks. Grouping by combination makes two things visible at a glance:

1. **Which combinations have enough samples** to support statistics.
2. **Which combinations are structurally empty** in the real open-source ecosystem — that emptiness is itself a finding, not a collection gap.

A case is placed in exactly one folder, named by the set of artifact types that are **directly loadable** from the text shipped in the case file.

---

## 2. Combination matrix

| Folder | Combination | Cases | Single-artifact | Agent-suite | Usable artifacts |
|---|---|---:|---:|---:|---:|
| [prompt-only](prompt-only/) | Prompt | **67** | 50 | 17 | 67 |
| [skill-only](skill-only/) | Skill | **65** | 50 | 15 | 65 |
| [tool-only](tool-only/) | Tool Schema | **49** | 49 | 0 | 49 |
| [prompt-skill](prompt-skill/) | Prompt + Skill | **0** | 0 | 0 | 0 |
| [prompt-tool](prompt-tool/) | Prompt + Tool Schema | **0** | 0 | 0 | 0 |
| [skill-tool](skill-tool/) | Skill + Tool Schema | **0** | 0 | 0 | 0 |
| [prompt-skill-tool](prompt-skill-tool/) | All three | **0** | 0 | 0 | 0 |
| [none](none/) | No loadable artifact | **24** | 0 | 24 | 0 |
| **Total** | | **205** | **149** | **56** | **181** |

`TC-003-mcp-tool-schema.json` (a 50th tool-schema case) currently sits in `_archive/temp/` and is not counted above.

---

## 3. What the matrix says

**Single-artifact cases cover all three types evenly** (50 / 50 / 49). This is the usable statistical base: 149 independent artifacts, each one directly loadable and independently gradeable.

**Multi-type combinations are empty across the entire corpus.** No case ships two or more loadable artifact types together. Two independent sampling frames produced the same result:

| Frame | Sample | Result |
|---|---|---|
| Artifact-first (2026-10-10 → 10-14) | 51 agent cases | 15 skill-only + 12 prompt-only + 24 none |
| Agent-first (2026-10-21) | 5 production products | 5 prompt-only |

This is not a collection failure. It reflects how production agents are actually built:

- **Prompt is universal** — every product ships instruction text.
- **Skill (`SKILL.md`) is a file-based-agent convention** — used by Claude-style agents, absent from business products.
- **Tool Schema as a loadable document is rare** — tools live as Python signatures, Go structs, PHP task definitions, or MCP servers, and are converted to schema at runtime rather than shipped as schema.

---

## 4. Folder contents

### Covered combinations

- **[prompt-only](prompt-only/)** — 50 single System Prompt cases (`TC-018`–`TC-137` range) + 17 agent cases.
  Agent cases: `TC-064`, `065`, `066`, `067`, `071`, `090`, `091`, `092`, `094`, `095`, `096`, `101`, `247`, `248`, `249`, `250`, `251`.
- **[skill-only](skill-only/)** — 50 single Skill cases (`TC-002`–`TC-181` range) + 15 agent cases.
  Agent cases: `TC-006`, `007`, `031`, `032`, `033`, `034`, `039`, `041`, `056`, `057`, `058`, `059`, `068`, `069`, `070`.
- **[tool-only](tool-only/)** — 49 MCP / function-calling Tool Schema cases (`TC-050`, `TC-182`–`TC-246`).
- **[none](none/)** — 24 agent cases with no loadable artifact: summarised, truncated, missing frontmatter, or logic embedded in code. Retained as exclusion evidence, not as an analysis denominator.

### Empty combinations

Each empty folder carries a short `README.md` recording why it is empty, so the absence is documented rather than looking like an oversight.

---

## 5. Counting standard

A text counts as an artifact only when it can be loaded directly, without editing:

| Type | Requirement |
|---|---|
| System Prompt | Complete instruction unit usable as a system message: task plus its own constraints or output contract |
| Skill | `SKILL.md` with `name` and `description` frontmatter and a complete body |
| Tool Schema | Single tool in OpenAI / Anthropic / MCP structure with `type: object`, `properties`, `required` |

Not counted: summaries, excerpts, `...`-truncated text, missing frontmatter, non-standard tool definitions (decorators, TypeBox/Zod source, LangChain `Tool(...)`), backend code, configuration.

Template variables (`{var}`, `${var}`, `{{.Var}}`) do not disqualify a case; they are runtime inputs.

---

## 6. Pending reclassification

Two agent cases have **deterministically extracted** tool schemas that are verified but not yet written into the case file:

| Case | Product | Extracted tools | Extractor |
|---|---|---:|---|
| `TC-247` | OpenContracts | 12 | Python AST (`_archive/extract_tool_schema.py`, output `_archive/opencontracts_tools.json`) |
| `TC-251` | Mattermost Agents | MCP tools via `jsonschema` struct tags | Not yet written |

Both currently sit in `prompt-only`. Once the tool schemas are materialised into their case files, they move to `prompt-tool` — making it the only non-empty multi-type combination in the corpus.

---

## 7. Provenance

- **Single-artifact cases** — 149 cases collected 2026-10-10 → 10-14 from 176 unique source projects; see [STATISTICS.md](STATISTICS.md) for the per-project appendix.
- **Agent-first cases (TC-247–251)** — 5 production products collected 2026-10-21 at pinned commits. Statistics: `_archive/agent-suite/README-2026-10-21-agent-first-5cases.md`.
- **Archived agent batch (TC-004–107)** — 51 cases, 2026-10-10 → 10-14. Statistics: `_archive/agent-suite/README.md`.
- Local clones used for verbatim extraction: `_archive/_clones/` (read-only, shallow, commit pinned per case).

---

## 8. Naming convention

`TC-{NNN}-{project-name}-{artifact-type}.{ext}`

- `{artifact-type}` reflects what the case was originally collected as (`system-prompt`, `skill`, `tool-schema`, `multi-agent-suite`, `agent-suite`, `file-based-agents`).
- The **folder** now reflects the loadable combination, which may differ from the filename suffix — for example `TC-031-...-file-based-agents.md` lives in `skill-only/`.
- Filenames were not changed, so external references remain valid.
