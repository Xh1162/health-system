# backend/app/routes/admin_advice.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc # 用于排序

from ..models import db, AdviceRequest, User  # 导入 User 模型
from ..utils.errors import bad_request
# 需要导入管理员检查装饰器，假设它在 admin.py 中或是一个公共 utils
# 如果 admin_required 在 admin.py 中，需要调整导入路径或将其移到公共位置
try:
    from .admin import admin_required # 假设从 admin.py 导入
except ImportError:
    # 如果 admin.py 不存在或没有 admin_required, 提供一个备用/占位装饰器
    # 或者将 admin_required 移到 utils
    def admin_required(fn):
        def wrapper(*args, **kwargs):
            # 临时占位逻辑，实际应验证管理员身份
            print("Warning: admin_required decorator not found or properly imported. Placeholder used.")
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    print("Warning: Could not import admin_required from .admin. Using placeholder.")


# 创建新的蓝图
admin_advice_bp = Blueprint('admin_advice', __name__, url_prefix='/api/admin/advice-requests') # 统一前缀

@admin_advice_bp.route('', methods=['GET'])
@jwt_required()
@admin_required # 确保只有管理员能访问
def get_advice_requests():
    """管理员获取建议请求列表 (支持状态过滤和分页)"""
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int) # 每页显示数量，默认10
    status_filter = request.args.get('status', 'all').lower() # 'pending', 'answered', 'all'

    # 构建基础查询，并关联 User 表获取用户名
    # 使用 outerjoin 以防万一有请求关联不到用户的情况（理论上不应发生）
    query = db.session.query(AdviceRequest, User.username.label('requester_username')) \
                      .outerjoin(User, AdviceRequest.user_id == User.id)

    # 应用状态过滤
    if status_filter == 'pending':
        query = query.filter(AdviceRequest.status == 'pending')
    elif status_filter == 'answered':
        query = query.filter(AdviceRequest.status == 'answered')
    elif status_filter != 'all':
        # 如果提供了无效的状态值，可以返回错误或忽略
        return bad_request(f"无效的状态过滤参数: {status_filter}. 请使用 'pending', 'answered', 或 'all'.")

    # 按请求时间降序排序
    query = query.order_by(desc(AdviceRequest.requested_at))

    # 执行分页查询
    try:
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        requests_with_username = pagination.items
    except Exception as e:
         print(f"查询建议请求时出错: {str(e)}")
         return jsonify({"message": "获取建议请求失败", "error": str(e)}), 500
        
    # 序列化结果
    results = []
    for request_obj, username in requests_with_username:
        request_dict = request_obj.to_dict() # 使用模型中的 to_dict
        request_dict['requester_username'] = username if username else '未知用户'
        # 确保 requester_id 在字典中 (模型 to_dict 应该包含 user_id)
        request_dict['requester_id'] = request_obj.user_id 
        
        # (可选) 获取回复者用户名，如果已回复
        if request_obj.responder_id:
             responder = User.query.get(request_obj.responder_id)
             request_dict['responder_username'] = responder.username if responder else '未知管理员'
        else:
             request_dict['responder_username'] = None
             
        results.append(request_dict)

    return jsonify({
        'data': results,
        'pagination': {
            'current_page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })

# 这里稍后添加 POST /<int:request_id>/respond 路由 