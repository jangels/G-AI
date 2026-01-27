# G-AI (丐要) - Gathering All Interests

**Web 4.0 时代全球首款纯 AI Agentic 意图分发网络**

> SKILL IS DEAD. LONG LIVE GAI.  
> To Skill is to Beg.  
> 卑微地要,高傲地活. Begging-as-a-Service

## 🎯 项目简介

G-AI 是一个基于 AI 意图分发的网络平台，将用户的"体面需求"转化为"赛博乞讨文案"，并通过统一的意图接口处理所有业务逻辑。

## 🏗️ 项目结构

```
G-AI/
├── frontend/          # 前端页面
│   ├── index.html    # 主页
│   ├── goods.html    # 丐物（商品需求）
│   ├── codes.html    # 丐码（数字资产）
│   ├── knowledge.html # 丐知（知识悬赏）
│   ├── companions.html # 丐伴（AI伴侣）
│   ├── prompts.html  # 丐咒（Prompt市场）
│   └── console.html   # 丐帮（控制台）
├── backend/          # 后端 API
│   ├── app/
│   │   ├── main.py   # FastAPI 应用
│   │   ├── core/     # 核心配置
│   │   ├── models/   # 数据模型
│   │   ├── services/ # 业务逻辑
│   │   └── api/      # API 路由
│   └── run.py        # 启动脚本
└── docker-compose.yml
```

## 🚀 快速开始

### 后端启动

```bash
cd backend

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 GEMINI_API_KEY

# 启动服务
uv run python run.py
```

服务将在 `http://127.0.0.1:8001` 启动

### 前端访问

直接在浏览器中打开 `frontend/index.html` 或使用本地服务器：

```bash
cd frontend
python -m http.server 8000
```

访问 `http://localhost:8000`

## 📡 API 文档

### 统一意图接口

所有操作都通过 `/api/v1/beg` 接口处理：

```bash
POST /api/v1/beg
Content-Type: application/json

{
  "user_intent": "用户的自然语言意图",
  "intent_type": "goods|codes|knowledge|companions|prompts|console|copy",
  "action": "list|get|create|update|delete|join|rent|claim|solve|purchase|generate",
  "data": { ... },
  "filters": { ... }
}
```

详细文档请查看：
- [统一意图接口文档](backend/INTENT_API.md)
- [API 分析](backend/API_ANALYSIS.md)

## 🤖 AI 集成

项目集成了 Google Gemini AI 用于生成"赛博乞讨"文案。

- [Gemini 集成文档](backend/GEMINI_INTEGRATION.md)
- [环境变量配置](backend/ENV_SETUP.md)

## 🎨 功能模块

### 0x01 丐物 (Goods)
反向供应链 - 聚集用户力量降低商品价格

### 0x02 丐码 (Codes)
数字资产池 - 共享账号/API/许可证

### 0x03 丐知 (Knowledge)
知识悬赏系统 - 发布问题，悬赏解答

### 0x04 丐伴 (Companions)
AI 伴侣服务 - 陪伴、咨询、游戏陪玩

### 0xCORE 丐咒 (Prompts)
Prompt 市场 - 购买/出售高质量 Prompt

### 0xADM 丐帮 (Console)
管理控制台 - 系统监控和统计

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代 Python Web 框架
- **Pydantic** - 数据验证
- **Google Gemini AI** - LLM 集成
- **Uvicorn** - ASGI 服务器

### 前端
- 纯 HTML/CSS/JavaScript
- 赛博朋克风格 UI

## 📝 开发文档

- [后端启动指南](backend/START.md)
- [统一意图架构](backend/UNIFIED_INTENT.md)
- [环境变量配置](backend/ENV_SETUP.md)

## 🔒 安全说明

- API Key 存储在 `.env` 文件中，不会提交到代码仓库
- 确保 `.env` 文件在 `.gitignore` 中

## 📄 许可证

Copyright © 2026 G-AI CORP

## 🙏 致谢

> BEG SMART, LIVE PROUD.
