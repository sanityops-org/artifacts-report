# TC-057: baoyu-skills - File-Based Multi-Logical-Artifact Agent Suite

## Metadata
- **Source Project**: jimliu/baoyu-skills
- **GitHub**: github.com/JimLiu/baoyu-skills
- **License**: MIT (skills republished to ClawHub are released under MIT-0 per registry rules)
- **Artifact Type**: File-based logical artifacts (Markdown `SKILL.md` suite, one directory per skill)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub fetch, branch `main`:
  - `https://raw.githubusercontent.com/jimliu/baoyu-skills/main/skills/baoyu-cover-image/SKILL.md`
  - `https://raw.githubusercontent.com/jimliu/baoyu-skills/main/skills/baoyu-post-to-wechat/SKILL.md`
  - `https://raw.githubusercontent.com/JimLiu/baoyu-skills/main/README.md`

---

## Project Overview

baoyu-skills is a **collection of independent, non-coding content Agents** shared by the author "Baoyu" for improving daily work efficiency with AI Agents (Claude Code, Codex, and other runtime agents). Each skill is a self-contained directory containing a `SKILL.md` plus optional `scripts/` and `references/`. The suite focuses on **content creation and publishing**: cover images, article illustrations, social image cards, infographics, SVG diagrams, Markdown formatting, and publishing to WeChat Official Accounts.

The README describes the repository as containing **"20+ skills"**, organized into **Content Skills**, **AI Generation Skills**, and **Utility Skills**. Skills are distributed via `skills.sh`, as a Claude Code plugin marketplace (`/plugin marketplace add JimLiu/baoyu-skills`), and individually to ClawHub/OpenClaw.

### Key Features
- **One directory per skill**: `<skills>/baoyu-<name>/SKILL.md` with co-located scripts and references.
- **Explicit preference files**: skills read an `EXTEND.md` (project → XDG → user-home) for saved preferences such as default output directory or preferred image backend.
- **Runtime-agnostic**: skills detect the host runtime (Claude Code, Codex, Cursor) and select the appropriate native tool.
- **Content-pipeline composition**: a typical WeChat article workflow chains `baoyu-cover-image` → `baoyu-article-illustrator` → `baoyu-post-to-wechat`.
- **Domain**: content creation, visual asset generation, publishing. Non-code.

---

## Logical Artifact Inventory

### Skill Inventory (as determinable from the fetched README and `SKILL.md` files)

Content Skills:
- `baoyu-xhs-images` - Xiaohongshu image-card series generator (Style × Layout system)
- `baoyu-infographic` - Infographic generator (21 layout types × visual styles)
- `baoyu-diagram` - Publication-ready SVG diagram generator (writes SVG by hand, no image model)
- `baoyu-cover-image` - Article cover-image generator (5 dimensions)

Publishing / formatting:
- `baoyu-post-to-wechat` - Post to WeChat Official Account via API or Chrome CDP
- `baoyu-article-illustrator` - Article illustration planner/generator (referenced as part of the WeChat minimal set)
- `baoyu-markdown-to-html` - Markdown → WeChat-ready HTML (bundled inside `baoyu-post-to-wechat`, not separately required)
- `baoyu-format-markdown` - Turn raw text/drafts into structured Markdown articles

AI generation / utility:
- `baoyu-image-gen` - Image generation backend skill (referenced as a non-native backend option)

> The README states the repository contains **"20+ skills"** and organizes them into Content Skills, AI Generation Skills, and Utility Skills. The fetched README output was truncated before the full list; the skills above are those determinable verbatim from the fetched files. The remaining skills are not enumerated here to avoid fabrication.

### Artifact 1: `skills/baoyu-cover-image/SKILL.md` (verbatim excerpt)

```markdown
---
name: baoyu-cover-image
description: Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) combining 11 color palettes and 7 rendering styles. Supports cinematic (2.35:1), widescreen (16:9), and square (1:1) aspects. Use when user asks to "generate cover image", "create article cover", or "make cover".
version: 1.117.5
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-cover-image
---
# Cover Image Generator
Generate elegant cover images for articles with 5-dimensional customization.
## User Input Tools
When this skill prompts the user, follow this tool-selection rule (priority order):
1. **Prefer built-in user-input tools** exposed by the current agent runtime — e.g., `AskUserQuestion`, `request_user_input`, `clarify`, `ask_user`, or any equivalent.
2. **Fallback**: if no such tool exists, emit a numbered plain-text message and ask the user to reply with the chosen number/answer for each question.
3. **Batching**: if the tool supports multiple questions per call, combine all applicable questions into a single call; if only single-question, ask them one at a time in priority order.
Concrete `AskUserQuestion` references below are examples — substitute the local equivalent in other runtimes.
...
## Five Dimensions
| Dimension | Values | Default |
|-----------|--------|---------|
| **Type** | hero, conceptual, typography, metaphor, scene, minimal | auto |
| **Palette** | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro, duotone, macaron | auto |
| **Rendering** | flat-vector, hand-drawn, painterly, digital, pixel, chalk, screen-print | auto |
| **Text** | none, title-only, title-subtitle, text-rich | title-only |
| **Mood** | subtle, balanced, bold | balanced |
| **Font** | clean, handwritten, serif, display | clean |
...
## Workflow
### Progress Checklist
```
Cover Image Progress:
- [ ] Step 0: Check preferences (EXTEND.md) ⛔ BLOCKING
- [ ] Step 1: Analyze content + save refs + determine output dir
- [ ] Step 2: Confirm options (6 dimensions) ⚠️ unless --quick
- [ ] Step 3: Create prompt
- [ ] Step 4: Generate image
- [ ] Step 5: Completion report
```
...
### Step 0: Load Preferences ⛔ BLOCKING
Check EXTEND.md in priority order — the first one found wins:
| Priority | Path | Scope |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-cover-image/EXTEND.md` | Project |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-cover-image/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-cover-image/EXTEND.md` | User home |
```

The skill also defines an ordered **image-backend resolution** rule (current-request override → saved `preferred_image_backend` → auto-select runtime-native tool such as Codex `imagegen` / Cursor `GenerateImage` → ask the user), a **Confirmation Policy** ("confirm before generation"), an `Options` table, a `File Structure` layout, and a `Composition Principles` section.

### Artifact 2: `skills/baoyu-post-to-wechat/SKILL.md` (verbatim excerpt)

```markdown
---
name: baoyu-post-to-wechat
description: Posts content to WeChat Official Account (微信公众号) via API or Chrome CDP. Supports article posting (文章) with HTML, markdown, or plain text input, and image-text posting (贴图, formerly 图文) with multiple images. Markdown article workflows default to converting ordinary external links into bottom citations for WeChat-friendly output. Use when user mentions "发布公众号", "post to wechat", "微信公众号", or "贴图/图文/文章".
version: 1.118.2
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat
    requires:
      anyBins:
        - bun
        - npx
---
# Post to WeChat Official Account
...
## Language
Respond in the user's language. If they write in Chinese, reply in Chinese; if English, English. Keep technical tokens (paths, flags, field names) in English.
## Script Directory
`{baseDir}` = this SKILL.md's directory. Resolve `${BUN_X}`: prefer `bun`; else `npx -y bun`; else suggest `brew install oven-sh/bun/bun`.
| Script | Purpose |
|--------|---------|
| `scripts/wechat-browser.ts` | Image-text posts (图文) |
| `scripts/wechat-article.ts` | Article posting via browser (文章) |
| `scripts/wechat-api.ts` | Article posting via API (文章) |
| `scripts/md-to-wechat.ts` | Markdown → WeChat-ready HTML with image placeholders |
| `scripts/check-permissions.ts` | Verify environment & permissions |
...
## Article Posting Workflow (文章)
```
- [ ] Step 0: Load preferences (EXTEND.md)
- [ ] Step 0.5: Resolve account (multi-account only — see references/multi-account.md)
- [ ] Step 1: Determine input type
- [ ] Step 2: Select method and configure credentials
- [ ] Step 3: Resolve theme/color and validate metadata
- [ ] Step 4: Publish to WeChat
- [ ] Step 5: Report completion
```
...
## Feature Comparison
| Feature | Image-Text | Article (API) | Article (Remote API) | Article (Browser) |
|---------|:---:|:---:|:---:|:---:|
| Plain text input | ✗ | ✓ | ✓ | ✓ |
| HTML input | ✗ | ✓ | ✓ | ✓ |
| Markdown input | Title/content | ✓ | ✓ | ✓ |
| Multiple images | ✓ (up to 9) | ✓ (inline) | ✓ (inline) | ✓ (inline) |
| Themes | ✗ | ✓ | ✓ | ✓ |
| Requires Chrome | ✓ | ✗ | ✗ | ✓ |
| Requires API credentials | ✗ | ✓ | ✓ | ✗ |
| Speed | Medium | Fast | Fast | Slow |
```

Note: this skill directory ships TypeScript `scripts/*.ts` alongside `SKILL.md`. The scripts are implementation helpers invoked by the instructions; the behavioral "brain" remains the Markdown file.

---

## Evaluation Dimensions (file-based artifacts specific)

### 1. Slot-Based Skill Organization
- [ ] One skill per directory, each with a single `SKILL.md` entry point
- [ ] Co-located `scripts/` and `references/` next to the skill
- [ ] Naming convention consistent (`baoyu-<name>/`)

### 2. Markdown Structure & Frontmatter
- [ ] Valid YAML frontmatter (`name`, `description`, `version`, `metadata`)
- [ ] `description` carries trigger phrases in the user's language(s)
- [ ] Clear heading hierarchy and tabular option references

### 3. Runtime Portability
- [ ] Tool-selection rules abstract over runtimes (Claude Code / Codex / Cursor)
- [ ] Backend resolution is explicit and ordered
- [ ] Preference files (`EXTEND.md`) with a documented priority chain

### 4. Safety & Confirmation Policies
- [ ] Destructive/expensive actions (image generation, publishing) require confirmation by default
- [ ] No silent substitution (e.g. raster images must not be replaced with SVG/HTML)
- [ ] Credentials handled outside the skill file (`.env`, `EXTEND.md`), never inlined

### 5. Composition & Extensibility
- [ ] Skills chain cleanly (cover → illustrator → post-to-wechat)
- [ ] New skills can be added as standalone directories
- [ ] Bulk-install is discouraged to protect agent context

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Slot-Based Skill Organization | 20% | | |
| Markdown Structure & Frontmatter | 20% | | |
| Runtime Portability | 20% | | |
| Safety & Confirmation Policies | 20% | | |
| Composition & Extensibility | 20% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. **Frontmatter validation**: confirm each `SKILL.md` has `name` and `description`, and that `metadata.openclaw.homepage` resolves to the correct anchor.
2. **Directory layout**: verify each skill directory bundles its own `scripts/` / `references/` and does not depend on files outside itself.
3. **Preference resolution**: place `EXTEND.md` at project, XDG, and user-home scopes and confirm the priority chain wins in order.

### Behavioral Tests
1. **Backend resolution**: run `baoyu-cover-image` in a runtime with a native image tool and in one without, and confirm the skill selects the correct backend or asks the user.
2. **Confirmation gate**: invoke without `--quick` and confirm generation waits for confirmation; then invoke with `--quick` and confirm it proceeds.
3. **Publish method selection**: for `baoyu-post-to-wechat`, verify API vs browser vs remote-api selection and that markdown is not pre-converted.

### Output Tests
1. **Composability**: chain cover-image → article-illustrator → post-to-wechat and confirm artifacts flow through.
2. **Citation default**: confirm ordinary external links in Markdown input become bottom citations unless `--no-cite`.
3. **Multi-account**: with 2+ `accounts:` entries, confirm the account-selection step appears.

---

## Notes

- The repository is **MIT**; note that skills published individually to ClawHub are released under **MIT-0** per ClawHub registry rules, as stated in the README.
- This is a **file-based, non-coding content Agent suite** for creators/publishers: the value is in visual-asset generation and Chinese-platform publishing.
- Skills intentionally **co-locate helper scripts** with `SKILL.md`; this differs from pure-prose suites such as TC-055 / TC-056, and is worth noting when assessing "logical artifact" purity.
- **Coverage caveat**: the fetched README was truncated, so the skill list above is limited to what was determinable from the fetched files. The README states the repo contains "20+ skills"; the remaining skills are not enumerated here to avoid fabrication.
- All quoted content was fetched from raw GitHub URLs on branch `main`.
