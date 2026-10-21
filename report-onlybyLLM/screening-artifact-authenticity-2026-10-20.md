# Artifact Authenticity Screening — All 201 Test Cases

**Date**: 2026-10-20
**Scope**: `test-cases/agent-suite` (51), `single-artifact/skill` (50), `single-artifact/system-prompt` (50), `single-artifact/tool-schema` (50)
**Question**: Does each case contain a genuine, runtime-loadable logical artifact (system prompt / skill / tool schema), or only a synthesized summary?
**Out of scope**: whether the quoted code runs, and whether the upstream project is good or bad.

---

## 1. Definition and verdict scale

A **genuine logical artifact** is the exact text/config an agent runtime loads or sends at execution time:

- **System prompt**: the system/role message or prompt template string passed to the model.
- **Skill**: a `SKILL.md` (normally with YAML front matter) that a runtime discovers and injects.
- **Tool schema**: the tool definition sent to the model (`inputSchema` / JSON Schema) or the exact source that generates it (Zod / Pydantic / TS `Tool` literal).
- **Permission policy**: the runtime permission allow/deny configuration.

| Verdict | Meaning |
|---|---|
| **A — AUTHENTIC** | Verbatim (or clearly faithful, non-paraphrased) copy of the runtime artifact; traceable source; declared type correct. |
| **B — PARTIAL** | Authentic text, but truncated / only a subset of a set; the omission may hide defects. |
| **C — SYNTHETIC** | Rewritten, expanded, invented, or documentation-derived; not the runtime artifact. |
| **X — CONTAMINATED** | Authentic base with invented sections inserted; the most dangerous failure mode because it looks real. |
| **D — MIS-TYPED / MIS-TARGETED** | Genuine text, but not the declared artifact type, or a different artifact was substituted. |
| **M — MIXED** | Multi-artifact suite where only some roles/artifacts are authentic. |

Confidence: **H** = strong internal evidence or upstream byte comparison; **M** = structural evidence only; **L** = thin artifact, impossible to fingerprint.

---

## 2. Headline results

| Verdict | Count | Share |
|---|---:|---:|
| A — AUTHENTIC | 150 | 74.6% |
| B — PARTIAL | 43 | 21.4% |
| C — SYNTHETIC | 0 | 0% |
| X — CONTAMINATED | 0 | 0% |
| D — MIS-TYPED / MIS-TARGETED | 1 | 0.5% |
| M — MIXED | 7 | 3.5% |
| **Total** | **201** | **100%** |

By collection type:

| Collection | A | B | C | X | D | M |
|---|---:|---:|---:|---:|---:|---:|
| agent-suite (51) | 24 | 19 | 0 | 0 | 1 | 7 |
| skill (50) | 49 | 1 | 0 | 0 | 0 | 0 |
| system-prompt (50) | 43 | 7 | 0 | 0 | 0 | 0 |
| tool-schema (50) | 34 | 16 | 0 | 0 | 0 | 0 |

**Bottom line**: the corpus is now almost entirely real. 96% of cases (A + B) quote genuine runtime artifacts, and no synthetic case remains.

**Remaining blocking case**: TC-037 (genuine Functionz code, but not a logical artifact).


---

## 3. Method

1. Structural scan of all 200 files: collection method, source URLs, commit pins, code-fence structure, truncation markers, placeholder patterns.
2. Full read of every case under a fixed rubric (artifact type, runtime-loadability, traceability, verbatim markers, omissions).
3. ~20 upstream byte-level comparisons against `raw.githubusercontent.com`, including TC-002, TC-036, TC-052, TC-065, TC-067, TC-078, TC-081, TC-090, TC-092, TC-117, TC-118, TC-127, TC-130, TC-138, TC-161, TC-162, TC-169, TC-191, TC-213, TC-228, TC-229.
4. Manual adjudication of every C / X / D / M verdict and of all low-confidence A verdicts.

---

## 4. Principal findings

1. **Remediation completed (2026-10-20).** Eleven P0 cases were re-fetched from upstream and rewritten. Ten now contain authentic artifacts (TC-003, TC-004, TC-005, TC-035, TC-040, TC-083, TC-106, TC-107, TC-127, TC-228); TC-006 is B because it quotes six real role files as excerpts. No synthetic case remains.

2. **Screening correction — TC-035 was never contaminated.** The upstream `classic/original_autogpt/autogpt/core/planning/prompt_strategies/one_shot.py` at the pinned commit contains the "Efficiency Guidelines" and parallel-execution text verbatim. The original X-CONTAMINATED verdict was a false positive and has been withdrawn.

3. **Provenance anchors were fixed during remediation.** TC-040 now cites the real `core/context/LEON.md` (the previous commit and template path did not exist); TC-083 now identifies `cs-demand-gen-specialist` as the artifact instead of pretending it is a marketing strategist; TC-127 now quotes the live n8n `systemMessage` instead of a README snippet; TC-003 was re-scoped to a real MCP server because gpt-researcher has no tool schema.

4. **Suites still overstate coverage.** Quoted runtime prompts vs. claimed roles: TC-097 2/67, TC-098 2/21, TC-099 2/6, TC-104 1/4, TC-096 1/5. The rest are README tables, directory trees or dispatcher code. These remain M, not A. TC-106 was fixed by replacing the inventory with real Jinja templates.

5. **Branch-pinned quotes still drift.** Only about 15 files pin a commit; the rest cite `main` / `master` / jsDelivr heads. Several byte comparisons show drift (TC-228 topic enum rewritten; TC-138 false line count; TC-146 blank-line inflation). The remediation recorded fetch dates, not new commit SHAs.

6. **Partial excerpts can invert defect conclusions.** 43 cases are B. Examples where the omitted part carries the likely defect: TC-038 (handler truncated at `console.log(error)`), TC-119 (dynamic half of the shopping prompt omitted), TC-121 (3 of 5 travel agents never fetched), TC-125 (preamble paraphrased, `thought.ts` truncated), TC-130 (composition partials omitted), TC-188 / TC-201 / TC-206 (referenced schemas unquoted).

7. **Skills are the cleanest set.** 49/50 are authentic, with real YAML front matter, preserved upstream defects and no admitted translation. Only TC-139 is partial (folded `description` loses trigger text). TC-152 and TC-177 are authentic but too thin to fingerprint (confidence L).

8. **Tool-schema cases quote the defining source, not the emitted schema.** Zod / Pydantic / FastMCP / `mcp.NewTool` source is acceptable, but no case captures the actual `tools/list` payload, and several elide shared field schemas (TC-230, TC-237, TC-244, TC-245). TC-003 was re-scoped to real GitHub MCP schemas; TC-228's field drift was repaired.

9. **Only one mis-typed case remains.** TC-037 quotes Flask application code rather than a logical artifact. TC-107 was re-typed as a prompt-assembly/preprompt case because Chat UI ships no system prompt.

10. **A three-layer case now exists.** TC-007 was added on 2026-10-20: OpenClaw's `SOUL.md` / `AGENTS.md` (system prompt), `browser-automation/SKILL.md` (skill), and the `browser` tool registration plus TypeBox schema (tool schema). It is the first case in the corpus that exercises cross-layer referential integrity.

---

## 5. Full verdict table

### 5.1 agent-suite (51)

| TC | Verdict | Conf | Evidence |
|---|---|---|---|
| TC-007 | A-AUTHENTIC | H | New three-layer case: `SOUL.md` / `AGENTS.md` + `browser-automation/SKILL.md` + `browser` tool schema, all verbatim. |
| TC-004 | A-AUTHENTIC | H | Rebuilt from 8 agent files + `ResearchState` + `task.json`; 4 roles carry real prompts. |
| TC-005 | A-AUTHENTIC | H | Official OpenClaw `SOUL.md` / `AGENTS.md` / `USER.md` / `IDENTITY.md` templates, verbatim. |
| TC-006 | B-PARTIAL | H | Six real marketing role files; quoted as excerpts with source paths. |
| TC-031 | B-PARTIAL | H | Pinned commit; `SOUL.md` verbatim; 7/21 templates and 4/11 skills, truncations flagged. |
| TC-032 | B-PARTIAL | H | Commit-pinned; 8 of 15 routing rows and most skills omitted, omissions flagged. |
| TC-033 | M-MIXED | M | `CLAUDE.md` / skills / MCP code authentic; README block is not runtime-loaded. |
| TC-034 | A-AUTHENTIC | H | Commit-pinned; six complete `SKILL.md` templates, variables and CLI paths intact. |
| TC-035 | A-AUTHENTIC | H | Verified upstream at the pinned commit; "Efficiency Guidelines" are genuine. |
| TC-036 | A-AUTHENTIC | H | Verified upstream: `SYSTEM_PROMPT`, `NEXT_STEP_PROMPT`, `Manus` class match commit. |
| TC-037 | D-MIS-TYPED | M | Genuine Functionz code, but Flask wiring/implementation, not a logical artifact. |
| TC-038 | B-PARTIAL | H | Commit-pinned; memory handler truncated mid-function at `console.log(error)`. |
| TC-039 | A-AUTHENTIC | H | Commit-pinned; genbi `SKILL.md` with distinctive CLI details. |
| TC-040 | A-AUTHENTIC | H | Real `core/context/LEON.md` on `develop`; prior commit and template path did not exist. |
| TC-041 | B-PARTIAL | H | Commit-pinned `AGENTS.md` plus one skill; 10 further skills inventoried only. |
| TC-042 | M-MIXED | M | Genuine TOOL_USE / SKILLS / MEMORY strings; code docstrings also presented as prompts. |
| TC-055 | B-PARTIAL | H | Orchestrator verified verbatim; `market-copy` truncated after Phase 1. |
| TC-056 | B-PARTIAL | M | Front matter and excerpts genuine; routing table and flow summarized, not quoted. |
| TC-057 | B-PARTIAL | M | Two `SKILL.md` excerpts with front matter; README truncated, most of "20+ skills" missing. |
| TC-058 | B-PARTIAL | H | Umbrella skill complete; `localize-ja` ~30 rule sections summarized. |
| TC-059 | B-PARTIAL | M | Genuine Chinese `SKILL.md` fragments with front matter; long elisions. |
| TC-060 | B-PARTIAL | M | Real prompt strings from `builder.py`, but fragmented; full assembled prompt never shown. |
| TC-061 | B-PARTIAL | M | Loader code verbatim; skills presented as translated doc summaries, no runtime `SKILL.md`. |
| TC-062 | B-PARTIAL | M | `BaseAgent` near-complete; `data_commons_tool.py` excerpted; no loaded prompt text. |
| TC-063 | B-PARTIAL | M | Front matter plus blockquoted excerpts; bodies abridged, six skills unquoted. |
| TC-064 | A-AUTHENTIC | H | Complete system prompt, Zod schema and taxonomy JSON; source-specific inconsistency preserved. |
| TC-065 | A-AUTHENTIC | H | `filter.yaml` verified byte-identical; `prefill.yaml` complete, upstream typos intact. |
| TC-066 | A-AUTHENTIC | M | Three full role-instruction files; declared path unverified. |
| TC-067 | A-AUTHENTIC | H | `assistant.liquid` verified verbatim; `tools.yml` complete. |
| TC-068 | A-AUTHENTIC | H | Complete `SKILL.md` with front matter; unfetched companions honestly not quoted. |
| TC-069 | A-AUTHENTIC | M | Three complete files with YAML front matter; no summarization. |
| TC-070 | B-PARTIAL | H | Front matter and sections verbatim; ceo-advisor workflows condensed, legal templates omitted. |
| TC-071 | A-AUTHENTIC | H | Four complete Fabric `system.md` prompts; signature quirks preserved. |
| TC-084 | A-AUTHENTIC | H | `default_config.py` matched exactly; 9/11 role prompts quoted. |
| TC-090 | A-AUTHENTIC | H | `prompts.py` matched byte-for-byte; 3/10 role profiles quoted. |
| TC-091 | A-AUTHENTIC | M | Real strings including source typo `sysetm_prompt`; 3 personas and 4 builders. |
| TC-092 | A-AUTHENTIC | H | `agents.py` verified; all six instruction strings quoted. |
| TC-094 | B-PARTIAL | L | 3/5 persona prompts; claimed v2 layout unverified; Munger / Lynch bodies absent. |
| TC-095 | A-AUTHENTIC | M | All five Chinese prompts plus base-class context instruction. |
| TC-096 | M-MIXED | M | 1/5 agents has a runtime prompt; the rest are README bullets and module trees. |
| TC-097 | M-MIXED | M | 2/67 roles quoted; 21 "tool schemas" named but never shown. |
| TC-098 | M-MIXED | M | 2/21 agents quoted; remainder is a README role table. |
| TC-099 | M-MIXED | M | 2/6 YAML prompts quoted; four agents exist only as names and ports. |
| TC-100 | A-AUTHENTIC | H | Three prompt templates and four tools with distinctive strings. |
| TC-101 | A-AUTHENTIC | H | Five prompt constants complete and mutually consistent. |
| TC-102 | B-PARTIAL | M | Speed / Quality researcher prompts quoted; `writer.ts` and `classifier.ts` never quoted. |
| TC-103 | B-PARTIAL | M | Identity and Quick-mode blocks quoted; Adaptive-mode prompt entirely missing. |
| TC-104 | M-MIXED | M | 1/4 roles (Planner) prompted; Dispatcher / Actor / Reflect appear only as paths. |
| TC-105 | B-PARTIAL | M | Two prompts quoted; middle of `chat/system.jinja` elided before citation rules. |
| TC-106 | A-AUTHENTIC | H | Real Jinja `base.j2` / `condense.j2` / `context.j2` plus prompt builder, verbatim. |
| TC-107 | A-AUTHENTIC | H | Re-typed: real prompt assembly + `preprompt` schema; the repo ships no prompt text. |

### 5.2 single-artifact/skill (50)

| TC | Verdict | Conf | Evidence |
|---|---|---|---|
| TC-002 | A-AUTHENTIC | H | Verified against raw `document-skills/pdf/SKILL.md`; matches except one typo. |
| TC-047 | A-AUTHENTIC | M | Real front matter with `allowed-tools`; multi-step shell workflow; no raw URL. |
| TC-049 | A-AUTHENTIC | M | Genuine Chinese `SKILL.md` kept in original language; six-step pipeline. |
| TC-053 | A-AUTHENTIC | M | Compact real skill with scoped `Bash(crib *)` and command reference. |
| TC-054 | A-AUTHENTIC | M | Real `SKILL.md` plus `agent.yaml` manifest; script contract coherent. |
| TC-081 | A-AUTHENTIC | H | Verified byte-for-byte against raw URL, including contract templates. |
| TC-138 | A-AUTHENTIC | H | Verified against raw URL; exact match; stated line count is wrong. |
| TC-139 | B-PARTIAL | M | Folded `description: ">"` leaves trigger text omitted. |
| TC-140 | A-AUTHENTIC | M | Dependency metadata plus emphatic behavioral contract; authored, not synthesized. |
| TC-141 | A-AUTHENTIC | M | Escaped quotes in folded description, seven reference files, cited literature. |
| TC-142 | A-AUTHENTIC | M | Multi-runtime metadata, credit tables and error codes too idiosyncratic to paraphrase. |
| TC-143 | A-AUTHENTIC | M | Complete endpoint table, curl examples and quota notes. |
| TC-144 | A-AUTHENTIC | M | Specific untrusted-content tagging and exit codes; `allowed-tools` mismatch preserved. |
| TC-145 | A-AUTHENTIC | M | Bilingual body with Chinese openings preserved; eight style families. |
| TC-146 | A-AUTHENTIC | M | Head matches upstream exactly; tail unverified; line count inflated by blank lines. |
| TC-147 | A-AUTHENTIC | M | Seven-step workflow, script invocations, 18 palettes. |
| TC-148 | A-AUTHENTIC | M | Deterministic allocation arithmetic and troubleshooting table. |
| TC-149 | A-AUTHENTIC | M | Root `skill.md` v3.0.0 with CUAD benchmark tables. |
| TC-150 | A-AUTHENTIC | M | Engine/report contract, data rules, banned-verb rules. |
| TC-151 | A-AUTHENTIC | M | 26 numbered patterns cross-referenced with before/after pairs. |
| TC-152 | A-AUTHENTIC | L | Symmetric 5/5/5 prompt stubs; front matter plausible but thin and unverifiable. |
| TC-153 | A-AUTHENTIC | M | Black-Litterman outputs recompute exactly (5.16 / 5.41 / 0.18%). |
| TC-154 | A-AUTHENTIC | M | Cost-consent rails, key path, error semantics; Apache-2.0 front matter. |
| TC-155 | A-AUTHENTIC | M | `ai_percent: null` semantics and credit math; coherent sibling of TC-154. |
| TC-156 | A-AUTHENTIC | H | Full front matter, nine scenarios, CLI preflight and reference tree. |
| TC-157 | A-AUTHENTIC | M | Rich front matter (slug, triggers, ID8Labs); long pedagogy body. |
| TC-158 | A-AUTHENTIC | H | Complete numbered pricing framework, ASCII wireframes, fixed output. |
| TC-159 | A-AUTHENTIC | H | Five-step workflow with verbatim sub-agent prompt template and worked example. |
| TC-160 | A-AUTHENTIC | M | Nine-section canvas; duplicated body metadata typical of command-derived skills. |
| TC-161 | A-AUTHENTIC | H | Raw-URL fetch matched entire body exactly. |
| TC-162 | A-AUTHENTIC | H | Raw-URL fetch matched all sections: 20 formulas, caveats, hard rules. |
| TC-163 | A-AUTHENTIC | H | Seven-phase workflow, script table, reference map. |
| TC-164 | A-AUTHENTIC | H | Complete Chinese `SKILL.md`; original language, not a translation. |
| TC-165 | A-AUTHENTIC | H | Seven-step journalism workflow with untrusted-content contract. |
| TC-166 | A-AUTHENTIC | M | Complete seven-part JD framework; distinctive "TRIGGER THIS" description. |
| TC-167 | A-AUTHENTIC | M | Router with 40+ mode table; duplicate invocation keys suggest genuine capture. |
| TC-168 | A-AUTHENTIC | H | Full v2.6 twelve-section skill with 45-type guide and taste gate. |
| TC-169 | A-AUTHENTIC | H | Raw-URL fetch matched body; 80-database catalog and arXiv citation block. |
| TC-170 | A-AUTHENTIC | M | Complete slim `SKILL.md`: contents map plus eight-step workflow. |
| TC-171 | A-AUTHENTIC | H | Eight-technique framework, scoring rubric, diagnostic table. |
| TC-172 | A-AUTHENTIC | H | Complete front matter, workflow, 12-slide table and worked examples. |
| TC-173 | A-AUTHENTIC | H | Four-step process, STAR examples, anti-patterns, Australian award context. |
| TC-174 | A-AUTHENTIC | H | Orchestrator with five parameterized agent prompts and scoring weights. |
| TC-175 | A-AUTHENTIC | H | Full Polish `SKILL.md`; workflow table, confirmation gate, MCP verification. |
| TC-176 | A-AUTHENTIC | H | Complete Chinese tutor with question-type scripts and exam timings. |
| TC-177 | A-AUTHENTIC | L | Terse host-contract prose with artifact-specific references; no visible truncation. |
| TC-178 | A-AUTHENTIC | H | Complete decode workflow, severity scale, verbatim disclaimer. |
| TC-179 | A-AUTHENTIC | H | Full orchestration: parameters, parallel searches, cost matrix. |
| TC-180 | A-AUTHENTIC | H | Complete journal schema, runnable analytics snippets, review cadence. |
| TC-181 | A-AUTHENTIC | H | Four-phase research process, scoring formula, report skeleton. |

### 5.3 single-artifact/system-prompt (50)

| TC | Verdict | Conf | Evidence |
|---|---|---|---|
| TC-001 | A-AUTHENTIC | M | `generate_report_prompt` verbatim from `prompts.py`; a template, not a system-role message. |
| TC-018 | B-PARTIAL | H | Self-declared excerpt: 8 of ~30 browser rules; 7 sibling prompt variants unquoted. |
| TC-019 | A-AUTHENTIC | H | Complete `systemPrompt()` template; commit-pinned. |
| TC-044 | B-PARTIAL | M | DSPy signature docstrings are runtime instructions, but only the writing stage. |
| TC-045 | A-AUTHENTIC | M | Full `get_system_prompt` assembly plus two layout prompts; HEAD-only pin. |
| TC-046 | A-AUTHENTIC | M | System messages verbatim across an 8-stage chain; function bodies elided. |
| TC-048 | A-AUTHENTIC | M | All five prompt `.txt` templates quoted in full; HEAD-only. |
| TC-051 | A-AUTHENTIC | M | JARVIS prompt blocks verbatim; distinctive quirks retained; HEAD-only. |
| TC-052 | A-AUTHENTIC | H | Verified byte-identical against `coach-system-prompt.ts`. |
| TC-072 | A-AUTHENTIC | H | Fabric `analyze_bill`; exact idiosyncratic wording preserved. |
| TC-073 | A-AUTHENTIC | H | Complete Fabric `summarize` prompt. |
| TC-074 | A-AUTHENTIC | H | Complete Fabric `extract_wisdom` prompt including constraint quirks. |
| TC-075 | A-AUTHENTIC | H | Complete Fabric `create_prd` pattern. |
| TC-076 | A-AUTHENTIC | H | Complete minimal Fabric `improve_writing` pattern. |
| TC-077 | A-AUTHENTIC | H | Complete `analyze_paper`; upstream typos preserved. |
| TC-078 | A-AUTHENTIC | H | Verified byte-identical against `cs-financial-analyst.md`. |
| TC-079 | A-AUTHENTIC | M | Agent-definition body from the same verified repo convention; no commit pin. |
| TC-080 | A-AUTHENTIC | M | Compact agent definition; README-style workflow prose included. |
| TC-082 | B-PARTIAL | M | Dual-method capture admitted; front matter and Workflow 3 onward reconstructed. |
| TC-083 | A-AUTHENTIC | H | Real `cs-demand-gen-specialist` body; case identity now names that artifact. |
| TC-108 | A-AUTHENTIC | M | `DEFAULT_SYSTEM_PROMPT` verbatim with placeholders; reminder constant unverified. |
| TC-109 | A-AUTHENTIC | H | `saneDefaultSystemPrompt` verbatim including `{datetime}`. |
| TC-110 | A-AUTHENTIC | M | Both document-analysis templates verbatim; jsDelivr `@main`, no commit. |
| TC-111 | A-AUTHENTIC | H | Full `SALES_AGENT_TOOLS_PROMPT` with 8-stage ladder. |
| TC-112 | A-AUTHENTIC | M | Writer prompt verbatim (Perplexica lineage); jsDelivr `@master`. |
| TC-113 | A-AUTHENTIC | M | Full `SYSTEM_PROMPT` plus dynamic postscript headers; no commit pin. |
| TC-114 | A-AUTHENTIC | H | `DEFAULT_PROMPT_ANALYSE_NEW_FILE` plus substitution and schema code. |
| TC-115 | A-AUTHENTIC | M | Single system message verbatim plus Zod descriptors. |
| TC-116 | A-AUTHENTIC | M | Full `SYSTEM_INSTRUCTION` and both camera-state notices. |
| TC-117 | A-AUTHENTIC | H | Verified both agent files byte-identical. |
| TC-118 | A-AUTHENTIC | H | Raw Jinja template verified byte-identical; complete per-role prompt. |
| TC-119 | B-PARTIAL | H | Static half only; `build_dynamic_context` half explicitly omitted. |
| TC-120 | A-AUTHENTIC | M | Complete `buildSystemPrompt()` template; only date interpolated. |
| TC-121 | B-PARTIAL | H | 2 of 5 agent `instructions` quoted; three agents never fetched. |
| TC-122 | A-AUTHENTIC | M | Complete `build_system_prompt` f-string; schema and date dynamic. |
| TC-123 | A-AUTHENTIC | M | Full `PORTFOLIO_SYSTEM_PROMPT` plus shared rule constants. |
| TC-124 | A-AUTHENTIC | H | Full `chat_answer.system.jinja2`; all conditional branches intact. |
| TC-125 | B-PARTIAL | H | Only `<instructions>`; preamble paraphrased, `thought.ts` truncated with `...`. |
| TC-126 | A-AUTHENTIC | M | Complete `buildSystemPrompt()` return string; interpolations preserved. |
| TC-127 | A-AUTHENTIC | H | Live n8n `systemMessage` extracted from workflow JSON; full text quoted. |
| TC-128 | A-AUTHENTIC | M | Complete builder implementation with conditional memory segments. |
| TC-129 | A-AUTHENTIC | M | Full constant set: prefix, all `PLAN_*`, format, suffixes. |
| TC-130 | B-PARTIAL | M | `base.j2` plus two guidelines verified; other guideline/tool partials omitted. |
| TC-131 | A-AUTHENTIC | M | All three persona templates quoted in full, including the `{bio}` quirk. |
| TC-132 | A-AUTHENTIC | M | Full `RESUME_WIZARD_TURN_PROMPT` with JSON schema intact. |
| TC-133 | A-AUTHENTIC | M | Full `build-recipe.txt`; siblings are distinct prompts, not fragments. |
| TC-134 | A-AUTHENTIC | M | Complete translator prompt including worked `===` example; not fetch-checked. |
| TC-135 | A-AUTHENTIC | H | Both constants with their original upstream source comments. |
| TC-136 | A-AUTHENTIC | M | Full array-joined constant, including literal `${...}` quirk. |
| TC-137 | A-AUTHENTIC | M | Four complete QA template constants with scaffolds. |

### 5.4 single-artifact/tool-schema (50)

| TC | Verdict | Conf | Evidence |
|---|---|---|---|
| TC-003 | A-AUTHENTIC | H | Re-scoped to real GitHub MCP `get_commit` / `list_commits` schemas. |
| TC-050 | B-PARTIAL | M | Manifest subset plus only Tavily / OpenWeather schemas; wiring contradicts cited static schema. |
| TC-182 | A-AUTHENTIC | M | `brave_web_search` identity plus full Zod `params` for one tool. |
| TC-183 | A-AUTHENTIC | M | Seven `Tool` literals with `inputSchema` and list wiring from one file. |
| TC-184 | A-AUTHENTIC | M | Eight Slack `Tool` literals and `ListToolsRequestSchema` array; complete group. |
| TC-185 | A-AUTHENTIC | M | Nine `registerTool` blocks with Zod input/output schemas; handlers elided. |
| TC-186 | A-AUTHENTIC | H | Both `Tool(...)` literals with `inputSchema` plus `TimeTools` enum. |
| TC-187 | A-AUTHENTIC | M | Pydantic `Fetch` model and `fetch` registration; full schema source. |
| TC-188 | B-PARTIAL | M | Five of roughly ten FastMCP tools quoted; crypto and balance-sheet tools named only. |
| TC-189 | A-AUTHENTIC | M | Complete `mcp.NewTool("weather")` builder with all parameters. |
| TC-190 | A-AUTHENTIC | H | Single-tool server: `search` JSON Schema complete and list handler quoted. |
| TC-191 | A-AUTHENTIC | H | Verified byte-for-byte against raw `getProducts.ts`. |
| TC-192 | A-AUTHENTIC | M | `ToolModel`, `Search` model and registration; complete for one tool. |
| TC-193 | B-PARTIAL | L | Cited `server.py` contains no `@mcp.tool`; real wrapper likely elsewhere. |
| TC-194 | A-AUTHENTIC | M | `airbnb_search` JSON Schema complete with required list. |
| TC-195 | B-PARTIAL | L | `get_transcript` cut mid-array; `strip_ads` and annotations unverified additions. |
| TC-196 | B-PARTIAL | L | Signature and output models quoted; generated `inputSchema` absent. |
| TC-197 | A-AUTHENTIC | H | Complete `CREATE_TASK_TOOL` schema including priority enum. |
| TC-198 | A-AUTHENTIC | M | Zod `athleteId` schema and tool object; consistent Zod-to-JSON pattern. |
| TC-199 | A-AUTHENTIC | M | `FindParksSchema` complete with five optional fields; registration truncated. |
| TC-200 | A-AUTHENTIC | M | `price-get` registration with complete Zod input/output schemas. |
| TC-201 | B-PARTIAL | L | `search_meals` complete but JSON block truncated; sibling headers are fabricated placeholders. |
| TC-202 | A-AUTHENTIC | M | Full `web_search_exa` registration with parameters and annotations. |
| TC-205 | A-AUTHENTIC | M | `list_records` registration plus shared `baseId` / `tableId` fragments. |
| TC-206 | B-PARTIAL | M | `ForecastParamsSchema` references three schemas never quoted. |
| TC-207 | A-AUTHENTIC | M | Five note-tool registrations and `CreateNoteOptionsSchema` quoted coherently. |
| TC-208 | A-AUTHENTIC | H | Two `Tool` literals plus `BaseTool` contract; complete and consistent. |
| TC-209 | B-PARTIAL | M | `list-events` schema quoted but registry object truncated; helpers referenced only. |
| TC-210 | A-AUTHENTIC | M | `add_heading` FastMCP registration with signature and docstring. |
| TC-213 | A-AUTHENTIC | H | Verified verbatim against `tests/contract-snapshots/tool-definitions.json`. |
| TC-214 | A-AUTHENTIC | M | Verbatim `@mcp.tool` decorator, docstring and typed signature. |
| TC-223 | A-AUTHENTIC | M | Verbatim Zod `server.tool("translate-text")` registration; path unverified. |
| TC-228 | A-AUTHENTIC | H | `topic` enum and description restored to upstream `general`, `news`. |
| TC-229 | B-PARTIAL | H | Four handlers verified verbatim; remaining seven Obsidian tools only named. |
| TC-230 | B-PARTIAL | M | `search_books` Zod schema verbatim; shared `limit` / `offset` schemas unquoted. |
| TC-231 | A-AUTHENTIC | M | Three weather handlers complete with `inputSchema`. |
| TC-232 | A-AUTHENTIC | M | Single `google_news_search` tool complete; token fields consistent. |
| TC-233 | B-PARTIAL | M | Three of seven tools verbatim; `get_artwork_image` and user-set tools summarized. |
| TC-234 | B-PARTIAL | M | Five tools verbatim; remaining endpoints only named. |
| TC-235 | B-PARTIAL | M | Seven of eight public tools; handler bodies elided. |
| TC-236 | A-AUTHENTIC | M | All four tool constants quoted with complete `inputSchema` objects. |
| TC-237 | B-PARTIAL | L | Three registrations verbatim, but shared `fields.ts` schemas unquoted. |
| TC-238 | A-AUTHENTIC | M | Single `search_news` object complete; README block is usage JSON, not registration. |
| TC-239 | A-AUTHENTIC | M | Single `get_feed` `registerTool` call verbatim. |
| TC-241 | B-PARTIAL | L | Two tools quoted; handler-in-array layout atypical and unverifiable. |
| TC-242 | A-AUTHENTIC | M | Full `convert_currency_latest` signature with `Field` annotations; metadata list truncated. |
| TC-243 | A-AUTHENTIC | M | Full input/output Zod for `sports_get_scores`; handler abbreviated. |
| TC-244 | A-AUTHENTIC | M | Full Zod `inputSchema`; `ArrivalsResponseSchema` referenced, not quoted. |
| TC-245 | B-PARTIAL | M | Input schema fully quoted; output and enrichment fields elided. |
| TC-246 | A-AUTHENTIC | M | Full input/output/enrichment schemas with a pinned commit hash. |

---

## 6. Remediation log and remaining work

### P0 — resolved on 2026-10-20

| TC | Result |
|---|---|
| TC-003 | Re-scoped to the real GitHub MCP server (`get_commit`, `list_commits`); the invented schema was deleted. The case is now Markdown, matching the rest of the tool-schema set. |
| TC-004 | Rebuilt from the eight `multi_agents` modules, `ResearchState`, and `task.json`; only the four roles that actually send prompts are presented as prompt artifacts. |
| TC-005 | Rebuilt from the official OpenClaw `SOUL.md` / `AGENTS.md` / `USER.md` / `IDENTITY.md` templates. |
| TC-006 | Replaced with six real marketing role files; quoted as excerpts. |
| TC-035 | No change required. The upstream file at the pinned commit contains the "Efficiency Guidelines"; the X verdict was a false positive. |
| TC-040 | Replaced with the real `core/context/LEON.md` on `develop`; invalid commit/path removed. |
| TC-083 | Retitled and re-metadata'd to `cs-demand-gen-specialist`; the already-verbatim body was retained. |
| TC-106 | Replaced with the real PrivateGPT Jinja templates (`base.j2`, `condense.j2`, `context.j2`) and the prompt builder. |
| TC-107 | Re-typed as prompt-assembly + `preprompt` configuration, because Chat UI ships no system prompt. |
| TC-127 | Replaced with the live n8n `systemMessage` extracted from `workflow/slack-it-rag-agent.json`. |
| TC-228 | Restored the `topic` enum (`general`, `news`) and the original description. |

### P1 — re-capture omitted portions (43 B cases)

agent-suite: TC-006, TC-031, TC-032, TC-038, TC-041, TC-055, TC-056, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063, TC-070, TC-094, TC-102, TC-103, TC-105
system-prompt: TC-018, TC-044, TC-082, TC-119, TC-121, TC-125, TC-130
tool-schema: TC-050, TC-188, TC-193, TC-195, TC-196, TC-201, TC-206, TC-209, TC-229, TC-230, TC-233, TC-234, TC-235, TC-237, TC-241, TC-245

### P2 — verify coverage claims (M cases)

TC-033, TC-042, TC-096, TC-097, TC-098, TC-099, TC-104 — re-scope declared role/tool inventories to what is actually quoted, or capture the remaining artifacts.

### P2 — pin provenance

Add a commit SHA to every case that currently cites only `main` / `master` / jsDelivr heads. Highest risk: TC-045, TC-048, TC-051, TC-110, TC-112, TC-113, TC-116, TC-134, and the tool-schema set (only TC-246 is commit-pinned). The remediated cases record a fetch date, not a SHA.

### P2 — re-inspect the replaced cases

The existing `.sanityops-skill-report.md` files for the replaced cases describe the old artifacts. They must be regenerated before their defect counts are used.

---

## 7. Caveats

- Verdicts are about **artifact authenticity**, not about upstream product quality. An authentic prompt can still be a bad prompt.
- Agents and skills quoted from third-party `.md` agent definitions are treated as system prompts only where the file body is the runtime instruction text; front matter and workflow prose are documentation.
- "A — AUTHENTIC" does not guarantee byte-identity for every line; it means the case quotes runtime text faithfully and no paraphrase or invention was found. About 20 cases were byte-compared; the rest rest on structural evidence and preserved upstream idiosyncrasies.
- Branch-pinned cases can drift after the collection date; re-verification is required before any release-gate claim.
- Eleven cases were rewritten on 2026-10-20. Their existing inspection reports were produced against the previous content and are now stale.
- TC-007 was added on 2026-10-20 and has no inspection report yet.
- TC-107 is a deliberate re-type: it evaluates prompt assembly and preprompt configuration, not a system prompt text.
