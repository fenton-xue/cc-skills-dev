---
description: 将需求文档、表结构变更清洗为结构化的JSON格式，便于后续生成测试用例
parameters:
  input:
    type: string
    description: 需求文件夹路径（包含需求文档.md和表结构变更.md）
    required: true
  context:
    type: string
    description: 测试配置文件路径（默认为 context/test-context.yaml）
    required: false
  output:
    type: string
    description: 输出文件路径（默认为 cleaned/{原文件夹名}-cleaned.json）
    required: false
---

# clean-requirement

## 功能说明

此Skill会自动：

1. **读取需求文档**：解析 `需求文档.md`
2. **读取表结构变更**：解析 `表结构变更.md`（如果存在）
3. **读取数据库设计文档**：从 `database-designs/` 读取引用的表结构
4. **提取结构化信息**：
   - 需求ID和标题
   - 需求类型和优先级
   - 业务规则列表
   - 数据库设计（表结构、字段变更、数据流转）
   - 验收标准
   - 可测试点
5. **生成JSON格式输出**：保存到 `cleaned/` 目录
6. **质量检查**：确保提取的信息完整性和准确性

## 输出格式

生成的JSON文件包含以下结构：

```json
{
  "requirement_info": {
    "source_folder": "需求文件夹路径",
    "req_doc": "需求文档.md",
    "table_change_doc": "表结构变更.md（如果存在）",
    "cleaned_date": "清洗日期时间",
    "cleaned_by": "Claude Code Agent"
  },
  "system_context": {
    "system_name": "系统名称（从.claude/CLAUDE.md读取）",
    "core_business": "核心业务描述"
  },
  "requirement": {
    "req_id": "需求编号",
    "title": "需求标题",
    "type": "需求类型",
    "priority": "优先级",
    "description": "需求描述",
    "module_name": "需求名称（用于Excel的一级模块）",
    "business_rules": [
      {
        "rule_id": "规则编号",
        "description": "规则描述",
        "conditions": ["前置条件"],
        "expected_outcome": "预期结果"
      }
    ],
    "acceptance_criteria": ["验收标准"],
    "related_requirements": ["关联需求ID"]
  },
  "database_design": {
    "tables_involved": [
      {
        "table_name": "t_marine_order",
        "table_description": "海运单表",
        "changes": [
          {
            "change_type": "ADD_COLUMN",
            "field_name": "merge_group_no",
            "field_type": "VARCHAR(20)",
            "description": "并单组编号"
          }
        ]
      }
    ],
    "data_flow": [
      "并单：生成merge_group_no，写入t_marine_order",
      "合并清关：生成merge_clearance_group_no，写入t_receipt_order"
    ],
    "validation_rules": [
      "合并清关与拆分清关字段互斥",
      "编号格式：VB/CM/CS + YYYYMMDD + 4位序号"
    ]
  },
  "business_functions": [
    {
      "function_name": "录入SO",
      "function_level": "二级模块",
      "function_priority": "P1",
      "scenarios": [
        {
          "scenario_id": "A001",
          "scenario_name": "录入SO - 航程类型字段验证",
          "priority": "P1",
          "description": "验证录入SO时航程类型字段的显示和保存",
          "test_steps": [
            {
              "step_order": 1,
              "step_description": "对于处于待订舱的订单, 点击录入SO",
              "expected_result": "录入SO弹窗中, 新增航程类型字段, 位于船公司和船名航次之间, 有必填符号*, 默认文本请选择"
            },
            {
              "step_order": 2,
              "step_description": "B2B + 非自发 + 美国 + 待订舱 订单, 点击录入SO, 航船类型选择 直达",
              "expected_result": "订单状态流转至确认发船中, 订舱状态流转至已订舱, 航程类型正常落库 t_marine_order.voyage_type 操作日志记录该字段, 值从无->直达"
            }
          ]
        }
      ]
    },
    {
      "function_name": "导入SO",
      "function_level": "二级模块",
      "function_priority": "P1",
      "scenarios": [...]
    }
  ],
  "summary": {
    "total_business_rules": "业务规则总数",
    "total_functions": "功能模块数量",
    "total_scenarios": "测试场景总数",
    "total_test_steps": "测试步骤总数"
  }
}
```

## 文档格式建议

### 需求文档.md（必需）

```markdown
# 需求标题

**需求编号**: REQ-001
**优先级**: 高
**需求类型**: 功能需求

## 需求描述
详细描述功能需求...

## 业务规则
1. 规则1描述
   - 前置条件：...
   - 预期结果：...

## 验收标准
- [ ] 验收标准1
- [ ] 验收标准2

## 依赖关系
- 前置需求：REQ-002
- 相关需求：REQ-003
```

### 表结构变更.md（可选，强烈推荐）

```markdown
# #需求编号 表结构变更

## 变更概述
本需求涉及3个表的字段新增和1个新表创建

## 新增字段

### 1. t_marine_order 表新增字段

| 字段名         | 类型        | 说明                                  |
| -------------- | ----------- | ------------------------------------- |
| merge_group_no | VARCHAR(20) | 并单组编号，格式：VB+YYYYMMDD+3位序号  |

**SQL**：
```sql
ALTER TABLE t_marine_order
ADD COLUMN merge_group_no VARCHAR(20) DEFAULT NULL;
```

## 新增表

### t_order_group_sequence（编号序列表）

**完整结构**：（因为是新表，写完整）

| 字段名       | 类型        | 说明                    |
| ------------ | ----------- | ----------------------- |
| id           | BIGINT      | 主键ID                  |
| group_type   | VARCHAR(10) | 组类型                  |
| ...          | ...         | ...                     |

**SQL**：
```sql
CREATE TABLE t_order_group_sequence (...);
```

## 引用表结构
- t_marine_order：见 `database-designs/公共表设计.md`
- t_receipt_order：见 `database-designs/公共表设计.md`

## 数据流转规则
1. 并单操作：生成merge_group_no，写入t_marine_order
2. 合并清关：生成merge_clearance_group_no，写入t_receipt_order

## 数据验证规则
- 合并清关与拆分清关字段互斥
- 编号格式校验
```

### database-designs/*.md（可选，推荐）

存放通用表结构，供多个需求复用。在`表结构变更.md`中引用即可。

## 执行步骤

当用户执行此Skill时，我将按以下步骤操作：

1. **读取系统背景**（如果存在）
   - 读取 `.claude/CLAUDE.md`
   - 提取系统名称、核心业务、订单状态流转等

2. **读取需求文档**
   - 读取 `{{input}}/需求文档.md`
   - 提取需求ID、标题、描述、业务规则、验收标准

3. **读取表结构变更**（如果存在）
   - 检查 `{{input}}/表结构变更.md` 是否存在
   - 如果存在，解析表结构变更信息：
     * 新增字段
     * 新增表
     * 索引变更
     * 数据流转规则
     * 数据验证规则

4. **读取数据库设计文档**（如果被引用）
   - 从`表结构变更.md`中提取引用的表：`见 database-designs/XXX.md`
   - 读取 `database-designs/` 目录下对应文档
   - 合并完整的表结构信息

5. **读取测试配置**（如果存在）
   - 读取 `context/test-context.yaml`
   - 提取测试规范、优先级定义

6. **生成测试点**
   - 基于业务规则生成功能测试点
   - 基于表结构变更生成数据库验证测试点
   - 基于数据流转规则生成集成测试点

7. **生成JSON输出**
   - 组织所有提取的信息
   - 生成唯一ID（req_id, rule_id, point_id）
   - 填充database_design字段

8. **保存并报告**
   - 保存到 `cleaned/` 目录
   - 打印清洗摘要

## 注意事项

- `表结构变更.md`是可选的，但强烈推荐提供
- 如果`表结构变更.md`引用了`database-designs/`中的文档，会自动读取
- 建议人工检查生成的JSON文件，必要时手动调整
- 数据库验证测试点会根据表结构变更自动生成

---

## 执行指令

当用户调用此Skill时，请按以下步骤执行：

1. **解析参数**
   - 从 `{{input}}` 参数获取需求文件夹路径（注意：是文件夹，不是文件）
   - 从 `{{context}}` 参数获取测试配置路径（如果提供）
   - 从 `{{output}}` 参数获取输出路径（如果提供）

2. **读取系统背景**
   - 使用Read工具读取 `.claude/CLAUDE.md`（如果存在）
   - 提取系统名称、核心业务、订单状态流转等信息

3. **读取需求文档**
   - 使用Read工具读取 `{{input}}/需求文档.md`
   - 如果文件不存在，提示用户并提供帮助

4. **读取表结构变更**（可选）
   - 检查 `{{input}}/表结构变更.md` 是否存在
   - 如果存在，使用Read工具读取
   - 提取：
     * 变更概述
     * 新增字段（表名、字段名、类型、说明、SQL）
     * 新增表（表名、完整结构、SQL）
     * 索引变更
     * 数据流转规则
     * 数据验证规则
     * 引用的database-designs文档

5. **读取数据库设计文档**（如果被引用）
   - 从`表结构变更.md`中提取引用信息，如：`见 database-designs/公共表设计.md`
   - 使用Read工具读取对应的`database-designs/`目录下的文档
   - 提取完整的表结构信息
   - 合并到表结构变更信息中

6. **读取测试配置**（可选）
   - 如果 `context/test-context.yaml` 存在，使用Read工具读取
   - 提取测试规范、优先级定义

7. **解析并提取信息**
   - 从需求文档提取：
     * 需求编号、标题、类型、优先级
     * 需求描述
     * 业务规则（包括规则ID、描述、前置条件、预期结果）
     * 验收标准
     * 依赖关系
   - 从表结构变更提取：
     * 涉及的表清单
     * 字段变更详情
     * 数据流转规则
     * 数据验证规则

8. **生成测试点**
   - 基于业务规则生成业务功能测试场景
   - 按功能模块分组（如"录入SO"、"导入SO"）
   - 每个场景包含多个测试步骤（步骤之间是独立的测试点，不是因果关系）
   - 基于表结构变更生成数据库验证步骤
   - 为每个测试步骤生成唯一序号
   - **重要**：不区分测试类型（positive/negative等），只关注业务功能

9. **生成JSON输出**
   - 按照上述"输出格式"部分定义的JSON结构组织数据
   - 填充以下字段：
     * requirement_info（源文件信息）
     * system_context（系统背景）
     * requirement（需求信息，包含module_name）
     * database_design（数据库设计，如果有表结构变更）
     * business_functions（按功能模块组织的测试场景）
     * summary（汇总信息）
   - **关键**：business_functions数组中的每个function包含：
     * function_name（功能模块名称，用于Excel的二级/三级模块）
     * function_level（模块级别）
     * scenarios（测试场景数组）
     * 每个scenario包含scenario_id（字母编号，如A001、A002）和test_steps数组

10. **保存输出文件**
    - 确定输出文件路径（默认为 `cleaned/{原文件夹名}-cleaned.json`）
    - 使用Write工具保存JSON文件
    - 确保JSON格式正确且可解析

11. **报告结果**
    - 向用户展示清洗摘要：
      * 需求ID和标题
      * 业务规则数量
      * 涉及的表数量
      * 生成的测试点数量（包括数据库验证测试点）
      * 输出文件路径
    - 提示用户检查生成的JSON文件，必要时手动调整

12. **错误处理**
    - 如果`需求文档.md`不存在，报错并提示
    - 如果`表结构变更.md`不存在，提示"未找到表结构变更，跳过数据库相关提取"
    - 如果引用的`database-designs/`文档不存在，警告但继续执行
    - 如果某些信息无法提取，使用默认值或标注为null

**重要提示**：
- `{{input}}`是文件夹路径，不是文件路径
- `表结构变更.md`是可选的，但强烈推荐
- 数据库验证测试点会根据表结构变更自动生成，这对功能测试很重要
- 如果引用了`database-designs/`中的文档，一定要确保读取并合并完整信息
