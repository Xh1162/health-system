from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..models import db, User, SystemSetting, Announcement, ActivityLog
from ..utils.errors import bad_request, not_found, unauthorized

admin_bp = Blueprint('admin', __name__)

# 管理员权限检查装饰器
def admin_required(fn):
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin():
            return unauthorized('需要管理员权限')
        
        return fn(*args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """获取所有用户"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    """获取特定用户详情"""
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_status(user_id):
    """更新用户状态（激活/禁用）"""
    data = request.get_json()
    if not data or 'is_active' not in data:
        return bad_request('缺少必要参数')
    
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 不允许禁用自己
    admin_id = get_jwt_identity()
    if user_id == admin_id:
        return bad_request('不能修改自己的状态')
    
    user.is_active = data['is_active']
    db.session.commit()
    
    # 记录活动
    log = ActivityLog(
        user_id=admin_id,
        action='update_user_status',
        details=f"更新用户 {user.username} 的状态为 {'激活' if user.is_active else '禁用'}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '用户状态已更新'})

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_role(user_id):
    """更新用户角色"""
    data = request.get_json()
    if not data or 'role' not in data:
        return bad_request('缺少必要参数')
    
    if data['role'] not in ['user', 'admin']:
        return bad_request('无效的角色')
    
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 不允许降级自己的权限
    admin_id = get_jwt_identity()
    if user_id == admin_id and data['role'] != 'admin':
        return bad_request('不能降级自己的权限')
    
    user.role = data['role']
    db.session.commit()
    
    # 记录活动
    log = ActivityLog(
        user_id=admin_id,
        action='update_user_role',
        details=f"更新用户 {user.username} 的角色为 {user.role}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '用户角色已更新'})

@admin_bp.route('/settings', methods=['GET'])
@jwt_required()
@admin_required
def get_system_settings():
    """获取系统设置"""
    settings = SystemSetting.query.all()
    return jsonify([setting.to_dict() for setting in settings])

@admin_bp.route('/settings', methods=['POST'])
@jwt_required()
@admin_required
def create_system_setting():
    """创建系统设置"""
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return bad_request('缺少必要参数')
    
    # 检查设置是否已存在
    existing = SystemSetting.query.filter_by(key=data['key']).first()
    if existing:
        return bad_request('设置已存在，请使用PUT方法更新')
    
    setting = SystemSetting(
        key=data['key'],
        value=data['value'],
        description=data.get('description', '')
    )
    
    db.session.add(setting)
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='create_setting',
        details=f"创建系统设置 {setting.key}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(setting.to_dict()), 201

@admin_bp.route('/settings/<string:key>', methods=['PUT'])
@jwt_required()
@admin_required
def update_system_setting(key):
    """更新系统设置"""
    data = request.get_json()
    if not data or 'value' not in data:
        return bad_request('缺少必要参数')
    
    setting = SystemSetting.query.filter_by(key=key).first()
    if not setting:
        return not_found('设置不存在')
    
    setting.value = data['value']
    if 'description' in data:
        setting.description = data['description']
    
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='update_setting',
        details=f"更新系统设置 {setting.key}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(setting.to_dict())

@admin_bp.route('/settings/<string:key>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_system_setting(key):
    """删除系统设置"""
    setting = SystemSetting.query.filter_by(key=key).first()
    if not setting:
        return not_found('设置不存在')
    
    db.session.delete(setting)
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='delete_setting',
        details=f"删除系统设置 {key}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '设置已删除'})

@admin_bp.route('/announcements', methods=['GET'])
@jwt_required()
@admin_required
def get_announcements():
    """获取所有公告"""
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify([announcement.to_dict() for announcement in announcements])

@admin_bp.route('/announcements', methods=['POST'])
@jwt_required()
@admin_required
def create_announcement():
    """创建公告"""
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return bad_request('缺少必要参数')
    
    announcement = Announcement(
        title=data['title'],
        content=data['content'],
        is_active=data.get('is_active', True)
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='create_announcement',
        details=f"创建公告 {announcement.title}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(announcement.to_dict()), 201

@admin_bp.route('/announcements/<int:announcement_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_announcement(announcement_id):
    """更新公告"""
    data = request.get_json()
    if not data:
        return bad_request('缺少必要参数')
    
    announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return not_found('公告不存在')
    
    if 'title' in data:
        announcement.title = data['title']
    if 'content' in data:
        announcement.content = data['content']
    if 'is_active' in data:
        announcement.is_active = data['is_active']
    
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='update_announcement',
        details=f"更新公告 {announcement.title}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(announcement.to_dict())

@admin_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_announcement(announcement_id):
    """删除公告"""
    announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return not_found('公告不存在')
    
    db.session.delete(announcement)
    db.session.commit()
    
    # 记录活动
    admin_id = get_jwt_identity()
    log = ActivityLog(
        user_id=admin_id,
        action='delete_announcement',
        details=f"删除公告 {announcement.title}"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '公告已删除'})

@admin_bp.route('/logs', methods=['GET'])
@jwt_required()
@admin_required
def get_activity_logs():
    """获取活动日志"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': logs.page
    })

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_dashboard():
    """获取管理员仪表板数据"""
    # 用户统计
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(role='admin').count()
    
    # 最近注册的用户
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # 最近的活动日志
    recent_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
    
    # 活跃公告
    active_announcements = Announcement.query.filter_by(is_active=True).count()
    
    return jsonify({
        'user_stats': {
            'total': total_users,
            'active': active_users,
            'admin': admin_users
        },
        'recent_users': [user.to_dict() for user in recent_users],
        'recent_logs': [log.to_dict() for log in recent_logs],
        'active_announcements': active_announcements
    }) 