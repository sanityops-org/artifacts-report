# TC-040: Leon - Personal Assistant Suite

## Metadata
- **Source Project**: Leon (leon-ai/leon)
- **GitHub**: github.com/leon-ai/leon
- **License**: MIT
- **Artifact Type**: Personal assistant with multi-language SDK and skills
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction at commit 111ccc8de5719108eebd4906ed0485cba5de7a50
- **Scope**: Leon open-source personal assistant; multi-language SDK, tools, and prompt templates

---

## Project Overview

Leon is an **open-source personal AI assistant** with a granular structure: **skills > actions > tools > functions > binaries**. It provides multi-language SDKs for building skills and tools, with template-based prompt generation.

### Key Characteristics
- **Multi-language SDK**: Node.js (TypeScript) and Python SDKs
- **Granular architecture**: Skills > Actions > Tools > Functions > Binaries
- **Template-based prompts**: Create skill/tool templates with prompts
- **Skill synchronization**: Setup scripts for dependency management

---

## Prompt Templates

### 1. Create Skill Template

```markdown
# Create New Skill for Leon AI

I'm developing Leon AI, an open-source personal AI assistant. It has a granular structure: skills > actions > tools > functions > binaries.

## Goal

...
```

### 2. Create Tool Template

Similar template structure for tool creation with prompts and configuration.

---

## Tool SDKs

### 1. Node.js Base Tool SDK

```typescript
// bridges/nodejs/src/sdk/base-tool.ts
// Multi-language tool SDK for Node.js/TypeScript
```

### 2. Python Base Tool SDK

```python
# bridges/python/src/sdk/base_tool.py
# Multi-language tool SDK for Python
```

---

## Skill Scripts

### 1. Sync Skill Dependencies

```javascript
// scripts/setup/setup-skills/sync-skill-dependencies.js
// Synchronize skill dependencies across the project
```

### 2. Setup Skills

```javascript
// scripts/setup/setup-skills/setup-skills.js
// Initialize and configure skills for Leon
```

### 3. Setup Skills Settings

```javascript
// scripts/setup/setup-skills/setup-skills-settings.js
// Configure skill settings during setup
```

---

## Architecture Pattern

### Leon Structure

```
leon/
├── bridges/              # Multi-language SDKs
│   ├── nodejs/
│   │   └── src/sdk/      # TypeScript SDK
│   └── python/
│       └── src/sdk/      # Python SDK
├── scripts/
│   └── setup/
│       └── setup-skills/ # Skill setup scripts
└── skills/               # Skill definitions
```

### Granular Hierarchy

```
Skills (High-level capabilities)
  └── Actions (Named operations)
      └── Tools (External integrations)
          └── Functions (API calls)
              └── Binaries (Executables)
```

---

## Evaluation Dimensions

### 1. SDK Design Quality
- [ ] TypeScript SDK is well-typed
- [ ] Python SDK follows Python conventions
- [ ] Both SDKs have consistent API
- [ ] Base classes provide good defaults

### 2. Template System
- [ ] Skill template is comprehensive
- [ ] Tool template follows best practices
- [ ] Prompts are customizable
- [ ] Template generation is automated

### 3. Skill Management
- [ ] Dependency synchronization
- [ ] Setup automation
- [ ] Version management
- [ ] Cross-platform support

### 4. Multi-Language Support
- [ ] Node.js SDK parity with Python
- [ ] Language-specific conventions respected
- [ ] Shared patterns between SDKs
- [ ] Easy to add new languages

### 5. Extensibility
- [ ] New skills can be added easily
- [ ] Tools integrate cleanly
- [ ] Custom actions supported
- [ ] Plugin architecture

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| SDK Design Quality | 25% | | |
| Template System | 20% | | |
| Skill Management | 20% | | |
| Multi-Language Support | 20% | | |
| Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### SDK Tests
1. Create tool using Node.js SDK
2. Create tool using Python SDK
3. Verify SDK API consistency

### Template Tests
1. Generate skill from template
2. Generate tool from template
3. Customize prompts

### Setup Tests
1. Run skill dependency sync
2. Run skill setup script
3. Verify skill configuration

### Integration Tests
1. Create skill with multiple actions
2. Add tool to skill
3. Execute skill end-to-end

---

## Notes

- Leon demonstrates granular personal assistant architecture
- Multi-language SDK support (Node.js, Python)
- Template-based skill/tool creation
- Hierarchical structure: Skills > Actions > Tools > Functions > Binaries
- MIT license allows full examination and modification
- Good reference for building extensible personal assistants