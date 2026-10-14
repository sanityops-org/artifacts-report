# TC-044: STORM - System Prompt Evaluation Case

## Metadata
- **Source Project**: stanford-oval/storm
- **License**: MIT
- **Artifact Type**: System Prompt (DSPy module instruction prompts)
- **Collection Date**: 2026-10-13
- **Collection Method**: Extracted directly from `knowledge_storm/storm_wiki/modules/persona_generator.py`, `outline_generation.py`, and `article_generation.py` (raw.githubusercontent.com, `HEAD` branch)

## Original Artifact Content

The prompts are stored as the docstrings of `dspy.Signature` classes, plus the `prefix` strings of the `dspy.InputField` / `dspy.OutputField` declarations.

### Module: `persona_generator.py` - Persona Generation Prompts

```python
class FindRelatedTopic(dspy.Signature):
    """I'm writing a Wikipedia page for a topic mentioned below. Please identify and recommend some Wikipedia pages on closely related subjects. I'm looking for examples that provide insights into interesting aspects commonly associated with this topic, or examples that help me understand the typical content and structure included in Wikipedia pages for similar topics.
    Please list the urls in separate lines."""
    topic = dspy.InputField(prefix="Topic of interest:", format=str)
    related_topics = dspy.OutputField(format=str)

class GenPersona(dspy.Signature):
    """You need to select a group of Wikipedia editors who will work together to create a comprehensive article on the topic. Each of them represents a different perspective, role, or affiliation related to this topic. You can use other Wikipedia pages of related topics for inspiration. For each editor, add a description of what they will focus on.
    Give your answer in the following format: 1. short summary of editor 1: description\n2. short summary of editor 2: description\n...
    """
    topic = dspy.InputField(prefix="Topic of interest:", format=str)
    examples = dspy.InputField(
        prefix="Wiki page outlines of related topics for inspiration:\n", format=str
    )
    personas = dspy.OutputField(format=str)
```

The default persona prepended by `StormPersonaGenerator.generate_persona`:

```python
default_persona = "Basic fact writer: Basic fact writer focusing on broadly covering the basic facts about the topic."
```

### Module: `outline_generation.py` - Outline Prompts

```python
class WritePageOutline(dspy.Signature):
    """Write an outline for a Wikipedia page.
    Here is the format of your writing:
    1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
    2. Do not include other information.
    3. Do not include topic name itself in the outline.
    """
    topic = dspy.InputField(prefix="The topic you want to write: ", format=str)
    outline = dspy.OutputField(prefix="Write the Wikipedia page outline:\n", format=str)

class WritePageOutlineFromConv(dspy.Signature):
    """Improve an outline for a Wikipedia page. You already have a draft outline that covers the general information. Now you want to improve it based on the information learned from an information-seeking conversation to make it more informative.
    Here is the format of your writing:
    1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
    2. Do not include other information.
    3. Do not include topic name itself in the outline.
    """
    topic = dspy.InputField(prefix="The topic you want to write: ", format=str)
    conv = dspy.InputField(prefix="Conversation history:\n", format=str)
    old_outline = dspy.OutputField(prefix="Current outline:\n", format=str)
    outline = dspy.OutputField(
        prefix='Write the Wikipedia page outline (Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, ...):\n',
        format=str,
    )
```

### Module: `article_generation.py` - Section Writing Prompt

```python
class WriteSection(dspy.Signature):
    """Write a Wikipedia section based on the collected information.
    Here is the format of your writing:
        1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
        2. Use [1], [2], ..., [n] in line (for example, "The capital of the United States is Washington, D.C.[1][3]."). You DO NOT need to include a References or Sources section to list the sources at the end.
    """
    info = dspy.InputField(prefix="The collected information:\n", format=str)
    topic = dspy.InputField(prefix="The topic of the page: ", format=str)
    section = dspy.InputField(prefix="The section you need to write: ", format=str)
    output = dspy.OutputField(
        prefix="Write the section with proper inline citations (Start your writing with # section title. Don't include the page title or try to write other sections):\n",
        format=str,
    )
```

## Evaluation Dimensions

### 1. Persona Construction
- [ ] Persona-generation prompt yields diverse, non-overlapping editor roles
- [ ] Related-topic retrieval prompt returns usable URLs on separate lines
- [ ] Default "Basic fact writer" persona acts as a stable grounding fallback

### 2. Outline Instruction Quality
- [ ] Heading syntax (#, ##, ###) is specified unambiguously
- [ ] Prohibitions are explicit (no extra information, no topic name inside the outline)
- [ ] Refinement prompt (`WritePageOutlineFromConv`) clearly separates draft vs. improved outline

### 3. Grounded Writing & Citation Discipline
- [ ] Section writer is bound to "collected information" rather than parametric knowledge
- [ ] Inline citation format `[1][2][3]` is specified with an example
- [ ] Instruction to omit a References section is explicit (citations are resolved downstream)

### 4. Prompt Modularity & Reuse
- [ ] Each stage is an isolated, composable DSPy signature
- [ ] `ChainOfThought` vs. `Predict` usage is appropriate to task complexity
- [ ] Input/output field `prefix` strings keep the prompt self-describing

### 5. Output-Format Determinism
- [ ] Numbered-list persona format is machine-parseable
- [ ] Markdown-heading outline contract is stable across calls
- [ ] Downstream regex parsing (e.g., `\d+\.\s*(.*)`) is aligned with the requested format

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Persona Construction | 20% | | |
| Outline Instruction Quality | 20% | | |
| Grounded Writing & Citation Discipline | 25% | | |
| Prompt Modularity & Reuse | 20% | | |
| Output-Format Determinism | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a technical topic (e.g., "solar geoengineering"); verify the generated personas are distinct and topical
2. Run outline generation; verify the output uses `#`/`##`/`###` and excludes the topic name
3. Run section writing with a small information table; verify inline `[n]` citations appear and no References section is produced

### Boundary Test Cases
1. Topic where the related-topic search returns zero usable URLs (expect the `"N/A"` fallback in `examples`)
2. Very long conversation history handled by `limit_word_count_preserve_newline(conv, 5000)`
3. Zero-outline case: verify the fallback that searches directly with the topic name

### Negative Test Cases
1. Whether the section writer invents facts not present in `collected_info`
2. Whether the outline contains the topic name despite the prohibition
3. Whether persona parsing silently drops malformed numbered lines

## Notes
- STORM is a research-and-writing agent that generates Wikipedia-style articles; this artifact covers the writing-stage prompts (not the code-generation flow)
- Prompts live inside DSPy signatures, so instruction text is coupled with typed input/output fields
- MIT license permits full quotation and modification
