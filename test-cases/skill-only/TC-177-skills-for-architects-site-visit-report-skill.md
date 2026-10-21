# TC-177: AlpacaLabsLLC/skills-for-architects (Site Visit Report) - Skill Evaluation Case

## Metadata
- **Source Project**: AlpacaLabsLLC/skills-for-architects
- **License**: MIT (LICENSE file present at repo root; Copyright (c) 2026 Alpaca Design Lab LLC)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/AlpacaLabsLLC/skills-for-architects/main/skills/site-visit-report/SKILL.md (default branch `main`). Repository README: https://raw.githubusercontent.com/AlpacaLabsLLC/skills-for-architects/main/README.md . License file: https://raw.githubusercontent.com/AlpacaLabsLLC/skills-for-architects/main/LICENSE

## Original Artifact Content

````markdown
---
name: site-visit-report
description: "Prepare a sourced site-visit record separating direct observations, participant reports, interpretations, limitations and proposed follow-ups."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:site-visit-report

Before acting, read the [host contract](../../docs/host-harness-contract.md), this component's [declaration](host-contract.json) (`skill:site-visit-report`), and applicable [workspace semantics](../../docs/workspace-model.md). Load only the required modes from the [shared catalog](../../corpus/host-contracts.json).

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Apply the receive-owned semantic document rules directly; no installed library, nested skill invocation, runner or executable reconstruction is required. Resolve context before durable work. Existing exact authorization persists; ask only for material missing information or missing permission.

Own authored event documents of kind `site-visit`. Use the [site template](templates/site-visit-report.md). Keep direct observations, participant-reported information, interpretations, issues and proposed actions separate; give stable item labels. Record participants, date, visit scope and access/visibility/weather/testing/equipment/document limits. Inaccessible or concealed work is Not observed, never no issue observed. Do not fabricate photo identity, location, dates or certainty about concealed conditions.

Resolve the project and authorized notes/photos. Distinguish visit, source and created dates. Inspect available photos before describing their content; a filename or caption alone is not visual evidence. Link registered attachments by ID and actual resolved path. This record does not certify code, life-safety, structural, MEP, accessibility, environmental or contractual compliance; route substantive conclusions to the relevant specialist/professional workflow.

## Before changing records

Before persistent changes, follow the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence): **Inspect → Prepare → Verify preparation → Apply → Verify result → Complete**. Inspect pending work first. Finish and verify preparation before the first canonical write: separately reread every saved original and prepared file, check its complete actual bytes, establish durable saving, and inspect actual permissions, ownership and ACLs. Merely writing recovery files does not finish verification. Apply only that verified set. Mark complete only after fresh readback validates the entire affected result and its relationships. Read-only requests and inline drafts need no publication sequence.

Saving a report affects the complete site-visit document plus DOCUMENTS.csv and any explicitly authorized attachment registrations. Prepare and verify that full set before writing the first member. Notes/photos remain source read guards; no project-fact, task or decision promotion belongs to this publication set.

Prepare the report, then resolve confirmed coordinates and register through `documents.register`, kind `site-visit`. An explicit revision is a new document with `supersedes`; preserve old bytes. For client/authority-facing or regulated-conclusion reports, apply the existing [disclaimer procedure](../../rules/professional-disclaimer.md) when applicable, including the required terminal `<!-- architecture-studio:requires-disclaimer -->` marker; do not invent a universal disclaimer for an internal administrative draft.

Reopen the actual report and inspect requested presentation. Only after saving, offer selected project-fact/decision/task promotions with exact item IDs. Report approval alone is not promotion approval. Keep observations, reports and interpretations in their original epistemic category. No silent mutation of PROJECT.md, TASKS.csv or decision records.

`site_visit.prepare` means the authored preparation procedure above; it may produce an inline draft without a workspace write. Persistence uses the shared native document contract, restricted here to kind `site-visit` and authorized attachments. A saved record does not authorize its proposed actions or promote facts/decisions automatically.
````

## Evaluation Dimensions

### 1. Skill Metadata & Trigger Description
- [ ] YAML frontmatter contains `name`, a `description`, and an explicit `allowed-tools` allowlist
- [ ] The `description` states the output contract (a sourced record separating observations, reports, interpretations, limitations, follow-ups)
- [ ] Tool scope is least-privilege (Read/Write/Edit/Glob/Grep/Bash/AskUserQuestion)

### 2. Instruction Structure & Organization
- [ ] Decomposes the task into distinct concerns: context resolution, document ownership, mutation sequence, publication set, promotion boundary
- [ ] Provides an explicit ordered mutation sequence (Inspect → Prepare → Verify → Apply → Verify → Complete)
- [ ] Distinguishes read-only/inline work from persistent publication

### 3. Domain Coverage & Professional Accuracy
- [ ] Reflects real professional-reporting discipline (separating observation vs. report vs. interpretation vs. action)
- [ ] Enforces evidentiary rigor ("a filename or caption alone is not visual evidence"; concealed work is "Not observed")
- [ ] Correctly scopes the report: it does not certify code/life-safety/structural/MEP/accessibility compliance

### 4. Safety, Integrity & Guardrails
- [ ] Explicit anti-fabrication rule ("Do not fabricate photo identity, location, dates or certainty about concealed conditions")
- [ ] Requires the professional-disclaimer procedure with a mandated terminal marker for client/authority-facing reports
- [ ] Forbids silent mutation of PROJECT.md/TASKS.csv/decision records and keeps epistemic categories intact

### 5. System Integration & Precision
- [ ] References a host contract, host-adapters, workspace model, and shared catalog with relative links
- [ ] Defines precise document semantics (`documents.register`, kind `site-visit`, `supersedes`, attachment IDs)
- [ ] `site_visit.prepare` is defined as authored procedure, not an installed executable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata & Trigger Description | 15% | | |
| Instruction Structure & Organization | 20% | | |
| Domain Coverage & Professional Accuracy | 25% | | |
| Safety, Integrity & Guardrails | 25% | | |
| System Integration & Precision | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask to prepare a site-visit report from notes and photos; verify the skill separates observations/reports/interpretations, labels items, records visit scope and limitations
2. Provide a photo with a descriptive filename but no visual inspection; verify the skill inspects the image before describing it and does not treat the filename as evidence
3. Request a client-facing report; verify the disclaimer procedure and terminal marker are applied

### Boundary Test Cases
1. Concealed/inaccessible work; verify it is recorded as "Not observed", never "no issue observed"
2. A read-only request or inline draft; verify no publication sequence is forced
3. Notes that also mention project facts/decisions; verify these are not silently promoted and are offered only after saving, with exact item IDs

### Negative Test Cases
1. Whether the skill ever fabricates dates, locations, or photo identity
2. Whether it certifies code/life-safety/structural/MEP/accessibility compliance (out of scope)
3. Whether it mutates PROJECT.md/TASKS.csv/decision records without explicit authorization

## Notes
- End-user professional skill for architecture/AEC practice (site-visit documentation); content is a workflow contract in prose, not application code
- MIT license permits verbatim reproduction and modification
- The skill is one of many under `skills/` and depends on workspace docs (`docs/`, `rules/`, `corpus/`, `templates/`) in the same repo; it is designed for a host that provides the "architecture-studio" workspace semantics
