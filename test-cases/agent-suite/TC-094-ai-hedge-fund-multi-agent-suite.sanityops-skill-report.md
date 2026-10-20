# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one Logic Artifact type is present). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A): Inspect P0 = 9, P1 = 2, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present, and the module map lists module names with no parameter schemas).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No persona prompt declares a security boundary or a permission-control boundary.
  2. QD-P-2.2.1 - The input source is undeclared: each persona only references "the data provided" / "the data given".
  3. QD-P-2.2.2 / QD-P-2.2.3 - The fundamentals input has no declared format and no required/optional marking.
  4. QD-P-2.3.4 - No sensitive-data filtering or output privacy constraint is declared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-094 bundles one coordinated multi-agent suite (AI Hedge Fund v2 engine). Artifact types present, by structural signature:

- System Prompt (present, 3 verbatim): the investor-persona system prompts for Buffett (`signals/buffett.py`), Graham (`signals/graham.py`) and Druckenmiller (`signals/druckenmiller.py`). Basis: prose/instruction strings returned by `get_system_prompt()`.
- System Prompt (identified, not quoted, 2): the Munger and Lynch persona prompts exist per the directory listing but their bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): the module map (`data/`, `signals/`, `llm/`, `portfolio/`, `risk/`, `pipeline/`) provides module names and one-line purposes only; no JSON `parameters` schema is shown. `Signal`/`QuantSignals` are data contracts, not Tool Schemas.
- Embedded code snippets (QC scope): the `class <Persona>Agent(LLMAgent)` bodies that carry the prompts.
- Out of coverage: `munger.py`, `lynch.py`, `signals/pead.py`, and the `portfolio/`/`risk/`/`pipeline/`/`brokers/` implementation files are described but not quoted.

Scope note: every persona is a sub-agent of the same orchestrated fund suite (one `AlphaModel` interface, blended by the portfolio module, gated by the risk module, executed by the pipeline). All artifacts belong to the same agent suite, so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (investor-persona agents)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the suite is a multi-agent orchestration (5 LLM personas + 1 quant model blended by a portfolio module, gated by a risk module, executed by a pipeline whose workflow exceeds 5 steps: data -> alpha models -> portfolio -> risk -> execution -> ledger); it is finance/security-sensitive (it drives an investment book). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-094, sections 1.1-1.3, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-094, sections 1.1-1.3, the "Signal rules" and "Hard rules" do not conflict in any scenario.
- QD-P-1.1.3 | PASS | evidence: TC-094, sections 1.1-1.3, no worked example contradicts a rule (only the output schema is shown, and it matches the rules).
- QD-P-1.2.1 | PASS | evidence: TC-094, sections 1.1-1.3, each persona identity (Buffett/Graham/Druckenmiller, a value/inflection investor) matches its checklist responsibility.
- QD-P-1.2.2 | PASS | evidence: TC-094, sections 1.1-1.3, the persona voice matches the output style rule ("<your thesis in Buffett's voice, 2-4 sentences>").
- QD-P-1.2.3 | PASS | evidence: TC-094, sections 1.1-1.3, the constraints (reason only from the data, do not invent numbers) do not prohibit the core evaluation responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-094, sections 1.1-1.3, quantities are bounded ("2-4 sentences", confidence 0-100, "the whole record shown").
- QD-P-1.3.2 | FAIL | evidence: TC-094, sections 1.1-1.3, vague qualifiers carry the signal boundary - e.g. Buffett "a strong, durable business at a reasonable or better price"; Graham "A P/E far above 15-20 demands extraordinary justification you will rarely grant".
- QD-P-1.3.3 | PASS | evidence: TC-094, sections 1.1-1.3, the "Hard rules" declare a prohibition scope ("Reason ONLY from the data provided ... Do not invent numbers") and the JSON schema defines the handoff.
- QD-P-1.4.1 | PASS | evidence: TC-094, sections 1.1-1.3, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-094, sections 1.1-1.3, the bullish/bearish/neutral branches are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-094, sections 1.1-1.3, no Skill definition is given in the persona prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-094, sections 1.1-1.3, the checklist responsibilities support the objective (emit a signal with a thesis).
- QD-P-1.5.2 | PASS | evidence: TC-094, sections 1.1-1.3, the workflow only reasons over the provided snapshot; it declares no unresolved resource/tool invocation.
- QD-P-1.6.1 | PASS | evidence: TC-094, sections 1.1-1.3, the vague words steer an investment-analytical signal rather than a security/permission boundary, and the signal conditions plus the numeric confidence scale are defined.
- QD-P-1.6.2 | PASS | evidence: TC-094, sections 1.1-1.3, control flow keys on the provided fundamentals, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-094, sections 1.1-1.3, the quality-vs-price interweaving is arbitrated - Buffett "neutral: ... a great business at a clearly excessive price"; Graham "A weak balance sheet disqualifies regardless of prospects".
- QD-P-1.6.4 | PASS | evidence: TC-094, sections 1.1-1.3, no constraint fixes an internal reasoning method beyond the checklist structure.
- QD-P-1.6.5 | PASS | evidence: TC-094, sections 1.1-1.3, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-094, sections 1.1-1.3, the assumed availability of fundamentals fields is handled by the insufficient-data rule (go neutral).
- QD-P-1.6.7 | PASS | evidence: TC-094, sections 1.1-1.3, the persona is invoked once per ticker/date over a fixed snapshot and declares no multi-turn update path (determination basis: single-shot evaluation, no conversation).
- QD-P-2.1.1 | PASS | evidence: TC-094, sections 1.1-1.3, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-094, sections 1.1-1.3, the referenced fields (market cap, P/E, EPS, book value per share) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-094, sections 1.1-1.3, the checklist / signal rules / hard rules / schema hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-094, sections 1.1-1.3, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-094, sections 1.1-1.3, the input source, type and acquisition method are undeclared - the prompt only refers to "the data provided" / "the data given".
- QD-P-2.2.2 | FAIL | evidence: TC-094, sections 1.1-1.3, the fundamentals input format is unconstrained (fields such as "market cap, P/E, EPS, and book value per share" are used but no format/encoding/size is declared).
- QD-P-2.2.3 | FAIL | evidence: TC-094, sections 1.1-1.3, no input field is marked required or optional (correctness relies on fields such as current ratio, debt-to-equity, book value).
- QD-P-2.2.4 | PASS | evidence: TC-094, sections 1.1-1.3, missing/insufficient input is handled - "If the data is insufficient to judge, say so and go neutral."
- QD-P-2.3.1 | PASS | evidence: TC-094, sections 1.1-1.3, output format declared - "Respond with JSON only, in exactly this schema".
- QD-P-2.3.2 | PASS | evidence: TC-094, sections 1.1-1.3, output schema fields are declared (signal enum, confidence 0-100, reasoning string).
- QD-P-2.3.3 | PASS | evidence: TC-094, sections 1.1-1.3, the exact-schema requirement plus "JSON only" bounds output format stability.
- QD-P-2.3.4 | FAIL | evidence: TC-094, sections 1.1-1.3, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-094, sections 1.1-1.3, the numbered checklist is a complete step sequence ending in a defined output.
- QD-P-2.4.2 | PASS | evidence: TC-094, sections 1.1-1.3, the persona invokes no tool or resource (vacuous).
- QD-P-2.4.3 | PASS | evidence: TC-094, sections 1.1-1.3, no tool invocation is declared (vacuous).
- QD-P-2.5.1 | PASS | evidence: TC-094, sections 1.1-1.3, no loop, retry, or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-094, sections 1.1-1.3, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-094, sections 1.1-1.3, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-094, sections 1.1-1.3, the signal rules arbitrate the quality-vs-price tension; no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-094, sections 1.1-1.3, no resource invocation is declared (vacuous).
- QD-P-2.6.1 | PASS | evidence: TC-094, sections 1.1-1.3, no tool/network/external call is made and the one applicable anomaly (insufficient data) is handled (go neutral).
- QD-P-2.6.2 | PASS | evidence: TC-094, sections 1.1-1.3, degradation is defined - insufficient data degrades to a "neutral" signal rather than fabricating a thesis.
- QD-P-2.6.3 | PASS | evidence: TC-094, sections 1.1-1.3, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-094, sections 1.1-1.3, no positive worked example is provided (only the output schema shape is shown).
- QD-P-2.7.2 | FAIL | evidence: TC-094, sections 1.1-1.3, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-094, sections 1.1-1.3, no boundary-case examples are provided.

### 3.A.2 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-094 carries no Tool Schema artifact (determination basis: the module map lists module names and one-line purposes, not JSON `parameters` schemas; `Signal`/`QuantSignals` are data contracts). No QD-T verdict is emitted.

### 3.A.3 Embedded code snippets (QC)

QC-0 baseline: the `class <Persona>Agent(LLMAgent)` snippets parse as valid Python (QC-0.1 PASS) and are fenced with `python` (QC-0.2 PASS).

- QC-0.1 | PASS | evidence: TC-094, sections 1.1-1.3, the class snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-094, fenced blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-094, sections 1.1-1.3, each class body is complete (docstring, class attribute, `name` property, and a complete `get_system_prompt` return) and is not truncated.
- QC-1.1 | PASS | evidence: TC-094, the only name undefined within the snippets is the un-imported base class `LLMAgent`; recorded once under QC-3.2.
- QC-1.2 | PASS | evidence: TC-094, no import statement is present to validate.
- QC-1.3 | PASS | evidence: TC-094, no API call is present in the snippets.
- QC-1.4 | PASS | evidence: TC-094, `get_system_prompt` is annotated `-> str` and returns a string; no type-mismatched call.
- QC-2.1 | N/A | evidence: TC-094, no file-handle pattern in the snippets (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-094, no network-connection constructor in the snippets (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-094, no high-risk file/network/DB call in the snippets (determination basis: no such pattern).
- QC-3.1 | PASS | evidence: TC-094, no import is present, so no unused import exists.
- QC-3.2 | FAIL | evidence: TC-094, sections 1.1-1.3, `LLMAgent` is referenced as the base class but is never imported or defined in the snippets.
- QC-3.3 | PASS | evidence: TC-094, `investment_approach = "long_only"` is a class configuration value, not a hardcoded demo credential or machine-specific value.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the five persona prompts plus the quant model are independent `AlphaModel` implementations blended by the portfolio module; no cyclic role orchestration (Agent A calling Agent B and back) is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each persona prompt states its role and responsibilities (e.g. section 1.1 "You are Warren Buffett, evaluating a single company as a long-term business owner, not a trader." followed by the numbered checklist).
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the module map lists module names with no parameter schemas).

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill, no Tool Schema).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-094 System Prompt set (3 persona prompts) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The "Hard rules" (reason only from the data provided, do not use post-filing knowledge, do not invent numbers, go neutral on insufficient data) are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional (qualitative signal boundary may drift) |
| QD-P-2.2.1, QD-P-2.2.2, QD-P-2.2.3 | AS-01, AS-02 | FM-01, FM-04 | Medium (input source/format/necessity undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Consistency, Robustness, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 3 persona prompts), QD-T (N/A, no Tool Schema), QC (embedded snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
