from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

from ..models import db, User, UserProfile, Announcement
from ..utils.errors import ValidationError, AuthenticationError, bad_request, not_found

user_bp = Blueprint('user', __name__)

@user_bp.route('/info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取用户信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return not_found('用户不存在')
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_info(user_id):
    """更新用户信息"""
    try:
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            raise AuthenticationError("无权修改其他用户的信息")

        data = request.get_json()
        
        # 查询用户
        user = User.query.get(user_id)
        if not user:
            return not_found('用户不存在')
            
        # 更新用户基本信息
        if 'username' in data:
            # 检查用户名是否已存在
            existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
            if existing_user:
                return bad_request('用户名已被使用')
            user.username = data['username']
        
        # 注意：系统不再使用邮箱
        
        if 'phone' in data:
            user.phone = data['phone']
        
        # 更新密码
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '用户信息更新成功',
            'data': user.to_dict()
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户个人资料"""
    user_id = get_jwt_identity()
    
    # 查询用户及其个人资料
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 获取用户资料，包括个人信息
    user_data = user.to_dict()
    
    # 如果用户有个人资料，添加到返回数据中
    if user.profile:
        user_data['profile'] = user.profile.to_dict()
    else:
        user_data['profile'] = None
    
    return jsonify(user_data)

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户个人资料"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return bad_request('无效的请求数据')
    
    # 查询用户
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 更新用户基本信息
    if 'username' in data:
        # 检查用户名是否已存在
        existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
        if existing_user:
            return bad_request('用户名已被使用')
        user.username = data['username']
    
    # 注意：系统不再使用邮箱
    
    if 'phone' in data:
        user.phone = data['phone']
    
    # 更新密码
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    # 更新或创建用户个人资料
    profile_data = data.get('profile', {})
    if profile_data:
        if not user.profile:
            # 创建新的个人资料
            profile = UserProfile(user_id=user_id)
            user.profile = profile
        
        # 更新个人资料字段
        if 'height' in profile_data:
            user.profile.height = profile_data['height']
        if 'weight' in profile_data:
            user.profile.weight = profile_data['weight']
        if 'birth_date' in profile_data:
            # 将字符串转换为日期对象
            try:
                birth_date_str = profile_data['birth_date']
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
                user.profile.birth_date = birth_date
            except ValueError:
                return bad_request('出生日期格式无效，请使用YYYY-MM-DD格式')
        if 'gender' in profile_data:
            user.profile.gender = profile_data['gender']
        if 'weight_goal' in profile_data:
            user.profile.weight_goal = profile_data['weight_goal']
        if 'activity_level' in profile_data:
            user.profile.activity_level = profile_data['activity_level']
    
    db.session.commit()
    
    # 返回更新后的用户数据
    user_data = user.to_dict()
    if user.profile:
        user_data['profile'] = user.profile.to_dict()
    
    return jsonify(user_data)

@user_bp.route('/announcements', methods=['GET'])
@jwt_required()
def get_announcements():
    """获取活跃的公告"""
    # 查询所有活跃的公告
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).all()
    
    return jsonify([announcement.to_dict() for announcement in announcements])

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    """获取用户仪表板数据"""
    user_id = get_jwt_identity()
    
    # 获取用户信息
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 获取最新公告
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).limit(3).all()
    
    # 从记录服务获取统计数据
    from ..services.records import RecordService
    stats = RecordService.get_records_stats(user_id, 30)
    
    # 从报告服务获取最新报告
    from ..services.reports import ReportService
    recent_reports = ReportService.get_recent_reports(user_id, 3)
    
    return jsonify({
        'user': user.to_dict(),
        'announcements': [a.to_dict() for a in announcements],
        'stats': stats,
        'recent_reports': recent_reports
    })

@user_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传用户头像"""
    user_id = get_jwt_identity()
    
    # 查询用户
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 检查是否有文件上传
    if 'avatar' not in request.files:
        return bad_request('未找到头像文件')
    
    file = request.files['avatar']
    
    # 如果用户没有选择文件，浏览器也会提交一个空的文件
    if file.filename == '':
        return bad_request('未选择文件')
    
    # 检查文件类型
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return bad_request('不支持的文件类型')
    
    # 生成安全的文件名
    filename = secure_filename(file.filename)
    # 添加唯一标识符，避免文件名冲突
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # 确保上传文件夹存在
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    # 更新用户头像URL
    avatar_url = f"/uploads/{unique_filename}"
    user.avatar = avatar_url
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '头像上传成功',
        'avatar_url': avatar_url
    }) 