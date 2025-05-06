import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from datetime import timedelta
from .models import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 初始化扩展
jwt = JWTManager()
migrate = Migrate()

def create_app(test_config=None):
    """
    应用工厂函数
    
    Args:
        test_config: 测试配置，默认为None
        
    Returns:
        Flask应用实例
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # 配置数据库
    # !!! 注释掉下面这行，让配置从 config.py 加载 !!!
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///health_system.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Add SQLALCHEMY_ECHO = True for debugging SQL queries
    
    # 配置JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # 配置上传文件夹
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/uploads')
    
    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 配置CORS，完全开放，解决预检请求问题
    CORS(app, 
         origins=["http://localhost:3005", "http://localhost:3006", "*"],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         expose_headers=["Content-Type", "Authorization"],
         supports_credentials=False,
         max_age=86400,  # 预检请求缓存24小时
         automatic_options=True)  # 自动处理OPTIONS请求
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 配置JWT
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        print(f"用户身份加载器: {user}")
        return user
        
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from .models.user import User
        identity = jwt_data["sub"]
        print(f"用户查找回调: {identity}")
        return User.query.filter_by(id=identity).one_or_none()
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"令牌已过期: {jwt_payload}")
        return {
            'success': False,
            'message': '令牌已过期，请重新登录'
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        print(f"无效的令牌: {error_string}")
        return {
            'success': False,
            'message': f'无效的令牌: {error_string}'
        }, 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        print(f"缺少令牌: {error_string}")
        return {
            'success': False,
            'message': '缺少令牌'
        }, 401
    
    # 导入并注册错误处理器
    from .utils.errors import register_error_handlers
    register_error_handlers(app)
    
    # 导入蓝图
    from .routes.auth import auth_bp
    from .routes.records import records_bp
    from .routes.reports import reports_bp
    from .routes.user import user_bp
    from .routes.admin import admin_bp
    from .routes.admin_api import admin_api_bp
    from .routes.suggestions import suggestions_bp
    from .routes.advice import advice_bp
    from .routes.admin_advice import admin_advice_bp
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_api_bp)
    app.register_blueprint(suggestions_bp, url_prefix='/api/suggestions')
    app.register_blueprint(advice_bp, url_prefix='/api/advice-requests')
    app.register_blueprint(admin_advice_bp)
    
    # 配置前端静态文件
    frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend/dist')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(frontend_dist_path, path)):
            return send_from_directory(frontend_dist_path, path)
        return send_from_directory(frontend_dist_path, 'index.html')
    
    # 添加静态文件服务
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # 添加默认头像路由
    @app.route('/default-avatar.png')
    def default_avatar():
        # 打印调试信息
        print("请求默认头像")
        try:
            # 确保上传文件夹存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # 检查默认头像文件是否存在
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'default-avatar.png')
            if not os.path.exists(avatar_path):
                # 如果不存在，创建一个空文件
                with open(avatar_path, 'wb') as f:
                    f.write(b'')
                print(f"创建了默认头像文件: {avatar_path}")
            
            return send_from_directory(app.config['UPLOAD_FOLDER'], 'default-avatar.png')
        except Exception as e:
            print(f"提供默认头像时出错: {str(e)}")
            # 返回一个简单的响应，避免500错误
            return "", 200
    
    # 创建数据库表
    with app.app_context():
        # 按照依赖关系顺序导入模型
        from .models.user import User, UserProfile
        from .models.record import Record
        from .models.report import Report, Recommendation
        from .models.admin import SystemSetting, Announcement, ActivityLog
        from .models.manual_suggestion import ManualSuggestion
        from .models.food import FoodItem
        
        # 创建表
        db.create_all()
        
        # 创建初始管理员用户
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print('已创建初始管理员用户')
    
    return app 