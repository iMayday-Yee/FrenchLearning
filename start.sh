#!/bin/bash

# 法语学习助手 - 一键启动脚本
# 支持 Linux 和 macOS

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}法语学习助手 - 启动脚本${NC}"
echo "============================================"

# 检查系统依赖
check_dependencies() {
    echo -e "${YELLOW}检查系统依赖...${NC}"

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python3 未安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python3 已安装${NC}"

    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}✗ Node.js 未安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Node.js 已安装${NC}"

    # 检查 FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "${YELLOW}! FFmpeg 未安装，某些功能可能受限${NC}"
    else
        echo -e "${GREEN}✓ FFmpeg 已安装${NC}"
    fi
}

# 启动后端
start_backend() {
    echo -e "${YELLOW}启动后端服务...${NC}"
    cd "$BACKEND_DIR"

    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "创建 Python 虚拟环境..."
        python3 -m venv venv
    fi

    # 激活虚拟环境
    source venv/bin/activate

    # 安装依赖
    if [ -f "requirements.txt" ]; then
        echo "安装后端依赖..."
        pip install -q -r requirements.txt
    fi

    # 启动应用
    echo "启动 Flask 应用..."
    nohup python3 app.py > /tmp/flask.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}✓ 后端已启动 (PID: $BACKEND_PID)${NC}"

    # 等待服务启动
    sleep 2
}

# 启动前端
start_frontend() {
    echo -e "${YELLOW}启动前端应用...${NC}"
    cd "$FRONTEND_DIR"

    # 安装依赖
    if [ ! -d "node_modules" ]; then
        echo "安装前端依赖..."
        npm install -q
    fi

    # 启动 Vite 开发服务器
    echo "启动 Vite 开发服务器..."
    nohup npm run dev > /tmp/vite.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ 前端已启动 (PID: $FRONTEND_PID)${NC}"

    # 等待服务启动
    sleep 2
}

# 显示启动信息
show_info() {
    echo ""
    echo "============================================"
    echo -e "${GREEN}服务已启动！${NC}"
    echo "============================================"
    echo ""
    echo "前端应用: ${GREEN}http://localhost:3000${NC}"
    echo "后端 API: ${GREEN}http://localhost:5000${NC}"
    echo ""
    echo "日志文件:"
    echo "  后端: /tmp/flask.log"
    echo "  前端: /tmp/vite.log"
    echo ""
    echo "停止服务:"
    echo "  pkill -f 'python3 app.py'  # 停止后端"
    echo "  pkill -f 'npm run dev'     # 停止前端"
    echo ""
    echo "查看日志:"
    echo "  tail -f /tmp/flask.log  # 查看后端日志"
    echo "  tail -f /tmp/vite.log   # 查看前端日志"
    echo ""
}

# 主流程
main() {
    check_dependencies
    echo ""
    start_backend
    echo ""
    start_frontend
    echo ""
    show_info

    # 保持脚本运行
    echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
    wait
}

# 信号处理
cleanup() {
    echo ""
    echo -e "${YELLOW}正在停止服务...${NC}"
    pkill -f "python3 app.py" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    echo -e "${GREEN}✓ 服务已停止${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 执行主流程
main
