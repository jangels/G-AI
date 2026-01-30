#!/bin/bash

# G-AI 项目停止脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# PID 文件
BACKEND_PID_FILE="/tmp/g-ai-backend.pid"
FRONTEND_PID_FILE="/tmp/g-ai-frontend.pid"

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 停止服务
stop_service() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            print_info "停止 $service_name (PID: $pid)..."
            kill $pid 2>/dev/null || true
            sleep 1
            # 强制杀死（如果还在运行）
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid 2>/dev/null || true
            fi
            print_success "$service_name 已停止"
        else
            print_warning "$service_name 未运行"
        fi
        rm -f "$pid_file"
    else
        print_warning "$service_name PID 文件不存在，可能未运行"
    fi
}

echo ""
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   停止 G-AI 项目服务                  ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

stop_service "后端服务" "$BACKEND_PID_FILE"
stop_service "前端服务" "$FRONTEND_PID_FILE"

# 清理端口（如果还有进程占用）
print_info "清理端口占用..."
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

print_success "所有服务已停止"
echo ""
