# none — No loadable artifact (24 cases)

These agent cases were collected but contain **no directly loadable** System Prompt, Skill, or Tool Schema under the counting standard in `../README.md` §5. They are retained as exclusion evidence, not as an analysis denominator.

## Composition

| Cause | Cases | Notes |
|---|---|---|
| Verbatim text truncated (`...`, `[...]`, "abridged", "excerpt") | `TC-004`, `TC-084`, `TC-097`, `TC-098`, `TC-099`, `TC-100`, `TC-102`, `TC-103`, `TC-104`, `TC-105`, `TC-040`, `TC-042` | Recoverable by re-fetching the full source |
| Missing standard header (`SKILL.md` frontmatter) or body not a complete file | `TC-005`, `TC-055`, `TC-061`, `TC-063` | Recoverable by adding frontmatter / full body |
| Logic embedded in code or configuration only | `TC-035`, `TC-036`, `TC-037`, `TC-038`, `TC-060`, `TC-062`, `TC-106`, `TC-107` | Not recoverable as text artifacts; candidates for dynamic validation |

## How to use this folder

- **Do not** include these cases in any defect-rate denominator.
- **Do** report them in the sampling funnel: 56 agent cases identified → 32 with at least one loadable artifact → 24 excluded by the causes above.
- Eligibility was assessed **before** any inspection, so no case was excluded based on inspection outcome.
- The first two causes (16 cases) are data-collection defects, not properties of the source projects. If recovered, the corpus grows and the funnel changes; record the recovery date when that happens.
