# TC-111+213+140：deeplogic-cli vs sanityops-inspect-lite 对比报告

- **对比日期**：2026-10-21
- **测试用例**：
  - TC-111: SalesGPT System Prompt（系统提示词）
  - TC-213: Firecrawl MCP Tool Schema（工具模式）
  - TC-140: CSV Data Summarizer Skill（技能定义）

---

## 一、总体结论摘要

| 测试用例 | deeplogic-cli 门禁 | sanityops-inspect-lite Gate | 主要差异 |
|----------|-------------------|----------------------------|----------|
| TC-111 | FAIL (B级, 89.22/100) | Gate-0 Not passed | 一致：都发现直接冲突 |
| TC-213 | **PASS (A级, 100/100)** | Gate-0 Not passed | **分歧**：CLI 零缺陷，lite 发现 P1/P2 |
| TC-140 | FAIL (D级, 20.55/100) | Gate-0 Not passed | 一致：都发现严重边界问题 |

### 核心差异

1. **TC-213**：deeplogic-cli 报告零缺陷并给出满分，sanityops-inspect-lite 发现 5 项缺陷（P1: 2, P2: 3）
2. **TC-111**：两者发现的缺陷数量接近，严重级别判断一致
3. **TC-140**：两者都发现严重问题，但 sanityops-inspect-lite 额外进行了 Risk Explicit 审计

---

## 二、TC-111: SalesGPT System Prompt 对比

### 量化结果

| 指标 | deeplogic-cli | sanityops-inspect-lite |
|------|---------------:|------------------------|
| P0 | 1 | 2 |
| P1 | 2 | 8 |
| P2 | 0 | 3 |
| **总缺陷** | **3** | **13** |
| 独立 QC | 2 项 P1 | 2 项 P1 |
| 分数 | 89.22/100 (B级) | 未计算 |
| 门禁 | FAIL | Gate-0 Not passed |
| 风险审计 | 无 | 4 项 EX |

### 共同发现

| 问题 | deeplogic-cli | sanityops-inspect-lite | 一致性 |
|------|---------------|------------------------|--------|
| 首轮问候与介绍阶段矛盾 | QDP-1.1.1 P0 | QD-P-1.1.1 P0 | **一致** |
| "short length" 模糊 | QDP-1.3.2 P1 | QD-P-1.3.2 P1 | **一致** |
| `<END_OF_CALL>` 格式模糊 | QDP-2.3.1 P1 | QD-P-2.3.1 P1 | **一致** |
| 代码块缺少语言标识 | QC-0.2 P1 (×2) | QC-0.2 P1 (×2) | **一致** |

### sanityops-inspect-lite 独有发现

1. **QD-P-2.5.2 P0**：欺骗指令 —— "say you got it from public records" 缺乏同意披露
2. **QD-P-2.6.1 P1**：运行时异常未完全覆盖
3. **QD-P-2.6.2 P2**：缺少降级策略
4. **EX 发现**：
   - NL-A-4：条件性欺骗指令（Explicit·P1·conditional）
   - NL-B-10：跨对象条件-行为链

### 严重级别差异分析

| 问题 | deeplogic-cli | sanityops-inspect-lite | 差异原因 |
|------|---------------|------------------------|----------|
| 欺骗指令 | 未检出 | QD-P-2.5.2 P0 | CLI 未将其作为安全边界问题检出 |

---

## 三、TC-213: Firecrawl MCP Tool Schema 对比

### 量化结果

| 指标 | deeplogic-cli | sanityops-inspect-lite |
|------|---------------:|------------------------|
| P0 | **0** | **0** |
| P1 | **0** | **2** |
| P2 | **0** | **3** |
| **总缺陷** | **0** | **5** |
| 分数 | **100.0/100 (A级)** | 未计算 |
| 门禁 | **PASS** | Gate-0 Not passed |
| 风险审计 | 无 | 3 项 EX |

### 关键分歧

**deeplogic-cli 判定**：
- 零缺陷，完美评分
- 工具描述清晰，区分了兄弟工具
- JSON Schema 结构正确，约束完整
- 风险注解存在

**sanityops-inspect-lite 额外发现**：

| 缺陷 | 严重级别 | 证据 |
|------|----------|------|
| QD-T-4.1 | P1 | `schema` 参数描述不足 |
| QD-T-4.7 | P1 | 无 `outputSchema` |
| QD-T-2.5 | P1 | `maxCredits` 缺少单位/货币语义 |
| QD-T-1.4 | P2 | `schema` 对象 `additionalProperties: false` 可能拒绝有效模式 |
| QD-T-3.2 | P2 | `urls` 数组接受任意 URI，无域名白名单 |

### EX 风险发现（sanityops-inspect-lite 独有）

| EX ID | 风险表达 | 严重级别 |
|-------|----------|----------|
| NR-S-2 | `openWorldHint: true` 外部网络访问 | Explicit·P1·conditional |
| NR-S-6 | `maxCredits` 默认 2500 无明确同意 | Explicit·P1·conditional |
| NR-S-1 | `strictConstrainToURLs` 范围控制机制 | Explicit·P2·conditional |

### 分歧原因分析

1. **检查级别差异**：CLI L1 完成但 L2 超时；lite 按完整规则检查
2. **规则覆盖差异**：CLI 主要检查 QDP；lite 检查 QD-T 完整规则集
3. **适配层影响**：CLI 需要适配 MCP `inputSchema` → `input_schema`；lite 直接检查 JSON
4. **语义质量要求**：lite 对描述质量（QD-T-4.1）有更细粒度检查

---

## 四、TC-140: CSV Data Summarizer Skill 对比

### 量化结果

| 指标 | deeplogic-cli | sanityops-inspect-lite |
|------|---------------:|------------------------|
| P0 | 5 | 5 |
| P1 | 11 | 10 |
| P2 | 0 | 2 |
| **总缺陷** | **16** | **17** |
| 分数 | 20.55/100 (D级) | 未计算 |
| 门禁 | FAIL | Gate-0 Not passed |
| 风险审计 | 无 | 6 项 EX |

### 共同发现

| 问题 | deeplogic-cli | sanityops-inspect-lite | 一致性 |
|------|---------------|------------------------|--------|
| 输入边界缺失 | QDS-1.1 P0 | QD-S-1.1 P0 | **一致** |
| 执行资源边界缺失 | QDS-1.3 P0 | QD-S-1.3 P0 | **一致** |
| 无界数量声明 | QDS-2.1 P0 | QD-S-2.1 P0 | **一致** |
| 缺少 non_goals | QDS-3.4 P0 | QD-S-3.4 P0 | **一致** |
| 无失败处理策略 | QDS-4.1 P0 | QD-S-4.1 P0 | **一致** |
| 输出大小缺失 | QDS-1.2 P1 | QD-S-1.2 P1 | **一致** |
| 权限边界缺失 | QDS-1.4/5.1 P1 | QD-S-1.4/5.1 P1 | **一致** |
| 触发条件模糊 | QDS-3.2 P1 | QD-S-3.2 P1 | **一致** |
| 歧义输入无处理 | QDS-3.3 P1 | QD-S-3.3 P1 | **一致** |

### EX 风险发现（sanityops-inspect-lite 独有）

| EX ID | 风险表达 | 严重级别 |
|-------|----------|----------|
| **NL-A-7** | "DO NOT ASK THE USER" 约束移除 | **Explicit·P0·unconditional** |
| NL-A-1 | 假设用户意图 "JUST DO IT" | Explicit·P1·unconditional |
| NL-A-4 | 无条件立即执行全面分析 | Explicit·P1·unconditional |
| NL-B-2 | 渐进式覆盖：全面输出 + 所有可视化 + 无问题 | Explicit·P1·unconditional |
| NL-B-10 | 触发条件 + 自动分析 + 无问题的跨对象链 | Explicit·P1·unconditional·to-be-verified |
| NL-A-3 | 技能身份强化 | Explicit·P2·conditional |

### 严重级别差异

| 问题 | deeplogic-cli | sanityops-inspect-lite | 差异原因 |
|------|---------------|------------------------|----------|
| 环境边界 | QDS-5.3 P1 | QD-S-5.3 P1 | 一致 |
| 链式调用权限 | QDS-5.4 P1 | QD-S-5.4 P1 | 一致 |

---

## 五、方法论差异总结

| 维度 | deeplogic-cli | sanityops-inspect-lite |
|------|---------------|------------------------|
| **检查规则集** | QDP/QD-S/QD-T | QD-P/QD-S/QD-T + QD-PS/QD-PT/QD-ST/QD-CYC/QD-SS/QD-TT |
| **风险审计** | 无 | 有（EX 分类：NL-A/B/NR-O/NR-S） |
| **Gate-0 条件** | P0 阻断门禁 | G0-3（责任边界可定位）+ G0-4（Tool Schema 完整性） |
| **保真度分类** | 无 | 有（`full`/`summary` 影响检查范围） |
| **跨工件检查** | 有限 | 完整（29 项规则） |
| **输出格式** | 结构化缺陷列表 + 分数 | 状态板 + 缺陷列表 + 影响卡片 |
| **分数计算** | 有（扣分模型） | Gate-0 未通过时不计算 |

---

## 六、推荐使用场景

### deeplogic-cli 更适合

- CI/CD 流水线中的自动化门禁
- 需要分数排名的场景
- 快速回归检查

### sanityops-inspect-lite 更适合

- 需要完整框架覆盖的场景
- 需要静态风险审计的场景
- 需要详细影响分析的场景
- 零安装、模型执行的轻量级检查

### 组合使用建议

1. 先用 **sanityops-inspect-lite** 做完整检查 + 风险审计
2. 对关键工件再用 **deeplogic-cli** 做标准化门禁
3. 人工复核 P0 冲突项和 EX 风险项

---

## 七、关键发现汇总

### TC-111 共识

- 首轮问候规则与介绍阶段直接矛盾（P0）
- 输出长度约束模糊
- 终止令牌格式未整合

### TC-213 分歧

- deeplogic-cli：零缺陷，完美工具模式
- sanityops-inspect-lite：描述质量和输出模式有改进空间
- 建议：对于生产级工具，两者结果应结合评估

### TC-140 共识

- 严重缺乏边界约束（输入、输出、执行、失败）
- "不做任何问题"的设计导致操作风险
- 建议：重构以添加明确边界和失败处理

---

## 证据文件

### TC-111
- deeplogic-cli：[`TC-111-salesgpt-system-prompt.deeplogic-cli-report.md`](../TC-111-salesgpt-system-prompt.deeplogic-cli-report.md)
- sanityops-inspect-lite：[`sanityops-inspect-lite/TC-111-salesgpt-system-prompt.md`](./sanityops-inspect-lite/TC-111-salesgpt-system-prompt.md)

### TC-213
- deeplogic-cli：[`TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md`](../TC-213-firecrawl-mcp-tool-schema.deeplogic-cli-report.md)
- sanityops-inspect-lite：[`sanityops-inspect-lite/TC-213-firecrawl-mcp-tool-schema.md`](./sanityops-inspect-lite/TC-213-firecrawl-mcp-tool-schema.md)

### TC-140
- deeplogic-cli：[`TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md`](../TC-140-csv-data-summarizer-skill.deeplogic-cli-report.md)
- sanityops-inspect-lite：[`sanityops-inspect-lite/TC-140-csv-data-summarizer-skill.md`](./sanityops-inspect-lite/TC-140-csv-data-summarizer-skill.md)