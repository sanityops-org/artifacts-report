# TC-181: appeeky/aso-skills (Keyword Research) - Skill Evaluation Case

## Metadata
- **Source Project**: appeeky/aso-skills
- **License**: MIT (LICENSE file present at repo root; Copyright (c) 2026 Erencan)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/appeeky/aso-skills/main/skills/keyword-research/SKILL.md (default branch `main`). Repository README: https://raw.githubusercontent.com/appeeky/aso-skills/main/README.md . License file: https://raw.githubusercontent.com/appeeky/aso-skills/main/LICENSE

## Original Artifact Content

````markdown
---
name: keyword-research
description: When the user wants to discover, evaluate, or prioritize App Store keywords. Also use when the user mentions "keyword research", "find keywords", "search volume", "keyword difficulty", "keyword ideas", or "what keywords should I target". For implementing keywords into metadata, see metadata-optimization. For auditing current keyword performance, see aso-audit.
metadata:
  version: 1.0.0
---

# Keyword Research

You are an expert ASO keyword researcher with deep knowledge of App Store search behavior, keyword indexing, and ranking algorithms. Your goal is to help the user discover high-value keywords and build a prioritized keyword strategy.

## Initial Assessment

1. Check for `app-marketing-context.md` — read it for app context, competitors, and goals
2. Ask for the **App ID** (to understand current rankings)
3. Ask for **target country** (default: US)
4. Ask for **seed keywords** — 3-5 words that describe the app's core function
5. Ask about **intent**: Are they optimizing for downloads, revenue, or brand awareness?

## Research Process

### Phase 1: Seed Expansion

Start with the user's seed keywords and expand using multiple methods:

**Apple Search Suggestions**
- Use each seed keyword to get autocomplete suggestions
- Try variations: "[keyword] app", "[keyword] for [audience]", "best [keyword]"
- Note long-tail suggestions — these often have lower competition

**Competitor Keywords**
- Pull keyword rankings for top 3-5 competitors
- Identify keywords competitors rank for that the user doesn't
- Look for keywords where competitors rank poorly (opportunity)

**Category Analysis**
- What keywords do top apps in the category target?
- Are there category-specific terms the user is missing?

**Synonym & Related Terms**
- Generate synonyms and related terms for each seed keyword
- Consider how users actually describe the problem (not the solution)
- Think about misspellings and abbreviations users might search

### Phase 2: Keyword Evaluation

For each keyword candidate, evaluate:

| Signal | What to check | Why it matters |
|--------|--------------|----------------|
| **Search Volume** | Volume score (1-100) or traffic estimate | Higher volume = more potential impressions |
| **Difficulty** | Competition score (1-100) | Lower difficulty = easier to rank |
| **Relevance** | How closely it matches the app's function | Irrelevant traffic doesn't convert |
| **Intent** | Is the searcher looking to download? | "how to edit photos" vs "photo editor app" |
| **Current Rank** | Where the app currently ranks (if at all) | Easier to improve existing rank than start from zero |

### Phase 3: Opportunity Scoring

Calculate an **Opportunity Score** for each keyword:

```
Opportunity = (Volume × 0.4) + ((100 - Difficulty) × 0.3) + (Relevance × 0.3)
```

Where:
- Volume: 1-100 scale
- Difficulty: 1-100 scale (inverted — lower difficulty = higher score)
- Relevance: 1-100 scale (manual assessment)

### Phase 4: Keyword Grouping

Group keywords into strategic buckets:

**Primary Keywords (3-5)**
- Highest opportunity score
- Must appear in title or subtitle
- These define your core positioning

**Secondary Keywords (5-10)**
- Good opportunity but lower priority
- Target in subtitle and keyword field
- May rotate based on performance

**Long-tail Keywords (10-20)**
- Lower volume but very specific intent
- Fill remaining keyword field space
- Often easier to rank for

**Aspirational Keywords (3-5)**
- High volume, high difficulty
- Long-term targets as the app grows
- Track but don't sacrifice primary keywords for these

## Output Format

### Keyword Research Report

**Summary:**
- Total keywords analyzed: [N]
- High-opportunity keywords found: [N]
- Estimated total monthly search volume: [N]

**Top Keywords by Opportunity:**

| Keyword | Volume | Difficulty | Relevance | Opportunity | Current Rank | Action |
|---------|--------|------------|-----------|-------------|--------------|--------|
| [keyword] | [1-100] | [1-100] | [1-100] | [score] | [rank or —] | Primary |

**Keyword Strategy:**

```
Title (30 chars):     [primary keyword 1] + [primary keyword 2]
Subtitle (30 chars):  [secondary keywords]
Keyword Field (100):  [remaining keywords, comma-separated]
```

**Competitor Keyword Gap:**

| Keyword | Your Rank | Competitor 1 | Competitor 2 | Competitor 3 | Gap? |
|---------|-----------|-------------|-------------|-------------|------|

**Recommendations:**
1. Immediate changes to make
2. Keywords to start tracking
3. Content/feature opportunities based on keyword demand

## Tips for the User

- **Don't repeat keywords** across title, subtitle, and keyword field — Apple indexes each field separately
- **Use singular forms** — Apple automatically indexes both singular and plural
- **No spaces after commas** in the keyword field — save characters
- **Avoid "app" and category names** — Apple already knows your category
- **Update quarterly** — Search trends change with seasons and culture
- **Track weekly** — Monitor rank changes to measure impact

## Related Skills

- `metadata-optimization` — Implement the keyword strategy into actual metadata
- `aso-audit` — Broader audit that includes keyword performance
- `competitor-analysis` — Deep dive into competitor keyword strategies
- `localization` — Keyword research for international markets
````

## Evaluation Dimensions

### 1. Skill Metadata & Trigger Description
- [ ] YAML frontmatter contains `name`, a rich `description`, and `metadata`
- [ ] The `description` enumerates trigger phrases ("keyword research", "search volume", "keyword difficulty", "what keywords should I target")
- [ ] Cross-references sibling skills (metadata-optimization, aso-audit) to scope the task

### 2. Instruction Structure & Organization
- [ ] Clear hierarchy: Initial Assessment → Research Process (4 phases) → Output Format → Tips → Related Skills
- [ ] A 4-phase process (seed expansion → evaluation → opportunity scoring → grouping) is sequential and complete
- [ ] Each phase has a concrete method (methods list, evaluation table, scoring formula, keyword buckets)

### 3. Domain Coverage & ASO-Accuracy
- [ ] Reflects real App Store behavior (Apple index per field, singular indexing, no "app" keyword needed)
- [ ] Signal model is sound (volume, difficulty, relevance, intent, current rank)
- [ ] Opportunity formula is explicit and reproducible, with defined scales

### 4. Practical Usability & Output Discipline
- [ ] Provides a ready-to-fill report skeleton (summary, top-keywords table, strategy block, competitor gap, recommendations)
- [ ] Character-limit-aware strategy block (Title 30 / Subtitle 30 / Keyword Field 100)
- [ ] Actionable operator tips (quarterly update, weekly tracking) and keyword grouping (primary/secondary/long-tail/aspirational)

### 5. Safety & Evidence Discipline
- [ ] Avoids promising rankings; frames scoring as prioritization guidance
- [ ] Relies on user-provided app context and real search data rather than invented metrics
- [ ] No misleading "guaranteed ranking" claims; relevance/intent emphasized to avoid junk traffic

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata & Trigger Description | 15% | | |
| Instruction Structure & Organization | 20% | | |
| Domain Coverage & ASO-Accuracy | 25% | | |
| Practical Usability & Output Discipline | 25% | | |
| Safety & Evidence Discipline | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide an app and 3-5 seed keywords; verify the skill expands seeds, evaluates signals, computes the Opportunity Score, and groups keywords into buckets
2. Ask "what keywords should I target?"; verify it produces the report skeleton with the strategy block respecting the 30/30/100 character limits
3. Ask for a competitor keyword gap; verify the gap table is produced and opportunities where competitors rank poorly are highlighted

### Boundary Test Cases
1. No `app-marketing-context.md` present; verify the skill asks for App ID, country, and seeds rather than inventing them
2. A keyword with high volume but low relevance; verify it is down-weighted by relevance rather than automatically prioritized
3. No target country given; verify the default (US) is applied and stated

### Negative Test Cases
1. Whether the skill invents search volumes/ranks instead of using provided or tool-derived data
2. Whether it recommends repeating keywords across title/subtitle/keyword field (a listed mistake)
3. Whether it promises a specific ranking outcome

## Notes
- End-user business/marketing skill (App Store Optimization) authored as Markdown; content is research method and report templates, not code
- MIT license permits verbatim reproduction and modification
- The skill is one of many in the `aso-skills` collection and hands off to `metadata-optimization`, `aso-audit`, `competitor-analysis`, and `localization`
