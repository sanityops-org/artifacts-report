# TC-005 评测结果阅读指南

本目录比较两种方式对 `test-cases/agent-suite/TC-005-openclaw-file-based-agents.md` 的评测结果：

1. **DeepSeek-FLASH 直接模型评测**
2. **deeplogic-cli L2 评测**

建议先阅读对比结论，再按需查看两个方法的完整报告和原始证据。

---

## 一、先看什么

### 只关心最终结论

阅读：

1. [`comparison-deepseek-flash-vs-deeplogic-cli.md`](./comparison-deepseek-flash-vs-deeplogic-cli.md)
   - 第一节：结论摘要
   - 第三节：量化结果对比
   - 第四节：共同确认的问题
   - 第十节：最终判断

### 关心具体缺陷

按以下顺序阅读：

1. [`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md)
2. [`deeplogic-cli.md`](./deeplogic-cli.md)
3. [`deeplogic-cli.inspect-raw.md`](./deeplogic-cli.inspect-raw.md)

### 关心评测方法与复现

继续阅读：

1. [`comparison-deepseek-flash-vs-deeplogic-cli.md`](./comparison-deepseek-flash-vs-deeplogic-cli.md) 第二节和第七节
2. [`deeplogic-cli.console.log`](./deeplogic-cli.console.log)
3. [`.deeplogic/inspect_config.yaml`](./.deeplogic/inspect_config.yaml)
4. [`.deeplogic/results/inspect-20261020-182035.md`](./.deeplogic/results/inspect-20261020-182035.md)

---

## 二、推荐阅读顺序

| 顺序 | 文件 | 作用 | 建议阅读方式 |
|---:|---|---|---|
| 1 | [`comparison-deepseek-flash-vs-deeplogic-cli.md`](./comparison-deepseek-flash-vs-deeplogic-cli.md) | 汇总两种方法的结果、交叉确认项、差异和最终建议 | 全篇阅读；时间有限时看第 1、3、4、10 节 |
| 2 | [`DeepSeek-FLASH.md`](./DeepSeek-FLASH.md) | 直接模型对完整六类 Markdown 工件的评测原文 | 重点看 P0、P1、P2 表和优先修复建议 |
| 3 | [`deeplogic-cli.md`](./deeplogic-cli.md) | deeplogic-cli 结果的结构化中文摘要 | 用于快速了解规则 ID、得分、门禁和覆盖边界 |
| 4 | [`deeplogic-cli.inspect-raw.md`](./deeplogic-cli.inspect-raw.md) | deeplogic-cli 自动生成的完整原始报告副本 | 需要核对原文、规则位置和修复建议时阅读 |
| 5 | [`deeplogic-cli.console.log`](./deeplogic-cli.console.log) | CLI 实际执行记录，包括分析、缺陷检查、耗时和门禁状态 | 排查执行过程或验证统计来源时阅读 |
| 6 | [`.deeplogic/inspect_config.yaml`](./.deeplogic/inspect_config.yaml) | 本次 CLI 的输入配置 | 关注“1 个 Prompt、0 Tool、0 Skill”的评测口径 |
| 7 | [`.deeplogic/results/inspect-20261020-182035.md`](./.deeplogic/results/inspect-20261020-182035.md) | CLI 原始结果文件 | 与第 4 项互相校验 |

---

## 三、文件关系

```text
被测文件
test-cases/agent-suite/TC-005-openclaw-file-based-agents.md
        │
        ├── 直接模型评测
        │      └── DeepSeek-FLASH.md
        │
        └── deeplogic-cli L2
               ├── deeplogic-cli.console.log
               ├── .deeplogic/inspect_config.yaml
               └── .deeplogic/results/inspect-20261020-182035.md
                        │
                        └── deeplogic-cli.inspect-raw.md（完整报告副本）
                                 │
                                 └── deeplogic-cli.md（中文摘要）

两种结果
   └── comparison-deepseek-flash-vs-deeplogic-cli.md（对比与综合判断）
```

---

## 四、当前结论速览

| 指标 | DeepSeek-FLASH | deeplogic-cli |
|---|---:|---:|
| P0 | 4 | 10 |
| P1 | 12 | 7 |
| P2 | 10 | 1 |
| 主检查缺陷合计 | **26** | **18** |
| 独立 QC 缺陷 | 无独立 QC 阶段 | **2 项 P1** |
| 分数 | 2.1 / 5，约 42 / 100 | 52.63 / 100 |
| 等级 | 未采用字母等级 | C |
| 门禁 | 未提供二值门禁 | FAIL |
| 权限检查 | 已形成独立风险结论 | GATE0_BLOCKED，未执行 |

两种方式均认为：

> TC-005 的“文件驱动 Agent”设计方向清晰，但当前在路由闭环、工具与 Skill 契约、安全边界、用户与记忆隔离、输出与验收标准方面存在重大缺口，不能直接作为可靠的生产级 Agent 套件。

---

## 五、阅读时必须注意的口径

### 1. 两个分数不能直接比较

- `2.1 / 5` 是直接模型按套件六维评分表给出的综合成熟度评分。
- `52.63 / 100` 是 deeplogic-cli 按 QDP 规则计算出的 Prompt 检查得分。
- 两者评分公式、输入粒度和严重级别定义不同，不能据此得出哪一方“认为质量更高”。

### 2. 两个缺陷总数不能直接相加

两个报告存在大量重叠主题。把 `26 + 18 + 2` 直接相加会重复计算，不能作为唯一缺陷总数。

### 3. deeplogic-cli 本次只检查了一个 Prompt

本次 CLI 配置为：

- 1 个 Prompt
- 0 个 Tool
- 0 个 Skill

因此 SOUL、AGENTS、USER、IDENTITY、HEARTBEAT、MEMORY 只是作为同一份 Markdown 的内容被检查，没有分别注册为独立工件。这会影响：

- 跨工件一致性检查
- 多 Agent 权限检查
- Tool/Skill 独立检查
- CROSS 结论

### 4. 权限检查被前置门禁阻断

deeplogic-cli 的 QD-PM 权限检查因上游 P0 和 Gate-0 条件失败而跳过。**跳过不等于通过**，不能据此认为权限问题不存在。

### 5. 直接模型的严重级别需要人工复核

DeepSeek-FLASH 对完整套件的覆盖更广，但 P0/P1/P2 分级是模型自行判断，前后口径不完全统一。建议把其严重级别作为风险线索，并结合对比报告第七节进行裁决。

### 6. deeplogic-cli 使用了兼容层

当前 `deeplogic-cli 1.18.0` 与已安装的 `defect-check 1.2.8` 存在接口差异。执行时使用了只处理参数兼容和关闭方式的适配层，未改变检查规则、L2 级别或被测内容。详细记录见 [`deeplogic-cli.console.log`](./deeplogic-cli.console.log)。

---

## 六、建议的使用方式

| 目标 | 建议优先阅读或采用 |
|---|---|
| 快速了解总体风险 | 对比报告第 1、3、4、10 节 |
| 制定修复清单 | DeepSeek-FLASH 的 P0/P1/P2 表 + deeplogic-cli 规则表 |
| 做 CI 门禁 | deeplogic-cli，并先拆分独立工件后重新检查 |
| 审查完整多 Agent 套件 | DeepSeek-FLASH，再人工复核严重级别 |
| 核对机器输出 | `deeplogic-cli.inspect-raw.md` 与控制台记录 |
| 复现 CLI 评测 | `.deeplogic/inspect_config.yaml` + 原始结果文件 |

**综合建议：** 先用 deeplogic-cli 建立可重复的基线门禁，再由模型进行完整套件语义复核，最后人工合并去重并统一严重级别。
