# G-AI 统一意图接口文档

## 核心理念

**所有操作都抽象为"意图"**，通过单一的 `/api/v1/beg` 接口处理所有需求。

## 接口地址

```
POST /api/v1/beg
```

## 请求模型

```json
{
  "user_intent": "用户的自然语言意图描述",
  "intent_type": "意图类型/模块",
  "action": "操作类型",
  "data": { "业务数据" },
  "filters": { "查询筛选" },
  "budget": "预算（可选）",
  "platform": "分发平台（可选）"
}
```

## 参数说明

### intent_type (意图类型)

- `goods` - 丐物（商品需求）
- `codes` - 丐码（数字资产）
- `knowledge` - 丐知（知识悬赏）
- `companions` - 丐伴（AI伴侣）
- `prompts` - 丐咒（Prompt市场）
- `console` - 丐帮（控制台）
- `copy` - 纯文案生成（默认）

### action (操作类型)

- `list` - 查询列表
- `get` - 获取详情
- `create` - 创建
- `update` - 更新
- `delete` - 删除
- `join` - 加入（goods专用）
- `rent` - 租用（codes专用）
- `claim` - 认领（knowledge专用）
- `solve` - 解决（knowledge专用）
- `purchase` - 购买（prompts专用）
- `generate` - 生成文案（copy专用，默认）

## 使用示例

### 1. 生成乞讨文案（原始功能）

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想买个便宜的iPhone",
    "intent_type": "copy",
    "action": "generate",
    "budget": "2000元"
  }'
```

### 2. 查询商品需求列表

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想查看所有商品需求",
    "intent_type": "goods",
    "action": "list",
    "filters": {"status": "GATHERING"}
  }'
```

### 3. 创建商品需求

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想发起一个iPhone团购需求",
    "intent_type": "goods",
    "action": "create",
    "data": {
      "item_name": "iPhone 15 Pro",
      "market_price": 7999,
      "target_price": 6500,
      "target_users": 1000
    }
  }'
```

### 4. 加入商品需求

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我要加入这个需求",
    "intent_type": "goods",
    "action": "join",
    "data": {"id": 1}
  }'
```

### 5. 查询数字资产列表

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想看看有什么数字资产可以租",
    "intent_type": "codes",
    "action": "list"
  }'
```

### 6. 租用数字资产

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我要租用Netflix账号",
    "intent_type": "codes",
    "action": "rent",
    "data": {"id": 1}
  }'
```

### 7. 查询知识悬赏

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想看看有什么悬赏可以接",
    "intent_type": "knowledge",
    "action": "list",
    "filters": {"search": "Rust"}
  }'
```

### 8. 创建知识悬赏

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想发布一个技术问题悬赏",
    "intent_type": "knowledge",
    "action": "create",
    "data": {
      "title": "如何在 Rust 中优化 WebAssembly？",
      "description": "处理大文件时内存占用过高",
      "reward_amount": 200.0
    }
  }'
```

### 9. 查询Prompt列表

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想找一些Midjourney的Prompt",
    "intent_type": "prompts",
    "action": "list",
    "filters": {"search": "Midjourney"}
  }'
```

### 10. 购买Prompt

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我要购买这个Prompt",
    "intent_type": "prompts",
    "action": "purchase",
    "data": {"id": 1}
  }'
```

### 11. 查询控制台统计

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想查看系统统计",
    "intent_type": "console",
    "action": "stats"
  }'
```

## 响应模型

```json
{
  "success": true,
  "intent_type": "goods",
  "action": "list",
  "data": [ ... ],
  "copy": { ... },  // 仅当 intent_type="copy" 时存在
  "error": null,
  "message": "找到 10 个需求",
  "timestamp": "2026-01-27T16:30:00"
}
```

## 架构优势

1. **统一接口** - 所有操作都通过一个接口
2. **意图驱动** - 自然语言描述 + 结构化参数
3. **易于扩展** - 新增模块只需添加路由处理器
4. **类型安全** - 使用 Pydantic 进行数据验证
5. **灵活查询** - 支持筛选和搜索

## 注意事项

- 当前使用内存存储，重启后数据会丢失（生产环境应使用数据库）
- `user_intent` 字段主要用于日志和AI处理，业务逻辑主要依赖 `intent_type` 和 `action`
- 所有操作都是异步的，支持高并发
