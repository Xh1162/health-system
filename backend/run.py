import os
from dotenv import load_dotenv
from app import create_app
from flask_migrate import Migrate
from app.models import db

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'development'))
migrate = Migrate(app, db)

if __name__ == '__main__':
    port = 5006  # 直接设置端口为5006
    print(f"启动Flask服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)