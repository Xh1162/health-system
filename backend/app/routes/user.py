from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user import UserService
from ..utils.errors import ValidationError, AuthenticationError

user_bp = Blueprint('user', __name__)

@user_bp.route('/info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取用户信息"""
    try:
        user_id = get_jwt_identity()
        user = UserService.get_user_info(user_id)
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
        user = UserService.update_user_info(user_id, data)
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