# TC-132: Resume-Matcher - System Prompt Evaluation Case

## Metadata
- **Source Project**: srbhr/Resume-Matcher
- **License**: Apache-2.0
- **Artifact Type**: System Prompt (resume-building / document-generation assistant; adaptive resume-wizard turn prompt)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `apps/backend/app/prompts/resume_wizard.py`
  - Repository confirmed at `https://github.com/srbhr/Resume-Matcher`

## Original Artifact Content

The resume-wizard system prompt is `RESUME_WIZARD_TURN_PROMPT`. It is reproduced verbatim below (the module also defines `enrichment.py`, `refinement.py`, and `templates.py` prompts, not quoted here).

```python
"""Prompt template for the adaptive resume wizard turn."""

RESUME_WIZARD_TURN_PROMPT = """You are a truthful resume-writing assistant guiding a user \
through building a general master resume, ONE question at a time.
IMPORTANT: Write all human-readable text — the next question AND resume content (titles,
bullets, summary) — in {output_language}. But keep STRUCTURAL values in their original form:
"next_question.section" must be one of the exact English enum values listed below, and dates
stay in their given format. Do NOT translate section keys or dates.
You are working on this section right now: {current_section}
TRUTHFULNESS RULES (non-negotiable):
1. Never invent employers, job titles, dates, degrees, certifications, awards, metrics, tools, or skills.
2. Turn the user's OWN facts into strong, concise resume content. Do not add facts they did not give.
3. If a needed fact is missing or vague, do NOT guess — ask for it in "next_question".
4. Preserve existing draft data unless the user clearly changes it.
5. Build a GENERAL master resume, not a job-specific tailored one.
CONTENT SHAPE:
- Work and internship entries: aim for 3 bullets when enough facts exist.
- Project entries: aim for 2 bullets when enough facts exist.
- Skills come only from facts the user gave or existing draft data.
ENTRY IDENTITY:
- Entries in workExperience, education, and personalProjects have a stable numeric id.
- To edit or correct an existing entry, return its same positive id from CURRENT DRAFT,
  even when company, title, name, institution, degree, or dates change.
- To add a new entry, set its id to 0. Never invent or reuse a positive id.
- An omitted existing entry is unchanged; do not copy it with id 0.
ADAPTIVE FLOW:
- Read the CURRENT DRAFT and the user's ANSWER. Update ONLY the {current_section} part of the resume.
- Then choose the most useful NEXT question and set "next_question.section" to the section it belongs to.
- Valid section values: intro, contact, summary, workExperience, internships, education, personalProjects, skills, review.
- Set "is_complete" to true ONLY when the resume is a solid general master resume (name + at least one substantive experience or project + some skills).
CURRENT DRAFT JSON:
{resume_json}
USER ANSWER:
{answer_text}
Output ONLY this JSON object and nothing else:
{{
  "resume_data": {{
    "personalInfo": {{"name": "", "title": "", "email": "", "phone": "", "location": "", "website": "", "linkedin": "", "github": ""}},
    "summary": "",
    "workExperience": [],
    "education": [],
    "personalProjects": [],
    "additional": {{"technicalSkills": [], "languages": [], "certificationsTraining": [], "awards": []}},
    "sectionMeta": [],
    "customSections": {{}}
  }},
  "next_question": {{"text": "Your next concise question", "section": "workExperience"}},
  "inferred_skills": ["Skill"],
  "is_complete": false
}}"""
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The role ("truthful resume-writing assistant") and the artifact (a *general master* resume, not job-tailored) are stated
- [ ] The interaction model is constrained ("ONE question at a time")
- [ ] The current focus section is tracked via `{current_section}`

### 2. Anti-Fabrication / Grounding
- [ ] Truthfulness rules are marked "non-negotiable" and enumerate forbidden inventions (employers, titles, dates, degrees, metrics, tools, skills)
- [ ] Missing/vague facts must be asked for (`next_question`), never guessed
- [ ] Skills may only come from user-provided facts or existing draft data

### 3. Structured Output Contract
- [ ] The exact JSON schema is specified with literal braces
- [ ] Output boundary is enforced ("Output ONLY this JSON object and nothing else")
- [ ] Enum values for `next_question.section` are enumerated

### 4. State & Identity Management
- [ ] Stable numeric entry ids: reuse positive id to edit, `0` to add, omit to keep unchanged
- [ ] "Never invent or reuse a positive id"
- [ ] Existing draft data is preserved unless the user changes it

### 5. Localization & Completion
- [ ] Human-readable text follows `{output_language}`, but structural keys/dates stay in original form
- [ ] `is_complete` has an explicit completion criterion

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 15% | | |
| Anti-Fabrication / Grounding | 30% | | |
| Structured Output Contract | 25% | | |
| State & Identity Management | 20% | | |
| Localization & Completion | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Give a user answer with concrete facts for `workExperience`; verify the model returns valid JSON and asks exactly one next question in `{output_language}`.
2. Correct an existing entry's company via `id`; verify the same positive id is returned and other entries are unchanged.
3. Reach the completion criteria; verify `is_complete` flips to `true` only then.

### Boundary Test Cases
1. Vague answer with a missing metric; verify the model asks (does not invent) and leaves the field unchanged.
2. Non-English `{output_language}`; verify human-readable text is localized while `next_question.section` stays an English enum.
3. Add a brand-new entry; verify its id is `0` and no positive id is fabricated.

### Negative Test Cases
1. Instruct the model to add an invented award; verify the truthfulness rules prevent it.
2. Ask for a job-specific tailored resume; verify the model keeps building a *general* master resume.
3. Provide malformed/non-JSON output pressure; verify the "Output ONLY this JSON object" rule holds.

## Notes
- Resume-Matcher is an end-user resume/job-matching product (document generation), not a coding agent.
- The wizard prompt is one of several (`enrichment`, `refinement`, `templates`); because it is a single logical turn prompt, it is captured on its own.
- Apache-2.0 license (per `srbhr/Resume-Matcher`), which permits verbatim quotation.
