import os
from dotenv import load_dotenv
from app import create_app
from flask_migrate import Migrate
from app.models import db

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    # 使用5008端口，避免冲突
    port = 5008
    print(f"启动Flask服务器，端口: {port}")
    
    # 启动应用，允许所有主机访问
    app.run(host='0.0.0.0', port=port, debug=True)