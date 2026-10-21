# SanityOps Test Case Folder

This folder stores SanityOps Inspect test cases: real agent logical artifacts and the
inspection reports produced from them. It is not a framework, a specification, or a
mirror of upstream repositories.

## 1. What counts as a test case

One case is either:

- **single artifact** — one System Prompt, Skill, Tool Schema, or Permission file, or
- **agent suite** — two or more artifacts belonging to the same agent
  (for example: system prompt + skill + tool schema).

Artifact types are those defined by the SanityOps framework: System Prompt, Skill,
Tool Schema, Permission. Permission is optional; most cases will not have one.

Not test cases: server source code, evaluation harnesses, datasets, benchmark suites,
or workflow configuration without a prompt, skill, or tool schema.

## 2. Layout

```
test-cases/
├── single-artifact/
│   ├── system-prompt/
│   ├── skill/
│   ├── tool-schema/
│   └── permission/
└── agent-suite/
```

Create a subdirectory only when the first case of that type is added.

## 3. Naming

Case file:

```
TC-{NNN}-{project}-{type}.{ext}
```

- `NNN` — globally unique number, 001–999, never reused.
- `project` — source project name in kebab-case.
- `type` — `system-prompt`, `skill`, `tool-schema`, `permission`, or `multi-agent-suite`.
- `ext` — the artifact's original extension (`.md`, `.json`, `.yaml`, `.ts`).

Report file — replace the extension, do not append a second one:

```
TC-{NNN}-{project}-{type}.sanityops-skill-report.md
TC-{NNN}-{project}-{type}.sanityops-cli-report.md
```

Summary reports:

```
sanityops-skill-inspection-summary.md
sanityops-cli-inspection-summary.md
```

## 4. Provenance

Every case records, in its header:

- source URL,
- commit SHA (immutable reference; never a moving branch),
- license,
- collection date.

A case without provenance is a draft and must not be listed as a test case.

## 5. Language

Files are written in English. Content quoted verbatim from the original artifact keeps
its original language. An explicit user request may override this; record the override
in the file where it applies.

## 6. Inspection

A case is verified only after it has been checked with `sanityops-inspect-lite` or
`sanityops-cli` and the report is stored next to it. An artifact without a report is a
sample, not a verified case.

## 7. Precedence

1. The user's instruction in the current request.
2. This file.
3. The SanityOps framework in `d:\My Docunments\AI\sanityops-framework\`.
4. Existing conventions in this folder.

## 8. Maintenance

- Find the next free number before adding a case; never renumber existing cases.
- Do not rename existing cases in bulk; apply this file to new and touched cases.
- Keep this file short. Navigation and ecosystem maps belong to the doc-router skill,
  not here. If a rule cannot be checked by reading a filename or a header, it does not
  belong in this file.
