# TC-038: AnythingLLM Agent - Knowledge Base/RAG Agent Suite

## Metadata
- **Source Project**: AnythingLLM Agent (Mintplex-Labs/anything-llm)
- **GitHub**: github.com/Mintplex-Labs/anything-llm
- **License**: MIT
- **Artifact Type**: Knowledge base/RAG agent with skills and tools
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction at commit 2a10d052a1812d7be12c43f9024072cf26a27a8b
- **Scope**: Workspace @agent; four default JS Skills and the dedicated opt-in clarifying-question feature; native and fallback tool-calling modes

---

## Project Overview

AnythingLLM is an all-in-one document chat platform with a powerful **workspace agent** that combines RAG (Retrieval-Augmented Generation) capabilities with autonomous tool use. The agent can search local documents, store information to memory, summarize content, and browse the web.

### Key Characteristics
- **RAG-based memory**: Search and store information in vector database
- **4 default skills**: Memory, document summarization, web scraping, web browsing — plus opt-in clarifying-questions tools (request-user-input)
- **Dynamic skill loading**: Skills can be enabled/disabled per workspace
- **Multi-user mode support**: Single-user only skills are gated
- **MCP compatibility**: Integration with Model Context Protocol

---

## Agent Definition

### Workspace Agent Configuration

```javascript
const USER_AGENT = {
  name: "USER",
  getDefinition: () => {
    return {
      interrupt: "ALWAYS",
      role: "I am the human monitor and oversee this chat. Any questions on action or decision making should be directed to me.",
    };
  },
};

const WORKSPACE_AGENT = {
  name: "@agent",
  /**
   * Get the definition for the workspace agent with its role (prompt) and functions in Aibitat format
   * @param {string} _provider - Unused, kept for call-site compatibility
   * @param {import("@prisma/client").workspaces | null} workspace
   * @param {import("@prisma/client").users | null} user
   * @param {string} [prompt] - Current user message for memory reranking
   * @returns {Promise<{ role: string, functions: object[] }>}
   */
  getDefinition: async (
    _provider = null,
    workspace = null,
    user = null,
    prompt = ""
  ) => {
    let [role, clarifyingQuestionsSkills] = await Promise.all([
      Provider.systemPrompt({
        workspace,
        user,
        prompt,
      }),
      clarifyingQuestionsSkillIfEnabled(),
    ]);

    // If clarifying questions tools are enabled, add a note to the role that the user must use the request-user-input tool to ask questions.
    if (!!clarifyingQuestionsSkills?.length)
      role +=
        "\n\nWhen you need information from the user (URLs, file paths, preferences, choices, etc.), you MUST use the request-user-input tool. Do not ask questions in your text response - the user cannot reply to text. Only the tool can collect user input.";

    return {
      role,
      functions: [
        ...(await agentSkillsFromSystemSettings()),
        ...clarifyingQuestionsSkills,
        ...ImportedPlugin.activeImportedPlugins(),
        ...AgentFlows.activeFlowPlugins(),
        ...(await new MCPCompatibilityLayer().activeMCPServers()),
      ],
    };
  },
};
```

---

## Skill Definitions

### 1. Memory (RAG) Skill

```javascript
const memory = {
  name: "rag-memory",
  startupConfig: {
    params: {},
  },
  plugin: function () {
    return {
      name: this.name,
      setup(aibitat) {
        aibitat.function({
          super: aibitat,
          tracker: new Deduplicator(),
          name: this.name,
          description:
            "Search your local documents and workspace files for relevant information, or store information to long-term memory. Use search to find answers in uploaded documents, embedded files, or previously stored memories. Use store only when explicitly asked to remember or save something.",
          examples: [
            {
              prompt: "Check my files for information about the project",
              call: JSON.stringify({
                action: "search",
                content: "<project information to search for>",
              }),
            },
            {
              prompt: "What do you know about Plato's motives?",
              call: JSON.stringify({
                action: "search",
                content: "What are the facts about Plato's motives?",
              }),
            },
            {
              prompt: "Remember that you are a robot",
              call: JSON.stringify({
                action: "store",
                content: "I am a robot, the user told me that i am.",
              }),
            },
          ],
          parameters: {
            $schema: "http://json-schema.org/draft-07/schema#",
            type: "object",
            properties: {
              action: {
                type: "string",
                enum: ["search", "store"],
                description:
                  "The action we want to take to search for existing similar context or storage of new context.",
              },
              content: {
                type: "string",
                description:
                  "The plain text to search our local documents with or to store in our vector database.",
              },
            },
            additionalProperties: false,
          },
          handler: async function ({ action = "", content = "" }) {
            try {
              const { isDuplicate } = this.tracker.isDuplicate(this.name, {
                action,
                content,
              });
              if (isDuplicate)
                return `This was a duplicated call and it's output will be ignored.`;

              let response = "There was nothing to do.";
              if (action === "search") response = await this.search(content);
              if (action === "store") response = await this.store(content);

              this.tracker.trackRun(this.name, { action, content });
              return response;
            } catch (error) {
              console.log(error);
```

---

## Default Skills Configuration

```javascript
// This is a list of skills that are built-in and default enabled.
const DEFAULT_SKILLS = [
  AgentPlugins.memory.name,
  AgentPlugins.docSummarizer.name,
  AgentPlugins.webScraping.name,
  AgentPlugins.webBrowsing.name,
];

// Skills that must never be injected when the instance is running in multi-user mode.
const SINGLE_USER_ONLY_SKILLS = new Set(["create-scheduled-job"]);

/**
 * Configuration for agent skills that require availability checks and disabled sub-skill lists.
 * Each entry maps a skill name to its availability checker and disabled skills list key.
 */
const SKILL_FILTER_CONFIG = {
  "filesystem-agent": {
    getAvailability: () =>
      require("./aibitat/plugins/filesystem/lib").isToolAvailable(),
    disabledSettingKey: "disabled_filesystem_skills",
  },
  "create-files-agent": {
    getAvailability: () =>
      require("./aibitat/plugins/create-files/lib").isToolAvailable(),
    disabledSettingKey: "disabled_create_files_skills",
  },
  "gmail-agent": {
    getAvailability: async () =>
      require("./aibitat/plugins/gmail/lib").GmailBridge.isToolAvailable(),
    disabledSettingKey: "disabled_gmail_skills",
  },
  "outlook-agent": {
    getAvailability: async () =>
      require("./aibitat/plugins/outlook/lib").OutlookBridge.isToolAvailable(),
    disabledSettingKey: "disabled_outlook_skills",
  },
  "google-calendar-agent": {
    getAvailability: async () =>
      require("./aibitat/plugins/google-calendar/lib").GoogleCalendarBridge.isToolAvailable(),
    disabledSettingKey: "disabled_google_calendar_skills",
  },
};
```

---

## Available Skills (5 Total)

| Skill (registered slug) | Plugin key | Description | Default |
|-------|-------------|---------|------|
| rag-memory | ragMemory | Search/store in vector database | Yes |
| document-summarizer | docSummarizer | Summarize documents | Yes |
| web-scraping | webScraping | Scrape web content | Yes |
| web-browsing | webBrowsing | Browse the web | Yes |
| request-user-input | clarifyingQuestions | Ask user for input | Opt-in |

*(Note — `DEFAULT_SKILLS` contains exactly 4 entries (memory, doc summarizer, web scraping, web browsing); `request-user-input` is only enabled when `agent_clarifying_questions_enabled` is `"true"`.)*

---

## Evaluation Dimensions

### 1. RAG Integration Quality
- [ ] Vector database search works reliably
- [ ] Store operation persists information
- [ ] Deduplication prevents redundant calls
- [ ] Error handling is comprehensive

### 2. Skill Architecture
- [ ] Skills are modular and independent
- [ ] JSON schema for parameters
- [ ] Examples provided for guidance
- [ ] Handler implementation is clear

### 3. Multi-User Support
- [ ] Single-user skills are gated
- [ ] Availability checks for external services
- [ ] Disabled skills configuration
- [ ] Workspace-level skill control

### 4. Tool Integration
- [ ] Dynamic function loading
- [ ] MCP protocol support
- [ ] Imported plugin support
- [ ] Agent flow plugins

### 5. User Interaction
- [ ] Clarifying questions opt-in
- [ ] Tool-based user input collection
- [ ] Clear guidance in system prompt
- [ ] Text vs tool distinction

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| RAG Integration Quality | 25% | | |
| Skill Architecture | 25% | | |
| Multi-User Support | 15% | | |
| Tool Integration | 20% | | |
| User Interaction | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### RAG Functionality Tests
1. Search for information in uploaded documents
2. Store new information to memory
3. Test deduplication behavior
4. Verify vector database persistence

### Skill Loading Tests
1. Verify default skills are loaded
2. Test disabled skill configuration
3. Verify multi-user mode restrictions
4. Test availability checks for external skills

### User Interaction Tests
1. Enable clarifying questions
2. Test request-user-input tool
3. Verify tool vs text distinction
4. Test user input collection

### MCP Integration Tests
1. Connect external MCP servers
2. Invoke MCP tools
3. Test tool schema discovery

---

## Notes

- AnythingLLM demonstrates RAG-first agent design
- Memory skill combines search and store in one tool
- Deduplication prevents wasteful vector operations
- Multi-user mode gating ensures security
- MIT license allows full examination and modification
- Shows best practices for document-centric agents
- Good reference for building knowledge base agents