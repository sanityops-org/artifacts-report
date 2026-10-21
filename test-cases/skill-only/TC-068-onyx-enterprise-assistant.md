# TC-068: Onyx - Enterprise AI Assistant Skill Suite

## Metadata
- **Source Project**: Onyx (onyx-dot-app/onyx)
- **GitHub**: github.com/onyx-dot-app/onyx
- **License**: MIT (core); some `ee` directories are under a separate enterprise license
- **Artifact Type**: Enterprise AI assistant / search platform with agent skills (`.agents/skills/`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw content fetch from `https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.agents/skills/feature-map/SKILL.md` (branch: `main`)
- **Scope**: Agent skill definitions that describe product surfaces, code paths, and change safety for the Onyx assistant

---

## Project Overview

Onyx is an open-source **enterprise AI assistant and search platform** that connects an organisation's knowledge sources into a single, permission-aware assistant. Beyond the platform code, the repository ships a set of **agent skills** under `.agents/skills/` that teach a coding/operating agent how to reason about the product itself: what each surface does, which code implements it, and what a change can break.

### Key Characteristics
- **Enterprise focus**: permission-aware search, connectors, and assistant experiences for organisations
- **Skills as logical artifacts**: Markdown `SKILL.md` files with YAML frontmatter, one per capability
- **Knowledge-mapping skill**: `feature-map` describes every product surface as a single component document
- **Review-oriented reasoning**: the skill supports "before you change a feature" and "when you review a diff or PR" workflows
- **Mixed licensing surface**: core is MIT, while some `ee` (enterprise edition) directories fall under a separate enterprise license

---

## Agent Prompts

### 1. Skill: feature-map (`.agents/skills/feature-map/SKILL.md`)

````markdown
---
name: feature-map
description: Use the Onyx feature map (.agents/feature-map/) to learn what a product surface does, the code behind it, and what a change can break. Use it before changing a feature, when reviewing a diff or PR, and when asked what a feature does or how parts connect.
---
# Onyx feature map
`.agents/feature-map/` describes every Onyx product surface as one component
document: what the user sees, the code paths, the data model, the contracts, what
else a change touches, how to verify it, and the known traps.
## Find the component
- From a code path: look it up in `.agents/feature-map/PATHS.md`. The longest
  matching prefix wins. A path with no row is unmapped: say so, and read the
  nearest code and tests yourself.
- From a feature name: browse `.agents/feature-map/INDEX.md`.
- Before you trust a name, read `.agents/feature-map/GLOSSARY.md`. Onyx uses words
  such as Persona, Tool, turn and SearchDoc in more than one sense.
## Before you change code
Read the component document under `.agents/feature-map/components/`:
- §1 and §4: what the code must do.
- §5 Contracts and invariants: the rules a change can break without any test
  failing.
- §7 Blast radius: the other files to check for your kind of change.
- §9 Footguns: the known traps.
Follow the `[[component]]` links in §6 for any area your change reaches into.
## When you review a diff or PR
Follow `.agents/feature-map/VERIFYING.md` step by step. Check every invariant in §5
of each touched component and state a verdict for each one. Report what you could
not verify.
## Keep the map true
If your change alters behaviour that a component document describes, update that
document in the same PR. If you add a code path, add its row to `PATHS.md`. Cite
only paths and symbols that exist; a wrong reference is worse than none.
````

---

## Skill Definitions

The skill is expressed as a single `SKILL.md` (YAML frontmatter + Markdown body). Its structure defines a reusable operating procedure over a repository-resident knowledge base.

### Skill Frontmatter

| Field | Value |
|-------|-------|
| name | `feature-map` |
| description | "Use the Onyx feature map (`.agents/feature-map/`) to learn what a product surface does, the code behind it, and what a change can break..." |

### Referenced Knowledge Base (`.agents/feature-map/`)

The skill is a navigation layer over companion documents, each named in the skill body:

| Artifact | Role |
|----------|------|
| `PATHS.md` | Maps code paths → component (longest matching prefix wins) |
| `INDEX.md` | Browse components by feature name |
| `GLOSSARY.md` | Disambiguates overloaded terms (Persona, Tool, turn, SearchDoc) |
| `components/` | One component document per product surface |
| `VERIFYING.md` | Step-by-step procedure for reviewing a diff or PR |

### Component Document Sections (referenced by skill)

| Section | Purpose |
|---------|---------|
| §1 / §4 | What the code must do |
| §5 Contracts and invariants | Rules a change can break without any test failing |
| §6 | `[[component]]` links to adjacent areas |
| §7 Blast radius | Other files to check for your kind of change |
| §9 Footguns | Known traps |

---

## Skill Workflows (as defined in the artifact)

| Workflow | Trigger | Procedure |
|----------|---------|-----------|
| Find the component | Given a code path | Look up in `PATHS.md`; unmapped → read nearest code/tests |
| Find the component | Given a feature name | Browse `INDEX.md`; confirm names via `GLOSSARY.md` |
| Before changing code | Any feature change | Read component §1/§4, §5, §7, §9; follow §6 links |
| Review a diff or PR | Code review | Follow `VERIFYING.md`; verdict per §5 invariant; report unverifiable items |
| Keep the map true | Change alters described behaviour | Update component doc in same PR; add rows to `PATHS.md` |

---

## Evaluation Dimensions

### 1. Skill Definition Quality
- [ ] Frontmatter includes a clear `name` and a trigger-oriented `description`
- [ ] Description states what the skill is for and when to use it
- [ ] Scope is bounded to a single, coherent responsibility (feature knowledge)
- [ ] Body references only artifacts that are named and locatable

### 2. Knowledge-Base Navigability
- [ ] Multiple entry points (code path via `PATHS.md`, feature name via `INDEX.md`)
- [ ] Disambiguation rule for overloaded terms (`GLOSSARY.md`)
- [ ] Explicit fallback behaviour for unmapped paths
- [ ] Component docs decomposed into stable, cited section numbers

### 3. Change-Safety Guidance
- [ ] Invariants (§5) surfaced as first-class review targets
- [ ] Blast radius (§7) and footguns (§9) guidance provided
- [ ] Cross-component links (§6) for downstream areas
- [ ] Verification procedure (`VERIFYING.md`) prescribed for reviews

### 4. Maintainability / Truth-Keeping
- [ ] Docs updated in the same PR as behaviour changes
- [ ] New code paths require new `PATHS.md` rows
- [ ] Instruction to cite only existing paths/symbols
- [ ] Explicit preference for omission over a wrong reference

### 5. Licensing Clarity
- [ ] Core license (MIT) stated
- [ ] Enterprise-licensed `ee` directories flagged separately
- [ ] License boundary documented for evaluators/consumers

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Definition Quality | 20% | | |
| Knowledge-Base Navigability | 25% | | |
| Change-Safety Guidance | 25% | | |
| Maintainability / Truth-Keeping | 20% | | |
| Licensing Clarity | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Skill Loading & Trigger Tests
1. Verify the `SKILL.md` frontmatter parses (name, description) without errors
2. Confirm the skill is selected when the prompt asks "what does feature X do" or "review this diff"
3. Confirm the skill is *not* selected for unrelated tasks (bounded trigger)

### Navigation Tests
1. Given a known code path, confirm the skill resolves the correct component via `PATHS.md`
2. Given an unmapped path, confirm the skill reports it as unmapped rather than guessing
3. Given an ambiguous term (e.g., "turn", "Persona"), confirm `GLOSSARY.md` is consulted

### Change-Safety Tests
1. Provide a diff touching a component; confirm each §5 invariant gets an explicit verdict
2. Confirm unverifiable invariants are reported rather than silently passed
3. Confirm blast-radius (§7) files are surfaced for the change type

### Truth-Keeping Tests
1. Change behaviour described by a component doc; confirm the doc is updated in the same PR
2. Add a code path; confirm a `PATHS.md` row is required
3. Seed a doc with a non-existent symbol; confirm the skill flags the bad reference

### Licensing Tests
1. Confirm the collection notes distinguish MIT core from enterprise `ee` directories
2. Confirm no enterprise-licensed content is quoted beyond what is publicly retrievable

---

## Notes

- Onyx is a **NON-coding, enterprise knowledge-assistant** project; the artifact examined is a *skill that reasons about the product*, not application code.
- The `.agents/skills/feature-map/SKILL.md` file was fetched successfully from the `main` branch (exact URL recorded in Metadata).
- Only the single `SKILL.md` above was retrieved; the companion files it references (`PATHS.md`, `INDEX.md`, `GLOSSARY.md`, `VERIFYING.md`, `components/`) were **not fetched** — they are named in the skill body and are described here from that body only. No companion content is quoted.
- **License note (as required by the task):** the repository core is MIT, but some `ee` directories are distributed under a **separate enterprise license**. Evaluators should keep this boundary in mind before reusing or redistributing artifact text.
- Good reference for **skill-as-navigation-layer** designs, where a small instruction file governs access to a larger curated knowledge base.
