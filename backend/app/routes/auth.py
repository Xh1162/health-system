from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from ..services.auth import AuthService
from ..utils.errors import ValidationError, AuthenticationError, bad_request, unauthorized, not_found
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os
import time
import uuid
from datetime import timedelta, datetime

from ..models import db, User, ActivityLog, UserProfile

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
    # email = data.get('email') # Removed email input
    
    if not username or not password:
        print(f"注册失败: 用户名或密码为空 - username: {username}, password: {'已提供' if password else '未提供'}")
        return bad_request('用户名和密码不能为空')
    
    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"注册失败: 用户名 {username} 已被使用")
        return bad_request('用户名已被使用')
    
    # Removed email existence check
    
    try:
        # 创建新用户
        user = User(username=username)
        user.password = password
        # Removed setting user.email
        
        db.session.add(user)
        
        # --- BEGIN UserProfile Creation ---
        # 从请求数据中获取 Profile 信息
        height_str = data.get('height')
        weight_str = data.get('weight')
        birth_date_str = data.get('birth_date') # Expecting 'YYYY-MM-DD' format from frontend
        gender = data.get('gender')
        activity_level = data.get('activity_level')

        # 创建 UserProfile 实例
        user_profile = UserProfile(user=user) # Associate with the user immediately

        # Safely convert and assign values
        try:
            user_profile.height = float(height_str) if height_str else None
        except (ValueError, TypeError):
            print(f"Warning: Invalid height value '{height_str}' for user {username}, setting to None.")
            user_profile.height = None
            
        try:
            user_profile.weight = float(weight_str) if weight_str else None
        except (ValueError, TypeError):
            print(f"Warning: Invalid weight value '{weight_str}' for user {username}, setting to None.")
            user_profile.weight = None

        try:
            user_profile.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        except (ValueError, TypeError):
            print(f"Warning: Invalid birth_date format '{birth_date_str}' for user {username} (expected YYYY-MM-DD), setting to None.")
            user_profile.birth_date = None
            
        user_profile.gender = gender
        user_profile.activity_level = activity_level
        
        db.session.add(user_profile)
        # --- END UserProfile Creation ---

        # 第一次提交，保存 User 和 UserProfile，以便获取 user.id
        # 注意：如果后续 ActivityLog 创建失败，这里可能需要调整事务处理
        db.session.commit() 
        
        # 记录注册活动 (现在 user.id 是可用的)
        log = ActivityLog(
            user_id=user.id, 
            action='register',
            details={'ip': request.remote_addr},
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit() # 第二次提交，保存 ActivityLog
        
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
                'user': user.to_dict() # Use the updated to_dict which excludes email
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
            'user': user.to_dict() # Use the updated to_dict which excludes email
        }
    })

@auth_bp.route('/password/change', methods=['PUT'])
@jwt_required()
def change_user_password():
    """修改当前登录用户的密码"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return bad_request('无效的请求数据')

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return bad_request('当前密码和新密码不能为空')

    if len(new_password) < 8:
        return bad_request('新密码长度至少需要8位')

    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')

    # 验证当前密码
    if not user.verify_password(current_password):
        return unauthorized('当前密码错误')

    # 设置新密码 (setter会自动处理哈希)
    user.password = new_password
    # Consider adding password_updated_at field
    # user.password_updated_at = datetime.utcnow()

    db.session.commit() # Commit user password change

    # 记录密码修改活动 (可选)
    try:
        log = ActivityLog(
            user_id=user.id,
            action='change_password',
            details={'ip': request.remote_addr},
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit() # Commit activity log
    except Exception as log_error:
        print(f"Error logging password change for user {user_id}: {log_error}")
        # Decide if failure to log should prevent success response
        # db.session.rollback() # Optionally rollback if logging is critical

    return jsonify({
        'success': True,
        'message': '密码修改成功'
    }) 