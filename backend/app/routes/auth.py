from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from ..services.auth import AuthService
from ..utils.errors import ValidationError, AuthenticationError, bad_request, unauthorized, not_found
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os
import time
import uuid
from datetime import timedelta

from ..models import db, User, ActivityLog

auth_bp = Blueprint('auth', __name__)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 添加详细日志
    print(f"收到注册请求: {data}")
    
    if not data:
        print("注册失败: 无效的请求数据")
        return bad_request('无效的请求数据')
    
    username = data.get('username')
    password = data.get('password')
    # 邮箱为可选项
    email = data.get('email')
    
    if not username or not password:
        print(f"注册失败: 用户名或密码为空 - username: {username}, password: {'已提供' if password else '未提供'}")
        return bad_request('用户名和密码不能为空')
    
    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"注册失败: 用户名 {username} 已被使用")
        return bad_request('用户名已被使用')
    
    # 如果提供了邮箱，检查是否已存在
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"注册失败: 邮箱 {email} 已被使用")
            return bad_request('邮箱已被使用')
    
    try:
        # 创建新用户
        user = User(username=username)
        user.password = password
        if email:  # 只有在提供邮箱时才设置
            user.email = email
        
        db.session.add(user)
        db.session.commit()
        
        # 记录注册活动
        log = ActivityLog(
            user_id=user.id,
            action='register',
            details={'ip': request.remote_addr},
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        # 生成JWT令牌
        expires = timedelta(hours=24)
        access_token = create_access_token(
            identity=user.id,
            expires_delta=expires
        )
        
        print(f"注册成功: 用户ID {user.id}, 用户名 {username}")
        
        return jsonify({
            'success': True,
            'data': {
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'avatar': user.avatar,
                    'role': user.role
                }
            }
        }), 201
    except Exception as e:
        print(f"注册异常: {str(e)}")
        # 回滚数据库会话
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data:
        return bad_request('无效的请求数据')
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return bad_request('用户名和密码不能为空')
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    # 如果用户不存在，创建测试用户（仅用于开发环境）
    if not user and current_app.config.get('FLASK_ENV') == 'development':
        user = User(username=username)
        user.password = password
        # 不再自动生成邮箱
        db.session.add(user)
        db.session.commit()
    
    # 验证密码
    if not user or not user.verify_password(password):
        return unauthorized('用户名或密码错误')
    
    # 记录登录活动
    log = ActivityLog(
        user_id=user.id,
        action='login',
        details={'ip': request.remote_addr},
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    # 生成JWT令牌
    expires = timedelta(hours=24)
    access_token = create_access_token(
        identity=user.id,
        expires_delta=expires
    )
    
    return jsonify({
        'success': True,
        'data': {
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar,
                'role': user.role
            }
        }
    }) 