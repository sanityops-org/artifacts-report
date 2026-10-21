# TC-195: mcp-server-youtube-transcript (kimtaeyoon83) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: kimtaeyoon83/mcp-server-youtube-transcript (MCP server for retrieving YouTube transcripts)
- **License**: MIT (see `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `get_transcript` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/index.ts` — the `TOOLS: Tool[]` array containing the `get_transcript` tool (raw JSON Schema `inputSchema`, `outputSchema`, and `annotations`)
  - `README.md` — Components/tool documentation
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### The `get_transcript` tool (`src/index.ts`, fetched verbatim)

```typescript
// Define tool configurations
const TOOLS: Tool[] = [
  {
    name: "get_transcript",
    description: "Extract transcript from a YouTube video URL or ID. Automatically falls back to available languages if requested language is not available.",
    inputSchema: {
      type: "object",
      properties: {
        url: {
          type: "string",
          description: "YouTube video URL or ID"
        },
        lang: {
          type: "string",
          description: "Language code for transcript (e.g., 'ko', 'en'). Will fall back to available language if not found.",
          default: "en"
        },
        include_timestamps: {
          type: "boolean",
          description: "Include timestamps in output (e.g., '[0:05] text'). Useful for referencing specific moments. Default: false",
          default: false
        },
        strip_ads: {
          type: "boolean",
          description: "Filter out sponsored segments from transcript based on chapter markers (e.g., chapters marked as 'Werbung', 'Ad', 'Sponsor'). Default: true",
          default: true
        }
      },
      required: ["url"]
    },
    // OutputSchema describes structuredContent format for Claude Code
    outputSchema: {
      type: "object",
      properties: {
        meta: { type: "string", description: "Title | Author | Subs | Views | Date" },
        content: { type: "string" }
      },
      required: ["content"]
    },
    annotations: {
      title: "Get Transcript",
      readOnlyHint: true,
      openWorldHint: true,
    },
  },
```

### Tool registration (`src/index.ts`, fetched verbatim)

```typescript
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: TOOLS
    }));
```

### Documented usage examples (from `README.md`, fetched verbatim)

```typescript
await server.callTool("get_transcript", {
  url: "https://www.youtube.com/watch?v=VIDEO_ID",
  lang: "en"
});
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete raw JSON Schema (`type: object`, `properties`, `required`)
- [ ] Types are accurate (`string`, `string`, `boolean`, `boolean`)
- [ ] Required vs optional parameters are distinguishable (`url` required; `lang`/`include_timestamps`/`strip_ads` have defaults)
- [ ] Defaults are declared inline (`lang="en"`, `include_timestamps=false`, `strip_ads=true`)

### 2. Description Clarity
- [ ] The tool description states the capability and the language-fallback behavior
- [ ] Every parameter has a human-readable `description`
- [ ] The `strip_ads` description explains the mechanism (chapter markers) and gives examples

### 3. Integration Compatibility
- [ ] Built with the official `@modelcontextprotocol/sdk` `Server` class
- [ ] Both an `inputSchema` and an `outputSchema` are declared, and `annotations` carry `readOnlyHint`/`openWorldHint`
- [ ] The raw JSON Schema is standards-compliant and consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] Concrete examples are embedded (`'[0:05] text'`, `'Werbung'`, `'ko'`, `'en'`)
- [ ] The README provides runnable `callTool` examples for URL, video ID, Shorts URL, and timestamp variants
- [ ] The `outputSchema` documents the response shape (`meta`, `content`)

### 5. Extensibility
- [ ] Tools are declared in a single `TOOLS` array, so the optional `analyze_video` tool is added as a sibling entry
- [ ] The optional TwelveLabs-backed tool is gated on `TWELVELABS_API_KEY`, keeping the transcript tool credential-free
- [ ] Multiple URL formats (watch, Shorts, bare ID) are normalized internally, so the schema stays simple

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Schema Completeness | 25% | | |
| Description Clarity | 20% | | |
| Integration Compatibility | 25% | | |
| Example Quality | 20% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "get the transcript of https://www.youtube.com/watch?v=VIDEO_ID"; verify `get_transcript` is called with `url` set to the full URL (default `lang: "en"`).
2. Issue "summarize this Korean video"; verify `url` is set and `lang: "ko"`.
3. Issue "give me the transcript with timestamps"; verify `include_timestamps: true`.

### Boundary Test Cases
1. `lang` for a video without that language; verify the documented automatic fallback and the resulting notice.
2. A bare 11-character video ID (no URL); verify the ID is accepted.
3. A YouTube Shorts URL; verify the `/shorts/{id}` path is parsed.
4. `strip_ads` at both `true` and `false`; verify the filtering behavior difference on a chapter-marked video.

### Negative Test Cases
1. `get_transcript` without the required `url`; verify the handler throws an `InvalidParams` error.
2. A malformed URL/ID (not a valid URL and not an ID pattern); verify it is rejected.
3. `lang` provided as a non-string; verify type validation rejects it.
4. A video with no available transcript; verify the documented "unavailable transcript" error path.

## Notes
- This is one logical artifact: the `get_transcript` tool. The server also exposes `analyze_video` (TwelveLabs Pegasus).
- The `inputSchema`/`outputSchema` are author-written raw JSON Schemas, quoted verbatim from `src/index.ts`. The `outputSchema` is documented in-source as describing `structuredContent` for Claude Code.
- A useful quality discussion point: `strip_ads` filters by chapter markers, and the handler adds fallback notices when no chapter markers exist — schema description and runtime behavior are aligned.
- License is MIT; verbatim quotation is permissible.
