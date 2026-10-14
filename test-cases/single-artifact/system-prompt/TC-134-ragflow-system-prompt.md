# TC-134: RAGFlow - System Prompt Evaluation Case

## Metadata
- **Source Project**: infiniflow/ragflow
- **License**: Apache-2.0
- **Artifact Type**: System Prompt (RAG answer pipeline prompt template; multilingual batch-translation system prompt)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `internal/rag/prompts/cross_languages_sys_prompt.md`
  - Prompt is loaded by `internal/rag/prompts/templates.go` (embedded via `//go:embed`)
  - Repository confirmed at `https://github.com/infiniflow/ragflow`

## Original Artifact Content

The multilingual system prompt (`cross_languages_sys_prompt.md`) is embedded by the RAG answer pipeline and is reproduced verbatim below.

```markdown
## Role
A streamlined multilingual translator.

## Behavior Rules
1. Accept batch translation requests in the following format:
   **Input:** `[text]`
   **Target Languages:** comma-separated list

2. Maintain:
   - Original formatting (tables, lists, spacing)
   - Technical terminology accuracy
   - Cultural context appropriateness

3. Output translations in the following format:

[Translation in language1]
===
[Translation in language2]

---

## Example

**Input:**
Hello World! Let's discuss AI safety.
===
Chinese, French, Japanese

**Output:**
你好世界！让我们讨论人工智能安全问题。
===
Bonjour le monde ! Parlons de la sécurité de l'IA.
===
こんにちは世界！AIの安全性について話し合いましょう。
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The role ("a streamlined multilingual translator") is stated in one line
- [ ] Scope is limited to batch translation of an input `[text]` into a target language list
- [ ] Output is confined to translations only (no commentary)

### 2. Input/Output Format Determinism
- [ ] The input format (`**Input:**` / **Target Languages:**) is specified
- [ ] The output separator (`===`) between translations is fixed
- [ ] A worked example pins the exact input/output shape

### 3. Fidelity Requirements
- [ ] Original formatting (tables, lists, spacing) must be preserved
- [ ] Technical terminology accuracy is required
- [ ] Cultural context appropriateness is required

### 4. Multilingual Behavior
- [ ] Order of outputs must match the order of the requested target-language list
- [ ] Multiple target languages are handled in a single response

### 5. Testability
- [ ] The `===`-delimited output can be split and counted against the number of requested languages
- [ ] Formatting preservation (tables/lists) is diff-checkable against the input
- [ ] The worked example provides a golden reference for regression

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 15% | | |
| Input/Output Format Determinism | 30% | | |
| Fidelity Requirements | 25% | | |
| Multilingual Behavior | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide an input table with two comma-separated target languages; verify two `===`-separated translations are returned with the table structure intact.
2. Provide the worked example verbatim; verify output ordering matches (Chinese, French, Japanese).
3. Translate text containing technical terminology; verify domain terms are accurate and untranslated where appropriate.

### Boundary Test Cases
1. Request a single target language; verify exactly one translation block (no trailing `===`).
2. Provide input with mixed lists and spacing; verify preservation.
3. Provide text with culturally sensitive content; verify localized rendering.

### Negative Test Cases
1. Ask the translator to answer a question instead of translating; verify it stays in the translator role.
2. Attempt to inject extra output sections (e.g., commentary); verify only translation blocks are emitted.
3. Provide an unknown/unparseable language name; verify it does not silently drop the language slot.

## Notes
- RAGFlow is an open-source RAG engine used for enterprise document Q&A and agent workflows; the `internal/rag/prompts/` templates (e.g., `citation_prompt.md`, `keyword_prompt.md`, `related_question.md`, `ask_summary.md`) drive an end-user document-analysis experience.
- The repository also ships downloadable agent templates under `internal/agent/templates/` (e.g., `trip_planner.json`, `seo_article_writer.json`, `text2sql_data_expert.json`); this case captures the multilingual answer-pipeline system prompt only.
- Apache-2.0 license (per `infiniflow/ragflow`; the prompt file carries the Apache-2.0 header via `templates.go`), which permits verbatim quotation.
