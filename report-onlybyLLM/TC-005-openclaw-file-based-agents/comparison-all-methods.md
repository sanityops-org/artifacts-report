# TC-005：三种评测方法对比报告

- **对比对象 A**：[`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md)（直接由 DeepSeek 模型完成评测）
- **对比对象 B**：[`deeplogic-cli.md`](./deeplogic-cli.md)（deeplogic-cli L2 评测）
- **对比对象 C**：[`sanityops-inspect-lite.md`](./sanityops-inspect-lite.md)（sanityops-inspect-lite 评测）
- **对比日期**：2026-10-21
- **被测文件**：`test-cases/agent-suite/TC-005-openclaw-file-based-agents.md`

---

## 一、结论摘要

| 维度 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|------|----------------|---------------|------------------------|
| **定性结论** | 需重点修复 | Gate FAIL | Gate-0 Not passed |
| **P0 数量** | 4 | 10 | 10 |
| **P1 数量** | 12 | 7 | 12 |
| **P2 数量** | 10 | 1 | 2 |
| **总缺陷数** | 26 | 18 (LLM) + 2 (QC) | 24 |
| **评分** | 2.1/5 (42/100) | 52.63/100 (C级) | 未给出分数（Gate-0 未通过） |
| **风险审计** | 未独立审计 | 未独立审计 | 有（9 项 EX 发现） |
| **权限检查** | 有风险分析 | GATE0_BLOCKED | Gate-0 未通过，未执行 |

### 核心一致判断

三种评测方式均认为：

> TC-005 的"文件驱动 Agent"设计方向清晰，但当前在路由闭环、工具与 Skill 契约、安全边界、用户与记忆隔离、输出与验收标准方面存在重大缺口，不能直接作为可靠的生产级 Agent 套件。

---

## 二、评测口径对比

| 对比项 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|--------|----------------|---------------|------------------------|
| **输入理解** | 完整 Agent 套件，区分六类文件 | 1 个 Prompt 工件 | `summary` 保真度，系统提示词类 |
| **工件粒度** | 六类文件分别分析 + 跨文件关联 | 0 Tool、0 Skill、1 Prompt | 单一系统提示词工件 |
| **评测方法** | 自由评审 + 六维评估框架 | QDP 规则集 L2 + QD-PM + QC Lint | QD-P/QD-PS/QD-PT/QD-ST/QD-SS/QD-CYC/QC + EX 风险审计 |
| **规则来源** | 模型自行组织 | 固定 QD/QDP/QC 规则集 | SanityOps Framework v1.0 规则包 |
| **跨工件检查** | 有（人工式语义关联） | 缺少独立多工件组合 | 有（29 项 Cross 规则） |
| **权限检查** | 有风险分析 | GATE0_BLOCKED | Gate-0 条件未满足 |
| **风险审计** | 无独立审计 | 无独立审计 | 有（EX 分类的 9 项发现） |
| **可重复性** | 中等 | 高（固定规则） | 高（固定规则） |
| **证据形式** | 工件位置 + 影响 + 修复建议 | 规则 ID + 严重级别 + 位置 + 影响 | 规则 ID + 严重级别 + 位置 + EX 分类 |
| **门禁输出** | 定性结论 | Gate FAIL | Gate-0 Not passed |
| **执行时间** | 未记录 | 291.62 秒 | 约 15 分钟（模型执行） |

### 口径差异的影响

1. **DeepSeek-FLASH**：能识别六个示例文件，覆盖套件结构类问题最广，但严重级别判断口径不完全统一。

2. **deeplogic-cli**：将整个文档作为一个 Prompt 提交，会报告"测试文档缺少任务说明"等问题，这些是"测试容器与 Prompt 对象之间表示差异"。

3. **sanityops-inspect-lite**：
   - 首先进行 **保真度分类**（`summary`），仅运行矛盾类检查，跳过缺失类检查
   - 有独立的 **Risk Explicit (EX) 风险审计阶段**，发现 9 项风险项
   - Gate-0 条件包括责任边界可定位性和 Tool Schema 完整性，本次 G0-3/G0-4 未满足

---

## 三、量化结果对比

| 指标 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|------|---------------:|---------------:|------------------------|
| P0 | 4 | 10 | 10 |
| P1 | 12 | 7 | 12 |
| P2 | 10 | 1 | 2 |
| **主检查缺陷合计** | **26** | **18** | **24** |
| 独立 QC 缺陷 | 无 | 2 项 P1 | 1 项 P1 |
| **EX 风险项** | 无 | 无 | **9 项** |
| 分数 | 2.1/5 (约 42/100) | 52.63/100 (C级) | 未计算（Gate-0 未通过） |
| 门禁 | 定性结论 | FAIL | Gate-0 Not passed |

### 分数不可比的原因

- **DeepSeek-FLASH**：采用 TC-005 自带的六维加权表（20/15/20/20/15/10），是套件成熟度综合评分。
- **deeplogic-cli**：采用 QDP 规则扣分模型，关注已配置 Prompt 的规则命中情况。
- **sanityops-inspect-lite**：Gate-0 条件未满足时不输出分数，强调"门禁通过是评分的前提"。

---

## 四、共同确认的问题（三方法交叉验证）

以下 8 个主题在三份报告中均被指出：

| # | 共同主题 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite | 一致性判断 |
|---|----------|----------------|---------------|------------------------|------------|
| 1 | 核心文件类型数量矛盾 | P2-1：声称 4 类，实际 6 类 | QDP-1.1.1：直接冲突 P0 | QD-P-1.1.1：P0 | **问题确认一致**；CLI/lite 严重级别更高 |
| 2 | 多 Agent 路由不闭合 | P0-1：路由目标未注册 | QDP-1.4.2：未注册 Agent P2 | QD-P-1.2.1：P0 | **问题确认一致** |
| 3 | Skill 与 Tool 调用契约不足 | P1-7/8：参数、返回值、权限缺失 | QDP-1.4.3/QDP-2.4.x：P0/P1 | QD-P-1.4.3：P0 | **问题确认一致** |
| 4 | 外部动作缺少安全治理 | P0-2：Shell 仅靠自然语言标只读 | QDP-2.5.2：高风险能力 P0 | QD-P-2.5.2：P0 + EX 发现 | **高度一致** |
| 5 | 用户数据与长期记忆风险 | P0-3/P1-10/11：隔离不足 | QDP-2.3.4：PII 过滤 P0 | QD-P-2.5.3：P0 | **高度一致** |
| 6 | 输出与验收契约不足 | P2-7/P2-10 | QDP-1.3.3/2.3.1/2.3.2：P0 | QD-P-2.4.1：P0 | **问题确认一致** |
| 7 | Markdown/代码块结构问题 | P2-3：嵌套代码围栏错误 | QC-0.2：行 140/258 P1 | QC-0.2：P1 | **部分一致** |
| 8 | 调用频率与运行治理不足 | P1-9：缺少幂等、去重、上限 | QDP-2.5.5：频率限制 P1 | QD-PS-1.7：前置条件缺失 P1 | **部分一致** |

---

## 五、各方法独有发现

### 5.1 DeepSeek-FLASH 独有或明显更强

1. **渠道路由 YAML 解析问题**：`#support`、`#sales` 会被 YAML 当作注释
2. **渠道声明与路由表矛盾**：sales-assistant 声明 WhatsApp/Email，却出现在 Telegram/Slack 路由中
3. **语言策略冲突**：SOUL 强制英文，USER 标明 Mandarin 母语，无优先级
4. **Handoff 契约不完整**：缺少上下文传递、接收确认、拒绝、超时规则
5. **长期记忆可被污染**：缺少来源证明、写入权限、过期机制
6. **多 Agent 隔离没有可审计配置**
7. **时间语义不明确**：`yesterday 18:00` 等条件缺少时区定义
8. **可观测性与测试可执行性不足**

### 5.2 deeplogic-cli 独有或明显更强

1. **任务边界缺失**：QDP 判为 P0
2. **输入来源与输入格式缺失**：P0
3. **输出格式与输出 Schema 不完整**：P0
4. **对话/任务终止条件缺失**
5. **负例覆盖不足**
6. **边界条件示例不足**
7. **评测标准含不可操作措辞**
8. **代码块语言标识缺失的精确位置**：行 140 和 258
9. **统一缺陷结构**：适合作为工程工单或 CI 输出

### 5.3 sanityops-inspect-lite 独有或明显更强

1. **保真度分类前置**：识别 `summary` 保真度，区分矛盾类检查与缺失类检查
2. **独立 Risk Explicit (EX) 风险审计**：
   - NL-B-2：渐进式约束放松组合导致安全边界消除（**Explicit·P0**）
   - NR-S-6：HEARTBEAT 中自动邮件发送循环无同意机制（**Explicit·P0**）
   - NL-A-7：Shell "只读" 约束仅靠注释
   - NL-B-10：跨对象条件-行为链（SOUL + HEARTBEAT）
3. **Gate-0 门禁结构**：明确 G0-3（责任边界可定位性）和 G0-4（Tool Schema 完整性）条件
4. **Cross 规则完整性**：29 项跨工件检查（QD-PS/QD-PT/QD-ST/QD-CYC/QD-SS/QD-TT）
5. **影响展望 (Impact Outlook)**：AS-* 攻击面和 FM-* 失败模式候选关联
6. **自我验证 (Stage G)**：ID 回溯、措辞红线、输出契约验证

---

## 六、Risk Explicit 发现详情（sanityops-inspect-lite 独有）

| EX ID | 风险表达 | 影响 | 严重级别 | 触发条件 |
|-------|----------|------|----------|----------|
| NL-B-2 | 多个约束放松语句组合消除安全边界 | D1, D2, D3 | **Explicit·P0·unconditional** |
| NR-S-6 | HEARTBEAT 自动邮件循环无同意 | D1 | **Explicit·P0·unconditional** |
| NL-A-7 | Shell "只读" 仅靠注释表达 | D3 | Explicit·P1·unconditional |
| NL-A-4 | 条件触发外部服务调用 | D1, D3 | Explicit·P1·conditional |
| NL-B-10 | 跨对象条件-行为链 | D1 | Explicit·P1·unconditional·to-be-verified |
| NR-S-2 | 隐含的外部调用允许 | D1, D3 | Explicit·P1·conditional |
| NR-S-9 | HEARTBEAT 中的数据外泄模式 | D1 | Explicit·P1·conditional |
| NL-A-1 | 账单问题立即升级指令 | D3 | Explicit·P2·conditional |
| NL-A-3 | Skills 范围未定义 | D3 | Explicit·P2·conditional |

---

## 七、严重级别冲突与人工裁决建议

| 问题 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite | 差异原因 | 建议裁决 |
|------|----------------|---------------|------------------------|----------|----------|
| 路由目标未注册 | P0 | P2 | P0 | CLI 按单 Prompt "不可达条件" 判断 | **P0**：完整套件口径下路由缺失应高优先级 |
| 核心文件类型矛盾 | P2 | P0 | P0 | 直接模型视为范围说明问题 | **P1**：会误导但不等于整个系统不可用 |
| HEARTBEAT 依赖未声明 | P1 | P0 | P0 | 涉及核心外联流程 | **P0**：定时任务属于主流程则按 P0 |
| 输出与验收契约不足 | P2 | P0 | P0 | CLI/lite 对 Prompt 输出契约更严格 | **P1**：若直接注入模型则 P0 合理 |
| Shell 安全边界 | P0 | P0 | P0 + EX·P1 | 三方法一致 | **P0** |

---

## 八、按 TC-005 评测维度对比

| 评测维度 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|----------|----------------|---------------|------------------------|
| 角色/责任划分 | **强** | 中 | 强 |
| 工作流/生命周期 | **强** | 中 | 强 |
| 工件一致性 | **强** | 弱-中 | **强**（Cross 规则完整） |
| 工具/工件模块化 | **强** | 中 | 强 |
| 审计/可观测性 | **强** | 弱 | 中 |
| 可扩展性 | 中 | 弱 | 中 |
| 输入/输出契约 | 中-强 | **强** | 强 |
| 固定规则与门禁 | 弱 | **强** | **强** |
| 可重复性与工程集成 | 中 | **强** | **强** |
| **风险审计** | 无 | 无 | **有（EX 分类）** |
| **保真度分类** | 无 | 无 | **有** |
| **Gate-0 结构门禁** | 无 | 有 | **有（G0-3/G0-4 条件）** |

---

## 九、推荐使用场景

### 适合 DeepSeek-FLASH

- 首次审查完整 Agent 套件
- 需要理解角色边界、路由、交接、记忆和多文件一致性
- 需要发现"规则未显式写出，但跨文件组合后会出错"的问题
- 需要面向架构和产品风险的综合判断

### 适合 deeplogic-cli

- 在 CI 中设置稳定质量门禁
- 对 Prompt 的输入、输出、安全、终止、示例和格式做固定规则检查
- 需要统一缺陷 ID、位置、严重级别和修复建议
- 需要跨版本回归比较

### 适合 sanityops-inspect-lite

- 需要完整框架覆盖（QD-P/QD-S/QD-T/QD-PS/QD-PT/QD-ST/QD-CYC/QD-SS/QD-TT/QC/EX）
- 需要独立的风险审计（Risk Explicit EX 分类）
- 需要 Gate-0 结构门禁（责任边界、Tool Schema 完整性）
- 需要影响展望（攻击面、失败模式候选关联）
- 零安装、模型执行的轻量级检查

---

## 十、推荐组合流程

1. **先用 sanityops-inspect-lite 做快速基线门禁**：
   - 保真度分类确定检查范围
   - Gate-0 验证结构前提条件
   - Risk Explicit 审计发现显式风险

2. **拆分 TC-005 内部六类工件**，分别注册为 Prompt/Skill/Tool 后：
   - 重新运行 sanityops-inspect-lite 以启用完整跨工件检查
   - 或运行 deeplogic-cli 以启用 QDP 规则门禁

3. **用 DeepSeek-FLASH 或其他直接模型做完整套件复核**：
   - 重点检查路由、命名、渠道、交接、记忆、权限和生命周期

4. **统一严重级别口径后做人工裁决**：
   - 重点复核 P0 冲突项

5. **合并去重后形成唯一修复清单**

---

## 十一、最终判断

### 一致结论

三种评测方式都支持以下判断：

> TC-005 具有清晰的"文件驱动 Agent"设计方向，但当前配置在路由闭环、工具与 Skill 契约、安全边界、用户与记忆隔离、输出与验收标准方面存在重大缺口，不能直接作为可靠的生产级 Agent 套件。

### 主要差异总结

| 方法 | 优势 | 局限 |
|------|------|------|
| **DeepSeek-FLASH** | 完整套件语义覆盖最广 | 严重级别口径不统一 |
| **deeplogic-cli** | 标准化、适合 CI | 单工件粒度、缺少独立风险审计 |
| **sanityops-inspect-lite** | 框架完整、有独立风险审计、Gate-0 结构门禁 | 保真度受限时跳过缺失类检查 |

### 推荐结论

如果必须在三者中选择：

- **评价完整 TC-005 套件的语义质量**：优先采用 DeepSeek-FLASH 的完整套件视角
- **建立工程化质量门禁**：优先采用 sanityops-inspect-lite 或 deeplogic-cli
- **正式评测或发布前**：采用"lite 基线门禁 + CLI 规则检查 + 模型跨工件复核 + 人工严重级别裁决"的组合方式

---

## 证据文件

- 直接模型评测：[`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md)
- deeplogic-cli 总结：[`deeplogic-cli.md`](./deeplogic-cli.md)
- deeplogic-cli 原始报告：[`deeplogic-cli.inspect-raw.md`](./deeplogic-cli.inspect-raw.md)
- deeplogic-cli 控制台记录：[`deeplogic-cli.console.log`](./deeplogic-cli.console.log)
- sanityops-inspect-lite 报告：[`sanityops-inspect-lite.md`](./sanityops-inspect-lite.md)
- 之前对比（DeepSeek-FLASH vs deeplogic-cli）：[`comparison-deepseek-flash-vs-deeplogic-cli.md`](./comparison-deepseek-flash-vs-deeplogic-cli.md)