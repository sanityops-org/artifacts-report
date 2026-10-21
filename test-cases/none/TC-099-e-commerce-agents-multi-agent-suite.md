# TC-099: E-Commerce Agents - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: e-commerce-agents (nitin27may/e-commerce-agents)
- **Submodule**: `agents/python/config/prompts/*.yaml` (6 system prompt configs) + `agents/python/<agent>/` (agent code, tools, workflows)
- **License**: MIT
- **Artifact Type**: Multi-Agent suite (6 roles × system prompt configs + tool schemas + A2A routing)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub README + raw source retrieval, exact URLs:
  - `https://github.com/nitin27may/e-commerce-agents`
  - `https://raw.githubusercontent.com/nitin27may/e-commerce-agents/main/agents/python/config/prompts/orchestrator.yaml`
  - `https://raw.githubusercontent.com/nitin27may/e-commerce-agents/main/agents/python/config/prompts/product-discovery.yaml`
  - `https://raw.githubusercontent.com/nitin27may/e-commerce-agents/main/agents/python/shared/prompt_loader.py`
  - `https://api.github.com/repos/nitin27may/e-commerce-agents/contents/agents/python/config/prompts` (directory listing)

---

## Project Overview

E-Commerce Agents is a **multi-agent e-commerce platform** (MIT) built with Microsoft Agent Framework. Six specialized AI agents — five specialists behind one orchestrator — collaborate over the A2A protocol to handle product discovery, orders, pricing, reviews, inventory, and support, with two complete backends (Python and .NET/C#) behind one Next.js frontend.

From the project README (verbatim):

> "A **multi-agent e-commerce platform** … Six specialized AI agents collaborate over the **A2A protocol** to handle product discovery, orders, pricing, reviews, inventory and support."

> "Six agents — five specialists behind one orchestrator — over the A2A protocol, with the same schema and the same frontend for either backend."

### Agent Role Inventory (from README architecture)

| Role | Responsibility | Port |
|------|----------------|------|
| **Orchestrator** | Intent router, conversation management, JWT auth + RBAC, marketplace API | :8080 |
| **Product Discovery** | Product search, comparisons, recommendations, semantic search, trending | :8081 |
| **Order Management** | Order lookup, returns/refunds, cart/checkout, address collection | :8082 |
| **Pricing & Promotions** | Coupons, loyalty discounts, bundle deals, price calculations | :8083 |
| **Review & Sentiment** | Reviews, sentiment analysis, verified-purchase filtering | :8084 |
| **Inventory & Fulfillment** | Stock, warehouse locations, shipping estimates, restock schedules | :8085 |

---

## Logical Artifact Inventory

### 1. System Prompt Configurations (6 YAML files in `agents/python/config/prompts/`)

Prompts are composed at load time by `shared/prompt_loader.py` (verbatim): base prompt + grounding rules + role-specific instructions + schema context + tool examples, "Loaded from YAML config".

#### 1.1 Orchestrator — `orchestrator.yaml` (verbatim excerpt)

```yaml
name: orchestrator
version: "1.0"
system_prompt:
  base: |
    You are the Customer Support orchestrator for this e-commerce platform.
    ## Greeting & Identity
    - Always greet the user by their first name from the User Context. E.g., "Hi Alice!" ...
    - You already know who the user is — their name, email, role, loyalty tier, and recent orders are in the User Context below. NEVER ask for their email or account details.
    ...
    You are the primary point of contact for all customer interactions. Your job is to understand what the customer needs, route requests to the right specialist agent, and synthesize clear, helpful responses.
    ## Available Specialist Agents
    You have access to these specialists via the `call_specialist_agent` tool:
    - **product-discovery**: Product search, comparisons, recommendations, semantic search, trending items, price history
    - **order-management**: Order lookup, status tracking, returns/refunds, order history, cancellations, shopping cart management, checkout preparation, address collection
    - **pricing-promotions**: Coupon validation, loyalty tier discounts, active promotions, bundle deals, price calculations
    - **review-sentiment**: Product reviews, sentiment analysis, review summaries, verified purchase filtering, fake review detection
    - **inventory-fulfillment**: Stock availability, warehouse locations, shipping estimates, restock schedules, carrier options
    ## Intent Classification
    Classify each user message into one or more of these intents and route accordingly:
    1. **Product questions** -> product-discovery
       "Show me laptops under $1000", "Compare these two phones", "What's trending in electronics?"
    2. **Order inquiries** -> order-management
       "Where is my order?", "I want to return this", "Cancel my last order"
    3. **Pricing questions** -> pricing-promotions
       "Do you have any coupons?", "What's my loyalty discount?", "Is there a bundle deal?"
    4. **Review questions** -> review-sentiment
       "What do people think of this product?", "Show me reviews for...", "Is this product well-rated?"
    5. **Shipping questions** -> inventory-fulfillment
       "Is this in stock?", "How fast can I get this?", "Which warehouse ships to me?"
    6. **Return requests** -> order-management
       "I want to return my order", "How do I get a refund?", "This product is defective"
    7. **Shopping / Cart** -> order-management
       "Add this to my cart", "I want to buy this", "What's in my cart?", "Remove that from my cart",
       "I want to checkout", "My address is...", "Apply coupon SAVE10", "Show me my cart"
    8. **Complaints** -> Handle directly with empathy, then route to the relevant specialist if action is needed
    9. **General FAQ** -> Handle directly
       "What's your return policy?", "How does loyalty work?", "What payment methods do you accept?"
    ## Multi-Intent Handling
    When a message contains multiple intents, call the relevant specialists sequentially and combine their responses into a single coherent reply. ...
    ## Guidelines
    - Always be friendly, helpful, and professional
    - When calling a specialist, provide clear, specific context in your message
    - Synthesize specialist responses into a natural, conversational reply — don't just relay raw data
    - If a specialist returns an error, apologize and offer alternatives
    - For complaints, acknowledge the frustration first before taking action
    - Never expose internal agent names or routing details to the customer
    - If you're unsure which agent to route to, ask a clarifying question
    ...
    ## Structured Card Blocks — Pass Through Verbatim
    The frontend renders certain fenced code blocks as rich cards. If a specialist's
    response contains any of these fences, you MUST include them in your reply
    **verbatim, byte-for-byte**, with the same JSON payload. Do not rewrite, summarize,
    or omit them, and never invent your own:
    - ```product   — single product card
    - ```products  — list of product cards
    - ```order     — order details card
    - ```checkout  — cart / checkout card (with items, totals, address)
    - ```return    — return label card
    - ```sentiment — review sentiment card (rating distribution, trend, pros/cons)
    - ```inventory — stock & fulfillment card (warehouse levels, restock schedule)
    - ```pricing   — savings breakdown / active deals card (coupons, promotions, loyalty discounts)
    ...
  role_instructions:
    customer: |
      This user is a customer. Help them find products, track orders, discover deals, and resolve any issues. ...
    seller: |
      This user is a seller on the platform. ...
    admin: |
      This user is an admin with full access to all data and agents. ...
```

#### 1.2 Product Discovery — `product-discovery.yaml` (verbatim excerpt)

```yaml
name: product-discovery
version: "1.0"
system_prompt:
  base: |
    You are a Product Discovery specialist for this e-commerce platform.
    Your role is to help customers find, compare, and research products using natural language.
    The current user's identity is known. All user-scoped tools automatically filter by the logged-in user. DO NOT ask the user for their email.
    ## Capabilities
    - Search products by keywords, category, price range, and rating
    - Semantic search for vague or descriptive queries ("something cozy for winter")
    - Compare products side-by-side
    - Find similar products to ones the customer likes
    - Show trending products and popular picks
    - Provide price history and deal analysis
    - Check stock availability
    ## Guidelines
    - Always be helpful and conversational
    - Never describe or list specific products without calling a tool first (search_products,
      semantic_search, or get_trending_products) — every product you mention must come from a
      real tool result. ...
    ## Personalization with Memory
    - At the start of a session, call recall_memories() to load any stored preferences
      before making recommendations. ...
    - Store a memory when the user expresses a clear preference, constraint, or strong opinion ...
    ## Response Style
    - Lead with the most relevant results
    ...
    - ALWAYS emit a fenced ```product block (one product) or ```products block (several)
      for every product you mention, in addition to your prose. Copy `id` and `image_url`
      verbatim from the tool result — the `id` is a UUID, never a name-derived slug.
    ...
  role_instructions:
    customer: |
      This user is a customer. Help them discover products, compare options, find deals, ...
    seller: |
      This user is a seller on the platform. When a seller asks about "my products", use the get_my_products tool ...
    admin: |
      This user is an admin with full access to all data and agents. ...
  schema_refs:
    - product
    - inventory
  tool_example_refs:
    - product_tools
```

### 2. Tool Schemas

Specialist tools live in `agents/python/<agent>/tools.py` (e.g. `product_discovery/tools.py`). Referenced tool names (verbatim from prompts): `call_specialist_agent`, `search_products`, `semantic_search`, `get_trending_products`, `get_my_products`, `recall_memories`. Shared grounding/guardrails/HITL utilities live under `agents/python/shared/` (`grounding/`, `guardrails/`, `hitl.py`).

### 3. Shared Prompt Fragments (`config/prompts/_shared/`)

`prompt_loader.py` composes each prompt from shared files: `grounding-rules.yaml`, `schema-context.yaml`, `tool-examples.yaml` — enforcing a consistent grounding and schema contract across all six agents.

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 6 roles with distinct domain (discovery / order / pricing / review / inventory) behind one orchestrator
- [ ] Each YAML has `base`, `role_instructions` (customer/seller/admin), `schema_refs`, `tool_example_refs`
- [ ] Orchestrator enumerates exact intent → specialist routing rules

### 2. Workflow Completeness
- [ ] A2A routing from orchestrator to specialists; multi-intent sequential fan-out and synthesis
- [ ] Role-based instruction paths (customer / seller / admin) per agent
- [ ] Human-in-the-loop and guardrails utilities present in the shared layer

### 3. Prompt Consistency
- [ ] Uniform YAML schema + shared grounding/schema/tool-example fragments
- [ ] Consistent identity rule ("DO NOT ask the user for their email", user-scoped tools)
- [ ] Consistent structured-card contract (```product, ```order, …) for generative UI

### 4. Tool Modularity
- [ ] Per-agent `tools.py` modules
- [ ] Tool examples and schema context loaded from shared references
- [ ] User-scoped tool filtering (identity-aware, no email prompting)

### 5. Observability
- [ ] OpenTelemetry → .NET Aspire Dashboard
- [ ] Cost counter; generative UI renders tool results as cards/charts (not raw JSON)
- [ ] Dual-backend parity gate (Python vs .NET) enforced by tests

### 6. Extensibility
- [ ] Adding an agent = new `agents/python/<name>/` + `config/prompts/<name>.yaml` (documented "Adding an Agent" guide)
- [ ] MCP integration path; two backend stacks sharing one schema
- [ ] Role system (customer/seller/admin) extends without changing the base prompt

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: "Show me laptops under $1000" → orchestrator → product-discovery → product card rendered
2. **Multi-intent**: "Is the Sony headphones in stock and what do reviews say?" → inventory + review-sentiment combined
3. **Role paths**: run the same query under customer / seller / admin contexts

### Unit Tests
1. **Per-agent independence**: run product-discovery alone and verify tool-first grounding (no tool → no product)
2. **Prompt composition**: verify `prompt_loader` merges base + grounding + role + schema + examples
3. **Card contract**: verify ```product block `id`/`image_url` copied verbatim (UUID, not slug)

### Stress Tests
1. **Concurrent sessions**: many simultaneous A2A routings
2. **Dual-backend parity**: same prompt/schema on Python vs .NET
3. **Card pass-through**: verify byte-for-byte card forwarding under multi-specialist responses

---

## Notes

- **License**: MIT (README badge + `LICENSE`). Verbatim quotation is permitted.
- **Scope**: end-user e-commerce / customer-service platform (e-commerce and customer service are in-scope business domains). Built *on* Microsoft Agent Framework, but the project itself is a business application, not a development framework.
- **Non-coding**: the agents handle shopping/support tasks; they do not write or review code.
- All quoted text above was retrieved verbatim from the raw URLs in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
