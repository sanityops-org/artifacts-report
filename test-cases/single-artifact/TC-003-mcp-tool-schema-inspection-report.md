# SanityOps Framework v1.0 检查报告

**文件路径**: `d:\My Docunments\AI\artifacts-report\test-cases\single-artifact\TC-003-mcp-tool-schema.json`

**检查日期**: 2026-10-10

**检查员**: SanityOps Inspect Lite

---

## 执行摘要

### 统计概览

| 阶段 | P0 | P1 | P2 | N/A |
|---|---|---|---|---|
| Stage A (QD-T) | 8 FAIL / 5 PASS | 1 FAIL | 0 | 1 |
| Stage B (Cross) | - | - | - | 全部 |
| Stage C (Gate-0) | 2 FAIL / 2 INFO | - | - | - |
| Stage D (QD-PM) | 6 FAIL / 2 PASS | - | - | 4 |
| Stage E (EX Risk) | S3: 1 / S2: 0 / S1: 4 / S0: 0 | - | - | - |

### Gate结果
- **Gate-0**: ❌ **未通过** (G0-3, G0-4 失败)
- **Stage A**: ❌ **失败** (8个P0级问题)
- **Stage D**: ❌ **失败** (6个P0级问题)

### Risk-Explicit S-level摘要
- **S3 (Critical)**: 1项 - NR-S-2 Dangerous Capability Flag
- **S1 (Medium)**: 4项 - NR-S-1, NR-S-3, NR-S-4, NR-S-6
- **总扣分估算**: ~33.5分

---

## 状态板

```
┌─────────────────────────────────────────────────────────────────┐
│                    SANITYOPS INSPECTION STATUS                  │
├─────────────────────────────────────────────────────────────────┤
│  Artifact: TC-003-mcp-tool-schema.json                          │
│  Tier: L3 (High Risk)                                           │
│  AC-L: AC-L2  |  OR-L: OR-L3                                    │
├─────────────────────────────────────────────────────────────────┤
│  Stage A (Tool Schema)    │  ████████░░  FAIL  (8 P0)           │
│  Stage B (Cross-artifact) │  ░░░░░░░░░░  N/A   (单工件)          │
│  Stage C (Gate-0)         │  ██████░░░░  FAIL  (G0-3, G0-4)     │
│  Stage D (Permission)     │  ██████░░░░  FAIL  (6 P0)           │
│  Stage E (Risk Explicit)  │  ████░░░░░░  S3/S1 (5项风险)         │
│  Stage F (Impact)         │  ████░░░░░░  MAPPED                 │
├─────────────────────────────────────────────────────────────────┤
│  OVERALL: FAIL - 14 P0 findings, Gate-0 not satisfied             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage A: Tool Schema检查 (L3 Tier)

**Tier判定**: L3 (High Risk)

**判定依据**: Tool包含`command`字段用于执行系统命令，`args`传递参数，`env`设置环境变量。这属于"irreversible or sensitive operations"，符合L3定义。

### QD-T规则检查结果

| ID | Rule Name | Level | Result | Evidence |
|---|---|---|---|---|
| QD-T-1.1 | Base Field Missing | P0 | **PASS** | 包含`name` (line 12), `description` (line 13), `parameters` (line 14) |
| QD-T-1.2 | Required Field Inconsistency | P0 | **PASS** | `required: ["query"]`与`properties`一致 |
| QD-T-1.3 | Invalid Enum Constraints | P0 | **PASS** | `enum`定义有效，无重复/空值 |
| QD-T-1.4 | Uncontrolled additionalProperties | P0 | **FAIL** | `mcp_configs`数组项对象未设置`additionalProperties: false` |
| QD-T-2.1 | String Without Length Constraint | P0 | **FAIL** | `query`, `name`, `command`等string字段无长度限制 |
| QD-T-2.2 | String Without Format Constraint | P1 | **FAIL** | `command`字段无`pattern`或`format`约束 |
| QD-T-2.3 | Number Without Boundary | P0 | **PASS** | 无number类型字段 |
| QD-T-2.4 | Array Without Length Constraint | P0 | **FAIL** | `mcp_configs`和`args`数组无`maxItems`/`minItems` |
| QD-T-3.1 | Write Operation Not Identified | P0 | **FAIL** | 未明确声明会执行外部命令 |
| QD-T-3.2 | Raw Input Passthrough | P0 | **FAIL** | `command`/`args`直接传递用户输入到系统执行 |
| QD-T-3.3 | Batch Operation Without Limit | P0 | **FAIL** | `mcp_configs`数组无`maxItems`限制 |
| QD-T-3.4 | Internal Parameter Exposure | P0 | **PASS** | 未发现内部参数暴露 |
| QD-T-3.5 | Cross-Tool Data Flow Risk | P0 | **PASS** | 单工件无法评估 |
| QD-T-4.1 | Insufficient Description Quality | P0 | **FAIL** | `command`和`args`描述过于简单 |
| QD-T-4.2 | Undeclared Side Effects | P0 | **FAIL** | 未声明执行外部命令的副作用 |
| QD-T-4.3 | Multi-Tool Semantic Competition | P1 | **N/A** | 单工件无法评估 |

### Stage A FAIL详情

#### QD-T-1.4 | FAIL | Uncontrolled additionalProperties
**证据** (line 24-51):
```json
"mcp_configs": {
  "type": "array",
  "items": {
    "type": "object",
    "properties": { ... },
    "required": ["name", "command", "args"]
    // 缺少: "additionalProperties": false
  }
}
```

#### QD-T-2.1 | FAIL | String Without Length Constraint
**证据** (line 17-20):
```json
"query": {
  "type": "string",
  "description": "The research query to investigate"
  // 缺少: "maxLength": ..., "minLength": ...
}
```

#### QD-T-2.2 | FAIL | String Without Format Constraint
**证据** (line 31-34):
```json
"command": {
  "type": "string",
  "description": "Command to launch the MCP server"
  // 缺少: "pattern": "^[a-zA-Z0-9_-]+$" 或 "enum": [...]
}
```

#### QD-T-2.4 | FAIL | Array Without Length Constraint
**证据** (line 21-52):
```json
"mcp_configs": {
  "type": "array",
  // 缺少: "maxItems": ..., "minItems": ...
}
```

#### QD-T-3.1 | FAIL | Write Operation Not Identified
**证据** (line 13):
```json
"description": "MCP tool configuration for researching GitHub repositories alongside web search"
```
**问题**: 未包含"[This operation will execute system commands...]"等写入操作声明

#### QD-T-3.2 | FAIL | Raw Input Passthrough
**证据** (line 31-41):
```json
"command": {"type": "string"},
"args": {
  "type": "array",
  "items": {"type": "string"}
}
```
**问题**: 用户输入直接传递到系统命令执行，无结构化约束

#### QD-T-3.3 | FAIL | Batch Operation Without Limit
**证据**: `mcp_configs`数组无`maxItems`限制，可配置无限数量的MCP服务器

#### QD-T-4.1 | FAIL | Insufficient Description Quality
**证据** (line 33, 40):
```json
"description": "Command to launch the MCP server"
"description": "Arguments for the MCP server command"
```
**问题**: 未说明安全风险和使用限制

#### QD-T-4.2 | FAIL | Undeclared Side Effects
**问题**: 未声明执行`npx`等命令可能带来的网络访问、文件系统操作等副作用

---

## Stage B: Cross-artifact检查

**状态**: N/A (单工件用例)

**说明**: 此用例仅包含单个Tool Schema文件，无System Prompt或Skill定义，Cross-artifact检查不适用。

---

## Stage C: Gate-0检查

| ID | Condition | Result | Evidence |
|---|---|---|---|
| G0-1 | Single-artifact no unfixed P0 | INFO | Stage A发现8个P0 FAIL，非阻塞流程继续 |
| G0-2 | Cross-artifact no unfixed P0 | N/A | 单工件，Cross检查不适用 |
| G0-3 | Responsibility boundary statements exist | **FAIL** | 无System Prompt或Skill定义，无法定位责任边界 |
| G0-4 | Schema fields complete | **FAIL** | `command`和`args`参数描述不充分 |

**Gate-0结果**: ❌ 未通过 (G0-3, G0-4失败)

---

## Stage D: Permission QD-PM Quick Mode检查

**AC-L**: AC-L2 (存在Tool，无多Agent协作)

**OR-L**: OR-L3 (命令执行属于高风险操作)

| ID | Rule | Applicability | Result | Evidence |
|---|---|---|---|---|
| QD-PM-1.1 | Unexplainable permission | All | **FAIL** | `command`字段允许任意命令执行，无责任基线说明业务目的 |
| QD-PM-1.3 | Insufficient permission | All | **N/A** | 单工件，无完整上下文 |
| QD-PM-2.4 | Environment boundary not declared | All | **FAIL** | 无环境适用声明，未禁止生产环境执行 |
| QD-PM-3.3 | Role substitution | All | **PASS** | 无身份短语替代 |
| QD-PM-3.4 | High-risk operations not separated | Conditional | **FAIL** | 命令执行与常规操作共享授权路径 |
| QD-PM-4.2 | Downstream exceeds upstream | All | **N/A** | 单工件，无三层结构 |
| QD-PM-4.4 | Delegation escalation | AC-L4 only | **N/A** | AC-L2，无委托 |
| QD-PM-4.8 | External permission not incorporated | Conditional | **FAIL** | MCP连接外部协议，操作未声明 |
| QD-PM-5.4 | Isolation substitution | All | **N/A** | 未声明运行时隔离 |
| QD-PM-5.7 | Exemption uncontrolled | Conditional | **PASS** | 无豁免表达式 |
| QD-PM-6.3 | No human confirmation | Conditional | **FAIL** | 命令执行(OR-L3)无人工确认 |
| QD-PM-6.5 | Permission list not enumerable | All | **FAIL** | `command`可执行任意命令，权限集不可枚举 |

### Stage D FAIL详情

#### QD-PM-1.1 | FAIL | Unexplainable permission
**Classification Basis**: Command execution → OR-L3 → Basic mapping → P0
**证据**: `command`字段允许执行任意系统命令，但无责任基线说明其业务目的

#### QD-PM-2.4 | FAIL | Environment boundary not declared
**Classification Basis**: Write/delete via command → P0 (item-specific inline rule)
**证据**: 无环境适用声明，未明确禁止在生产环境执行高风险操作

#### QD-PM-3.4 | FAIL | High-risk operations not separated
**Classification Basis**: Irreversible operations → Fixed P0 (R1)
**证据**: 命令执行（不可逆操作）与常规查询操作共享同一授权路径

#### QD-PM-4.8 | FAIL | External permission not incorporated
**Classification Basis**: External operations contain write/delete → P0
**证据**: MCP服务器连接外部协议，但操作未在工件中声明

#### QD-PM-6.3 | FAIL | No human confirmation
**Classification Basis**: Fixed P0 (R1)
**证据**: 命令执行（OR-L3操作）无人工确认或审批要求

#### QD-PM-6.5 | FAIL | Permission list not enumerable
**Classification Basis**: Fixed P0 (R1)
**证据**: `command`字段可接受任意字符串，实际可执行权限无法枚举

---

## Stage E: Risk Explicit检查

### NL-A家族 (Continuous Type)

| ID | Result | Evidence |
|---|---|---|
| NL-A-1 ~ NL-A-9 | **PASS** | 未发现连续型自然语言风险 |

### NL-B家族 (Non-Continuous Type)

| ID | Result | Evidence |
|---|---|---|
| NL-B-1 ~ NL-B-10 | **PASS** | 单工件，无跨对象风险碎片 |

### NR-O家族 (Obfuscated Coding)

| ID | Result | Evidence |
|---|---|---|
| NR-O-1 ~ NR-O-5 | **PASS** | 未发现编码/混淆风险 |

### NR-S家族 (Structured Configuration) - **关键发现**

| ID | Result | Evidence | D1/D2/D3 | S-Level | Deduction |
|---|---|---|---|---|---|
| NR-S-1 | **FAIL** | `command`字段允许任意命令 | D1-2/D2-2/D3-2 | S1 | ~4.0 |
| NR-S-2 | **FAIL** | `command`+`args`启用代码执行 | D1-3/D2-3/D3-3 | **S3** | ~17.5 |
| NR-S-3 | **FAIL** | `command`无约束声明 | D1-2/D2-2/D3-2 | S1 | ~4.0 |
| NR-S-4 | **FAIL** | `args`数组传递代码片段 | D1-2/D2-2/D3-2 | S1 | ~4.0 |
| NR-S-5 | **PASS** | 描述字段无指令注入 | - | S0 | 0 |
| NR-S-6 | **FAIL** | 示例包含可执行命令 | D1-1/D2-1/D3-1 | S0 | ~0 |
| NR-S-7 | **PASS** | 无异常回调地址 | - | S0 | 0 |
| NR-S-8 | **PASS** | 工具名称无冲突 | - | S0 | 0 |

### Stage E关键风险详情

#### NR-S-2 | S3 (Critical) | Dangerous Capability Flag Explicitly Enabled
**风险表达式**:
```json
"command": {"type": "string"},
"args": {"type": "array", "items": {"type": "string"}}
```
**分析**: 此配置实质启用了任意代码执行能力，等同于`"allow_code_execution": true`

**D1/D2/D3评估**:
- D1 (Confidentiality): D1-3 - 可能导致完整对话历史泄露
- D2 (Integrity): D2-3 - 系统数据可能被不可逆破坏
- D3 (Authorization): D3-3 - 权限验证机制可被完全绕过

**S-Level**: S3 (Critical) - Rule-1 One-Vote Veto (D2-3 OR D3-3)

---

## Stage F: Impact映射

### Attack Surface (AS) 映射

| Finding | AS分类 | 描述 |
|---|---|---|
| QD-T-3.2 | AS-CMD | 命令注入攻击面 |
| QD-T-3.4 | AS-ENV | 环境变量暴露攻击面 |
| QD-PM-4.8 | AS-EXT | 外部服务权限攻击面 |
| NR-S-2 | AS-EXEC | 代码执行攻击面 |

### Failure Mode (FM) 映射

| Finding | FM分类 | 描述 |
|---|---|---|
| QD-T-1.4 | FM-VAL | 验证失败模式 |
| QD-T-2.1/2.4 | FM-DOS | 拒绝服务风险 |
| QD-T-3.3 | FM-DOS | 批量操作拒绝服务 |
| QD-PM-6.3 | FM-UNA | 未授权操作 |
| QD-PM-6.5 | FM-ENU | 权限枚举失败 |
| NR-S-2 | FM-RCE | 远程代码执行 |

---

## 附录: 原始引用

### 关键代码片段

**Line 12-14 - Tool基础定义**:
```json
"name": "github_mcp_research",
"description": "MCP tool configuration for researching GitHub repositories alongside web search",
"parameters": { ... }
```

**Line 21-52 - MCP配置数组**:
```json
"mcp_configs": {
  "type": "array",
  "description": "List of MCP server configurations",
  "items": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "command": { "type": "string" },
      "args": { "type": "array", "items": { "type": "string" } },
      "env": { "type": "object", "additionalProperties": { "type": "string" } }
    },
    "required": ["name", "command", "args"]
  }
}
```

**Line 66 - Required字段**:
```json
"required": ["query"]
```

---

## 结论与建议

### 总体评估

**检查结果**: ❌ **FAIL**

**关键问题**:
1. **命令执行风险**: Tool允许通过`command`和`args`执行任意系统命令，属于高危操作
2. **缺乏约束**: 关键字段无长度、格式、数量限制
3. **权限不可枚举**: `command`字段可接受任意字符串，实际权限范围无法确定
4. **无人工确认**: 高风险操作无人工审批流程

### 修复建议

1. **限制命令范围**: 使用`enum`限定允许的命令，而非任意字符串
2. **添加约束**: 为所有string和array字段添加`maxLength`/`maxItems`
3. **声明副作用**: 在description中明确说明会执行系统命令及其风险
4. **环境隔离**: 声明仅允许在沙箱/隔离环境中执行
5. **人工确认**: 为命令执行操作添加人工确认要求

---

*报告生成时间: 2026-10-10*

*SanityOps Framework v1.0 - Inspect Lite*
