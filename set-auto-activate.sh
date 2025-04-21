#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_ACTIVATE="$BACKEND_DIR/venv/bin/activate"

echo -e "${GREEN}配置自动激活虚拟环境...${NC}"

# 检查是否存在虚拟环境
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo -e "${YELLOW}错误：虚拟环境未找到，请先运行 ./setup.sh 配置环境${NC}"
    exit 1
fi

# 创建.env文件存储项目路径
echo "HEALTH_SYSTEM_DIR=$SCRIPT_DIR" > "$SCRIPT_DIR/.env"

# 为不同shell添加自动激活配置
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
if grep -q "health-system-auto-activate" "$SHELL_RC"; then
    echo -e "${YELLOW}自动激活配置已存在${NC}"
else
    # 添加自动激活函数到shell配置
    cat >> "$SHELL_RC" << EOF

# health-system-auto-activate
health_cd() {
    # 正常的cd命令
    \cd "\$@"
    
    # 检查当前目录是否是健康系统目录或其子目录
    CURRENT_DIR=\$(pwd)
    if [[ -f ".env" && \$(cat .env | grep HEALTH_SYSTEM_DIR) ]]; then
        # 在项目根目录
        HEALTH_DIR=\$(cat .env | grep HEALTH_SYSTEM_DIR | cut -d= -f2)
        if [ -f "\$HEALTH_DIR/backend/venv/bin/activate" ]; then
            # 如果虚拟环境没有激活，则激活它
            if [[ "\$VIRTUAL_ENV" != "\$HEALTH_DIR/backend/venv" ]]; then
                echo "自动激活健康系统虚拟环境..."
                source "\$HEALTH_DIR/backend/venv/bin/activate"
            fi
        fi
    elif [[ \$CURRENT_DIR == *"health-system"* && -f "$SCRIPT_DIR/.env" ]]; then
        # 在项目子目录
        HEALTH_DIR="$SCRIPT_DIR"
        if [ -f "\$HEALTH_DIR/backend/venv/bin/activate" ]; then
            # 如果虚拟环境没有激活，则激活它
            if [[ "\$VIRTUAL_ENV" != "\$HEALTH_DIR/backend/venv" ]]; then
                echo "自动激活健康系统虚拟环境..."
                source "\$HEALTH_DIR/backend/venv/bin/activate"
            fi
        fi
    else
        # 如果离开项目目录并且虚拟环境已激活，则停用虚拟环境
        if [[ -n "\$VIRTUAL_ENV" && "\$VIRTUAL_ENV" == *"health-system"*/backend/venv ]]; then
            echo "离开健康系统项目，停用虚拟环境..."
            deactivate
        fi
    fi
}

# 替换cd命令
alias cd="health_cd"
EOF

    echo -e "${GREEN}配置已添加到 $SHELL_RC${NC}"
    echo -e "${YELLOW}请执行以下命令使配置生效：${NC}"
    echo -e "source $SHELL_RC"
fi

echo -e "${GREEN}完成！${NC}"
echo -e "现在，每当您进入 ${YELLOW}$SCRIPT_DIR${NC} 或其子目录时，虚拟环境将自动激活。"
echo -e "当您离开此目录树时，虚拟环境将自动停用。" 