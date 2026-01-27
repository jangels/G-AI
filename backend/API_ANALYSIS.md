# 前端页面 API 需求分析

## 各页面功能需求

### 1. **goods.html** (丐物 - 商品需求)
**需要的 API:**
- `GET /api/v1/goods/demands` - 获取需求列表（带状态筛选）
- `POST /api/v1/goods/demands` - 创建新需求
- `POST /api/v1/goods/demands/{id}/join` - 加入需求（更新人数）
- `GET /api/v1/goods/demands/{id}` - 获取单个需求详情

**数据操作:**
- 查询（列表、详情）
- 创建（新需求）
- 更新（加入人数、状态）

---

### 2. **codes.html** (丐码 - 数字资产)
**需要的 API:**
- `GET /api/v1/codes/assets` - 获取资产列表（可用性筛选）
- `POST /api/v1/codes/assets/{id}/rent` - 租用资产
- `GET /api/v1/codes/assets/{id}` - 获取资产详情
- `GET /api/v1/codes/assets/{id}/status` - 查询租用状态/倒计时

**数据操作:**
- 查询（列表、详情、状态）
- 创建（租用记录）
- 更新（资产状态、倒计时）

---

### 3. **knowledge.html** (丐知 - 知识悬赏)
**需要的 API:**
- `GET /api/v1/knowledge/bounties` - 获取悬赏列表（搜索、筛选）
- `POST /api/v1/knowledge/bounties` - 创建悬赏
- `POST /api/v1/knowledge/bounties/{id}/claim` - 认领悬赏
- `POST /api/v1/knowledge/bounties/{id}/solve` - 提交解决方案
- `GET /api/v1/knowledge/bounties/{id}` - 获取悬赏详情

**数据操作:**
- 查询（列表、搜索、详情）
- 创建（悬赏、认领记录）
- 更新（状态、奖励发放）

---

### 4. **companions.html** (丐伴 - AI伴侣)
**需要的 API:**
- `GET /api/v1/companions` - 获取伴侣列表（类型筛选）
- `POST /api/v1/companions` - 创建自定义伴侣
- `GET /api/v1/companions/{id}` - 获取伴侣详情
- `PUT /api/v1/companions/{id}/status` - 更新状态（ONLINE/BUSY/OFFLINE）

**数据操作:**
- 查询（列表、详情）
- 创建（新伴侣）
- 更新（状态）

---

### 5. **prompts.html** (丐咒 - Prompt市场)
**需要的 API:**
- `GET /api/v1/prompts` - 获取Prompt列表（搜索、类型筛选）
- `POST /api/v1/prompts/{id}/purchase` - 购买/解密Prompt
- `POST /api/v1/prompts` - 发布Prompt
- `GET /api/v1/prompts/{id}` - 获取Prompt详情
- `GET /api/v1/user/balance` - 查询用户余额

**数据操作:**
- 查询（列表、搜索、详情、余额）
- 创建（购买记录、新Prompt）
- 更新（使用次数、余额扣减）

---

### 6. **console.html** (丐帮 - 控制台)
**需要的 API:**
- `GET /api/v1/console/stats` - 系统统计（请求数、GMV、Agent状态）
- `GET /api/v1/console/logs` - 实时日志流
- `GET /api/v1/console/dashboard` - 仪表板数据
- `GET /api/v1/console/agents` - Agent状态列表

**数据操作:**
- 查询（统计、日志、状态）
- 实时数据流（WebSocket 或轮询）

---

## 结论：`/beg` 接口无法承接所有需求

### ❌ 单一 `/beg` 接口的局限性：

1. **功能不匹配**
   - `/beg` 是**意图转化接口**（输入需求 → 输出乞讨文案）
   - 前端需要的是**CRUD操作**（查询、创建、更新、删除）

2. **数据操作类型不同**
   - `/beg`: 文本生成（无状态）
   - 前端需求: 数据持久化（有状态）

3. **业务逻辑不同**
   - `/beg`: AI处理（LLM调用）
   - 前端需求: 业务逻辑（状态管理、交易、资源分配）

### ✅ 建议的架构：

```
/beg (核心意图转化)
  ↓
  ├── /goods/* (商品需求 CRUD)
  ├── /codes/* (数字资产 CRUD)
  ├── /knowledge/* (知识悬赏 CRUD)
  ├── /companions/* (AI伴侣 CRUD)
  ├── /prompts/* (Prompt市场 CRUD)
  └── /console/* (控制台查询)
```

### 💡 可能的统一方案（不推荐）：

如果**强制**使用单一接口，需要：

1. **扩展 `/beg` 接口参数**：
```json
{
  "user_intent": "我想买个iPhone",
  "action_type": "goods.create",  // 新增：操作类型
  "module": "goods",              // 新增：模块标识
  "data": { ... }                 // 新增：业务数据
}
```

2. **在 `beggar_brain` 中路由到不同处理逻辑**

**问题：**
- 接口职责不清（违反单一职责原则）
- 难以维护和扩展
- 不符合RESTful设计
- 性能问题（所有请求都走AI处理）

### 🎯 推荐方案：

**保留 `/beg` 作为核心意图转化接口**，同时添加各模块的专用API：

- `/api/v1/beg` - 意图转化（现有）
- `/api/v1/goods/*` - 商品需求模块
- `/api/v1/codes/*` - 数字资产模块
- `/api/v1/knowledge/*` - 知识悬赏模块
- `/api/v1/companions/*` - AI伴侣模块
- `/api/v1/prompts/*` - Prompt市场模块
- `/api/v1/console/*` - 控制台模块

**架构优势：**
- 职责清晰
- 易于维护
- 符合RESTful规范
- 性能优化（按需调用）
- 可独立扩展
