from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, ManualSuggestion, User
from ..utils.errors import ValidationError, bad_request, not_found

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/manual/<int:user_id>', methods=['GET'])
@jwt_required()
def get_manual_suggestions(user_id):
    """获取指定用户的手动建议列表"""
    current_user_id = get_jwt_identity()
    
    # 检查当前用户是否是管理员或者正在请求自己的建议
    user = User.query.get(current_user_id)
    if not user:
        return not_found('用户不存在')
    
    if not user.is_admin and current_user_id != user_id:
        return jsonify({
            'success': False,
            'message': '无权访问其他用户的建议'
        }), 403
    
    # 查询指定用户的所有手动建议，按时间倒序排列
    suggestions = ManualSuggestion.query.filter_by(user_id=user_id).order_by(
        ManualSuggestion.created_at.desc()
    ).all()
    
    return jsonify({
        'success': True,
        'data': [suggestion.to_dict() for suggestion in suggestions]
    })

@suggestions_bp.route('/manual/<int:user_id>', methods=['POST'])
@jwt_required()
def add_manual_suggestion(user_id):
    """为指定用户添加手动建议"""
    admin_id = get_jwt_identity()
    
    # 检查当前用户是否是管理员
    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin:
        return jsonify({
            'success': False,
            'message': '只有管理员可以添加手动建议'
        }), 403
    
    # 检查目标用户是否存在
    user = User.query.get(user_id)
    if not user:
        return not_found('用户不存在')
    
    # 获取并验证请求数据
    data = request.get_json()
    if not data:
        return bad_request('无效的请求数据')
    
    content = data.get('content')
    if not content or not content.strip():
        return bad_request('建议内容不能为空')
    
    # 创建新的手动建议
    suggestion = ManualSuggestion(
        user_id=user_id,
        admin_id=admin_id,
        content=content
    )
    
    # 保存到数据库
    db.session.add(suggestion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '建议已添加',
        'data': suggestion.to_dict()
    }), 201

@suggestions_bp.route('/manual/<int:suggestion_id>', methods=['DELETE'])
@jwt_required()
def delete_manual_suggestion(suggestion_id):
    """删除手动建议"""
    current_user_id = get_jwt_identity()
    
    # 检查当前用户是否是管理员
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({
            'success': False,
            'message': '只有管理员可以删除建议'
        }), 403
    
    # 查找建议
    suggestion = ManualSuggestion.query.get(suggestion_id)
    if not suggestion:
        return not_found('建议不存在')
    
    # 删除建议
    db.session.delete(suggestion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '建议已删除'
    })
