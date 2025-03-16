# 健康管理系统

一个现代化的健康管理系统，帮助用户记录和分析健康数据，提供个性化健康建议。

## 功能特点

- 用户认证与个人资料管理
- 健康数据记录（饮食、运动、心情、健康状况）
- 数据可视化与分析报告
- 个性化健康建议
- 响应式设计，支持移动端和桌面端

## 技术栈

### 前端
- Vue.js 3
- Vite
- Element Plus
- Axios

### 后端
- Node.js
- Express
- JWT认证
- Flask (Python后端API服务)
- SQLAlchemy (ORM框架)
- MongoDB (NoSQL数据库)

## 安装与运行

### 前端

```bash
cd frontend
npm install
npm run dev
```

### Node.js后端

```bash
cd backend
npm install
node server.js
```

### Flask后端 (可选)

```bash
cd backend
pip install -r requirements.txt
python run.py
```

## 项目结构

```
health_system/
├── frontend/           # 前端代码
│   ├── public/         # 静态资源
│   └── src/            # 源代码
│       ├── api/        # API请求
│       ├── assets/     # 资源文件
│       ├── components/ # 组件
│       ├── router/     # 路由
│       ├── stores/     # 状态管理
│       └── views/      # 页面
├── backend/            # 后端代码
│   ├── models/         # 数据模型
│   ├── routes/         # 路由
│   ├── middleware/     # 中间件
│   ├── app/            # Flask应用
│   │   ├── models/     # Flask数据模型
│   │   ├── routes/     # Flask路由
│   │   ├── services/   # 业务逻辑服务
│   │   └── utils/      # 工具函数
│   └── run.py          # Flask启动脚本
└── public/             # 公共资源
    └── uploads/        # 上传文件存储
```

## 许可证

MIT 