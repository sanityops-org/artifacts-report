# TC-063: Claude Gym Coach - File-Based Agent Skill Suite

## Metadata
- **Source Project**: claude-gym-coach (nikitavovch/claude-gym-coach)
- **GitHub**: github.com/nikitavovch/claude-gym-coach
- **License**: MIT
- **Artifact Type**: File-based skill suite for a personal strength coach (Claude Code plugin)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub raw-content fetch on branch `main` — `https://raw.githubusercontent.com/nikitavovch/claude-gym-coach/main/skills/gym/SKILL.md` and `https://raw.githubusercontent.com/nikitavovch/claude-gym-coach/main/skills/plan/SKILL.md`; skill inventory and behaviour cross-checked against `https://raw.githubusercontent.com/nikitavovch/claude-gym-coach/main/README.md`
- **Scope**: Two of the plugin's SKILL.md files (`gym`, `plan`) among the eight-skill suite, quoted verbatim; the athlete-facing data files are plain Markdown the skills read and write

---

## Project Overview

Claude Gym Coach is a **personal strength coach** delivered as a Claude Code plugin. It designs a training programme, writes each session from the athlete's own history and the gym's real plates, logs what the athlete dictates after training, reviews every block, and keeps all of it as plain Markdown files in a folder the athlete owns.

### Key Characteristics
- **File-based artifacts**: skills are `SKILL.md` files; athlete data is Markdown (`profile.md`, `program.md`, `phases.md`, `gym.md`, `log/<date>.md`, `reviews/*.md`)
- **Eight skills / eight subagents / one SessionStart hook** — the inventory names `init`, `plan`, `log`, `review`, `phase`, `import`, `exercise`, `gym`
- **Numbers in code, judgement in prompts**: every figure (e1RM, trends, stalls, records, fatigue signals, bodyweight rate, cardio gaps) is computed by `scripts/stats.mjs` (plain Node, no dependencies, 400+ tests); the next working weight is the planner's call under the programme's rules
- **Athlete-local language**: `SKILL.md` bodies are written in English *for the model*, while everything said to the athlete and every file written for them is in the athlete's own language
- **Multi-athlete folders**: one folder can coach several athletes, each with their own programme, log and gym
- **Explicit safety boundaries**: PAR-Q+ health screen, a pain "traffic light", and a refusal to write drug protocols

### The Eight-Skill Suite

| Command | What it does (from README) |
|-------|-------------|
| `/coach:init` | First setup, or a new athlete in the same folder |
| `/coach:plan` | Writes the next session from the programme and history |
| `/coach:log` | Records a session from free dictation, reports deviations and records |
| `/coach:review` | Analyses a period and proposes programme changes, one confirmation each |
| `/coach:phase` | Cut, bulk or maintain — and whether bodyweight follows the target |
| `/coach:import` | Turns a paper notebook (text or photos) into log files |
| `/coach:exercise` | Teaches the coach an exercise or another name for one |
| `/coach:gym` | Updates equipment and checks the programme against it |

---

## Logical Artifact Inventory

### 1. `skills/gym/SKILL.md` — Gym Inventory Skill

**Frontmatter:**

```markdown
---
name: coach-gym
description: This skill should be used when the athlete's equipment changes — "we got new dumbbells", "купил микроблины", "в зале убрали жим ногами", "I moved to a new gym", "перешёл в другой зал", "update my gym", "обнови инвентарь", or runs /coach:gym. It edits the gym inventory the coach plans against, without re-running init, and says which programmed exercises the change affects.
argument-hint: "[athlete] <what changed>"
---
```

**Opening — the invariant the skill protects:**

> Keeps the gym inventory current. Every plan the coach writes is rounded to the plates in that file and built from the equipment in it, and the SessionStart hook prints it into every session — so an inventory that still lists a leg press the gym sold, or misses the microplates the athlete just bought, makes every later plan quietly wrong. This skill edits it in place, then checks each affected programme against the new equipment and says what changed for it.

**Scope discipline (language + write boundary):**

> This document is written in English, for the model. Everything the coach says to the athlete during a run is in the athlete's own language.
> It writes only the inventory (`gym.md` or `athletes/<id>/gym.md`) and, when an athlete switches between the shared gym and one of their own, that athlete's `gym` field in `.coach.json`. It never touches `program.md`: what to do about an exercise the gym can no longer support is `plan`'s or `review`'s call, with the athlete (§6).

**Guard clause (§1) — schema versioning as a hard stop:**

> Check for `.coach.json` in the working directory. Missing — tell the athlete to run `/coach:init` and stop. Present — check its `schema` field: anything other than `1` means the plugin and the data folder are out of sync, so say so and stop without attempting to auto-migrate.

**Shared-gym rule (§2) — name the affected athletes before writing:**

> - `own` → `athletes/<id>/gym.md`.
> - `shared`, or no field → the root `gym.md`, which every `shared` athlete in the folder trains against. Name them before changing anything: "this is the gym Danila and Vera share — the change is for both of you."

**Machine-readable plate lines (§3) — the reason a plate must be recorded, not just described:**

> When it touches the bar, the plates or the dumbbells, update the matching machine-readable line too (`- bar:`, `- plates:`, `- dumbbells: … step …`, or `гриф`, `блины`, `гантели … шаг`) — `stats.mjs load` rounds every future plan from it, so a plate bought and not written there is a plate never used.

**Confirmation gate and re-check against programmes (§5–§6):**

> Show the edited section back in plain words and wait for a yes before writing the file.
> 1. Turn the new inventory into equipment tags — the vocabulary of `${CLAUDE_PLUGIN_ROOT}/knowledge/exercises.md` §3 … and run:
> ```
> node "${CLAUDE_PLUGIN_ROOT}/scripts/stats.mjs" catalog --lang <athlete's language> --equipment <tags, comma-separated> --json
> ```
> 2. Every exercise in the tables under `program.md`'s `## Sessions` that the catalogue no longer lists is one the new gym can't support.
> 3. If the smallest plate jump changed, say so: the planner rounds every load to it, so progression steps change with it — finer after microplates, coarser without them.

**Closing "Rules that apply throughout":**

> - **Only the inventory and the athlete's `gym` field are written**, and only after the athlete confirms the change shown to them.
> - **Every other line of the inventory stays as the athlete wrote it.**
> - **A shared gym is changed for everyone on it** — say who before writing.
> - Plugin-side text (this file) is English; everything said to the athlete, and every file written for them, is in their language.

### 2. `skills/plan/SKILL.md` — Session Planning Skill

**Frontmatter:**

```markdown
---
name: coach-plan
description: This skill should be used when the user asks "what am I doing today", "write my workout", "plan the session", "что сегодня", "напиши тренировку", or runs /coach:plan. It writes the next workout from the athlete's program and recent history.
argument-hint: "[athlete] [date or session]"
---
```

**Opening — path discipline and "never state a date from memory":**

> Writes the next workout — the session the athlete does today, or another date if they ask — from their program, their gym inventory, and their recent training history. This is the skill the athlete runs most often, usually right before leaving for the gym, so getting the athlete and the weights right matters more here than almost anywhere else in the plugin.
> Plugin files — the statistics script, anything under `knowledge/` or `templates/` — are addressed by their full path, which Claude Code fills in before this text is read. … A skill that gets this backwards cannot find a single file at runtime.
> Take today's date from running `node "${CLAUDE_PLUGIN_ROOT}/scripts/stats.mjs" today`. Never state a date from memory.

**Guard and athlete resolution (§1–§2):**

> Check for `.coach.json` in the working directory. Missing — tell the athlete to run `/coach:init` and stop; this skill creates nothing on its own.
> Per the athlete-resolution rule: the first argument, if it case-insensitively matches an athlete's `id` or `name` in `.coach.json`, selects that athlete; otherwise use `default_athlete`. There is no session-level "current athlete" memory — resolve fresh every run, since a stale guess written to the wrong athlete's log is worse than asking. Whatever athlete is resolved, name them in the first line of the final reply ("Vera, Lower A, 2026-09-22") so a wrong-athlete mistake is visible immediately …

**Stale-plan handling (§4) — three explicit choices:**

> `brief`'s `openPlanned` for this athlete lists every planned file dated before today, however far back — `recent`'s five rows can miss an old one. If there is one, surface it before anything else in the reply …
> - **Log it** — tell them to run `/coach:log` for that date; this skill doesn't parse free-text diction, so don't try to fill in the facts here.
> - **Drop it** — set that file's `status` to `skipped` and add a short note to its Notes section ("skipped — superseded, never logged").
> - **Move it** — the old plan becomes today's plan: rename the file to today's date and update its `date` frontmatter field to match.

**Rotation logic (§6) — dates and sessions come from the script, not memory:**

> look at `Meta → rotation` and the `recent` output from step 4: find the athlete's last `done` session — skipping rows marked `cardio only` … — and take the next name in the rotation list, wrapping to the first after the last. If none of the five rows qualifies, re-run `recent` with `--n 20` rather than guessing.

**Delegation to the planner subagent (§7) — the skill packages a full, self-contained brief:**

> The planner agent cannot ask the athlete anything — it works once, autonomously, and returns a report — so its task must contain everything it needs. Invoke it with the Agent tool, `subagent_type: coach:planner`, and give it, explicitly, in the prompt: …
> - The `Progression rules` and `Deload rules` sections of `program.md`, copied verbatim, not summarized …
> - The athlete's `profile.md` content … never trim it from the package to save space.
> **If the agent's report names something it was missing**, don't guess: ask the athlete that one specific question, then call the agent again with the same full package plus the answer.

**Post-generation verification (§8) — every load is re-checked against the plates before the athlete sees it:**

> Before printing anything to the athlete, read the weights the agent wrote into the log file's `## Plan` section and check each barbell and dumbbell load with the script:
> ```
> node "${CLAUDE_PLUGIN_ROOT}/scripts/stats.mjs" load <kg> --athlete <id> [--dumbbell]
> ```
> A load the script returns unchanged is buildable. One it changes wasn't: use the script's load, edit the file, and note the correction as an extra adjustment line when you print the plan.

### 3. Athlete Data Files (plain Markdown, referenced by the skills)

The skills read and write a fixed folder layout (from the README):

```text
~/gym/
  .coach.json            # athletes, language, units (kg or lb)
  gym.md                 # the shared gym's equipment
  exercises.md           # the exercise table, with your own additions
  athletes/
    danila/
      profile.md         # goal, history, injuries in your own words
      program.md         # the current block, with a changelog
      phases.md          # cut / bulk / maintain, with target rates
      log/2026-09-23.md  # one file per training day
      reviews/2026-W39.md
    vera/
      …                  # a second athlete, fully separate
      gym.md             # only if she trains somewhere else
```

A single training day file (from the README):

```markdown
---
date: 2026-09-23
session: Lower A
status: done
time: 18:30
duration_min: 70
feel: 4
bodyweight: 82.4
---
## Plan
- Back Squat: 105x5x3 @8
## Actual
- Back Squat: 105x5 @8, 105x5 @8, 105x5 @8.5
- Romanian Deadlift: 82.5x8x3 @7
- Lying Leg Curl: 40x12x3
## Cardio
- Run 30min Z2, 5km, 08:00
## Notes
Slept six hours.
```

---

## Evaluation Dimensions

### 1. Skill Corpus Consistency
- [ ] All skills share the same SKILL.md + YAML frontmatter contract
- [ ] Frontmatter `description` names concrete trigger phrases and the slash command
- [ ] The eight skills partition responsibilities without overlap

### 2. Guardrail Design
- [ ] Each skill guards on `.coach.json` presence and `schema` version
- [ ] Irreversible/structural writes require athlete confirmation
- [ ] Safety rules (PAR-Q+, pain traffic light, no drug protocols) are explicit

### 3. Data-Source Discipline
- [ ] Dates and figures come from `stats.mjs`, never from memory
- [ ] Plugin paths vs athlete-relative paths are disambiguated at the top of each skill
- [ ] "No data means no data" — the coach never invents a number

### 4. Delegation & Verification
- [ ] The planner subagent receives a fully self-contained brief
- [ ] Missing-input reports loop back as a single targeted question
- [ ] Generated loads are re-verified against the plate inventory before display

### 5. Localisation & Portability
- [ ] Skill prose is English (for the model); athlete output is in the athlete's language
- [ ] File formats are plain Markdown, hand-editable and diff-friendly
- [ ] Multi-athlete folders isolate each athlete's programme, log and gym

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Corpus Consistency | 20% | | |
| Guardrail Design | 25% | | |
| Data-Source Discipline | 20% | | |
| Delegation & Verification | 20% | | |
| Localisation & Portability | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Skill Loading Tests
1. Load all eight skills from the plugin and confirm each declares `name` + `description` + `argument-hint`
2. Confirm the SessionStart hook prints the gym inventory into each session
3. Verify the absence of `.coach.json` and a `schema != 1` both stop the skill cleanly

### Guardrail Tests
1. Run `/coach:gym` with a plate change and confirm the machine-readable line is updated, not just the prose
2. Change a shared gym and confirm every affected athlete is named before the write
3. Attempt a structural programme change and confirm it routes to `/coach:review` with a confirmation, never a silent edit

### Data & Verification Tests
1. Run `/coach:plan` and confirm every printed load passes `stats.mjs load` unchanged (or is corrected)
2. Force the planner subagent to report a missing input and confirm the skill asks exactly that one question
3. Verify no date is ever stated without `stats.mjs today`

### Localisation Tests
1. Coach an athlete whose `language` is Russian and confirm the reply and written files are Russian while the skill text stays English
2. Add a second athlete to the folder and confirm `/coach:plan vera` resolves the correct athlete and never uses a stale "current athlete"

---

## Notes

- **MIT license** permits full quotation and modification.
- Claude Gym Coach is a **fitness-coaching agent**, a non-coding use of file-based skills: the skills plan, log and review workouts, not repositories.
- The suite is a strong reference for **skill-file authoring at scale**: eight skills with a shared guard, a shared path convention, and a shared "numbers in code, judgement in prompts" split.
- The `plan` skill demonstrates **subagent delegation with a self-contained package** and a **post-generation verification gate** before the human sees output.
- Only `skills/gym/SKILL.md` and `skills/plan/SKILL.md` were quoted (the `plan` file is quoted up to section 9, where the fetched content ends); the remaining six skills and the data-file formats are described from the README.
