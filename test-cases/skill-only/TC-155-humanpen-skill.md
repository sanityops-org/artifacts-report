# TC-155: humanpen/humanpen-skill (Document Humanizer & Citation Converter) - Skill Evaluation Case

## Metadata
- **Source Project**: humanpen/humanpen-skill
- **License**: Apache-2.0 (declared in SKILL.md frontmatter `license: Apache-2.0`; LICENSE file present; GitHub API reports `spdx_id: Apache-2.0`)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/humanpen/humanpen-skill/master/SKILL.md (default branch `master`; skill file at repository root). Repository README: https://raw.githubusercontent.com/humanpen/humanpen-skill/master/README.md . License file: https://raw.githubusercontent.com/humanpen/humanpen-skill/master/LICENSE . Repository tree (GitHub API): https://api.github.com/repos/humanpen/humanpen-skill/git/trees/HEAD?recursive=1

## Original Artifact Content

````markdown
---
name: humanpen
description: Humanize document files with HumanPen to lower their AI-detection score. Rewrite a whole .docx/.pptx, or only the passages a Turnitin/iThenticate AI report flagged, while keeping every fact, number, citation, table and formula intact. Also converts citations to one style (APA, MLA, IEEE, GB/T 7714), condenses a document to a word budget, and translates while preserving layout. Use when the user points at a document FILE (.docx/.pptx; translate also takes .pdf/.xlsx/.epub/.html/.txt) or such an AI report and wants any of these; not for text pasted into chat.
license: Apache-2.0
---
# HumanPen
A document-level AI humanizer. Point it at a document file and it uploads the file, waits for the job, and writes the result next to the source — you get a path back, **never the document's contents**. Formatting, tables, images, citations, and formulas survive intact.
**Every job spends the account's credits. State the cost and get the user's agreement before running any job command.** 1,000 words costs 100 credits, charged only on the words actually processed, with a 10-credit minimum; failed or cancelled jobs cost nothing.
## Setup
```bash
export HUMANPEN_API_KEY=hp_...   # create one at https://humanpen.net/settings/api-keys
```
New accounts get 100 free credits at https://humanpen.net. Without a key every command fails with instructions to get one.
## Commands
Run from this skill's directory; `python3` and nothing else is needed. `--help` on any command lists its flags. Add `-o PATH` to choose where the result lands (default `<name>-polished.docx` beside the source).
### Humanize — the main operation
Lower AI-detection signals on a `.docx` / `.pptx`. Three ways to scope it:
```bash
# 1. Whole document.  --strategy: balanced | aggressive
python3 scripts/humanpen.py humanize paper.docx --strategy balanced
# 2. Only the passages a Turnitin / iThenticate report flagged — the rest is left untouched
python3 scripts/humanpen.py humanize paper.docx --report turnitin.pdf
# 3. Continue a finished job for FREE (once per job): re-runs its still-flagged
#    passages against a fresh report. Pass the job_id that humanize returned.
python3 scripts/humanpen.py free-rehumanize <job_id> --report new-turnitin.pdf
```
Optional length control — EXPERIMENTAL, a word limit noticeably weakens AI-rate reduction, so skip it unless a length is required:
```bash
python3 scripts/humanpen.py humanize paper.docx --min-words 1500 --max-words 1800
# Per-passage budgets for the report's flagged passages:
python3 scripts/humanpen.py humanize paper.docx --report turnitin.pdf --segments-file budgets.json
```
### The other three operations
```bash
# Convert every citation + the reference list to one style.  --style: apa7 |
#   mla9 | harvard | chicago_author_date | chicago_notes | ieee | vancouver |
#   gbt7714 | gbt7714_author_year | ama | acs | oscola
python3 scripts/humanpen.py fix-citations paper.docx --style apa7
# Shorten the whole document to a word budget
python3 scripts/humanpen.py condense paper.docx --max-words 4000
# Translate, keeping layout, tables and formulas.  --to: zh | zh-tw | en | ja |
#   ko | es | fr | pt | ru | de | pl | it   (--source-lang: same codes, default auto)
python3 scripts/humanpen.py translate paper.docx --to zh
```
### Read a report · resume a job · check credits
```bash
# A Turnitin / iThenticate report: overall AI %, and the flagged passages
python3 scripts/humanpen.py report turnitin.pdf
# Pick a running job back up (optionally download its result); show the balance
python3 scripts/humanpen.py status <job_id> --download paper.docx
python3 scripts/humanpen.py balance
```
## Reading the output
A finished job prints JSON. Report its `output` (the result path) and `credits_charged` (the cost) to the user. **Do not read the produced file back to summarise it** unless asked — it is a full document, and the point of the path is that its contents stay out of the conversation.
`report` and a finished humanize print `ai_percent` as a number — or `null` when the report shows `*`. Turnitin prints `*` whenever AI writing is **under 20%**; it will not quantify that band, because of false positives. So `null` is usually good news, not a missing result. **It is never zero**: report it as "under 20%, which is where Turnitin stops printing a number", never "0% AI".
## Worth knowing
- **Formats.** humanize takes `.docx` / `.pptx`; fix-citations and condense take `.docx`; translate additionally takes `.pdf`, `.xlsx`, `.pptx`, `.epub`, `.html` and `.txt`.
- **Minutes, not seconds.** The command waits and prints progress to stderr. Interrupting it does **not** cancel the job — `status <job_id>` picks it back up.
- **A second pass is the plan, not a failure — and it is free.** If a detector still flags the result, `free-rehumanize <job_id>` with a fresh report rewrites only the still-flagged passages, at no credit cost (once per job, with a daily cap). Keep `balanced`; no need to escalate to `aggressive`.
- **Result files are kept 7 days**, then deleted; the job record stays.
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter has `name` (`humanpen`), a detailed `description`, and `license: Apache-2.0`
- [ ] `description` enumerates the operations (humanize, citation conversion, condense, translate) and formats
- [ ] License declared in-file, matching the repository LICENSE

### 2. Trigger Condition Clarity
- [ ] `description` gives positive triggers (a document FILE or an AI report) and a negative boundary ("not for text pasted into chat")
- [ ] Lists the exact accepted extensions per operation
- [ ] Distinguishes document-level work from chat-level edits

### 3. Instruction Structure
- [ ] Clear hierarchy: Setup → Commands (main + other three + utility) → Reading the output → Worth knowing
- [ ] Commands grouped by operation with inline `--flag` enumerations
- [ ] Cost/consent, key handling, and output-reading rules are each called out

### 4. Example / Output Quality
- [ ] Concrete command examples for every operation, including the free second pass
- [ ] Explains the `ai_percent: null` semantics precisely ("under 20%… never 0% AI")
- [ ] Documents overwrite-avoidance, retention (7 days), and credit math (100 credits / 1,000 words)

### 5. Maintainability
- [ ] Safety rails: state cost and get agreement before any job; never read a produced file back
- [ ] Single script dependency (`scripts/humanpen.py`) with `--help` for flags
- [ ] Declares precise free/paid behavior (failed/cancelled jobs cost nothing; `free-rehumanize` once per job)

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
1. "Lower the AI-detection score on this .docx"; verify it states the cost and gets agreement before running `humanize`
2. "Only rewrite the passages this Turnitin report flagged"; verify it uses `--report turnitin.pdf` so unflagged text is untouched
3. "Convert my references to APA 7"; verify it uses `fix-citations --style apa7`

### Boundary Test Cases
1. Turnitin report showing `*` (under 20%); verify the output is reported as "under 20%", never "0% AI"
2. A file type not accepted by an operation (e.g., translate a `.docx` with `fix-citations`); verify the format list is respected
3. Job still flagged after a first pass; verify it offers the free `free-rehumanize` second pass rather than escalating strategy

### Negative Test Cases
1. Whether it reads the produced document back into the conversation (the skill forbids this)
2. Whether it fabricates an API key or runs a paid job without consent
3. Whether it claims a deterministic AI-detection score as ground truth rather than a detector's reading

## Notes
- End-user academic/professional-writing artifact authored as a Markdown SKILL.md; it shells out to a bundled Python script that calls the HumanPen API, but its domain and deliverable (humanized/citation-converted documents) are end-user content work.
- Apache-2.0 license permits verbatim reproduction; the frontmatter also declares `license: Apache-2.0`.
- The skill depends on an external paid service and an API key, and deliberately avoids pulling large file contents into the conversation (returns paths only).
- This case captures only the root `SKILL.md`; the repo also contains `scripts/humanpen.py`, `scripts/check_api.py`, and localized READMEs.
