#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到后端目录
cd "$SCRIPT_DIR/backend"

# 检查虚拟环境是否存在并激活
if [ -f "venv/bin/activate" ]; then
    echo "正在激活虚拟环境..."
    source venv/bin/activate
else
    echo "错误：虚拟环境未找到，请先运行 ./setup.sh 配置环境"
    exit 1
fi

# 启动Flask应用
echo "启动后端服务器..."
python run.py || python3 run.py 