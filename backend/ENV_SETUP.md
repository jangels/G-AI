# 环境变量配置说明

## 📋 配置步骤

### 1. 创建 .env 文件

在 `backend/` 目录下创建 `.env` 文件：

```bash
cd backend
cp .env.example .env
```

### 2. 配置 Gemini API Key

编辑 `.env` 文件，填入你的 Gemini API Key：

```env
GEMINI_API_KEY=your-actual-api-key-here
GEMINI_MODEL=models/gemini-2.5-flash
LLM_PROVIDER=gemini
```

### 3. 验证配置

启动服务后，配置会自动从 `.env` 文件加载。

## 🔒 安全说明

- ✅ `.env` 文件已在 `.gitignore` 中，不会被提交到代码仓库
- ✅ API Key 不会出现在代码中
- ✅ 使用 `.env.example` 作为配置模板

## 📝 环境变量列表

### 必需配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `GEMINI_API_KEY` | Gemini API 密钥 | `AIzaSy...` |

### 可选配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `GEMINI_MODEL` | Gemini 模型名称 | `models/gemini-2.5-flash` |
| `LLM_PROVIDER` | LLM 提供商 | `gemini` |
| `OPENAI_API_KEY` | OpenAI API 密钥（备用） | `sk-placeholder` |
| `OPENAI_MODEL` | OpenAI 模型名称 | `gpt-3.5-turbo` |

## 🚀 启动服务

配置完成后，正常启动服务即可：

```bash
cd backend
uv run python run.py
```

服务会自动从 `.env` 文件读取配置。

## ⚠️ 注意事项

1. **不要提交 .env 文件**：确保 `.env` 在 `.gitignore` 中
2. **API Key 安全**：不要在代码中硬编码 API Key
3. **环境变量优先级**：系统环境变量会覆盖 `.env` 文件中的值
