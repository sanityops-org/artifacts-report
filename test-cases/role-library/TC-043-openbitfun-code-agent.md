# TC-043: OpenBitFun - Code Agent with Rust Runtime Suite

## Metadata
- **Source Project**: OpenBitFun (GCWing/OpenBitFun)
- **GitHub**: github.com/GCWing/OpenBitFun
- **License**: MIT
- **Artifact Type**: Code Agent with general-purpose capabilities and Rust runtime
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction at commit 543e429a01475af0dff552ed44e34d63aa0eeb3a
- **Scope**: Code Agent with general-purpose capabilities and Rust runtime

---

## Project Overview

OpenBitFun is a **Rust workspace plus React frontends** that implements a comprehensive code agent platform. It follows the principle: **"keep product logic platform-agnostic, then expose it through platform adapters"**. The project supports multiple remote scenarios and has a layered architecture.

### Key Characteristics
- **Rust workspace**: Core agent runtime in Rust
- **React frontends**: Desktop, Web UI, Mobile Web
- **9 built-in skills**: Debug, create-agent, find-skills, miniapp-dev, multitask, plan, ppt-design, writing-skills, agent-browser, commit-push-pr
- **Remote workspace support**: SSH, Docker, jump-host chains
- **Layered architecture**: 6 layers from interfaces to contracts

---

## Agent Prompts

### 1. Repository AGENTS.md

```markdown
[中文](AGENTS-CN.md) | **English**

# AGENTS.md

OpenBitFun is a Rust workspace plus React frontends.

Repository rule: **keep product logic platform-agnostic, then expose it through platform adapters**.

## Quick start

1. Read `README.md` and `CONTRIBUTING.md` before architecture-sensitive changes.
2. Use the primary product loop below for normal development.
3. After Rust file changes, prefer `pnpm run fmt:rs` to format only changed or staged `.rs` files.
4. After changes, use the nearest local `AGENTS.md` for the focused verification command.
5. Workspace Rust dependencies own compatible versions, not broad capability unions.

## Layered Module Index

Dependencies flow top to bottom. This table is the physical crate layout, not
the full conceptual architecture.

| # | Layer | Path | Owns |
|---|---|---|---|
| 1 | Interfaces and entrypoints | `src/apps/*`, `src/web-ui` | Product hosts, commands, UI entrypoints |
| 2 | Product assembly | `src/crates/assembly` | Compatibility exports, product capability selection |
| 3 | Adapters | `src/crates/adapters` | AI/transport/WebDriver protocol adapters |
| 4 | Services | `src/crates/services` | Reusable OS, filesystem, terminal, MCP primitives |
| 5 | Execution primitives | `src/crates/execution` | Portable Agent Runtime, named-workflow policy |
| 6 | Stable contracts | `src/crates/contracts` | Shared DTOs, event shapes, runtime ports |

Boundary rules:
- Interfaces and app entrypoints expose selected product behavior; reusable behavior moves down.
- Assembly wires lower layers and selects product capability facts.
- Adapters translate protocols and external-provider shapes.
- Services implement reusable concrete OS, process, terminal capabilities.
```

---

## Skill Definitions

### 1. Debug Skill

```markdown
---
name: debug
description: Use this skill to locate a runtime bug. Add targeted instrumentation, collect reproduction evidence, and confirm the root cause before changing code.
---

# Evidence-driven debugging

Evidence-driven debugging mode activated. Follow the workflow below:

1. Generate multiple hypotheses based on the problem described by the user.

2. Insert narrow, hypothesis-specific instrumentation for each hypothesis.

3. Provide reproduction steps and ask the user to reproduce the issue.

4. Read the captured runtime data and identify the confirmed root cause.

5. Implement fix based on the confirmed root cause.

6. If the user confirms the issue has been resolved, clean up all inserted log 
   statements; otherwise, add more logs or generate new hypotheses

IMPORTANT: Do not implement a fix until it is supported by runtime evidence.
IMPORTANT: Do not clean up instrumentation until the user confirms the issue
has been fixed.

## Rules

- Before reading `debug-agent.log`, check its size and approximate entry count.
  Do not read a large log end-to-end in one pass; filter by hypothesis ID,
  location, time range, or other relevant keywords.

- Before each new request for the user to reproduce the issue, clear the
  existing `debug-agent.log`.

- Separate diagnosis from repair selection.

## How to Write to Log Files

1. All logs must be written to `{project_root}/debug-agent.log`.

2. Inserted log statements should be wrapped with appropriate comment statements.

3. Log content should include: hypothesis ID (A/B/C/...), log location, and specific information.

4. Backend: write via file IO
```rust
// #region agent log
{
    use std::io::Write;
    if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(r"absolute\path\to\debug-agent.log") {
        let _ = writeln!(f, "log_content");
    }
}
// #endregion
```

5. Frontend: start the bundled receiver script, then write via `fetch`.
```

---

## Available Skills (9 Total)

| Skill | Description |
|-------|-------------|
| debug | Evidence-driven debugging with instrumentation |
| create-agent | Create new agent instances |
| find-skills | Discover and search available skills |
| miniapp-dev | MiniApp development skill |
| multitask | Parallel task execution |
| plan | Task planning and breakdown |
| ppt-design | PowerPoint design assistance |
| writing-skills | Writing and documentation skills |
| agent-browser | Browser automation skill |
| commit-push-pr | Git commit, push, and PR creation |

---

## Remote Scenarios

| Scenario | Description | Design Entry Point |
|----------|-------------|-------------------|
| Remote workspace | Workspace lives on SSH host, Docker container, or jump-host chain | remote-workspace-transport.md |
| Remote control | Mobile web or bot drives session on Desktop/CLI host | mobile-web AGENTS.md |
| Peer Device Mode | One device becomes data plane of another | peer-device-mode.md |
| Detached Dispatch | Submit durable job to another host | detached-task-dispatch.md |

**Remote Rules:**
- Design the remote path together with the feature
- Degrade loudly when unsupported
- Keep blocking interaction answerable from a distance
- Survive disconnect
- Remote workspace paths are POSIX on every client OS

---

## Layered Architecture

```
Layer 1: Interfaces and entrypoints
  └── desktop, CLI, server, relay, Web UI, mobile web, installer

Layer 2: Product assembly
  └── agent-content, core, external-sources, product-capabilities

Layer 3: Adapters
  └── agent-runtime-ipc, ai-adapters, opencode-adapter, claude-code-adapter

Layer 4: Services
  └── services-core, services-integrations, miniapp-market-service

Layer 5: Execution primitives
  └── agent-runtime, agent-workflows, agent-stream, tool-contracts

Layer 6: Stable contracts
  └── core-types, events, runtime-ports, product-domains
```

---

## Evaluation Dimensions

### 1. Layered Architecture Quality
- [ ] Clear layer boundaries
- [ ] Dependency direction enforced
- [ ] Reusable behavior in lower layers
- [ ] Platform-agnostic core

### 2. Skill Definition Quality
- [ ] Clear name and description
- [ ] Step-by-step workflow
- [ ] Important rules highlighted
- [ ] Multi-language logging support

### 3. Remote Workspace Support
- [ ] SSH host support
- [ ] Docker container support
- [ ] Jump-host chain support
- [ ] POSIX path handling

### 4. Debug Skill Workflow
- [ ] Hypothesis generation
- [ ] Instrumentation insertion
- [ ] Evidence collection
- [ ] Root cause confirmation

### 5. Rust Runtime Quality
- [ ] Async runtime support
- [ ] Cross-platform compatibility
- [ ] Memory safety
- [ ] Performance optimization

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Layered Architecture Quality | 25% | | |
| Skill Definition Quality | 20% | | |
| Remote Workspace Support | 20% | | |
| Debug Skill Workflow | 20% | | |
| Rust Runtime Quality | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Architecture Tests
1. Verify layer dependencies
2. Test platform-agnostic core
3. Validate adapter isolation

### Skill Tests
1. Run debug skill workflow
2. Test hypothesis instrumentation
3. Verify log file operations

### Remote Workspace Tests
1. Connect to SSH host
2. Execute in Docker container
3. Test jump-host chain

### Multi-Platform Tests
1. Run on Windows
2. Run on macOS
3. Run on Linux
4. Verify POSIX path handling

### Debug Workflow Tests
1. Generate hypotheses
2. Insert instrumentation
3. Collect evidence
4. Confirm root cause
5. Clean up logs

---

## Notes

- OpenBitFun demonstrates sophisticated layered architecture
- Platform-agnostic core with platform adapters
- Evidence-driven debugging skill shows best practices
- Remote workspace support is first-class
- MIT license allows full examination and modification
- Good reference for building code agents with Rust runtime