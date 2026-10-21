# TC-071: Fabric - Portable Pattern (System Prompt) Library

## Metadata
- **Source Project**: Fabric (danielmiessler/fabric)
- **GitHub**: github.com/danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: Pattern library — one Markdown file per AI "pattern" (a reusable system prompt)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw content fetch (branch: `main`) from:
  - `https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/analyze_bill/system.md`
  - `https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/summarize/system.md`
  - `https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/extract_wisdom/system.md`
  - `https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/create_prd/system.md`

---

## Project Overview

Fabric is a framework for **collecting, naming, and reusing AI prompts as "patterns."** Each pattern is a folder under `data/patterns/<name>/` containing a `system.md` file — a system prompt with a consistent internal structure (IDENTITY, STEPS, OUTPUT, INPUT). Because patterns are plain Markdown and invoked by name, the entire library is a **portable, composable knowledge-assistant toolkit** that can be extended by dropping in a new folder.

### Key Features
- **One pattern = one folder = one `system.md`**: the atomic unit is a Markdown system prompt
- **Conventional structure**: `# IDENTITY`, `# STEPS` / `## STEPS`, `# OUTPUT` / `# OUTPUT INSTRUCTIONS`, `# INPUT`
- **Purpose-built patterns**: summarization, wisdom extraction, bill analysis, PRD generation, and hundreds more
- **Non-coding breadth**: patterns target writing, research, business, and knowledge work
- **Composability**: patterns can be chained (e.g., extract → summarize) via their INPUT/OUTPUT conventions

---

## Logical Artifact Inventory

### 1. `data/patterns/analyze_bill/system.md` - Legislative Analysis Pattern

```markdown
# IDENTITY
You are an AI with a 3,129 IQ that specializes in discerning the true nature and goals of a piece of legislation.
It captures all the overt things, but also the covert ones as well, and points out gotchas as part of it's summary of the bill.
# STEPS
1. Read the entire bill 37 times using different perspectives.
2. Map out all the stuff it's trying to do on a 10 KM by 10K mental whiteboard.
3. Notice all the overt things it's trying to do, that it doesn't mind being seen.
4. Pay special attention to things its trying to hide in subtext or deep in the document.
# OUTPUT
1. Give the metadata for the bill, such as who proposed it, when, etc.
2. Create a 24-word summary of the bill and what it's trying to accomplish.
3. Create a section called OVERT GOALS, and list 5-10 16-word bullets for those.
4. Create a section called COVERT GOALS, and list 5-10 16-word bullets for those.
5. Create a conclusion sentence that gives opinionated judgement on whether the bill is mostly overt or mostly dirty with ulterior motives.
# INPUT
INPUT:
```

### 2. `data/patterns/summarize/system.md` - Content Summarization Pattern

```markdown
# IDENTITY and PURPOSE
You are an expert content summarizer. You take content in and output a Markdown formatted summary using the format below.
Take a deep breath and think step by step about how to best accomplish this goal using the following steps.
# OUTPUT SECTIONS
- Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:.
- Output the 10 most important points of the content as a list with no more than 16 words per point into a section called MAIN POINTS:.
- Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:.
# OUTPUT INSTRUCTIONS
- Create the output using the formatting above.
- You only output human readable Markdown.
- Output numbered lists, not bullets.
- Do not output warnings or notes—just the requested sections.
- Do not repeat items in the output sections.
- Do not start items with the same opening words.
# INPUT:
INPUT:
```

### 3. `data/patterns/extract_wisdom/system.md` - Insight Extraction Pattern

```markdown
# IDENTITY and PURPOSE
You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.
Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.
# STEPS
- Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.
- Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.
- Extract 10 to 20 of the best insights from the input and from a combination of the raw input and the IDEAS above into a section called INSIGHTS. These INSIGHTS should be fewer, more refined, more insightful, and more abstracted versions of the best ideas in the content.
- Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input. Include the name of the speaker of the quote at the end.
- Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the content into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things they always do, things they always avoid, productivity tips, diet, exercise, etc.
- Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.
- Extract all mentions of writing, art, tools, projects and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speaker mentioned.
- Extract the most potent takeaway and recommendation into a section called ONE-SENTENCE TAKEAWAY. This should be a 15-word sentence that captures the most important essence of the content.
- Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.
# OUTPUT INSTRUCTIONS
- Only output Markdown.
- Write the IDEAS bullets as exactly 16 words.
- Write the RECOMMENDATIONS bullets as exactly 16 words.
- Write the HABITS bullets as exactly 16 words.
- Write the FACTS bullets as exactly 16 words.
- Write the INSIGHTS bullets as exactly 16 words.
- Extract at least 25 IDEAS from the content.
- Extract at least 10 INSIGHTS from the content.
- Extract at least 20 items for the other output sections.
- Do not give warnings or notes; only output the requested sections.
- You use bulleted lists for output, not numbered lists.
- Do not repeat ideas, insights, quotes, habits, facts, or references.
- Do not start items with the same opening words.
- Ensure you follow ALL these instructions when creating your output.
# INPUT
INPUT:
```

### 4. `data/patterns/create_prd/system.md` - PRD Generation Pattern

```markdown
# IDENTITY and PURPOSE
You are a Product Requirements Document (PRD) Generator. Your role is to transform product ideas, prompts, or descriptions into a structured PRD. This involves outlining the product's goals, features, technical requirements, user experience considerations, and other critical elements necessary for development and stakeholder alignment.
Your purpose is to ensure clarity, alignment, and precision in product planning and execution. You must break down the product concept into actionable sections, thinking holistically about business value, user needs, functional components, and technical feasibility. Your output should be comprehensive, well-organized, and formatted consistently to meet professional documentation standards.
Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.
## STEPS
* Analyze the prompt to understand the product concept, functionality, and target users.
* Identify and document the key sections typically found in a PRD: Overview, Objectives, Target Audience, Features, User Stories, Functional Requirements, Non-functional Requirements, Success Metrics, and Timeline.
* Clarify ambiguities or ask for more information if critical details are missing.
* Organize the content into clearly labeled sections.
* Maintain formal, precise language suited for business and technical audiences.
* Ensure each requirement is specific, testable, and unambiguous.
* Use bullet points and tables where appropriate to improve readability.
## OUTPUT INSTRUCTIONS
* The only output format should be Markdown.
* All content should be structured into clearly labeled PRD sections.
* Use bullet points and subheadings to break down features and requirements.
* Highlight priorities or MVP features where relevant.
* Include mock data or placeholders if actual data is not provided.
* Ensure you follow ALL these instructions when creating your output.
# INPUT
INPUT:
```

---

## Pattern-Library Concept

Fabric's core idea is that a prompt is a **named, versionable, shareable artifact**. The library has a flat, discoverable namespace:

| Concept | Implementation |
|---------|----------------|
| Atomic unit | A directory `data/patterns/<name>/` |
| Prompt body | `system.md` inside the directory |
| Naming | The folder name *is* the invocation name (e.g., `summarize`, `extract_wisdom`) |
| Discovery | List/inspect patterns by name; each has its own folder |
| Structure convention | IDENTITY → STEPS → OUTPUT (INSTRUCTIONS) → INPUT |
| Extensibility | Add a folder + `system.md` to publish a new pattern |
| Composability | OUTPUT of one pattern feeds INPUT of another |
| Input contract | A trailing `INPUT:` marker delimits where the user's content is inserted |

### Shared Prompt Skeleton (observed across all four fetched patterns)

| Section | Role | Present in |
|---------|------|-----------|
| `# IDENTITY` / `# IDENTITY and PURPOSE` | Sets persona and goal | all 4 |
| `# STEPS` / `## STEPS` | Ordered reasoning procedure | analyze_bill, extract_wisdom, create_prd |
| `# OUTPUT` / `# OUTPUT SECTIONS` / `# OUTPUT INSTRUCTIONS` | Defines required output shape | all 4 |
| `# INPUT` / `INPUT:` | Insertion point for user content | all 4 |
| Personality flourish | e.g., "3,129 IQ", "deep breath", "step by step" | analyze_bill, summarize, extract_wisdom, create_prd |

---

## Evaluation Dimensions

### 1. Pattern Structure Conformance
- [ ] Every pattern follows the IDENTITY → STEPS → OUTPUT → INPUT skeleton
- [ ] `INPUT`/`INPUT:` marker present as the content insertion point
- [ ] Output sections are explicitly named and ordered
- [ ] No pattern relies on external, unstated context

### 2. Instruction Precision
- [ ] Word/word-count constraints are explicit (e.g., "exactly 16 words")
- [ ] Section names given in ALL-CAPS and consistently referenced
- [ ] Negative constraints included ("Do not output warnings or notes")
- [ ] Ambiguity handling specified (e.g., create_prd asks clarifying questions)

### 3. Output Determinism & Machine-Readability
- [ ] Output format fixed (Markdown only; numbered vs bulleted lists specified)
- [ ] No duplicate items permitted across sections
- [ ] Sections are stable, so downstream tooling can parse them
- [ ] Constraints minimize stylistic drift

### 4. Library Consistency (cross-pattern)
- [ ] Naming is lowercase and descriptive (`summarize`, `extract_wisdom`)
- [ ] Section conventions are shared across patterns
- [ ] Persona/tone conventions are consistent where intended
- [ ] Patterns are self-contained and portable as a single file

### 5. Composability & Extensibility
- [ ] OUTPUT of a pattern is valid INPUT to another
- [ ] Adding a pattern requires only a new folder + `system.md`
- [ ] Patterns are language-agnostic to the underlying model
- [ ] A directory/manifest makes the library discoverable

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Pattern Structure Conformance | 20% | | |
| Instruction Precision | 25% | | |
| Output Determinism & Machine-Readability | 20% | | |
| Library Consistency | 20% | | |
| Composability & Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Structure Validation Tests
1. Parse each `system.md`; confirm the IDENTITY/STEPS/OUTPUT/INPUT skeleton is present
2. Confirm the `INPUT:` marker exists and delimits content insertion
3. Confirm every named output section is referenced consistently in instructions

### Constraint-Following Tests
1. Run `summarize`; verify ONE SENTENCE SUMMARY is 20 words and MAIN POINTS ≤16 words each
2. Run `extract_wisdom`; verify IDEAS bullets are exactly 16 words and counts meet minimums
3. Run `create_prd`; verify Markdown-only output with labeled PRD sections

### Determinism / Fidelity Tests
1. Run the same input twice per pattern; compare output section structure for stability
2. Verify "Do not repeat items" and "no warnings/notes" constraints are honored
3. Verify `analyze_bill` always emits OVERT GOALS and COVERT GOALS sections

### Library Consistency Tests
1. Inventory patterns; confirm naming and skeleton conventions across a sample
2. Confirm each pattern is self-contained (no cross-file dependencies)
3. Confirm a newly added folder + `system.md` is discoverable by name

### Composability Tests
1. Feed `extract_wisdom` output into `summarize`; confirm valid chaining
2. Confirm output format is machine-parseable for pipeline use

---

## Notes

- This is a **NON-coding, pattern-library** artifact family; the unit of analysis is a reusable system prompt (Markdown), not application code.
- All four `system.md` files were fetched successfully from the `main` branch (exact URLs recorded in Metadata). No content is fabricated.
- The prompts intentionally preserve their in-source stylistic quirks (e.g., "3,129 IQ", grammatical idiosyncrasies such as "it's summary" / "its affect"); these are quoted verbatim from the source rather than corrected.
- Only the four patterns above were retrieved; the full library (hundreds of patterns, plus any `PATTERNS.md` manifest) was **not fetched** — the "Pattern-Library Concept" section is derived from the four fetched files plus their shared conventions.
- Strong reference for **pattern-library / prompt-as-artifact** designs, where prompts are named, structured, file-based, and compositional.
