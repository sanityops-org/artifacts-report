# TC-041: Buzz - Hive Mind Communication Platform Suite

## Metadata
- **Source Project**: Buzz (block/buzz)
- **GitHub**: github.com/block/buzz
- **License**: Apache-2.0
- **Artifact Type**: Hive mind communication platform with multi-agent skills
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction at commit 30873ba46b5e08602ae61a2a0592ecedd37f7289
- **Scope**: Hive mind communication platform with multi-agent skills

---

## Project Overview

Buzz is a **hive mind communication platform** that spans multiple repos and supports multiple agent frameworks (Claude, Codex, Goose). It provides cross-platform skills and a desktop app with managed agents for screenshot capture and skill management.

### Key Characteristics
- **Multi-framework support**: Claude, Codex, Goose skill directories
- **11 skill entries** across 6 locations (5 distinct skills, duplicated per framework): desktop-screenshot, buzz-cli, GitHub research, etc.
- **Desktop app**: Tauri 2 + React 19 with managed agents
- **Relay server**: WebSocket relay for communication

---

## Agent Prompts

### 1. AGENTS.md

```markdown
# AGENTS.md — AI Agent Contributor Guide

This guide is for AI agents contributing to the Buzz codebase. It covers
agent-specific context and conventions. For general contributor info (setup,
code style, PR process, architecture), see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Product Contract

Before planning or reviewing a non-trivial change:

1. Read [VISION.md](VISION.md).
2. Read the `VISION_*.md` documents relevant to the affected product surface.
3. Read the applicable guidance in [TESTING.md](TESTING.md) and any
   package-local `TESTING.md`.
4. Check that the proposed design advances, or at least does not contradict,
   that product intent. Call out any intentional tension explicitly.

Implementation describes the product today; the vision documents describe the
product it is becoming. A locally correct change can still be wrong if it works
against that direction.

---

## Before opening a PR

Open work in progress as a draft PR. Mark it ready for review only when this
checklist holds for the current change.

1. **Agent review ran** under [Reviewing](#reviewing), and its recommended
   blockers were fixed or explicitly declined by the human author.
2. **An agent exercised the changed behavior.**
3. **A human then tested it themselves**.
4. **Add `buzz-review-completed` to the PR description** once steps 1–3 hold.

## Reviewing

- Before reviewing, read [VISION.md](VISION.md), the `VISION_*.md` docs for the affected surface, and the PR's stated goal and linked issue.
- Check the change against the [Review-Proven Rules](#review-proven-rules).
- Judge minimalism, elegance, and correctness, aiming for 9/10 on each.
- Recommend blocking only for concrete correctness, security, or agreed-contract defects.
```

---

## Skill Definitions

### 1. Desktop Screenshot Skill

```markdown
---
name: desktop-screenshot
description: >
  Capture desktop app screenshots and post them to GitHub PRs with immutable URLs.
version: 1
---

# Desktop Screenshot Skill

## CRITICAL: How to Host Screenshots for PRs

**NEVER use `buzz upload`, the relay media endpoint, or any third-party image
host (imgur, imgbb, etc.) for PR screenshots.** Relay media URLs fail through
GitHub's camo proxy (`Non-Image content-type returned`). External hosts are
unreliable and may expose content.

**ALWAYS use `scripts/post-screenshots.sh`** — it hosts PNGs on a per-developer
git branch with immutable commit-SHA URLs that render correctly on GitHub.

## Step 1 — Capture Screenshots

`just desktop-screenshot` builds the frontend, starts a preview server, and
runs Playwright with the mock bridge (no relay needed).

```bash
just desktop-screenshot --name home
just desktop-screenshot --name channel --route /channels/general
just desktop-screenshot --name ctx-menu --right-click channel-random --clip 0,200,320,300
```

**Flags:** `--name` (filename, required), `--route` (client route), `--active-channel`
(channel to view), `--click`/`--right-click`/`--hover` (interact before capture),
`--clip` (crop as `x,y,w,h`), `--messages` (JSON file), `--wait` (ms, default 2000),
`--viewport` (WxH, default 1280x720), `--outdir` (default `test-results/screenshots`).

## Step 2 — Post to a PR

```bash
./scripts/post-screenshots.sh <PR-number> test-results/screenshots
./scripts/post-screenshots.sh <PR-number> test-results/screenshots body.md
```

The script pushes images to `agent-screenshots/<github-username>` and posts a
PR comment with `## Screenshots` and all images. Re-runs overwrite that PR's
images only.
```

---

## Available Skills (11 Total)

*(Note — 5 distinct skills are duplicated across agent-framework directories; the `.claude/`, `.codex/`, `.goose/`, and `.agents/` copies are pointer files to the managed-agent sources under `desktop/src-tauri/src/managed_agents/`.)*

| Skill | Location | Description |
|-------|----------|-------------|
| desktop-screenshot | .claude/skills/ | Capture and host PR screenshots |
| buzz-cli (dir: sprout-cli) | .claude/skills/ | Buzz CLI for relay operations (owner-reviewed agent drafts, messaging, channels, DMs, users, workflows, feed, reactions, canvas, social, repos, uploads, and agent memory); skill frontmatter name is `buzz-cli`, directory keeps the legacy `sprout-cli` name |
| desktop-screenshot | .codex/skills/ | Codex version |
| buzz-cli (dir: sprout-cli) | .codex/skills/ | Codex version |
| desktop-screenshot | .goose/skills/ | Goose version |
| buzz-cli (dir: sprout-cli) | .goose/skills/ | Goose version |
| desktop-screenshot | .agents/skills/ | Agents-format version |
| buzz-cli (dir: sprout-cli) | .agents/skills/ | Agents-format version |
| github-research | examples/meadow-core/skills/github-research/ | GitHub research skill |
| buzz-cli | desktop/src-tauri/src/managed_agents/nest_skill.md | Managed agent skill (source file for the buzz-cli skill) |
| desktop-screenshot | desktop/src-tauri/src/managed_agents/screenshot_skill.md | Managed screenshot skill (source file) |

---

## Repo Structure

```
crates/
  # Relay + core
  buzz-relay          # WebSocket relay server
  buzz-core           # Core types, event verification
  buzz-db             # Postgres event store
  buzz-auth           # Authentication and authorization
  buzz-pubsub         # Redis pub/sub fan-out
  # Agent surface
  buzz-acp            # ACP harness bridging Buzz events to AI agents
  buzz-agent          # Minimal ACP-compliant agent
  buzz-dev-mcp        # Developer MCP server
  buzz-persona        # Agent persona packs
  buzz-workflow       # YAML-as-code workflow engine
  # Clients + interop
  buzz-cli            # Agent-first CLI
  buzz-sdk            # Typed Nostr event builders
  sprig               # All-in-one harness

desktop/              # Tauri 2 + React 19 desktop app
mobile/               # Flutter mobile app
migrations/           # SQL migrations
```

---

## Evaluation Dimensions

### 1. Multi-Framework Skill Support
- [ ] Claude skills directory
- [ ] Codex skills directory
- [ ] Goose skills directory
- [ ] Cross-framework skill compatibility

### 2. Skill Definition Quality
- [ ] Clear name and description
- [ ] Version metadata
- [ ] Step-by-step instructions
- [ ] Critical warnings highlighted

### 3. Screenshot Workflow
- [ ] Capture via Playwright
- [ ] Immutable URL hosting
- [ ] PR integration
- [ ] GitHub camo compatibility

### 4. Managed Agent Support
- [ ] Nest skill for managed agents
- [ ] Screenshot skill as managed agent
- [ ] Desktop app integration
- [ ] Tauri command interface

### 5. Ecosystem Integration
- [ ] Relay for communication
- [ ] Persona packs
- [ ] Workflow engine
- [ ] MCP server support

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Multi-Framework Skill Support | 25% | | |
| Skill Definition Quality | 20% | | |
| Screenshot Workflow | 20% | | |
| Managed Agent Support | 20% | | |
| Ecosystem Integration | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Skill Execution Tests
1. Capture desktop screenshot
2. Post screenshot to PR
3. Verify immutable URL

### Multi-Framework Tests
1. Load Claude skills
2. Load Codex skills
3. Load Goose skills
4. Test cross-framework compatibility

### Desktop App Tests
1. Run managed screenshot agent
2. Test nest skill functionality
3. Verify Tauri commands

### Relay Tests
1. Connect to relay
2. Test event verification
3. Test pub/sub fan-out

---

## Notes

- Buzz demonstrates multi-framework skill architecture
- Cross-platform skill definitions (Claude, Codex, Goose)
- Screenshot skill shows proper GitHub PR integration
- Managed agents via Tauri desktop app
- Apache-2.0 license allows full examination and modification
- Good reference for building hive mind communication platforms