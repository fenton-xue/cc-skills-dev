# SeaGen Testcases - 上下文恢复文档

**项目位置**：`cc-skills-dev/sea-gen-testcases/`

生成时间：2026-01-02
项目状态：核心功能已完成，等待测试验证

---

## 项目说明

本文档记录了 **cc-skills-dev** 工作空间中 **SeaGen Testcases** 示例项目的开发上下文。

**cc-skills-dev** 是一个用于开发和维护Claude Code Agent Skills的工作空间，包含完整的Skills开发示例。SeaGen Testcases 是其中的第一个示例项目，展示如何为海运系统开发测试用例自动生成Skills。

---

## 一、项目背景

### 用户身份
- 角色：软件测试工程师
- 工作系统：海运管理系统（Web系统）
- 日常任务：将产品需求文档转换为测试用例，导入项目管理系统

### 核心诉求
1. 自动化需求清洗：将非结构化的需求文档转换为结构化JSON
2. 自动化用例生成：将清洗后的需求生成可直接导入的Excel测试用例
3. **只关注业务功能测试**：接口测试、性能测试、安全测试单独开展，不在此项目中

---

## 二、核心设计理念（非常重要！）

### 1. 测试步骤是独立的测试点
**特点**：
- 一条测试用例包含多个测试步骤
- 步骤之间**是独立的测试点**，不是因果关系的步骤顺序
- 例如："验证字段显示"和"验证数据保存"是两个独立的步骤

**格式**：用`#`分隔步骤和预期结果
```
步骤描述：#步骤1#步骤2#步骤3
预期结果：#结果1#结果2#结果3
```

### 2. 只生成业务功能测试用例
**不做**：接口测试、性能测试、安全测试
**只做**：业务功能测试
**用例类型**：固定为"功能测试"

理由：这些测试类型在用户的工作中是单独开展的，不需要在这个项目中体现。

### 3. 按功能模块组织测试用例
**从需求到测试用例的转换**：

需求文档：
```
## 1、订舱管理增加字段说明
1）录入SO...
2）导入SO...
3）订舱管理tab...
```

清洗后（business_functions）：
```json
{
  "business_functions": [
    {
      "function_name": "录入SO",
      "scenarios": [...]
    },
    {
      "function_name": "导入SO",
      "scenarios": [...]
    }
  ]
}
```

生成的测试用例：
```
一级模块           | 二级模块 | 用例名称
#77879 海运系统   | 录入SO   | 77879-A001-录入SO
#77879 海运系统   | 导入SO   | 77879-A002-导入SO
```

### 4. 简化的字段映射

| 字段 | 生成方式 | 说明 |
|------|---------|------|
| 一级模块 | 需求名称 | 自动填充 |
| 二/三/四级模块 | 从function_name提取 | 按需生成 |
| 用例名称 | {需求ID}-{场景ID}-{简短描述} | 自动生成 |
| 优先级 | 从业务重要性推断 | P0/P1/P2/P3 |
| 用例类型 | 固定"功能测试" | 不可更改 |
| 前置条件 | 空 | 不生成 |
| 步骤描述 | 用`#`拼接 | 多个独立步骤 |
| 预期结果 | 用`#`拼接 | 对应每个步骤 |
| 备注 | 空 | 不生成 |
| 维护人 | 空 | 用户后续补充 |

---

## 三、四层上下文机制

### 第一层：系统背景知识（`.claude/CLAUDE.md`）
存放被测试系统的核心业务信息：
- 系统定位：海运管理系统，追踪海运订单的物流信息
- 上游系统：OSJ、B2B、3PL
- 订单业务维度：5个国家（美国/加拿大/英国/德国/日本），3种类型（非自发/自发/LOCAL）
- 订单状态流转：待分区→待排船→待确认发船→确认发船中→海运中→已到港→已到仓→空箱待还→完成

### 第二层：需求与DB文档（`requirements/{需求ID}/`）
- `需求文档.md`：产品经理写的功能需求（必需）
- `表结构变更.md`：DB相关设计（新增字段、新增表、数据流转规则）- 强烈推荐
- `技术文档.md`：开发技术文档（仅参考，不清洗）

### 第三层：通用表结构（`database-designs/`）
存放通用表结构（如t_marine_order、t_receipt_order），供多个需求复用。
在`表结构变更.md`中引用即可。

### 第四层：测试配置（`context/test-context.yaml`）
测试用例编写规范、优先级定义规则、测试数据设计原则。

---

## 四、项目结构

```
sea-gen-testcases/                       # 这是一个完整的测试项目
├── .claude/
│   ├── skills/                           # Agent Skills定义
│   │   ├── clean-requirement/            # Skill 1: 需求清洗
│   │   │   └── SKILL.md
│   │   └── gen-test-case/               # Skill 2: 测试用例生成
│   │       └── SKILL.md
│   └── CLAUDE.md                         # 系统背景知识（海运管理系统）
│
├── database-designs/                     # 数据库设计（通用表结构）
│   ├── README.md
│   ├── 公共表设计.md
│   └── 编号序列表.md
│
├── requirements/                         # 需求文档目录
│   ├── #1001 用户登录功能/
│   │   ├── 需求文档.md
│   │   └── 技术设计.md
│   ├── #77879 海运系统添加直达中转字段/
│   │   ├── 需求文档.md
│   │   ├── testcase_output.txt           # 用户实际测试用例（参考）
│   │   └── template_output.txt           # Excel导入模板（参考）
│   └── #71489 新增并单、合并清关、拆分清关功能/
│   │       ├── 需求文档.md
│   │       ├── 表结构变更.md
│   │       └── 技术文档.md
│   ├── context/                          # 测试上下文配置
│   │   └── test-context.yaml
│   ├── cleaned/                          # 清洗后的需求（JSON格式）
│   └── testcases/                        # 生成的测试用例（Excel格式）
│
├── README.md                             # 项目说明文档
└── sea-gen-testcases.md                  # 本文档
```

---

## 五、工作流程

```
需求文档.md + 表结构变更.md(可选) + 系统背景(CLAUDE.md)
    ↓
[Skill 1: clean-requirement] → 读取database-designs/中的表结构
    ↓
清洗后需求(JSON) → 包含完整的DB信息 + 按功能模块组织的测试场景
    ↓
[Skill 2: gen-test-case] → 读取测试用Excel模板
    ↓
测试用例.xlsx → 可直接导入项目管理系统的Excel文件
```

### 执行命令

```bash
cd sea-gen-testcases

# 1. 执行需求清洗
clean-requirement --input "requirements/#77879 海运系统添加直达中转字段"

# 2. 生成测试用例
gen-test-case --input "cleaned/#77879 海运系统添加直达中转字段-cleaned.json"
```

---

## 六、关键文件说明

### 1. clean-requirement Skill

**文件**：`sea-gen-testcases/.claude/skills/clean-requirement/SKILL.md`

**功能**：将需求文档和表结构变更解析为结构化JSON

**输入**：
- `--input`：需求文件夹路径（包含`需求文档.md`和`表结构变更.md`）
- 系统背景（自动读取`.claude/CLAUDE.md`）
- 数据库设计（自动读取`database-designs/`中的表结构）

**输出**：
- `cleaned/{需求名称}-cleaned.json`

**关键特性**：
- 按功能模块组织测试场景（business_functions）
- 只关注业务功能测试（不生成接口/性能/安全测试）
- 提取数据库设计信息（用于DB验证测试）

**输出JSON结构**：
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
      "scenarios": [
        {
          "scenario_id": "A001",
          "scenario_name": "录入SO - 航程类型字段验证",
          "priority": "P1",
          "test_steps": [
            {
              "step_order": 1,
              "step_description": "对于处于待订舱的订单, 点击录入SO",
              "expected_result": "录入SO弹窗中, 新增航程类型字段, 位于船公司和船名航次之间"
            }
          ]
        }
      ]
    }
  ]
}
```

### 2. gen-test-case Skill

**文件**：`sea-gen-testcases/.claude/skills/gen-test-case/SKILL.md`

**功能**：将清洗后的需求转换为可导入的Excel测试用例

**输入**：
- `--input`：清洗后的需求JSON文件路径
- `--template`：测试用例导入模板路径（可选）
- `--output`：输出Excel文件路径（可选）

**输出**：
- `testcases/{需求名称}-测试用例.xlsx`

**关键特性**：
- 生成符合12列模板的Excel
- 测试步骤和预期结果用`#`分隔
- 用例类型固定为"功能测试"
- 一级模块自动填充需求名称
- 二/三/四级模块从功能模块提取

**Excel列结构**：
| 一级模块 | 二级模块 | 三级模块 | 四级模块 | 用例名称 | 优先级 | 用例类型 | 前置条件 | 步骤描述 | 预期结果 | 备注 | 维护人 |

---

## 七、重要设计决策及原因

### 决策1：不生成前置条件
**原因**：用户不喜欢写前置条件，如果必须写会直接写在测试步骤里

### 决策2：用例类型固定为"功能测试"
**原因**：用户在工作中只会用这一种类型，接口、性能、安全测试是单独开展的

### 决策3：不生成备注和维护人
**原因**：用户会在导入前手动补充这些字段

### 决策4：一级模块自动填充，二/三/四级模块按需生成
**原因**：用户不确定最终把用例放在哪个目录下，需要在导入前根据实际情况调整

### 决策5：测试步骤用`#`分隔，且是独立测试点
**原因**：这是用户工作系统的特殊要求，步骤之间不是因果关系，而是并列的测试点

### 决策6：从test_points改为business_functions
**原因**：按功能模块组织更符合用户思维，也便于映射到Excel的模块层级

---

## 八、已完成的工作

✅ **Skill 1: clean-requirement**
- 创建SKILL.md文件
- 定义输入参数（input, context, output）
- 定义输出JSON结构（business_functions格式）
- 编写执行指令和错误处理逻辑

✅ **Skill 2: gen-test-case**
- 创建SKILL.md文件
- 定义输入参数（input, template, output）
- 定义Excel生成逻辑（12列格式）
- 编写测试用例组装规则

✅ **README文档**
- 完整的项目说明
- 工作流程图
- 核心设计理念说明
- 快速开始指南
- 注意事项

✅ **示例项目结构**
- 创建系统背景配置（.claude/CLAUDE.md）
- 创建数据库设计文档结构（database-designs/）
- 准备示例需求文档（#77879, #71489）

---

## 九、下一步工作

### 待验证
1. **测试clean-requirement skill**
   - 运行：`clean-requirement --input "requirements/#77879 海运系统添加直达中转字段"`
   - 检查生成的JSON文件格式是否正确
   - 验证business_functions结构是否符合预期

2. **测试gen-test-case skill**
   - 运行：`gen-test-case --input "cleaned/#77879 海运系统添加直达中转字段-cleaned.json"`
   - 检查生成的Excel文件格式
   - 验证是否能正确导入项目管理系统

3. **端到端测试**
   - 使用#71489需求文档（包含完整的表结构变更）测试完整流程
   - 验证DB验证测试点是否正确生成

### 待完善（可选）
1. 创建测试配置文件（context/test-context.yaml）
2. 增加更多的错误处理和友好提示
3. 优化business_functions的自动识别逻辑
4. 添加人工校验检查点

---

## 十、环境配置

### Conda环境
```bash
# 创建环境
conda create -n claude-code python=3.11

# 激活环境
conda activate claude-code

# 安装依赖
pip install pandas==2.0.3 openpyxl==3.1.2 xlsxwriter==3.1.9 numpy==1.24.3
```

### 辅助脚本
`read_excel.py`：用于读取Excel文件（处理中文编码问题）

```python
import pandas as pd
import sys

file_path = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_excel(file_path)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('=== 列名 ===\n')
    f.write(str(df.columns.tolist()))
    # ... 更多输出
```

---

## 十一、关键注意事项

1. **系统背景要准确**：`.claude/CLAUDE.md`是所有技能的基础
2. **表结构变更很重要**：帮助生成数据库验证测试点
3. **人工校验必要**：清洗后的JSON建议人工检查
4. **用例可调整**：生成后可手动调整模块层级和维护人
5. **测试步骤是独立的**：不是因果关系，是并列的测试点
6. **只生成功能测试**：不涉及接口、性能、安全测试

---

## 十二、参考文档位置

### 用户实际测试用例
`sea-gen-testcases/requirements/#77879 海运系统添加直达中转字段/testcase_output.txt`

关键发现：
- 7个测试用例
- 前置条件全部为空（NaN）
- 步骤用`#`分隔
- 多个独立测试步骤
- 用例名称格式：{需求ID}-{字母编号}-{简短描述}

### Excel导入模板
`sea-gen-testcases/requirements/#77879 海运系统添加直达中转字段/template_output.txt`

关键信息：
- 12列结构
- 第一行是说明文档
- 第二行是示例数据
- 从第三行开始是实际测试用例

### 需求文档示例
`sea-gen-testcases/requirements/#77879 海运系统添加直达中转字段/#77879 海运系统添加直达中转字段.md`

包含完整的功能需求描述。

---

## 十三、快速恢复工作流

如果您在公司打开Claude Code，可以这样恢复上下文：

1. **阅读本文档**：了解项目背景和核心设计理念

2. **查看README.md**：了解完整的使用说明

3. **查看Skills定义**：
   - `sea-gen-testcases/.claude/skills/clean-requirement/SKILL.md`
   - `sea-gen-testcases/.claude/skills/gen-test-case/SKILL.md`

4. **开始测试**：
   ```bash
   # 在sea-gen-testcases/目录下执行
   clean-requirement --input "requirements/#77879 海运系统添加直达中转字段"
   ```

5. **如果有问题**：提醒Claude Code查看`sea-gen-testcases.md`恢复上下文

---

## 附录：用户反馈的关键点

1. **"测试步骤是独立的测试点"**
   - 用户："这个用例有个与众不同的地方, 就是它一条测试用例中, 有很多测试步骤, 这些步骤更像是要测哪些功能点, 而并非完成一个动作要几步走"

2. **"只做功能测试"**
   - 用户："关于测试类型, 事实上我在工作中只会写一种, 就是功能测试"

3. **"不写前置条件"**
   - 用户："我不喜欢写前提条件, 如果必须要写, 我一般直接写在测试步骤里"

4. **"模块层级手动调整"**
   - 用户："关于几级模块, 这个本质上是一种目录索引, 我不确定最终把这个用例放在哪个目录下"

5. **"开发的技术文档质量不稳定"**
   - 用户："开发写的技术文档, 不仅风格严重不统一, 而且有效的信息也不太多"
   - 解决方案：创建专门的`表结构变更.md`文件

---

**文档结束**

下次对话时，可以直接说："继续cc-skills-dev工作空间"或"继续sea-gen-testcases项目"，或者"查看context-guide.md恢复上下文"，Claude Code就能理解上下文。
