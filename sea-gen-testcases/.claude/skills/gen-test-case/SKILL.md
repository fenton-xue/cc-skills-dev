---
description: 将清洗后的需求自动转换为测试用例Excel文件，可直接导入项目管理系统
parameters:
  input:
    type: string
    description: 清洗后的需求JSON文件路径（相对于项目根目录）
    required: true
  output:
    type: string
    description: 输出Excel文件路径（默认为 testcases/{需求名称}-测试用例.xlsx）
    required: false
---

# gen-test-case

## 功能说明

此Skill会自动：

1. **读取清洗后的需求JSON**：解析 `cleaned/{需求}-cleaned.json`
2. **生成测试用例**：
   - 按功能模块组织测试用例
   - 每个测试场景生成一行测试用例
   - 测试步骤和预期结果用`#`分隔（第一条前也要加`#`）
   - 一级模块填充需求名称
   - 二/三/四级模块从功能模块层级获取
3. **调用Python脚本生成Excel**：使用 `.claude/skills/gen-test-case/scripts/generate_excel.py`
4. **输出Excel文件**：保存到 `testcases/` 目录，符合导入格式

## 输出格式

生成符合导入模板的Excel文件，包含以下列：

| 一级模块 | 二级模块 | 三级模块 | 四级模块 | 用例名称 | 优先级 | 用例类型 | 前置条件 | 步骤描述 | 预期结果 | 备注 | 维护人 |
|---------|---------|---------|---------|----------|--------|---------|---------|---------|---------|------|--------|
| 需求名称 | 录入SO | | | 77879-A001-录入SO | P1 | 功能测试 | | #步骤1#步骤2 | #结果1#结果2 | | |
| 需求名称 | 导入SO | | | 77879-A002-导入SO | P1 | 功能测试 | | #步骤1#步骤2 | #结果1#结果2 | | |

**字段说明**：
- **一级模块**：需求名称（自动填充）
- **二级/三级/四级模块**：从business_functions中提取
- **用例名称**：`{需求ID}-{场景ID}-{简短描述}`
- **优先级**：P0/P1/P2/P3（从场景优先级获取）
- **用例类型**：固定为"功能测试"
- **前置条件**：空（不生成）
- **步骤描述**：用`#`分隔的测试步骤（**第一条前也要加`#`**）
- **预期结果**：用`#`分隔的预期结果（**第一条前也要加`#`**）
- **备注**：空
- **维护人**：空

## Excel文件结构

```
行1: 12列表头（由脚本生成）
行2: 测试用例1
行3: 测试用例2
...
```

**注意**：不再需要模板文件，脚本直接生成符合导入格式的Excel。

## 输入JSON格式

期望的cleaned.json结构：

```json
{
  "requirement": {
    "req_id": "REQ-77879",
    "title": "海运系统添加直达/中转字段",
    "module_name": "#77879 海运系统添加直达/中转字段"
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
              "expected_result": "录入SO弹窗中, 新增航程类型字段, 位于船公司和船名航次之间"
            },
            {
              "step_order": 2,
              "step_description": "B2B + 非自发 + 美国 + 待订舱 订单, 点击录入SO, 航船类型选择 直达",
              "expected_result": "订单状态流转至确认发船中, 订舱状态流转至已订舱, 航程类型正常落库"
            }
          ]
        }
      ]
    }
  ]
}
```

## 执行步骤

当用户执行此Skill时，我将按以下步骤操作：

1. **读取清洗后的需求JSON**
   - 读取 `{{input}}` 指定的JSON文件
   - 提取需求信息和business_functions数组

2. **读取测试用例模板**
   - 读取Excel模板文件（默认从需求文件夹获取）
   - 保存模板的前两行（说明和示例）

3. **生成测试用例数据**
   - 遍历business_functions数组
   - 对每个function下的每个scenario：
     * 生成用例名称：`{req_id}-{scenario_id}-{scenario_name的简短描述}`
     * 一级模块：requirement.module_name
     * 二级模块：function.function_name（如果level是"二级模块"）
     * 三级模块：function.function_name（如果level是"三级模块"）
     * 优先级：scenario.priority
     * 用例类型：固定为"功能测试"
     * 前置条件：空
     * 步骤描述：用`#`拼接所有test_steps的step_description
     * 预期结果：用`#`拼接所有test_steps的expected_result
     * 备注：空
     * 维护人：空

4. **生成Excel文件**
   - 使用xlsxwriter创建Excel文件
   - 第一、二行从模板复制
   - 后续行写入测试用例数据
   - 保存到 `testcases/` 目录

5. **报告结果**
   - 向用户展示生成摘要：
     * 生成的测试用例数量
     * 涉及的功能模块数量
     * 总测试步骤数量
     * 输出文件路径

## 注意事项

- 测试步骤用`#`分隔，每个步骤是独立的测试点
- 不生成前置条件（按用户习惯）
- 用例类型固定为"功能测试"
- 不生成接口、性能、安全测试用例（这些测试单独开展）
- 二/三/四级模块按需生成（根据function_level）

---

## 执行指令

当用户调用此Skill时，请按以下步骤执行：

1. **解析参数**
   - 从 `{{input}}` 参数获取清洗后的JSON文件路径
   - 从 `{{template}}` 参数获取测试用例模板路径（如果提供）
   - 从 `{{output}}` 参数获取输出Excel文件路径（如果提供）

2. **读取清洗后的需求JSON**
   - 使用Read工具读取 `{{input}}` 指定的JSON文件
   - 如果文件不存在，提示用户并提供帮助
   - 解析JSON，提取：
     * requirement信息（req_id, title, module_name）
     * business_functions数组

3. **读取测试用例模板**
   - **此步骤已移除**，不再需要读取模板
   - Excel表头由Python脚本直接生成

4. **生成测试用例数据**
   - 初始化测试用例列表
   - 遍历business_functions：
     * 记录function_name和function_level
     * 遍历该function下的所有scenarios
     * 对每个scenario：
       - 生成用例名称：`{req_id}-{scenario_id}-{简短描述}`
       - 提取priority
       - 拼接test_steps：
         * 步骤描述：`#` + `#`.join([step['step_description'] for step in test_steps])
         * 预期结果：`#` + `#`.join([step['expected_result'] for step in test_steps])
       - 组装一行测试用例数据

5. **调用Python脚本生成Excel**
   - **此时需要调用Python脚本**
   - 脚本路径：`.claude/skills/gen-test-case/scripts/generate_excel.py`
   - 执行命令：
     ```bash
     conda run -n claude-code --no-capture-output python \
       .claude/skills/gen-test-case/scripts/generate_excel.py \
       <json_file_path> <output_file_path>
     ```
   - 脚本会：
     * 读取JSON文件
     * 生成12列表头（符合项目管理系统导入格式）
     * 写入测试用例数据（从第二行开始，不保留示例数据）
     * 设置列宽
     * 保存Excel文件

6. **保存输出文件**
   - 确定输出文件路径：
     * 如果提供了`{{output}}`参数，使用它
     * 否则使用默认路径：`testcases/{需求标题}-测试用例.xlsx`
   - 确保文件格式正确，可导入项目管理系统

7. **报告结果**
   - 向用户展示生成摘要：
     * 需求ID和标题
     * 生成的测试用例数量
     * 涉及的功能模块（列出所有function_name）
     * 总测试步骤数量
     * 输出文件路径
   - 提示用户：
     * 可以手动调整二/三/四级模块
     * 可以补充维护人
     * 确认Excel格式无误后导入项目管理系统

8. **错误处理**
   - 如果输入JSON格式不正确，提供友好的错误提示
   - 如果business_functions为空，警告并继续
   - 如果某个scenario的test_steps为空，警告并跳过该场景

**重要提示**：
- **Python环境**：使用 `claude-code` conda环境
- **步骤和预期结果**：必须用`#`分隔，第一条步骤前也要加`#`
- **用例类型**：固定为"功能测试"，不能更改
- **一级模块**：必须是requirement.module_name
- **Excel格式**：
  - 第一行是12列表头（不需要示例数据）
  - 第二行开始是实际测试用例
  - 符合项目管理系统导入格式
