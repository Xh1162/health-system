#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始配置健康生活系统环境...${NC}"

# 检查并安装Homebrew
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}安装Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 检查Python命令
PYTHON_CMD=""
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${YELLOW}通过Homebrew安装Python...${NC}"
    brew install python@3.11
    PYTHON_CMD="python3"
fi
echo -e "${GREEN}使用Python命令: ${PYTHON_CMD} ($(${PYTHON_CMD} --version))${NC}"

# 安装Node.js (如果需要)
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}通过Homebrew安装Node.js...${NC}"
    brew install node@16
else
    echo -e "${GREEN}已安装Node.js $(node --version)${NC}"
fi

# 安装Redis (如果需要)
if ! command -v redis-server &> /dev/null; then
    echo -e "${YELLOW}通过Homebrew安装Redis...${NC}"
    brew install redis
else
    echo -e "${GREEN}已安装Redis${NC}"
fi

# 配置后端环境
echo -e "${GREEN}配置后端环境...${NC}"
cd backend

# 创建Python虚拟环境
${PYTHON_CMD} -m venv venv
source venv/bin/activate

# 安装后端依赖
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# 返回根目录
cd ..

# 配置前端环境
echo -e "${GREEN}配置前端环境...${NC}"
cd frontend

# 安装前端依赖
npm install

# 返回根目录
cd ..

# 创建方便的启动脚本
echo -e "${GREEN}创建便捷启动脚本...${NC}"

# 创建后端启动脚本
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
python run.py
EOF
chmod +x start-backend.sh

# 创建前端启动脚本
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
chmod +x start-frontend.sh

echo -e "${GREEN}环境配置完成!${NC}"
echo -e "${YELLOW}启动后端: ${NC}./start-backend.sh"
echo -e "${YELLOW}启动前端: ${NC}./start-frontend.sh"
echo -e "${YELLOW}注意：${NC}必须先激活虚拟环境才能使用python命令" 