from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config
from .models import db
from .routes.auth import auth_bp
from .routes.records import records_bp
from .routes.reports import reports_bp
from .routes.user import user_bp

# 初始化扩展
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='development'):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称，默认为'development'
        
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # CORS配置
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS'], 
                                    "methods": app.config['CORS_METHODS'],
                                    "allow_headers": app.config['CORS_ALLOW_HEADERS'],
                                    "supports_credentials": app.config['CORS_SUPPORTS_CREDENTIALS']}})
    
    # 初始化扩展
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
        from .models import User
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
    
    # 注册错误处理器
    from .utils.errors import register_error_handlers
    register_error_handlers(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    return app 