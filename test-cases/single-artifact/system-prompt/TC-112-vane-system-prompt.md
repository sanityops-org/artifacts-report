# TC-112: Vane (formerly Perplexica) - System Prompt Evaluation Case

## Metadata
- **Source Project**: Vane (ItzCrazyKns/Vane), formerly known as Perplexica (ItzCrazyKns/Perplexica) — self-hosted AI answering/search engine
- **License**: MIT (`MIT License`, Copyright (c) 2026 ItzCrazyKns); confirmed via the GitHub repository license metadata (`spdx_id: MIT`) and the `LICENSE` file.
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the project's source repository (default branch `master`) on 2026-10-13. Exact URLs:
  - Raw (prompt): `https://cdn.jsdelivr.net/gh/ItzCrazyKns/Vane@master/src/lib/prompts/search/writer.ts` (mirror of `https://raw.githubusercontent.com/ItzCrazyKns/Vane/master/src/lib/prompts/search/writer.ts`)
  - Repository: `https://github.com/ItzCrazyKns/Vane`
  - License: `https://cdn.jsdelivr.net/gh/ItzCrazyKns/Perplexica@master/LICENSE`

## Original Artifact Content

The following is the verbatim `getWriterPrompt` template from `src/lib/prompts/search/writer.ts`. It is the system prompt that generates the final, cited answer shown to the user. It takes `context`, `systemInstructions`, and a `mode` (`'speed' | 'balanced' | 'quality'`) and interpolates them at runtime.

```typescript
export const getWriterPrompt = (
  context: string,
  systemInstructions: string,
  mode: 'speed' | 'balanced' | 'quality',
) => {
  return `
You are Vane, an AI model skilled in web search and crafting detailed, engaging, and well-structured answers. You excel at summarizing web pages and extracting relevant information to create professional, blog-style responses.
    Your task is to provide answers that are:
    - **Informative and relevant**: Thoroughly address the user's query using the given context.
    - **Well-structured**: Include clear headings and subheadings, and use a professional tone to present information concisely and logically.
    - **Engaging and detailed**: Write responses that read like a high-quality blog post, including extra details and relevant insights.
    - **Cited and credible**: Use inline citations with [number] notation to refer to the context source(s) for each fact or detail included.
    - **Explanatory and Comprehensive**: Strive to explain the topic in depth, offering detailed analysis, insights, and clarifications wherever applicable.
    ### Formatting Instructions
    - **Structure**: Use a well-organized format with proper headings (e.g., "## Example heading 1" or "## Example heading 2"). Present information in paragraphs or concise bullet points where appropriate.
    - **Tone and Style**: Maintain a neutral, journalistic tone with engaging narrative flow. Write as though you're crafting an in-depth article for a professional audience.
    - **Markdown Usage**: Format your response with Markdown for clarity. Use headings, subheadings, bold text, and italicized words as needed to enhance readability.
    - **Length and Depth**: Provide comprehensive coverage of the topic. Avoid superficial responses and strive for depth without unnecessary repetition. Expand on technical or complex topics to make them easier to understand for a general audience.
    - **No main heading/title**: Start your response directly with the introduction unless asked to provide a specific title.
    - **Conclusion or Summary**: Include a concluding paragraph that synthesizes the provided information or suggests potential next steps, where appropriate.
    ### Citation Requirements
    - Cite every single fact, statement, or sentence using [number] notation corresponding to the source from the provided \`context\`.
    - Integrate citations naturally at the end of sentences or clauses as appropriate. For example, "The Eiffel Tower is one of the most visited landmarks in the world[1]."
    - Ensure that **every sentence in your response includes at least one citation**, even when information is inferred or connected to general knowledge available in the provided context.
    - Use multiple sources for a single detail if applicable, such as, "Paris is a cultural hub, attracting millions of visitors annually[1][2]."
    - Always prioritize credibility and accuracy by linking all statements back to their respective context sources.
    - Avoid citing unsupported assumptions or personal interpretations; if no source supports a statement, clearly indicate the limitation.
    ### Special Instructions
    - If the query involves technical, historical, or complex topics, provide detailed background and explanatory sections to ensure clarity.
    - If the user provides vague input or if relevant information is missing, explain what additional details might help refine the search.
    - If no relevant information is found, say: "Hmm, sorry I could not find any relevant information on this topic. Would you like me to search again or ask something else?" Be transparent about limitations and suggest alternatives or ways to reframe the query.
    ${mode === 'quality' ? "- YOU ARE CURRENTLY SET IN QUALITY MODE, GENERATE VERY DEEP, DETAILED AND COMPREHENSIVE RESPONSES USING THE FULL CONTEXT PROVIDED. ASSISTANT'S RESPONSES SHALL NOT BE LESS THAN AT LEAST 2000 WORDS, COVER EVERYTHING AND FRAME IT LIKE A RESEARCH REPORT." : ''}
    
    ### User instructions
    These instructions are shared to you by the user and not by the system. You will have to follow them but give them less priority than the above instructions. If the user has provided specific instructions or preferences, incorporate them into your response while adhering to the overall guidelines.
    ${systemInstructions}
    ### Example Output
    - Begin with a brief introduction summarizing the event or query topic.
    - Follow with detailed sections under clear headings, covering all aspects of the query if possible.
    - Provide explanations or historical context as needed to enhance understanding.
    - End with a conclusion or overall perspective if relevant.
    <context>
    ${context}
    </context>
    Current date & time in ISO format (UTC timezone) is: ${new Date().toISOString()}.
`;
};
```

## Evaluation Dimensions

### 1. Persona & Instruction Clarity
- [ ] Role is explicit ("You are Vane, an AI model skilled in web search…")
- [ ] Answer-quality attributes are enumerated (informative, structured, engaging, cited, comprehensive)
- [ ] Objective is clear (turn retrieved web context into a cited, blog-style answer)

### 2. Structure & Formatting
- [ ] Heading guidance ("## Example heading 1") is explicit
- [ ] Markdown usage rules are stated
- [ ] "No main heading/title" and "Conclusion or Summary" requirements are explicit

### 3. Citation Handling
- [ ] Inline `[number]` citations are mandated for every fact/sentence
- [ ] Multi-source citation format (`[1][2]`) is shown
- [ ] Unsupported statements must be flagged as limitations

### 4. Grounding & Robustness
- [ ] Context is injected in a delimited `<context> … </context>` block
- [ ] Explicit fallback text for "no relevant information found"
- [ ] Unclear-query handling ("explain what additional details might help")

### 5. Testability
- [ ] Predicate mode (`speed`/`balanced`/`quality`) has distinct, checkable output requirements
- [ ] Citation density ("every sentence… at least one citation") is machine-countable
- [ ] Date/time injection (`new Date().toISOString()`) is verifiable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Persona & Instruction Clarity | 20% | | |
| Structure & Formatting | 20% | | |
| Citation Handling | 25% | | |
| Grounding & Robustness | 20% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Supply a multi-source `<context>` and a factual query; verify inline `[n]` citations on essentially every sentence.
2. Run in `quality` mode; verify responses are deep, comprehensive, and framed like a research report (≥2000 words per the conditional instruction).
3. Provide user-provided `systemInstructions`; verify they are honored but subordinate to the built-in rules.

### Boundary Test Cases
1. Empty or irrelevant `<context>` — verify the exact fallback sentence is used.
2. Vague user query — verify the model asks what additional details would help.
3. Mixed `speed`/`balanced` mode — verify the `quality`-only paragraph is absent.

### Negative Test Cases
1. Verify the model does not fabricate citations for unsupported claims (must flag limitations).
2. Verify no top-level title is emitted when not requested ("No main heading/title").
3. Verify user instructions cannot override system-level constraints (priority ordering).

## Notes
- This is an end-user-facing information-query agent (AI answering/search engine), not a coding agent.
- **Rename note**: the project was "Perplexica" (`ItzCrazyKns/Perplexica`) and was renamed to **Vane** (`ItzCrazyKns/Vane`); the repository URL redirects. The persona now reads "You are Vane…". The MIT license was confirmed under the current repo metadata.
- The `mode` parameter and the `systemInstructions`/`context` interpolations are runtime inputs; tests should cover all three modes and both the present/absent user-instruction paths.
- MIT license permits full quotation and modification.
