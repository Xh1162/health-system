#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_ACTIVATE="$BACKEND_DIR/venv/bin/activate"

# 打印欢迎信息
echo -e "${GREEN}健康生活系统快速启动器${NC}"
echo -e "=================================="

# 检查虚拟环境是否存在
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo -e "${RED}错误：虚拟环境未找到${NC}"
    echo -e "是否要运行环境配置脚本? (y/n)"
    read -p "> " answer
    if [[ $answer =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}正在运行环境配置脚本...${NC}"
        bash "$SCRIPT_DIR/setup.sh"
    else
        echo -e "${RED}已取消，退出${NC}"
        exit 1
    fi
fi

# 询问用户要启动什么
echo -e "\n${GREEN}请选择要启动的服务:${NC}"
echo -e "1) 后端 (Flask API 服务器)"
echo -e "2) 前端 (Vue.js 开发服务器)"
echo -e "3) 全部 (同时启动前端和后端)"
echo -e "4) 设置Python别名 - 使python命令直接可用"
echo -e "5) 退出"
read -p "> " choice

case $choice in
    1)
        echo -e "${YELLOW}启动后端服务器...${NC}"
        cd "$BACKEND_DIR"
        source "$VENV_ACTIVATE"
        python run.py
        ;;
    2)
        echo -e "${YELLOW}启动前端服务器...${NC}"
        cd "$SCRIPT_DIR/frontend"
        npm run dev
        ;;
    3)
        echo -e "${YELLOW}启动所有服务...${NC}"
        # 在后台启动后端
        echo -e "${GREEN}启动后端服务器...${NC}"
        gnome-terminal --tab -- bash -c "cd \"$BACKEND_DIR\" && source \"$VENV_ACTIVATE\" && python run.py; exec bash" 2>/dev/null || 
        osascript -e "tell application \"Terminal\" to do script \"cd '$BACKEND_DIR' && source '$VENV_ACTIVATE' && python run.py\"" 2>/dev/null || 
        start "Backend" cmd /k "cd /d \"$BACKEND_DIR\" && \"$VENV_ACTIVATE\" && python run.py" 2>/dev/null || 
        xterm -e "cd \"$BACKEND_DIR\" && source \"$VENV_ACTIVATE\" && python run.py" 2>/dev/null || 
        {
            echo -e "${RED}无法在新窗口启动后端，将在后台启动${NC}"
            cd "$BACKEND_DIR"
            source "$VENV_ACTIVATE"
            python run.py &
            BACKEND_PID=$!
            echo -e "${GREEN}后端已在后台启动 (PID: $BACKEND_PID)${NC}"
            sleep 2
        }
        
        # 启动前端
        echo -e "${GREEN}启动前端服务器...${NC}"
        cd "$SCRIPT_DIR/frontend"
        npm run dev
        
        # 如果前端停止，终止后端（如果是在后台启动的）
        if [ -n "$BACKEND_PID" ]; then
            echo -e "${YELLOW}前端已停止，终止后端进程 (PID: $BACKEND_PID)${NC}"
            kill $BACKEND_PID 2>/dev/null
        fi
        ;;
    4)
        echo -e "${YELLOW}设置Python别名，使python命令可以直接使用...${NC}"
        SHELL_RC=""
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_RC="$HOME/.bashrc"
        else
            echo -e "${RED}未找到 .zshrc 或 .bashrc，无法设置别名${NC}"
            exit 1
        fi
        
        # 检查别名是否已存在
        if grep -q "alias python='$BACKEND_DIR/venv/bin/python'" "$SHELL_RC"; then
            echo -e "${YELLOW}Python别名已存在${NC}"
        else
            # 添加Python别名到shell配置
            echo "# 健康系统Python别名" >> "$SHELL_RC"
            echo "alias python='$BACKEND_DIR/venv/bin/python'" >> "$SHELL_RC"
            echo -e "${GREEN}Python别名已添加到 $SHELL_RC${NC}"
            echo -e "${YELLOW}请执行以下命令使配置生效：${NC}"
            echo -e "source $SHELL_RC"
        fi
        
        echo -e "\n${GREEN}现在您可以在任何目录下直接使用 python 命令${NC}"
        echo -e "例如，要启动后端，只需执行："
        echo -e "${YELLOW}cd $BACKEND_DIR && python run.py${NC}"
        ;;
    5)
        echo -e "${YELLOW}退出${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}无效选择，退出${NC}"
        exit 1
        ;;
esac 