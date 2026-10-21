# TC-046: GPT-Author - System Prompt Evaluation Case

## Metadata
- **Source Project**: mshumer/gpt-author
- **License**: MIT
- **Artifact Type**: System Prompt (multi-stage prompt chain for novel writing)
- **Collection Date**: 2026-10-13
- **Collection Method**: Extracted directly from `gpt_author_v2.ipynb` (raw.githubusercontent.com, `main` branch); the notebook is the canonical source, as the `.py` variant was not fetchable

## Original Artifact Content

### Stage 1-4: Plot Generation, Selection, Improvement, Title

```python
def generate_plots(prompt):
    ...
        messages=[
            {"role": "system", "content": "You are a creative assistant that generates engaging fantasy novel plots."},
            {"role": "user", "content": f"Generate 10 fantasy novel plots based on this prompt: {prompt}"}
        ]

def select_most_engaging(plots):
    ...
        messages=[
            {"role": "system", "content": "You are an expert in writing fantastic fantasy novel plots."},
            {"role": "user", "content": f"Here are a number of possible plots for a new novel: {plots}\n\n--\n\nNow, write the final plot that we will go with. It can be one of these, a mix of the best elements of multiple, or something completely new and better. The most important thing is the plot should be fantastic, unique, and engaging."}
        ]

def improve_plot(plot):
    ...
        messages=[
            {"role": "system", "content": "You are an expert in improving and refining story plots."},
            {"role": "user", "content": f"Improve this plot: {plot}"}
        ]

def get_title(plot):
    ...
        messages=[
            {"role": "system", "content": "You are an expert writer."},
            {"role": "user", "content": f"Here is the plot: {plot}\n\nWhat is the title of this book? Just respond with the title, do nothing else."}
        ]
```

### Stage 5: Storyline Generation (with output-format contract)

```python
def generate_storyline(prompt, num_chapters):
    json_format = """[{"Chapter CHAPTER_NUMBER_HERE - CHAPTER_TITLE_GOES_HERE": "CHAPTER_OVERVIEW_AND_DETAILS_GOES_HERE"}, ...]"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a world-class fantasy writer. Your job is to write a detailed storyline, complete with chapters, for a fantasy novel. Don't be flowery -- you want to get the message across in as few words as possible. But those words should contain lots of information."},
            {"role": "user", "content": f'Write a fantastic storyline with {num_chapters} chapters and high-level details based on this plot: {prompt}.\n\nDo it in this list of dictionaries format {json_format}'}
        ]
    )
    ...
    improved_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a world-class fantasy writer. Your job is to take your student's rough initial draft of the storyline of a fantasy novel, and rewrite it to be significantly better."},
            {"role": "user", "content": f"Here is the draft storyline they wrote: {response['choices'][0]['message']['content']}\n\nNow, rewrite the storyline, in a way that is far superior to your student's version. It should have the same number of chapters, but it should be much improved in as many ways as possible. Remember to do it in this list of dictionaries format {json_format}"}
        ]
    )
```

### Stage 6: First Chapter (Claude two-pass path)

```python
prompt_one = f"\n\nHuman: You are a world-class fantasy writer. I will give you the title of a novel, a high-level plot to follow, and a desired writing style to use. From the title, plot, and writing style, write the first chapter of the novel. Make it incredibly unique, engaging, and well-written. Start it off with a bang, and include dialogue. Include only the chapter text, and no surrounding explanations or text. Do you understand?\n\nAssistant: Yes, I understand. Please provide the title, plot, and writing style, and I will write a fantastic opening chapter with dialogue that will hook the reader.\n\nHuman: Here is the high-level plot to follow: {plot}\n\The title of the novel is: `{first_chapter_title}`.\n\nHere is a description of the writing style you should use: `{writing_style}`\n\nWrite the first chapter please!\n\nAssistant: Okay, I've got a really exciting first chapter for you. It's twenty paragraphs long and very well-written. As you can see, the language I use is very understandable — I avoided using overly complex words and phrases:\n\nTitle: {first_chapter_title}\n\nChapter #1 Text```"

prompt_two = f"\n\nHuman: You are a world-class fantasy writer. Your job is to take your student's rough initial draft of the first chapter of their fantasy novel, and rewrite it to be significantly better, with much more detail. Do you understand?\n\nAssistant: Yes, I understand. Please provide the plot and the student-written chapter, and I will rewrite the chapter in a far superior way.\n\nHuman: Here is the high-level plot you asked your student to follow: {plot}\n\nHere is the first chapter they wrote: {initial_first_chapter}\n\nNow, rewrite the first chapter of this novel, in a way that is far superior to your student's chapter. It should still follow the exact same plot, but it should be far more detailed, much longer, and more engaging. Here is a description of the writing style you should use: `{writing_style}`\n\nAssistant: Okay, I've rewritten the first chapter. I took great care to improve it. While the plot is the same, you can see that my version is noticeably longer, easier to read, and more exciting. Also, the language I used is far more accessible to a broader audience.\n\n```"
```

### Stage 7: Subsequent Chapters

```python
prompt = f"\n\nHuman: You are a world-class fantasy writer. I will provide you with the plot of the novel, the previous chapters, and the plan for the next chapter. Your task is to write the next chapter of the novel, following the plot and taking in the previous chapters as context. Do you understand?\n\nAssistant: Yes, I understand. You want me to write the next chapter of a novel, using the plot you provide, the previous chapters for context, and a specific plan for the next chapter. I will ensure the chapter is beautifully written and I will not rewrite the chapter name.\n\nHuman: That's correct. Here is the plot: {plot}\n\nHere are the previous chapters: {previous_chapters}\n\nHere is the plan for the next chapter: {chapter_title}\n\nWrite it beautifully. Include only the chapter text. There is no need to rewrite the chapter name.\n\nAssistant: Here is the next chapter. As you can see, it's around the same length as the previous chapters, and contains witty dialogue:\n```Chapter"
```

### Stage 8: Cover-Art Spec

```python
def generate_cover_prompt(plot):
    ...
        messages=[
            {"role": "system", "content": "You are a creative assistant that writes a spec for the cover art of a book, based on the book's plot."},
            {"role": "user", "content": f"Plot: {plot}\n\n--\n\nDescribe the cover we should create, based on the plot. This should be two sentences long, maximum."}
        ]
```

## Evaluation Dimensions

### 1. Chain Coherence & Handoff
- [ ] Each stage's output is a valid input to the next (plot → storyline → chapters)
- [ ] `write_fantasy_novel` orchestrates the stages in a consistent order
- [ ] Passing of `writing_style` and `plot` across stages is consistent

### 2. Role / Persona Consistency
- [ ] Persona evolves deliberately ("creative assistant" → "expert" → "world-class fantasy writer")
- [ ] The "student vs. teacher" refinement metaphor is applied consistently
- [ ] Assistant prefill turns reinforce the requested voice without contradicting the system role

### 3. Output-Contract Enforcement
- [ ] Storyline is constrained to a parseable list-of-dictionaries format
- [ ] Chapter prompts require "only the chapter text" (no chapter-name rewrite)
- [ ] Cover prompt enforces a two-sentence maximum

### 4. Refinement-Loop Quality
- [ ] Draft → improve pattern is applied to plot, storyline, and first chapter
- [ ] Improvement prompts require preserving the plot while increasing detail/length
- [ ] Length-minimum retry loop (discard chapters shorter than 100 characters) is defined

### 5. Robustness & Cleanup
- [ ] Markdown fence stripping (`split('```')[0]`) aligns with the requested output format
- [ ] `get_title` isolates the title ("Just respond with the title, do nothing else")
- [ ] JSON-string / literal-eval handling (`ast.literal_eval`) matches the storyline contract

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Chain Coherence & Handoff | 25% | | |
| Role / Persona Consistency | 20% | | |
| Output-Contract Enforcement | 25% | | |
| Refinement-Loop Quality | 20% | | |
| Robustness & Cleanup | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Run the full chain on a short premise; verify the final storyline parses as a list of dictionaries
2. Verify that improved chapters are longer and still follow the plot
3. Verify the title stage returns only the title string

### Boundary Test Cases
1. `num_chapters = 1` (single-chapter book; loop `range(num_chapters - 1)` produces no extra chapters)
2. Chapter output shorter than the 100-character minimum; verify the retry path
3. Writing style omitted or extremely short

### Negative Test Cases
1. Whether chapter text leaks explanations or the chapter name (contract violation)
2. Whether the "include only chapter text" and fence-stripping assumptions break on unexpected output
3. Whether later chapters contradict the established plot (continuity drift)

## Notes
- GPT-Author is a creative-writing agent that produces a full novel and packages it as an EPUB; the artifact is a prompt chain (non-coding domain)
- Some prompts use the legacy Anthropic "Human:/Assistant:" completion format (Claude-2 era), which is version-sensitive
- MIT license permits full quotation and modification
