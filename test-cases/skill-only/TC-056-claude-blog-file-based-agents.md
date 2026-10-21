# TC-056: claude-blog - File-Based Multi-Logical-Artifact Agent Suite

## Metadata
- **Source Project**: AgriciDaniel/claude-blog
- **GitHub**: github.com/AgriciDaniel/claude-blog
- **License**: MIT
- **Artifact Type**: File-based logical artifacts (Markdown `SKILL.md` suite; 1 orchestrator + 31 sub-skills)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub fetch, branch `main`:
  - `https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/skills/blog-write/SKILL.md`
  - `https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/skills/blog/SKILL.md`
  - `https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/README.md`

---

## Project Overview

claude-blog is a **full-lifecycle, non-coding content Agent** delivered as a Claude Code skill suite. Every capability — writing, rewriting, analysis, outlines, audits, schema, charts, images, repurposing, AI-citation SEO, topic clusters, multilingual publishing, and content-decay detection — is a Markdown `SKILL.md` file. No application logic defines behavior; the prose does.

The suite advertises **32 skill directories = 1 orchestrator (`skills/blog`) + 31 sub-skills**, 5 specialized agents, 22 references, and 12 content templates. It targets blog/marketing content production, not software development.

### Key Features
- **One orchestrator + 31 sub-skills**: `skills/blog/SKILL.md` parses `/blog` input, detects the platform, and routes to a `skills/blog-*/SKILL.md`.
- **Reference-driven**: 22 on-demand reference files (loaded only as needed) hold the detailed methodology.
- **Code-enforced quality gate**: a 5-gate Blog Delivery Contract scores drafts against a 100-point rubric and blocks delivery below 90.
- **Dual optimization**: written for Google rankings and for AI-assistant citation (ChatGPT, Perplexity, AI Overviews, Gemini).
- **Domain**: content writing, SEO, editorial quality, localization. Non-code.

### Version / Shape (from the README)
> Current v2.2.0 shape: **32 skill directories = 1 orchestrator + 31 sub-skills; 30 user-facing /blog commands (`blog-chart` is internal, not a command).** It also includes 5 specialized agents, repository consistency and public-release validators, 22 core references, 12 templates, a 250+ test suite, and the bundled Claude Blog Brain at `./brain`.

---

## Logical Artifact Inventory

### Skill Inventory (routing table, verbatim from README / orchestrator)

| Command | Sub-skill | What it does |
|---------|-----------|--------------|
| `/blog write <topic>` | `blog-write` | Write a new blog post from scratch |
| `/blog rewrite <file>` | `blog-rewrite` | Rewrite/optimize an existing blog post |
| `/blog analyze <file-or-url>` | `blog-analyze` | Audit blog quality with 0-100 score |
| `/blog brief <topic>` | `blog-brief` | Generate a detailed content brief |
| `/blog calendar` | `blog-calendar` | Generate an editorial calendar |
| `/blog strategy <niche>` | `blog-strategy` | Blog strategy and topic ideation |
| `/blog outline <topic>` | `blog-outline` | Generate SERP-informed content outline |
| `/blog seo-check <file>` | `blog-seo-check` | Post-writing SEO validation checklist |
| `/blog schema <file>` | `blog-schema` | Generate JSON-LD schema markup |
| `/blog repurpose <file>` | `blog-repurpose` | Repurpose content for other platforms |
| `/blog geo <file>` | `blog-geo` | AI citation readiness audit |
| `/blog audit [directory]` | `blog-audit` | Full-site blog health assessment |
| `/blog cannibalization [dir]` | `blog-cannibalization` | Detect keyword cannibalization across posts |
| `/blog factcheck <file>` | `blog-factcheck` | Verify statistics against cited sources |
| `/blog image [generate\|edit\|setup]` | `blog-image` | AI image generation and editing via Gemini |
| `/blog persona [...]` | `blog-persona` | Manage writing personas and voice profiles |
| `/blog brand [...]` | `blog-brand` | Generate BRAND.md + VOICE.md context files |
| `/blog discourse <topic>` | `blog-discourse` | Last-30-days API-free discourse research → DISCOURSE.md |
| `/blog taxonomy [...]` | `blog-taxonomy` | Tag/category management across CMS platforms |
| `/blog notebooklm <question>` | `blog-notebooklm` | Query NotebookLM for source-grounded research |
| `/blog audio [...]` | `blog-audio` | Generate audio narration of blog posts |
| `/blog google [command]` | `blog-google` | Google API data: PSI, CrUX, GSC, GA4, NLP, YouTube, Keywords |
| `/blog update <file>` | `blog-rewrite` (freshness alias) | Update existing post with fresh stats |
| `/blog cluster [...]` | `blog-cluster` | Semantic topic-cluster planning + execution |
| `/blog multilingual <topic>` | `blog-multilingual` | Write + translate + localize + emit hreflang |
| `/blog translate <file>` | `blog-translate` | SEO-optimized translation with format preservation |
| `/blog localize <file> --locale` | `blog-localize` | Cultural deep-adaptation (DACH, FR, ES, JA, custom) |
| `/blog locale-audit <directory>` | `blog-locale-audit` | Multilingual content QA |
| `/blog flow [...]` | `blog-flow` | FLOW framework prompts (evidence-led) |
| `/blog style learn <paths>` | `blog-style` | Learn author voice profile from 5-10 posts |
| `/blog decay <current> <previous>` | `blog-decay` | Detect 20%+ QoQ content decay from GSC exports |
| (internal, not a command) | `blog-chart` | Built-in SVG chart generation |

### Agents (from the orchestrator)

| Agent | Role |
|-------|------|
| `blog-researcher` | Research specialist: finds statistics, sources, images, competitive data |
| `blog-writer` | Content generation specialist: writes optimized blog content |
| `blog-seo` | SEO validation specialist: checks on-page SEO post-writing |
| `blog-reviewer` | Quality assessment: runs the 100-point internal editorial-readiness heuristic |
| `blog-translator` | Multilingual translation specialist; format preservation across markdown/MDX/HTML/frontmatter/schema |

### Artifact 1: `skills/blog/SKILL.md` - Orchestrator (verbatim excerpt)

```markdown
---
name: blog
description: >
  Full-lifecycle blog engine with 31 sub-skills, 12 templates, 100-point scoring,
  and 5 agents. Routes requests to the right sub-skill: writing, rewriting,
  analysis, outlines, audits, schema, charts, images, repurposing, AI citation
  SEO, FLOW prompts, topic clusters, and multilingual publishing. Optimized for
  Google rankings, E-E-A-T, and AI citations. Supports any platform. Use when
  user says "blog", "blog post", "blog audit", "topic cluster",
  "multilingual blog", or any /blog subcommand.
license: MIT
compatibility: Requires Claude Code and Python 3.11+ for quality scoring
metadata:
  author: AgriciDaniel
  version: "2.2.0"
user-invokable: true
argument-hint: "[write|rewrite|analyze|brief|calendar|cannibalization|strategy|outline|seo-check|schema|repurpose|geo|image|audit|factcheck|persona|brand|discourse|taxonomy|notebooklm|audio|google|update|cluster|multilingual|translate|localize|locale-audit|flow|style|decay] [topic-or-file]"
---
# Blog: Content Engine for Rankings & AI Citations
Full-lifecycle blog management: strategy, briefs, outlines, writing, analysis,
optimization, schema generation, repurposing, and editorial planning. Dual-optimized
for Google's May 2026 Core Update, March 2026 core quality baseline, March and
June 2026 spam enforcement, and AI citation platforms (ChatGPT, Perplexity,
Google AI Overviews, Gemini). Google treats gen-AI optimization as SEO, not a
separate discipline.
...
## Core Methodology: The 6 Pillars
Every blog post targets these 6 optimization pillars:
| Pillar | Impact | Implementation |
|--------|--------|---------------|
| Purpose-First Clarity | Reader and retrieval utility | Important sections state their point clearly; no prescribed heading form or passage length |
| Real Sourced Data | E-E-A-T trust | Tier 1-3 sources only, inline attribution |
| Visual Media | Engagement + citations | Pixabay/Unsplash images + AI generation via Gemini + built-in SVG charts + YouTube video embeds |
| Optional Q&A | Reader utility only | Use visible Q&A when it answers real user needs; FAQPage earns no Google rich-result or readiness points |
| Content Structure | Comprehension and reuse | Proper heading hierarchy, stable entities, useful tables/lists only where they fit |
| Substantive Maintenance | Accuracy over date churn | Update content and dateModified only when facts, methods, or recommendations materially change |
...
## Quality Gates
These are hard rules. Never ship content that violates them:
| Rule | Threshold | Action |
|------|-----------|--------|
| Fabricated statistics | Zero tolerance | Source material factual statistics, measurements, and public-data claims. ... |
| Paragraph pacing | Fit the audience and material | Split only when comprehension improves |
| Heading hierarchy | Never skip levels | H1 → H2 → H3 only |
| Source tier | Tier 1-3 only | Never cite content mills or affiliate sites |
| Image alt text | Required on all images | Descriptive, includes topic keywords naturally |
| Self-promotion | Max 1 brand mention | Author bio context only |
| Chart diversity | No duplicate types | Each chart must be a different type |
| Delivery contract (v1.9.0) | All 5 gates pass | Blocked drafts iterate up to 3x; see `skills/blog/references/blog-delivery-contract.md` |
## Scoring Methodology
Score with `skills/blog/references/quality-scoring.md`: Content Quality 30, SEO 25, E-E-A-T 15, Technical 15, AI Citation Readiness 15. Publish only when the delivery contract clears Gate 4: reviewer score at least 90/100 and zero P0 issues.
```

Key structural facts from the orchestrator body: it defines a **Command Routing** table, **Platform Detection** (`.mdx`→Next.js, `hugo.toml`→Hugo, `_config.yml`→Jekyll, `wp-content/`→WordPress, Ghost, Astro, 11ty, Gatsby), and an **Execution Flow** for `/blog write` (Parse → Research → Outline → Write → Optimize → Score → Delivery Contract Enforcement). See also the README's **5-Gate Delivery Contract**: (1) Capability Discovery, (2) Format Completeness, (3) Visual Verification, (4) Content Review, (5) Asset and Link Integrity.

### Artifact 2: `skills/blog-write/SKILL.md` - New Article Generation (verbatim excerpt)

```markdown
---
name: blog-write
description: >
  Write new blog articles from scratch optimized for Google rankings and AI
  citations. Generates full articles with template selection, answer-first
  formatting, Key Takeaways summary box, information gain markers, evidence-backed explanations, sourced
  statistics, Pixabay/Unsplash images, built-in SVG chart generation, optional FAQ sections,
  internal linking zones, and proper heading hierarchy. Supports MDX, markdown,
  and HTML output.
  Use when user says "write blog", "new blog post", "create article",
  "write about", "draft blog", "generate blog post".
user-invokable: true
argument-hint: "<topic>"
license: MIT
---
# Blog Writer: New Article Generation
Writes complete blog articles from a topic, brief, or outline. Every article
follows the 6 pillars of dual optimization (Google rankings + AI citations).
**Key references** (paths relative to repo root; references live in the
main `blog` skill's references directory, not in `blog-write/`):
- `skills/blog/references/synthesis-contract.md`: 6 LAWs for synthesis output ...
- `skills/blog/references/content-templates.md`: Template selection guide and usage
- `skills/blog/references/quality-scoring.md`: 5-category scoring (Content 30, SEO 25, E-E-A-T 15, Technical 15, AI Citation 15)
- `skills/blog/references/eeat-signals.md`: Experience, expertise, authority, trust markers
- `skills/blog/references/internal-linking.md`: Linking strategy and anchor text rules
- `skills/blog/references/visual-media.md`: Image sourcing and chart styling
- `skills/blog-write/references/delivery.md`: delivery contract steps and summary template for this sub-skill
## Workflow
### Phase 0: Surface Targeting (do this BEFORE research)
Decide which of the FLOW 5 surfaces this post is meant to win. The choice
shapes structure, length, citation density, and call-to-action. The 5 surfaces
in 2026:
1. Owned site (organic Google ranking)
2. SERP including AI Overviews
3. AI assistant citations (ChatGPT, Perplexity, Claude, Gemini, Copilot, You.com)
4. Local pack (out of scope for blog content; use claude-seo for local)
5. Communities and video (Reddit, YouTube, LinkedIn, Quora, niche forums)
...
### Phase 1.5: Template Selection
Select the appropriate content template from the 12 templates in
`skills/blog/templates/` (the main `blog` skill owns the templates directory).
1. **Auto-detect content type** from the topic and search intent:
   | Signal | Template |
   |--------|----------|
   | "How to...", process, steps | `how-to-guide` |
   | "Best X", "Top N", list format | `listicle` |
   | Client result, before/after, metrics | `case-study` |
   | "X vs Y", comparison, alternatives | `comparison` |
   | Broad topic, comprehensive guide | `pillar-page` |
   | "Is X worth it", product evaluation | `product-review` |
   | Opinion, prediction, industry take | `thought-leadership` |
   | Expert quotes, multi-source collection | `roundup` |
   | Code walkthrough, tool demo, technical | `tutorial` |
   | Breaking news, algorithm update, event | `news-analysis` |
   | Survey results, experiment, original data | `data-research` |
   | Q&A, knowledge base, "What is X" | `faq-knowledge` |
...
### Phase 5: Content Writing
... (5a Frontmatter, 5b Summary Box / Key Takeaways, 5c Purpose-First Formatting,
5d Information Gain Markers `[ORIGINAL DATA]` / `[PERSONAL EXPERIENCE]` / `[UNIQUE INSIGHT]`,
5e Evidence-Backed Explanations, 5f Internal Linking Zones `[INTERNAL-LINK: anchor text → target description]`)
```

The sub-skill continues through chart generation, media sourcing, and delivery. The main `blog` skill owns shared `references/` and `templates/`; sub-skills reference rather than duplicate them.

---

## Evaluation Dimensions (file-based artifacts specific)

### 1. Orchestrator / Sub-skill Architecture
- [ ] A single orchestrator owns routing and platform detection
- [ ] Each sub-skill is a self-contained Markdown file with a clear single job
- [ ] Shared assets (references, templates) are owned by one skill and referenced, not copied

### 2. Markdown Structure & Prompt Craft
- [ ] Consistent YAML frontmatter (`name`, `description`, `license`, `user-invokable`, `argument-hint`)
- [ ] Phased workflows (Phase 0..N) with explicit steps
- [ ] Deterministic routing/format tables instead of ambiguous prose

### 3. Reference-Discipline (Context Economy)
- [ ] Heavy detail lives in `references/*.md`, loaded only when needed
- [ ] Sub-skills point to canonical reference paths
- [ ] Number of references (22) and templates (12) is declared and consistent

### 4. Quality-Gate Encoding
- [ ] Hard rules (quality gates) are stated as non-negotiable
- [ ] A numeric rubric (100 points) and delivery thresholds (≥90) are explicit
- [ ] The "never the first reviewer" contract is expressed as file-enforced gates

### 5. Auditability & Extensibility
- [ ] All logic is plain Markdown, reviewable/diffable in git
- [ ] New sub-skills or templates can be added by adding files
- [ ] Behavior is inspectable without reading un-declared code

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Orchestrator / Sub-skill Architecture | 25% | | |
| Markdown Structure & Prompt Craft | 20% | | |
| Reference-Discipline (Context Economy) | 20% | | |
| Quality-Gate Encoding | 20% | | |
| Auditability & Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. **Routing coverage**: confirm all 30 user-facing `/blog` commands route to existing sub-skill directories, and that `blog-chart` is marked internal-only.
2. **Count parity**: verify the declared shape (1 orchestrator + 31 sub-skills, 5 agents, 22 references, 12 templates) matches the files on disk.
3. **Frontmatter validation**: check every `SKILL.md` has `name` and `description`.

### Behavioral Tests
1. **Platform detection**: feed `.mdx`, `hugo.toml`, and `wp-content/` projects and confirm the correct output format.
2. **Template selection**: give topics matching each of the 12 signals and verify the right template is chosen.
3. **Gate enforcement**: produce a draft scoring below 90 and confirm delivery is blocked and iterated.

### Output Tests
1. **Deterministic artifacts**: confirm `/blog write` emits `.md`, rendered `.html`, `.pdf`, a real hero image, and `preflight-report.json`.
2. **No fabricated statistics**: verify unverifiable numbers are dropped rather than softened.
3. **Cross-skill context**: confirm `BRAND.md` / `VOICE.md` from `/blog brand` are auto-loaded by `blog-write`.

---

## Notes

- The **MIT license** permits full quotation and modification of these Markdown artifacts.
- This is a large, production-grade **file-based, non-coding content Agent**: 32 skill directories of pure Markdown plus references and templates.
- The **5-gate delivery contract** is the distinguishing logical-artifact feature: quality is encoded as explicit, file-declared gates rather than implicit prompt behavior.
- The suite is a good reference for how a "one orchestrator → many sub-skills → shared references" topology is expressed entirely in Markdown.
- All quoted content was fetched from raw GitHub URLs on branch `main`; content beyond the quoted excerpts is summarized (not fabricated) from the same fetched files.
