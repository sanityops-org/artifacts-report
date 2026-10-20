# Comparative Analysis — Multi-LLM Defect Reports on TC-004

**Analyst-Output Meta-Review of Six LLM Inspection Reports**

| Field | Value |
|-------|-------|
| Target artifact | `TC-004-gpt-researcher-multi-agent-suite.md` (gpt-researcher `multi_agents/`, Apache-2.0) |
| Artifact type | Multi-Agent suite (8 roles × 3 artifact types) |
| Coverage of this analysis | 6 independent LLM inspection reports located in `report-onlybyLLM/` |
| Method | Manual extraction + cross-model consensus mapping |
| Analysis date | 2026-10-15 |
| Output language | English (per `.trae/rules.md`, Rule 1) |

> **Scope note.** This document is a *meta-analysis of six LLM reports*. It does not re-inspect the source artifact from scratch. Where a theme below is marked as a "consensus" finding, that means **six independent models converged on it**, which raises confidence that it is real; where a theme is found by only one model, it is a candidate finding that would need verification against the real `multi_agents/` source code.

---

## 1. The Six Reports Under Review

| # | Report file | Model | Items | P0 | P1 | P2 | Self-declared framing |
|---|-------------|-------|:-----:|:--:|:--:|:--:|------------------------|
| R1 | `Claude Fable 5.1.md` | Claude Fable 5.1 | **30** | 4 | 13 | 13 | N/A |
| R2 | `DeepSeek-V4-Pro.md` | DeepSeek-V4-Pro | **19** | 3 | 9 | 7 | N/A |
| R3 | `GLM-5.md` | GLM-5 | **25** | 5 | 14 | 6 | N/A |
| R4 | `GPT-5.6 Terra.md` | GPT-5.6 Terra | **16** | 2 | 9 | 5 | Explicit audit-boundary disclaimer |
| R5 | `Gemini 4 Argon.md` | Gemini 4 Argon | **15** | 5 | 6 | 4 | N/A |
| R6 | `sonnet-5.5.md` | sonnet-5.5 | **22** | 4 | 10 | 8 | Explicit limitations note |

All six follow the **same severity taxonomy** (P0 = blocking / must fix before release; P1 = high / fix before production; P2 = medium / iterative), which makes them directly comparable. Two models (R4, R6) explicitly state the artifact is a *documentation summary, not runnable source*, and caveat their findings accordingly.

---

## 2. Statistical Analysis

### 2.1 Volume Statistics

| Metric | P0 | P1 | P2 | Total |
|--------|:--:|:--:|:--:|:-----:|
| Sum across 6 reports | 23 | 61 | 43 | **127** |
| Mean per report | 3.83 | 10.17 | 7.17 | **21.17** |
| Median per report | 4.0 | 9.5 | 6.5 | 20.5 |
| Min (report) | 2 (R4) | 6 (R5) | 4 (R5) | 15 (R5) |
| Max (report) | 5 (R3/R5) | 14 (R3) | 13 (R1) | 30 (R1) |
| Std. deviation | 1.17 | 2.93 | 3.34 | **5.20** |

**Interpretation:** the total volume ranges 15→30 (a 2.0× spread) with a standard deviation of ~5 items. There is **no single "correct" count** — the spread reflects different interpretations of what counts as a distinct "issue" (granularity), not necessarily different discovery power. R1 (Claude) tends to split issues finely; R5 (Gemini) merges related root causes (e.g., both path issues folded into one P0).

### 2.2 Severity Distribution (Share of Each Report)

| Report | P0 share | P1 share | P2 share | Severity posture |
|--------|:--------:|:--------:|:--------:|------------------|
| R1 Claude Fable 5.1 | 13.3% | 43.3% | **43.3%** | Broad + detail-heavy (most P2) |
| R2 DeepSeek-V4-Pro | 15.8% | 47.4% | 36.8% | Balanced |
| R3 GLM-5 | 20.0% | **56.0%** | 24.0% | Security/ops weighted (most P1) |
| R4 GPT-5.6 Terra | 12.5% | **56.3%** | 31.3% | Conservative, low total |
| R5 Gemini 4 Argon | **33.3%** | 40.0% | 26.7% | Most severe-weighted |
| R6 sonnet-5.5 | 18.2% | 45.5% | 36.4% | Balanced |

**Interpretation:** R5 assigns the highest proportion of items to P0 (1 in 3), while R1 and R4 spread most findings into P1/P2 (more granular, lower average severity). R3 and R4 place emphasis on P1 (operational/compliance risk), R1 emphasises P2 (consistency/normative defects).

### 2.3 Category Distribution (where a report declares one)

Only three reports publish an explicit **defect / permission / explicit-risk** breakdown:

| Report | Defect | Permission | Explicit Risk | Notes |
|--------|:------:|:----------:|:-------------:|-------|
| R1 Claude Fable 5.1 | 14 | 8 | 8 | Sums to 30 (mutually exclusive) |
| R2 DeepSeek-V4-Pro | 11 | 3 | 5 | "Partially cross-classified" |
| R5 Gemini 4 Argon | 10 | 4 | 7 | Cross-attributes counted separately |
| R3, R4, R6 | — | — | — | Categories assigned per-item but no global tally |

**Interpretation:** across the three tabulations, **defects (contract/logic inconsistency) dominate at ~50%**, followed by explicit risks (~35%) and permissions (~15–20%). The models agree on the *shape* of the problem (mostly contract defects), even though they disagree on counts. R3 (GLM-5) frames nearly everything as risk/permission, making it the most security-leaning report.

---

## 3. Consensus, Divergence, and Blind Spots

### 3.1 Cross-Model Coverage Matrix

`✓` = the model raised the theme; `—` = not raised. Themes are normalized across models by root cause, so one model's single item may match another model's two.

| # | Issue theme | R1 Claude | R2 DeepSeek | R3 GLM-5 | R4 GPT | R5 Gemini | R6 sonnet | Coverage |
|---|-------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| T1 | Path traversal — `local_document_search.doc_path` has no whitelist/sandbox | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T2 | Arbitrary file write — `export_*` `filename`/`template` unrestricted | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T3 | HITL fail-open — Human node "default approval after 24h" | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T4 | Review↔Revise loop has no max iterations / circuit breaker | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T5 | Tool-name mismatch — Prompt tools vs Tool Schema disjoint | ✓ | ✓ | — | ✓ | ✓ | ✓ | 5/6 |
| T6 | Indirect prompt injection — untrusted web/local content | ✓ | — | ✓ | ✓ | ✓ | ✓ | 5/6 |
| T7 | Missing RBAC / role-to-tool authorization matrix | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T8 | Review contract inconsistency — score/format/naming | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |
| T9 | Concurrency — shared state fields lack reducers | ✓ | ✓ | ✓ | ✓ | ✓ | — | 5/6 |
| T10 | `current_phase` enum incomplete (no human/cancel/fail) | ✓ | ✓ | — | ✓ | ✓ | ✓ | 5/6 |
| T11 | Publisher claims HTML but no `export_html` | ✓ | ✓ | — | ✓ | ✓ | ✓ | 5/6 |
| T12 | Publication schema param-type defects (`"content": "string"`) | ✓ | — | — | — | ✓ | ✓ | 3/6 |
| T13 | Chief Editor super-role / responsibility overlap | ✓ | — | ✓ | — | ✓ | — | 3/6 |
| T14 | No rate limit / concurrency cap / token budget | — | — | ✓ | ✓ | — | ✓ | 3/6 |
| T15 | No audit log / observability | — | — | ✓ | ✓ | — | ✓ | 3/6 |
| T16 | Source credibility / hallucination / no fact-check | ✓ | ✓ | ✓ | — | — | ✓ | 4/6 |
| T17 | Export params missing (filename/metadata for pdf/docx) | ✓ | — | ✓ | — | ✓ | — | 3/6 |
| T18 | `web_search` params unbounded / API-key management | ✓ | ✓ | ✓ | — | — | ✓ | 4/6 |
| T19 | Config conflicts — sections/word-count vs `task.json`/stress | ✓ | ✓ | ✓ | — | ✓ | ✓ | 5/6 |
| T20 | Error handling / retry / degradation undefined | ✓ | ✓ | ✓ | — | — | ✓ | 4/6 |
| T21 | Human-node details undefined / unvalidated guidance injection | ✓ | — | ✓ | ✓ | ✓ | — | 4/6 |
| T22 | Citation format (APA/MLA) not globally enforced | ✓ | ✓ | — | — | — | — | 2/6 |
| T23 | State persistence — no encryption / desensitization / retention | ✓ | — | ✓ | ✓ | — | ✓ | 4/6 |
| T24 | Documentation fidelity — naming, miscount, blank rubric | ✓ | ✓ | — | — | — | ✓ | 3/6 |

### 3.2 The Unanimous Core (6/6) — Highest Confidence

Eight themes were found by **every** model. These are the strongest candidates for real, high-priority defects:

1. **T1 Path traversal** in `local_document_search.doc_path`.
2. **T2 Arbitrary file write** via `export_markdown.filename` / `export_docx.template`.
3. **T3 HITL fail-open** — "default approval after 24 hours" defeats human-in-the-loop.
4. **T4 Unbounded Review↔Revise loop** — no max iteration / termination condition.
5. **T7 Missing RBAC** — no enforced role-to-tool (and/or role-to-state-field) authorization.
6. **T8 Review-contract inconsistency** — `evaluate_draft` returns only `{score, feedback}`, while Reviewer's prompt expects `criteria_scores`/`gaps`/`approval_status`; criteria name `sources` vs `source_quality`; score type `int` vs `number`.
7. **(implied by all)** the underlying **three-layer contract drift** among *System Prompt ↔ Tool Schema ↔ State/Config* — the shared root cause behind T5, T8, T10, T11, T12, T17.

### 3.3 Contested Issues — Same Defect, Different Severity

The models disagree sharply on how severe several *agreed-upon* defects are. This is the most actionable signal, because it is not about discovery but about judgement.

| Issue | R1 Claude | R2 DeepSeek | R3 GLM-5 | R4 GPT | R5 Gemini | R6 sonnet | Split |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|-------|
| Path traversal (T1) | P0 | P0 | P0 | P0 | P0 | P0 | unanimous P0 |
| Arbitrary file write (T2) | P0 | P1 | P0 | P1 | P0 | P1 | **3 P0 / 3 P1** |
| HITL fail-open (T3) | P0 | P1 | P0 | P0 | P1 | P0 | **4 P0 / 2 P1** |
| Unbounded loop (T4) | P0 | P0 | P1 | P0 | P0 | P0 | **5 P0 / 1 P1** |
| Tool-name mismatch (T5) | P1 | P0 | — | P2 | P0 | P1 | **spread P0–P2** |
| Prompt injection (T6) | P1 | — | P0 | P1 | P0 | P0 | **spread P0–P1 + 1 miss** |
| Concurrency reducers (T9) | P1 | P1 | P1 | P1 | P0 | — | mostly P1 |
| Review contract (T8) | P1 | P1 | P2 | P2 | P1 | P1 | mostly P1 |

**Reading the divergence:**

- **Tool-name mismatch (T5)** is the single largest disagreement: R2 and R5 escalate it to **P0 (system cannot run at all)**, R4 downgrades it to **P2 (docs omission)** and R3 does not raise it. This is understandable — if the artifact is a *summary*, missing schema definitions may be a documentation gap (R4's view); if read literally as the spec, the agents call non-existent tools and the orchestrator fails (R2/R5's view).
- **Prompt injection (T6)** is the second-largest disagreement in coverage: five models flag it (two as P0), while **R2 (DeepSeek) omits it entirely** — the most notable blind spot in the set.
- **Arbitrary file write (T2)** splits neatly by whether the model treats *write* as equally dangerous as *read*: those focused on data exfiltration call it P0; those focused on the primary attack path call it P1.

### 3.4 Model-Specific Strengths & Blind Spots

| Model | Distinctive contribution (found by few others) | Notable blind spot / weakness |
|-------|-----------------------------------------------|-------------------------------|
| **R1 Claude Fable 5.1** | Copyright/licensing of embedded images; SSRF/LFI via `weasyprint`; third-party model data leakage (`sources.content` → `gpt-4o`); state bloat without dedup; documentation fidelity (`reviser.py` vs "Revisor"). Most granular. | Lowest P0 ratio; some items are stylistic/normative (P2 inflation). |
| **R2 DeepSeek-V4-Pro** | "Revisor has no retrieval tools" capability mismatch; identifies the 3-layer contract as the single source of truth to fix; notes the blank scoring rubric is a doc defect, correctly excluded from the 19. | **Missed prompt injection (T6)**; missed SSRF/XSS class. |
| **R3 GLM-5** | Broadest **security/ops** lens: no content-safety/DLP filter, API-key lifecycle, rate limiting, concurrency control, token budget, audit log, encrypted async state, metadata de-sensitization, source-degradation. Only model with a fix-timeline table. | Does not raise the tool-name mismatch (T5) or doc-fidelity (T24); lowest P2 share. |
| **R4 GPT-5.6 Terra** | Most disciplined method: explicit audit-boundary disclaimer; frames everything as "control seen in doc / not seen"; strongest on authorization-matrix and quality-gate closure. | Lowest volume (16); misses the whole ops cluster (T14/T15/T16) and config conflicts (T19). |
| **R5 Gemini 4 Argon** | Best root-cause consolidation (both path issues → one P0); highest P0 share; precise artifact-level cross-references; rich combined injection+SSRF+LFI+XSS analysis. | Merging lowers granularity; misses ops/audit themes (T14/T15) and citation (T22). |
| **R6 sonnet-5.5** | Plainest language; only model to explicitly self-limit ("no source code — could be summary omission"); flags doc self-consistency ("8 roles × 3 artifacts" miscount; blank rubric; best-practice contradiction). | Missed concurrency/reducers (T9), super-role overlap (T13), export-params (T17), unvalidated guidance (T21). |

---

## 4. Aggregate Quality Assessment of the Reports

| Dimension | Observation |
|-----------|-------------|
| **Structural consistency** | All 6 use P0/P1/P2 + a table with "issue / possible impact". Highly comparable. |
| **Evidence discipline** | R4 (best) and R6 explicitly caveat the doc-vs-source boundary; R1 and R5 show explicit re-check/re-verify passes. R3 asserts runtime risks more strongly on doc-only evidence. |
| **Root-cause depth** | R2, R5, R6 identify the *three-layer contract drift* as the shared root cause; R1 catalogs symptoms in more places but states the root cause less centrally. |
| **Security coverage** | R3, R5 strongest (injection, SSRF/XSS/LFI, DLP, keys, rate limits). R2 weakest (no injection). |
| **Consistency/quality coverage** | R1, R6 strongest (naming, citation format, doc fidelity, rubric). R3 weakest. |
| **Actionability** | R3 (fix-timeline table), R1 (priority "small changes, big coverage" note), R6 ("most urgent / most impactful" grouping) most actionable. |
| **Over-claiming risk** | R3 highest (many runtime assertions from text); R4 lowest. |

---

## 5. Synthesis — What All Six Models Jointly Establish

### 5.1 High-confidence defect set (agreed by ≥5/6)

> The artifact has a **broken three-layer contract** (System Prompt ↔ Tool Schema ↔ State/Config), plus **four unanimously-flagged blocking defects** and **an absent permission model**:
> - Path traversal (T1) · Arbitrary write (T2) · HITL fail-open (T3) · Unbounded revise loop (T4) · Missing RBAC (T7) · Review-contract mismatch (T8).

### 5.2 Recommended priority (reconciling all six)

| Priority | Action | Sourced from |
|----------|--------|--------------|
| **Must fix (blocking)** | Sandbox `local_document_search` (root allow-list + path normalization + `..` rejection); restrict `export_*` output to a fixed directory with extension allow-list. | T1, T2 (6/6) |
| **Must fix (blocking)** | Change Human timeout from **fail-open → fail-closed** (pause, not approve); require explicit human approval for publish when `include_human_feedback` is enabled. | T3 (4 P0 / 2 P1) |
| **Must fix (blocking)** | Add `max_iterations` / `revision_count` + fallback (escalate-to-human or accept-best) to the Review↔Revise loop. | T4 (5 P0 / 1 P1) |
| **High** | Pick the **Tool Schema as the single source of truth** and reverse-align all 8 prompts + state/config (tool names, score contract, phases, HTML export, param types). | T5, T8, T10, T11, T12, T17 |
| **High** | Introduce an explicit **role→tool authorization matrix** (RBAC/ACL) and, ideally, field-level state access rules. | T7 (6/6), T13 |
| **High** | Treat retrieved web/local content as **untrusted**: mark, sanitize, and separate instructions from data (anti-injection); sanitize Publisher HTML/images (anti-SSRF/XSS). | T6 (5/6), R3/R5 |
| **Medium** | Add observability & ops controls: audit log, rate limit, concurrency control, token/cost budget, encrypted & retention-bounded state. | T14, T15, T23, T9 |
| **Medium** | Resolve config conflicts (sections 3–5 vs `max_sections:3` vs stress `10`; 1500–2500 words vs 50+ pages) and enforce citation format globally. | T19, T22 |

### 5.3 Divergences that require verification against real source

The following depend on whether the artifact is read as *spec* or *summary*, and should be settled by checking `multi_agents/` source:

- **T5 tool-name mismatch** — real runtime failure (R2/R5, P0) or summary omission (R4, P2)?
- **T2 severity** — does the export tool actually write to a caller-controlled path?
- **T12 / T17** — are the published JSON schemas verbatim or condensed?

---

## 6. Conclusion

The six reports are **strongly convergent on the core**: eight themes were found by all six models, and the same four blocking defects recur everywhere. The reports diverge mainly on **granularity** (15–30 items), **severity calibration** (e.g., the tool-name mismatch spans P0→P2), and **breadth of the security lens** (GLM-5 and Gemini 4 are the most security-weighted; Claude Fable 5.1 and sonnet-5.5 are the most consistency-weighted; GPT-5.6 Terra is the most conservative; DeepSeek-V4-Pro has the one notable blind spot — prompt injection).

Because the artifact is a *documentation summary* rather than runnable source, the consensus findings (especially the six 5–6/6 themes) are the reliable core, while the single-model findings (T22, T13, T12, T17) are candidate issues to confirm against `multi_agents/` source before remediation.

> **Non-official-result statement:** This analysis is a meta-review produced by the host model over six prior LLM reports. It is **NOT** a conclusion of the official SanityOps engine. For a full, authoritative inspection use `sanityops-cli`.

---

## Appendix A — Per-Report Inventory (as declared by each report)

| Report | Total | P0 | P1 | P2 | Category tally | Extra artifacts |
|--------|:-----:|:--:|:--:|:--:|----------------|-----------------|
| Claude Fable 5.1 | 30 | 4 | 13 | 13 | Defect 14 / Permission 8 / Risk 8 | Re-check section (3 verified points) + priority note |
| DeepSeek-V4-Pro | 19 | 3 | 9 | 7 | Defect 11 / Permission 3 / Risk 5 | 3-point closing note (incl. rubric-blank exclusion) |
| GLM-5 | 25 | 5 | 14 | 6 | per-item only | Fix-priority timeline table |
| GPT-5.6 Terra | 16 | 2 | 9 | 5 | per-item only | Audit-boundary disclaimer + handling-order note |
| Gemini 4 Argon | 15 | 5 | 6 | 4 | Defect 10 / Permission 4 / Risk 7 | Artifact-level cross-references |
| sonnet-5.5 | 22 | 4 | 10 | 8 | per-item only | Overall conclusion + explicit limitations |

## Appendix B — Source Artifact Reference

All six reports target the same artifact: `TC-004-gpt-researcher-multi-agent-suite.md`
(8 System Prompts, 3 Tool Schemas — Research/Review/Publication, 2 config artifacts — `task.json` + `ResearchState`, plus evaluation dimensions and test suggestions).
