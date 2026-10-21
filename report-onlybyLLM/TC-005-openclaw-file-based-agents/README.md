# TC-005 评测结果阅读指南

本目录比较三种方式对 `test-cases/agent-suite/TC-005-openclaw-file-based-agents.md` 的评测结果：

1. **DeepSeek-FLASH 直接模型评测**
2. **deeplogic-cli L2 评测**
3. **sanityops-inspect-lite 评测**

建议先阅读三方法对比结论，再按需查看各方法的完整报告和原始证据。

---

## 一、先看什么

### 只关心最终结论

阅读：

1. [`comparison-all-methods.md`](./comparison-all-methods.md)
   - 第一节：结论摘要
   - 第三节：量化结果对比
   - 第四节：共同确认的问题
   - 第十一节：最终判断

### 关心具体缺陷

按以下顺序阅读：

1. [`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md) — 直接模型评测
2. [`deeplogic-cli.md`](./deeplogic-cli.md) — deeplogic-cli 中文摘要
3. [`sanityops-inspect-lite.md`](./sanityops-inspect-lite.md) — sanityops-inspect-lite 报告

### 关心风险审计

重点阅读：

1. [`sanityops-inspect-lite.md`](./sanityops-inspect-lite.md) 第 7 节：Stage E — Risk Explicit Audit

### 关心评测方法与复现

继续阅读：

1. [`comparison-all-methods.md`](./comparison-all-methods.md) 第二、八节
2. [`deeplogic-cli.console.log`](./deeplogic-cli.console.log)
3. [`.deeplogic/inspect_config.yaml`](./.deeplogic/inspect_config.yaml)

---

## 二、推荐阅读顺序

| 顺序 | 文件 | 作用 | 建议阅读方式 |
|---:|---|---|---|
| 1 | [`comparison-all-methods.md`](./comparison-all-methods.md) | 汇总三种方法的结果、交叉确认项、差异和最终建议 | 全篇阅读；时间有限时看第 1、3、4、11 节 |
| 2 | [`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md) | 直接模型对完整六类 Markdown 工件的评测原文 | 重点看 P0、P1、P2 表和优先修复建议 |
| 3 | [`deeplogic-cli.md`](./deeplogic-cli.md) | deeplogic-cli 结果的结构化中文摘要 | 用于快速了解规则 ID、得分、门禁和覆盖边界 |
| 4 | [`sanityops-inspect-lite.md`](./sanityops-inspect-lite.md) | sanityops-inspect-lite 完整报告 | 重点看 Stage A/B/E 发现和 Gate-0 状态 |
| 5 | [`deeplogic-cli.inspect-raw.md`](./deeplogic-cli.inspect-raw.md) | deeplogic-cli 自动生成的完整原始报告副本 | 需要核对原文、规则位置和修复建议时阅读 |
| 6 | [`deeplogic-cli.console.log`](./deeplogic-cli.console.log) | CLI 实际执行记录 | 排查执行过程或验证统计来源时阅读 |

---

## 三、文件关系

```text
被测文件
test-cases/agent-suite/TC-005-openclaw-file-based-agents.md
        │
        ├── 直接模型评测
        │      └── DeepSeek-FLASH.md
        │
        ├── deeplogic-cli L2
        │      ├── deeplogic-cli.console.log
        │      ├── .deeplogic/inspect_config.yaml
        │      └── .deeplogic/results/inspect-20261020-182035.md
        │               │
        │               └── deeplogic-cli.inspect-raw.md（完整报告副本）
        │                        │
        │                        └── deeplogic-cli.md（中文摘要）
        │
        └── sanityops-inspect-lite
               └── sanityops-inspect-lite.md

三种结果
   └── comparison-all-methods.md（三方法对比与综合判断）
```

---

## 四、当前结论速览

| 指标 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|---|---:|---:|---|
| P0 | 4 | 10 | 10 |
| P1 | 12 | 7 | 12 |
| P2 | 10 | 1 | 2 |
| 主检查缺陷合计 | **26** | **18** | **24** |
| 独立 QC 缺陷 | 无 | **2 项 P1** | **1 项 P1** |
| EX 风险项 | 无 | 无 | **9 项** |
| 分数 | 2.1/5，约 42/100 | 52.63/100 | 未计算（Gate-0 未通过） |
| 门禁 | 定性结论 | FAIL | Gate-0 Not passed |
| 权限检查 | 有风险结论 | GATE0_BLOCKED | Gate-0 未通过，未执行 |
| 风险审计 | 无 | 无 | **有（EX 分类）** |

三种方式均认为：

> TC-005 的"文件驱动 Agent"设计方向清晰，但当前在路由闭环、工具与 Skill 契约、安全边界、用户与记忆隔离、输出与验收标准方面存在重大缺口，不能直接作为可靠的生产级 Agent 套件。

---

## 五、阅读时必须注意的口径

### 1. 三个分数不能直接比较

- `2.1/5` 是 DeepSeek-FLASH 按套件六维评分表给出的综合成熟度评分
- `52.63/100` 是 deeplogic-cli 按 QDP 规则计算出的 Prompt 检查得分
- sanityops-inspect-lite 在 Gate-0 未通过时不输出分数

### 2. 缺陷总数不能直接相加

三份报告存在大量重叠主题。把 `26 + 18 + 24` 直接相加会重复计算，不能作为唯一缺陷总数。

### 3. deeplogic-cli 只检查了一个 Prompt

本次 CLI 配置为：1 个 Prompt、0 个 Tool、0 个 Skill

### 4. sanityops-inspect-lite 进行了保真度分类

本次被判定为 `summary` 保真度，因此仅运行**矛盾类检查**，跳过**缺失类检查**。

### 5. Gate-0 是结构前提条件

sanityops-inspect-lite 的 Gate-0 条件包括：
- G0-3：责任边界语句可定位
- G0-4：Tool Schema 的 name/description/参数描述完整

本次 G0-3、G0-4 均未满足，因此 Permission 阶段未执行。

### 6. Risk Explicit 是静态风险审计

sanityops-inspect-lite 的 EX 分类是**静态文本风险**，不等同于已确认的运行时漏洞。Risk Implicit（动态可利用性）未运行。

---

## 六、建议的使用方式

| 目标 | 建议优先阅读或采用 |
|---|---|
| 快速了解总体风险 | 三方法对比报告第 1、3、4、11 节 |
| 制定修复清单 | 三个报告的 P0/P1/P2 表 + EX 风险项 |
| 做 CI 门禁 | deeplogic-cli 或 sanityops-inspect-lite |
| 审查完整多 Agent 套件 | DeepSeek-FLASH，再人工复核严重级别 |
| 了解静态风险 | sanityops-inspect-lite 的 Stage E 报告 |
| 核对机器输出 | 原始报告文件与控制台记录 |

**综合建议：** 先用 sanityops-inspect-lite 或 deeplogic-cli 建立可重复的基线门禁，再由模型进行完整套件语义复核，最后人工合并去重并统一严重级别。

---

## 七、三方法特性对比

| 特性 | DeepSeek-FLASH | deeplogic-cli | sanityops-inspect-lite |
|---|---|---|---|
| 评测方法 | 自由评审 | 固定规则集 | 固定规则集 |
| 跨工件检查 | 有（人工式） | 有限 | **完整（29 项）** |
| 风险审计 | 无 | 无 | **有（EX 分类）** |
| Gate-0 门禁 | 无 | 有 | **有（G0-3/G0-4）** |
| 保真度分类 | 无 | 无 | **有** |
| 零安装执行 | 是 | 否（需 CLI） | **是** |
| 适合 CI | 否 | **是** | **是** |
| 套件语义覆盖 | **最强** | 中等 | 强 |