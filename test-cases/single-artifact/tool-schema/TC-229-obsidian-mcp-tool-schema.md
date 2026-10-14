# TC-229: Obsidian MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: MarkusPfundstein/mcp-obsidian (community Obsidian MCP server)
- **License**: MIT (Copyright (c) 2024 Markus Pfundstein)
- **Artifact Type**: Tool Schema (MCP tool definitions for Obsidian vault tools)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/mcp_obsidian/tools.py` — `ToolHandler` subclasses whose `get_tool_description()` returns the tool `name`, `description` and `inputSchema`
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definitions (`src/mcp_obsidian/tools.py`, fetched verbatim)

```python
class ListFilesInVaultToolHandler(ToolHandler):
    def __init__(self):
        super().__init__(TOOL_LIST_FILES_IN_VAULT)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Lists all files and directories in the root directory of your Obsidian vault.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
```

```python
class ListFilesInDirToolHandler(ToolHandler):
    def __init__(self):
        super().__init__(TOOL_LIST_FILES_IN_DIR)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Lists all files and directories that exist in a specific Obsidian directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "Path to list files from (relative to your vault root). Note that empty directories will not be returned."
                    },
                },
                "required": ["dirpath"]
            }
        )
```

```python
class GetFileContentsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("obsidian_get_file_contents")

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Return the content of a single file in your vault.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the relevant file (relative to your vault root).",
                        "format": "path"
                    },
                },
                "required": ["filepath"]
            }
        )
```

```python
class SearchToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("obsidian_simple_search")

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="""Simple search for documents matching a specified text query across all files in the vault. 
            Use this tool when you want to do a simple text search""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to a simple search for in the vault."
                    },
                    "context_length": {
                        "type": "integer",
                        "description": "How much context to return around the matching string (default: 100)",
                        "default": 100
                    }
                },
                "required": ["query"]
            }
        )
```

> The constants `TOOL_LIST_FILES_IN_VAULT = "obsidian_list_files_in_vault"` and `TOOL_LIST_FILES_IN_DIR = "obsidian_list_files_in_dir"` are declared at the top of the file. The module also defines handler classes for `obsidian_append_content`, `obsidian_patch_content`, `obsidian_put_content`, `obsidian_delete_file`, `obsidian_complex_search`, `obsidian_batch_get_file_contents` and `obsidian_get_periodic_note` using the same `get_tool_description()` pattern; the four representative tools above are quoted verbatim (a single cohesive registry from one file, mirroring TC-188).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool does ("Lists all files and directories...", "Return the content of a single file...")
- [ ] Scope is stated ("root directory of your Obsidian vault" vs "a specific Obsidian directory")
- [ ] `obsidian_simple_search` provides when-to-use guidance ("Use this tool when you want to do a simple text search")

### 2. Schema Correctness
- [ ] Each tool exposes a hand-written JSON Schema (`type: "object"`, `properties`, `required`)
- [ ] Types are accurate (`string`, `integer`)
- [ ] Required vs optional parameters are distinguishable (`dirpath`, `filepath`, `query` required; `context_length` optional)
- [ ] Empty-parameter tools declare `"properties": {}` and `"required": []` explicitly

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Path semantics are explained ("relative to your vault root")
- [ ] Behavioral caveats are documented ("empty directories will not be returned")
- [ ] Defaults are documented and declared (`context_length` default 100)

### 4. Integration Compatibility
- [ ] Conforms to the MCP tool model (each handler returns an `mcp.types.Tool` with `name`, `description`, `inputSchema`)
- [ ] Uses standard MCP TypeScript/Python SDK type shapes (`TextContent` responses)
- [ ] Environment-driven configuration (`OBSIDIAN_API_KEY`, `OBSIDIAN_HOST`)

### 5. Extensibility & Maintainability
- [ ] One handler class per tool, each implementing `get_tool_description()` and `run_tool()`
- [ ] A base `ToolHandler` enforces the interface (`raise NotImplementedError()`)
- [ ] Tool-name constants are centralized at the module top

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "list the files in my Obsidian vault"; verify `obsidian_list_files_in_vault` with an empty argument object.
2. Issue "show what's in the 'Projects' folder of my vault"; verify `obsidian_list_files_in_dir` with `dirpath: "Projects"`.
3. Issue "find all notes mentioning 'budget'"; verify `obsidian_simple_search` with `query: "budget"`.

### Boundary Test Cases
1. `obsidian_get_file_contents` with a path that does not exist; verify the error path returns a readable message.
2. `context_length` omitted; verify the documented default (100) is applied.
3. `dirpath` pointing to an empty directory; verify the "empty directories will not be returned" behavior.
4. `obsidian_simple_search` with a `query` matching many files; verify result formatting.

### Negative Test Cases
1. `obsidian_list_files_in_dir` without `dirpath`; verify schema validation rejects the call.
2. `obsidian_get_file_contents` without `filepath`; verify rejection.
3. `context_length` passed as a string; verify type validation rejects it.
4. Ambiguous request ("look at my notes") with no directory or query; verify the model asks which folder or search term to use.

## Notes
- This server talks to a locally hosted Obsidian REST API plugin; it is an end-user knowledge/notes tool. Four representative tools from a single registry file are quoted.
- Schemas are hand-written JSON Schema returned from each handler's `get_tool_description()`.
- License is MIT; long verbatim quotation is permissible.
