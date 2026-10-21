# TC-096: Multi-Agent Medical Assistant - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: Multi-Agent-Medical-Assistant (souvikmajumder26/Multi-Agent-Medical-Assistant)
- **Submodule**: `agents/` (rag_agent, web_search_processor_agent, image_analysis_agent, agent_decision, guardrails)
- **GitHub URL**: https://github.com/souvikmajumder26/Multi-Agent-Medical-Assistant
- **License**: Apache-2.0 (verified via GitHub API `spdx_id: "Apache-2.0"`; LICENSE file present, 11357 bytes)
- **Artifact Type**: Multi-Agent suite (RAG agent, web-search agent, image-analysis/CV agents, orchestrator/router, guardrails, human-in-the-loop)
- **Collection Date**: 2026-10-13
- **Collection Method**: Direct retrieval of raw files from `raw.githubusercontent.com` and GitHub API. Exact URLs:
  - https://github.com/souvikmajumder26/Multi-Agent-Medical-Assistant
  - https://api.github.com/repos/souvikmajumder26/Multi-Agent-Medical-Assistant (license: Apache-2.0)
  - https://raw.githubusercontent.com/souvikmajumder26/Multi-Agent-Medical-Assistant/main/README.md
  - https://raw.githubusercontent.com/souvikmajumder26/Multi-Agent-Medical-Assistant/main/agents/README.md
  - https://api.github.com/repos/souvikmajumder26/Multi-Agent-Medical-Assistant/contents/agents
  - https://api.github.com/repos/souvikmajumder26/Multi-Agent-Medical-Assistant/contents/agents/rag_agent
  - https://api.github.com/repos/souvikmajumder26/Multi-Agent-Medical-Assistant/contents/agents/web_search_processor_agent
  - https://raw.githubusercontent.com/souvikmajumder26/Multi-Agent-Medical-Assistant/main/agents/rag_agent/response_generator.py

---

## Project Overview

Multi-Agent Medical Assistant is an **end-user medical-consultation application**: an AI-powered chatbot for **medical diagnosis, research, and patient interaction**, designed for healthcare professionals, researchers, and patients. It orchestrates a LangGraph workflow of **specialized agents** — RAG-based retrieval, real-time web/PubMed search, computer-vision medical-image analysis, confidence-based routing, input/output guardrails, and human-in-the-loop validation.

This is a genuine multi-agent system: multiple distinct agent modules (`rag_agent/`, `web_search_processor_agent/`, `image_analysis_agent/`, `agent_decision.py`, `guardrails/`), each with its own subcomponents and responsibilities, coordinated through a structured graph with **agent-to-agent handoff** and **confidence-based routing**. The agents perform medical reasoning, retrieval, and image analysis — not code writing.

**Why it qualifies as an end-user business app:** medical consultation is an explicitly in-scope business scenario; the deliverable is a patient/clinician-facing web chatbot (FastAPI + HTML/JS UI); the roles are clinical/business roles, not coding roles.

### Agent Roles

| Role | Module | Responsibility | Artifact Type |
|------|------|------|-------------|
| **RAG Agent** | `agents/rag_agent/` | Retrieval-augmented generation over a medical vector store | System prompt + retrieval pipeline |
| **Web Search Processor Agent** | `agents/web_search_processor_agent/` | Real-time PubMed / Tavily medical-literature search | Tool schemas + processor |
| **Image Analysis Agent** | `agents/image_analysis_agent/` | Computer-vision diagnosis (brain tumor, chest X-ray, skin lesion) | CV model + agent |
| **Orchestrator / Router** | `agents/agent_decision.py` | Confidence-based routing and agent-to-agent handoff | Orchestration logic |
| **Guardrails** | `agents/guardrails/` | Input/output safety filtering | Guardrail config |
| **Human-in-the-Loop** | (LangGraph `NodeInterrupt` in `agent_decision.py`) | Expert validation of CV diagnoses before final output | Interaction config |

---

## Logical Artifact Inventory

### 1. RAG Agent — System Prompt (verbatim, `agents/rag_agent/response_generator.py`)

The RAG agent's response generator builds the LLM prompt from retrieved context. The core prompt (verbatim):

```python
# Build the prompt
prompt = f"""You are a medical assistant providing accurate information based on verified medical sources.
Here are the last few messages from our conversation:

{chat_history}
The user has asked the following question:
{query}
I've retrieved the following information to help answer this question:
{context}
{table_instructions}
{response_format_instructions}
Based on the provided information, please answer the user's question thoroughly but concisely.
If the information doesn't contain the answer, acknowledge the limitations of the available information.
Do not provide any source link that is not present in the context. Do not make up any source link.
Medical Assistant Response:"""
```

The response-format instructions embedded in that prompt (verbatim):

```python
response_format_instructions = """Instructions:
1. Answer the query based ONLY on the information provided in the context.
2. If the context doesn't contain relevant information to answer the query, state: "I don't have enough information to answer this question based on the provided context."
3. Do not use prior knowledge not contained in the context.
5. Be concise and accurate.
6. Provide a well-structured response with heading, sub-headings and tabular structure if required in markdown format based on retrieved knowledge. Keep the headings and sub-headings small sized.
7. Only provide sections that are meaningful to have in a chatbot reply. For example, do not explicitly mention references.
8. If values are involved, make sure to respond with perfect values present in context. Do not make up values.
9. Do not repeat the question in the answer or response."""
```

The table-handling instructions embedded in the prompt (verbatim):

```python
table_instructions = """
Some of the retrieved information is presented in table format. When using information from tables:
1. Present tabular data using proper markdown table formatting with headers, like this:
    | Column1 | Column2 | Column3 |
    |---------|---------|---------|
    | Value1  | Value2  | Value3  |
2. Re-format the table structure to make it easier to read and understand
3. If any new component is introduced during re-formatting of the table, mention it explicitly
4. Clearly interpret the tabular data in your response
5. Reference the relevant table when presenting specific data points
6. If appropriate, summarize trends or patterns shown in the tables
7. If only reference numbers are mentioned and you can fetch the corresponding values like research paper title or authors from the context, replace the reference numbers with the actual values
"""
```

### 2. RAG Agent — Pipeline Components (identified from `agents/rag_agent/`)

| Component | Purpose |
|-----------|---------|
| `doc_parser.py` | Docling-based parsing of text/tables/images from PDFs |
| `content_processor.py` | Semantic chunking, LLM image summaries |
| `query_expander.py` | LLM query expansion with medical domain terms |
| `vectorstore_qdrant.py` | Qdrant hybrid search (BM25 + dense embeddings) |
| `reranker.py` | HuggingFace cross-encoder reranking of retrieved chunks |
| `response_generator.py` | Prompt building + confidence calculation + source citation |

Confidence calculation (verbatim from `response_generator.py`):

```python
def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> float:
    """Calculate confidence score based on retrieved documents."""
    if not documents:
        return 0.0
    # Use combined score (both reranker and cosine similarity) if available, otherwise use original score
    if "combined_score" in documents[0]:
        scores = [doc.get("combined_score", 0) for doc in documents[:3]]
    elif "rerank_score" in documents[0]:
        scores = [doc.get("rerank_score", 0) for doc in documents[:3]]
    else:
        scores = [doc.get("score", 0) for doc in documents[:3]]
    # Average of top 3 document scores or fewer if less than 3
    return sum(scores) / len(scores) if scores else 0.0
```

### 3. Web Search Processor Agent (identified from `agents/web_search_processor_agent/`)

| Component | Purpose |
|-----------|---------|
| `pubmed_search.py` | PubMed literature search |
| `tavily_search.py` | Tavily general web search |
| `web_search_agent.py` | Web search agent wrapper |
| `web_search_processor.py` | Processes/aggregates web results |

### 4. Image Analysis Agent (identified from `agents/image_analysis_agent/`)

Computer-vision agents for medical imaging (per README, verbatim roles):
- **Brain Tumor**: Object Detection (PyTorch)
- **Chest X-ray**: Image Classification (PyTorch)
- **Skin Lesion**: Semantic Segmentation (PyTorch)

### 5. Orchestration & Human-in-the-Loop (verbatim from `agents/README.md`)

> In `agent_decision.py`:
> 1. Interrupt the workflow when human validation is needed
> 2. Store the interrupted state in memory
> 3. Add endpoints to expose pending validations and submit validation decisions
> 4. Resume the workflow after the human has provided feedback

> "Implemented a complete human-in-the-loop validation system using LangGraph's NodeInterrupt functionality, integrated with the backend and frontend."

### 6. Cross-cutting safety mechanisms (verbatim from `README.md`)

> "Confidence-based agent-to-agent handoff between RAG and Web Search to prevent hallucinations."

> "Input & Output Guardrails: Ensures safe, unbiased, and reliable medical responses while filtering out harmful or misleading content."

> "Expert Oversight System: Human-in-the-loop verification by medical professionals before finalizing outputs."

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] Distinct agent modules with clear separation: RAG (retrieval), Web Search (live literature), Image Analysis (CV), Orchestrator (routing), Guardrails (safety)
- [ ] Each agent's prompt/module states its scope (e.g. RAG prompt's "based ONLY on the information provided in the context")
- [ ] Human-in-the-loop role is explicitly bounded to CV diagnosis validation

### 2. Workflow Completeness
- [ ] Full intake flow: query → route (confidence) → RAG or Web Search or CV → guardrails → (optional) human validation → response
- [ ] Agent-to-agent handoff is confidence-gated to prevent hallucination
- [ ] Interrupted-state persistence and resume for human validation

### 3. Prompt Consistency
- [ ] RAG prompt enforces source-grounding ("do not make up source link", "answer based ONLY on context")
- [ ] Structured output guidance (markdown headings, tables) consistent with a clinician-facing UI
- [ ] Confidence scale (0.0–1.0 from top-3 scores) consistent across retrieval paths

### 4. Tool/Module Modularity
- [ ] RAG pipeline decomposed into single-responsibility components (parse → chunk → expand → retrieve → rerank → generate)
- [ ] Web search split by provider (PubMed vs Tavily)
- [ ] Guardrails isolated from reasoning agents

### 5. Safety & Observability
- [ ] Input/output guardrails filter harmful/misleading content
- [ ] Source citations and reference images attached to responses
- [ ] Human-in-the-loop gate on medical image diagnoses

### 6. Extensibility
- [ ] New retrieval source = new agent module + router registration
- [ ] New CV model = add to `image_analysis_agent` (brain tumor / chest X-ray / skin lesion slots are pluggable)
- [ ] Config-driven (Azure OpenAI vs OpenAI vs local models via `config.py`)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool/Module Modularity | 20% | | |
| Safety & Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: submit a text medical query → verify it routes to RAG/Web Search and returns a cited answer
2. **CV flow**: upload a chest X-ray → verify CV agent runs and the human-in-the-loop validation is triggered before final output
3. **Handoff**: submit a query where RAG confidence is low → verify confidence-based handoff to Web Search

### Unit Tests
1. **RAG prompt grounding**: feed context that lacks the answer → verify the model responds with the "not enough information" fallback
2. **Confidence calculation**: empty document list → confidence 0.0; top-3 averaged otherwise
3. **Guardrails**: inject a harmful/prompt-injection query → verify input guardrail blocks or flags it

### Boundary / Negative Tests
1. **No retrieved docs**: RAG agent must acknowledge limitation, not fabricate
2. **Human rejection**: a human reviewer rejects a CV diagnosis → verify the workflow records the rejection and does not emit a final diagnosis
3. **Provider failure**: PubMed/Tavily unavailable → verify graceful fallback and no hallucinated citations

---

## Notes

- **License**: Apache-2.0 (clear, permissive). Verified via `https://api.github.com/repos/souvikmajumder26/Multi-Agent-Medical-Assistant` (`spdx_id: "Apache-2.0"`) and the repo's LICENSE file.
- **Verbatim note**: The RAG prompt, response-format instructions, table instructions, and confidence-calculation code above are quoted verbatim from `raw.githubusercontent.com` (URLs in Metadata). Role/module descriptions are quoted verbatim from `README.md` and `agents/README.md`.
- **Uncertainty**: The full system prompts of the `web_search_processor_agent`, `image_analysis_agent`, and `agent_decision.py` orchestrator were identified by directory/module structure and README but not fully retrieved; only the RAG agent's prompt is quoted verbatim here. The role inventory above reflects the verified file/module layout.
- **Scope note**: This is an end-user medical-consultation application, not a development framework, benchmark (e.g. not a MedQA harness), or social simulation. The agents produce medical information and image analysis — not code.
