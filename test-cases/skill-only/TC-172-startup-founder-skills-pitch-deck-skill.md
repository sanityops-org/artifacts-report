# TC-172: shawnpang/startup-founder-skills (Pitch Deck) - Skill Evaluation Case

## Metadata
- **Source Project**: shawnpang/startup-founder-skills
- **License**: MIT (LICENSE file present at repo root)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/shawnpang/startup-founder-skills/main/skills/pitch-deck/SKILL.md (default branch `main`). Repository README: https://raw.githubusercontent.com/shawnpang/startup-founder-skills/main/README.md . License file: https://raw.githubusercontent.com/shawnpang/startup-founder-skills/main/LICENSE

## Original Artifact Content

````markdown
---
name: pitch-deck
description: When the user wants to create, review, or restructure a fundraising pitch deck for seed or Series A. Also activates when the user mentions "deck", "pitch", "investor presentation", or "slide structure".
related: [investor-research, data-room, fundraising-email]
reads: [startup-context]
---

# Pitch Deck

## When to Use

- The founder is preparing a pitch deck for a fundraising round (pre-seed through Series A).
- The founder has an existing deck and wants structural or narrative feedback.
- The founder asks what slides to include or how to tell their story to investors.

## Context Required

From `startup-context`: company one-liner, stage, product description, target customer, business model, traction metrics, team bios, fundraising history, and competitive landscape. If any of these are missing, prompt the founder before drafting slides.

From the user: target round size, target investor type (VC vs. angel), whether this is for a live pitch (fewer words, more visuals) or a send-ahead deck (more self-explanatory text).

## Workflow

1. **Read startup context** — Pull from `.agents/startup-context.md` to populate slide content. Flag any gaps.
2. **Determine deck type** — Ask if this is a live-pitch deck (visual-heavy, 30-40 words per slide max) or a send-ahead deck (can include more explanatory text, 60-80 words per slide).
3. **Draft the narrative arc** — Before writing any slides, outline the story: what is the world like today (problem), what changes with your product (solution), why now, why this team, and what you need to get there.
4. **Write slide-by-slide content** — Produce content for each of the 10-12 slides below. Each slide gets a title, key message, supporting points, and a suggested visual or data element.
5. **Review for investor lens** — Check every slide against the question an investor would ask at that point. Flag weak spots.
6. **Produce final output** — Deliver the deck outline as structured markdown. If the user wants a `.pptx`, chain to the Anthropic pptx skill after content is finalized.

## Output Format

Structured markdown with one H3 per slide. Each slide section contains:
- **Title**: The slide headline (concise, assertion-style, e.g., "Healthcare billing wastes $200B annually")
- **Key message**: The one thing the audience should remember from this slide
- **Content**: Bullet points or narrative text
- **Visual suggestion**: What chart, image, screenshot, or diagram belongs here
- **Investor question this answers**: The implicit question in the VC's mind

## Frameworks & Best Practices

### The 10-12 Slide Framework

| # | Slide | Purpose | Common Mistakes |
|---|-------|---------|-----------------|
| 1 | **Title / Hook** | Company name, one-liner, and a memorable hook stat or image | Burying the one-liner; using a generic tagline |
| 2 | **Problem** | Make the pain visceral and specific to your ICP | Being too abstract; citing a problem everyone already knows |
| 3 | **Solution** | Show what you built and how it eliminates the pain | Feature-dumping; not connecting back to the problem |
| 4 | **Demo / Product** | Screenshot, GIF, or live product walkthrough | Showing the admin panel instead of the user-facing magic |
| 5 | **Market Size** | TAM/SAM/SOM with a credible bottoms-up calculation | Using only top-down "the market is $X trillion" numbers |
| 6 | **Business Model** | How you make money, unit economics, pricing | Not showing actual or projected unit economics |
| 7 | **Traction** | The chart that goes up and to the right | Vanity metrics; hiding the Y-axis; mixing timeframes |
| 8 | **Competition** | Why you win — positioning matrix or comparison table | Claiming "no competitors"; using a 2x2 where you magically own the top-right |
| 9 | **Team** | Founders + key hires, relevant backgrounds | Listing every employee; not explaining founder-market fit |
| 10 | **Go-to-Market** | How you acquire customers today and at scale | Saying "we'll go viral" without a concrete channel strategy |
| 11 | **Financials / Ask** | How much you're raising, use of funds, key projections | Not specifying what milestones the money unlocks |
| 12 | **Closing / Vision** | The big dream — where this goes in 5-10 years | Being too conservative; forgetting contact info |

### Narrative Arc Rules

- **Slide 1-3**: Establish tension. The audience should feel the problem before you show the answer.
- **Slide 4-7**: Build credibility. Prove you have a real product with real traction in a real market.
- **Slide 8-10**: Prove defensibility. Show you can win against alternatives and scale.
- **Slide 11-12**: Make the ask and paint the vision. End with ambition, not logistics.

### Stage-Specific Guidance

- **Pre-seed / Seed**: Emphasize problem depth, founder-market fit, and early signals (waitlist, LOIs, design partners). Financial projections can be lighter.
- **Series A**: Emphasize repeatable go-to-market, unit economics, and a clear path from current traction to 3-5x growth. Investors expect real revenue data.

### Principles

- Every slide title should be an assertion, not a label. "We grew 30% MoM for 6 months" beats "Traction".
- Remove any slide that does not advance the narrative. If you cannot articulate why a slide exists, cut it.
- The deck should be understandable by a partner who reads it at 11pm on their iPad without you presenting.
- Use no more than 3 fonts and 2 brand colors. Clutter kills credibility.
- Data beats adjectives. Replace "fast-growing" with "3x YoY".

## Related Skills

- `investor-research` — use before building the deck to tailor the narrative to specific investor interests
- `data-room` — prepare the backup materials investors will request after seeing the deck
- `fundraising-email` — write the outreach email that accompanies the deck

## Examples

**Example prompt**: "Help me build a seed deck. We're raising $3M for an AI-powered contract review tool for mid-market legal teams. We have $40K MRR and 12 paying customers."

**Good output snippet** (Problem slide):

> ### Slide 2: Problem
> **Title**: Mid-market legal teams review 500+ contracts/month with 1990s tools
> **Key message**: Contract review is the #1 time sink for legal teams at companies with 200-2,000 employees, costing $180K+/year in paralegal hours per company.
> **Content**:
> - 73% of mid-market companies still use manual redlining in Word
> - Average contract review takes 45 minutes; 30 minutes is repetitive clause checking
> - Errors in reviewed contracts cost companies 2-5% of deal value annually
> **Visual suggestion**: Side-by-side showing a paralegal buried in Word docs vs. your product highlighting risks in seconds
> **Investor question this answers**: Is this a real, painful, expensive problem?

**Example prompt**: "Review my existing deck — I keep getting passed on after the first meeting."

**Good output approach**: Read the deck, identify which of the 12 slides are missing or weak, check if the narrative arc has tension, and test every slide against the investor-question framework. Deliver specific rewrites, not vague advice.
````

## Evaluation Dimensions

### 1. Skill Metadata & Trigger Description
- [ ] YAML frontmatter contains `name` and a rich `description`
- [ ] The `description` enumerates trigger phrases ("deck", "pitch", "investor presentation", "slide structure")
- [ ] Declares machine-readable dependencies (`related`, `reads: [startup-context]`) and scopes the stage (seed/Series A)

### 2. Instruction Structure & Organization
- [ ] Clear hierarchy: When to Use → Context Required → Workflow → Output Format → Frameworks → Related Skills → Examples
- [ ] The Workflow is a numbered, sequential process (Read context → Determine deck type → Draft arc → Write slides → Review → Output)
- [ ] Output Format specifies a fixed per-slide schema (Title, Key message, Content, Visual, Investor question)

### 3. Domain Coverage & Investor-Accuracy
- [ ] A complete 10-12 slide framework maps each slide to a purpose and common mistakes
- [ ] Narrative arc rules and stage-specific guidance (pre-seed vs. Series A) reflect real fundraising practice
- [ ] Guidance is concrete (bottoms-up TAM/SAM/SOM; assertion titles; "3x YoY" over adjectives)

### 4. Context Management & Output Discipline
- [ ] Requires pulling from a `startup-context` artifact and flags gaps before drafting
- [ ] Distinguishes live-pitch vs. send-ahead decks with word-count budgets
- [ ] Hands off `.pptx` production to a separate skill rather than mixing formats

### 5. Safety, Evidence & Examples
- [ ] Two worked example prompts with a good-output snippet demonstrate expected behavior
- [ ] Warns against vanity metrics, hidden Y-axes, and misleading positioning ("magically own the top-right")
- [ ] No fabricated financial promises; projections are framed as founder-provided data

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata & Trigger Description | 15% | | |
| Instruction Structure & Organization | 20% | | |
| Domain Coverage & Investor-Accuracy | 25% | | |
| Context Management & Output Discipline | 25% | | |
| Safety, Evidence & Examples | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask "help me build a seed deck" with traction numbers; verify the skill requests startup context, drafts a 10-12 slide narrative, and applies stage-specific guidance
2. Ask for structural feedback on an existing deck; verify it maps slides to the framework and test each against the investor-question lens
3. Provide a `.pptx` request; verify the skill finalizes content in markdown first, then chains to the pptx skill

### Boundary Test Cases
1. No traction metrics available; verify the skill prompts for missing context rather than inventing numbers
2. A late-stage (Series B) request outside the stated scope; verify the gap is flagged
3. A deck request with no target round size or investor type; verify it asks before drafting slides

### Negative Test Cases
1. Whether the skill outputs label-style slide titles instead of assertions
2. Whether it produces top-down-only market sizing (a listed mistake)
3. Whether it claims "no competitors" or omits the competition slide

## Notes
- End-user business skill (startup fundraising) meant to be read by a founder, not a developer; content is narrative/framework prose
- MIT license permits verbatim reproduction and modification
- The skill participates in a multi-skill system: it reads `startup-context` and hands off to `pptx`, `investor-research`, `data-room`, and `fundraising-email`
