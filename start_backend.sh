#!/bin/bash

# G-AI 后端启动脚本（仅启动后端）

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
BACKEND_PORT=8001
BACKEND_PID_FILE="/tmp/g-ai-backend.pid"
BACKEND_LOG="/tmp/g-ai-backend.log"

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 停止已运行的服务
if [ -f "$BACKEND_PID_FILE" ]; then
    pid=$(cat "$BACKEND_PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        print_info "停止已运行的后端服务..."
        kill $pid 2>/dev/null || true
        sleep 1
        rm -f "$BACKEND_PID_FILE"
    fi
fi

# 检查环境
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo -e "${YELLOW}[WARNING]${NC} .env 文件不存在，请先配置"
    exit 1
fi

# 启动后端
print_info "启动后端服务..."
cd "$BACKEND_DIR"

if command -v uv &> /dev/null; then
    nohup uv run python run.py > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
else
    if [ -d "$BACKEND_DIR/.venv" ]; then
        source "$BACKEND_DIR/.venv/bin/activate"
    fi
    nohup python3 run.py > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
fi

echo $BACKEND_PID > "$BACKEND_PID_FILE"

sleep 3

if curl -s http://127.0.0.1:$BACKEND_PORT/api/v1/health > /dev/null 2>&1; then
    print_success "后端服务启动成功 (PID: $BACKEND_PID)"
    echo "API: http://127.0.0.1:$BACKEND_PORT"
    echo "文档: http://127.0.0.1:$BACKEND_PORT/docs"
    echo "日志: $BACKEND_LOG"
else
    echo -e "${YELLOW}[WARNING]${NC} 后端可能未完全启动，请检查日志: $BACKEND_LOG"
fi
