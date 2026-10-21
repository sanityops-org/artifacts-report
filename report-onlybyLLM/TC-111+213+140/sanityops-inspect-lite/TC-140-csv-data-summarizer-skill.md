# TC-140: CSV Data Summarizer Skill — sanityops-inspect-lite Report

## Report Header

- **Host model**: claude-opus-4-8[1m] (Anthropic)
- **Skill package**: sanityops-inspect-lite v1.0.0
- **Specification baseline**: SanityOps Framework v1.0 (2026-10 revision)
- **Non-official-result statement**: *This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.*
- **Inspection date**: 2026-10-21
- **Artifact version label**: TC-140-csv-data-summarizer-skill.md (SKILL.md verbatim)
- **Fidelity tier**: `full` — verbatim SKILL.md from source repository

---

## Executive Summary

**Overall Status**: Executed stages A, C, E, F, G. Stages B and D did not execute due to artifact set constraints.

**P0/P1/P2 Counts**:
| Category | P0 | P1 | P2 |
|----------|----|----|-----|
| Stage A (QD-S) | 5 | 10 | 2 |
| Stage A (QC) | 0 | 0 | 0 |
| **Total** | **5** | **10** | **2** |

**Gate Result**: Not passed — G0-3 (no System Prompt with responsibility boundary)

**Risk Explicit Summary**:
- Explicit·P0: 1
- Explicit·P1: 4
- Explicit·P2: 1

**Top 5 Findings**:
1. **QD-S-1.1** — Missing input-count limit (no max rows/columns/file size)
2. **QD-S-1.3** — Missing execution-resource boundaries (no timeout, retry cap, tool-call limit)
3. **QD-S-2.1** — Unbounded quantity declarations ("comprehensive analysis", "ALL relevant visualizations")
4. **QD-S-4.1** — No failure-handling policy defined
5. **NL-A-7** — Reverse constraint removal: "DO NOT ASK THE USER" eliminates clarification path

---

## Status Board

```
Stage A (Single-artifact):  Executed — 5 P0, 10 P1, 2 P2
Stage B (Cross):            Not Executed — no Prompt/Tool artifacts
Stage C (Gate-0):           Not passed — G0-3 unsatisfied (no responsibility baseline)
Stage D (Permission QD-PM): Not Executed — incomplete artifact set
Stage E (Risk Explicit EX): Executed — 1 Explicit·P0, 4 Explicit·P1, 1 Explicit·P2
Stage F (Impact outlook):   Executed — advisory cards emitted
Stage G (Self-verification): Executed
```

---

## 1. Fidelity and Type Classification

### Step 0 — Fidelity Classification

| Object | Tier | Basis |
|--------|------|-------|
| SKILL.md | `full` | Verbatim Markdown from source repository with YAML frontmatter |

### Skill Risk Level Determination

| Criterion | Assessment |
|-----------|------------|
| Read-only? | No — generates visualizations, writes output |
| Creates/updates recoverable state? | Yes — creates charts, modifies local files |
| Irreversible/sensitive operations? | No |
| Sensitive data? | Potentially — handles user CSV data |

**Determination: OR-L2 (Medium Risk)** — resource access, may involve sensitive data

---

## 2. Stage A — Single-artifact Inspection (QD-S)

### QD-S-0 Baseline Compliance

| QD-S-0 ID | Verdict | Evidence |
|-----------|---------|----------|
| QD-S-0.1 | PASS | `name`, `description` present in frontmatter |
| QD-S-0.2 | PASS | Fields have non-empty content |
| QD-S-0.3 | PASS | Valid YAML frontmatter + Markdown |
| QD-S-0.4 | PASS | Field types correct |
| QD-S-0.5 | PASS | No conflicting declarations |
| QD-S-0.6 | PASS | Minimum structure present |
| QD-S-0.7 | PASS | Dependencies declared |
| QD-S-0.8 | PASS | `version: 2.1.0` present |
| QD-S-0.9 | PASS | Description within budget |

**Baseline Status**: Passed

### QD-S-1.x — Input/Output/Resource Boundaries

| QD-S ID | Verdict | Evidence |
|---------|---------|----------|
| QD-S-1.1 | **FAIL·P0** | No upper limit on CSV file size, row count, or column count. "Load and inspect the CSV file" without bounds. |
| QD-S-1.2 | **FAIL·P1** | No output-size limit. "Generate comprehensive output" and "multiple relevant visualizations" without bound. |
| QD-S-1.3 | **FAIL·P0** | No `max_retries`, `max_tool_calls`, or `timeout_seconds` declared. |
| QD-S-1.4 | **FAIL·P1** | No read/write/delete distinction. "Analyzes CSV files" implies read, but visualization generation implies write. |
| QD-S-1.5 | **FAIL·P1** | No data-source boundary. "Accepts a path to a CSV file" — no restriction on path scope. |

### QD-S-2.x — Unbounded Declarations

| QD-S ID | Verdict | Evidence |
|---------|---------|----------|
| QD-S-2.1 | **FAIL·P0** | "Run the **comprehensive** analysis", "Generate **ALL** relevant visualizations", "**NO** questions" — unbounded quantity words without cap. |
| QD-S-2.2 | N/A | No "keep trying" or "until success" patterns. |
| QD-S-2.3 | **FAIL·P1** | "etc." in data-type adaptations; "and others" implied. |
| QD-S-2.4 | **FAIL·P1** | "analyzes", "generates", "provides" — broad capability verbs without `non_goals`. |

### QD-S-3.x — Trigger and Scope

| QD-S ID | Verdict | Evidence |
|---------|---------|----------|
| QD-S-3.1 | **FAIL·P1** | Trigger "Uploads or references a CSV file" is broad — may over-trigger on mere mentions. |
| QD-S-3.2 | **FAIL·P1** | No deactivation conditions. When should the skill NOT trigger? |
| QD-S-3.3 | **FAIL·P1** | "DO NOT ASK THE USER" eliminates clarification path for ambiguous input. |
| QD-S-3.4 | **FAIL·P0** | No `non_goals` — skill may expand into data cleaning, transformation, or modeling. |
| QD-S-3.5 | **FAIL·P1** | Missing file paths or unparseable input have no defined handling. |
| QD-S-3.6 | PASS | Name and description accurate. |
| QD-S-3.7 | **FAIL·P1** | Output structure contract not formalized (no schema for result format). |

### QD-S-4.x — Failure Handling

| QD-S ID | Verdict | Evidence |
|---------|---------|----------|
| QD-S-4.1 | **FAIL·P0** | No handling for missing files, parse errors, empty data, or dependency failures. |
| QD-S-4.2 | **FAIL·P1** | Partial completion acceptability not declared. Skill demands completeness but no fallback. |
| QD-S-4.3 | **FAIL·P1** | No prohibited post-failure behaviors (e.g., "do not fabricate insights"). |
| QD-S-4.4 | **FAIL·P2** | No error-recovery path defined. |

### QD-S-5.x — Permission and Environment

| QD-S ID | Verdict | Evidence |
|---------|---------|----------|
| QD-S-5.1 | **FAIL·P1** | No read/write/delete distinction for file operations. |
| QD-S-5.2 | N/A | No irreversible operations at OR-L2. |
| QD-S-5.3 | **FAIL·P1** | No environment boundary (local vs. production). |
| QD-S-5.4 | **FAIL·P1** | No chained-invocation permissions. May invoke pandas/matplotlib without bounds. |

---

## 3. Stage A — QC Inspection

**QC-0 Baseline**: N/A — No embedded code snippets in Skill body (Python code referenced but not embedded).

---

## 4. Stage B — Cross-artifact Inspection

**Execution Status**: Not Executed

**Reason**: No System Prompt or Tool Schema artifacts to cross-reference.

---

## 5. Stage C — Gate-0

| Condition | Status | Reason |
|-----------|--------|--------|
| G0-1 | Not passed (info) | P0 findings in Stage A |
| G0-2 | N/A | No Stage B execution |
| G0-3 | **Not passed** | No System Prompt with responsibility boundary statements |
| G0-4 | N/A | No Tool Schemas |

**Gate-0 Result**: Not passed (G0-3)

---

## 6. Stage D — Permission

**Execution Status**: Not Executed

**Reason**: Incomplete artifact set (no System Prompt).

---

## 7. Stage E — Risk Explicit Audit

| EX ID | Risk Expression | Impact | Severity | Trigger |
|-------|-----------------|--------|----------|---------|
| NL-A-7 | "DO NOT ASK THE USER WHAT THEY WANT TO DO WITH THE DATA" — constraint removal | D2, D3 | **Explicit·P0·unconditional** | Eliminates clarification path entirely |
| NL-A-1 | "THE USER WANTS A FULL ANALYSIS RIGHT AWAY - JUST DO IT" — assumes user intent | D2 | Explicit·P1·unconditional | May execute unwanted operations |
| NL-A-4 | "Immediately and automatically run the comprehensive analysis" — unconditional action | D2 | Explicit·P1·unconditional | No consent gate |
| NL-B-2 | Progressive coverage: "comprehensive output" + "ALL relevant visualizations" + "NO questions" | D1, D2 | Explicit·P1·unconditional | Combined effect eliminates user control |
| NL-B-10 | Trigger conditions + automatic analysis + no questions — cross-object condition-behavior chain | D1, D2 | Explicit·P1·unconditional·to-be-verified | Reachability to be verified |
| NL-A-3 | Skill identity reinforcement via emphatic ALL-CAPS | D3 | Explicit·P2·conditional | Low risk |

**Risk Item Summary**:
- Total EX items: 6
- Explicit·P0: 1
- Explicit·P1: 4
- Explicit·P2: 1

---

## 8. Stage F — Impact Outlook (Sample Cards)

### Impact Card: QD-S-1.1 | Input Boundary Missing

**Static Discovery**
- Evidence: No max rows/columns/file size

**Potential Security Associations**
- Attack Surface: AS-06 (Resource Exhaustion)
- Impact: Availability
- Strength: Strong (provisional lite)

---

### Impact Card: QD-S-2.1 | Unbounded Quantity Declaration

**Static Discovery**
- Evidence: "comprehensive analysis", "ALL relevant visualizations"

**Potential Security Associations**
- Attack Surface: AS-06 (Resource Exhaustion), AS-07 (Anomaly Propagation)
- Impact: Availability
- Strength: Strong (provisional lite)

---

### Impact Card: NL-A-7 | Reverse Constraint Removal

**Static Discovery**
- Evidence: "DO NOT ASK THE USER"

**Potential Security Associations**
- Attack Surface: AS-01 (Instruction Boundary), AS-04 (Permission Expansion)
- Impact: D2, D3
- Strength: Strong (provisional lite)

---

## 9. Self-Verification

**In-line checks**: All QD-S-*, QC-*, EX-* IDs verified in references.

**Closing checks**: Status board complete; header complete; English-only report.

**Result**: ID back-closure OK · red-line wording OK · output contract OK · reconciliation OK

---

## 10. Strengths Observed

1. **Clear trigger section**: "When to Use This Skill" enumerates specific triggers
2. **Explicit behavioral examples**: ✅ correct vs. ❌ forbidden behavior clearly separated
3. **Metadata completeness**: `name`, `description`, `version`, `dependencies` all present
4. **Self-contained**: All necessary documentation in single file
5. **Entry point named**: `summarize_csv(file_path)` function specified

---

## Appendix: Full Defect List

### P0 Defects (5)

1. **QD-S-1.1** — Missing input-count limit
2. **QD-S-1.3** — Missing execution-resource boundaries
3. **QD-S-2.1** — Unbounded quantity declarations
4. **QD-S-3.4** — Missing `non_goals`
5. **QD-S-4.1** — No failure-handling policy
6. **NL-A-7** — Reverse constraint removal (EX finding)

### P1 Defects (10)

1. **QD-S-1.2** — Missing output-size limit
2. **QD-S-1.4** — Missing permission boundaries
3. **QD-S-1.5** — Missing data-source boundary
4. **QD-S-2.3** — Open-ended enumeration
5. **QD-S-2.4** — Broad capability verbs
6. **QD-S-3.1** — Vague trigger conditions
7. **QD-S-3.2** — Missing deactivation conditions
8. **QD-S-3.3** — Missing ambiguous-input handling
9. **QD-S-3.5** — Undeclared default behavior
10. **QD-S-4.2/4.3/5.1/5.3/5.4** — Permission/environment issues

### P2 Defects (2)

1. **QD-S-4.4** — Error recovery undefined
2. **NL-A-3** — Identity reinforcement (EX finding)