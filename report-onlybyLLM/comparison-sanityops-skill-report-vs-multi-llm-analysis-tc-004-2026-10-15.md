# Comparative Analysis — SanityOps Skill Report vs. Multi-LLM Analysis (TC-004)

**Cross-Comparison of an Official Rule-Package Inspection against Six Free-Form LLM Audits**

| Field | Value |
|-------|-------|
| Target artifact | `TC-004-gpt-researcher-multi-agent-suite.md` (gpt-researcher `multi_agents/`, Apache-2.0) |
| Document A | `test-cases/agent-suite/TC-004-gpt-researcher-multi-agent-suite.sanityops-skill-report.md` (SanityOps Inspect Lite v1.0.0) |
| Document B | `report-onlybyLLM/comparison-multi-llm-analysis-tc-004-2026-10-15.md` (meta-analysis of 6 LLM reports) |
| Analysis date | 2026-10-15 |
| Output language | English (per `.trae/rules.md`, Rule 1) |

---

## 1. Purpose

This report compares **two families of inspection output produced from the same source artifact**:

- **A — Official rule-package inspection.** A deterministic, rule-ID-driven static inspection (`sanityops-inspect-lite`), with fixed PASS/FAIL verdicts, staged execution (A/B/C/D/E/F/G), tier scoping (L1/L2/L3), and an explicit separation of *Inspect / Risk / Quality* conclusions.
- **B — Free-form LLM audits.** Six independent narrative audits (Claude Fable 5.1, DeepSeek-V4-Pro, GLM-5, GPT-5.6 Terra, Gemini 4 Argon, sonnet-5.5), each producing a P0/P1/P2 defect list, consolidated in the prior meta-analysis.

The goal is to determine **(1) where they agree, (2) where they diverge, and (3) whether they are competing or complementary.**

> **Non-official-result statement:** This analysis is produced by the host model. Document A is a *skill-package* result (not the official SanityOps engine). This document is not a SanityOps engine conclusion. For a full authoritative inspection use `sanityops-cli`.

---

## 2. Methodological Contrast (the root of every downstream difference)

| Dimension | A — SanityOps Skill Report | B — Multi-LLM Analysis (6 reports) |
|-----------|----------------------------|------------------------------------|
| Output unit | Rule ID + PASS/FAIL/N/A + one-line evidence citation | Narrative "issue" with severity + impact |
| Ruleset | Fixed, enumerated (`QD-P-*`, `QD-T-*`, `QD-PT-*`, `QD-CYC-*`, `QC-*`) | None; each model defines its own issue list |
| Determinism | High (same ruleset ⇒ reproducible) | Low (issue set and severity vary by model) |
| Severity model | Rule-tier severity, with Agent-L3 upgrade (P1→P0, P2→P1) | Analyst judgement, per item |
| Scope control | Strict: config artifacts (`task.json`, `ResearchState`) treated as *out-of-type*, QC-scope only | Broad: config, state, ops, security all in scope |
| Conclusion discipline | **Refuses** to state security/quality conclusions; Inspect ≠ Risk ≠ Quality | Freely states security conclusions (path traversal, injection, SSRF) |
| Stages | 7 defined; **A, B, C, E, F, G executed; D not run** (Gate-0 G0-4 unmet) | Single narrative pass per model; 2 of 6 explicitly caveat "doc ≠ source" |
| Risk audit | Stage E (Risk Explicit) executed → **0 items** | Risk is the dominant concern (path traversal, injection, SSRF, DLP) |
| Tiering | System-prompt set = L3 (47 items); research_tools = **L1 read-only**; publication_tools = L2 | No tiering; every tool judged on its own merits |

**Key structural fact:** Document A assigns `research_tools` to **L1 (read-only)** and therefore applies only a 7-item minimal rule set that contains **no path-safety rule**. Document B treats the same tool's `doc_path` as the single most dangerous surface. This one scoping decision explains the largest coverage gap between the two documents (see §4, theme T1).

---

## 3. Quantitative Comparison

### 3.1 Finding Volume and Severity

| Metric | A — Skill Report | B — 6 LLM reports (aggregate) |
|--------|:----------------:|:-----------------------------:|
| Total findings | **53** (Stage A+B FAILs) | 127 (mean **21.2** / report; range 15–30) |
| P0 | **37** (69.8%) | 23 (mean 3.83 / report) |
| P1 | **11** (20.8%) | 61 (mean 10.17 / report) |
| P2 | **5** (9.4%) | 43 (mean 7.17 / report) |
| Items evaluated | 94 (53 FAIL / 34 PASS / 7 N/A) | — |
| Explicit-risk findings | **0** (Stage E) | Present as a first-class category in all 6 |

**The severity profile is inverted.** Document A is **P0-heavy (70%)** because the L3 upgrade promotes nearly every severe rule violation to P0. Document B is **P1/P2-heavy (P0 ≈ 18%)** because each model calibrates severity by its own judgement. A reader comparing headline counts (53 vs 21) would wrongly conclude Document A found "2.5× more problems" — in reality the two use different granularity (rule tags vs. issues).

### 3.2 Finding Distribution in Document A

| Stage / artifact | Items | FAIL |
|------------------|:-----:|:----:|
| A.1 System prompts (L3) | 47 | 26 |
| A.2 `research_tools` (L1) | 7 | 6 |
| A.3 `review_tools` (L1) | 7 | 5 |
| A.4 `publication_tools` (L2) | 12 | 8 |
| A.5 Embedded-code QC | 13 | 2 |
| B Cross-artifact (`QD-PT` / `QD-CYC`) | 8 | 6 |
| **Total** | **94** | **53** |

Document A's **top-5 findings**: (1) declared tools do not exist in the Schema `QD-PT-2.1`; (2) no security boundaries in any role prompt `QD-P-2.5.2`; (3) no tool-invocation spec `QD-P-2.4.3`; (4) `publication_tools` raw `content` passthrough `QD-T-3.2`; (5) unbounded Reviewer↔Revisor loop `QD-P-2.5.1`.

---

## 4. Coverage Comparison — Document A against Document B's Consensus Themes

Themes T1–T24 are the normalized issues from Document B (the prior meta-analysis). "Covered by A" uses: **✅** = explicit rule FAIL matching the theme; **◐** = adjacent/partial rule; **✗** = not raised.

| # | Theme (from Document B) | LLM coverage | Covered by A? | Matching rule ID(s) in A |
|---|-------------------------|:------------:|:-------------:|--------------------------|
| T1 | Path traversal — `local_document_search.doc_path` unrestricted | 6/6 (all P0) | **✗** | — (research_tools scoped L1 read-only; no path-safety rule) |
| T2 | Arbitrary file write — `export_*` filename/template | 6/6 | ◐ | QD-T-3.1, QD-T-4.2 (undeclared write side effect; no output-path allow-list rule) |
| T3 | HITL fail-open — Human "default approval after 24h" | 6/6 | **✗** | — |
| T4 | Review↔Revise loop has no max iterations | 6/6 | ✅ | QD-P-2.5.1, **QD-CYC-1.2 (P0)** |
| T5 | Tool-name mismatch — Prompt vs Schema | 5/6 | ✅ | QD-P-1.5.2, QD-P-2.4.3, **QD-PT-2.1/2.2/2.3 (P0)** |
| T6 | Indirect prompt injection (untrusted content) | 5/6 | **✗** | — (Risk Explicit = 0; no injection rule) |
| T7 | Missing RBAC / access-boundary | 6/6 | ✅ | QD-P-2.5.2, QD-P-2.5.3 |
| T8 | Review contract inconsistency (score/format/naming) | 6/6 | ◐ | QD-P-1.1.3 (threshold only); return-shape/naming not flagged |
| T9 | Concurrency — shared state lacks reducers | 5/6 | **✗** | — |
| T10 | `current_phase` enum incomplete | 5/6 | **✗** | — |
| T11 | Publisher claims HTML but no `export_html` | 5/6 | **✗** | — |
| T12 | Publication schema param-type defects (`"content": "string"`) | 3/6 | ◐ | QD-T-2.1, QD-T-3.2 (length bound + raw passthrough) |
| T13 | Chief Editor super-role / overlap | 3/6 | **✗** | — |
| T14 | No rate limit / frequency cap | 3/6 | ✅ | QD-P-2.5.5, QD-PT-2.6 (frequency only; no cost/token budget) |
| T15 | No audit log / observability | 3/6 | **✗** | — |
| T16 | Source credibility / hallucination / fact-check | 4/6 | **✗** | — |
| T17 | Export params missing (filename/metadata) | 3/6 | ✗ | — (QD-T-1.2 covers `required` absence only) |
| T18 | `web_search` params unbounded / API-key mgmt | 4/6 | ✅ | QD-T-2.1, QD-T-2.3 (params only; key mgmt not flagged) |
| T19 | Config conflicts (sections / word-count / stress) | 5/6 | **✗** | — (config artifacts are out-of-type) |
| T20 | Error handling / retry / degradation undefined | 4/6 | ✅ | QD-P-1.6.1, QD-P-2.6.1, QD-P-2.6.2, **QD-PT-2.5 (P0)** |
| T21 | Human-node details undefined / guidance injection | 4/6 | **✗** | — |
| T22 | Citation format (APA/MLA) not globally enforced | 2/6 | ✅ | QD-P-2.1.2 |
| T23 | State persistence — no encryption/desensitization | 4/6 | ◐ | QD-P-2.3.4 (privacy handling declared absent) |
| T24 | Documentation fidelity (naming/miscount/rubric) | 3/6 | **✗** | — (out of scope by design) |

**Coverage tally:** ✅ fully covered **7** (T4, T5, T7, T14, T18, T20, T22) · ◐ partial **4** (T2, T8, T12, T23) · ✗ not covered **13** (T1, T3, T6, T9, T10, T11, T13, T15, T16, T17, T19, T21, T24).

### 4.1 The Critical Gaps

The most consequential divergences are the **unanimous-LLM themes that Document A does not raise at all**:

- **T1 Path traversal** — all 6 LLMs ranked it P0; Document A scopes `research_tools` to L1 and has no path-safety rule, so it is silent.
- **T3 HITL fail-open** — all 6 LLMs flagged "default approval after 24 hours"; Document A's rule set has no human-oversight-safety rule.
- **T6 Prompt injection** — 5/6 LLMs (two at P0) flagged it; Document A's Stage E explicitly reports **0 explicit risks** and has no injection rule.

### 4.2 The Critical Overlaps

The two documents converge most strongly on **contract and workflow-consistency defects**:

- **T5 Tool existence** — Document A's *#1 finding* (`QD-PT-2.1`) = Document B's most-disputed theme (P0 in DeepSeek/Gemini, P2 in GPT-5.6). Both agree the defect is real; they differ on severity.
- **T4 Loop termination** — Document A's `QD-CYC-1.2 (P0)` = Document B's 5-of-6 P0.
- **T20 Error handling** and **T18 Unbounded params** — explicit agreement at rule level.

---

## 5. Where They Agree vs. Diverge

### 5.1 Shared Ground (high confidence — two independent methods converge)

1. **Broken three-layer contract** (Prompt ↔ Tool Schema ↔ State/Config): both documents identify tool-definition/invocation inconsistency as the leading defect.
2. **Unbounded Review↔Revise loop**: flagged by A (`QD-CYC-1.2`, P0) and by all 6 LLMs.
3. **Error-handling and frequency gaps**: A's `QD-P-2.6.*` / `QD-P-2.5.5` align with B's T20/T14.
4. **Vague cross-references / unspecified constraints**: A's `QD-P-2.1.2`, `QD-P-1.3.2` align with B's citation-format and soft-constraint themes.

### 5.2 Divergence Type 1 — Scope (A silent, B loud)

Security, ops, and configuration concerns dominate Document B but are **out of, or not represented in, A's rule scope**: path traversal (T1), prompt injection (T6), concurrency (T9), enum completeness (T10), HTML capability (T11), config conflicts (T19), audit/observability (T15), source credibility (T16), state encryption (T23), doc fidelity (T24).

**Interpretation:** This is largely *by design*. A executes a **lite, static, Inspect-only** ruleset; it explicitly declines to draw Risk/Quality conclusions and treats configuration as out-of-type. B's audits make those conclusions freely. The gap is a **capability gap of the lite package**, not necessarily a defect in A's execution — and it is exactly the gap the `sanityops-cli` full ruleset (with Risk Explicit/Implicit + Quality) is intended to close.

### 5.3 Divergence Type 2 — Severity Calibration

For defects **both** documents see, severity can differ by up to two levels:

| Shared defect | A (skill) | B (LLM range) |
|---------------|:---------:|:-------------:|
| Tool existence mismatch | P0 | P0–P2 (spread) |
| Loop termination | P0 | P0–P1 |
| Raw content passthrough | FAIL (P0-class, L2 write) | P1–P2 |

**Interpretation:** A's severity is **rule-tier + upgrade driven** (near-uniform P0), whereas B's is **analyst-judgement driven** (graded). A gives a sharper, more conservative "block release" signal; B gives a more nuanced risk gradient.

### 5.4 Divergence Type 3 — Evidence Discipline

- A cites **exact section/rule evidence** for every verdict and states "PASS is not Risk PASS."
- B varies: GPT-5.6 Terra and sonnet-5.5 explicit-caveat the doc-vs-source boundary; GLM-5 asserts runtime risks more strongly from text alone.

**Interpretation:** A is more reproducible and more cautious about over-claiming; B is broader but uses heterogeneous evidence standards.

---

## 6. Reconciliation — Using Both Together

| Question | Document A answers | Document B answers |
|----------|--------------------|--------------------|
| Is the artifact structurally defective? | Yes — 53 rule FAILs, Gate-0 not passed | Yes — 15–30 issues each |
| Can I reproduce the verdict? | Yes (rule IDs) | No (narrative) |
| What is the security posture? | *Not answered* (Inspect ≠ Risk) | Answered (path traversal, injection, SSRF) |
| What blocks release? | 37 P0 rule violations | 6/6 consensus P0 set (path, write, HITL, loop) |
| What is the quality/RAG posture? | *Not run* | Partially addressed (source credibility, fact-check) |

**Recommended combined reading order for TC-004 remediation:**

1. **Structural fixes (authoritative, from A):** resolve the tool-existence/contract FAILs (`QD-PT-2.1`–`2.5`), the loop termination (`QD-CYC-1.2`), tool Schema completeness (`QD-T-1.1/1.2/1.4`), and error handling (`QD-P-2.6.*`).
2. **Security fixes (from B, then verify with the full CLI):** sandbox `local_document_search`, restrict `export_*` output paths, flip the Human timeout to fail-closed, and add anti-injection handling — these are precisely the themes A's lite scope does not cover, so they must be validated with `sanityops-cli` Risk (Explicit + Implicit) rather than assumed absent.
3. **Ops/quality (from B, optional):** rate limits, cost budget, audit log, state encryption.

---

## 7. Conclusion

The two documents are **complementary, not competing**:

- **Document A (skill report)** is the **reproducible, rule-anchored, scope-disciplined** view. It is authoritative on structural/contract defects, explicitly refuses to over-claim security or quality, and is P0-heavy by construction. Its limitation is a **coverage gap in the lite ruleset** — notably the L1 read-only tool tier, which omits the path-traversal class.
- **Document B (multi-LLM analysis)** is the **broad, security- and ops-oriented** view. It uniquely surfaces the path-traversal (T1), HITL fail-open (T3), and prompt-injection (T6) classes that all or most models independently flagged as P0 — but with no shared rule IDs, wide severity disagreement, and heterogeneous evidence discipline.

**Practical takeaway:** the highest-confidence defects are those found by **both** — the tool-contract and loop-termination issues (A's `QD-PT-*` / `QD-CYC-1.2` vs B's T4/T5). The highest-priority items found **only by B** (T1 path traversal, T3 fail-open, T6 injection) should be treated as **unverified-but-urgent**, and confirmed through the full `sanityops-cli` Risk stages — which is exactly the escalation Document A itself points to.

> **Non-official-result statement:** This comparison is produced by the host model over two prior artifacts. Neither the skill package (Document A) nor this document is a conclusion of the official SanityOps engine. For a full inspection use `sanityops-cli`.

---

## Appendix A — Source Metadata

| Item | Document A | Document B |
|------|------------|------------|
| Path | `test-cases/agent-suite/TC-004-...sanityops-skill-report.md` | `report-onlybyLLM/comparison-multi-llm-analysis-tc-004-2026-10-15.md` |
| Produced by | sanityops-inspect-lite v1.0.0 (host model unspecified) | Host-model meta-analysis of 6 LLM reports |
| Date | 2026-10-14 | 2026-10-15 |
| Findings | 53 FAIL (37 P0 / 11 P1 / 5 P2) | 127 items across 6 reports (mean 21.2) |
| Explicit-risk findings | 0 | First-class category in all 6 |
| Gate result | Gate-0 not passed (G0-4) | N/A |

## Appendix B — Rule-ID Index (Document A)

- **`QD-P-*`** — System-prompt rules (`1.x` structure/identity, `2.x` clarity/input/output/tool/error/example). 47 items, 26 FAIL.
- **`QD-T-*`** — Tool-Schema rules (`research_tools` L1, `review_tools` L1, `publication_tools` L2). 26 items, 19 FAIL.
- **`QD-PT-*`** — Cross-artifact Prompt↔Tool rules. 6 items, 5 FAIL.
- **`QD-CYC-*`** — Circular-invocation rules. 2 items, 1 FAIL (`QD-CYC-1.2`, the Reviewer↔Revisor loop).
- **`QC-*`** — Embedded-code quality checks. 13 items, 2 FAIL.
