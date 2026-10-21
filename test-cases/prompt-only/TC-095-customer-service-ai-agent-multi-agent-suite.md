# TC-095: Customer Service AI Agent - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: customer-service-ai-agent (handsomestWei/customer-service-ai-agent)
- **Submodule**: `multi_agents/` (LangGraph-based specialized agents)
- **GitHub URL**: https://github.com/handsomestWei/customer-service-ai-agent
- **License**: Apache-2.0 (verified via GitHub API `spdx_id: "Apache-2.0"`; LICENSE file present, 11357 bytes)
- **Artifact Type**: Multi-Agent suite (1 base class + 5 specialized customer-service agents + router/classifier)
- **Collection Date**: 2026-10-13
- **Collection Method**: Direct retrieval of raw files from `raw.githubusercontent.com` and GitHub API. Exact URLs:
  - https://github.com/handsomestWei/customer-service-ai-agent
  - https://api.github.com/repos/handsomestWei/customer-service-ai-agent (license: Apache-2.0)
  - https://api.github.com/repos/handsomestWei/customer-service-ai-agent/contents/multi_agents
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/base_agent.py
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/general_agent.py
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/billing_agent.py
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/complaint_agent.py
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/product_agent.py
  - https://raw.githubusercontent.com/handsomestWei/customer-service-ai-agent/main/multi_agents/tech_agent.py

---

## Project Overview

Customer Service AI Agent is an **end-user customer-service application** built on LangGraph. A classifier/routing node dispatches each customer message to one of five **specialized agents**, each with a distinct role, expertise list, and its own simulated domain database (service hours, billing/refund policies, complaint-resolution playbooks, product catalogs, tech-support runbooks). A shared `BaseAgent` provides conversation-context injection, session management, and LLM invocation.

This is a genuine multi-agent system: five separate agent classes (`BillingAgent`, `ComplaintAgent`, `GeneralAgent`, `ProductAgent`, `TechAgent`), each with its own `name`, `role`, `expertise`, and a distinct system-prompt template. The agents are business roles (billing, complaints, general inquiry, product, tech support) — not coding roles.

**Why it qualifies as an end-user business app:** customer service is an explicitly in-scope business scenario; the agents answer end-user customer queries (not code); the deliverable is a chat/web service for customers.

### Agent Roles

| Role | Class | Responsibility | Artifact Type |
|------|------|------|-------------|
| **General Agent** (综合客服) | `GeneralAgent` | General inquiries, service info, handoff | System prompt + service DB |
| **Billing Agent** (账单专家) | `BillingAgent` | Refunds, invoices, pricing, payments | System prompt + billing DB |
| **Complaint Agent** (投诉处理专家) | `ComplaintAgent` | Complaints & suggestions handling | System prompt + complaint DB |
| **Product Agent** (产品专家) | `ProductAgent` | Product specs, price comparison, recommendations | System prompt + product DB |
| **Tech Agent** (技术支持专家) | `TechAgent` | Technical diagnosis & resolution | System prompt + tech DB |
| **Base Agent** | `BaseAgent` | Shared context/session/prompt-enhancement machinery | Base class |

---

## Logical Artifact Inventory

> The specialized agents' system prompts are authored in Chinese (the repository's native language). Verbatim original text is quoted below with an English description; this is the "content originally in another language within a test case" exception permitted by folder rules.

### 1. Base Agent (verbatim structure, `multi_agents/base_agent.py`)

```python
class BaseAgent(ABC):
    def __init__(self, name: str, role: str, expertise: List[str], session_manager: LangChainSessionManager = None):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.llm = None  # 将在运行时注入
        self.session_manager = session_manager or LangChainSessionManager()
    ...
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理客户查询的抽象方法"""
        pass
```

The base class also defines a shared context-enhancement instruction appended to every agent's prompt (verbatim):

```python
def _enhance_system_prompt_with_context(self, base_prompt: str) -> str:
    context_instruction = """
重要：请结合对话历史上下文，理解客户之前的问题和需求，提供连贯、个性化的回答。
如果这是多轮对话，请参考之前的对话内容，避免重复信息，并基于客户的新问题提供补充信息。
保持对话的连贯性和自然性，让客户感受到你理解他们的完整需求。"""
    return base_prompt + context_instruction
```

(English: "Important: please combine the conversation-history context to understand the customer's previous questions and needs, and provide a coherent, personalized answer. In multi-turn conversations, refer to prior content, avoid repetition, and supplement based on the new question. Keep the conversation coherent and natural so the customer feels their full needs are understood.")

### 2. General Agent (verbatim prompt template, `multi_agents/general_agent.py`)

Role/expertise registration (verbatim):

```python
super().__init__(
    name="综合客服",
    role="一般咨询处理",
    expertise=["信息查询", "基础服务", "问题转接"]
)
```

System-prompt template (verbatim; `{self.name}` = "综合客服", `{self.role}` = "一般咨询处理", expertise = "信息查询, 基础服务, 问题转接"):

```
你是{self.name}，专门负责{self.role}。
你的专业领域包括：{', '.join(self.expertise)}
请以友好、专业的态度处理客户的一般咨询：
1. 耐心倾听客户的问题
2. 提供准确、有用的信息
3. 如果问题超出你的专业范围，建议转接给相关专家
4. 确保客户得到满意的答复
回答要友好、专业，体现良好的服务态度。如果问题复杂或需要专业知识，请说明并建议转接给相应的专业智能体。
```

(English: "You are {name}, specializing in {role}. Your expertise includes {expertise}. Handle general inquiries in a friendly, professional manner: 1. listen patiently; 2. provide accurate, useful information; 3. if out of scope, suggest handoff to a specialist; 4. ensure satisfaction. If the problem is complex or needs specialized knowledge, explain and suggest transferring to the appropriate specialized agent.")

### 3. Billing Agent (verbatim, `multi_agents/billing_agent.py`)

```python
super().__init__(
    name="账单专家",
    role="财务和账单问题处理",
    expertise=["退款处理", "发票管理", "价格计算", "支付问题"]
)
```

System-prompt template (verbatim):

```
你是{self.name}，专门负责{self.role}。
你的专业领域包括：{', '.join(self.expertise)}
请根据客户的账单问题提供专业的解答：
1. 仔细分析客户的具体问题
2. 提供明确的处理流程和时间预期
3. 说明需要提供的相关材料
4. 如果问题复杂，建议联系专门的财务人员
回答要准确、专业，涉及金额和时间的信息要具体明确。如果问题超出你的权限范围，请说明并建议转接给相关部门。
```

(English: "You are the billing specialist, responsible for financial/billing issues. Expertise: refund handling, invoice management, price calculation, payment problems. Provide professional answers with clear process steps and time expectations; state required materials; if complex, suggest contacting dedicated finance staff; be precise about amounts and timing; if beyond your authority, explain and suggest handoff.")

### 4. Complaint Agent (verbatim, `multi_agents/complaint_agent.py`)

```python
super().__init__(
    name="投诉处理专家",
    role="客户投诉和建议处理",
    expertise=["问题记录", "解决方案", "补偿措施", "服务改进"]
)
```

System-prompt template (verbatim):

```
你是{self.name}，专门负责{self.role}。
你的专业领域包括：{', '.join(self.expertise)}
请以专业、耐心的态度处理客户投诉：
1. 认真倾听客户的问题和不满
2. 表达理解和歉意
3. 提供具体的解决方案和时间承诺
4. 如果问题复杂，说明后续处理流程
回答要真诚、专业，体现对客户的重视。如果投诉超出你的处理权限，请说明并承诺转交给相关部门处理。
```

(English: "You are the complaint-handling specialist. Expertise: problem logging, solutions, compensation, service improvement. Handle complaints professionally and patiently: listen, express understanding and apology, provide concrete solutions with time commitments, and if complex, explain follow-up. If beyond authority, explain and commit to escalation.")

### 5. Product Agent (verbatim, `multi_agents/product_agent.py`)

```python
super().__init__(
    name="产品专家",
    role="产品信息咨询和推荐",
    expertise=["产品规格", "价格比较", "功能特点", "市场分析"]
)
```

System-prompt template (verbatim):

```
你是{self.name}，专门负责{self.role}。
你的专业领域包括：{', '.join(self.expertise)}
请根据客户查询提供专业、详细的产品信息，包括：
- 产品规格和功能特点
- 价格区间和性价比分析
- 适用场景和用户群体
- 与竞品的对比优势
回答要专业、准确、有说服力。如果客户询问的产品不在你的知识范围内，请说明并建议联系销售代表获取最新信息。
```

(English: "You are the product specialist. Expertise: product specs, price comparison, features, market analysis. Provide professional, detailed product information: specs and features, price range and value analysis, use cases and target users, competitive advantages. Be persuasive. If the product is outside your knowledge, explain and suggest contacting a sales rep.")

### 6. Tech Agent (verbatim, `multi_agents/tech_agent.py`)

```python
super().__init__(
    name="技术支持专家",
    role="技术问题诊断和解决",
    expertise=["故障诊断", "系统优化", "软件配置", "硬件维修"]
)
```

System-prompt template (verbatim):

```
你是{self.name}，专门负责{self.role}。
你的专业领域包括：{', '.join(self.expertise)}
请根据客户的技术问题提供专业的解决方案：
1. 仔细分析问题的技术细节
2. 提供清晰的解决步骤
3. 说明可能的原因和预防措施
4. 如果问题复杂，建议联系专业技术人员
回答要专业、准确，技术术语要通俗易懂。如果问题超出你的专业范围，请说明并建议转接给相应的技术专家。
```

(English: "You are the tech-support specialist. Expertise: fault diagnosis, system optimization, software configuration, hardware repair. Analyze technical details, provide clear step-by-step solutions, explain likely causes and prevention; keep terminology plain. If out of scope, explain and suggest handoff.")

### 7. Shared State Contract (observed across all agents, verbatim pattern)

Every specialized agent writes the same fields back to the LangGraph state:

```python
state["response"] = response_content
state["current_agent"] = self.name
state["tools_used"].append(f"{self.name}_processing")
return state
```

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 5 specialized agents with distinct `name`/`role`/`expertise` tuples and non-overlapping domains
- [ ] Each agent's system prompt states its scope and explicit handoff behavior for out-of-scope queries
- [ ] Shared `BaseAgent` cleanly separates common machinery from role-specific logic

### 2. Workflow Completeness
- [ ] Full routing lifecycle: classify → dispatch to specialized agent → respond → record `current_agent`/`tools_used`
- [ ] Conversation-context injection supports multi-turn coherence
- [ ] Handoff/escalation language present in every prompt

### 3. Prompt Consistency
- [ ] All 5 prompts share a common template skeleton (identity → expertise → numbered guidance → tone → escalation clause)
- [ ] Identical state-write contract across agents (`response`, `current_agent`, `tools_used`)
- [ ] Shared context-enhancement instruction appended uniformly via the base class

### 4. Tool/Data Modularity
- [ ] Each agent owns a scoped domain database (service hours, billing, complaints, products, tech) — clean separation
- [ ] LLM injection and session manager are abstracted behind `BaseAgent`
- [ ] Databases are mockable/plug-replaceable (explicit "should connect to real system" TODOs)

### 5. Observability
- [ ] `tools_used` and `current_agent` recorded per turn
- [ ] `persisted_dialogue` carries cross-process conversation history
- [ ] Graceful error fallback strings on LLM failure

### 6. Extensibility
- [ ] New agent = subclass `BaseAgent` + implement `process()` + register in router
- [ ] Role/expertise are data (constructor args), not hard-coded logic

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool/Data Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: send a billing query → verify it routes to `BillingAgent` and `current_agent == "账单专家"`
2. **Handoff**: send a query outside any agent's scope → verify the agent suggests transfer rather than hallucinating an answer
3. **Multi-turn**: two-turn conversation → verify `persisted_dialogue` context is injected into the second answer

### Unit Tests
1. **Per-agent independence**: instantiate `ProductAgent` alone and verify its prompt template renders with the correct `name`/`role`/`expertise`
2. **Domain match**: verify `_match_service_info`/`_match_billing_info`/`_match_products` return the correct category for a keyword
3. **State contract**: verify every agent writes `response`, `current_agent`, `tools_used`

### Boundary / Negative Tests
1. **Out-of-scope query**: an unknown topic must not crash; agent must fall back to a handoff message
2. **Empty context**: no `persisted_dialogue` → agent answers from the query alone without error
3. **LLM failure**: simulate LLM exception → verify the graceful error string is returned and recorded

---

## Notes

- **License**: Apache-2.0 (clear, permissive). Verified via `https://api.github.com/repos/handsomestWei/customer-service-ai-agent` (`spdx_id: "Apache-2.0"`) and the repo's LICENSE file.
- **Verbatim note**: All five specialized agents' `name`/`role`/`expertise` registrations and system-prompt templates above are quoted verbatim from `raw.githubusercontent.com` (URLs in Metadata). The prompts are in Chinese (the repository's native language); English translations are provided for readability and are NOT verbatim.
- **Scope note**: This is an end-user customer-service application, not a development framework, benchmark, or simulation. The agents answer customer-service queries (not code).
- **Limitation**: The classifier/router node (in `multi_agent_customer_service.py`) was identified by name in the file tree but not fully quoted here; the routing contract (`current_agent`, `tools_used`) was verified from the agent files themselves.
