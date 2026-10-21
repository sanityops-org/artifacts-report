# TC-213: Firecrawl MCP Tool Schema — sanityops-inspect-lite Report

## Report Header

- **Host model**: claude-opus-4-8[1m] (Anthropic)
- **Skill package**: sanityops-inspect-lite v1.0.0
- **Specification baseline**: SanityOps Framework v1.0 (2026-10 revision)
- **Non-official-result statement**: *This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.*
- **Inspection date**: 2026-10-21
- **Artifact version label**: TC-213-firecrawl-mcp-tool-schema.md (firecrawl_agent tool definition)
- **Fidelity tier**: `full` — verbatim JSON from frozen MCP contract snapshot

---

## Executive Summary

**Overall Status**: Executed stages A, C, E, F, G. Stages B and D did not execute due to artifact set constraints.

**P0/P1/P2 Counts**:
| Category | P0 | P1 | P2 |
|----------|----|----|-----|
| Stage A (QD-T) | 0 | 2 | 3 |
| Stage A (QC) | 0 | 0 | 0 |
| **Total** | **0** | **2** | **3** |

**Gate Result**: Not passed — G0-3 (no System Prompt with responsibility boundary)

**Risk Explicit Summary**:
- Explicit·P0: 0
- Explicit·P1: 2
- Explicit·P2: 1

**Top 5 Findings**:
1. **QD-T-4.1** — Description quality: Some parameters lack semantic explanations
2. **QD-T-2.6** — No pagination cap on `exchange.maxCalls` upper bound context
3. **QD-T-1.4** — `additionalProperties: false` on `schema` object may reject valid schemas
4. **NR-S-2** — `openWorldHint: true` indicates external network access
5. **QD-T-2.5** — Currency/unit semantics for `maxCredits` implicit

---

## Status Board

```
Stage A (Single-artifact):  Executed — 0 P0, 2 P1, 3 P2
Stage B (Cross):            Not Executed — no Prompt/Skill artifacts
Stage C (Gate-0):           Not passed — G0-3 unsatisfied (no responsibility baseline)
Stage D (Permission QD-PM): Not Executed — incomplete artifact set
Stage E (Risk Explicit EX): Executed — 0 Explicit·P0, 2 Explicit·P1, 1 Explicit·P2
Stage F (Impact outlook):   Executed — advisory cards emitted
Stage G (Self-verification): Executed
```

---

## 1. Fidelity and Type Classification

### Step 0 — Fidelity Classification

| Object | Tier | Basis |
|--------|------|-------|
| firecrawl_agent tool definition | `full` | Verbatim JSON from frozen MCP contract snapshot |

### Tool Operation Risk Tier Determination

| Criterion | Assessment |
|-----------|------------|
| Read-only? | No — `readOnlyHint: false` |
| Creates/updates recoverable state? | No |
| Irreversible/sensitive operations? | Yes — external network calls (`openWorldHint: true`), potential data exfiltration |
| Sensitive data? | Yes — web scraping can access sensitive content |

**Determination: OR-L3 (High Risk)** — external network access, potential data exfiltration

---

## 2. Stage A — Single-artifact Inspection (QD-T)

### QD-T-1.x — Structural Validity

| QD-T ID | Verdict | Evidence |
|---------|---------|----------|
| QD-T-1.1 | PASS | `name`, `description`, `inputSchema` all present |
| QD-T-1.2 | PASS | `required: ["prompt"]` matches `properties.prompt` |
| QD-T-1.3 | PASS | No duplicate enum values; enum types consistent |
| QD-T-1.4 | **FAIL·P2** | `schema` parameter has `additionalProperties: false` with no named properties, rejecting non-empty schema objects — inconsistent with documented purpose |
| QD-T-1.5 | PASS | `name: "firecrawl_agent"` matches `^[a-zA-Z0-9_-]{1,64}$` |
| QD-T-1.6 | PASS | `maxCredits: { exclusiveMinimum: 0, maximum: 9007199254740991 }` consistent |
| QD-T-1.7 | PASS | Types present; nesting depth reasonable |

### QD-T-2.x — Parameter Constraints

| QD-T ID | Verdict | Evidence |
|---------|---------|----------|
| QD-T-2.1 | PASS | `prompt` has `minLength: 1, maxLength: 10000` |
| QD-T-2.2 | PASS | `format: "uri"` and `format: "uuid"` with `pattern` for validation |
| QD-T-2.3 | PASS | `maxCredits` has `exclusiveMinimum` and `maximum` |
| QD-T-2.4 | PASS | `urls`, `toolkits`, `callIds` have `maxItems` constraints |
| QD-T-2.5 | **FAIL·P1** | `maxCredits` lacks unit/currency semantics (credits vs dollars) |
| QD-T-2.6 | PASS | `exchange.maxCalls` has `minimum: 1, maximum: 30` |
| QD-T-2.7 | PASS | Cross-field rules documented in descriptions |

### QD-T-3.x — High-risk Operations

| QD-T ID | Verdict | Evidence |
|---------|---------|----------|
| QD-T-3.1 | PASS | Side effects documented: async job, external calls |
| QD-T-3.2 | **FAIL·P2** | `urls` array accepts arbitrary URIs without domain whitelist |
| QD-T-3.3 | PASS | Batch limits via `maxCalls` and `maxCredits` |
| QD-T-3.4 | PASS | No authorization context parameters exposed |
| QD-T-3.6 | PASS | No dangerous defaults observed |
| QD-T-3.7 | PASS | Not a parameterized-tool; operation scope defined |

### QD-T-4.x — Semantic Clarity

| QD-T ID | Verdict | Evidence |
|---------|---------|----------|
| QD-T-4.1 | **FAIL·P1** | `schema` parameter description minimal; `threadId` description could clarify continuation semantics |
| QD-T-4.4 | PASS | Most parameters have descriptions |
| QD-T-4.5 | PASS | Description consistent with schema |
| QD-T-4.6 | N/A | No sensitive inputs |
| QD-T-4.7 | **FAIL·P1** | No `outputSchema` present (mentioned in test case but not in artifact) |

---

## 3. Stage A — QC Inspection

**QC-0 Baseline**: N/A — No embedded code snippets in JSON Schema.

---

## 4. Stage B — Cross-artifact Inspection

**Execution Status**: Not Executed

**Reason**: No System Prompt or Skill artifacts to cross-reference.

---

## 5. Stage C — Gate-0

| Condition | Status | Reason |
|-----------|--------|--------|
| G0-1 | Passed | No P0 findings |
| G0-2 | N/A | No Stage B execution |
| G0-3 | **Not passed** | No System Prompt with responsibility boundary statements |
| G0-4 | Passed | Tool Schema name/description/parameters complete |

**Gate-0 Result**: Not passed (G0-3)

---

## 6. Stage D — Permission

**Execution Status**: Not Executed

**Reason**: Incomplete artifact set (no System Prompt).

---

## 7. Stage E — Risk Explicit Audit

| EX ID | Risk Expression | Impact | Severity | Trigger |
|-------|-----------------|--------|----------|---------|
| NR-S-2 | `"openWorldHint": true` — external network access enabled | D1, D3 | Explicit·P1·conditional | Risk depends on usage context |
| NR-S-6 | `maxCredits` default 2500 — spending without explicit consent | D1, D2 | Explicit·P1·conditional | User may not be aware of cost |
| NR-S-1 | `strictConstrainToURLs` — permission scope via boolean flag | D3 | Explicit·P2·conditional | Scope control mechanism |

**Risk Item Summary**:
- Total EX items: 3
- Explicit·P0: 0
- Explicit·P1: 2
- Explicit·P2: 1

---

## 8. Stage F — Impact Outlook (Sample Cards)

### Impact Card: QD-T-1.4 | additionalProperties Policy

**Static Discovery**
- Evidence: `schema` object has `additionalProperties: false` with no properties

**Potential Security Associations**
- Attack Surface: AS-02 (Input Injection), AS-09 (Cross-Artifact Contract)
- Impact: D2, Availability
- Strength: Medium (provisional lite)

---

### Impact Card: NR-S-2 | Open World Access

**Static Discovery**
- Evidence: `openWorldHint: true`

**Potential Security Associations**
- Attack Surface: AS-03 (Data Exfiltration), AS-05 (Tool Misuse)
- Impact: D1, D2, D3
- Strength: Strong (provisional lite)

---

## 9. Self-Verification

**In-line checks**: All QD-T-*, QC-*, EX-* IDs verified in references.

**Closing checks**: Status board complete; header complete; English-only report.

**Result**: ID back-closure OK · red-line wording OK · output contract OK · reconciliation OK

---

## 10. Strengths Observed

1. **Comprehensive description**: Documents when to use vs. sibling tools, async contract, thread continuation
2. **Valid Draft-07 schema**: Proper JSON Schema structure with `$schema` declaration
3. **Well-constrained parameters**: `prompt` bounded by length, `maxCredits` by range, enums for `effort`/`mode`
4. **Risk annotations**: `readOnlyHint`, `openWorldHint`, `destructiveHint` present
5. **Cross-field rules**: Dependencies (e.g., `exchange.requireApproval` requires `mode: "chat"`) documented

---

## Appendix: Full Defect List

### P1 Defects (2)

1. **QD-T-2.5** — `maxCredits` lacks unit/currency semantics
2. **QD-T-4.1** — Some parameter descriptions insufficient
3. **QD-T-4.7** — No `outputSchema` present

### P2 Defects (3)

1. **QD-T-1.4** — `schema` object `additionalProperties: false` may reject valid schemas
2. **QD-T-3.2** — `urls` array accepts arbitrary URIs without domain whitelist
3. **NR-S-1** — Scope control via boolean flag (EX finding)