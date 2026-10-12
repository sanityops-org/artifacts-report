# TC-039: WrenAI - GenBI Knowledge Base Suite

## Metadata
- **Source Project**: WrenAI (Canner/WrenAI)
- **GitHub**: github.com/Canner/WrenAI
- **License**: Apache-2.0 (core/sdk/skills), AGPL-3.0 (some parts)
- **Artifact Type**: GenBI text-to-SQL platform with skills for data analysis
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction at commit fedf182b4bb8294623d9cc0a9db4fbae1edf63fb
- **Scope**: GenBI text-to-SQL platform with skills for data analysis

---

## Project Overview

WrenAI is a **GenBI (Generative Business Intelligence)** platform that transforms natural language into SQL queries and generates shareable analytics applications. It features a comprehensive skill system for data analysis, dashboard building, and context layer management.

### Key Characteristics
- **Text-to-SQL**: Natural language to database queries
- **Context Layer**: MDL (Modeling Definition Language) for data modeling
- **7 core skills**: dlt-connector, enrich-context, genbi, generate-mdl, onboarding, usage, main wren skill
- **CLI-driven workflow**: Skills orchestrated through `wren` CLI

---

## Agent Prompts

### 1. Repository AGENTS.md

```markdown
# AGENTS.md

Repository-wide instructions live in `.claude/CLAUDE.md`. Please refer to that file for shared build commands, architecture, and conventions.

**Before opening a pull request, read the "Contribution Bar" section of that file.** It sets out what is expected of a change here — reproduce a failure before claiming one, label honestly, make tests exercise the code they cover — and what will be closed rather than reviewed.

Per-module instructions live in `core/<module>/.claude/CLAUDE.md`, each with its own `AGENTS.md` pointing at it.
```

---

## Skill Definitions

### 1. GenBI Skill

```markdown
---
name: genbi
description: "Turn a Wren project's context layer into a shareable, browser-side GenBI web app and deploy it to the user's Vercel or Cloudflare account. Orchestrates the full flow: `wren genbi build` returns a project-hydrated build instruction, the agent authors the app from scratch into apps/<name>/, then register → verify → deploy produce a shareable URL. Use this skill whenever the user wants to: build a dashboard from their Wren project, make a shareable analytics app, deploy their context layer as a web app, host a GenBI app on Vercel or Cloudflare Pages, or asks for a 'genbi app'."
license: Apache-2.0
metadata:
  author: wrenai
---

# Wren GenBI App — Agent Workflow Guide

> This guide is served by the `wren` CLI (`wren skills get genbi`), so it
> always matches your installed wrenai version.

Turn a Wren context layer into a shareable GenBI app — from a natural-language
request to a public URL in one conversation.

**Division of labor:** the CLI owns the authoritative build instruction (it
knows the live project facts and the pinned `wren-core-wasm` version) and all
deterministic state (index, verify, deploy). You — the agent — author the app
code by following the instruction. Never hand-write `.wren/apps.yml`.

## Preconditions

1. A Wren project is discoverable (`wren_project.yml` in cwd/ancestors, or ask
   for the path and pass `-p`).
2. The context layer exists. If `target/mdl.json` is missing, `wren genbi
   build` compiles it implicitly — no separate step needed.
3. `wren` CLI ≥ the version that ships the `genbi` command group
   (`wren genbi --help` works).

## Workflow

### 1. Resolve the app name and data mode

- App name: short kebab-case derived from the request (e.g. `sales-overview`).
- Data mode:
  - `snapshot` (default) — data is bundled with the app as parquet/duckdb and
    queried client-side. Fully serverless. Right for demos, reports, small
    data, and dlt-pipeline output.
  - `live` — the app calls back to the user's warehouse/API at view time.
    Right for production-scale or always-fresh data. Requires a CORS-enabled
    endpoint and carries strict no-credentials rules.
- Ask the user ONLY if the choice is genuinely ambiguous.

### 2. Get the build instruction

```bash
wren genbi build <name> --prompt "<the user's request, verbatim>" --data-mode <mode>
```

For long or multi-line prompts use `--prompt-file <file>` or pipe to
`--prompt -`. The command prints the authoritative build instruction —
wasm wiring (pinned version, CDN load), the project's model/column inventory,
data-mode guidance, acceptance criteria, and the target folder. It writes no
app files — the only thing it may touch is `target/mdl.json`, which it compiles
first if missing (see Precondition 2).

### 3. Author the app

Follow the instruction exactly. Key conventions:

- Write everything under `apps/<name>/` — never outside it.
- Copy the compiled MDL into the app as `apps/<name>/mdl.json`.
- Load `wren-core-wasm` from the CDN given in the instruction; never bundle
  the ~68MB binary.
- snapshot: export the data the dashboard needs into `apps/<name>/data/` as
  parquet (`verify` requires at least one `.parquet`/`.duckdb` asset). See
  **Snapshot data export** below for the recipe and where the data comes from.
- live: write an endpoint-only connection config. NEVER inline credentials —
  `verify` scans for them (best-effort) and `deploy` gates on `verify`, but
  the rule is on you: a public static host exposes every shipped file.
- Design the dashboard to actually answer the user's request: pick the right
  charts/tables for the question, not a generic template.

### 4. Register and verify

```bash
wren genbi register <name> --data-mode <mode>
wren genbi verify <name>
```

### 5. Deploy (only if the user asked for it)

```bash
wren genbi deploy <name> --provider vercel      # or cloudflare
```

## Quick reference

| Step | Command |
| --- | --- |
| Get build instruction | `wren genbi build <name> --prompt "…" [--data-mode snapshot\|live]` |
| Record the app | `wren genbi register <name> --data-mode <mode>` |
| Preflight | `wren genbi verify <name>` |
| Local preview | `wren genbi open <name>` |
| Ship | `wren genbi deploy <name> --provider vercel\|cloudflare [--prod]` |
| Inventory | `wren genbi list` / `wren genbi remove <name>` |
```

---

## Available Skills (7 Total)

| Skill | Description |
|-------|-------------|
| dlt-connector | Connect SaaS data sources to Wren project |
| enrich-context | Enhance context layer with additional information |
| genbi | Build and deploy GenBI dashboard apps |
| generate-mdl | Generate MDL (Modeling Definition Language) |
| onboarding | Project setup and onboarding |
| usage | Usage analytics and tracking |
| wren | Main Wren CLI skill |

---

## Evaluation Dimensions

### 1. Skill Definition Quality
- [ ] Each skill has clear name and description
- [ ] License metadata included
- [ ] Author attribution provided
- [ ] Pre-conditions documented

### 2. Workflow Clarity
- [ ] Step-by-step process is clear
- [ ] Commands are enumerated
- [ ] Error handling described
- [ ] Success criteria defined

### 3. Data Mode Support
- [ ] Snapshot mode for serverless
- [ ] Live mode for production data
- [ ] Clear guidance on when to use each
- [ ] Security considerations for credentials

### 4. CLI Integration
- [ ] Commands map to skill operations
- [ ] Build instruction is authoritative
- [ ] Verify before deploy
- [ ] Quick reference table

### 5. Deployment Support
- [ ] Vercel deployment
- [ ] Cloudflare Pages deployment
- [ ] Preview vs production distinction
- [ ] URL verification after deploy

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Definition Quality | 20% | | |
| Workflow Clarity | 25% | | |
| Data Mode Support | 20% | | |
| CLI Integration | 20% | | |
| Deployment Support | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Skill Workflow Tests
1. Execute `wren genbi build` with various prompts
2. Test snapshot vs live data mode selection
3. Verify app authoring follows instructions

### Deployment Tests
1. Deploy GenBI app to Vercel
2. Deploy GenBI app to Cloudflare
3. Verify URL accessibility

### Data Export Tests
1. Export DuckDB data to parquet
2. Test live mode endpoint configuration
3. Verify no credentials inlined

### Skill Loading Tests
1. Load all 7 skills via CLI
2. Test skill chaining
3. Verify skill versioning

---

## Notes

- WrenAI demonstrates CLI-orchestrated skill workflow
- GenBI skill shows full pipeline from prompt to deployed app
- Division of labor between CLI (state) and agent (code authoring)
- Security focus: never inline credentials
- Apache-2.0 license for core/skills allows examination
- Good reference for building data analysis agent platforms