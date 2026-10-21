# TC-111: SalesGPT System Prompt - deeplogic-cli Evaluation Report

## Execution Record

| Item | Value |
|---|---|
| Source case | `test-cases/single-artifact/system-prompt/TC-111-salesgpt-system-prompt.md` |
| Evaluated artifact | `artifacts/TC-111-salesgpt-system-prompt.prompt.txt` |
| Artifact extraction | Python literal value of `SALES_AGENT_TOOLS_PROMPT`; assignment wrapper and Markdown were excluded |
| Tool | `deeplogic-cli 1.18.0` |
| Defect-check SDK | `defect-check 1.2.8` |
| Model | `anthropic / test-assistant` |
| Check level | **L1 completed** |
| Generated | 2026-10-20 19:07:04 |
| Inspection duration | 381.62s |
| Registered artifact | 1 Prompt, 0 Tools, 0 Skills |
| QD-P input length | 3,338 characters |

## Result

| Metric | Result |
|---|---:|
| Total defects | **3** |
| Severity | **P0: 1 / P1: 2 / P2: 0** |
| Score | **89.22 / 100** |
| Grade | **B** |
| Quality gate | **FAIL** |
| QC lint | **PASS** (2 P1 warnings) |
| Permission inspection | **Skipped** (`GATE0_BLOCKED`) |

The prompt is substantially complete and has a recognizable sales workflow, but it contains one direct behavioral conflict. The first-turn greeting rule says not to pitch, while the Introduction stage says to introduce the person and company and explain the reason for the call. The CLI therefore fails the quality gate despite the relatively high numeric score.

## Defects

| Rule | Severity | Finding | Location | Recommended fix |
|---|---|---|---|---|
| QDP-1.1.1 | P0 | **Direct Conflict.** The first-turn rule instructs the salesperson to only greet the prospect and ask how they are doing ('without pitching'), while the Introduction stage rule requires introducing the salesperson and company and always clarifying the reason for the call in the greeting. These cannot both be followed on the first turn. Impact: The LLM's behavior is unpredictable under contradictory instructions; it may choose any one of them, resulting in inconsistent output | 'Start the conversation by just a greeting and how is the prospect doing without pitching in your first turn.' vs '1: Introduction... Always clarify in your greeting the reason why you are calling.' | Remove one of the conflicting rules, or add a priority declaration specifying which rule takes precedence |
| QDP-1.3.2 | P1 | **Vague Qualifier.** 'short length' is not operationalized; the prompt does not specify a word count, sentence count, or other objective measure, so the required response length is ambiguous. Impact: The LLM interprets vague qualifiers inconsistently, causing substantial output variation across calls | 'Keep your responses in short length to retain the user's attention.' | Replace vague qualifiers with quantifiable criteria, such as no more than 500 characters or within 30 seconds |
| QDP-2.3.1 | P1 | **Undefined Output Format.** The prompt does not define how the <END_OF_CALL> token should be formatted in relation to the required response format. It is unclear whether the final output should consist solely of the token, include it in the salesperson line, or append it after a Thought line. Impact: The LLM produces inconsistent output formats that downstream systems cannot parse | 'When the conversation is over, output <END_OF_CALL>' vs 'you MUST use the format: Thought: ... {salesperson_name}: [your response here]' | Declare the output format: output must be JSON containing the fields title, content, and summary |

## QC Lint

| Rule | Severity | Line | Finding | Fix |
|---|---|---:|---|---|
| QC-0.2 | P1 | 24 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |
| QC-0.2 | P1 | 32 | Code block has no explicit language identifier | Add language identifier after opening backticks (e.g., ```python) |

## Interpretation

**Strengths**

- Persona, company, purpose, channel, and conversation stages are clearly parameterized.
- The prompt defines an explicit tool-call protocol and a stable response envelope.
- It has a structured eight-stage sales conversation ladder and a clear end-of-call signal.

**Primary risks**

- The greeting conflict creates observable turn-to-turn inconsistency.
- “Short length” is not measurable and should be replaced by a concrete sentence, word, or character limit.
- `<END_OF_CALL>` is not integrated into the required `Thought`/salesperson response format, making downstream parsing ambiguous.

## Execution Caveats

- Two L2 attempts timed out after approximately 488 seconds without producing defect data. The completed L1 run is used as the official result and still applies the same QDP defect rules, but at reduced inspection depth.
- The final run skipped automatic corpus upload (`API key not configured`).
- A compatibility shim adapted the CLI to the installed SDK by accepting an unsupported `force_permission` option, ignoring an unsupported timeout constructor argument, and awaiting a synchronous `close()`. It did not change the artifact, rules, or scoring.
- The permission inspection was skipped because Gate-0 already found an unfixed P0 and the prompt lacks a specific responsibility-boundary statement.

## Evidence

- [Raw deeplogic-cli report](./TC-111-salesgpt-system-prompt.deeplogic-cli.inspect-raw.md)
- [CLI console log](./TC-111-salesgpt-system-prompt.deeplogic-cli.console.log)
- [Run configuration](./runs/TC-111/inspect_config.yaml)
