# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-142-youtube-skills-youtube-full-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 0, P1 = 0, P2 = 0. Embedded-code QC: 0 defects (QC-0 baseline PASS; QC-1..3 Not Applicable - the snippets are HTTP/JSON, not Python/typed code).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect): none - no QD-S defect was located in the L2 mandatory set.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-142, YAML front matter carries `name`, `description`, `version`, `compatibility`, and `required_environment_variables`.
QD-S-0.2 | PASS | evidence: TC-142, all required fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-142, the YAML front matter parses (including an inline JSON `metadata` value).
QD-S-0.4 | PASS | evidence: TC-142, field values match expected types (strings and lists).
QD-S-0.5 | PASS | evidence: TC-142, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-142, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the Skill makes network requests to an external system (transcriptapi.com) using an API key -> external system access / resource access, at least L2; no delete or irreversible operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | PASS | evidence: TC-142, "Search". Excerpt: "| `q` | yes | - | 1-200 chars |" and "| `limit` | no | `20` | 1-50 |" - input parameters carry explicit upper bounds.
QD-S-1.3 | PASS | evidence: TC-142, "Errors". Excerpt: "| 408 | Timeout | Retry once after 2s |" and "| 429 | Rate limited | Wait, respect Retry-After |" - a bounded retry policy is declared.
QD-S-2.1 | PASS | evidence: TC-142, no unbounded quantity wording (all/every/entire/complete) attached to a processing instruction was located.
QD-S-2.2 | PASS | evidence: TC-142, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | PASS | evidence: TC-142, front matter description. Excerpt: "Not for uploads, account management, or written-source-only research." - an explicit out-of-scope (non_goals) declaration is present.
QD-S-4.1 | PASS | evidence: TC-142, "Errors" table. Excerpt: "| 401 | Bad API key | Check key |", "| 403/1010 | Cloudflare block | Add or fix User-Agent header |" - failure behavior is declared with actions.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): No defect - the description states the capability scope and explicit exclusions ("Not for uploads, account management, or written-source-only research.").
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set; positive triggers are enumerated and negative scope is stated ("Not for uploads...").
INPUT (QD-S-1.1, QD-S-3.3): No defect - input parameters carry explicit bounds (`q` 1-200 chars, `limit` 1-50).
EXECUTION (QD-S-1.3, QD-S-5.4): No defect - a bounded retry policy is declared in the Errors table.
OUTPUT (QD-S-1.2, QD-S-2.3): No defect at the L2 mandatory set; a sample JSON response and response shapes are documented (QD-S-1.2 is outside the L2 mandatory set).
FAILURE (QD-S-4.x): No defect - error codes map to actions.

### 2.5 Defect list (sorted P0 first)

None. No P0, P1, or P2 defect was located in the L2 mandatory set.

### 2.6 QC - embedded code contract (QC-0 baseline first)

Embedded snippets: several fenced `http` request blocks and one fenced `json` response block.
QC-0.1 | PASS | the request/response snippets are well-formed for their declared formats.
QC-0.2 | PASS | language identifiers (`http`, `json`) are present.
QC-0.3 | PASS | the snippets are complete (request line + headers; full JSON body).
QC-1.1, QC-1.2, QC-1.3, QC-1.4, QC-2.1, QC-2.2, QC-2.3, QC-3.1, QC-3.2, QC-3.3 | Not Applicable | the embedded snippets are HTTP/JSON, not Python/typed code; these sub-checks target Python/typed snippets.
QC-3.3 note: the API key is referenced as the environment variable `$TRANSCRIPT_API_KEY`, not a hardcoded literal - no demo-credential pattern.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): Satisfied - Stage A records no unfixed P0 finding.
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Satisfied - the description states scope and exclusions ("Not for uploads, account management, or written-source-only research.").
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text: no data-exfiltration instruction, no encoded payload, no zero-width/homoglyph obfuscation, no dangerous config flag, and no hardcoded credential or PII (the API key is referenced by variable name only). This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

No Stage A FAILs occurred, so no Impact Card is emitted (mapping is performed only for defects that actually FAILED inspection).

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - no FAIL to map (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
