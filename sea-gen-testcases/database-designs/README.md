# 数据库设计文档

## 文档说明
本目录存放海运管理系统的数据库表结构设计文档。

## 使用方式
- 需求的`表结构变更.md`中引用这里的基础表结构
- clean-requirement skill会自动读取并合并表结构信息

## 表分类

### 核心业务表
- `公共表设计.md` - 海运单、入库单等核心表
- `编号序列表.md` - 订单组编号序列表

### 上游系统表
- `上游系统表.md` - OSJ、B2B、3PL相关表

### 状态流转表
- `状态流转表.md` - 订单状态流转日志表

## 引用方式

在`表结构变更.md`中这样引用：

```markdown
## 引用表结构
- t_marine_order：见 `database-designs/公共表设计.md`
- t_receipt_order：见 `database-designs/公共表设计.md`
- t_order_group_sequence：见 `database-designs/编号序列表.md`
```

clean-requirement skill会自动读取这些文档并合并完整的表结构信息。
