# 健康生活系统环境配置指南

这个仓库包含一个基于Flask和Vue.js的健康生活管理系统。下面提供了使用脚本快速配置环境的方法。

## 快速开始

### 一键启动（最简单方法）

我们提供了一个简单的交互式脚本来启动系统：

```bash
# 给脚本添加执行权限
chmod +x quick-start.sh

# 运行快速启动脚本
./quick-start.sh
```

脚本会引导您完成以下操作：
1. 检查环境是否配置好，如果没有会提示您配置
2. 让您选择启动后端、前端或两者一起启动
3. 自动处理虚拟环境激活和目录切换

这是最简单、最推荐的使用方式！

### 全局Python命令（推荐）

如果您想在任何目录下都能使用`python`命令启动后端，我们提供了一个专门的配置脚本：

```bash
# 给脚本添加执行权限
chmod +x python-everywhere.sh

# 运行配置脚本
./python-everywhere.sh

# 使配置生效
source ~/.zshrc  # 如果使用zsh
# 或
source ~/.bashrc  # 如果使用bash
```

配置完成后，您将获得两个新命令：

1. `python-health` - 在任何目录下使用项目的Python环境
   ```bash
   python-health -c "print('hello')"
   ```

2. `python-run` - 在任何目录下启动后端服务器
   ```bash
   python-run
   ```

这是最方便的使用方式，不需要手动激活虚拟环境或切换目录！

### 使用自动配置脚本

我们提供了一个自动配置脚本，它将帮助您安装所有必要的依赖并设置环境：

```bash
# 给脚本添加执行权限
chmod +x setup.sh

# 运行安装脚本
./setup.sh
```

脚本将自动：
1. 检查并安装必要的系统依赖（使用Homebrew）
   - Python 3.11
   - Node.js 16
   - Redis
2. 为后端设置Python虚拟环境并安装所有依赖
3. 初始化数据库
4. 为前端安装所有npm依赖

### 自动激活虚拟环境（推荐）

以下提供两种方法配置自动激活虚拟环境，请选择一种适合您的方法：

#### 方法一：使用direnv（更简洁，推荐）

[direnv](https://direnv.net/)是一个优秀的环境管理工具，可以在进入目录时自动加载环境变量和激活虚拟环境。

```bash
# 给脚本添加执行权限
chmod +x direnv-setup.sh

# 运行配置脚本
./direnv-setup.sh

# 使配置生效
source ~/.zshrc  # 如果使用zsh
# 或
source ~/.bashrc  # 如果使用bash
```

配置完成后，您将获得以下便利：
- 进入项目目录时自动激活虚拟环境
- 离开项目目录时自动停用虚拟环境
- 可使用`backend`和`frontend`快速进入对应目录
- 可使用`start-b`和`start-f`快速启动服务

#### 方法二：使用自定义脚本

如果您不想安装额外的工具，也可以使用我们提供的自定义脚本：

```bash
# 给脚本添加执行权限
chmod +x set-auto-activate.sh

# 运行配置脚本
./set-auto-activate.sh

# 使配置生效
source ~/.zshrc  # 如果使用zsh
# 或
source ~/.bashrc  # 如果使用bash
```

配置完成后，每当您进入项目目录或其子目录时，虚拟环境会自动激活；当您离开项目目录时，虚拟环境会自动停用。

### 手动配置

如果您想手动配置环境，请按照以下步骤操作：

#### 系统依赖

- Python 3.8+
- Node.js 16+
- Redis

#### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

#### 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

## 启动应用

配置完成后，您可以按照以下方式启动应用：

### 启动后端

```bash
# 方法1：使用便捷脚本（推荐）
./start-backend.sh

# 方法2：手动启动
cd backend
source venv/bin/activate  # Linux/macOS 【重要！必须先激活虚拟环境】
# venv\Scripts\activate   # Windows
python run.py
```

后端服务将在 http://localhost:5008 运行

### 启动前端

```bash
cd frontend
npm run dev
```

前端将在 http://localhost:3005 运行

## 技术栈

### 后端
- Flask - Python Web框架
- SQLAlchemy - ORM数据库操作
- Flask-JWT - JWT认证
- Flask-CORS - 跨域资源共享
- Redis - 缓存和会话管理

### 前端
- Vue.js - 前端框架
- Vite - 构建工具
- Element Plus - UI组件库
- Axios - HTTP客户端
- ECharts - 数据可视化

## 功能特点

- 用户认证与授权
- 健康数据记录（运动、饮食、心情、健康状况）
- 数据可视化与分析
- 健康报告生成
- 个性化建议

## API文档

API文档位于 `backend/docs` 目录下。

## 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件 

# 创建记录
record = Record(
    user_id=user_id,  # 将记录与当前用户关联
    type=record_type,
    note=data.get('note', ''),
    record_date=datetime.utcnow()
) 

@records_bp.route('/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_record(record_id):
    """删除记录"""
    user_id = get_jwt_identity()
    
    # 查找记录，并验证所有权
    record = Record.query.filter_by(id=record_id, user_id=user_id).first()
    if not record:
        return not_found('记录不存在或无权限')
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': '记录已删除'}) 