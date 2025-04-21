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
VENV_PYTHON="$BACKEND_DIR/venv/bin/python"

echo -e "${GREEN}配置全局Python命令...${NC}"
echo -e "=================================="

# 检查虚拟环境是否存在
if [ ! -f "$VENV_PYTHON" ]; then
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

# 创建一个python启动器脚本
echo -e "${YELLOW}创建Python启动器脚本...${NC}"
mkdir -p "$HOME/bin" 2>/dev/null

cat > "$HOME/bin/python-health" << EOF
#!/bin/bash
# 这是健康系统的Python启动器
source "$VENV_ACTIVATE"
python "\$@"
EOF

chmod +x "$HOME/bin/python-health"

# 设置shell配置
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo -e "${RED}未找到 .zshrc 或 .bashrc，无法设置PATH${NC}"
    exit 1
fi

# 检查PATH设置是否已存在
if grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_RC"; then
    echo -e "${YELLOW}PATH设置已存在${NC}"
else
    # 添加PATH到shell配置
    echo '# 健康系统Python路径' >> "$SHELL_RC"
    echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
    echo -e "${GREEN}PATH设置已添加到 $SHELL_RC${NC}"
fi

# 创建别名
if grep -q "alias python-run=" "$SHELL_RC"; then
    echo -e "${YELLOW}python-run别名已存在${NC}"
else
    # 添加别名到shell配置
    echo '# 健康系统Python别名' >> "$SHELL_RC"
    echo "alias python-run='cd $BACKEND_DIR && python-health run.py'" >> "$SHELL_RC"
    echo -e "${GREEN}python-run别名已添加到 $SHELL_RC${NC}"
fi

echo -e "\n${GREEN}配置完成！${NC}"
echo -e "${YELLOW}请执行以下命令使配置生效：${NC}"
echo -e "source $SHELL_RC"

echo -e "\n${GREEN}使用方法:${NC}"
echo -e "1. 使用 ${YELLOW}python-health${NC} 命令可以在任何目录直接使用健康系统的Python"
echo -e "   例如: ${YELLOW}python-health -c \"print('hello')\"${NC}"
echo -e ""
echo -e "2. 使用 ${YELLOW}python-run${NC} 命令可以在任何目录直接启动后端"
echo -e "   例如: ${YELLOW}python-run${NC}" 