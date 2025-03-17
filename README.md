# 健康生活系统

一个基于Flask和Vue.js的健康生活管理系统，帮助用户记录和分析健康数据。

## 功能特点

- 用户认证与授权
- 健康数据记录（运动、饮食、心情、健康状况）
- 数据可视化与分析
- 健康报告生成
- 个性化建议

## 技术栈

### 后端
- Flask - Python Web框架
- SQLAlchemy - ORM数据库操作
- Flask-JWT-Extended - JWT认证
- Flask-CORS - 跨域资源共享

### 前端
- Vue.js - 前端框架
- Vite - 构建工具
- Axios - HTTP客户端
- Chart.js - 数据可视化

## 安装与运行

### 前提条件
- Python 3.8+
- Node.js 16+
- npm 8+

### 后端设置
1. 进入后端目录
   ```
   cd backend
   ```

2. 创建并激活虚拟环境
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖
   ```
   pip install -r requirements.txt
   ```

4. 初始化数据库
   ```
   python init_db.py
   ```

5. 运行后端服务器
   ```
   python run.py
   ```
   服务器将在 http://localhost:5006 运行

### 前端设置
1. 进入前端目录
   ```
   cd frontend
   ```

2. 安装依赖
   ```
   npm install
   ```

3. 运行开发服务器
   ```
   npm run dev
   ```
   前端将在 http://localhost:3005 运行

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