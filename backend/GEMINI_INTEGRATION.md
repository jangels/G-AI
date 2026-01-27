# Gemini LLM 集成文档

## ✅ 集成完成

项目已成功集成 Google Gemini AI，用于生成"赛博乞讨"文案。

## 配置

### API Key
- 已配置在 `app/core/config.py` 中
- Key: `AIzaSyAgUmvNiAHbqfsheA4PcztKddLyoK4rWUs`

### 模型
- 默认模型: `models/gemini-2.5-flash`
- 可选模型: `models/gemini-2.5-pro`, `models/gemini-pro-latest`

### 环境变量（可选）

如需通过环境变量配置，可在 `.env` 文件中设置：

```env
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=models/gemini-2.5-flash
LLM_PROVIDER=gemini
```

## 使用方式

### 1. 通过统一意图接口

```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想买个便宜的iPhone，预算2000元",
    "intent_type": "copy",
    "action": "generate",
    "budget": "2000元"
  }'
```

### 2. 响应格式

```json
{
  "success": true,
  "intent_type": "copy",
  "action": "generate",
  "copy": {
    "style": "CYBER_MISERABLE_TECH_BEGGAR",
    "content": "生成的文案内容...",
    "hashtags": ["#赛博乞讨", "#标签1", "#标签2"],
    "skill_confidence": 0.95
  },
  "message": "文案生成成功（由 Gemini AI 生成）"
}
```

## 实现细节

### 文件结构

```
backend/app/services/
├── llm_service.py      # LLM 服务封装
└── intent_router.py    # 意图路由器（调用 LLM 服务）
```

### LLM 服务 (`llm_service.py`)

- `LLMService` 类：封装 Gemini API 调用
- `generate_begging_copy()`: 生成乞讨文案
- 支持 JSON 格式解析和降级处理

### 错误处理

- JSON 解析失败：使用响应文本作为内容
- API 调用失败：降级到默认文案
- 所有错误都有日志记录

## 可用模型列表

通过 API 查询到的可用模型：

- `models/gemini-2.5-flash` ✅ (推荐，快速)
- `models/gemini-2.5-pro` ✅ (更强大)
- `models/gemini-pro-latest` ✅ (最新版本)
- `models/gemini-2.0-flash` ✅
- 更多模型可通过 `genai.list_models()` 查询

## 测试

### 测试命令

```bash
# 测试文案生成
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{
    "user_intent": "我想买个MacBook Pro",
    "intent_type": "copy",
    "action": "generate",
    "budget": "8000元"
  }'
```

### 预期结果

- ✅ 返回真实的 AI 生成文案
- ✅ 包含 style, content, hashtags, skill_confidence
- ✅ 文案风格符合"赛博乞讨"主题

## 依赖

```txt
google-generativeai==0.3.2
```

已添加到 `requirements.txt` 和 `pyproject.toml`

## 注意事项

1. **API Key 安全**: 生产环境应将 API Key 放在 `.env` 文件中，不要提交到代码仓库
2. **速率限制**: Gemini API 有速率限制，注意控制请求频率
3. **成本**: 注意 API 调用成本，建议监控使用量
4. **降级处理**: 如果 API 调用失败，会自动降级到默认文案

## 未来优化

- [ ] 添加请求缓存（相同意图复用结果）
- [ ] 支持流式响应
- [ ] 添加更多提示词模板
- [ ] 支持多语言生成
- [ ] 添加生成质量评估
