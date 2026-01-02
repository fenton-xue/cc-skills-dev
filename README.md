# CC Skills Dev - Claude Code Skills开发工作空间

这是用于开发和维护Claude Code Agent Skills的工作空间。

## 项目说明

本项目包含完整的Skills开发示例，展示如何为特定业务场景开发Claude Code Agent Skills。当前示例项目是海运系统测试用例自动生成工具。

## 核心Skills

### 1. clean-requirement
将需求文档、表结构变更清洗为结构化的JSON格式

### 2. gen-test-case
将清洗后的需求自动转换为测试用例Excel文件

## 快速开始

本项目包含一个完整的海运系统测试项目，展示了如何使用这些Skills：

```bash
cd sea-gen-testcases

# 1. 执行需求清洗
clean-requirement --input "requirements/#77879 海运系统添加直达中转字段"

# 2. 生成测试用例
gen-test-case --input "cleaned/#77879 海运系统添加直达中转字段-cleaned.json"
```

## 项目结构

```
.
├── sea-gen-testcases/         # 海运系统测试项目（可直接使用）
│   ├── .claude/
│   │   ├── skills/           # Skills定义
│   │   │   ├── clean-requirement/SKILL.md
│   │   │   └── gen-test-case/
│   │   │       ├── SKILL.md
│   │   │       └── scripts/
│   │   │           └── generate_excel.py
│   │   └── CLAUDE.md         # 海运管理系统背景
│   ├── database-designs/     # 通用表结构
│   ├── requirements/         # 需求文档
│   ├── cleaned/              # 清洗后的JSON
│   ├── testcases/            # 生成的Excel
│   └── README.md            # 详细使用说明
│
├── context-guide.md          # 上下文恢复文档
└── README.md                # 本文件
```

## 如何应用到您的项目

复制Skills到您的项目：

```bash
# 1. 在您的测试项目中创建.claude目录
mkdir -p 您的项目/.claude/skills

# 2. 复制Skills
cp -r sea-gen-testcases/.claude/skills/* 您的项目/.claude/skills/

# 3. 参考sea-gen-testcases/README.md配置您的项目
```

## 详细文档

请查看 `sea-gen-testcases/README.md` 了解完整的使用说明、设计理念和最佳实践。

## 上下文恢复

如果需要恢复开发上下文，请查看 `context-guide.md`。

## 许可

MIT License
