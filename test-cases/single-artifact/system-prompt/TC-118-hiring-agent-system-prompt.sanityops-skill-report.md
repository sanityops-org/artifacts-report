# SanityOps Inspect Lite - Report

Artifact: TC-118-hiring-agent-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 6, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints; resume content is not declared as untrusted data (indirect-injection / hidden-text surface).
  - QD-P-2.3.4 - no security/privacy filtering declared for candidate PII.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-1.3.2 - vague qualifiers ("real-world impact", "significantly lower scores").
  - QD-P-2.7.1 - positive examples of an expected output are not provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-118-hiring-agent-system-prompt.md` -> **System Prompt** (a Jinja2 system-message template delivered as the `system` message for resume scoring). Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a scoring instruction template with Jinja fragments, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Embedded snippet present (inspected as embedded code, not a standalone file): the Jinja2 template block (`{% if bonus_rules %}` / `{% for rule in bonus_rules %}` and the `{{ bonus_max }}` variable).
- Referenced-but-not-supplied: `criteria.jinja` (evaluation criteria) and `role.json` (weights/caps). Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the prompt scores one resume against one role and returns one JSON object; no tool invocations, no multi-turn dialogue, and no complex workflow are declared. L1 criteria satisfied (single skill; no tool invocations; no multi-turn dialogue; no complex reasoning); L2/L3 criteria not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-118 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-118 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-118 - the mandated JSON field list is consistent with the category names scored in the body.
- QD-P-1.2.1 | PASS | evidence: TC-118 - the "expert technical recruiter" role supports the scoring task.
- QD-P-1.2.2 | PASS | evidence: TC-118 - the JSON-scoring output style matches the evaluator role.
- QD-P-1.2.3 | PASS | evidence: TC-118 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-118 - quantifiers ("ALL FIVE categories", "1-5 items") are bounded and numeric.
- QD-P-1.3.2 | FAIL | evidence: TC-118, self_projects section - vague qualifiers used; excerpt: "Complex projects with real-world impact, advanced architecture, or contributions to popular open source projects should receive HIGH SCORES (20-30 points)." (also "significantly lower scores").
- QD-P-1.3.3 | PASS | evidence: TC-118 - behavior is bounded by the fairness exclusions and the numeric score caps.
- QD-P-1.4.1 | PASS | evidence: TC-118 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-118 - the Jinja bonus block is reachable and gated by `{% if bonus_rules %}`.
- QD-P-1.5.1 | PASS | evidence: TC-118 - stated behaviors support the resume-scoring objective.
- QD-P-1.6.1 | PASS | evidence: TC-118 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-118 - no rule keyed on the model's own internal state found.
- QD-P-1.6.3 | PASS | evidence: TC-118 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-118 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-118 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-118 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-118 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-118 - input sources declared (resume text, plus labeled '=== GITHUB DATA ===' and '=== BLOG DATA ===' sections, plus the structured 'profiles' section).
- QD-P-2.2.2 | FAIL | evidence: TC-118 - no input format/encoding/size limits declared for the resume text (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-118 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-118 - missing-data handling declared; excerpt: "Only apply deductions if profiles are genuinely missing from the structured data."
- QD-P-2.3.1 | PASS | evidence: TC-118 - output format declared (a single JSON object with the named fields).
- QD-P-2.3.2 | PASS | evidence: TC-118 - the required field list and score caps are enumerated (candidate_name, scores{...}, bonus_points, deductions, key_strengths, areas_for_improvement).
- QD-P-2.3.4 | FAIL | evidence: TC-118 - no sensitive-data filtering or privacy handling rules declared (absence) for candidate PII (name, demographics) carried in the input.
- QD-P-2.5.2 | FAIL | evidence: TC-118 - no security boundary constraints declared (absence); the resume content is not declared as untrusted data to be treated as data, not instructions.
- QD-P-2.7.1 | FAIL | evidence: TC-118 - no worked positive example of an expected evaluation output is provided (absence).
- QD-P-2.7.2 | FAIL | evidence: TC-118 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-118 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-118, ```jinja block - the Jinja2 template fragment parses as valid template syntax (balanced `{% if %}` / `{% endif %}` and `{% for %}` / `{% endfor %}`).
- QC-0.2 | PASS | evidence: TC-118 - the template is inside a fenced block with an explicit language identifier (`jinja`).
- QC-0.3 | PASS | evidence: TC-118 - the fragment is structurally complete for its scope.
- QC-0.4 | PASS | evidence: TC-118 - the fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-118 - the declared language identifier matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-118 - referenced names (`bonus_rules`, `rule.label`, `rule.tiers`, `loop`, `bonus_max`) are template variables/constructs; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-118 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-118 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-118 - the template performs no file/network/high-risk operations.
- QC-3.1, QC-3.2 | PASS | evidence: TC-118 - no unused/missing imports (no imports).
- QC-3.3 | PASS | evidence: TC-118 - no hardcoded credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-118 - the JSON field names in the template match the field list declared in the prompt body.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in the first line ("You are an expert technical recruiter evaluating resumes.").
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
No explicitly expressed risk item matching an EX classification was found. The fairness instructions ("SCORES MUST NEVER DEPEND ON THE FOLLOWING FACTORS") and the anti-gaming rules ("Having personal GitHub repositories does NOT constitute open source contribution") are constraint statements, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Format Compliance, Consistency, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
