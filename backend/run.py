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
    with app.app_context():
        db.create_all()  # 创建数据库表
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5001)), debug=True)