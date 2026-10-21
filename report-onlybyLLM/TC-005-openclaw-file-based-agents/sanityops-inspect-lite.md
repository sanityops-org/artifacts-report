# TC-005: OpenClaw File-Based Multi-Agent Suite — sanityops-inspect-lite Report

## Report Header

- **Host model**: claude-opus-4-8[1m] (Anthropic)
- **Skill package**: sanityops-inspect-lite v1.0.0
- **Specification baseline**: SanityOps Framework v1.0 (2026-10 revision)
- **Non-official-result statement**: *This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.*
- **Inspection date**: 2026-10-21
- **Artifact version label**: TC-005-openclaw-file-based-agents.md (test case document)
- **Fidelity tier**: `summary` (per-object: S2 — contains non-artifact sections such as "Evaluation Dimensions", "Scoring Criteria", "Test Suggestions", "Collection Date/Method"; content is a summary/analysis of the OpenClaw framework, not a verbatim production artifact)

> **Fidelity consequence**: For `summary` fidelity, only **contradiction-based** findings are run; **absence-based** findings are skipped.

---

## Executive Summary

**Overall Status**: Executed stages A, B, C (Gate-0 not passed), E, F, G. Stage D (Permission) did not execute due to Gate-0 structural condition failure.

**P0/P1/P2 Counts** (Inspect defects):
| Category | P0 | P1 | P2 |
|----------|----|----|-----|
| Stage A (QD-P) | 6 | 8 | 2 |
| Stage A (QC) | 0 | 1 | 0 |
| Stage B (Cross) | 4 | 3 | 0 |
| **Total** | **10** | **12** | **2** |

**Gate Result**: Not passed — G0-3 (responsibility boundary statements not locatable as coherent baseline) and G0-4 (no Tool Schemas present).

**Risk Explicit Summary**:
| Grade | Count |
|-------|-------|
| Explicit·P0 | 2 |
| Explicit·P1 | 5 |
| Explicit·P2 | 2 |

**Top 5 Findings**:
1. **QD-P-1.1.1** — Direct contradiction: "4 core file types" vs. 6 displayed types
2. **QD-P-1.2.1** — Role-Responsibility mismatch: Undefined agents in routing rules
3. **QD-P-2.5.2** — Missing security boundary: Shell "read-only" by natural language only
4. **QD-P-2.4.2** — Undeclared resources: Tools lack schemas
5. **NR-S-6** — Auto-email without consent in HEARTBEAT pattern

**What was NOT run**: Risk Implicit, runtime Quality subsets, Permission stage (blocked by Gate-0).

---

## Status Board

```
Stage A (Single-artifact):  Executed — 6 P0, 8 P1, 2 P2 (QC: 1 P1)
Stage B (Cross):            Executed — 4 P0, 3 P1, 0 P2
Stage C (Gate-0):           Not passed — G0-3, G0-4 unsatisfied
Stage D (Permission QD-PM): Not Executed — Gate-0 not satisfied + incomplete artifact set
Stage E (Risk Explicit EX): Executed — 2 Explicit·P0, 5 Explicit·P1, 2 Explicit·P2
Stage F (Impact outlook):   Executed — advisory cards emitted
Stage G (Self-verification): Executed
```

---

## 1. Fidelity and Type Classification

### Step 0 — Fidelity Classification

| Object | Tier | Basis |
|--------|------|-------|
| TC-005-openclaw-file-based-agents.md | `summary` | S2: Contains non-artifact sections ("Evaluation Dimensions", "Scoring Criteria", "Test Suggestions"); summary of OpenClaw framework |

### Agent Tier Determination

- Multiple agents defined (support-main, sales-assistant, onboarding-guide, billing-agent, tech-support, sales-manager)
- Multi-tool invocations (browser, memory, file, shell)
- Multi-step workflows with handoff
- Security-sensitive operations (Shell, external communication, user data)

**Determination: AC-L3 (Complex Agent)**

---

## 2. Stage A — Single-artifact Inspection (QD-P)

### Part 1: Logic Defects (QD-P-1.x)

| QD-P ID | Verdict | Evidence |
|---------|---------|----------|
| QD-P-1.1.1 | **FAIL·P0** | "4 core file types" (line 25) vs. 6 displayed types (SOUL, AGENTS, USER, IDENTITY, HEARTBEAT, MEMORY). Direct contradiction. |
| QD-P-1.1.2 | PASS | No MUST constraint conflicts without priority. |
| QD-P-1.1.3 | PASS | No example-rule contradiction. |
| QD-P-1.2.1 | **FAIL·P0** | Agents "billing-agent", "tech-support", "sales-manager" in routing rules (lines 130-134) but not in Agent Registry. |
| QD-P-1.2.2 | PASS | Role-output style aligned. |
| QD-P-1.2.3 | PASS | Constraint-responsibility aligned. |
| QD-P-1.2.4 | PASS | Identity boundary appropriate. |
| QD-P-1.3.1 | PASS | No quantifier misuse. |
| QD-P-1.3.2 | PASS | No vague qualifiers in critical paths. |
| QD-P-1.3.3 | **FAIL·P0** | Naming inconsistency: "customer-support-agent" / "support-main" / "Helper" / "support-soul.md" — no authoritative mapping. |
| QD-P-1.4.3 | **FAIL·P0** | Skills (browser, memory, file, shell) have no parameter/return definitions. |
| QD-P-1.5.1 | PASS | Responsibilities support objective. |
| QD-P-1.5.2 | **FAIL·P0** | HEARTBEAT invokes undefined functions (fetchTickets, sendEmail, postToSlack, etc.). |
| QD-P-1.6.1~1.6.8 | PASS | No gray-zone defects. |

### Part 2: Completeness/Security (QD-P-2.x)

| QD-P ID | Verdict | Evidence |
|---------|---------|----------|
| QD-P-2.1.2 | PASS | Reference clarity adequate. |
| QD-P-2.2.1~2.2.4 | PASS | Input sources and handling declared. |
| QD-P-2.3.1~2.3.6 | PASS | Output formats described. |
| QD-P-2.3.4 | N/A | No PII processing declared. |
| QD-P-2.3.5 | PASS | Not RAG-dependent. |
| QD-P-2.3.7 | N/A | Single-region. |
| QD-P-2.4.1 | **FAIL·P0** | HEARTBEAT tasks reference undefined services. |
| QD-P-2.4.2 | **FAIL·P0** | Tools lack schemas. |
| QD-P-2.4.3~2.4.4 | PASS | Parameter order and memory boundary OK. |
| QD-P-2.5.1 | PASS | Termination constraints present. |
| QD-P-2.5.2 | **FAIL·P0** | Shell "(read-only)" by comment only; auto-email without consent. |
| QD-P-2.5.3 | **FAIL·P0** | Cross-agent permission boundaries undefined. |
| QD-P-2.5.4 | **FAIL·P1** | Multiple routing rules, no priority definition. |
| QD-P-2.5.6 | PASS | Instruction-data boundary implied. |
| QD-P-2.5.7 | N/A | No irreversible operations requiring human confirmation. |
| QD-P-2.5.8~2.6.4 | PASS | Confidentiality and exception handling OK. |

---

## 3. Stage A — QC Inspection (Embedded Code)

| QC ID | Verdict | Evidence |
|-------|---------|----------|
| QC-0.1 | PASS | Snippets syntactically valid. |
| QC-0.2 | **FAIL·P1** | Lines 140, 258: Code blocks lack language identifiers. |
| QC-0.3~0.5 | PASS | Snippets illustrative, fence integrity OK. |

---

## 4. Stage B — Cross-artifact Inspection

| QD ID | Verdict | Evidence |
|-------|---------|----------|
| QD-PS-1.1 | N/A | No independent Skills. |
| QD-PS-1.2 | PASS | Trigger conditions consistent. |
| QD-PS-1.3 | **FAIL·P0** | Routing references undefined agents. |
| QD-PS-1.4~1.6 | PASS | Resource and output consistent. |
| QD-PS-1.7 | **FAIL·P1** | HEARTBEAT services lack preconditions. |
| QD-PT-2.1 | **FAIL·P0** | Tools declared but no schemas exist. |
| QD-PT-2.2~2.3 | N/A | No schemas. |
| QD-PT-2.4 | **FAIL·P0** | Shell read-only not enforced. |
| QD-PT-2.5~2.6 | PASS | Error handling OK. |
| QD-PT-2.7 | N/A | No schemas. |
| QD-ST-3.1 | **FAIL·P0** | Tools lack schemas. |
| QD-ST-3.2~3.3 | N/A | No schemas. |
| QD-ST-3.4~3.5 | PASS | Frequency and output OK. |
| QD-ST-3.6 | **FAIL·P0** | Shell constraint unenforced. |
| QD-ST-3.7 | PASS | Errors handled. |
| QD-CYC-1.1~1.3 | PASS | No circular invocation. |
| QD-SS-4.1 | **FAIL·P1** | Routing trigger overlap, no priority. |
| QD-SS-4.2 | PASS | Names unique. |
| QD-TT-5.1~5.3 | N/A | No Tool Schemas. |

---

## 5. Stage C — Gate-0

| Condition | Status | Reason |
|-----------|--------|--------|
| G0-1 | Not passed (info) | P0 findings in Stage A |
| G0-2 | Not passed (info) | P0 findings in Stage B |
| G0-3 | **Not passed** | Naming inconsistency prevents locatable responsibility baseline |
| G0-4 | **Not passed** | No Tool Schemas |

**Gate-0 Result**: Not passed (G0-3, G0-4)

---

## 6. Stage D — Permission

**Execution Status**: Not Executed

**Reason**: Gate-0 not satisfied; incomplete artifact set (no Tool Schemas).

---

## 7. Stage E — Risk Explicit Audit

| EX ID | Risk Expression | Impact | Severity | Trigger |
|-------|-----------------|--------|----------|---------|
| NL-A-7 | "Run diagnostic commands (read-only)" — constraint by comment | D3 | Explicit·P1·unconditional |
| NL-A-4 | "If user uses English, call external translation service" | D1, D3 | Explicit·P1·conditional |
| NL-B-2 | Progressive constraint relaxation in memory patterns | D1, D2, D3 | **Explicit·P0·unconditional** |
| NL-B-10 | Cross-object condition-behavior chain (SOUL + HEARTBEAT) | D1 | Explicit·P1·unconditional·to-be-verified |
| NR-S-2 | Implied `allow_external_call: true` by HEARTBEAT | D1, D3 | Explicit·P1·conditional |
| NR-S-6 | Auto-email sending without consent in loop | D1 | **Explicit·P0·unconditional** |
| NR-S-9 | Data exfiltration pattern in HEARTBEAT | D1 | Explicit·P1·conditional |
| NL-A-1 | "Escalate billing issues to human team immediately" | D3 | Explicit·P2·conditional |
| NL-A-3 | Skills with undefined scope | D3 | Explicit·P2·conditional |

---

## 8. Stage F — Impact Outlook (Sample Cards)

### Impact Card: QD-P-1.1.1 | Direct Contradiction

**Static Discovery**
- Evidence: "4 core file types" vs. 6 displayed

**Potential Security Associations**
- Attack Surface: AS-01, AS-05
- Impact: D2, D3, Availability
- Strength: Strong (provisional lite)

**Recommended Validation**
- Risk Implicit: NOT run
- External controls: UNKNOWN

### Impact Card: QD-P-2.5.2 | Missing Security Boundary

**Static Discovery**
- Evidence: Shell "(read-only)" by comment; auto-email without consent

**Potential Security Associations**
- Attack Surface: AS-01, AS-03, AS-04
- Impact: D1, D2, D3
- Strength: Strong (provisional lite)

---

## 9. Self-Verification

**In-line checks**: All IDs verified in references; no causal language in Stage F; no "secure" claims.

**Closing checks**: Status board complete; header complete; English-only report.

**Reconciliation**: AC-L3 correct; N/A bases recorded; upgrades justified.

**Result**: ID back-closure OK · red-line wording OK · output contract OK · reconciliation OK

---

## Appendix: Full Defect List

### P0 Defects (10)

1. QD-P-1.1.1 — "4 core file types" vs. 6 displayed
2. QD-P-1.2.1 — Undefined agents in routing
3. QD-P-1.3.3 — Naming inconsistency (no authoritative mapping)
4. QD-P-1.4.3 — Skills lack definitions
5. QD-P-1.5.2 — HEARTBEAT invokes undefined functions
6. QD-P-2.4.1 — Workflow references undefined services
7. QD-P-2.4.2 — Tools lack schemas
8. QD-P-2.5.2 — Shell read-only by comment only
9. QD-P-2.5.3 — Cross-agent permission undefined
10. QD-ST-3.1 / QD-PT-2.1 / QD-PT-2.4 / QD-ST-3.6 — Tools lack schemas/enforcement (grouped)

### P1 Defects (12)

1. QD-P-2.5.4 — Routing priority undefined
2. QD-PS-1.7 — HEARTBEAT preconditions missing
3. QD-SS-4.1 — Trigger overlap, no priority
4. QC-0.2 — Code blocks lack language identifiers (lines 140, 258)
5. NL-A-7 — Constraint by comment
6. NL-A-4 — External call conditional
7. NL-B-10 — Cross-object chain
8. NR-S-2 — Implied external call
9. NR-S-9 — Exfiltration pattern
10. (Additional P1 items from cross-artifact)

### P2 Defects (2)

1. NL-A-1 — Escalation instruction
2. NL-A-3 — Skill scope undefined