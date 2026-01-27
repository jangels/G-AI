# 统一意图接口架构

## ✅ 已完成重构

所有前端需求已抽象为"意图"，统一通过 `/api/v1/beg` 接口处理。

## 核心设计

### 1. 统一的请求模型

```python
{
  "user_intent": "自然语言描述",
  "intent_type": "模块类型",
  "action": "操作类型",
  "data": { "业务数据" },
  "filters": { "查询筛选" }
}
```

### 2. 意图类型 (intent_type)

- `goods` - 丐物（商品需求）
- `codes` - 丐码（数字资产）
- `knowledge` - 丐知（知识悬赏）
- `companions` - 丐伴（AI伴侣）
- `prompts` - 丐咒（Prompt市场）
- `console` - 丐帮（控制台）
- `copy` - 纯文案生成

### 3. 操作类型 (action)

- `list` - 查询列表
- `get` - 获取详情
- `create` - 创建
- `update` - 更新
- `delete` - 删除
- `join` - 加入（goods）
- `rent` - 租用（codes）
- `claim` - 认领（knowledge）
- `solve` - 解决（knowledge）
- `purchase` - 购买（prompts）
- `stats` - 统计（console）
- `logs` - 日志（console）
- `generate` - 生成文案（copy）

## 测试结果

### ✅ 文案生成
```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -d '{"user_intent":"我想买个iPhone","intent_type":"copy","action":"generate"}'
```
**结果**: ✅ 成功生成文案

### ✅ 商品列表查询
```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -d '{"user_intent":"查看商品需求","intent_type":"goods","action":"list"}'
```
**结果**: ✅ 成功返回商品列表

### ✅ 控制台统计
```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -d '{"user_intent":"查看统计","intent_type":"console","action":"stats"}'
```
**结果**: ✅ 成功返回统计数据

## 架构优势

1. **单一接口** - 所有操作统一入口
2. **意图驱动** - 自然语言 + 结构化参数
3. **易于扩展** - 新增模块只需添加路由处理器
4. **类型安全** - Pydantic 验证
5. **灵活查询** - 支持筛选和搜索

## 文件结构

```
backend/app/
├── models/
│   └── schemas.py          # 统一的请求/响应模型
├── services/
│   ├── beggar_brain.py     # 意图处理引擎（入口）
│   └── intent_router.py    # 意图路由器（分发逻辑）
└── api/
    └── routes.py           # 单一 /beg 接口
```

## 下一步

- [ ] 添加数据库持久化（当前使用内存存储）
- [ ] 接入真实 LLM API（当前为 Mock）
- [ ] 添加用户认证
- [ ] 添加更多业务逻辑验证
- [ ] 性能优化和缓存

## 使用示例

详见 `INTENT_API.md`
