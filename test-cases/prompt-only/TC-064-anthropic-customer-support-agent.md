# TC-064: Anthropic Quickstart - Customer Support Agent

## Metadata
- **Source Project**: anthropics/anthropic-quickstarts
- **GitHub**: github.com/anthropics/anthropic-quickstarts
- **License**: MIT
- **Artifact Type**: RAG-based customer support chatbot agent (Next.js API route + category taxonomy)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub content fetch from branch `main`:
  - https://raw.githubusercontent.com/anthropics/anthropic-quickstarts/main/customer-support-agent/app/api/chat/route.ts
  - https://raw.githubusercontent.com/anthropics/anthropic-quickstarts/main/customer-support-agent/app/lib/customer_support_categories.json
- **Scope**: A single-agent customer support assistant that answers product questions from a RAG pipeline, classifies inquiries into support categories, and escalates to a human agent.

---

## Project Overview

This quickstart implements a **customer support chatbot** for Anthropic's products and services. The agent runs behind a Next.js App Router API route (`app/api/chat/route.ts`) and:

- **Retrieves context** via a RAG pipeline (`retrieveContext`) before every response.
- **Answers strictly from provided context** — it is instructed to only use retrieved information and to redirect to a human when it cannot help.
- **Classifies inquiries** into a fixed taxonomy of 8 support categories and returns matched category IDs.
- **Detects user mood** from a fixed enum (positive / neutral / negative / curious / frustrated / confused).
- **Decides to escalate** to a human agent via a structured `redirect_to_agent` object.
- **Enforces a strict JSON response contract** validated by a Zod schema (`responseSchema`), with `temperature: 0.3` and `max_tokens: 1000`.

### Key Characteristics
- **Non-coding agent**: purely a support/assistant role — no code generation.
- **Structured output contract**: every reply is a JSON object (thinking, response, mood, suggested questions, categories, redirect decision).
- **Human-in-the-loop escalation** built into the schema.
- **Category-driven internal classification** supplied by a JSON taxonomy file.

---

## Agent Prompts

### 1. System Prompt (`app/api/chat/route.ts`)

The system prompt is assembled at runtime. It interleaves RAG context and a category-classification block into a base instruction. Quoted below verbatim (template literal placeholders preserved as in source):

```text
You are acting as an Anthropic customer support assistant chatbot inside a chat window on a website. You are chatting with a human user who is asking for help about Anthropic's products and services. When responding to the user, aim to provide concise and helpful responses while maintaining a polite and professional tone.
  To help you answer the user's question, we have retrieved the following information for you. It may or may not be relevant (we are using a RAG pipeline to retrieve this information):
  ${isRagWorking ? `${retrievedContext}` : "No information found for this query."}
  Please provide responses that only use the information you have been given. If no information is available or if the information is not relevant for answering the question, you can redirect the user to a human agent for further assistance.
  ${categoriesContext}
  If the question is unrelated to Anthropic's products and services, you should redirect the user to a human agent.
  You are the first point of contact for the user and should try to resolve their issue or provide relevant information. If you are unable to help the user or if the user explicitly asks to talk to a human, you can redirect them to a human agent for further assistance.

  To display your responses correctly, you must format your entire response as a valid JSON object with the following structure:
  {
      "thinking": "Brief explanation of your reasoning for how you should address the user's query",
      "response": "Your concise response to the user",
      "user_mood": "positive|neutral|negative|curious|frustrated|confused",
      "suggested_questions": ["Question 1?", "Question 2?", "Question 3?"],
      "debug": {
        "context_used": true|false
      },
      "matched_categories": ["category_id1", "category_id2"],
      "redirect_to_agent": {
        "should_redirect": boolean,
        "reason": "Reason for redirection (optional, include only if should_redirect is true)"
      }
    }
  Here are a few examples of how your response should look like:
  Example of a response without redirection to a human agent:
  {
    "thinking": "Providing relevant information from the knowledge base",
    "response": "Here's the information you requested...",
    "user_mood": "curious",
    "suggested_questions": ["How do I update my account?", "What are the payment options?"],
    "debug": {
      "context_used": true
    },
    "matched_categories": ["account_management", "billing"],
    "redirect_to_agent": {
      "should_redirect": false
    }
  }
  Example of a response with redirection to a human agent:
  {
    "thinking": "User request requires human intervention",
    "response": "I understand this is a complex issue. Let me connect you with a human agent who can assist you better.",
    "user_mood": "frustrated",
    "suggested_questions": [],
    "debug": {
      "context_used": false
    },
    "matched_categories": ["technical_support"],
    "redirect_to_agent": {
      "should_redirect": true,
      "reason": "Complex technical issue requiring human expertise"
    }
  }
```

### 2. Category-Classification Instruction Block (injected as `${categoriesContext}`)

```text
    To help with our internal classification of inquiries, we would like you to categorize inquiries in addition to answering them. We have provided you with 8 customer support categories.
    Check if your response fits into any category and include the category IDs in your "matched_categories" array.
    The available categories are: account, billing, feature, internal, legal, other, technical, usage
    If multiple categories match, include multiple category IDs. If no categories match, return an empty array.
```

### 3. Response Schema (Zod, `responseSchema`)

```typescript
const responseSchema = z.object({
  response: z.string(),
  thinking: z.string(),
  user_mood: z.enum([
    "positive",
    "neutral",
    "negative",
    "curious",
    "frustrated",
    "confused",
  ]),
  suggested_questions: z.array(z.string()),
  debug: z.object({
    context_used: z.boolean(),
  }),
  matched_categories: z.array(z.string()).optional(),
  redirect_to_agent: z
    .object({
      should_redirect: z.boolean(),
      reason: z.string().optional(),
    })
    .optional(),
});
```

---

## Skill Definitions

### 1. Support Category Taxonomy (`app/lib/customer_support_categories.json`)

The agent's classification "skills" are defined by a keyword-driven taxonomy of 8 categories. Each category has an `id`, a human-readable `name`, and a list of `keywords`.

```json
{
  "categories": [
    {
      "id": "account",
      "name": "Account",
      "keywords": [
        "ban",
        "appeal",
        "deletion",
        "logging in",
        "phone verification",
        "roles",
        "permissions"
      ]
    },
    {
      "id": "billing",
      "name": "Billing",
      "keywords": [
        "AR",
        "billing details",
        "invoice",
        "receipt",
        "payment method",
        "pricing",
        "refund request",
        "subscription management",
        "taxes"
      ]
    },
    {
      "id": "feature",
      "name": "Feature",
      "keywords": [
        "functionality",
        "tools",
        "capabilities",
        "options",
        "modules",
        "features"
      ]
    },
    {
      "id": "internal",
      "name": "Internal",
      "keywords": [
        "auto-reply",
        "forward",
        "ignore",
        "spam",
        "other",
        "sales reroute"
      ]
    },
    {
      "id": "legal",
      "name": "Legal",
      "keywords": ["data privacy", "policy", "terms of service", "usage policy"]
    },
    {
      "id": "other",
      "name": "Other",
      "keywords": ["job inquiry", "3rd party company"]
    },
    {
      "id": "technical",
      "name": "Technical",
      "keywords": [
        "guides",
        "issue",
        "security",
        "downtime",
        "performance",
        "interface",
        "system"
      ]
    },
    {
      "id": "usage",
      "name": "Usage",
      "keywords": [
        "errors",
        "capabilities",
        "quality",
        "techniques",
        "limits",
        "availability"
      ]
    }
  ]
}
```

### 2. Category Coverage Summary

| Category ID | Name | # Keywords |
|-------------|------|-----------|
| account | Account | 7 |
| billing | Billing | 9 |
| feature | Feature | 6 |
| internal | Internal | 6 |
| legal | Legal | 4 |
| other | Other | 2 |
| technical | Technical | 7 |
| usage | Usage | 6 |

---

## Evaluation Dimensions

### 1. System Prompt Quality
- [ ] Role and scope are clearly stated (Anthropic support only)
- [ ] Instruction to answer only from provided context
- [ ] Out-of-scope requests routed to a human
- [ ] Tone guidance (concise, polite, professional)

### 2. Structured Output Contract
- [ ] JSON schema is fully specified in the prompt
- [ ] Few-shot examples cover both normal and redirection cases
- [ ] Enum for `user_mood` matches the Zod schema
- [ ] Optional vs. required fields are consistent between prompt and schema

### 3. Classification Taxonomy
- [ ] Categories have stable IDs, names, and keywords
- [ ] Multi-category matching supported
- [ ] Empty-array fallback when nothing matches
- [ ] Category list is injected dynamically (count + IDs)

### 4. Human Escalation Logic
- [ ] `redirect_to_agent.should_redirect` gate is explicit
- [ ] Escalation reasons are human-readable
- [ ] Agent is first point of contact before escalating
- [ ] Escalation triggered by out-of-scope or explicit user request

### 5. RAG Grounding
- [ ] Retrieval happens before generation
- [ ] Failure path degrades gracefully (`isRagWorking = false`)
- [ ] `debug.context_used` reflects actual context use
- [ ] RAG sources surfaced via response headers

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| System Prompt Quality | 25% | | |
| Structured Output Contract | 25% | | |
| Classification Taxonomy | 20% | | |
| Human Escalation Logic | 15% | | |
| RAG Grounding | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Positive Tests
1. Ask an in-scope product question with matching RAG context; verify answer is grounded and `debug.context_used` is `true`.
2. Submit a billing query; verify `matched_categories` includes `billing` and the reply is polite and concise.
3. Ask a question spanning account and technical topics; verify multiple category IDs are returned.

### Boundary Tests
1. Ask a question with no relevant retrieved context; verify the agent declines rather than hallucinating.
2. Provide a query matching no category; verify `matched_categories` returns an empty array.
3. Send a message at the `message_length_limit`/token boundary; verify valid JSON is still returned and parsed.

### Negative Tests
1. Ask about an unrelated third-party product; verify the agent redirects to a human (`should_redirect: true`).
2. Force an invalid JSON output; verify `sanitizeAndParseJSON` throws and the route returns the 500 fallback payload.
3. Attempt prompt injection via user message to override the system role; verify scope constraints hold.

### Contract/Integration Tests
1. Validate every response against `responseSchema` (Zod) with no parse errors.
2. Verify `x-rag-sources` and `X-Debug-Data` headers are present when applicable.
3. Confirm `temperature: 0.3`, `max_tokens: 1000` and model passthrough behave as configured.

---

## Notes

- This is a **NON-coding customer support agent**; its logical artifacts are the system prompt, the response schema, and the category taxonomy.
- The system prompt is built by string interpolation at request time; the interpolated `${retrievedContext}` and `${categoriesContext}` are provided by the RAG pipeline and the JSON taxonomy respectively.
- Quoted content is taken verbatim from the fetched `main` branch sources on 2026-10-13; the few-shot examples in the prompt reference category IDs (`account_management`, `billing`, `technical_support`) that do not all match the taxonomy IDs (`account`, `billing`, `technical`) — a real inconsistency present in the source.
- License is MIT, which permits examination and reuse.
- Useful reference for RAG-grounded support bots with structured output, mood detection, and human-in-the-loop escalation.
