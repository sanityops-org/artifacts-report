# TC-001: GPT Researcher - System Prompt 评估用例

## 元信息
- **来源项目**: gpt-researcher (assafelovic/gpt-researcher)
- **许可证**: Apache-2.0
- **工件类型**: System Prompt
- **采集日期**: 2026-10-10
- **采集方式**: 直接提取自 prompts.py

## 原始工件内容

### generate_report_prompt 方法

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

## 评估维度

### 1. 指令清晰度 (Instruction Clarity)
- [ ] 指令无歧义，LLM 能准确理解任务目标
- [ ] 输出格式要求明确（markdown、APA格式、字数要求）
- [ ] 约束条件清晰（必须/禁止事项明确标注）

### 2. 结构化程度 (Structure)
- [ ] 使用明确的标题层级指令 (# ## ###)
- [ ] 有清晰的段落组织要求
- [ ] 包含表格等结构化元素的使用指导

### 3. 引用与来源处理 (Citation Handling)
- [ ] 明确引用格式要求（APA）
- [ ] 区分 Web 来源与本地文档的不同处理方式
- [ ] 要求去重和超链接格式

### 4. 质量控制 (Quality Control)
- [ ] 要求基于给定信息形成独立观点
- [ ] 强调来源的可信度和时效性
- [ ] 禁止无意义的一般性结论

### 5. 可测试性 (Testability)
- [ ] 输出可量化评估（字数、引用数量）
- [ ] 有明确的格式检查点
- [ ] 支持自动化验证（如引用格式检查）

## 评分标准
| 维度 | 权重 | 得分 (1-5) | 备注 |
|------|------|------------|------|
| 指令清晰度 | 25% | | |
| 结构化程度 | 20% | | |
| 引用与来源处理 | 25% | | |
| 质量控制 | 20% | | |
| 可测试性 | 10% | | |
| **总分** | 100% | | |

## 测试建议

### 正向测试用例
1. 提供完整上下文，验证报告生成质量
2. 测试不同 report_source 类型（Web/Local）的引用差异
3. 验证 tone 参数对输出风格的影响

### 边界测试用例
1. 上下文为空或极短时的处理
2. 超长上下文（>token limit）的处理
3. 多语言输出验证

### 负面测试用例
1. 检查是否会出现幻觉内容（与上下文不符的信息）
2. 验证是否遵循"不生成目录"的约束
3. 检查引用格式的一致性

## 备注
- 该 prompt 用于研究报告生成场景，是典型的"信息综合类"System Prompt
- 包含动态参数注入（question, context, tone 等），测试时需关注参数边界
- Apache-2.0 许可允许完整引用和修改
