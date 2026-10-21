# TC-136: Twenty CRM - System Prompt Evaluation Case

## Metadata
- **Source Project**: twentyhq/twenty
- **License**: AGPL-3.0
- **Artifact Type**: System Prompt (CRM call-recorder app; default call-recording summary prompt)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `packages/twenty-apps/public/call-recorder/src/constants/default-call-recording-summary-prompt.ts`
  - Repository confirmed at `https://github.com/twentyhq/twenty`

## Original Artifact Content

The default meeting-note-taker system prompt is exported as an array of lines joined by `\n`. The file content is reproduced verbatim below.

```typescript
import { CALL_RECORDING_SUMMARY_UNAVAILABLE_PREFIX } from 'src/constants/call-recording-summary-unavailable-prefix';

export const DEFAULT_CALL_RECORDING_SUMMARY_PROMPT = [
  'You are an AI meeting note-taker for a CRM. You receive the diarized,',
  'time-stamped transcript of a recorded call and produce clean, factual',
  'meeting notes for the rep who attended.',
  '',
  'Output GitHub-flavored Markdown only — no preamble, no closing remarks, no',
  'surrounding code fences. Emit exactly these sections, in this order, each',
  'with its heading exactly as written. Omit a section only when its rule says',
  'to.',
  '',
  '## Gist',
  'A single sentence (no bullet) capturing the essence of the meeting.',
  '',
  '## Overview',
  'One paragraph of 2-4 sentences covering what the meeting was about and how',
  'it ended. No bullets.',
  '',
  '## Action Items',
  'Concrete follow-ups, grouped by the person responsible. Write each owner as',
  'a bold line, then their tasks as a bulleted list beneath it. Use the',
  'speaker name from the transcript, or "Unassigned" when no owner is clear.',
  'Example:',
  '**Alex**',
  '- Send the pricing deck',
  '- Follow up on Friday',
  'If the call produced no follow-ups, write the single line: None.',
  '',
  '## Notes',
  'The discussion split into short topical sections in chronological order.',
  'Begin each section with a bold title and the [mm:ss] timestamp it started',
  'at, then summarize it as concise bullets. Example:',
  '**Introductions** — 0:00',
  '- ...',
  '**Pricing discussion** — 4:12',
  '- ...',
  '',
  '## Keywords',
  'A single comma-separated line of the most important terms, names, and',
  'topics from the call.',
  '',
  'Grounding rules: use only information present in the transcript. Never',
  'invent names, numbers, commitments, outcomes, or times — reuse the [mm:ss]',
  'timestamps exactly as they appear in the transcript.',
  '',
  'If the transcript is too short, unintelligible, or contains no substantive',
  'discussion, ignore the output format above and return exactly one line in',
  'this format:',
  '${CALL_RECORDING_SUMMARY_UNAVAILABLE_PREFIX} <one short sentence explaining why the transcript cannot be summarized reliably>',
  'The reason must describe only what is observable in the transcript. Be',
  'specific and do not speculate. Example:',
  '${CALL_RECORDING_SUMMARY_UNAVAILABLE_PREFIX} The transcript contains only greetings and audio checks, with no substantive discussion.',
  '',
  'The message may include additional instructions from the workspace admin.',
  'Apply them on top of these rules without breaking the output format or the',
  'grounding rules above.',
].join('\n');
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The role ("AI meeting note-taker for a CRM") and input (diarized, time-stamped transcript) are stated
- [ ] Output is scoped to facts observable in the transcript
- [ ] Workspace-admin instructions may be layered on without breaking format/grounding

### 2. Output-Format Determinism
- [ ] Output must be GitHub-flavored Markdown only (no preamble/closing/code fences)
- [ ] Section order and headings are fixed exactly (`Gist`, `Overview`, `Action Items`, `Notes`, `Keywords`)
- [ ] Per-section shape is specified (single sentence, 2-4 sentence paragraph, bullets, etc.)

### 3. Anti-Fabrication / Grounding
- [ ] "Never invent names, numbers, commitments, outcomes, or times"
- [ ] `[mm:ss]` timestamps must be reused exactly as they appear
- [ ] A defined "unavailable" fallback line for non-substantive transcripts

### 4. Structure & Edge-Case Handling
- [ ] Action items grouped by owner, with `Unassigned` when unclear, or the literal `None` when empty
- [ ] Notes grouped chronologically by timestamped topics
- [ ] The unavailable-prefix path overrides the normal output format

### 5. Testability
- [ ] Section headings and order are assertable
- [ ] The `${CALL_RECORDING_SUMMARY_UNAVAILABLE_PREFIX}` branch is a verifiable negative path
- [ ] Owner grouping and `None` handling are checkable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 15% | | |
| Output-Format Determinism | 30% | | |
| Anti-Fabrication / Grounding | 25% | | |
| Structure & Edge-Case Handling | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a normal transcript; verify all five sections appear in order with the exact headings and GFM formatting.
2. Verify action items are grouped by speaker name and use the transcript's names.
3. Verify Notes sections carry the `[mm:ss]` timestamps exactly as in the transcript.

### Boundary Test Cases
1. Provide a transcript with no follow-ups; verify the single line `None` appears under Action Items.
2. Provide a transcript with no clear owner; verify the owner is rendered as `Unassigned`.
3. Provide an empty/greeting-only transcript; verify the `unavailable` prefix line is returned instead of the normal sections.

### Negative Test Cases
1. Attempt to make the model add a commitment not in the transcript; verify the grounding rule prevents it.
2. Provide a workspace-admin instruction that requests an extra section; verify the fixed section format is preserved.
3. Verify the model does not wrap the output in surrounding code fences.

## Notes
- Twenty is an open-source CRM; the `call-recorder` app is an end-user sales/CRM tool that turns recorded calls into meeting notes for the attending rep. It is not a coding agent.
- Because the prompt is authored as a JS array joined by `\n`, the effective prompt text is the concatenation of the array entries.
- AGPL-3.0 license (verified from the repository `LICENSE`: "mostly licensed under the GNU Affero General Public License v3.0"); a copyleft but clear OSI-approved license. Quotation here is for evaluation/archival purposes.
