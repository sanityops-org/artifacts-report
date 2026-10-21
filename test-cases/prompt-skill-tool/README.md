# prompt-skill-tool — EMPTY (0 cases)

No case in the corpus ships all three artifact types as loadable text. This is the central structural finding of the collection, not an oversight.

## Why this folder is empty

Each artifact type is universal or rare for a different structural reason:

| Type | Coverage in the corpus | Reason |
|---|---|---|
| System Prompt | 67 cases | Every product ships instruction text; it is the only layer with no alternative implementation. |
| Skill | 65 cases | Confined to file-based agents; business products express capabilities as code plus prompt. |
| Tool Schema | 49 cases | Confined to MCP servers; products that define tools in code generate the schema at runtime. |

The three sets are almost disjoint: 50 prompt cases, 50 skill cases, and 49 tool cases were collected **from different projects**. No single project in either sampling frame published all three as documents.

## Why this matters

A static inspection that assumes a complete three-layer artifact set will find almost nothing to inspect in a real production agent. The practical consequences:

1. **Cross-artifact consistency checks** (Prompt ↔ Skill ↔ Tool agreement) have no population to run against in this corpus.
2. **Single-artifact checks** are the only ones with statistical power: 149 artifacts across three types.
3. Tool contracts must be recovered from code before they can be inspected at all — see `_archive/extract_tool_schema.py` for a deterministic (AST-only, no LLM) recovery method validated on OpenContracts (12 tools).

## Cross-reference

- `../README.md` §3 — the two sampling frames and their identical result.
- `../prompt-tool/README.md` — the closest combination to becoming non-empty.
