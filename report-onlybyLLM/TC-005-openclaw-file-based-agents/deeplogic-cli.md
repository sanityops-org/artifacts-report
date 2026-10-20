# TC-005：OpenClaw 文件驱动多智能体套件 — deeplogic-cli 评测结果

## 执行信息

| 项目 | 值 |
|---|---|
| 评测对象 | `test-cases/agent-suite/TC-005-openclaw-file-based-agents.md` |
| 工具 | `deeplogic-cli 1.18.0` |
| 缺陷检查 SDK | `defect-check 1.2.8` |
| 模型入口 | `anthropic / test-assistant`（本地兼容接口） |
| 检查级别 | L2 |
| 评测时间 | 2026-10-20 18:20:35（Asia/Shanghai） |
| 执行耗时 | 291.62 秒 |
| 注册工件 | 1 个 Prompt、0 个 Tool、0 个 Skill |
| QDP 输入长度 | 10,685 字符 |

> **执行口径**：按单文件逻辑工件方式，将 TC-005 的完整 Markdown 作为一个 Prompt 交付 CLI；未改写测试用例，也未将内嵌的 SOUL/AGENTS/USER/IDENTITY/HEARTBEAT/MEMORY 示例拆分为独立工件。

## 总览

| 指标 | 结果 |
|---|---:|
| 总缺陷 | **18** |
| P0 | **10** |
| P1 | **7** |
| P2 | **1** |
| QDP 得分 | **52.63 / 100** |
| 等级 | **C** |
| 质量门禁 | **FAIL** |
| 权限检查 | **跳过（GATE0_BLOCKED）** |
| QC Lint | **PASS**（2 项 P1） |

**结论：** TC-005 作为展示型配置样例具有清晰的“文件即 Agent”设计，但当前文本尚不能作为可靠的生产级多智能体规范。主要问题集中在任务/输入/输出契约缺失、工具与资源未声明、安全与隐私边界不足，以及多 Agent 路由关系不闭合。

## P0 缺陷（10 项）

| 规则 | 问题 | 依据位置 |
|---|---|---|
| QDP-1.1.1 | “4 core file types”与实际展示的 6 类文件直接冲突 | Logical Artifact Inventory / Key Features |
| QDP-2.4.2 | HEARTBEAT 调用了 8 个未声明来源与访问方式的函数 | HEARTBEAT.md - Tasks |
| QDP-2.4.3 | 未定义工具调用参数格式、调用时机和结果处理方式 | SOUL.md - Skills / AGENTS.md |
| QDP-1.3.3 | 未说明输出物与任务边界，无法确定应评测、评分、生成测试还是总结 | Prompt overall |
| QDP-2.3.1 | 缺少输出格式、结构、约定和最终报告 Schema | Scoring Criteria / overall prompt |
| QDP-2.3.2 | 评分表未定义 1–5 分含义、汇总方法和最终字段 | Scoring Criteria |
| QDP-2.2.1 | 未声明渠道消息的输入来源与事件载荷格式 | AGENTS.md - Routing Rules |
| QDP-2.2.2 | 未约束输入长度、编码和字符集 | AGENTS.md - channels/bindings |
| QDP-2.3.4 | USER.md 与 MEMORY.md 含个人/客户数据，但没有隐私过滤与输出保护 | USER.md / MEMORY.md / SOUL.md |
| QDP-2.5.2 | 自动外联、Shell 等高风险能力缺少同意、确认和禁止操作边界 | HEARTBEAT.md / SOUL.md |

## P1 / P2 缺陷（8 项）

| 规则 | 级别 | 问题 |
|---|---|---|
| QDP-2.5.4 | P1 | 多组路由规则与约束同时生效，但没有优先级 |
| QDP-1.4.3 | P1 | Skill 仅有一行声明，没有参数、调用方式或结果处理 |
| QDP-2.5.1 | P1 | 会话和评测任务均缺少终止条件 |
| QDP-2.7.2 | P1 | 除语气示例外，路由、安全、工具和输出区域缺少负例 |
| QDP-2.7.3 | P1 | 缺少空输入、超长输入、未知意图、缺失配置等边界示例 |
| QDP-1.3.2 | P1 | 评测标准使用 “clear/reasonable/appropriate” 等不可操作措辞 |
| QDP-2.5.5 | P1 | 未声明工具/资源调用频率上限 |
| QDP-1.4.2 | P2 | 路由目标 `billing-agent`、`tech-support`、`sales-manager` 未在 Registry 中定义 |

## QC Lint

| 规则 | 级别 | 行号 | 问题 |
|---|---|---:|---|
| QC-0.2 | P1 | 140 | 代码块缺少显式语言标识 |
| QC-0.2 | P1 | 258 | 代码块缺少显式语言标识 |

## 门禁与覆盖说明

- 权限检查（QD-PM）被 Gate-0 阻断：上游存在未修复 P0，且责任边界与具体定位不足。
- 本次配置只有 1 个 Prompt 工件，因此未形成独立的 Prompt/Skill/Tool 跨工件组合；CROSS 的独立结论不可用。
- QC Lint 通过，不代表 LLM 缺陷检查通过；QC 只发现 2 项格式级问题。
- 为适配当前已安装 SDK 与 CLI 的接口差异，执行时使用了兼容层：忽略 SDK 不支持的 CLI 超时/权限选项，并适配同步 `close()`；未改变检查规则、检查级别或被测内容。
- 为避免测试语料自动上传，本次评测关闭了服务端上传。

## 证据文件

- 完整 CLI 原始报告：[`deeplogic-cli.inspect-raw.md`](./deeplogic-cli.inspect-raw.md)
- CLI 控制台记录：[`deeplogic-cli.console.log`](./deeplogic-cli.console.log)
- CLI 配置：[`.deeplogic/inspect_config.yaml`](./.deeplogic/inspect_config.yaml)
