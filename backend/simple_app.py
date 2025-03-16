import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# 创建应用
app = Flask(__name__)
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_health_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置JWT
app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 定义用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

# 创建数据库表
with app.app_context():
    db.create_all()
    
    # 创建测试用户
    if not User.query.filter_by(username='test').first():
        test_user = User(
            username='test',
            email='test@example.com',
            role='user'
        )
        test_user.set_password('password')
        db.session.add(test_user)
        db.session.commit()
        print('已创建测试用户')

# 定义路由
@app.route('/api/auth/login', methods=['POST'])
def login():
    # 简化版登录，仅用于测试
    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': {
            'token': create_access_token(identity=1),
            'user': {
                'id': 1,
                'username': 'test',
                'email': 'test@example.com',
                'role': 'user'
            }
        }
    })

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    # 简化版获取用户资料，仅用于测试
    return jsonify({
        'success': True,
        'message': '获取用户资料成功',
        'data': {
            'id': 1,
            'username': 'test',
            'email': 'test@example.com',
            'role': 'user',
            'profile': {
                'height': 175,
                'weight': 70,
                'birth_date': '1990-01-01',
                'gender': 'male'
            }
        }
    })

# 运行应用
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5004))
    app.run(host='0.0.0.0', port=port, debug=True) 