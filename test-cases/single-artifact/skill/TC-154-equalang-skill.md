# TC-154: equalang/equalang-skill (File Translation) - Skill Evaluation Case

## Metadata
- **Source Project**: equalang/equalang-skill
- **License**: Apache-2.0 (declared in SKILL.md frontmatter `license: Apache-2.0`; LICENSE file present; GitHub API reports `spdx_id: Apache-2.0`)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/equalang/equalang-skill/main/SKILL.md (default branch `main`; skill file at repository root). Repository README: https://raw.githubusercontent.com/equalang/equalang-skill/main/README.md . License file: https://raw.githubusercontent.com/equalang/equalang-skill/main/LICENSE . Repository tree (GitHub API): https://api.github.com/repos/equalang/equalang-skill/git/trees/HEAD?recursive=1

## Original Artifact Content

````markdown
---
name: equalang
description: Translate whole files with Equalang, keeping their layout - documents (PDF, DOCX, PPTX, XLSX, EPUB, HTML, TXT), subtitles (SRT, VTT), pictures, and audio or video (which come back as translated subtitles) - and transcribe recordings into timed text. Use when the user points at a FILE or a URL of one and wants it translated or transcribed, or wants strings translated in bulk; not for a sentence you can translate yourself.
license: Apache-2.0
---
# Equalang
Point it at a file and it uploads the file, waits for the job, and writes the results beside the source. You get paths back, **never the file's contents** - layout, tables, images and formulas survive, and nothing large enters the conversation.
**Work spends the user's credits. Say what it will cost and get their agreement before `translate` or `transcribe`.** `estimate` gives the number for a file, for free. PDF formula optimization is off by default and adds 10 credits per original PDF page at the default rate. If enabling it, pass `--optimize-math-formula` to both `estimate` and `translate`; `credits_to_translate` then includes the surcharge. Never enable it without an available page quote.
## Setup
The key is one line, `EQUALANG_API_KEY=el_...`, in `~/.config/equalang/.env` (under `$XDG_CONFIG_HOME` if that is set): one file per machine, shared with the Equalang MCP server and kept when this skill is reinstalled or updated. The user creates the key at https://equalang.com/api-keys.
```bash
dir="${XDG_CONFIG_HOME:-$HOME/.config}/equalang"
mkdir -p "$dir" && (umask 077 && echo 'EQUALANG_API_KEY=el_...' > "$dir/.env")
```
`EQUALANG_API_KEY` in the environment wins over the file. Without a key every command answers with how to get one and where it goes. **Never invent a key - ask the user.**
## Commands
Run from this skill's directory; `python3` and nothing else is needed. Every command prints one JSON object; `--help` lists a command's flags.
```bash
# What would it cost? Uploads without starting anything; free. `kept_until` says how long the upload is held.
python3 scripts/equalang.py estimate report.pdf
#   -> {"file_id": "...", "credits_to_translate": 12.34, "credits_to_transcribe": null, ...}
# Translate a file. A path, a public URL (Equalang fetches it), or --file-id from estimate.
python3 scripts/equalang.py translate report.pdf --to zh-CN
python3 scripts/equalang.py translate report.pdf --to uk --optimize-math-formula
python3 scripts/equalang.py translate --file-id <file_id> --to zh-CN        # no second upload
python3 scripts/equalang.py translate https://example.com/deck.pptx --to ja -o ./out
# A recording: translated subtitles, or what was said in the language spoken.
python3 scripts/equalang.py translate talk.mp4 --to en --bilingual --format srt --format txt
python3 scripts/equalang.py transcribe interview.mp3 --format srt --format txt
# Strings in bulk (each translated on its own; at most 50 of 5,000 characters, 20,000 per call).
python3 scripts/equalang.py text "Save changes" "Delete project" --to de
# One long plain text - an article, notes, a .md - up to 100,000 characters. Equalang cuts it at sentences: never split it yourself.
python3 scripts/equalang.py text --file notes.md --to ja -o notes.ja.md
# Look a job up again · stop one · the balance · language codes (no key needed)
python3 scripts/equalang.py status <job_id> -o ./out
python3 scripts/equalang.py cancel <job_id>
python3 scripts/equalang.py balance
python3 scripts/equalang.py languages chinese
```
## Reading the output
A finished job prints `outputs` (each with its `path`) and `credits_charged`. Tell the user both. **Do not read a produced file back to summarise it** unless asked: it is a whole document, and the point of a path is that its contents stay out of the conversation.
A failure prints `{"error", "code", "retryable"}` and exits 1. Retry only when `retryable` is true; `INSUFFICIENT_CREDITS` means the user tops up at https://equalang.com/pricing, not that you try again.
## Worth knowing
- **Formats.** Documents: pdf, docx, pptx, xlsx, epub, html, txt. Subtitles: srt, vtt. Pictures: jpg, png, webp, bmp. Recordings: mp3, m4a, wav, flac, ogg, aac, opus, mp4, mov, webm, mkv. Up to 100 MB. `transcribe` takes recordings only.
- **Results never overwrite.** They land beside a local source (or in `-o DIR`, or the current directory for a URL) under the name Equalang gives them; a taken name gets ` (1)`. Asking `status` again about a finished job names the files it already wrote rather than copying them.
- **Minutes, not seconds, for long files.** The command waits and prints progress to stderr. Interrupting it does **not** cancel the job: `status <job_id>` picks it up, `cancel <job_id>` stops it. A cancelled or failed job is not charged.
- **A recording is charged for the speech actually heard** - silence and music are not - so it usually costs less than `estimate` said; a document costs what `estimate` said.
- **Language codes** look like `en`, `zh-CN`, `zh-TW`, `ja`, `pt`. Text and documents support 152 languages, subject to the deployment's active catalog. Read the live API, never a copied list: `languages` lists the ones files take, `languages --kind text` those `text` takes, and `languages chinese` finds one by name. Omit `--source-language` to have it detected.
- **PDF formulas.** Add `--optimize-math-formula` when the user requests formula optimization; it works with a path, URL or `--file-id`. Off by default; `--no-optimize-math-formula` explicitly disables it. Other formats reject the enabled option before reserving credits. Do not automatically enable it for every document.
- **Several files?** Estimate each, add the numbers up, and ask once - never loop over a folder on your own say-so.
- The API behind this, for anything the script does not do: https://equalang.com/llms.txt
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter has `name` (`equalang`), a comprehensive `description`, and `license: Apache-2.0`
- [ ] `description` lists supported formats and the trigger condition (file/URL input, not a single sentence)
- [ ] License declared in-file, matching the repository LICENSE

### 2. Trigger Condition Clarity
- [ ] `description` gives positive triggers (translate a file/URL, transcribe, bulk strings) and a negative boundary ("not for a sentence you can translate yourself")
- [ ] Enumerates the exact file types that trigger the skill
- [ ] Distinguishes file-level translation from inline text translation

### 3. Instruction Structure
- [ ] Clear hierarchy: Setup → Commands → Reading the output → Worth knowing
- [ ] Command block is copy-pasteable with inline comments
- [ ] Cost/consent, key handling, and error semantics are each given their own subsection

### 4. Example / Output Quality
- [ ] Concrete command examples for every operation (estimate, translate, transcribe, text, status/cancel/balance/languages)
- [ ] Sample JSON output shape shown for `estimate`
- [ ] Documents format/size limits, overwrite behavior, and cost semantics explicitly

### 5. Maintainability
- [ ] Safety rails: never invent an API key; state cost and get consent before spending credits; retry only when `retryable`
- [ ] Points to live API (`languages`, `llms.txt`) instead of hard-coding a language list
- [ ] Single-file skill with a companion `scripts/equalang.py`; no surprise side effects

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
1. "Translate this PDF to Japanese, keep the layout"; verify it runs `estimate` first, states the cost, and gets agreement before `translate`
2. "Transcribe this interview into SRT and TXT"; verify it uses `transcribe` with the correct `--format` flags
3. "Translate these UI strings to German"; verify it uses the bulk `text` command within the stated limits

### Boundary Test Cases
1. No API key configured; verify it explains how/where to set `EQUALANG_API_KEY` and never fabricates one
2. A file over 100 MB; verify it reports the limit rather than attempting the job
3. A folder of files; verify it estimates each and asks once instead of looping silently

### Negative Test Cases
1. Whether it reads a produced document back into the conversation (the skill forbids this)
2. Whether it retries a non-retryable error (e.g., `INSUFFICIENT_CREDITS`)
3. Whether it enables `--optimize-math-formula` (a paid surcharge) without explicit user request

## Notes
- End-user document-translation artifact authored as a Markdown SKILL.md; it shells out to a bundled Python script that calls the Equalang API, but its domain and deliverable (translated/transcribed documents) are end-user business content.
- Apache-2.0 license permits verbatim reproduction; the frontmatter also declares `license: Apache-2.0`.
- The skill depends on an external paid service and an API key, and it deliberately avoids pulling large file contents into the conversation (returns paths only).
- This case captures only the root `SKILL.md`; the repo also contains `scripts/equalang.py`, tests, and localized READMEs.
