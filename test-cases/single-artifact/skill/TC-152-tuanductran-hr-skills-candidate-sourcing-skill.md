# TC-152: tuanductran/hr-skills (Candidate Sourcing) - Skill Evaluation Case

## Metadata
- **Source Project**: tuanductran/hr-skills
- **License**: MIT (LICENSE file present; GitHub API reports `spdx_id: MIT`)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/tuanductran/hr-skills/main/skills/hr-candidate-sourcing/SKILL.md (default branch `main`). Repository README: https://raw.githubusercontent.com/tuanductran/hr-skills/main/README.md . License file: https://raw.githubusercontent.com/tuanductran/hr-skills/main/LICENSE . Skills directory listing (GitHub API): https://api.github.com/repos/tuanductran/hr-skills/contents/skills

## Original Artifact Content

````markdown
---
name: hr-candidate-sourcing
description: "Help talent acquisition and recruiting teams find, engage, and build pipelines of qualified candidates. Use when asked to source candidates, build a talent pipeline, write a Boolean search string, find passive candidates, draft an outreach message, or similar sourcing tasks."
metadata:
  author: Tuan Duc Tran
  version: "1.0.1"
---
# HR candidate sourcing
Helps recruiters and sourcers identify, research, and engage active and passive candidates across channels, and build repeatable sourcing pipelines.
## Supported tasks
- Writing Boolean and X-ray search strings for job boards and search engines
- Building candidate personas and ideal-candidate profiles
- Identifying sourcing channels for a given role or market
- Drafting personalized outreach and InMail messages
- Designing multi-touch outreach cadences
- Building talent pipelines and talent pools for future openings
- Mapping competitor organizations for talent mapping
- Screening and shortlisting candidate profiles against a role
- Writing referral program messaging
- Evaluating sourcing channel effectiveness and cost-per-hire drivers
- Creating diversity sourcing strategies
- Drafting re-engagement messages for dormant candidates
## Key prompts
### Search strategy
1. "Write a Boolean search string for a [role] with [years] years of experience in [industry]."
2. "Create an X-ray search for LinkedIn profiles matching [skill set] in [location]."
3. "Suggest niche job boards and communities for sourcing [role]."
4. "Build a candidate persona for a [role] at a [company stage] company."
5. "List signals that indicate a candidate may be open to new opportunities."
### Outreach and engagement
1. "Draft a personalized LinkedIn InMail for a passive [role] candidate."
2. "Write a 3-touch outreach cadence for candidates who haven't responded."
3. "Create a re-engagement email for candidates from a past pipeline."
4. "Draft a referral request message to send to current employees."
5. "Write a follow-up message after a candidate viewed but didn't respond to an InMail."
### Pipeline and talent mapping
1. "Build a talent pipeline plan for [role] we expect to hire in [timeframe]."
2. "Map competitor companies likely to have candidates for [role]."
3. "Create a scoring rubric to shortlist candidates against [role] requirements."
4. "Design a diversity sourcing strategy for [role]."
5. "Summarize a sourcing channel report and recommend where to invest more effort."
## Tips
- Personalize outreach with a specific, verifiable detail from the candidate's profile.
- Keep first-touch messages short; save role details for a follow-up or call.
- Track response and conversion rates per channel to know where to invest.
- Build pipelines ahead of anticipated openings rather than starting from zero.
- Revisit and re-engage silver-medalist candidates from past searches — they already know your role and passed your bar, and their circumstances may have changed since you last spoke.
## Common mistakes
- Sending generic, templated outreach with no personalization.
- Over-indexing on a single channel (e.g., only LinkedIn) instead of diversifying.
- Losing track of previously sourced candidates instead of maintaining a pipeline.
- Writing Boolean strings that are too broad or too narrow to be useful.
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter has `name` (`hr-candidate-sourcing`), a quoted `description`, and `metadata.author` / `metadata.version`
- [ ] `description` enumerates concrete sourcing triggers (Boolean search, talent pipeline, outreach, passive candidates)
- [ ] No in-file `license` field, but the repository LICENSE is MIT

### 2. Trigger Condition Clarity
- [ ] `description` states the "when to use" cases in a single quoted sentence
- [ ] Named triggers match the "Supported tasks" and "Key prompts" sections
- [ ] Scope is clearly sourcing/recruiting, distinct from broader HR administration

### 3. Instruction Structure
- [ ] Clear hierarchy: Supported tasks → Key prompts (grouped) → Tips → Common mistakes
- [ ] Task groups are logically separated (search strategy, outreach, pipeline/talent mapping)
- [ ] Prompt templates use explicit placeholders ("[role]", "[years]", "[location]")

### 4. Example / Output Quality
- [ ] Fifteen concrete, fill-in-the-blank prompt templates across three task groups
- [ ] Practical tips grounded in sourcing practice (personalization, channel mix, silver-medalists)
- [ ] A "Common mistakes" section listing anti-patterns to avoid

### 5. Maintainability
- [ ] Self-contained; no external dependencies or scripts
- [ ] Versioned (`1.0.1`) and attributed (`author: Tuan Duc Tran`)
- [ ] Single-responsibility scope within a larger HR skills library

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. "Write a Boolean search string for a senior backend engineer in fintech"; verify it produces a scoped Boolean/X-ray string
2. "Draft a LinkedIn InMail for a passive candidate"; verify it personalizes and keeps the first touch short
3. "Build a talent pipeline for data scientists we'll hire next year"; verify it produces a pipeline/pool plan

### Boundary Test Cases
1. Ambiguous request ("help with hiring"); verify it clarifies whether the need is sourcing vs. screening vs. outreach
2. Role with no clear market; verify it proposes channels/personas rather than inventing candidate names
3. Request for a diversity sourcing strategy; verify it addresses diverse channels without fabricating legal claims

### Negative Test Cases
1. Whether it fabricates candidate profiles or real contact details
2. Whether generated Boolean strings are so broad/narrow they violate the skill's own "Common mistakes"
3. Whether it drifts into non-sourcing HR work (compensation, discipline) outside its stated scope

## Notes
- End-user HR / talent-acquisition artifact authored as a Markdown SKILL.md; the body is task lists, prompt templates, and best practices, not executable code.
- MIT license permits verbatim reproduction.
- The repository ships a large HR skills library (many `skills/hr-*` directories, e.g. `hr-analytics`, `hr-candidate-assessment`, `hr-onboarding`); this case captures only the single `hr-candidate-sourcing` skill. It is a Claude Code plugin plus a TypeScript build toolchain, but the captured artifact is the domain skill itself.
- Same repository also bundles generic dev-toolchain skills under `.agents/skills/` (biome, bun, turbo, etc.); those are out of scope and were not captured.
