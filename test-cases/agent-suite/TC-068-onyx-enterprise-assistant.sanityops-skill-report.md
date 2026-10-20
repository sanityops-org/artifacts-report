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
- Finding counts (Stage A, Skill): Inspect P0 = 1, P1 = 1, P2 = 1.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - No `non_goals` declaration (the skill does not state what it does NOT do).
  2. QD-S-2.1 - Unbounded quantity wording ("describes every Onyx product surface") with no quantity limit.
  3. QD-S-3.2 - No deactivation conditions (the skill does not declare when it should NOT trigger).
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A (no embedded code was found).
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-068 bundles one agent skill (Onyx `feature-map`). Artifact types present, by structural signature:

- Skill (present, 1): `.agents/skills/feature-map/SKILL.md`, markdown with `name`/`description` YAML front matter. Basis: the front-matter signature.
- System Prompt (absent): the skill body is the artifact; no separate prose/system-prompt file is quoted. Basis: no standalone instruction artifact.
- Tool Schema (absent): the skill references companion documents by path (`PATHS.md`, `INDEX.md`, `GLOSSARY.md`, `VERIFYING.md`, `components/`) but exposes no JSON `parameters`/`inputSchema`. Basis: no schema object is present.
- Embedded code snippets (QC scope): none found in the skill body.
- Out of coverage: the companion files named in the body (`PATHS.md`, `INDEX.md`, `GLOSSARY.md`, `VERIFYING.md`, `components/`) were not fetched and are not quoted.

Scope note: the single skill is inspected as one artifact belonging to the Onyx assistant suite.

Tier/level determination (Skill risk level): **L1 (Low Risk)** - text/knowledge-processing and documentation navigation; no tool invocations declared inside the skill; no sensitive data handling; no irreversible operations executed by the skill itself. Determination basis: the skill reads repository markdown knowledge and states a navigation procedure; the "update the doc in the same PR" guidance is repository-maintainer workflow, not an operation the skill executes autonomously. (If one classifies the shared knowledge base as sensitive resource access, the level would rise to L2; the L1 determination is recorded here.) Applied minimum set = QD-S-0 baseline + the 6 L1 mandatory items + the 3 optional items.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 Skill (`feature-map`)

QD-S-0 baseline (entry gate) - all six items checked automatically:

- QD-S-0.1 | PASS | evidence: TC-068, SKILL.md frontmatter, `name` and `description` are present.
- QD-S-0.2 | PASS | evidence: TC-068, SKILL.md frontmatter, both fields carry non-empty content.
- QD-S-0.3 | PASS | evidence: TC-068, SKILL.md frontmatter, the YAML parses.
- QD-S-0.4 | PASS | evidence: TC-068, SKILL.md frontmatter, both values are strings.
- QD-S-0.5 | PASS | evidence: TC-068, SKILL.md frontmatter plus body, no conflicting declarations found.
- QD-S-0.6 | PASS | evidence: TC-068, SKILL.md, the definition meets minimum structural completeness (frontmatter + body procedure).

QD-S-0 baseline PASSED; proceeding to the L1 minimum set.

L1 mandatory items:

- QD-S-1.1 Input Boundary Missing | PASS | evidence: TC-068, SKILL.md, the input is a single lookup key (a code path or a feature name); no unbounded multi-record input applies (determination basis: navigation query, not bulk input).
- QD-S-1.2 Output Size Missing | PASS | evidence: TC-068, SKILL.md, the output is derived from a single component document/verdict set; no bulk output channel is declared (determination basis: bounded navigation output).
- QD-S-2.1 Unbounded Quantity Declaration | FAIL | evidence: TC-068, SKILL.md, unbounded wording carries the scope with no quantity limit - "`.agents/feature-map/` describes every Onyx product surface as one component document".
- QD-S-3.4 Undefined Task Scope | FAIL | evidence: TC-068, SKILL.md, no `non_goals` declaration - the skill states what it does (what a surface does, the code, what a change can break) but not what it does NOT do.
- QD-S-4.1 Undefined Failure Behavior | PASS | evidence: TC-068, SKILL.md, failure/fallback behavior is declared ("A path with no row is unmapped: say so, and read the nearest code and tests yourself"; "Report what you could not verify.").
- QD-S-3.6 Metadata Expression Defects | PASS | evidence: TC-068, SKILL.md, `name: feature-map` and the trigger-oriented description are consistent with the body.

Optional items (recommended, not required):

- QD-S-3.1 Vague Trigger Conditions | PASS | evidence: TC-068, SKILL.md, the description declares specific triggers ("Use it before changing a feature, when reviewing a diff or PR, and when asked what a feature does or how parts connect.").
- QD-S-3.2 Missing Deactivation Conditions | FAIL | evidence: TC-068, SKILL.md, the skill does not declare when it should NOT be triggered (no `forbidden_when`-style condition).
- QD-S-3.3 Missing Ambiguous Input Handling | PASS | evidence: TC-068, SKILL.md, ambiguous/unmapped input is handled ("A path with no row is unmapped: say so"; "confirm names via `GLOSSARY.md`").

### 3.A.2 System Prompt

- QD-P-1.x .. QD-P-2.x | N/A | evidence: TC-068 carries no separate System Prompt artifact (determination basis: only the SKILL.md is provided). No QD-P verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-068 carries no Tool Schema artifact (determination basis: companion documents are referenced by path but no JSON `parameters`/`inputSchema` is present). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

- QC-0.1 .. QC-4.2 | N/A | evidence: TC-068, SKILL.md contains no embedded code snippet (determination basis: prose + path references only). No QC verdict is emitted as PASS/FAIL.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (Skill) is present; no Prompt/Skill/Tool pair exists, so QD-PS, QD-PT, QD-ST and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) is Not Applicable - the artifact defines no multi-agent orchestration.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the skill states its responsibility and scope (e.g. "Use the Onyx feature map (.agents/feature-map/) to learn what a product surface does, the code behind it, and what a change can break.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no System Prompt, no Tool Schema).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-068 Skill (`feature-map`).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifact.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The instructions ("cite only paths and symbols that exist"; "update that document in the same PR") are maintainer-discipline rules, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A (no snippets). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-S-3.4 | AS-01, AS-05 | FM-02, FM-07, FM-09 | Conditional |
| QD-S-2.1 | AS-06, AS-07 | FM-08, FM-10 | Conditional |
| QD-S-3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Relevance, Decomposition Capability, Boundary Recognition, Completeness, Robustness. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-S (L1, feature-map skill), QD-P (N/A, no System Prompt), QD-T (N/A, no Tool Schema), QC (N/A, no embedded snippets).
Stage B (Cross):            Not Executed - only one artifact type present (Skill); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no System Prompt, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
