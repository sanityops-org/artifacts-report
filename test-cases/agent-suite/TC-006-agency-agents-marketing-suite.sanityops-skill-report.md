> **STALE (2026-10-20)**: the inspected artifact was replaced with upstream-verified content. Re-run the inspection before using these findings.

# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one artifact type present); Stage D did not run (incomplete artifact set).
- Finding counts (Stage A): Inspect P0 = 4, P1 = 4, P2 = 0.
- Gate-0 result: Passed (G0-3 satisfied; G0-4 vacuously satisfied - no Tool Schema in the set).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.4.2 - Workflow steps reference resources/actions (SEO audit, analytics pull) but no resource or tool is declared.
  2. QD-P-1.5.2 - The workflow requires resources the artifact set does not include.
  3. QD-P-2.2.4 - No handling is defined for a missing or incomplete brief.
  4. QD-P-2.3.4 - No security/privacy filtering is declared for content that touches community data.
  5. QD-P-1.6.2 - "Submit for approval (if required)" depends on unobservable model judgment.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was applied in Stage A (no executable snippets present).
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-006 is a role-definition library (marketing department). Artifact types present, by structural signature:

- System Prompt (present, 6 role definitions): content-creator, reddit-community-builder, growth-hacker, social-media-strategist, seo-specialist, linkedin-content-creator. Basis: prose role/persona definitions (identity, mission, rules, workflow, deliverables).
- Skill (absent as classified): the role definitions carry `name`/`description` front matter, which is also the Skill structural signature; however their bodies are persona and role instructions rather than a discrete invokable capability, so they are classified as System Prompts here.
- Tool Schema (absent): no JSON Schema / function-calling definition.

Edge case recorded: if the user re-declares these role files as Skills (front-matter signature), the QD-S checklist would apply instead of QD-P. The current classification is stated so the user can correct it.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (6 role definitions)

Tier determination: **L2 Multi-turn Interactive**. Basis (any 2 or more of the L2 criteria): a simple top-level workflow of 4 phases (<=5 steps); limited state (content calendar / campaign state); iterative content optimization implying multi-turn engagement. No tools are declared. Scope = L2 (40 items).

- QD-P-1.1.1 | PASS | evidence: TC-006, sections 1-6, no mutually exclusive attributes found within a role.
- QD-P-1.1.3 | PASS | evidence: TC-006, section 1 "Examples" (Good/Bad) are consistent with the stated rules.
- QD-P-1.2.1 | PASS | evidence: TC-006, each role Identity matches its Core Mission.
- QD-P-1.2.3 | PASS | evidence: TC-006, section 2 "NEVER use multiple accounts to upvote (vote manipulation)" does not prohibit the core mission.
- QD-P-1.5.1 | PASS | evidence: TC-006, each role's responsibilities support its Core Mission.
- QD-P-2.2.1 | PASS | evidence: TC-006, section 1 Phase 1 "Review content calendar and brief" declares the input source.
- QD-P-2.3.4 | FAIL | evidence: TC-006, sections 1-6 declare no sensitive-data filtering or privacy handling for content touching community/user data.
- QD-P-2.5.2 | PASS | evidence: TC-006, section 5 "NEVER use black-hat techniques (cloaking, hidden text, link schemes)" sets a prohibited-operation boundary.
- QD-P-1.3.3 | PASS | evidence: TC-006, each role's "Critical Rules" define the behavioral boundary.
- QD-P-1.5.2 | FAIL | evidence: TC-006, section 5 Phase 1 "Run technical SEO audit" and section 3 "Analyze current funnel metrics" require resources that are not declared.
- QD-P-1.6.1 | PASS | evidence: TC-006, section 1 "MUST include clear call-to-action" is a clear rule.
- QD-P-2.2.2 | PASS | evidence: TC-006, input is a content brief (natural language), no structured parser defined (not triggered).
- QD-P-2.2.3 | PASS | evidence: TC-006, no parameterized input is declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-006, sections 1-6 declare no handling for a missing or incomplete brief.
- QD-P-2.3.1 | PASS | evidence: TC-006, section 1 "Blog Post" / "Social Media Post" templates define output format.
- QD-P-2.3.2 | PASS | evidence: TC-006, outline/fields are enumerated in the deliverable templates.
- QD-P-2.4.2 | FAIL | evidence: TC-006, sections 1-6 reference analysis/audit actions but declare no database, API, or tool resource.
- QD-P-2.4.3 | PASS | evidence: TC-006, no tool is declared, so no invocation specification is defined to be missing (subsumed by QD-P-2.4.2).
- QD-P-1.2.2 | PASS | evidence: TC-006, each role Voice matches its output style.
- QD-P-1.3.1 | PASS | evidence: TC-006, section 6 "max 20% promotional" and "3-5 pieces/week" are bounded.
- QD-P-1.3.2 | FAIL | evidence: TC-006, section 1 "AVOID generic fluff" uses a vague qualifier.
- QD-P-1.4.1 | PASS | evidence: TC-006, no duplicate constraint found within a role.
- QD-P-1.4.2 | PASS | evidence: TC-006, all four workflow phases are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-006, no Skill definition is present in the prompts (vacuous).
- QD-P-1.6.2 | FAIL | evidence: TC-006, section 1 Phase 4 "Submit for approval (if required)" is keyed on unobservable model judgment.
- QD-P-1.6.3 | PASS | evidence: TC-006, section 1 "professional for B2B, conversational for social" does not conflict with the other soft rules.
- QD-P-1.6.4 | PASS | evidence: TC-006, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-006, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-006, no explicit unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-006, no rule requires revising earlier conclusions on new information.
- QD-P-2.3.3 | FAIL | evidence: TC-006, sections 1-6 declare success metrics but no output stability/consistency assurance mechanism.
- QD-P-2.4.1 | PASS | evidence: TC-006, each role's 4-phase workflow is complete.
- QD-P-2.5.1 | PASS | evidence: TC-006, workflows terminate at "Publish"/"Report" phases.
- QD-P-2.5.3 | PASS | evidence: TC-006, roles perform content work only; no permission-bearing system operation is declared.
- QD-P-2.5.4 | PASS | evidence: TC-006, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | PASS | evidence: TC-006, no resource invocation is declared (not triggered).
- QD-P-2.7.1 | PASS | evidence: TC-006, sections 1 and 2 provide positive examples.
- QD-P-2.7.2 | PASS | evidence: TC-006, section 1 provides counter-examples ("Bad Output").
- QD-P-2.7.3 | FAIL | evidence: TC-006, sections 1-6 provide no boundary-case examples (empty/oversized/ambiguous brief).

### 3.A.2 Embedded snippets (QC)

The fenced blocks are declarative document templates (` ```template `), not executable code.

- QC-0.1 | N/A | evidence: TC-006 template blocks are not executable code (determination basis: no target-language syntax to parse).
- QC-0.2 | PASS | evidence: TC-006 fenced blocks declare a language identifier (`template`).
- QC-0.3 | N/A | evidence: TC-006 template blocks are declarative (determination basis: no imports or executable body expected).
- QC-1.1 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-1.2 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-1.3 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-1.4 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-2.1 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-2.2 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-2.3 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-3.1 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-3.2 | N/A | evidence: no executable code snippet present (determination basis: not triggered).
- QC-3.3 | N/A | evidence: no executable code snippet present (determination basis: not triggered).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - fewer than two same-agent artifact types present (only the System Prompt type is present; no Skill and no Tool Schema).

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied (QD-P-2.3.4, QD-P-1.5.2, QD-P-2.2.4, QD-P-2.4.2) - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each role states Identity and Core Mission (e.g., section 1 "Role: Multi-platform content strategist and writer").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): satisfied vacuously - no Tool Schema is present in the artifact set.

Gate-0 result: **Passed** (G0-3 satisfied; G0-4 vacuously satisfied).

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: none at Gate-0; blocking precondition is the artifact set.
Blocking Reasons:
  The full artifact set required for permission quick mode is incomplete - no Skill and no Tool Schema are present (only the System Prompt type).
Remediation Actions: Provide the Skill and all Tool Schemas for the same agent, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-006 System Prompt set (6 role definitions).
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression was found in the static artifact text. Ethical/prohibited-behavior rules (e.g., "NEVER use black-hat techniques", "AVOID dark patterns") are constraints, not risk expressions, and are not graded here. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-1.5.2, QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium (workflow resources undeclared) |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Conditional |
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Consistency, Format Compliance. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L2, System Prompt set) + QC (no executable snippets).
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present.
Stage C (Gate-0):           Passed - G0-3 satisfied; G0-4 vacuously satisfied (G0-1 informational).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
