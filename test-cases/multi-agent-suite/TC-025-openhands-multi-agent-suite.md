# TC-025: OpenHands - Multi-Agent Suite

## Metadata
- **Source Project**: OpenHands (OpenHands/OpenHands)
- **Commit SHA**: fa1f724ab5737a17453ad6081129eb91c5a423c6
- **License**: MIT
- **Artifact Type**: Multi-Agent Framework / Development Platform
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

OpenHands is an **autonomous software development agent platform** that provides comprehensive tools and skills for software development workflows. It includes specialized skills for desktop development, testing, frontend development, and more.

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Development Skills** | Specialized workflows for various development tasks | Skill |
| **Desktop Electron** | Electron app packaging and development | Skill |
| **Frontend Development** | React/Vue/TypeScript development patterns | Skill |
| **E2E Testing** | End-to-end testing workflows | Skill |
| **PR Design Doc** | Pull request documentation patterns | Skill |

---

## Logical Artifact Inventory

### 1. System Prompts (0)

Note: OpenHands core system prompts are defined in the codebase. The project focuses on **skills-based workflows** rather than explicit system prompts for agents.

---

### 2. Tool Schemas (0)

Note: OpenHands tools (bash, editor, browser, search) are defined in the codebase. This test case focuses on the **bundled skills**.

---

### 3. Skills (8)

#### 3.1 Desktop Electron Skill
```markdown
# .agents/skills/desktop-electron/SKILL.md

---
name: desktop-electron
description: This skill should be used when the user asks to "change the desktop app", "package Electron", "build a universal macOS app", "bundle Node or uv", "fix Electron startup", or changes electron/, electron-builder.config.mjs, desktop workflows, bundled runtimes, or desktop process startup.
---

# Electron Desktop

Preserve desktop startup reliability and packaging invariants across development, installed single-architecture builds, and universal macOS builds.

## Workflow

1. Read `references/guide.md` before changing Electron startup, branding, packaging hooks, runtime resources, or desktop CI.
2. Test cold-start readiness independently from ingress readiness.
3. Keep packaged dependency stripping and the explicit runtime package closure synchronized.
4. Validate bundled Node and uv paths on every affected platform and architecture.
5. Test installed artifacts outside the repository tree so local `node_modules` cannot hide missing packaged dependencies.

## Reference

- **`references/guide.md`** — Cold-start coordination, loading feedback, node_modules stripping, universal runtime layout, macOS development branding, and bundled Node/npm/npx behavior.
```

#### 3.2 E2E Testing Skill
```markdown
# .agents/skills/e2e-testing/SKILL.md

---
name: e2e-testing
description: This skill should be used when the user asks to "add an E2E test", "run live E2E", "run mock-LLM tests", "debug Playwright CI", "test the Docker image", or changes tests/e2e, Playwright configs, E2E workflows, artifacts, or test reporting.
---
```

#### 3.3 Frontend API Contracts Skill
```markdown
# .agents/skills/frontend-api-contracts/SKILL.md

---
name: frontend-api-contracts
description: This skill should be used when the user asks to "add an API call", "change a backend", "update settings persistence", "change conversation events", "fix backend auth", "add Agent Server support", or changes src/api, backend registry, Cloud/runtime transport, settings, secrets, compatibility, or conversation resume behavior.
---
```

#### 3.4 Frontend Development Skill
```markdown
# .agents/skills/frontend-development/SKILL.md

---
name: frontend-development
description: This skill should be used when the user asks to "add UI copy", "add a translation", "optimize the frontend bundle", "change onboarding", "change conversation UI", "add a query key", "change MSW mocks", or modifies React components, hooks, routes, i18n, lazy loading, persisted UI state, or shared frontend behavior.
---
```

#### 3.5 Local Stack Runtime Skill
```markdown
# .agents/skills/local-stack-runtime/SKILL.md

---
name: local-stack-runtime
description: This skill should be used when the user asks to "change the dev stack", "add a runtime service", "change the launcher", "update Docker", "bump Agent Server", "change ingress routing", or changes scripts/dev-*.mjs, runtime-services metadata, config/defaults.json, Docker, automation startup, process shutdown, or local authentication.
---
```

#### 3.6 PR Design Doc Skill
```markdown
# .agents/skills/pr-design-doc/SKILL.md

---
name: pr-design-doc
description: >
  For a non-trivial pull request, write a self-contained HTML design doc under the
  temporary `.pr/` directory and link a visibility-appropriate preview in the PR
  description, so maintainers grasp the proposal at a glance - code/API design, and the
  before/after of the change, grounded to real code. Use when opening or updating a
  non-trivial PR, or when the user says "add a design doc", "document this PR for
  reviewers", "show the before/after", "make the design reviewable", or "write the .pr/
  page".
triggers:
- /pr-design-doc
- /design-doc
license: MIT
metadata:
  tags: pull-request, design-doc, html, review, before-after, htmlpreview
---
```

#### 3.7 Telemetry Analytics Skill
```markdown
# .agents/skills/telemetry-analytics/SKILL.md

---
name: telemetry-analytics
description: This skill should be used when the user asks to "add tracking", "add a PostHog event", "change telemetry consent", "instrument onboarding", "debug analytics", or changes telemetry.ts, use-tracking.ts, cloud funnel analytics, or analytics environment variables.
---
```

#### 3.8 Verify OpenHands Skill
```markdown
# .agents/skills/verify-openhands/SKILL.md

---
name: verify-openhands
description: >
  This skill should be used to "verify OpenHands features", "test the Canvas UI
  like a user", "drive Agent Canvas", "check a UI change in the real app",
  "create or update the feature map", "run the daily pass" or "run the weekly
  feature audit". Ships control-openhands (launch, doctor, browser, LLM
  profiles, conversations, evidence, map tooling, cleanup) and the maintained
  map of every user-facing feature.
triggers:
- /verify-openhands
- feature map
- verify feature
---
```

*(Note — `.agents/skills/` additionally contains two loose skill-format files with the same frontmatter style: `custom-codereview-guide.md` and `release.md`; counting them, the directory holds 10 skill artifacts.)*

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Each skill has clear trigger conditions in description
- [ ] Skills define specific workflow steps
- [ ] Reference documentation links provided

### 2. Workflow Completeness
- [ ] Step-by-step instructions in skill bodies
- [ ] Reference guides for complex workflows
- [ ] Integration with development toolchain

### 3. Prompt Consistency
- [ ] Standardized skill format with name and description
- [ ] Clear workflow sections
- [ ] Reference documentation structure

### 4. Tool Modularity
- [ ] Skills reference external tools (electron-builder, playwright, etc.)
- [ ] Tool-specific workflow steps
- [ ] Integration with CI/CD

### 5. Observability
- [ ] Test instructions in skills
- [ ] Validation steps
- [ ] Debugging guidance

### 6. Extensibility
- [ ] Custom skill creation pattern
- [ ] Reference guide system
- [ ] Modular skill organization

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Electron packaging**: Test desktop app build on multiple platforms
2. **E2E testing**: Run Playwright tests with mock-llm configuration
3. **PR workflow**: Test skill-triggered PR documentation generation

### Unit Tests
1. **Skill matching**: Verify correct skill activation from user queries
2. **Workflow execution**: Test skill step execution
3. **Reference loading**: Verify reference guide access

### Integration Tests
1. **Frontend development**: Test React component creation workflow
2. **Telemetry**: Verify analytics implementation patterns
3. **Local stack**: Test runtime configuration and startup

---

## Notes

- **MIT license** allows full quotation and modification
- OpenHands emphasizes **skill-based workflows** for development tasks
- Skills provide **domain-specific guidance** for software development
- The platform integrates **CI/CD and testing** into skill definitions