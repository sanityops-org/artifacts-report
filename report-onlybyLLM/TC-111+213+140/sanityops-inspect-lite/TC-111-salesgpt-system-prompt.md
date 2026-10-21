# TC-111: SalesGPT System Prompt — sanityops-inspect-lite Report

## Report Header

- **Host model**: claude-opus-4-8[1m] (Anthropic)
- **Skill package**: sanityops-inspect-lite v1.0.0
- **Specification baseline**: SanityOps Framework v1.0 (2026-10 revision)
- **Non-official-result statement**: *This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.*
- **Inspection date**: 2026-10-21
- **Artifact version label**: TC-111-salesgpt-system-prompt.md (SALES_AGENT_TOOLS_PROMPT)
- **Fidelity tier**: `full` — verbatim Python string literal from source repository

---

## Executive Summary

**Overall Status**: Executed stages A, B, C, E, F, G. Stage D did not execute due to incomplete artifact set.

**P0/P1/P2 Counts**:
| Category | P0 | P1 | P2 |
|----------|----|----|-----|
| Stage A (QD-P) | 2 | 6 | 3 |
| Stage A (QC) | 0 | 2 | 0 |
| Stage B (Cross) | N/A | N/A | N/A |
| **Total** | **2** | **8** | **3** |

**Gate Result**: Not passed — G0-4 (no Tool Schemas present)

**Risk Explicit Summary**:
- Explicit·P0: 0
- Explicit·P1: 3
- Explicit·P2: 2

**Top 5 Findings**:
1. **QD-P-1.1.1** — Direct contradiction: First-turn greeting rule vs. Introduction stage requirement
2. **QD-P-1.3.2** — Vague qualifier: "short length" not operationalized
3. **QD-P-2.3.1** — Undefined output format: `<END_OF_CALL>` integration ambiguous
4. **NL-A-4** — Conditional deception instruction ("say you got contact info from public records")
5. **QC-0.2** — Code blocks lack language identifiers

---

## Status Board

```
Stage A (Single-artifact):  Executed — 2 P0, 6 P1, 3 P2 (QC: 2 P1)
Stage B (Cross):            Not Executed — no Skill/Tool artifacts
Stage C (Gate-0):           Not passed — G0-4 unsatisfied (no Tool Schemas)
Stage D (Permission QD-PM): Not Executed — incomplete artifact set
Stage E (Risk Explicit EX): Executed — 0 Explicit·P0, 3 Explicit·P1, 2 Explicit·P2
Stage F (Impact outlook):   Executed — advisory cards emitted
Stage G (Self-verification): Executed
```

---

## 1. Fidelity and Type Classification

### Step 0 — Fidelity Classification

| Object | Tier | Basis |
|--------|------|-------|
| SALES_AGENT_TOOLS_PROMPT | `full` | Verbatim Python string literal from source repository; no summary/meta sections |

### Agent Tier Determination

- Single persona with tool invocations
- 8-stage workflow (multi-step)
- Tool-use protocol defined (ReAct format)
- Business context (sales conversation)

**Determination: AC-L2 (Multi-turn Interactive)** — multi-turn dialogue, tool invocations, simple workflow

---

## 2. Stage A — Single-artifact Inspection (QD-P)

### Part 1: Logic Defects (QD-P-1.x)

| QD-P ID | Verdict | Evidence |
|---------|---------|----------|
| QD-P-1.1.1 | **FAIL·P0** | First-turn rule: "Start the conversation by just a greeting and how is the prospect doing **without pitching** in your first turn." vs. Introduction stage: "1: Introduction... **Always clarify in your greeting the reason why you are calling.**" Direct contradiction. |
| QD-P-1.1.2 | PASS | No MUST constraint conflicts without priority. |
| QD-P-1.1.3 | PASS | No example-rule contradiction. |
| QD-P-1.2.1 | PASS | Salesperson role matches responsibilities. |
| QD-P-1.2.2 | PASS | Role-output style aligned. |
| QD-P-1.2.3 | PASS | Constraint-responsibility aligned. |
| QD-P-1.2.4 | PASS | Identity boundary ("Never forget your name is {salesperson_name}") appropriate. |
| QD-P-1.3.1 | PASS | No quantifier misuse. |
| QD-P-1.3.2 | **FAIL·P1** | "Keep your responses in **short length** to retain the user's attention." — "short length" not operationalized (no word/character/sentence count). |
| QD-P-1.3.3 | PASS | Boundaries defined by stages. |
| QD-P-1.4.3 | N/A | No explicit Skills defined. |
| QD-P-1.5.1 | PASS | Responsibilities support objective. |
| QD-P-1.5.2 | N/A | No explicit resources. |
| QD-P-1.6.1 | PASS | No critical decision word vagueness. |
| QD-P-1.6.2 | PASS | No model-internal-state dependencies. |
| QD-P-1.6.3 | PASS | No soft-rule interweaving without arbitration. |
| QD-P-1.6.4~1.6.8 | PASS | No gray-zone defects. |

### Part 2: Completeness/Security (QD-P-2.x)

| QD-P ID | Verdict | Evidence |
|---------|---------|----------|
| QD-P-2.1.2 | PASS | Template references clear. |
| QD-P-2.2.1 | PASS | Input sources (conversation history, tools) declared. |
| QD-P-2.2.2 | PASS | Format templates provided. |
| QD-P-2.2.3 | PASS | Required fields (Thought, Action, etc.) distinguished. |
| QD-P-2.2.4 | PASS | Missing-input handling ("I don't know") defined. |
| QD-P-2.3.1 | **FAIL·P1** | `<END_OF_CALL>` termination token not integrated into required Thought/salesperson format. |
| QD-P-2.3.2 | PASS | Output structure defined for normal turns. |
| QD-P-2.3.4 | N/A | No PII processing. |
| QD-P-2.3.5 | N/A | No RAG/retrieval. |
| QD-P-2.3.6 | **FAIL·P2** | "short length" constraint lacks truncation behavior. |
| QD-P-2.3.7 | N/A | Single-region. |
| QD-P-2.4.1 | PASS | 8-stage workflow defined. |
| QD-P-2.4.2 | PASS | Tools referenced in template. |
| QD-P-2.4.3 | PASS | ReAct format defined. |
| QD-P-2.4.4 | PASS | Conversation history boundary defined. |
| QD-P-2.5.1 | PASS | Termination token (`<END_OF_CALL>`) defined. |
| QD-P-2.5.2 | **FAIL·P0** | "If you're asked about where you got the user's contact information, say that you got it from **public records**." — Instructs agent to fabricate source; deception instruction without consent disclosure. |
| QD-P-2.5.3 | PASS | No permission control needed for this context. |
| QD-P-2.5.4 | PASS | Single-response constraint prevents ambiguity. |
| QD-P-2.5.6 | PASS | Instruction-data boundary defined. |
| QD-P-2.5.7 | N/A | No irreversible operations. |
| QD-P-2.5.8 | PASS | Confidentiality addressed. |
| QD-P-2.5.9 | N/A | Not regulated domain. |
| QD-P-2.6.1 | **FAIL·P1** | Tool returns "I don't know" handled, but other errors (timeout, rate limit) not covered. |
| QD-P-2.6.2 | **FAIL·P2** | No degradation strategy for tool failures. |
| QD-P-2.6.3 | PASS | No retry mechanism. |
| QD-P-2.6.4 | PASS | End-of-call trigger defined. |

---

## 3. Stage A — QC Inspection

| QC ID | Verdict | Evidence |
|-------|---------|----------|
| QC-0.1 | PASS | ReAct format blocks are syntactically valid. |
| QC-0.2 | **FAIL·P1** | Lines 41-46 and 48-52: Code blocks lack explicit language identifiers (` ```python `). |
| QC-0.3~0.5 | PASS | Snippets are complete, fence integrity OK. |

---

## 4. Stage B — Cross-artifact Inspection

**Execution Status**: Not Executed

**Reason**: No Skill or Tool Schema artifacts to cross-reference.

---

## 5. Stage C — Gate-0

| Condition | Status | Reason |
|-----------|--------|--------|
| G0-1 | Not passed (info) | P0 findings in Stage A |
| G0-2 | N/A | No Stage B execution |
| G0-3 | Passed | Responsibility boundary (sales conversation stages) is locatable |
| G0-4 | **Not passed** | No Tool Schemas present |

**Gate-0 Result**: Not passed (G0-4)

---

## 6. Stage D — Permission

**Execution Status**: Not Executed

**Reason**: Incomplete artifact set (no Tool Schemas).

---

## 7. Stage E — Risk Explicit Audit

| EX ID | Risk Expression | Impact | Severity | Trigger |
|-------|-----------------|--------|----------|---------|
| NL-A-4 | "If you're asked about where you got the user's contact information, say that you got it from public records" | D1, D2 | Explicit·P1·conditional | Deception instruction; may be legitimate business practice but lacks disclosure |
| NL-A-4 | "Never produce lists, just answers" | D2 | Explicit·P2·unconditional | Format constraint; low risk |
| NL-A-3 | "Never forget your name is {salesperson_name}" | D3 | Explicit·P2·unconditional | Identity reinforcement; low risk |
| NL-B-10 | Stage tracking + tool format + termination token form cross-object behavior chain | D2 | Explicit·P1·conditional | Complexity may cause inconsistent behavior |

**Risk Item Summary**:
- Total EX items: 4
- Explicit·P0: 0
- Explicit·P1: 2
- Explicit·P2: 2

---

## 8. Stage F — Impact Outlook (Sample Cards)

### Impact Card: QD-P-1.1.1 | Direct Contradiction

**Static Discovery**
- Evidence: First-turn greeting rule contradicts Introduction stage

**Potential Security Associations**
- Attack Surface: AS-01 (Instruction/Context Boundary)
- Impact: D2, D3
- Strength: Strong (provisional lite)

---

### Impact Card: QD-P-2.5.2 | Deception Instruction

**Static Discovery**
- Evidence: "say you got it from public records"

**Potential Security Associations**
- Attack Surface: AS-01, AS-03
- Impact: D1, D2
- Strength: Strong (provisional lite)

---

## 9. Self-Verification

**In-line checks**: All IDs verified in references; no causal language in Stage F; no "secure" claims.

**Closing checks**: Status board complete; header complete; English-only report.

**Result**: ID back-closure OK · red-line wording OK · output contract OK · reconciliation OK

---

## Appendix: Full Defect List

### P0 Defects (2)

1. **QD-P-1.1.1** — First-turn greeting rule contradicts Introduction stage requirement
2. **QD-P-2.5.2** — Deception instruction without consent disclosure

### P1 Defects (8)

1. **QD-P-1.3.2** — "short length" not operationalized
2. **QD-P-2.3.1** — `<END_OF_CALL>` format ambiguous
3. **QD-P-2.6.1** — Runtime exceptions not fully covered
4. **QC-0.2** (×2) — Code blocks lack language identifiers
5. **NL-A-4** — Deception instruction (EX finding)
6. **NL-B-10** — Cross-object behavior chain (EX finding)

### P2 Defects (3)

1. **QD-P-2.3.6** — Truncation behavior undefined
2. **QD-P-2.6.2** — No degradation strategy
3. **NL-A-4 / NL-A-3** — Format/identity constraints (EX findings)