#!/bin/bash

# G-AI 前端启动脚本（仅启动前端）

set -e

# 颜色定义
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
FRONTEND_PORT=8000
FRONTEND_PID_FILE="/tmp/g-ai-frontend.pid"
FRONTEND_LOG="/tmp/g-ai-frontend.log"

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 停止已运行的服务
if [ -f "$FRONTEND_PID_FILE" ]; then
    pid=$(cat "$FRONTEND_PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        print_info "停止已运行的前端服务..."
        kill $pid 2>/dev/null || true
        sleep 1
        rm -f "$FRONTEND_PID_FILE"
    fi
fi

# 启动前端
print_info "启动前端服务..."
cd "$FRONTEND_DIR"

nohup python3 -m http.server $FRONTEND_PORT > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!

echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

sleep 2

if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    print_success "前端服务启动成功 (PID: $FRONTEND_PID)"
    echo "前端: http://127.0.0.1:$FRONTEND_PORT"
    echo "日志: $FRONTEND_LOG"
else
    echo "前端服务启动失败，请检查日志: $FRONTEND_LOG"
    exit 1
fi
