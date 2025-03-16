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
    
    if not data:
        return bad_request('无效的请求数据')
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return bad_request('用户名、邮箱和密码不能为空')
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return bad_request('用户名已被使用')
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return bad_request('邮箱已被使用')
    
    # 创建新用户
    user = User(username=username, email=email)
    user.password = password
    
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
    
    return jsonify({
        'success': True,
        'data': {
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar
            }
        }
    }), 201

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
        user.email = f"{username}@example.com"
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
                'avatar': user.avatar
            }
        }
    })

@auth_bp.route('/password', methods=['POST'])
def update_password():
    """更新密码"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        AuthService.update_password(user_id, old_password, new_password)
        
        return jsonify({
            'success': True,
            'message': '密码更新成功'
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'密码更新失败: {str(e)}'
        }), 500

@auth_bp.route('/password/reset', methods=['POST'])
def reset_password():
    """重置密码"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        AuthService.reset_password(email, code, new_password)
        
        return jsonify({
            'success': True,
            'message': '密码重置成功'
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'密码重置失败: {str(e)}'
        }), 500

@auth_bp.route('/avatar/<int:user_id>', methods=['POST'])
@jwt_required()
def upload_avatar(user_id):
    """上传用户头像"""
    # 验证用户身份
    current_user_id = get_jwt_identity()
    if int(current_user_id) != user_id:
        return unauthorized('无权操作其他用户的头像')
    
    # 检查是否有文件上传
    if 'avatar' not in request.files:
        return bad_request('没有文件上传')
    
    file = request.files['avatar']
    
    # 检查文件名
    if file.filename == '':
        return bad_request('没有选择文件')
    
    # 检查文件类型
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
        return bad_request('不支持的文件类型')
    
    # 生成安全的文件名
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # 确保上传目录存在
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_folder, new_filename)
    file.save(file_path)
    
    # 更新用户头像
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 设置头像路径
    avatar_url = f"/static/uploads/{new_filename}"
    user.avatar = avatar_url
    db.session.commit()
    
    # 构建完整URL
    base_url = request.host_url.rstrip('/')
    full_avatar_url = f"{base_url}{avatar_url}"
    
    return jsonify({
        'success': True,
        'data': {
            'avatar': full_avatar_url
        }
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return not_found('用户不存在')
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    }) 