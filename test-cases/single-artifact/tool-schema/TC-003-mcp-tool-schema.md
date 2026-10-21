# TC-003: GitHub MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: github-mcp-server (github/github-mcp-server)
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions registered on the server)
- **Collection Date**: 2026-10-20
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `pkg/github/repositories.go` — the `GetCommit` and `ListCommits` tool registrations, including their `jsonschema.Schema` input schemas
- **Re-scope note**: The previous TC-003 claimed a gpt-researcher MCP tool schema. That artifact does not exist upstream: `gpt_researcher/mcp/client.py` only implements `MCPClientManager` (config conversion plus `MultiServerMCPClient.get_tools()`); it declares no tool schema. This case has therefore been re-scoped to a real MCP server whose tool definitions are declared in source.

---

## Original Artifact Content

### 1. `get_commit` (`pkg/github/repositories.go`, verbatim)

```go
func GetCommit(t translations.TranslationHelperFunc) inventory.ServerTool {
	schema := WithPagination(&jsonschema.Schema{
		Type: "object",
		Properties: map[string]*jsonschema.Schema{
			"owner": {
				Type:        "string",
				Description: "Repository owner",
			},
			"repo": {
				Type:        "string",
				Description: "Repository name",
			},
			"sha": {
				Type:        "string",
				Description: "Commit SHA, branch name, or tag name",
			},
			"detail": {
				Type:        "string",
				Enum:        []any{"none", "stats", "full_patch"},
				Description: "Level of detail to include for changed files. \"none\" omits stats and files entirely. \"stats\" (default) includes per-file metadata: filename, status, and lines-of-code counts (additions, deletions, changes), with no patch content. \"full_patch\" additionally includes the unified diff content for each file and can be very large.",
				Default:     json.RawMessage(`"stats"`),
			},
		},
		Required: []string{"owner", "repo", "sha"},
	})
	return NewToolWithSchemaOptions[GetCommitInput, MinimalCommit](
		ToolsetMetadataRepos,
		mcp.Tool{
			Name:        "get_commit",
			Description: t("TOOL_GET_COMMITS_DESCRIPTION", "Get details for a commit from a GitHub repository"),
			Annotations: &mcp.ToolAnnotations{
				Title:        t("TOOL_GET_COMMITS_USER_TITLE", "Get commit details"),
				ReadOnlyHint: true,
			},
			InputSchema: schema,
		},
		scopes.PublicRead(scopes.Repo),
		inventory.TypedSchemaOptions{ValidationInputSchema: relaxedPaginationValidationSchema(schema)},
		func(ctx context.Context, deps ToolDependencies, _ *mcp.CallToolRequest, input GetCommitInput) (*mcp.CallToolResult, MinimalCommit, error) {
			if input.Owner == "" {
				return utils.NewToolResultError("missing required parameter: owner"), MinimalCommit{}, nil
			}
			if input.Repo == "" {
				return utils.NewToolResultError("missing required parameter: repo"), MinimalCommit{}, nil
			}
			if input.SHA == "" {
				return utils.NewToolResultError("missing required parameter: sha"), MinimalCommit{}, nil
			}
			detail, err := parseCommitDetail(input.Detail)
			if err != nil {
				return utils.NewToolResultError(err.Error()), MinimalCommit{}, nil
			}
```

### 2. `list_commits` (`pkg/github/repositories.go`, verbatim)

```go
func ListCommits(t translations.TranslationHelperFunc) inventory.ServerTool {
	schema := &jsonschema.Schema{
		Type: "object",
		Properties: map[string]*jsonschema.Schema{
			"owner": {
				Type:        "string",
				Description: "Repository owner",
			},
			"repo": {
				Type:        "string",
				Description: "Repository name",
			},
			"sha": {
				Type:        "string",
				Description: "Commit SHA, branch or tag name to list commits of. If not provided, uses the default branch of the repository. If a commit SHA is provided, will list commits up to that SHA.",
			},
			"author": {
				Type:        "string",
				Description: "Author username or email address to filter commits by",
			},
			"path": {
				Type:        "string",
				Description: "Only commits containing this file path will be returned",
			},
			"since": {
				Type:        "string",
				Description: "Only commits after this date will be returned (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DD)",
			},
			"until": {
				Type:        "string",
				Description: "Only commits before this date will be returned (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DD)",
			},
		},
		Required: []string{"owner", "repo"},
	}
	schema.Properties["fields"] = fieldsSchemaProperty(
		"Subset of fields to return for each commit. If omitted, all fields are returned. Use this to reduce response size when you only need specific fields, e.g. just 'sha' and 'html_url'.",
		listCommitsItemFieldEnum,
	)
	WithPagination(schema)
	return NewToolWithSchemaOptions[ListCommitsInput, []ListCommitOutput](
		ToolsetMetadataRepos,
		mcp.Tool{
			Name:        "list_commits",
			Description: t("TOOL_LIST_COMMITS_DESCRIPTION", "Get list of commits of a branch in a GitHub repository. Returns at least 30 results per page by default, but can return more if specified using the perPage parameter (up to 100)."),
			Annotations: &mcp.ToolAnnotations{
				Title:        t("TOOL_LIST_COMMITS_USER_TITLE", "List commits"),
				ReadOnlyHint: true,
			},
			InputSchema: schema,
		},
		scopes.PublicRead(scopes.Repo),
		inventory.TypedSchemaOptions{ValidationInputSchema: relaxedPaginationValidationSchema(schema)},
```

> Both schemas pass through `WithPagination`, which appends `page` and `perPage`; `list_commits` additionally receives a `fields` property from `fieldsSchemaProperty`. The response schema is declared by `MinimalCommit` / `[]ListCommitOutput`, not inline above.

---

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Every declared property has a type
- [ ] Required parameters are marked
- [ ] Defaults and enums are declared
- [ ] Pagination parameters are documented

### 2. Description Clarity
- [ ] Tool purpose is stated unambiguously
- [ ] Parameter semantics explain accepted values
- [ ] Enum values are explained in the description, not only listed

### 3. Integration Compatibility
- [ ] Conforms to the MCP tool contract (`name`, `description`, `inputSchema`, `annotations`)
- [ ] Annotations correctly express read-only behavior
- [ ] Schema is generated into valid JSON Schema at runtime

### 4. Example Quality
- [ ] Representative calls are documented (upstream README)
- [ ] Error cases (missing owner/repo/sha) are handled with actionable messages

### 5. Extensibility
- [ ] New tools follow the same `NewToolWithSchemaOptions` pattern
- [ ] Shared helpers (`WithPagination`, `fieldsSchemaProperty`) keep schemas consistent

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|---|---|---|---|
| Schema Completeness | 25% | | |
| Description Clarity | 25% | | |
| Integration Compatibility | 20% | | |
| Example Quality | 15% | | |
| Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

1. Call `get_commit` with all required fields and verify the `detail` default is `stats`.
2. Omit `owner`, `repo`, or `sha` and verify the tool returns an actionable error.
3. Call `list_commits` without `sha` and verify it resolves the default branch.
4. Request `fields: ["sha", "html_url"]` and verify the response is reduced.
5. Verify `page` / `perPage` are accepted and bounded.

---

## Notes

- Source file: `https://raw.githubusercontent.com/github/github-mcp-server/main/pkg/github/repositories.go`
- The quoted fragments are verbatim. Handler bodies are cut where marked by the excerpt boundary, not rewritten.
- This case was re-scoped on 2026-10-20 because its original gpt-researcher premise had no upstream tool schema.
