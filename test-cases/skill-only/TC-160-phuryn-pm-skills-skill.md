# TC-160: phuryn/pm-skills (Product Strategy Canvas) - Skill Evaluation Case

## Metadata
- **Source Project**: phuryn/pm-skills
- **License**: MIT (GitHub API reports `spdx_id: MIT`; LICENSE file present)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/phuryn/pm-skills/HEAD/pm-product-strategy/skills/product-strategy/SKILL.md (resolved default branch). Repository README: https://raw.githubusercontent.com/phuryn/pm-skills/HEAD/README.md . License file: https://raw.githubusercontent.com/phuryn/pm-skills/HEAD/LICENSE

## Original Artifact Content

````markdown
---
name: product-strategy
description: "Create a comprehensive product strategy using the 9-section Product Strategy Canvas — vision, segments, costs, value propositions, trade-offs, metrics, growth, capabilities, and defensibility. Use when building a product strategy, creating a strategic plan, or defining product direction."
---
# Product Strategy Canvas

## Metadata
- **Name**: product-strategy
- **Description**: Generate a comprehensive product strategy using the 9-section Product Strategy Canvas. Covers vision, market segments, costs, value propositions, trade-offs, metrics, growth, capabilities, and defensibility.
- **Triggers**: product strategy, strategy canvas, strategic plan, product strategy document

## Instructions

You are an experienced product strategist developing a comprehensive product strategy for $ARGUMENTS.

Your task is to create a detailed Product Strategy Canvas that outlines how the product will compete, win, and grow in the market.

## Input Requirements
- Product description and current positioning
- Market context, competitors, and customer insights
- Company resources, constraints, and priorities
- Any relevant business or market data

## Product Strategy Canvas Template

### 1. Vision
- How can we inspire people?
- What are we aspiring to achieve?
- What values do we uphold?

### 2. Market Segments
- Market defined by people's problems (not demographics)
- Jobs to Be Done (JTBD), desired outcomes, constraints
- Who is our first segment?
- Why this segment first?

### 3. Relative Costs
- Do we optimize for low cost (like Southwest Airlines)?
- Or do we emphasize unique value (like Starbucks)?
- What's our cost position relative to competitors?

### 4. Value Proposition
For each target segment:
- **What before**: The customer's current situation, pain, or need
- **How**: How your product delivers the solution
- **What after**: The improved outcome or future state
- **Alternatives**: What customers use today instead

### 5. Trade-offs
- What will we NOT do?
- What features or markets are out of scope?
- How does saying "no" create focus and amplify our value?

### 6. Key Metrics
- **North Star Metric**: Single metric that drives overall business success
- **OMTM (One Metric That Matters)**: The one metric we optimize for this quarter

### 7. Growth
- Sales-Led Growth or Product-Led Growth?
- Primary acquisition channels
- How do we scale?
- What's our unit economics?

### 8. Capabilities
- What competencies and resources do we need?
- What do we build vs. partner for?
- What capabilities must we develop to win?

### 9. Can't/Won't
- Why can't competitors easily copy this?
- What defensibility do we have (network effects, switching costs, IP)?
- What barriers to entry exist for new competitors?

## Output Process
1. Define the vision and aspirational impact
2. Identify 2-3 target market segments with their JTBD
3. Establish cost positioning (low cost vs. premium value)
4. Develop value propositions for each segment
5. List explicit trade-offs (what we won't do)
6. Set North Star and quarterly OMTM
7. Outline growth strategy and channels
8. Document required capabilities and partnerships
9. Explain defensibility and barriers to competition
10. Validate strategy coherence: ensure elements reinforce each other
11. Surface critical hypotheses that must be true for success
12. Suggest low-effort experiments to test key assumptions

## Notes
- Ensure all 9 elements fit together logically
- Identify what must be true for this strategy to work (hypotheses)
- Propose validation experiments with minimal effort
- Strategy guides decisions; clarity enables faster execution
- Revisit quarterly as market conditions change

---

### Templates

- [Product Strategy Canvas (PPTX)](https://docs.google.com/presentation/d/1xRBqSOISvAKzwM_z5tC8fiuO5O2YhboB/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### Further Reading

- [Product Strategy Canvas: From Vision to Action](https://www.productcompass.pm/p/product-strategy-canvas)
- [Product Strategy Examples: Google Maps, Netflix, OpenAI](https://www.productcompass.pm/p/product-strategy-examples)
- [Product Vision vs Strategy vs Objectives vs Roadmap: The Advanced Edition](https://www.productcompass.pm/p/product-vision-strategy-goals-and)
- [Product Model First Principles: Product Team and Product Strategy In Depth](https://www.productcompass.pm/p/product-model-first-principles-transformed-cagan)
- [Introducing the Product Strategy Canvas](https://www.productcompass.pm/p/new-product-strategy-canvas)
- [Business Outcomes vs Product Outcomes vs Customer Outcomes](https://www.productcompass.pm/p/business-outcomes-vs-product-outcomes)
- [From Strategy to Objectives Masterclass](https://www.productcompass.pm/p/product-vision-strategy-objectives-course) (video course)
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter contains the required `name` field (`product-strategy`)
- [ ] `description` states the trigger conditions and the 9-section scope
- [ ] No `license` field in frontmatter (repository LICENSE is MIT)

### 2. Trigger Condition Clarity
- [ ] `description` enumerates trigger situations (building a product strategy, strategic plan, product direction)
- [ ] A `## Metadata` section lists explicit trigger keywords (`product strategy`, `strategy canvas`, `strategic plan`)
- [ ] Scoping input via `$ARGUMENTS` is documented

### 3. Instruction Structure
- [ ] Clear 9-section template with a numbered `## Output Process`
- [ ] Separate `## Input Requirements` and `## Notes` sections
- [ ] Coherent flow from inputs to template to output process

### 4. Example / Output Quality
- [ ] Each canvas section gives concrete guiding questions
- [ ] The output process names the concrete deliverable (a filled canvas)
- [ ] Provides a template link (Google Slides) and a Further Reading list

### 5. Maintainability
- [ ] Single self-contained Markdown file with no external dependencies
- [ ] Sections are modular and independently editable
- [ ] References an external source (Product Compass) for evolution

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
1. "Build a product strategy for our B2B analytics tool"; verify the skill produces all 9 canvas sections
2. "Create a strategic plan for a freemium marketplace"; verify North Star and OMTM are defined
3. "Define product direction for an AI writing assistant"; verify hypotheses and low-effort experiments are surfaced

### Boundary Test Cases
1. Vague input with no market context; verify it asks for or states assumptions instead of fabricating data
2. A product targeting multiple unrelated segments; verify it suggests narrowing to a first segment
3. A strategy request with no metrics available; verify it still proposes candidate North Star metrics with caveats

### Negative Test Cases
1. Whether a non-strategy request ("write a PRD") triggers this skill incorrectly
2. Whether it invents competitor/market facts not provided by the user
3. Whether it omits the trade-offs ("what we won't do") section under time pressure

## Notes
- End-user product-management artifact; part of the `pm-skills` marketplace (69 skills / 42 workflows across 9 plugins, MIT).
- The SKILL.md is an instruction body (no executable code); `$ARGUMENTS` is the host's input placeholder.
- MIT license permits verbatim reproduction.
- Distinct from TC-158 (openclaudia pricing-strategy) and TC-081 (contract-proposal-writer): this is a full product-strategy canvas skill.
