# TC-033: OpenAgent - File-Based Multi-Agent Suite

## Metadata
- **Source Project**: the-open-agent/openagent
- **GitHub**: https://github.com/the-open-agent/openagent
- **Commit SHA**: ff329d8fa818de702df696da199b3a72afe02143
- **License**: Apache-2.0
- **Artifact Type**: File-based logical artifacts
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API retrieval via `gh api`

---

## Project Overview

OpenAgent is a **next-generation personal AI assistant** that ships as a **single binary** with no installation needed. It combines LLMs, RAG knowledge bases, and autonomous agent loops in one self-hostable platform. Built with Go backend (Beego framework) and React frontend (shadcn/ui, Vite), it supports 30+ model providers and 54 skills across productivity, automation, and integrations.

### Key Features
- **Single binary deployment**: Ships as one executable, no dependencies required
- **30+ model providers**: OpenAI, Anthropic, Gemini, DeepSeek, Mistral, and more
- **Autonomous agent loops**: Browser-use, web search, shell execution, office automation
- **MCP integration**: Plug any MCP-compatible server (SSE/Stdio/StreamableHTTP)
- **RAG knowledge base**: Document ingestion, semantic search, pluggable embeddings
- **Cross-platform**: Linux, macOS, Windows (x86_64/arm64)

---

## Logical Artifact Inventory

### 1. CLAUDE.md - Development Guidance

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Backend (Go)**
```bash
go build                    # build backend binary
go run main.go              # run backend (port 14000)
go test ./...               # run all tests
```

**Frontend (React + shadcn/ui, built with Vite)**
```bash
cd web && yarn install
yarn start                  # dev server on port 13001
yarn build                  # production build
```

## Architecture

### Backend (Go / Beego)

Every entity follows the same three-layer pattern:

1. **`object/<entity>.go`** — struct definition (xorm tags for DB), and all DB access functions
2. **`controllers/<entity>.go`** — Beego controller methods wired to routes
3. **`routers/router.go`** — `beego.Router` calls grouped by entity

**DB schema** is auto-migrated via `object/adapter.go` → `createTable()`.

### Frontend (React + shadcn/ui on Tailwind, TypeScript, Vite)

**Routing** lives in `web/src/App.tsx`; every file in `web/src/pages` is its own lazy chunk.

### Key conventions

- Owner is always `"admin"` for system-created entities.
- Entity `Name` is a random string or a user-provided slug.
- All API responses go through `c.ResponseOk(data)` or `c.ResponseError(msg)`.
```

### 2. README.md Overview

```markdown
# OpenAgent

**Next-generation personal AI assistant powered by LLM, RAG and agent loops — ships as a single binary, no installation needed**

## Quick Start

**macOS / Linux / WSL**
```bash
curl -fsSL https://raw.githubusercontent.com/the-open-agent/openagent/master/scripts/install.sh | bash
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/the-open-agent/openagent/master/scripts/install.ps1 | iex
```

Open [http://localhost:14000](http://localhost:14000) and you're in.

## Features

### 30+ Model Providers
`OpenAI` · `Azure OpenAI` · `Anthropic Claude` · `Google Gemini` · `DeepSeek` · `Mistral` · `Grok` · `Qwen` · `Doubao` · `Moonshot` · `ChatGLM` · `Baichuan` · `Ernie` · `iFlytek` · `HuggingFace` · `Cohere` · `Amazon Bedrock` · `OpenRouter` · `Ollama` · `APIMart` · `and more`

### Autonomous Agent Loops

| Capability | Description |
|:-----------|:------------|
| **Browser-Use** | Drive a real browser — navigate, click, fill forms, scrape |
| **Web Search & Fetch** | Search the web and pull live page content |
| **Shell Execution** | Run shell commands and scripts |
| **Office Automation** | Read and write Word, Excel, PowerPoint files |
| **MCP Integration** | Plug in any MCP-compatible server |

### RAG & Knowledge Base

| Capability | Description |
|:-----------|:------------|
| **Document Ingestion** | Upload PDFs, Word docs, Excel sheets |
| **Semantic Search** | Retrieves relevant passages before each response |
| **Pluggable Embeddings** | OpenAI, Azure, Gemini, Qwen, Cohere, Jina, local models |
```

---

## Tool Definitions (Go)

### MCP Tools

```go
// Copyright 2026 The OpenAgent Authors. All Rights Reserved.
// Licensed under the Apache License, Version 2.0

package mcp

import (
	"context"
	"fmt"
	"time"

	"github.com/ThinkInAIXYZ/go-mcp/client"
	"github.com/ThinkInAIXYZ/go-mcp/protocol"
	"github.com/ThinkInAIXYZ/go-mcp/transport"
)

// GetToolsFromURL connects to an HTTP-based MCP server and returns its tool list.
// Always uses StreamableHTTP transport (the current MCP standard).
func GetToolsFromURL(url, token string) ([]*protocol.Tool, error) {
	var tr transport.ClientTransport
	var err error

	if token != "" {
		tr, err = transport.NewStreamableHTTPClientTransport(url,
			transport.WithStreamableHTTPClientOptionHeader(map[string]string{
				"Authorization": "Bearer " + token,
			}),
		)
	} else {
		tr, err = transport.NewStreamableHTTPClientTransport(url)
	}
	if err != nil {
		return nil, fmt.Errorf("mcp: create transport for %s: %w", url, err)
	}

	cli, err := client.NewClient(tr)
	if err != nil {
		return nil, fmt.Errorf("mcp: create client for %s: %w", url, err)
	}
	defer cli.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	list, err := cli.ListTools(ctx)
	if err != nil {
		return nil, fmt.Errorf("mcp: list tools from %s: %w", url, err)
	}
	return list.Tools, nil
}

// GetToolsFromConfig — URL-based (SSE / StreamableHTTP) or stdio (command + args).
// It is the stdio-aware counterpart of GetToolsFromURL.
func GetToolsFromConfig(cfg ServerConfig) ([]*protocol.Tool, error) {
	cli, err := createClient(cfg)
	if err != nil {
		return nil, fmt.Errorf("mcp: create client for %s: %w", describeServerConfig(cfg), err)
	}
	defer cli.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	list, err := cli.ListTools(ctx)
	if err != nil {
		return nil, fmt.Errorf("mcp: list tools from %s: %w", describeServerConfig(cfg), err)
	}
	return list.Tools, nil
}
```

---

## Skills (Selected Examples)

### GitHub Skill

```markdown
---
name: github
description: Use when interacting with GitHub repositories, authentication, remotes, pushes, or repository creation through the GitHub CLI and related git workflows.
homepage: https://cli.github.com/
metadata:
  { "emoji": "🐙" }
---

# GitHub

## Core Rules

- Prefer `gh` over raw GitHub API calls.
- Prefer existing authenticated state over asking for new credentials.
- Prefer non-interactive checks before prompting the user.
- Never print, echo, log, summarize, or restate secrets.
- Never switch credential strategy unless the current one actually fails.

## Credential Handling Priority

### 1. Reuse `gh` authentication first
- `gh auth status`
- If authenticated, continue with repo detection, `gh repo create`, remote setup, push

### 2. If `gh` exists but **is** not authenticated, log in with `gh` directly
- Browser/web login: `gh auth login -h github.com -w`
- Standard interactive: `gh auth login -h github.com`

### 3. If `gh` is unavailable, try to install it first
- Homebrew on macOS, `apt`/`dnf` on Linux, `winget` on Windows

### 4. If `gh` is still unavailable, fall back to Git
- Plain `git` with existing SSH auth or credential helpers

## Standard Execution Flow

1. Detect environment: Git repo? Remote? `gh` installed? `gh` authenticated?
2. If already connected to GitHub: just push
3. If Git repo exists but no GitHub repo: create with `gh repo create`
4. If not a Git repo: initialize, create GitHub repo, add remote, push
```

### Coding-Agent Skill

```markdown
---
name: coding-agent
description: 'Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat. Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.'
metadata:
  { "openclaw": { "emoji": "🧩", "requires": { "anyBins": ["claude", "codex", "opencode", "pi"] } } }
---

# Coding Agent (bash-first)

Use **bash** (with optional background mode) for all coding agent work.

## ⚠️ PTY Mode: Codex/Pi/OpenCode yes, Claude Code no

For **Codex, Pi, and OpenCode**, PTY is required:

```bash
# ✅ Correct for Codex/Pi/OpenCode
bash pty:true command:"codex exec 'Your prompt'"
```

For **Claude Code**, use `--print --permission-mode bypassPermissions`:

```bash
# ✅ Correct for Claude Code (no PTY needed)
cd /path/to/project && claude --permission-mode bypassPermissions --print 'Your task'
```

## The Pattern: workdir + background + pty

```bash
# Start agent in target directory
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build feature'"

# Monitor progress
process action:log sessionId:XXX

# Send input
process action:submit sessionId:XXX data:"yes"
```

## Parallel Issue Fixing with git worktrees

```bash
# Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main

# Launch Codex in each
bash pty:true workdir:/tmp/issue-78 background:true command:"codex --yolo 'Fix issue #78'"

# Create PR after fix
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --title "fix: ..."
```
```

### Notion Skill

```markdown
---
name: notion
description: Notion API for creating and managing pages, databases, and blocks.
homepage: https://developers.notion.com
metadata:
  { "emoji": "📝", "requires": { "env": ["NOTION_API_KEY"] } }
---

# notion

Use the Notion API to create/read/update pages, data sources (databases), and blocks.

## Setup

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it: `echo "ntn_your_key_here" > ~/.config/notion/api_key`
4. Share target pages/databases with your integration

## API Basics

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

## Common Operations

**Search for pages and data sources:**
```bash
curl -X POST "https://api.notion.com/v1/search" \
  -d '{"query": "page title"}'
```

**Create page in a data source:**
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -d '{"parent": {"database_id": "xxx"}, "properties": {...}}'
```

**Query a data source (database):**
```bash
curl -X POST "https://api.notion.com/v1/data_sources/{id}/query" \
  -d '{"filter": {...}, "sorts": [...]}'
```

## Key Differences in 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries
- **Two IDs:** Each database has both `database_id` and `data_source_id`
```

### Weather Skill

```markdown
---
name: weather
description: "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed."
homepage: https://wttr.in/:help
metadata:
  { "emoji": "☔", "requires": { "bins": ["curl"] } }
---

# Weather Skill

## When to Use

✅ Weather queries, temperature, forecasts for any location
❌ Historical weather, severe weather alerts, meteorological analysis

## Commands

### Current Weather

```bash
# One-line summary
curl "wttr.in/London?format=3"

# Detailed current conditions
curl "wttr.in/London?0"
```

### Forecasts

```bash
# 3-day forecast
curl "wttr.in/London"

# Week forecast
curl "wttr.in/London?format=v2"
```

### Format Codes

- `%c` — Weather condition emoji
- `%t` — Temperature
- `%w` — Wind
- `%h` — Humidity
```

### Obsidian Skill

*(Correction — the previously quoted "filesystem-first `OBSIDIAN_VAULT_PATH`" content belonged to hermes-agent's obsidian skill, not openagent. The real openagent skill below is obsidian-cli based.)*

```markdown
---
name: obsidian
description: Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.
homepage: https://help.obsidian.md
metadata:
  {
    "openclaw":
      {
        "emoji": "💎",
        "requires": { "bins": ["obsidian-cli"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "yakitrak/yakitrak/obsidian-cli",
              "bins": ["obsidian-cli"],
              "label": "Install obsidian-cli (brew)",
            },
          ],
      },
  }
---

# Obsidian

Obsidian vault = a normal folder on disk.

Vault structure (typical)

- Notes: `*.md` (plain text Markdown; edit with any editor)
- Config: `.obsidian/` (workspace + plugin settings; usually don’t touch from scripts)
- Canvases: `*.canvas` (JSON)
- Attachments: whatever folder you chose in Obsidian settings (images/PDFs/etc.)

## Find the active vault(s)

Obsidian desktop tracks vaults here (source of truth):

- `~/Library/Application Support/obsidian/obsidian.json`

`obsidian-cli` resolves vaults from that file; vault name is typically the **folder name** (path suffix).

Fast “what vault is active / where are the notes?”

- If you’ve already set a default: `obsidian-cli print-default --path-only`
- Otherwise, read `~/Library/Application Support/obsidian/obsidian.json` and use the vault entry with `"open": true`.

Notes

- Multiple vaults common (iCloud vs `~/Documents`, work/personal, etc.). Don’t guess; read config.
- Avoid writing hardcoded vault paths into scripts; prefer reading the config or using `print-default`.

## obsidian-cli quick start

Pick a default vault (once):

- `obsidian-cli set-default "<vault-folder-name>"`
- `obsidian-cli print-default` / `obsidian-cli print-default --path-only`

Search

- `obsidian-cli search "query"` (note names)
- `obsidian-cli search-content "query"` (inside notes; shows snippets + lines)

Create

- `obsidian-cli create "Folder/New note" --content "..." --open`
- Requires Obsidian URI handler (`obsidian://…`) working (Obsidian installed).
- Avoid creating notes under “hidden” dot-folders (e.g. `.something/...`) via URI; Obsidian may refuse.

Move/rename (safe refactor)

- `obsidian-cli move "old/path/note" "new/path/note"`
- Updates `[[wikilinks]]` and common Markdown links across the vault (this is the main win vs `mv`).

Delete

- `obsidian-cli delete "path/note"`

Prefer direct edits when appropriate: open the `.md` file and change it; Obsidian will pick it up.
```

---

## Evaluation Dimensions

### 1. Single-Binary Deployment
- [ ] True single-binary distribution (no external dependencies)
- [ ] Cross-platform support (Linux, macOS, Windows)
- [ ] Embedded static file serving for frontend

### 2. Model Provider Abstraction
- [ ] 30+ model providers supported out of the box
- [ ] Per-conversation model switching
- [ ] Pluggable provider architecture

### 3. Skill Architecture
- [ ] Skills follow consistent SKILL.md format with YAML frontmatter
- [ ] Each skill has clear prerequisites (env vars, binaries)
- [ ] Skills provide practical command examples

### 4. MCP Integration
- [ ] StreamableHTTP transport for HTTP-based MCP servers
- [ ] Stdio transport for command-based MCP servers
- [ ] Token-based authentication support

### 5. Agent Loop Capabilities
- [ ] Browser-use for web automation
- [ ] Web search and fetch for live content
- [ ] Shell execution for system operations
- [ ] Office automation for document manipulation

### 6. RAG Knowledge Base
- [ ] Document ingestion with automatic chunking
- [ ] Semantic search with pluggable embeddings
- [ ] Isolated stores per chat/application

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Single-Binary Deployment | 15% | | |
| Model Provider Abstraction | 20% | | |
| Skill Architecture | 20% | | |
| MCP Integration | 15% | | |
| Agent Loop Capabilities | 15% | | |
| RAG Knowledge Base | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Deployment Tests
1. **Single-binary verification**: Verify binary runs without external dependencies
2. **Cross-platform**: Test on Linux, macOS, Windows (x86_64 and arm64)
3. **Embedded frontend**: Verify frontend assets are correctly embedded

### Model Provider Tests
1. **Provider switching**: Verify per-conversation model changes
2. **Credential management**: Test API key storage and retrieval
3. **Fallback models**: Verify fallback chain works correctly

### MCP Integration Tests
1. **StreamableHTTP**: Test connection to HTTP-based MCP servers
2. **Stdio transport**: Test command-based MCP servers
3. **Tool discovery**: Verify tools are correctly discovered and exposed

### Skill Tests
1. **Skill loading**: Verify skills load from correct paths
2. **Prerequisites**: Test missing prerequisites are detected
3. **Command execution**: Verify skill commands work correctly

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- Demonstrates **single-binary deployment** pattern for AI assistants
- **54 skills** cover productivity, automation, and integrations
- **MCP integration** enables extensible tool ecosystem
- **Go backend + React frontend** provides robust cross-platform solution