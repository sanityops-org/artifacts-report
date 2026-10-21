# TC-111+213+140 三方法评测对比总报告

## 范围

本报告对比三种独立评测方法对同一批工件的结果：

1. **直接模型评测**（综合评测报告.md）：人工维度评审 + 1-5 分制 + 加权评分
2. **deeplogic-cli 评测**：QDP/QDT/QDS 规则引擎 + QC lint + 质量门禁
3. **sanityops-inspect-lite 评测**：完整 SanityOps 框架规则包 + Risk Explicit 审计 + Gate-0 结构门禁

---

## 执行摘要

### 排名一致性

三种方法在工件质量排名上完全一致：

1. TC-213 Firecrawl Tool Schema（最佳）
2. TC-111 SalesGPT System Prompt（中等）
3. TC-140 CSV Data Summarizer Skill（最需改进）

### 关键分歧

| 工件 | 直接模型 | deeplogic-cli | sanityops-inspect-lite | 关键分歧 |
|------|----------|---------------|------------------------|----------|
| TC-111 | 59.0/100, P0:1 | 89.22/100 (B), P0:1 | Gate-0 Not passed, P0:2 | CLI 评分最高 |
| TC-213 | 64.5/100, P0:0 | **100/100 (A), P0:0** | Gate-0 Not passed, P0:0, P1:2 | **CLI 零缺陷，lite 有发现** |
| TC-140 | 58.0/100, P0:0 | 20.55/100 (D), P0:5 | Gate-0 Not passed, P0:5 | 一致：都认为问题严重 |

---

## 量化对比

### TC-111: SalesGPT System Prompt

| 指标 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|---------:|---------------:|------------------------|
| P0 | 1 | 1 | 2 |
| P1 | 7 | 2 | 8 |
| P2 | 3 | 0 | 3 |
| **总缺陷** | **11** | **3** | **13** |
| 分数 | 59.0/100 | 89.22/100 | 未计算 |
| 门禁 | 定性判断 | FAIL | Gate-0 Not passed |
| 风险审计 | 有（合规风险） | 无 | **有（4 项 EX）** |

### TC-213: Firecrawl MCP Tool Schema

| 指标 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|---------:|---------------:|------------------------|
| P0 | 0 | **0** | **0** |
| P1 | 4 | **0** | **2** |
| P2 | 3 | **0** | **3** |
| **总缺陷** | **7** | **0** | **5** |
| 分数 | 64.5/100 | **100/100** | 未计算 |
| 门禁 | 定性判断 | **PASS** | Gate-0 Not passed |
| 风险审计 | 有（模式问题） | 无 | **有（3 项 EX）** |

### TC-140: CSV Data Summarizer Skill

| 指标 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|---------:|---------------:|------------------------|
| P0 | 0 | 5 | 5 |
| P1 | 6 | 11 | 10 |
| P2 | 4 | 0 | 2 |
| **总缺陷** | **10** | **16** | **17** |
| 分数 | 58.0/100 | 20.55/100 | 未计算 |
| 门禁 | 定性判断 | FAIL | Gate-0 Not passed |
| 风险审计 | 有（边界风险） | 无 | **有（6 项 EX）** |

---

## 方法论差异

### 规则覆盖

| 规则类别 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|----------|----------|---------------|------------------------|
| 系统提示词检查 | 自定义维度 | QDP (L1-L2) | QD-P (完整 48 项) |
| 工具模式检查 | 自定义维度 | QDT (L1-L2) | QD-T (完整 31 项) |
| 技能检查 | 自定义维度 | QDS (L2) | QD-S (完整 24 项) |
| 跨工件检查 | 人工关联 | 有限 | **完整 29 项** |
| QC 检查 | 人工 | QC lint | QC-0~4 |
| 风险审计 | 人工判断 | 无 | **EX 分类（34 子类）** |
| Gate-0 门禁 | 无 | 有 | **有（G0-3/G0-4 结构条件）** |

### 特色功能

| 功能 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|----------|---------------|------------------------|
| 保真度分类 | 无 | 无 | **有（full/summary）** |
| 风险显式审计 | 人工判断 | 无 | **有（NL-A/B/NR-O/NR-S）** |
| 影响展望 | 无 | 无 | **有（AS-*/FM-* 映射）** |
| 分数排名 | 有 | 有 | Gate-0 未通过时无 |
| 可重复性 | 低 | **高** | **高** |
| 零安装执行 | 是 | 否（需 CLI） | **是** |

---

## TC-213 详细对比：为什么 CLI 给满分？

### deeplogic-cli 判断依据

1. 描述清晰：区分了兄弟工具，说明了异步合同
2. JSON Schema 结构正确：`$schema`、`properties`、`required`、`additionalProperties: false` 都存在
3. 约束声明：`prompt` 有 `minLength/maxLength`，`maxCredits` 有边界
4. 枚举约束：`effort`、`mode`、`onTermsRequired` 都有 `enum`
5. 风险注解：`readOnlyHint`、`openWorldHint`、`destructiveHint` 存在

### 直接模型发现的问题

| 问题 | 严重级别 | 验证方式 |
|------|----------|----------|
| `schema` 对象 `additionalProperties: false` 只接受空对象 | P1 | Draft-07 实例测试验证 |
| 跨字段约束未在 Schema 中表达 | P1 | 多个无效实例通过验证 |
| `threadId` pattern 接受字面量 `<uuid>` | P1 | 正则验证 |
| 无 `outputSchema` | P1 | Schema 检查 |
| 参数描述不完整 | P2 | 人工审查 |

### sanityops-inspect-lite 发现的问题

| 问题 | 规则 ID | 严重级别 |
|------|---------|----------|
| `schema` 参数描述不足 | QD-T-4.1 | P1 |
| 无 `outputSchema` | QD-T-4.7 | P1 |
| `maxCredits` 缺少单位语义 | QD-T-2.5 | P1 |
| `urls` 接受任意 URI | QD-T-3.2 | P2 |
| `schema` 对象过于严格 | QD-T-1.4 | P2 |

### EX 风险发现（sanityops-inspect-lite 独有）

| EX ID | 风险表达 | 严重级别 |
|-------|----------|----------|
| NR-S-2 | `openWorldHint: true` 外部网络访问 | Explicit·P1·conditional |
| NR-S-6 | `maxCredits` 默认 2500 无明确同意 | Explicit·P1·conditional |

### 结论

**TC-213 的 CLI 满分是假阳性**。直接模型和 sanityops-inspect-lite 都发现了实质性问题。CLI 的 L1 检查过于宽松，L2 超时后回退到 L1 导致遗漏。

---

## TC-140 详细对比：三方法一致性

### 共识发现

| 问题 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|----------|---------------|------------------------|
| 无输入大小边界 | P1 | QDS-1.1 P0 | QD-S-1.1 P0 |
| 无执行资源边界 | P1 | QDS-1.3 P0 | QD-S-1.3 P0 |
| 无界数量声明（"ALL"） | P1 | QDS-2.1 P0 | QD-S-2.1 P0 |
| 无失败处理策略 | P1 | QDS-4.1 P0 | QD-S-4.1 P0 |
| 无 non_goals | 隐含 | QDS-3.4 P0 | QD-S-3.4 P0 |
| 触发条件过宽 | P1 | QDS-3.2 P1 | QD-S-3.2 P1 |
| 无歧义输入处理 | P1 | QDS-3.3 P1 | QD-S-3.3 P1 |

### EX 风险发现（sanityops-inspect-lite 独有）

| EX ID | 风险表达 | 严重级别 |
|-------|----------|----------|
| **NL-A-7** | "DO NOT ASK THE USER" 约束移除 | **Explicit·P0·unconditional** |
| NL-A-1 | 假设用户意图 "JUST DO IT" | Explicit·P1·unconditional |
| NL-A-4 | 无条件立即执行全面分析 | Explicit·P1·unconditional |
| NL-B-2 | 渐进式覆盖：全面输出 + 所有可视化 + 无问题 | Explicit·P1·unconditional |

### 结论

三方法都认为 TC-140 存在严重的操作风险。"不做任何问题"的设计导致：
- 资源消耗无上限
- 失败路径无定义
- 用户控制被移除（EX 发现）

---

## TC-111 详细对比：合规性发现差异

### 共识发现

| 问题 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|----------|---------------|------------------------|
| 首轮问候与介绍阶段矛盾 | P1 | QDP-1.1.1 P0 | QD-P-1.1.1 P0 |
| "short length" 模糊 | P2 | QDP-1.3.2 P1 | QD-P-1.3.2 P1 |
| `<END_OF_CALL>` 格式模糊 | P2 | QDP-2.3.1 P1 | QD-P-2.3.1 P1 |

### 独有发现对比

| 问题 | 直接模型 | deeplogic-cli | sanityops-inspect-lite |
|------|----------|---------------|------------------------|
| "public records" 欺骗指令 | **P0** | 未检出 | QD-P-2.5.2 **P0** |
| 工具输入强制为简单字符串 | P1 | 未检出 | 未检出 |
| 阶段状态机缺失 | P1 | 未检出 | 未检出 |
| 运行时异常未覆盖 | P1 | 未检出 | QD-P-2.6.1 P1 |
| 提示注入隔离 | P1 | 未检出 | 未检出 |

### EX 风险发现（sanityops-inspect-lite）

| EX ID | 风险表达 | 严重级别 |
|-------|----------|----------|
| NL-A-4 | 条件性欺骗指令 | Explicit·P1·conditional |
| NL-B-10 | 跨对象条件-行为链 | Explicit·P1·conditional |

---

## 推荐使用场景

### 直接模型评测

- 需要语义深度和合规性审查
- 需要 JSON Schema 行为的具体验证
- 需要实现契约和文档完整性检查
- 需要与案例特定维度对比

### deeplogic-cli

- CI/CD 流水线中的可重复门禁
- 需要分数排名和字母等级
- 需要标准化规则应用和审计证据
- 大规模工件库的一致性基线

### sanityops-inspect-lite

- 需要完整框架覆盖
- 需要静态风险审计（Risk Explicit）
- 需要 Gate-0 结构门禁
- 需要影响展望（攻击面、失败模式）
- 零安装、模型执行的轻量级检查

---

## 推荐裁决

| 工件 | 推荐决策 | 原因 |
|------|----------|------|
| TC-111 | **FAIL / 需要修复** | 接受直接报告的合规 P0 和 CLI/lite 的冲突发现；添加可测量的长度限制和机器可读的终止令牌契约 |
| TC-213 | **FAIL / 条件性修复** | 不要接受 CLI 的 100/A 作为发布批准；解决 `schema`、跨字段、UUID 和 `outputSchema` 问题后重新评测 |
| TC-140 | **FAIL / 需要重新设计** | 接受 CLI/lite 的资源和失败边界 P0 集合，以及直接报告的执行契约、可视化和文档发现 |

---

## 证据文件

### 直接模型评测
- [综合评测报告.md](../综合评测报告.md)

### deeplogic-cli 评测
- [TC-111 CLI 报告](../TC-111-salesgpt-system-prompt.deeplogic-cli-report.md)
- [TC-213 CLI 报告](../TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md)
- [TC-140 CLI 报告](../TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md)

### sanityops-inspect-lite 评测
- [TC-111 lite 报告](./sanityops-inspect-lite/TC-111-salesgpt-system-prompt.md)
- [TC-213 lite 报告](./sanityops-inspect-lite/TC-213-firecrawl-mcp-tool-schema.md)
- [TC-140 lite 报告](./sanityops-inspect-lite/TC-140-csv-data-summarizer-skill.md)
- [CLI vs lite 对比](./sanityops-inspect-lite/comparison-deeplogic-cli-vs-sanityops-inspect-lite.md)