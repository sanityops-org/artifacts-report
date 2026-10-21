# TC-055: AI Marketing Suite - File-Based Multi-Logical-Artifact Agent Suite

## Metadata
- **Source Project**: zubair-trabzada/ai-marketing-claude
- **GitHub**: github.com/zubair-trabzada/ai-marketing-claude
- **License**: MIT
- **Artifact Type**: File-based logical artifacts (Markdown `SKILL.md` suite)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub fetch, branch `HEAD` (default branch):
  - `https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/HEAD/market/SKILL.md`
  - `https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/HEAD/skills/market-copy/SKILL.md`
  - `https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/HEAD/README.md`

---

## Project Overview

The AI Marketing Suite is a **non-coding, content/marketing Agent** packaged entirely as a suite of Markdown `SKILL.md` files for Claude Code. It turns a generic coding agent into a marketing analyst, copywriter, and strategist that audits websites, generates copy, builds email sequences, produces content calendars, analyzes competitors, and emits client-ready reports — all driven from the command line via `/market <command>`.

### Key Features
- **Markdown as the brain**: every capability is a `SKILL.md` file; changing agent behavior is a plain-text edit, not a code change.
- **One orchestrator + 14 sub-skills**: `market/SKILL.md` routes `/market ...` commands to a matching `skills/market-*/SKILL.md`.
- **Parallel subagents**: `/market audit` launches 5 subagents defined as Markdown files in `agents/market-*.md`.
- **Content artifacts, not programs**: outputs are Markdown reports (e.g. `MARKETING-AUDIT.md`, `COPY-SUGGESTIONS.md`), plus an optional PDF.
- **Domain**: marketing copywriting, funnel/conversion analysis, SEO, competitive intelligence, product launch, brand voice. Non-code.

### Architecture (from the project README)

```text
ai-marketing-claude/
├── market/SKILL.md                     # Main orchestrator (routes all /market commands)
│
├── skills/                             # 14 sub-skills
│   ├── market-audit/SKILL.md           # Full audit orchestration
│   ├── market-copy/SKILL.md            # Copywriting analysis & generation
│   ├── market-emails/SKILL.md          # Email sequence generation
│   ├── market-social/SKILL.md          # Social media content calendar
│   ├── market-ads/SKILL.md             # Ad creative & copy
│   ├── market-funnel/SKILL.md          # Funnel analysis & optimization
│   ├── market-competitors/SKILL.md     # Competitive intelligence
│   ├── market-landing/SKILL.md         # Landing page CRO
│   ├── market-launch/SKILL.md          # Launch playbook generation
│   ├── market-proposal/SKILL.md        # Client proposal generator
│   ├── market-report/SKILL.md          # Marketing report (Markdown)
│   ├── market-report-pdf/SKILL.md      # Marketing report (PDF)
│   ├── market-seo/SKILL.md             # SEO content audit
│   └── market-brand/SKILL.md           # Brand voice analysis
│
├── agents/                             # 5 parallel subagents
│   ├── market-content.md               # Content & messaging analysis
│   ├── market-conversion.md            # CRO & funnel optimization
│   ├── market-competitive.md           # Competitive positioning
│   ├── market-technical.md             # Technical SEO & tracking
│   └── market-strategy.md              # Brand, pricing & growth strategy
│
├── scripts/                            # Python utility scripts
│   ├── analyze_page.py                 # Webpage marketing analysis
│   ├── competitor_scanner.py           # Competitor website scanner
│   ├── social_calendar.py              # Social content calendar generator
│   └── generate_pdf_report.py          # PDF report generator
│
├── templates/                          # Marketing templates
│   ├── email-welcome.md                # Welcome email sequence (5 emails)
│   ├── email-nurture.md                # Lead nurture sequence (6 emails)
│   ├── email-launch.md                 # Product launch sequence (8 emails)
│   ├── proposal-template.md            # Client proposal template
│   ├── content-calendar.md             # 30-day content calendar
│   └── launch-checklist.md             # Launch checklist
│
├── install.sh
├── uninstall.sh
├── requirements.txt
└── LICENSE                             # MIT License
```

---

## Logical Artifact Inventory

### Skill Inventory (user-facing `/market` commands)

| Skill file | Command | Purpose |
|-----------|---------|---------|
| `market/SKILL.md` | (orchestrator) | Routes all `/market` commands to sub-skills |
| `skills/market-audit/SKILL.md` | `/market audit <url>` | Full audit via 5 parallel subagents |
| `skills/market-copy/SKILL.md` | `/market copy <url>` | Copywriting analysis & generation |
| `skills/market-emails/SKILL.md` | `/market emails <topic>` | Email sequence generation |
| `skills/market-social/SKILL.md` | `/market social <topic>` | Social media content calendar |
| `skills/market-ads/SKILL.md` | `/market ads <url>` | Ad creative & copy |
| `skills/market-funnel/SKILL.md` | `/market funnel <url>` | Funnel analysis & optimization |
| `skills/market-competitors/SKILL.md` | `/market competitors <url>` | Competitive intelligence |
| `skills/market-landing/SKILL.md` | `/market landing <url>` | Landing page CRO |
| `skills/market-launch/SKILL.md` | `/market launch <product>` | Launch playbook generation |
| `skills/market-proposal/SKILL.md` | `/market proposal <client>` | Client proposal generator |
| `skills/market-report/SKILL.md` | `/market report <url>` | Marketing report (Markdown) |
| `skills/market-report-pdf/SKILL.md` | `/market report-pdf <url>` | Marketing report (PDF) |
| `skills/market-seo/SKILL.md` | `/market seo <url>` | SEO content audit |
| `skills/market-brand/SKILL.md` | `/market brand <url>` | Brand voice analysis & guidelines |

### Artifact 1: `market/SKILL.md` - Main Orchestrator (verbatim)

```markdown
# AI Marketing Suite — Main Orchestrator
You are a comprehensive AI marketing analysis and content generation system for Claude Code. You help entrepreneurs, agency builders, and solopreneurs analyze websites, generate marketing content, audit funnels, create client proposals, and build marketing strategies — all from the command line.
## Command Reference
| Command | Description | Output |
|---------|-------------|--------|
| `/market audit <url>` | Full marketing audit (parallel subagents) | MARKETING-AUDIT.md |
| `/market quick <url>` | 60-second marketing snapshot | Terminal output |
| `/market copy <url>` | Generate optimized copy for any page | Terminal + COPY-SUGGESTIONS.md |
| `/market emails <topic/url>` | Generate email sequences | EMAIL-SEQUENCES.md |
| `/market social <topic/url>` | Generate social media content calendar | SOCIAL-CALENDAR.md |
| `/market ads <url>` | Generate ad creative and copy | AD-CAMPAIGNS.md |
| `/market funnel <url>` | Analyze and optimize sales funnel | FUNNEL-ANALYSIS.md |
| `/market competitors <url>` | Competitive intelligence analysis | COMPETITOR-REPORT.md |
| `/market landing <url>` | Landing page CRO analysis | LANDING-CRO.md |
| `/market launch <product>` | Generate launch playbook | LAUNCH-PLAYBOOK.md |
| `/market proposal <client>` | Generate client proposal | CLIENT-PROPOSAL.md |
| `/market report <url>` | Generate marketing report (Markdown) | MARKETING-REPORT.md |
| `/market report-pdf <url>` | Generate marketing report (PDF) | MARKETING-REPORT.pdf |
| `/market seo <url>` | SEO content audit | SEO-AUDIT.md |
| `/market brand <url>` | Brand voice analysis and guidelines | BRAND-VOICE.md |
## Routing Logic
When the user invokes `/market <command>`, route to the appropriate sub-skill:
### Full Marketing Audit (`/market audit <url>`)
This is the flagship command. It launches **5 parallel subagents** to analyze the website simultaneously:
1. **market-content** agent → Content quality, messaging, copy effectiveness
2. **market-conversion** agent → CRO, funnels, landing pages, signup flows
3. **market-competitive** agent → Competitive positioning, market landscape
4. **market-technical** agent → Technical SEO, site architecture, page speed
5. **market-strategy** agent → Overall strategy, pricing, growth opportunities
**Scoring Methodology (Marketing Score 0-100):**
| Category | Weight | What It Measures |
|----------|--------|------------------|
| Content & Messaging | 25% | Copy quality, value props, clarity, persuasion |
| Conversion Optimization | 20% | CTAs, forms, friction, social proof, urgency |
| SEO & Discoverability | 20% | On-page SEO, technical SEO, content structure |
| Competitive Positioning | 15% | Differentiation, market awareness, alternatives pages |
| Brand & Trust | 10% | Brand consistency, trust signals, social proof |
| Growth & Strategy | 10% | Pricing, referral, retention, expansion opportunities |
**Composite Marketing Score** = Weighted average of all 6 categories
### Quick Snapshot (`/market quick <url>`)
Fast 60-second assessment. Do NOT launch subagents. Instead:
1. Fetch the homepage using WebFetch
2. Evaluate: headline clarity, CTA strength, value proposition, trust signals, mobile readiness
3. Output a quick scorecard with top 3 wins and top 3 fixes
4. Keep output under 30 lines
### Individual Commands
For all other commands (`/market copy`, `/market emails`, etc.), route to the corresponding sub-skill in `skills/market-<command>/SKILL.md`.
## Business Context Detection
Before running any analysis, detect the business type:
- **SaaS/Software** → Focus on: trial-to-paid conversion, onboarding, feature pages, pricing tiers
- **E-commerce** → Focus on: product pages, cart abandonment, upsells, reviews
- **Agency/Services** → Focus on: case studies, portfolio, contact forms, trust signals
- **Local Business** → Focus on: Google Business Profile, local SEO, reviews, directions
- **Creator/Course** → Focus on: lead magnets, email capture, testimonials, community
- **Marketplace** → Focus on: two-sided messaging, supply/demand balance, trust mechanisms
## Output Standards
All outputs must follow these rules:
1. **Actionable over theoretical** — Every recommendation must be specific enough to implement
2. **Prioritized** — Always rank by impact (High/Medium/Low)
3. **Revenue-focused** — Connect every suggestion to business outcomes
4. **Example-driven** — Include before/after copy examples, not just advice
5. **Client-ready** — Reports should be presentable to clients without editing
## File Output
Save detailed outputs to markdown files in the current directory:
- Use descriptive filenames: `MARKETING-AUDIT.md`, `COMPETITOR-REPORT.md`, etc.
- Include the URL, date, and overall score at the top
- Structure with clear headers and tables
- Include an executive summary for client-facing reports
## Cross-Skill References
Many skills work together:
- `/market audit` calls all subagents → produces comprehensive analysis
- `/market proposal` can reference audit results if available
- `/market report` and `/market report-pdf` compile all available analysis data
- `/market copy` benefits from `/market brand` voice guidelines if run first
- `/market emails` uses insights from `/market funnel` analysis if available
```

### Artifact 2: `skills/market-copy/SKILL.md` - Copywriting Engine (verbatim excerpt)

```markdown
# Copywriting Analysis & Generation
You are the copywriting engine for `/market copy <url>`. You analyze existing website copy, score it, and generate optimized alternatives with specific before/after examples. Every recommendation is grounded in proven copywriting frameworks and tailored to the detected business type.
## When This Skill Is Invoked
The user runs `/market copy <url>`. Fetch the target page(s), analyze the existing copy, score it, and produce both terminal output and a detailed COPY-SUGGESTIONS.md file.
---
## Phase 1: Copy Discovery
### 1.1 Fetch and Parse
Use `WebFetch` to retrieve the target URL. Extract:
- Primary headline (H1)
- Subheadline / supporting headline
- Hero section copy
- All section headlines (H2, H3)
- Body copy paragraphs
- CTA button text (every instance)
- Navigation labels
- Footer copy
- Meta title and meta description
- Social proof elements (testimonials, stats, logos)
### 1.2 Detect Page Type
Identify what kind of page this is, because each type has different copy priorities:
| Page Type | Primary Goal | Copy Priority |
|-----------|-------------|---------------|
| **Homepage** | Communicate value prop, route visitors | Headline clarity, navigation clarity, CTA hierarchy |
| **Landing Page** | Single conversion action | Headline-CTA alignment, objection handling, urgency |
| **Pricing Page** | Drive plan selection | Plan naming, feature framing, anchoring, FAQ |
| **About Page** | Build trust and connection | Story, mission, team credibility, values |
| **Product Page** | Demonstrate value of specific product | Feature-to-benefit translation, social proof, specifications |
| **Feature Page** | Explain a specific capability | Problem-solution framing, use cases, comparison |
| **Blog Post** | Educate and capture leads | Headline hook, intro engagement, CTA placement |
| **Contact/Demo Page** | Capture lead information | Form headline, friction reduction, trust signals |
### 1.3 Voice and Tone Analysis
Before generating new copy, analyze the existing voice:
**Voice Dimensions to Assess:**
- **Formality:** Casual ←→ Formal (1-5 scale)
- **Emotion:** Neutral ←→ Passionate (1-5 scale)
- **Complexity:** Simple ←→ Technical (1-5 scale)
- **Humor:** Serious ←→ Playful (1-5 scale)
- **Authority:** Peer ←→ Expert (1-5 scale)
Document this voice profile so all generated copy matches the brand's existing tone, unless the existing tone is clearly ineffective.
```

The skill then continues through **Phase 2: Copy Analysis** (headline scoring, PAS / AIDA / Before-After-Bridge / 4U frameworks, a 5-dimension 0-10 copy scoring rubric totaling X/50, and a Value Proposition Canvas), **Phase 3: Copy Generation** (per-page-type copy structures, CTA optimization, at least 5 before/after pairs, and a swipe file), a structured **Output Format** (terminal summary + `COPY-SUGGESTIONS.md`), and **Cross-Skill Integration** (reading `BRAND-VOICE.md`, `MARKETING-AUDIT.md`, and `COMPETITOR-REPORT.md`).

---

## Evaluation Dimensions (file-based artifacts specific)

### 1. Orchestration Clarity
- [ ] Single orchestrator (`market/SKILL.md`) clearly owns all routing
- [ ] Every `/market` command maps to exactly one sub-skill
- [ ] Score weights and output filenames are declared centrally

### 2. Markdown Structure & Prompt Craft
- [ ] Consistent heading hierarchy across all `SKILL.md` files
- [ ] Tabular command/score references rather than prose
- [ ] Explicit, executable instructions (phases, checklists) instead of vague advice

### 3. Skill Granularity & Separation of Concerns
- [ ] Each sub-skill owns one job (copy, emails, social, ads, funnel, ...)
- [ ] Cross-skill references are declared (e.g. copy reads brand voice)
- [ ] Subagents (5) are separated from sub-skills (14)

### 4. Output Contract
- [ ] Every skill declares a deterministic output file and format
- [ ] Client-ready standards are stated (prioritized, example-driven, executive summary)
- [ ] Optional PDF path is isolated from Markdown path

### 5. Auditability & Extensibility
- [ ] All logical artifacts are plain Markdown, diffable and reviewable in git
- [ ] New marketing skills can be added by copying a `SKILL.md` template
- [ ] No behavior is hidden in un-inspected code

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Orchestration Clarity | 20% | | |
| Markdown Structure & Prompt Craft | 20% | | |
| Skill Granularity & Separation of Concerns | 20% | | |
| Output Contract | 20% | | |
| Auditability & Extensibility | 20% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. **Routing coverage**: verify each `/market` command in the orchestrator resolves to an existing `skills/market-*/SKILL.md`.
2. **Frontmatter/inventory parity**: confirm the 14 sub-skills and 5 agents listed in the README all exist as files.
3. **Output-name consistency**: check that declared output filenames match the orchestrator table.

### Behavioral Tests
1. **Business-context detection**: feed a SaaS, e-commerce, and local-business URL and confirm the agent selects the right focus areas.
2. **Scoring reproducibility**: run `/market audit` twice on the same URL and compare category scores for drift.
3. **Sub-agent parallelism**: verify `/market audit` actually dispatches 5 distinct subagents rather than collapsing into one pass.

### Output Tests
1. **Artifact generation**: confirm `/market copy` writes `COPY-SUGGESTIONS.md` containing at least 5 before/after pairs and a swipe file.
2. **Client-readiness**: verify generated reports are presentable without manual editing (executive summary present).
3. **Cross-skill wiring**: run `/market brand` before `/market copy` and confirm voice guidelines influence generated copy.

---

## Notes

- The **MIT license** permits full quotation and modification of these Markdown artifacts.
- This is a representative **file-based, non-coding marketing Agent**: the "intelligence" lives entirely in `SKILL.md` prose, not in application logic.
- The suite intentionally pairs **user-facing sub-skills** (14) with **parallel subagents** (5) — a two-layer logical-artifact design worth contrasting with single-file agents.
- Suitable as an evaluation baseline for **non-technical marketers** who want to inspect and edit an agent's behavior without programming.
- All content in this case was fetched from raw GitHub URLs on branch `HEAD`; no artifact content is inferred or fabricated.
