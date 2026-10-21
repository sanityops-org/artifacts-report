# TC-140: CSV Data Summarizer Skill - deeplogic-cli Evaluation Report

## Execution Record

| Item | Value |
|---|---|
| Source case | `test-cases/single-artifact/skill/TC-140-csv-data-summarizer-skill.md` |
| Evaluated artifact | `artifacts/TC-140-csv-data-summarizer-skill.SKILL.md` |
| Artifact extraction | Verbatim Skill Markdown, including YAML frontmatter |
| Tool | `deeplogic-cli 1.18.0` |
| Defect-check SDK | `defect-check 1.2.8` |
| Model | `anthropic / test-assistant` |
| Check level | **L2 completed** |
| Generated | 2026-10-20 18:43:13 |
| Inspection duration | 97.74s |
| Registered artifact | 0 Prompts, 0 Tools, 1 Skill |
| QD-S input length | 5,630 characters |

## Result

| Metric | Result |
|---|---:|
| Total defects | **16** |
| Severity | **P0: 5 / P1: 11 / P2: 0** |
| Score | **20.55 / 100** |
| Grade | **D** |
| Quality gate | **FAIL** |
| QC lint | **PASS** (0 defects) |
| Permission inspection | **Skipped** (`GATE0_BLOCKED`) |

This Skill has a strong trigger description and unusually explicit behavioral examples, but its instruction design is aggressively open-ended. It requires a complete analysis, all relevant visualizations, and no follow-up questions, while omitting input-size, runtime, failure, and permission boundaries. The CLI rates the resulting operational risk as severe.

## Defects

| Rule | Severity | Finding | Location | Recommended fix |
|---|---|---|---|---|
| QDS-1.1 | P0 | **Missing input-count limit.** The skill declares no maximum number of rows, columns, or file size, so it will process entire CSV files and can overflow context/token limits. Impact: The LLM processes all submitted content without truncation; if the user submits 500 items, it processes all 500, causing token overflow and uncontrolled cost | Skill metadata and Automatic Analysis Steps: 'Load and inspect the CSV file into pandas DataFrame' | Add a limit: 'Process at most 50 items. If more are provided, process the first 50 and notify the user.' |
| QDS-1.2 | P1 | **Missing output-size limit.** The skill requires comprehensive output and multiple visualizations but declares no output-size bound, which can overflow the context window. Impact: The response size explodes and overflows the context window, and the LLM may generate extremely long output | Automatic Analysis Steps: 'Generate comprehensive output automatically' and Example Output | Add: 'Limit output to 1,500 Chinese characters or 1,000 English words.' |
| QDS-1.3 | P0 | **Missing execution-resource boundaries.** No max_retries, max_tool_calls, or timeout are declared, so the LLM may retry or run tools without limit. Impact: The LLM retries or calls tools without limit, with every retry or call consuming tokens and time | Skill metadata and Files section | Add: 'Maximum retries: 3. Timeout: 60 seconds. Maximum tool calls per execution: 10.' |
| QDS-1.4 | P1 | **Missing permission boundaries.** The skill does not explicitly declare read/write/delete permissions; it only implies analysis, leaving broader operations unconstrained. Impact: The LLM interprets a broad capability description such as 'manage data' as implicit authorization for every operation, including DELETE | Description: 'Analyzes CSV files, generates summary stats, and plots quick visualizations' | List explicitly: 'Allowed: read and list. Prohibited: write, delete, update, and overwrite.' |
| QDS-1.5 | P1 | **Missing data-source boundaries.** The skill does not declare permitted or prohibited data sources, so the LLM may read arbitrary file paths or external data. Impact: The LLM gathers data from conversation history, external systems, or other Skills on its own | Usage: 'Accepts a path to a CSV file' | Declare: 'Use only data explicitly provided in the current request. Do not access conversation history or external systems.' |
| QDS-2.1 | P0 | **Unbounded comprehensive analysis and output.** Instructs the LLM to 'Run the comprehensive analysis' and 'Generate ALL relevant visualizations/charts' without any upper-bound constraint, leading to exhaustive processing. Impact: The LLM attempts exhaustive processing; 'process all files' means the LLM tries to process every single file | Critical Behavior Requirement and Automatic Analysis Steps sections | Replace 'all' with 'at most N items,' or add an explicit upper bound after the unbounded term. |
| QDS-3.2 | P1 | **Missing non-activation conditions.** The skill does not specify when it should not trigger, so it may activate for any CSV-related mention (e.g., a quick column rename or a CSV format question) and run an unwanted full analysis. Impact: The LLM forcibly activates the Skill in borderline scenarios and executes unrelated operations | When to Use This Skill / trigger conditions | Add: 'Do not activate for debugging, code review, or system-administration requests.' |
| QDS-3.3 | P1 | **No ambiguous-input handling policy.** There is no policy for missing file paths or unparseable input; the 'DO NOT ASK THE USER' instruction could cause the LLM to fabricate data instead of requesting the CSV. Impact: The LLM fills in missing input itself and may fabricate content, producing incorrect results | How It Works - CRITICAL BEHAVIOR REQUIREMENT / Usage | Add: 'When input is incomplete or ambiguous, ask the user instead of guessing.' |
| QDS-3.4 | P0 | **Missing non_goals.** The skill does not declare what it does not do, allowing scope creep beyond CSV summarization into data cleaning, transformation, or modeling. Impact: The LLM expands the task boundary to matters it considers reasonably related and executes operations beyond the intended scope | Skill description / top-level metadata | Add a 'Does not do' section: 'Does not infer from conversation history, add facts that were not provided, or expand into related tasks.' |
| QDS-3.6 | P1 | **Inaccurate capability description.** Notes claim visualizations are generated only when date columns exist, but the analysis steps also create histograms, heatmaps, and category charts; this contradiction misleads expected behavior. Impact: The LLM misunderstands the Skill's capabilities during the trigger stage, causing subsequent behavior to diverge from expectations | Notes - 'Generates visualizations only when date columns are present' | Rename it to describe the capability accurately, such as 'readonly-database-diagnostic' instead of 'database-maintenance-assistant.' |
| QDS-4.1 | P0 | **No failure-handling policy.** Skill instructs automatic comprehensive analysis but does not define stop, retry, report, or escalate behavior for failures such as missing files, parse errors, or empty data. Impact: The LLM explores alternative paths on its own, making its behavior unpredictable and potentially creating greater risk | Skill Content / How It Works / Automatic Analysis Steps | Add: 'If execution fails, stop immediately and report the error. Do not attempt alternatives.' |
| QDS-4.2 | P1 | **Partial completion acceptability not declared.** Skill demands complete analysis and forbids follow-up questions, but does not declare whether partial results are acceptable if full analysis cannot be completed. Impact: The LLM insists on completeness and enters an endless iteration cycle, consuming large amounts of tokens and time | Skill Content / How It Works / Behavior Guidelines | Add: 'Partial results are acceptable. When information is insufficient for a section, skip it or mark it as insufficient.' |
| QDS-4.3 | P1 | **No prohibited post-failure behaviors.** Skill does not explicitly prohibit scope expansion or fabricated data after failure, allowing the LLM to lower standards or invent insights when analysis fails. Impact: After a failure, the LLM lowers its standards or broadens the search scope and may fabricate data or execute unauthorized operations | Skill Content / How It Works / Behavior Guidelines | Add: 'After a failure, do not expand the task scope, fabricate data to fill gaps, or lower quality standards.' |
| QDS-5.1 | P1 | **Missing explicit read/write permissions.** The skill does not explicitly distinguish read, write, update, or delete permissions, leaving the LLM to infer an implicit operational boundary. Impact: The LLM interprets DELETE as a reasonable data operation and may execute destructive operations | description; Usage: summarize_csv(file_path) | List explicitly: 'Allowed: read, list, and query. Prohibited: write, update, delete, insert, and DROP.' |
| QDS-5.3 | P1 | **No environment boundary declaration.** The skill does not declare whether operations are restricted to local/sandbox environments or prohibit production/external/third-party targets. Impact: The LLM treats production environments, external networks, cloud storage, or third-party services as valid operation targets | description; Automatic Analysis Steps; Usage | Add: 'Do not access production databases, production APIs, live systems, or unauthorized external services. Use only local, test, or sandbox environments.' |
| QDS-5.4 | P1 | **Missing chained-invocation permissions.** The skill does not declare permitted or prohibited downstream Skills/tools, creating risk of indirect high-privilege operations. Impact: A low-privilege Skill indirectly reaches high-privilege operations by invoking another Skill, creating a privilege-escalation chain | metadata.dependencies; Automatic Analysis Steps | Add: 'May invoke only skill-A and skill-B. Invocation of skill-C, which has administrator privileges, is prohibited.' |

## Interpretation

**Strengths**

- The metadata names the Skill accurately and declares Python, pandas, matplotlib, and seaborn dependencies.
- The trigger section covers uploads, analysis, visualization, and insight requests.
- The examples and correct/forbidden behavior sections make the intended style easy to recognize.
- The Skill is self-contained and names the `summarize_csv(file_path)` entry point.

**Primary risks**

- No file-size, row-count, output-size, retry, timeout, or tool-call limits are declared.
- “Run the comprehensive analysis,” “Generate ALL relevant visualizations,” and “NO questions” combine into an unbounded execution contract.
- Missing or malformed input has no clarification or graceful-failure path.
- Read/write/delete permissions, data sources, execution environment, and chained tool permissions are not defined.

**Reviewer notes beyond the CLI result**

- Some security-oriented findings may be disproportionate for a locally executed CSV summarization Skill, but they are consistent with the CLI's L2 policy.
- The suggested fix for `QDS-3.6` (“readonly-database-diagnostic”) is unrelated to the Skill and should not be applied literally.
- The core resource-bound and failure-handling findings should be addressed regardless of whether every permission finding is adopted.

## Execution Caveats

- The final run skipped automatic corpus upload (`API key not configured`).
- Permission inspection was skipped because Gate-0 already found unfixed P0 defects and the Skill lacks a specific responsibility-boundary statement.
- The compatibility shim described in the combined summary was used for SDK/CLI interface compatibility only.

## Evidence

- [Raw deeplogic-cli report](./TC-140-csv-data-summarizer-skill.deeplogic-cli.inspect-raw.md)
- [CLI console log](./TC-140-csv-data-summarizer-skill.deeplogic-cli.console.log)
- [Run configuration](./runs/TC-140/inspect_config.yaml)
