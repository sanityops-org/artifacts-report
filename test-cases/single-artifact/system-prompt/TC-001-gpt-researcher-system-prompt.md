# TC-001: GPT Researcher - System Prompt Evaluation Case

## Metadata
- **Source Project**: gpt-researcher (assafelovic/gpt-researcher)
- **License**: Apache-2.0
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-10
- **Collection Method**: Extracted directly from prompts.py

## Original Artifact Content

### generate_report_prompt Method

```python
@staticmethod
def generate_report_prompt(
    question: str,
    context,
    report_source: str,
    report_format="apa",
    total_words=1000,
    tone=None,
    language="english",
):
    """Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            research_summary (str): The research summary to generate the report prompt for
    Returns: str: The report prompt for the given question and research summary
    """
    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.
Every url should be hyperlinked: [url website](url)
Additionally, you MUST include hyperlinks to the relevant URLs wherever they are referenced in the report:
eg: Author, A. A. (Year, Month Date). Title of web page. Website Name. [url website](url)
"""
    else:
        reference_prompt = f"""
You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
"""
    tone_prompt = f"Write the report in a {tone.value} tone." if tone else ""
    return f"""
Information: "{context}"
---
Using the above information, answer the following query or task: "{question}" in a detailed report --
The report should focus on the answer to the query, should be well structured, informative,
in-depth, and comprehensive, with facts and numbers if available and at least {total_words} words.
You should strive to write the report as long as you can using all relevant and necessary information provided.
Please follow all of the following guidelines in your report:
- You MUST determine your own concrete and valid opinion based on the given information. Do NOT defer to general and meaningless conclusions.
- You MUST write the report with markdown syntax and {report_format} format.
- Structure your report with clear markdown headers: use # for the main title, ## for major sections, and ### for subsections.
- Use markdown tables when presenting structured data or comparisons to enhance readability.
- You MUST prioritize the relevance, reliability, and significance of the sources you use. Choose trusted sources over less reliable ones.
- You must also prioritize new articles over older articles if the source can be trusted.
- You MUST NOT include a table of contents, but DO include proper markdown headers (# ## ###) to structure your report clearly.
- Use in-text citation references in {report_format} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
- Don't forget to add a reference list at the end of the report in {report_format} format and full url links without hyperlinks.
- {reference_prompt}
- {tone_prompt}
You MUST write the report in the following language: {language}.
Please do your best, this is very important to my career.
Assume that the current date is {date.today()}.
"""
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Instructions are unambiguous; the LLM can accurately understand the task objective
- [ ] Output format requirements are explicit (markdown, APA format, word count requirements)
- [ ] Constraints are clear (must/forbidden items explicitly marked)

### 2. Structure
- [ ] Uses explicit heading hierarchy instructions (# ## ###)
- [ ] Clear paragraph organization requirements
- [ ] Includes guidance on using structured elements such as tables

### 3. Citation Handling
- [ ] Explicit citation format requirements (APA)
- [ ] Distinguishes handling between Web sources and local documents
- [ ] Requires deduplication and hyperlink formats

### 4. Quality Control
- [ ] Requires forming an independent opinion based on the given information
- [ ] Emphasizes source credibility and timeliness
- [ ] Prohibits meaningless general conclusions

### 5. Testability
- [ ] Output is quantitatively evaluable (word count, citation count)
- [ ] Clear format checkpoints
- [ ] Supports automated verification (e.g., citation format checking)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 25% | | |
| Structure | 20% | | |
| Citation Handling | 25% | | |
| Quality Control | 20% | | |
| Testability | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide complete context and verify report generation quality
2. Test citation differences across different `report_source` types (Web/Local)
3. Verify the effect of the `tone` parameter on output style

### Boundary Test Cases
1. Handling when context is empty or extremely short
2. Handling of overly long context (>token limit)
3. Multi-language output verification

### Negative Test Cases
1. Check whether hallucinated content appears (information inconsistent with context)
2. Verify compliance with the "no table of contents" constraint
3. Check citation format consistency

## Notes
- This prompt is used in research report generation scenarios, a typical "information synthesis" System Prompt
- Contains dynamic parameter injection (question, context, tone, etc.); pay attention to parameter boundaries during testing
- The Apache-2.0 license allows full quotation and modification
