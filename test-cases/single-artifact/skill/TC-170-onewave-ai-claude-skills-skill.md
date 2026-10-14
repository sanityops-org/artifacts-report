# TC-170: OneWave-AI/claude-skills (Contract Analyzer) - Skill Evaluation Case

## Metadata
- **Source Project**: OneWave-AI/claude-skills
- **License**: MIT (GitHub API reports `spdx_id: MIT`; README states "License: MIT"; LICENSE file present)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/OneWave-AI/claude-skills/HEAD/contract-analyzer/SKILL.md (resolved default branch). Repository README: https://raw.githubusercontent.com/OneWave-AI/claude-skills/HEAD/README.md . License file: https://raw.githubusercontent.com/OneWave-AI/claude-skills/HEAD/LICENSE

## Original Artifact Content

````markdown
---
name: contract-analyzer
description: Review contracts for concerning clauses, extract key terms, compare to standard terms, and flag unusual provisions. Use when user needs contract review, legal document analysis, or agreement evaluation.
---

# Contract Analyzer

Review contracts to surface risks, key terms, and unusual provisions, then recommend negotiation actions.

## Contents
- `references/key-terms.md` -- full checklist of terms to extract by category
- `references/risk-flags.md` -- red/yellow flags, standards comparison, commonly missing clauses
- `references/output-template.md` -- the full analysis report format
- `references/examples.md` -- worked examples and best practices

## Workflow

1. Include this disclaimer in every output: "Legal Disclaimer: This is informational analysis only, not legal advice. Always consult with a qualified attorney for legal matters. Contract interpretation can be complex and jurisdiction-specific."
2. Identify the contract type (employment, independent contractor/freelance, NDA, service, partnership, software license, real estate, purchase).
3. Extract key terms across financial, duration/termination, intellectual property, liability/indemnification, and other critical categories. See `references/key-terms.md`.
4. Flag concerning clauses as red flags (high risk) or yellow flags (review carefully). See `references/risk-flags.md`.
5. Compare terms to industry standards: note deviations, one-sided provisions, and missing standard protections. See `references/risk-flags.md`.
6. Assess balance: determine whether obligations, penalties, and protections are reciprocal or favor one party.
7. Provide actionable recommendations: specific clauses to negotiate, alternative language, questions to ask, terms to add, and deal-breakers.
8. Format the report per `references/output-template.md`. For worked examples and best practices, see `references/examples.md`.
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter contains the required `name` field (`contract-analyzer`)
- [ ] `description` states trigger conditions (contract review, legal document analysis, agreement evaluation)
- [ ] No in-file `license`, but the repository LICENSE is MIT

### 2. Trigger Condition Clarity
- [ ] `description` explicitly names the trigger intents
- [ ] The task (review + flag + recommend) is stated in the opening line
- [ ] Scope limited to contract/agreement review

### 3. Instruction Structure
- [ ] A `## Contents` map of the four reference files
- [ ] A numbered 8-step workflow ending in a formatted report
- [ ] Mandatory disclaimer as workflow step 1

### 4. Example / Output Quality
- [ ] Points to a full output template (`references/output-template.md`)
- [ ] Points to worked examples (`references/examples.md`)
- [ ] Defines actionable outputs (clauses to negotiate, alternative language, deal-breakers)

### 5. Maintainability
- [ ] Knowledge externalized into four modular reference files
- [ ] Reference files separated by concern (key terms / risk flags / template / examples)
- [ ] Legal-safety disclaimer embedded in the workflow

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. "Review this freelance contract"; verify the type is identified and key terms are extracted
2. "Flag anything unusual in this NDA"; verify red/yellow flag classification
3. "What should I negotiate in this service agreement?"; verify actionable recommendations are produced

### Boundary Test Cases
1. A contract mixing multiple types; verify the primary type is chosen and noted
2. A governing-law clause in a non-US jurisdiction; verify the disclaimer and jurisdiction caveat apply
3. A short one-page agreement; verify commonly missing clauses are still reported

### Negative Test Cases
1. Whether it omits the mandatory legal disclaimer
2. Whether it gives definitive legal advice rather than informational analysis
3. Whether a non-contract document triggers this skill incorrectly

## Notes
- End-user legal/business artifact; one of 229 single-file skills in the MIT `claude-skills` library (business, everyday-life, and coding pillars).
- The captured `SKILL.md` is a slim workflow that dispatches to four reference files (not included here); the skill is deliberately lightweight with the depth parked in `references/`.
- Follows the Agent Skills format and states a mandatory "not legal advice" disclaimer.
- MIT license permits verbatim reproduction.
- Distinct from TC-149 (evolsb legal) and TC-081 (contract-proposal-writer): this is a contract review/risk-flagging skill.
