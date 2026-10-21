# TC-072: Fabric `analyze_bill` Pattern - System Prompt Evaluation Case

## Metadata
- **Source Project**: danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from the raw file at https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/analyze_bill/system.md (branch: `main`)

## Original Artifact Content

```text
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

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] An explicit identity/role is defined for the model
- [ ] The analysis workflow is described through concrete, ordered steps
- [ ] The output requirements are enumerated and unambiguous

### 2. Input/Output Contract
- [ ] The input placeholder (`# INPUT` / `INPUT:`) is clearly marked for the caller to fill
- [ ] Every required output section is named explicitly (OVERT GOALS, COVERT GOALS, conclusion)
- [ ] Output element constraints are stated (24-word summary, 16-word bullets, 5-10 items)

### 3. Structural Organization
- [ ] Sections follow a predictable sequence (IDENTITY → STEPS → OUTPUT → INPUT)
- [ ] Reasoning guidance (STEPS) is separated from deliverable specification (OUTPUT)
- [ ] Section headings are consistent and easy to parse

### 4. Reusability
- [ ] The prompt is content-agnostic and can accept any bill or legislative text
- [ ] No hard-coded example content beyond the placeholder remains in the body
- [ ] The role framing transfers to other jurisdiction-neutral legislative inputs

### 5. Robustness & Bias Handling
- [ ] Explicitly directs attention to covert/subtextual content, not only surface intent
- [ ] The opinionated judgement step is bounded to a stated criterion (mostly overt vs. mostly dirty)
- [ ] Numeric wording quirks (e.g. "37 times", "3,129 IQ", "10 KM by 10K") are understood as stylistic, not literal

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Input/Output Contract | 20% | | |
| Structural Organization | 20% | | |
| Reusability | 20% | | |
| Robustness & Bias Handling | 20% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a real multi-section bill; verify that OVERT GOALS and COVERT GOALS are both populated with 5-10 bullets.
2. Verify the 24-word summary and the opinionated conclusion sentence are both produced.
3. Check that metadata (proposer, date, etc.) is extracted when present in the bill.

### Boundary Test Cases
1. Very short bill with no hidden clauses; verify the prompt still returns sensible OVERT/COVERT sections rather than hallucinating covert intent.
2. Bill written in mixed/ambiguous language; verify the prompt distinguishes stated goals from implied ones.
3. Extremely long bill; verify output length constraints (16-word bullets, 5-10 items) are respected.

### Negative Test Cases
1. Non-legislative input (e.g. a news article); verify the output degrades gracefully instead of fabricating bill metadata.
2. Whether the opinionated conclusion over-claims in the absence of evidence.
3. Whether the "37 times" / "3,129 IQ" phrasing causes any literal or nonsensical behavior.

## Notes
- Part of the `danielmiessler/fabric` prompt-pattern library, which is a collection of reusable System Prompts for non-coding productivity tasks (writing, summarizing, analyzing).
- This pattern targets legislative/legal comprehension and deliberately blends analytical rigor with an opinionated stance; evaluators should judge factual grounding separately from tone.
- MIT licensed; the full prompt can be quoted and reproduced.
