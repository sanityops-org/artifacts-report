# TC-058: i18nstack - File-Based Multi-Logical-Artifact Agent Suite

## Metadata
- **Source Project**: i18n-agent/i18nstack
- **GitHub**: github.com/i18n-agent/i18nstack
- **License**: MIT
- **Artifact Type**: File-based logical artifacts (Markdown `SKILL.md` suite; one skill per language)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub fetch, branch `HEAD` (default branch):
  - `https://raw.githubusercontent.com/i18n-agent/i18nstack/HEAD/localize-ja/SKILL.md`
  - `https://raw.githubusercontent.com/i18n-agent/i18nstack/HEAD/i18nstack/SKILL.md` (umbrella skill)
  - `https://raw.githubusercontent.com/i18n-agent/i18nstack/HEAD/README.md`
  - Note: `.../HEAD/SKILL.md` (repo-root) **could not be fetched** — per the README, the root `SKILL.md` is a `setup`-generated, git-ignored entrypoint that points to `i18nstack/SKILL.md`. The real umbrella skill therefore lives at `i18nstack/SKILL.md`.

---

## Project Overview

i18nstack turns an AI coding agent into a **full localization team**: a format engineer, a QA tester, a release gate, and **46 native-quality translators**. It is a **non-coding, localization/content Agent** expressed almost entirely as Markdown `SKILL.md` files — one per target language — plus a small number of workflow skills and three globally-installed CLI tools.

The README's one-line pitch:

> **i18nstack turns AI coding agents into a full localization team: format engineer, QA tester, release gate, and 46 native-quality translators.**

### Key Features
- **One skill per language**: each `localize-XX` directory is a standalone skill distilled from production translation prompts.
- **Native-writer rules**: skills enforce formality registers, particle selection, plural systems, script conventions, and false-friend avoidance.
- **Umbrella routing skill**: `i18nstack/SKILL.md` routes any i18n task to the right tool or `localize-XX` skill.
- **CLI companions**: `i18n-convert` (32 formats), `i18n-pseudo` (QA pseudo-translation), `i18n-validate` (release gate).
- **Domain**: internationalization, translation, localization, content QA. Non-code (though CLI tools install globally).

---

## Logical Artifact Inventory

### Skill Inventory (as stated in the fetched umbrella skill and README)

Routing / tool skills (in `i18nstack/SKILL.md`):

| Task | Use |
|------|-----|
| Convert a localization file to another format | `i18n-convert` CLI (see `i18n-convert` skill) |
| Generate pseudo-translations to test an i18n setup | `i18n-pseudo` CLI (see `i18n-pseudo` skill) |
| Check translation files for missing keys, placeholder drift, plural errors | `i18n-validate` CLI (see `i18n-validate` skill) |
| Translate text into language XX with native-quality rules | `localize-XX` skill (46 languages, e.g. `localize-ja`, `localize-de`) |
| Wrap hardcoded strings in code with i18n functions | `i18n-wrap` skill |
| Audit existing i18n wrapping for quality issues | `i18n-review` skill |
| Validate AND fix all findings until green | `i18n-validate-workflow` skill |
| Safe format conversion with data-loss checks | `i18n-convert-workflow` skill |
| Pseudo-locale QA sweep with fix-up | `i18n-pseudo-workflow` skill |

Translation skills — **46 languages** (verbatim from the umbrella skill and README):

```text
ar bg bn ca cs cy da de el es et fa fi fr ga he hi hr hu id is it ja ko lt lv
ms mt nl no pl pt ro ru sk sl sr sv sw th tl tr uk ur vi zh
```

Expanded: Arabic (ar), Bulgarian (bg), Bengali (bn), Catalan (ca), Czech (cs), Welsh (cy), Danish (da), German (de), Greek (el), Spanish (es), Estonian (et), Persian (fa), Finnish (fi), French (fr), Irish (ga), Hebrew (he), Hindi (hi), Croatian (hr), Hungarian (hu), Indonesian (id), Icelandic (is), Italian (it), Japanese (ja), Korean (ko), Lithuanian (lt), Latvian (lv), Malay (ms), Maltese (mt), Dutch (nl), Norwegian (no), Polish (pl), Portuguese (pt), Romanian (ro), Russian (ru), Slovak (sk), Slovenian (sl), Serbian (sr), Swedish (sv), Swahili (sw), Thai (th), Tagalog (tl), Turkish (tr), Ukrainian (uk), Urdu (ur), Vietnamese (vi), Chinese (zh).

Distribution note (README): the suite ships **55 skills total** installable via `skills.sh` (`npx skills add i18n-agent/i18nstack -g -y`).

### Artifact 1: `i18nstack/SKILL.md` - Umbrella Skill (verbatim)

```markdown
---
name: i18nstack
description: |
  Complete i18n/localization toolkit for AI coding agents. Use when doing ANY
  internationalization work: converting localization files between 32 formats
  (i18n-convert), pseudo-translating files to QA an i18n implementation
  (i18n-pseudo), validating translation files for missing keys / placeholder
  drift / plural errors (i18n-validate), or translating UI strings, marketing
  copy, and docs into 46 languages with native-quality rules (localize-*).
allowed-tools:
  - Bash
  - Read
---
# i18nstack: the i18n toolkit for AI coding agents
Three CLI tools + 46 language-specific translation skills. Route any i18n task
to the right piece:
| Task | Use |
|------|-----|
| Convert a localization file to another format | `i18n-convert` CLI (see `i18n-convert` skill) |
| Generate pseudo-translations to test an i18n setup | `i18n-pseudo` CLI (see `i18n-pseudo` skill) |
| Check translation files for missing keys, placeholder drift, plural errors | `i18n-validate` CLI (see `i18n-validate` skill) |
| Translate text into language XX with native-quality rules | `localize-XX` skill (46 languages, e.g. `localize-ja`, `localize-de`) |
| Wrap hardcoded strings in code with i18n functions | `i18n-wrap` skill |
| Audit existing i18n wrapping for quality issues | `i18n-review` skill |
| Validate AND fix all findings until green | `i18n-validate-workflow` skill |
| Safe format conversion with data-loss checks | `i18n-convert-workflow` skill |
| Pseudo-locale QA sweep with fix-up | `i18n-pseudo-workflow` skill |
## Setup check (run BEFORE using any CLI)
```bash
for t in i18n-convert i18n-pseudo i18n-validate; do command -v $t >/dev/null || echo "MISSING: $t"; done
```
If anything is missing:
```bash
npm install -g @i18n-agent/i18n-convert @i18n-agent/i18n-pseudo @i18n-agent/i18n-validate
```
Or run full agent wiring: `npx skills add i18n-agent/i18nstack -g -y --skill '*'` then `./setup`.
## Recommended workflow (new locale end to end)
1. **Convert** the source file into the target project's format if needed:
   `i18n-convert en.json --to android-xml -o strings.xml`
2. **Pseudo-translate** before paying for real translations to catch hardcoded
   strings, overflow, and encoding bugs:
   `i18n-pseudo en.json --preset layout -o pseudo/`
3. **Translate** using the matching `localize-XX` skill — it enforces
   native-writer rules (formality, particles, plurals, script conventions).
4. **Validate** the result before shipping:
   `i18n-validate ./locales --strict`
## Available localize skills (46)
ar bg bn ca cs cy da de el es et fa fi fr ga he hi hr hu id is it ja ko lt lv
ms mt nl no pl pt ro ru sk sl sr sv sw th tl tr uk ur vi zh
Each is a standalone skill (`localize-ja`, `localize-de`, …) distilled from
production translation prompts — invoke the one matching your target language.
```

### Artifact 2: `localize-ja/SKILL.md` - Japanese Translation Skill (verbatim excerpt)

```markdown
---
name: localize-ja
description: Use when translating or localizing UI strings, marketing copy, documentation, or any source text into Japanese (ja). Enforces keigo consistency, SOV restructuring, full-width punctuation, particle/measure-word accuracy, and removes English calques so output reads like native Japanese.
---
# Japanese Translation Rules (ja / 日本語)
Distilled from the production translation prompts. Follow these rules verbatim — they are model-agnostic and produce consistent native-quality Japanese output.
## Mindset
> あなたは日本語ネイティブの厳格な作家で、英語からの直訳や不自然な日本語表現を嫌います。
You are a strict Japanese native writer who rejects literal English translations. Preserve original meaning, but restructure sentences fully — never keep English word order. Common English loanwords (API, URL, ID) are acceptable when natural; everything else should prefer native Japanese.
## Pre-Translation Setup
Before translating, lock in:
1. **Formality level (keigo)** — Default to **丁寧語 (teineigo)**: です/ます. Never mix with casual or imperatives.
2. **Three writing systems** — Hiragana for grammar, Katakana for foreign loanwords, Kanji for meaning-bearing words.
3. **Word order** — Japanese is SOV (Subject-Object-Verb). Restructure ALL English SVO sentences.
4. **Pro-drop language** — Drop あなた / 私 / subject pronouns when context is clear.
5. **Placeholders** — Preserve `{variables}` and ICU plural syntax exactly.
## Register Auto-Detection (run after Pre-Translation Setup, before translating)
If the user has NOT explicitly specified the formality level, infer it from the source text register. ...
### Worked examples
| Source | Detected register | Japanese output style |
|----------------|-------------------|-----------------------|
| "Please review the terms of service before proceeding." | formal | お手続きを進める前に、利用規約をご確認ください。 |
| "Hey! Tap here to get started — it's super quick 🚀" | informal | こんにちは！ここをタップして始めましょう。すぐに完了します 🚀 |
| "Submit your application by the deadline." | formal (no contractions, directive) | 期限までに申請書を提出してください。 |
| "Don't forget to save your work!" | informal (contraction + exclamation) | 作業内容を保存するのを忘れずに！ |
...
## Critical Accuracy Rules (NEVER violate)
### 1. Word vs Character — completely different meanings
| English | Wrong | Correct |
|---------|-------|---------|
| word count | 文字数 | **単語数** |
| character count | 単語数 | **文字数** |
...
```

The `localize-ja` skill continues with sections on FOR vs PER, measurement-unit words, temporal expressions, placeholder type markers, particles (助詞), measure words (助数詞), IT domain terminology, UI conventions (buttons, status, completion, empty states, drag-and-drop, validation), keigo consistency, full-width punctuation, spacing, native-vs-loanword preferences, honorific prefixes (お/ご), false friends (和製英語), calques, compound adjectives/nouns, spatial metaphors, temporal similes, polysemy, proper nouns, name suffixes (敬称), question phrasing, cultural conventions, and number/date formatting.

---

## Evaluation Dimensions (file-based artifacts specific)

### 1. One-Skill-Per-Language Symmetry
- [ ] Every target language is a standalone `localize-XX` skill directory
- [ ] Naming is uniform and machine-derivable from the ISO language code
- [ ] The umbrella skill enumerates the full language set

### 2. Markdown Structure & Frontmatter
- [ ] Valid YAML frontmatter (`name`, `description`)
- [ ] `description` states the trigger ("Use when translating ... into Japanese")
- [ ] Rules are organized as tables and imperative lists (verbatim-followable)

### 3. Rule Specificity (Native-Quality Encoding)
- [ ] Concrete wrong-vs-correct pairs, not general advice
- [ ] Register/keigo policy is explicit with a "no mixing" rule
- [ ] Placeholder/plural safety rules are stated (do not break `{variables}` / ICU)

### 4. Routing & Composition
- [ ] The umbrella skill routes tasks to the right tool/skill
- [ ] A documented end-to-end workflow (convert → pseudo → translate → validate)
- [ ] Localize skills are independent and invoke the correct one per language

### 5. Distribution & Auditability
- [ ] All language logic is plain Markdown, diffable and reviewable
- [ ] Skills are installable individually or as a set
- [ ] Behavior is inspectable without executing hidden code

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| One-Skill-Per-Language Symmetry | 25% | | |
| Markdown Structure & Frontmatter | 20% | | |
| Rule Specificity (Native-Quality Encoding) | 25% | | |
| Routing & Composition | 15% | | |
| Distribution & Auditability | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Configuration Validation Tests
1. **Inventory parity**: confirm the 46 ISO codes listed in the umbrella skill each have a corresponding `localize-XX/SKILL.md`.
2. **Frontmatter validation**: verify every `localize-XX` skill declares `name` and a trigger-bearing `description`.
3. **Umbrella routing**: check each task row in `i18nstack/SKILL.md` resolves to a real skill or documented CLI.

### Behavioral Tests
1. **Register auto-detection**: feed formal and informal English sources to `localize-ja` and confirm the output register matches (and never mixes).
2. **Placeholder safety**: translate strings containing `{variables}` and ICU plural syntax and confirm they are preserved exactly.
3. **False-friend handling**: translate "mansion" / "smart" and confirm the skill does not emit マンション / スマート for the English meanings.

### Output Tests
1. **End-to-end workflow**: run convert → pseudo → translate → validate and confirm each stage's artifact is produced.
2. **Unit accuracy**: verify `{days}日後` is used (not `{days}日中`) and that `{n}s/m/h/d` become explicit 秒/分/時間/日.
3. **Punctuation/formatting**: confirm full-width punctuation and correct date/number formatting in the Japanese output.

---

## Notes

- The repository is **MIT**.
- This is a **file-based, non-coding localization Agent suite** whose defining trait is **symmetry**: 46 language skills of the same shape, fronted by one routing umbrella.
- **Fetch caveat (recorded per the task's rules)**: `https://raw.githubusercontent.com/i18n-agent/i18nstack/HEAD/SKILL.md` (repo-root) **could not be fetched**. The README explains the root `SKILL.md` is a `setup`-generated, git-ignored entrypoint pointing to `i18nstack/SKILL.md`; the actual umbrella skill at `i18nstack/SKILL.md` was fetched successfully and is quoted above. No content was fabricated for the missing root path.
- The three global CLI tools (`i18n-convert`, `i18n-pseudo`, `i18n-validate`) are separate npm packages, not Markdown; the *skill definitions* that drive them are Markdown.
- All quoted content was fetched from raw GitHub URLs on branch `HEAD`.
