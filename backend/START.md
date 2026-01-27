# G-AI Backend 启动说明

## 启动方式

### 方式 1: 从 backend 目录启动（推荐）
```bash
cd backend
uv run python run.py
```

### 方式 2: 从项目根目录启动
```bash
# 从项目根目录运行
uv run --directory backend run.py
```

## 验证服务

服务启动后，访问以下端点验证：

1. **健康检查**: http://127.0.0.1:8001/api/v1/health
2. **API 文档**: http://127.0.0.1:8001/docs
3. **测试 API**:
```bash
curl -X POST http://127.0.0.1:8001/api/v1/beg \
  -H "Content-Type: application/json" \
  -d '{"user_intent":"我想买个便宜的iPhone","budget":"2000元"}'
```

## 服务信息

- **端口**: 8001
- **主机**: 127.0.0.1
- **热重载**: 已启用（代码修改自动重启）
