#!/bin/bash

# G-AI 项目启动脚本
# 同时启动前端和后端服务

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 端口配置
BACKEND_PORT=8001
FRONTEND_PORT=8000

# PID 文件
BACKEND_PID_FILE="/tmp/g-ai-backend.pid"
FRONTEND_PID_FILE="/tmp/g-ai-frontend.pid"

# 日志文件
BACKEND_LOG="/tmp/g-ai-backend.log"
FRONTEND_LOG="/tmp/g-ai-frontend.log"

# 打印带颜色的消息
print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        exit 1
    fi
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
        fi
        rm -f "$pid_file"
    fi
}

# 清理函数
cleanup() {
    print_info "正在清理..."
    stop_service "后端服务" "$BACKEND_PID_FILE"
    stop_service "前端服务" "$FRONTEND_PID_FILE"
    exit 0
}

# 捕获退出信号
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║   G-AI (丐要) 项目启动脚本            ║${NC}"
    echo -e "${PURPLE}║   Gathering All Interests              ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════╝${NC}"
    echo ""
    
    # 检查必要的命令
    print_info "检查依赖..."
    check_command "python3"
    check_command "uv" || {
        print_warning "uv 未安装，尝试使用 python3 启动后端..."
    }
    
    # 停止已运行的服务
    print_info "检查并停止已运行的服务..."
    stop_service "后端服务" "$BACKEND_PID_FILE"
    stop_service "前端服务" "$FRONTEND_PID_FILE"
    
    # 检查后端环境
    print_info "检查后端环境..."
    if [ ! -f "$BACKEND_DIR/.env" ]; then
        print_warning ".env 文件不存在，正在从 .env.example 创建..."
        if [ -f "$BACKEND_DIR/.env.example" ]; then
            cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
            print_warning "请编辑 $BACKEND_DIR/.env 文件，填入 GEMINI_API_KEY"
        else
            print_error ".env.example 文件不存在"
            exit 1
        fi
    fi
    
    # 启动后端
    print_info "启动后端服务 (端口: $BACKEND_PORT)..."
    cd "$BACKEND_DIR"
    
    # 检查依赖
    if command -v uv &> /dev/null; then
        print_info "使用 uv 启动后端..."
        nohup uv run python run.py > "$BACKEND_LOG" 2>&1 &
        BACKEND_PID=$!
    else
        print_warning "使用 python3 启动后端（建议安装 uv）..."
        # 检查虚拟环境
        if [ -d "$BACKEND_DIR/.venv" ]; then
            source "$BACKEND_DIR/.venv/bin/activate"
        fi
        nohup python3 run.py > "$BACKEND_LOG" 2>&1 &
        BACKEND_PID=$!
    fi
    
    echo $BACKEND_PID > "$BACKEND_PID_FILE"
    
    # 等待后端启动
    print_info "等待后端服务启动..."
    sleep 3
    
    # 检查后端是否启动成功
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        if curl -s http://127.0.0.1:$BACKEND_PORT/api/v1/health > /dev/null 2>&1; then
            print_success "后端服务启动成功 (PID: $BACKEND_PID)"
        else
            print_warning "后端服务已启动，但健康检查未通过，请检查日志: $BACKEND_LOG"
        fi
    else
        print_error "后端服务启动失败，请检查日志: $BACKEND_LOG"
        exit 1
    fi
    
    # 启动前端
    print_info "启动前端服务 (端口: $FRONTEND_PORT)..."
    cd "$FRONTEND_DIR"
    
    # 检查 Python HTTP 服务器
    nohup python3 -m http.server $FRONTEND_PORT > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
    
    # 等待前端启动
    sleep 2
    
    # 检查前端是否启动成功
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_success "前端服务启动成功 (PID: $FRONTEND_PID)"
    else
        print_error "前端服务启动失败，请检查日志: $FRONTEND_LOG"
        exit 1
    fi
    
    # 显示服务信息
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   服务启动成功！                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}后端 API:${NC}  http://127.0.0.1:$BACKEND_PORT"
    echo -e "${CYAN}API 文档:${NC}  http://127.0.0.1:$BACKEND_PORT/docs"
    echo -e "${CYAN}前端页面:${NC}  http://127.0.0.1:$FRONTEND_PORT"
    echo ""
    echo -e "${YELLOW}日志文件:${NC}"
    echo -e "  后端: $BACKEND_LOG"
    echo -e "  前端: $FRONTEND_LOG"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
    echo ""
    
    # 保持脚本运行
    while true; do
        # 检查服务是否还在运行
        if [ -f "$BACKEND_PID_FILE" ]; then
            BACKEND_PID=$(cat "$BACKEND_PID_FILE")
            if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
                print_error "后端服务意外停止"
                cleanup
            fi
        fi
        
        if [ -f "$FRONTEND_PID_FILE" ]; then
            FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
            if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
                print_error "前端服务意外停止"
                cleanup
            fi
        fi
        
        sleep 5
    done
}

# 运行主函数
main
