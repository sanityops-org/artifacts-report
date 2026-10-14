# TC-101: kotaemon - Agent Suite Evaluation Case

## Metadata
- **Source Project**: kotaemon (Cinnamon/kotaemon)
- **Submodule**: `libs/ktem/ktem/reasoning/` (reasoning pipelines) + `libs/ktem/ktem/reasoning/simple.py` (5 QA/rewrite prompts) + `libs/ktem/ktem/reasoning/{react,rewoo}.py` (agent pipelines)
- **License**: Apache-2.0
- **Artifact Type**: Single-Agent suite (RAG document-QA agent: 5 prompt templates + ReAct/ReWOO agent pipelines + retrieval/answer orchestration)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/Cinnamon/kotaemon`
  - `https://raw.githubusercontent.com/Cinnamon/kotaemon/main/README.md`
  - `https://raw.githubusercontent.com/Cinnamon/kotaemon/main/libs/ktem/ktem/reasoning/simple.py`
  - `https://api.github.com/repos/Cinnamon/kotaemon/contents/libs/ktem/ktem/reasoning` (directory listing)
  - `https://api.github.com/repos/Cinnamon/kotaemon` (repository metadata, license = Apache-2.0)

---

## Project Overview

kotaemon is an open-source, customizable **RAG UI for chatting with your documents**. It is an end-user-facing business/knowledge application (document Q&A) that also exposes a developer-facing pipeline. It ships a multi-user Gradio web UI, hybrid retrieval, citation preview, and agent-based reasoning.

From the project README (verbatim):

> "An open-source clean & customizable RAG UI for chatting with your documents. Built with both end users and developers in mind."

> "This project serves as a functional RAG UI for both end users who want to do QA on their documents and developers who want to build their own RAG pipeline."

> "Support complex reasoning methods: Use question decomposition to answer your complex/multi-hop question. Support agent-based reasoning with `ReAct`, `ReWOO` and other agents."

> "Configurable settings UI: You can adjust most important aspects of retrieval & generation process on the UI (incl. prompts)."

---

## Logical Artifact Inventory

### 1. Prompt Templates (`libs/ktem/ktem/reasoning/simple.py`) — 5 templates (verbatim)

#### 1.1 `DEFAULT_QA_TEXT_PROMPT`

```
"Use the following pieces of context to answer the question at the end in detail with clear explanation. "
"If you don't know the answer, just say that you don't know, don't try to "
"make up an answer. Give answer in "
"{lang}.\n\n"
"{context}\n"
"Question: {question}\n"
"Helpful Answer:"
```

#### 1.2 `DEFAULT_QA_TABLE_PROMPT`

```
"Use the given context: texts, tables, and figures below to answer the question, "
"then provide answer with clear explanation."
"If you don't know the answer, just say that you don't know, "
"don't try to make up an answer. Give answer in {lang}.\n\n"
"Context:\n"
"{context}\n"
"Question: {question}\n"
"Helpful Answer:"
```

#### 1.3 `DEFAULT_QA_CHATBOT_PROMPT`

```
"Pick the most suitable chatbot scenarios to answer the question at the end, "
"output the provided answer text. If you don't know the answer, "
"just say that you don't know. Keep the answer as concise as possible. "
"Give answer in {lang}.\n\n"
"Context:\n"
"{context}\n"
"Question: {question}\n"
"Answer:"
```

#### 1.4 `DEFAULT_QA_FIGURE_PROMPT`

```
"Use the given context: texts, tables, and figures below to answer the question. "
"If you don't know the answer, just say that you don't know. "
"Give answer in {lang}.\n\n"
"Context: \n"
"{context}\n"
"Question: {question}\n"
"Answer: "
```

#### 1.5 `DEFAULT_REWRITE_PROMPT`

```
"Given the following question, rephrase and expand it "
"to help you do better answering. Maintain all information "
"in the original question. Keep the question as concise as possible. "
"Give answer in {lang}\n"
"Original question: {question}\n"
"Rephrased question: "
```

### 2. Reasoning / Agent Pipelines (`libs/ktem/ktem/reasoning/`)

Registered in `flowsettings.py` (from README, verbatim):

```python
KH_REASONINGS = [
    "ktem.reasoning.simple.FullQAPipeline",
    "ktem.reasoning.simple.FullDecomposeQAPipeline",
    "ktem.reasoning.react.ReactAgentPipeline",
    "ktem.reasoning.rewoo.RewooAgentPipeline",
]
```

- `simple.py` — `AnswerWithContextPipeline` selects the prompt per evidence mode (TEXT / TABLE / CHATBOT / FIGURE).
- `react.py` — ReAct agent pipeline.
- `rewoo.py` — ReWOO agent pipeline.
- `libs/ktem/ktem/reasoning/prompt_optimization/` — `DecomposeQuestionPipeline`, `RewriteQuestionPipeline`.

### 3. Evidence Assembly (verbatim header of `PrepareEvidencePipeline`)

```
class PrepareEvidencePipeline(BaseComponent):
    """Prepare the evidence text from the list of retrieved documents
    ...
    max_context_length: int = 32000
    """
```

Evidence modes are encoded as integers, verbatim:

```
EVIDENCE_MODE_TEXT = 0
EVIDENCE_MODE_TABLE = 1
EVIDENCE_MODE_CHATBOT = 2
EVIDENCE_MODE_FIGURE = 3
MAX_IMAGES = 10
```

---

## Evaluation Dimensions

### 1. Role & Mode Clarity
- [ ] Answer behavior is selected by evidence mode (text/table/chatbot/figure) rather than one blended prompt
- [ ] A dedicated question-rewrite prompt separates query optimization from answering
- [ ] System prompt (`system_prompt`) is an overridable field on the pipeline

### 2. Workflow Completeness
- [ ] Retrieval → evidence assembly → (optional) rewrite/decompose → answer → citation is an explicit chain
- [ ] RAG pipeline is hybrid (full-text + vector) with re-ranking
- [ ] Agentic modes (ReAct, ReWOO) selectable per deployment

### 3. Prompt Consistency
- [ ] Shared placeholders (`{context}`, `{question}`, `{lang}`) used consistently
- [ ] Common anti-hallucination clause ("If you don't know the answer, just say that you don't know")
- [ ] Multilingual output supported via the `{lang}` slot

### 4. Tool / Pipeline Modularity
- [ ] Pipelines are registered components, swappable via `flowsettings.py`
- [ ] `PrepareEvidencePipeline` isolates evidence formatting from prompting
- [ ] Multimodal QA can be toggled (`KH_REASONINGS_USE_MULTIMODAL`)

### 5. Observability
- [ ] Citation preview with relevance scores in the in-browser PDF viewer
- [ ] Warning emitted when retrieval returns low-relevance passages
- [ ] Context length is measured/logged (`len (original)` / `len (trimmed)`)

### 6. Extensibility
- [ ] Custom reasoning pipeline registrable
- [ ] Prompt templates editable from the UI
- [ ] Multiple doc-stores / vector-stores selectable (Elasticsearch, LanceDB, ChromaDB, Milvus, Qdrant)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Mode Clarity | 20% | | |
| Workflow Completeness | 20% | | |
| Prompt Consistency | 15% | | |
| Tool / Pipeline Modularity | 20% | | |
| Observability | 15% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Document QA**: upload a PDF, ask a question answerable from it, and verify the answer cites the correct page.
2. **Compound question**: ask a multi-hop question and verify `FullDecomposeQAPipeline` splits then recombines.
3. **Table question**: ask about tabular data and verify the TABLE evidence mode + `DEFAULT_QA_TABLE_PROMPT` are used.

### Unit Tests
1. **Prompt selection**: given each `evidence_mode`, assert the correct template is chosen.
2. **Answer-with-context**: assert `{context}`, `{question}`, `{lang}` are all populated.
3. **Evidence assembly**: assert tables/figures/chatbot windows are tagged with their source.

### Stress Tests
1. **Huge documents**: verify context trimming to `max_context_length` at 32k tokens.
2. **Low-relevance retrieval**: confirm the low-relevance warning fires below the 0.7 threshold.
3. **ReAct/ReWOO loops**: ensure agents terminate within their step budget.

---

## Notes

- **License**: Apache-2.0 (verified via GitHub API `license.spdx_id = "apache-2.0"`). Verbatim quotation is permitted.
- **Scope**: chatting with documents is an end-user knowledge-assistant scenario; the agents do not write or review code.
- **Caveat**: kotaemon is simultaneously a UI app and a developer framework (`import kotaemon`); the artifacts evaluated here are the end-user document-QA prompts and agent pipelines.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long pipelines are excerpted.
