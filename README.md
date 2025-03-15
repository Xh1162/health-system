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

## 安装与运行

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 后端

```bash
cd backend
npm install
node server.js
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
│   └── middleware/     # 中间件
└── public/             # 公共资源
    └── uploads/        # 上传文件存储
```

## 许可证

MIT 