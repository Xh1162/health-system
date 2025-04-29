from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import db, AdviceRequest # 导入 AdviceRequest 模型
from ..utils.errors import bad_request

# 创建蓝图，定义 URL 前缀
advice_bp = Blueprint('advice', __name__, url_prefix='/api/advice-requests')

@advice_bp.route('', methods=['POST'])
@jwt_required() # 确保用户已登录
def submit_advice_request():
    """用户提交一个新的建议请求"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        # 允许没有 request_text 的空请求体，表示用户只想触发请求
        request_text = None 
    else:
        request_text = data.get('request_text')
        # 你可以在这里添加对 request_text 长度等的验证

    try:
        # 创建新的建议请求记录
        new_request = AdviceRequest(
            user_id=user_id,
            request_text=request_text
            # status 默认为 'pending', requested_at 默认为 now
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '建议请求已成功提交',
            'data': new_request.to_dict() # 返回创建的请求详情
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"提交建议请求时发生错误 (User {user_id}): {str(e)}")
        return jsonify({
            'success': False,
            'message': f'提交建议请求失败: {str(e)}'
        }), 500

# 未来可以在这里添加获取用户自己的建议请求历史等路由 