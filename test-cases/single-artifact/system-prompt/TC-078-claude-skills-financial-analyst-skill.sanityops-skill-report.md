# SanityOps Inspect Lite - Report

Artifact: TC-078-claude-skills-financial-analyst-skill.md (System Prompt / Agent Role Definition)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L3): P0 = 18, P1 = 1, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-1.3.3 - authorization/prohibition boundary scope not declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.6.1 - no runtime exception handling declared.
  - QD-P-2.6.2 - no degradation/recovery strategy declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Stage A - System Prompt inspection (QD-P)

Tier determination: L3 (Complex Agent). Basis: frontmatter declares 5 tools ([Read, Write, Bash, Grep, Glob]) = 4+ tool invocations; six multi-step workflows; finance domain. Two or more L3 criteria are satisfied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-078, full prompt - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-078, Core Workflows - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-078, Integration Examples / Core Workflows - examples consistent with body rules.
- QD-P-1.2.1 | PASS | evidence: TC-078, Role & Expertise - role supports the listed workflows.
- QD-P-1.2.2 | PASS | evidence: TC-078, Output Standards - output style matches the analyst role.
- QD-P-1.2.3 | PASS | evidence: TC-078 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-078, Output Standards - "All models include key assumptions section" is a scoped quantifier.
- QD-P-1.3.2 | PASS | evidence: TC-078 - no constraining vague qualifier on a critical behavior found.
- QD-P-1.3.3 | FAIL | evidence: TC-078, Role & Expertise - authorization scope, prohibition scope, and handoff conditions are not declared; excerpt: "Financial analyst covering valuation, ratio analysis, forecasting, and industry-specific financial modeling".
- QD-P-1.4.1 | PASS | evidence: TC-078 - no duplicated constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-078 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-078, Skill Integration - skills are declared; external validity is not verifiable in single-artifact isolation.
- QD-P-1.5.1 | PASS | evidence: TC-078 - responsibilities support the stated objective.
- QD-P-1.5.2 | PASS | evidence: TC-078, Skill Integration - workflow-referenced scripts and references are declared.
- QD-P-1.6.1 | PASS | evidence: TC-078 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-078 - no rule keyed on model internal state (uncertainty/intent/confidence) found.
- QD-P-1.6.3 | PASS | evidence: TC-078 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-078 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-078 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-078 - no behavior-visible rule keyed on an unstated assumption found beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-078 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | PASS | evidence: TC-078 - prompt is well-formatted and consistently structured.
- QD-P-2.1.2 | PASS | evidence: TC-078, Skill Integration - referenced files/scripts are enumerated.
- QD-P-2.1.3 | PASS | evidence: TC-078 - clear section hierarchy.
- QD-P-2.1.4 | PASS | evidence: TC-078 - concise, no verbosity defect found.
- QD-P-2.2.1 | PASS | evidence: TC-078, Core Workflows - input sources declared (user-supplied data; script input files).
- QD-P-2.2.2 | FAIL | evidence: TC-078, Core Workflows - no input data format/encoding/size limits declared; excerpt: "python ../../finance/skills/financial-analyst/scripts/ratio_calculator.py financial_data.json --format json".
- QD-P-2.2.3 | FAIL | evidence: TC-078, Core Workflows - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-078, Core Workflows - handling when a required input is missing not defined (absence).
- QD-P-2.3.1 | PASS | evidence: TC-078, Output Standards - output form declared per deliverable.
- QD-P-2.3.2 | FAIL | evidence: TC-078, Output Standards - no field-level output schema declared (absence).
- QD-P-2.3.3 | FAIL | evidence: TC-078 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-078 - no sensitive-data filtering or privacy handling rules declared (absence) for a finance-data agent.
- QD-P-2.4.1 | PASS | evidence: TC-078, Core Workflows - workflows expose ordered steps.
- QD-P-2.4.2 | PASS | evidence: TC-078, Skill Integration / frontmatter tools - resources and tools declared.
- QD-P-2.4.3 | FAIL | evidence: TC-078 - no tool invocation parameter/sequence/failure specification declared (absence).
- QD-P-2.5.1 | FAIL | evidence: TC-078 - no termination constraints (loops/retries/iteration caps) declared (absence).
- QD-P-2.5.2 | FAIL | evidence: TC-078 - no prohibition/security boundary constraints on the granted tools declared (absence).
- QD-P-2.5.3 | FAIL | evidence: TC-078, frontmatter tools "tools: [Read, Write, Bash, Grep, Glob]" - permission control boundaries not declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-078 - arbitration rules for potentially conflicting constraints not defined (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-078 - resource invocation frequency limits not declared (absence).
- QD-P-2.6.1 | FAIL | evidence: TC-078 - runtime exception handling (tool/parse/external failure) not declared (absence).
- QD-P-2.6.2 | FAIL | evidence: TC-078 - degradation and recovery strategy not declared (absence).
- QD-P-2.6.3 | FAIL | evidence: TC-078 - no retry mechanism (bounded) declared (absence).
- QD-P-2.7.1 | FAIL | evidence: TC-078, Integration Examples - only script-invocation examples; behavior-level positive examples insufficient (absence).
- QD-P-2.7.2 | FAIL | evidence: TC-078 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-078 - no boundary-case examples (empty/oversized/anomalous input) provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-078, Integration Examples - bash snippets parse as valid shell syntax.
- QC-0.2 | PASS | evidence: TC-078, Integration Examples - fenced block carries explicit language identifier (`bash`).
- QC-0.3 | PASS | evidence: TC-078, Integration Examples - snippets are complete invocation commands.
- QC-1.1..1.4, QC-2.1..2.3, QC-3.1..3.3 | PASS | evidence: TC-078 - embedded snippets are shell invocation commands only (external .py scripts are referenced files, not embedded code); no undefined names, invalid imports, unclosed handles, missing imports, or hardcoded credentials detected.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - "Role & Expertise" and "Core Workflows" are locatable.
- G0-4 (each Tool Schema name/description/parameter descriptions complete): FAIL - no Tool Schema is supplied; field-by-field completeness cannot be verified.
- Gate-0 result: Not passed - G0-4.

## Stage D - Permission proportionality (QD-PM, Quick Mode)
Not Executed - incomplete artifact set (Gate-0 G0-4 unsatisfied; no Tool Schema supplied).

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - no Tool Schema supplied; operation semantics undeterminable; permission items cannot be categorized.
Remediation Actions: Fix above upstream items, then re-run Gate-0

(Wording note: the Permission stage was "Not Executed" because Gate-0 was not satisfied; it is not reported as FAIL and no ERROR/BLOCKED status is asserted.)

## Stage E - Risk Explicit (EX) - physically separated from Inspect verdicts
Scan scope: System Prompt static text (NL-A / NL-B / NR-O / NR-S).
Findings: none.
No explicitly expressed risk item (conversation/content leakage, tampering, privilege escalation, dangerous structured flags, hardcoded secrets/PII, obfuscation) matching an EX classification was found in the artifact text. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: this section is advisory context, not a verdict. It is based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.3 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium - boundary gap may permit out-of-scope behavior under some conditions |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium - needs dynamic verification of malformed input handling |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.2 | AS-03, AS-09 | FM-06 | Conditional - depends on downstream parser presence |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium - candidate association with data-output handling |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.1 | AS-06 | FM-08, FM-09, FM-10 | Conditional - depends on runtime loop presence |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium - candidate association with boundary handling |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.6.1 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.6.3 | AS-06, AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response (Prompt security/boundary and example-design groups). The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
