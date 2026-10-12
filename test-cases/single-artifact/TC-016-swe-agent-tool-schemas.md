# TC-016: SWE-agent - Tool Schemas Evaluation Case

## Metadata
- **Source Project**: princeton-nlp/SWE-agent
- **License**: MIT
- **Artifact Type**: Tool Definitions
- **Collection Date**: 2025-10-12
- **Collection Method**: Extracted from tools/ and sweagent/tools at commit 3ea751c087f32b16e039a2233dd6eefecef325d5

## Original Artifact Content

### tools/edit_anthropic/config.yaml

```yaml
tools:
  str_replace_editor:
    signature: |
      str_replace_editor <command> <path> [<file_text>] [<view_range>] [<old_str>] [<new_str>] [<insert_line>]
    docstring: >
      Custom editing tool for viewing, creating and editing files
      * State is persistent across command calls and discussions with the user
      * If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep
      * The `create` command cannot be used if the specified `path` already exists as a file
      * If a `command` generates a long output, it will be truncated and marked with `<response clipped>`
      * The `undo_edit` command will revert the last edit made to the file at `path`

      Notes for using the `str_replace` command:
      * The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!
      * If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique
      * The `new_str` parameter should contain the edited lines that should replace the `old_str`
    arguments:
      - name: command
        type: string
        description: "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
        required: true
        enum: ["view", "create", "str_replace", "insert", "undo_edit"]
      - name: path
        type: string
        description: "Absolute path to file or directory, e.g. `/testbed/file.py` or `/testbed`."
        required: true
      - name: file_text
        type: string
        description: "Required parameter of `create` command, with the content of the file to be created."
        required: false
      - name: old_str
        type: string
        description: "Required parameter of `str_replace` command containing the string in `path` to replace."
        required: false
      - name: new_str
        type: string
        description: "Optional parameter of `str_replace` command containing the new string."
        required: false
      - name: insert_line
        type: integer
        description: "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line`."
        required: false
      - name: view_range
        type: array
        items:
          type: integer
        description: "Optional parameter of `view` command when `path` points to a file. [start, end] line range."
        required: false
state_command: "_state_anthropic"
```

## Evaluation Dimensions

### 1. Tool Signature Clarity
- [ ] Clear command signature format
- [ ] Parameter types explicitly defined
- [ ] Required/optional distinction clear

### 2. Command Variety
- [ ] view - file/directory inspection
- [ ] create - new file creation
- [ ] str_replace - in-place editing
- [ ] insert - line insertion
- [ ] undo_edit - rollback capability

### 3. Edit Precision
- [ ] Exact string matching for old_str
- [ ] Uniqueness requirements enforced
- [ ] Whitespace sensitivity documented

### 4. Output Management
- [ ] Long output truncation
- [ ] Line number display (cat -n style)
- [ ] Response clipping markers

### 5. State Persistence
- [ ] Persistent state across calls
- [ ] Undo capability for edits
- [ ] History tracking

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Signature Clarity | 20% | | |
| Command Variety | 25% | | |
| Edit Precision | 25% | | |
| Output Management | 15% | | |
| State Persistence | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. File creation with create command
2. String replacement with unique old_str
3. Directory viewing with depth limit
4. Insert at specific line

### Boundary Test Cases
1. Non-unique old_str handling
2. Very large file viewing
3. Empty file creation
4. View range at file boundaries

### Negative Test Cases
1. Create on existing file
2. str_replace with mismatched whitespace
3. Invalid view range
4. Missing required parameters

## Notes
- SWE-agent is designed for automated GitHub issue resolution
- str_replace_editor is the primary file manipulation tool
- Emphasizes exact matching for reliable automated edits
- MIT license allows full quotation and modification