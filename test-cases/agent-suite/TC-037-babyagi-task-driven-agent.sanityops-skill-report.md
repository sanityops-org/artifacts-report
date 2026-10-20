# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact, Tool Schema only), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (fewer than two same-agent artifact types). Stage D did not run (incomplete artifact set).
- Finding counts (Stage A + B): Inspect P0 = 9, P1 = 0, P2 = 0.
- Gate-0 result: Not passed - G0-3 and G0-4 unsatisfied (no responsibility baseline; no tool field schemas).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-T-1.1 / QD-T-1.2 - The Functionz registration/invocation API declares no tool `name`/`description`/`inputSchema` or `properties`/`required`.
  2. QD-T-3.2 - `__getattr__` routes any attribute name through `executor.execute(name, *args, **kwargs)` (raw passthrough).
  3. QD-T-3.1 / QD-T-4.2 - Registered functions (including the `os` pack) may modify state; no write notice or side-effect declaration.
  4. QD-T-3.3 / QD-T-3.5 - No operation-count limit and no cross-function data-flow boundary.
  5. QD-T-4.1 - No description quality: the schema exposes function names only.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-037 is a single function-orchestration framework (BabyAGI/Functionz) at the pinned commit; it has no natural-language agent prompt and no markdown Skill. Types present, by structural signature:

- System Prompt (absent): no prose/markdown instruction artifact is shown; the case quotes Python framework code only.
- Skill (absent): no markdown with `name`/`description` front matter is shown.
- Tool Schema (present, partial): the Functionz registration/invocation API (`register_function`, `load_functions`, `__getattr__` executor) and the default function packs. Basis: function-calling definitions - registered functions are exposed and callable by name; no JSON `parameters` schema is shown.
- Out of coverage: the `functionz/` core implementation, packs, dashboard and API modules are not quoted; only the shown text is inspected.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 Tool Schema - Functionz registration/invocation API

Tier: **L3** (the executor can run any registered function, including the auto-loaded `os` pack - operation execution). Scope = L3 (16 items).

- QD-T-1.1 | FAIL | evidence: TC-037, the API exposes no tool `name`/`description`/`inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-037, no `properties`/`required` are declared.
- QD-T-1.3 | PASS | evidence: TC-037, no `enum` with duplicate/empty values is present.
- QD-T-1.4 | FAIL | evidence: TC-037, no `additionalProperties` declaration is present.
- QD-T-2.1 | N/A | evidence: TC-037, no typed string parameter is shown (determination basis: no parameter schema).
- QD-T-2.2 | N/A | evidence: TC-037, no typed string parameter is shown (determination basis: no parameter schema).
- QD-T-2.3 | N/A | evidence: TC-037, no typed number parameter is shown (determination basis: no parameter schema).
- QD-T-2.4 | N/A | evidence: TC-037, no typed array parameter is shown (determination basis: no parameter schema).
- QD-T-3.1 | FAIL | evidence: TC-037, registered functions (e.g. the `os` pack) may modify state but declare no write-operation notice.
- QD-T-3.2 | FAIL | evidence: TC-037, `__getattr__` returns `lambda *args, **kwargs: _func_instance.executor.execute(name, *args, **kwargs)` - raw passthrough to arbitrary functions.
- QD-T-3.3 | FAIL | evidence: TC-037, no operation-count/batch limit is declared for the executor.
- QD-T-3.4 | N/A | evidence: TC-037, no control parameter (`tenantId`/`isAdmin`/`token`) is exposed (determination basis: no parameter schema).
- QD-T-3.5 | FAIL | evidence: TC-037, one function's result may be passed to another via the executor with no declared data-flow boundary.
- QD-T-4.1 | FAIL | evidence: TC-037, no description quality - functions are exposed by name only.
- QD-T-4.2 | FAIL | evidence: TC-037, side effects of dynamically loaded packs (e.g. `os`) are not declared.
- QD-T-4.3 | PASS | evidence: TC-037, no competing near-synonym function names are shown.

### 3.A.2 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-037, the `python` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-037, snippets are fenced with `python`.
- QC-0.3 | FAIL | evidence: TC-037, the module snippets reference `Functionz`, `create_dashboard`, `create_api_blueprint` with no imports/definitions shown.
- QC-1.1 | FAIL | evidence: TC-037, `Functionz`, `create_dashboard`, `create_api_blueprint` are undefined in the snippets.
- QC-1.2 | PASS | evidence: TC-037, the shown imports (`flask`, `importlib.util`, `traceback`, `sys`, `os`) are standard-library.
- QC-1.3 | PASS | evidence: TC-037, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-037, no type-mismatched call present.
- QC-2.1 | N/A | evidence: TC-037, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-037, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-037, no high-risk file/network/DB call in the shown snippets (determination basis: no such pattern).
- QC-3.1 | PASS | evidence: TC-037, no unused import present.
- QC-3.2 | FAIL | evidence: TC-037, `Functionz`/`create_dashboard`/`create_api_blueprint` are referenced but never imported/defined.
- QC-3.3 | PASS | evidence: TC-037, no hardcoded demo credential value present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - fewer than two same-agent artifact types present (only a partial Tool Schema is present; no System Prompt or Skill).

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT evaluated - Stage B was Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): NOT passed - the artifact is framework code with no agent role/responsibility baseline.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - the Functionz API exposes no tool name/description/parameter schema.

Gate-0 result: **Not passed - G0-3, G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-3, G0-4; incomplete artifact set
Blocking Reasons:
  G0-3 - no responsibility boundary statements are present in the artifact.
  G0-4 - no Tool Schema field completeness can be verified.
  Incomplete artifact set - no System Prompt or Skill is present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(This is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-037 Tool Schema (Functionz API).

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed natural-language risk text (NL-A / NL-B / NR-O / NR-S) was found. Dynamic function discovery and arbitrary-pack loading are code capabilities; they are not explicitly expressed risk statements, and inferring risk from them is out of Risk Explicit scope.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-T-1.1, QD-T-1.2, QD-T-1.4 | AS-05, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-T-3.1, QD-T-3.5 | AS-03, AS-05 | FM-08, FM-09, FM-10 | Strong (write/data flow undeclared) |
| QD-T-3.2 | AS-02 | FM-08, FM-09, FM-10 | Strong (raw passthrough executor) |
| QD-T-3.3 | AS-05, AS-06 | FM-03, FM-05 | Medium |
| QD-T-4.1, QD-T-4.2 | AS-05, AS-08 | FM-03, FM-05 | Medium |
| QC-0.3, QC-1.1, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Traceability. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-T (Functionz L3), QC. No System Prompt or Skill present.
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present.
Stage C (Gate-0):           Not passed - G0-3, G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (Gate-0 G0-3/G0-4 not satisfied).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
