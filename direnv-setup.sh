#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}配置direnv自动激活虚拟环境...${NC}"

# 检查是否安装了direnv
if ! command -v direnv &> /dev/null; then
    echo -e "${YELLOW}安装direnv...${NC}"
    brew install direnv
fi

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 创建.envrc文件
cat > "$SCRIPT_DIR/.envrc" << EOF
# 自动激活虚拟环境
if [ -d "$SCRIPT_DIR/backend/venv" ]; then
    source_env "$SCRIPT_DIR/backend/venv/bin/activate"
    echo "已激活健康系统虚拟环境"
fi

# 设置常用别名
alias backend="cd $SCRIPT_DIR/backend"
alias frontend="cd $SCRIPT_DIR/frontend"
alias start-b="$SCRIPT_DIR/start-backend.sh"
alias start-f="$SCRIPT_DIR/start-frontend.sh"

# 使Python命令可用
export PATH="$SCRIPT_DIR/backend/venv/bin:\$PATH"
EOF

# 允许direnv使用这个目录
direnv allow "$SCRIPT_DIR"

# 检查shell配置
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo -e "${YELLOW}未找到 .zshrc 或 .bashrc，请手动配置${NC}"
    exit 1
fi

# 检查配置是否已存在
if grep -q "eval \"\$(direnv hook" "$SHELL_RC"; then
    echo -e "${YELLOW}direnv配置已存在${NC}"
else
    # 添加direnv钩子到shell配置
    echo 'eval "$(direnv hook zsh)"' >> "$SHELL_RC"
    echo -e "${GREEN}direnv配置已添加到 $SHELL_RC${NC}"
    echo -e "${YELLOW}请执行以下命令使配置生效：${NC}"
    echo -e "source $SHELL_RC"
fi

echo -e "${GREEN}完成！${NC}"
echo -e "现在，每当您进入 ${YELLOW}$SCRIPT_DIR${NC} 或其子目录时，虚拟环境将自动激活。"
echo -e "您还可以使用以下别名:"
echo -e "  ${YELLOW}backend${NC} - 进入后端目录"
echo -e "  ${YELLOW}frontend${NC} - 进入前端目录"
echo -e "  ${YELLOW}start-b${NC} - 启动后端服务器"
echo -e "  ${YELLOW}start-f${NC} - 启动前端服务器" 