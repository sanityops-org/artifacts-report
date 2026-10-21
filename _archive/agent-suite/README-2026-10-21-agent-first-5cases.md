# agent-suite — Agent-First Artifact Extraction: Statistics

> Scope: **TC-247 to TC-251** — five production-embedded agents, collected on 2026-10-21.
> Unit of collection: **prompt component extracted verbatim from product code**.
> This report replaces the previous artifact-first statistics. The earlier report (51 cases, TC-004 to TC-107) and its case files are archived together under `_archive/agent-suite/` and are **not comparable** to this one; see Section 7.

---

## 1. Scope and Sampling Frame

The previous batch sampled **repositories that happened to publish artifacts as standalone files**. That frame produced mostly framework defaults, platform templates, and demos. This batch samples **production products that ship business logic in code**, then extracts the embedded prompt components.

Inclusion criteria for an agent:

1. Open-source with a clear license.
2. End-user or enterprise product with a concrete business loop (contract review, recipe import, bookmarking, office work, collaboration).
3. Prompts are **shipped by the product**, not written by the customer.
4. Prompts live in product code paths (`tasks/`, `services/`, `lib/`, `packages/`), not in `examples/`, `demo/`, or `samples/`.

Excluded candidates and the reasons are recorded in Section 8.

---

## 2. Counting Standard

A component is counted only if it is a **directly usable logic artifact** under the same three-type standard used by the corpus:

| Type | Requirement |
|---|---|
| **System Prompt** | A complete instruction unit that can be pasted as a system message: it states the task and carries its own constraints or output contract. |
| **Skill** | `SKILL.md` with `name` and `description` frontmatter and complete body. |
| **Tool Schema** | A single tool definition in OpenAI, Anthropic, or MCP JSON structure with `type: object`, `properties`, and `required`. |

Judgement rules:

- **Template variables are acceptable**: `{var}`, `${var}`, `{{.Var}}`, `%1$s`, and f-string placeholders are treated as runtime inputs, not missing text.
- **Role is satisfied by an explicit persona sentence or by a task statement that fully fixes the actor.** Example: `Parse ingredient strings into components.` is treated as a complete task, not a fragment.
- **Composition is not acceptable**: a file whose content is only `{{template "..."}}` includes, or that must be concatenated with another file before it becomes an instruction, is not counted. This mirrors the previous rule that `...` truncation is not a runnable artifact: the text is not self-contained at load time.
- **Fragments are not counted**: prefixes, list constraints, style instructions, formatting fragments, and one-line image prompts.
- **Non-LLM prompts are not counted**: text-to-image prompts are out of scope for all three types.
- Line ranges, placeholders, and Python/PHP/Go/TypeScript wrappers are documented per artifact in the TC files. The statistics below count **content**, not the wrapper.

Two reason codes are used for non-counted components:

- **C — composition dependency**: include-only or concatenation-required.
- **G — generic fragment**: prefix, list constraint, style instruction, or partial rule.
- **N — non-text-LLM prompt**: image-generation prompt or other non-system-prompt instruction.

---

## 3. Overall Results

| Metric | Value |
|---|---:|
| Agents | **5** |
| Prompt components extracted | **44** |
| **Directly usable artifacts** | **26** |
| — System Prompt | 26 |
| — Skill | 0 |
| — Tool Schema | 0 |
| Agents with at least one usable artifact | 5 (100%) |
| Components not counted | 18 |
| Component-level usable rate | 59.1% |
| Average components per agent | 8.8 |
| Average usable artifacts per agent | 5.2 |

**Sensitivity.** If an explicit persona sentence is required literally, six task-only prompts drop out and the count becomes **20**. The 26 figure uses the functional rule stated in Section 2; both figures are reported so the criterion is auditable.

---

## 4. Per-Case Results

| Case | Project | Business scenario | Extracted | Usable | Not counted | Yield |
|---|---|---|---:|---:|---:|---:|
| [TC-247](TC-247-opencontracts-agent-suite.md) | JSv4/OpenContracts | Legal contract review | 10 | **9** | 1 | 90.0% |
| [TC-248](TC-248-mealie-agent-suite.md) | mealie-recipes/mealie | Recipe import and normalization | 7 | **7** | 0 | 100.0% |
| [TC-249](TC-249-karakeep-agent-suite.md) | karakeep-app/karakeep | Bookmark tagging and summary | 7 | **4** | 3 | 57.1% |
| [TC-250](TC-250-nextcloud-assistant-agent-suite.md) | nextcloud/assistant | Enterprise productivity assistant | 6 | **3** | 3 | 50.0% |
| [TC-251](TC-251-mattermost-agents-agent-suite.md) | mattermost/mattermost-plugin-agents | Enterprise collaboration / ChatOps | 14 | **3** | 11 | 21.4% |
| **Total** | | | **44** | **26** | **18** | **59.1%** |

No case contains a Skill or a Tool Schema.

---

## 5. Why 18 Components Are Not Counted

| Reason | Count | Cases |
|---|---:|---|
| **C — composition dependency** | 12 | TC-251 ×11, TC-247 ×1 |
| **G — generic fragment** | 5 | TC-249 ×3, TC-250 ×2 |
| **N — non-text-LLM prompt** | 1 | TC-250 ×1 |
| **Total** | **18** | |

Notable example: eleven of the fourteen Mattermost components are complete task instructions, but each begins with `{{template "standard_personality.tmpl" .}}` and several also include `citation_format.tmpl`. After rendering they are production system prompts; as files they are not loadable. They are therefore counted as **composition-dependent**, not as defects or missing prompts.

---

## 6. Component-Level Appendix

`R` = counted as a directly usable artifact. `C`, `G`, `N` = not counted, per Section 2.

### TC-247 OpenContracts (9 / 10)

| # | Component | Type | Result |
|---|---|---|---|
| 1 | Agentic Contract Highlighter System Directive | System Prompt | R |
| 2 | PII / Confidential-Data Highlighter Prompt | Template | R |
| 3 | Legal Citation Extraction Instructions | System Prompt | R |
| 4 | Document Corpus Action Agent System Prompt | System Prompt | R |
| 5 | Thread Corpus Action Agent System Prompt | System Prompt | R |
| 6 | Memory Curator System Prompt | System Prompt | R |
| 7 | CAML Writer Mission | Sub-prompt | C |
| 8 | Authority-Text Locator Instructions | System Prompt | R |
| 9 | Default Seeded Agent System Instructions | Template | R |
| 10 | Corpus Branding System Prompt | System Prompt | R |

### TC-248 Mealie (7 / 7)

| # | Component | Type | Result |
|---|---|---|---|
| 1 | build-recipe | Task Prompt | R |
| 2 | parse-recipe-ingredients | Task Prompt | R |
| 3 | parse-recipe-video | Task Prompt | R |
| 4 | resolve-organizers | Task Prompt | R |
| 5 | translate-recipe | Task Prompt | R |
| 6 | compile-source | System Prompt | R |
| 7 | transcribe-audio | System Prompt | R |

### TC-249 Karakeep (4 / 7)

| # | Component | Type | Result |
|---|---|---|---|
| 1 | Image Tagging Prompt | Prompt Builder | R |
| 2 | Text Tagging Prompt | Prompt Builder | R |
| 3 | Summary Prompt | Prompt Builder | R |
| 4 | OCR Extraction Prompt | System Prompt | R |
| 5 | Tag Style Instruction | Prompt Builder | G |
| 6 | Curated Tags Instruction | Prompt Builder | G |
| 7 | Potential Relevant Tags Instruction | Prompt Builder | G |

### TC-250 Nextcloud Assistant (3 / 6)

| # | Component | Type | Result |
|---|---|---|---|
| 1 | Chat session system prompt (`CHAT_USER_INSTRUCTIONS`) | System Prompt | R |
| 2 | Conversation title generation prompt | System Prompt | R |
| 3 | Session summary prompt | Task Prompt | R |
| 4 | Raw chat history memory prefix | Prefix | G |
| 5 | Outdated summary memory prefix | Prefix | G |
| 6 | Sticker generation prompt template | Image prompt | N |

### TC-251 Mattermost Agents (3 / 14)

| # | Component | Type | Result |
|---|---|---|---|
| 1 | Standard Personality (composite) | System Prompt | C |
| 2 | Thread Summarization System Prompt | System Prompt | C |
| 3 | Channel Summarization System Prompt | System Prompt | C |
| 4 | Channel Unread Summary System Prompt | System Prompt | C |
| 5 | Channel Range Summary System Prompt | System Prompt | C |
| 6 | Meeting Transcript Chunk Summary System Prompt | System Prompt | C |
| 7 | Meeting Summary System Prompt | System Prompt | R |
| 8 | Meeting Summary General Rules Fragment | System Prompt (fragment) | C |
| 9 | Action Item Extraction System Prompt | System Prompt | C |
| 10 | Open Question Extraction System Prompt | System Prompt | C |
| 11 | Search System Prompt | System Prompt | C |
| 12 | Emoji Selection System Prompt | System Prompt | R |
| 13 | Direct Message Question System Prompt | System Prompt | C |
| 14 | Standard Personality Without Locale (locale-free variant) | System Prompt | R |

---

## 7. Comparability with the Archived Report

| Dimension | Archived report | This report |
|---|---|---|
| Sampling frame | Repositories publishing standalone artifacts | Production products with embedded business prompts |
| Unit | One artifact as found in the test case | One prompt component extracted from product code |
| Cases | 51 | 5 |
| Usable artifacts | 74 | 26 |
| Cases with at least one usable artifact | 27 (52.9%) | 5 (100%) |
| Tool Schema usable | 0 | 0 |

The two reports must not be pooled. The archived 52.9% describes **artifact publication behaviour** in a repository sample; the 100% here describes **artifact presence** in products selected for shipping business prompts. The 0 Tool Schema result is, however, consistent across both frames and is the strongest cross-frame finding.

---

## 8. Findings

1. **Composition, not content, is the dominant reason a production prompt is not a usable artifact.** 12 of 18 non-counted components are complete instructions that only fail because they are assembled from includes. Static inspection of "the artifact" therefore requires a rendering step, or must target components rather than composed prompts.

2. **Architectural maturity and standalone rate are inversely related in this sample.** Mealie ships flat `.txt` files and scores 7/7; Mattermost ships a 20-file Go template library with tool gating, locale fragments, and conditional sections and scores 3/14. Modularization improves maintainability and testability but destroys per-file loadability and auditability. This is a testable hypothesis for a larger sample.

3. **Tool contracts remain invisible.** No agent exposes a usable tool schema, consistent with the archived report. Tools are Python signatures, Go structs, PHP task definitions, or MCP servers, none of which is a schema document in the artifact sense.

4. **Business prompts are task-specific, not role-playing.** The usable artifacts name concrete entities: contract, citation, annotation; recipe, ingredient, unit; bookmark, tag; channel, thread, meeting. Generic "helpful assistant" prompts appear only as platform defaults (excluded candidates).

5. **Licensing skew.** Three of five agents are AGPL-3.0, one MIT, one Apache-2.0. Verbatim quoting is permitted with attribution; the two AGPL prompt bodies and the Apache-2.0 template library should be attributed in the paper's appendix.

---

## 9. Provenance and Verification

| Case | Commit | License | Clone (read-only) |
|---|---|---|---|
| TC-247 | `8bc8254d0c03efcf3cdb7b383a675016fcb51351` | MIT | `_archive/_clones/opencontracts` |
| TC-248 | `9f9ef5f0bb594a7ebdcfb6365aa6e2de97496713` | AGPL-3.0 | `_archive/_clones/mealie` |
| TC-249 | `5c72fa95807df2d7dd96f0c9ac52a536b5bf3cfc` | AGPL-3.0 | `_archive/_clones/karakeep` |
| TC-250 | `0911bc12c9443c96574fe7cca0c030266c7e6cc2` | AGPL-3.0 | `_archive/_clones/nc-assistant` |
| TC-251 | `d3fcf323fe3e33ce6d52b1b4f70e2d824897a1d3` | Apache-2.0 | `_archive/_clones/mm-agents` |

- All clones were shallow (`--depth 1`) and verified clean after extraction.
- Each quoted block was compared character-by-character against its source literal or file. Mealie 7/7, Karakeep 7/7, Nextcloud 6/6, and Mattermost 14/14 passed exact comparison; OpenContracts blocks preserve Python f-string and `str.format` placeholders verbatim.
- No source repository was modified.

---

## 10. Limitations

1. **Five agents, one domain each.** No domain has more than one agent, so domain effects cannot be separated from project effects.
2. **OpenContracts blocks retain Python literal wrappers** for f-string artifacts. They are verbatim but not directly pasteable until normalized; this is recorded per artifact in TC-247.
3. **Adoption evidence is partial.** Deployment paths were confirmed for Mealie (`docker:prod`), Mattermost (`make deploy`, e2e), and Nextcloud (official app); OpenContracts and Karakeep deployment evidence still needs verification.
4. **No Skill and no Tool Schema** in this batch, so two of the three artifact types remain unrepresented.
5. **Business domains still missing**: healthcare, recruiting, insurance, e-commerce, tax/finance, and logistics. The five agents cover legal, food, knowledge management, office productivity, and collaboration.
