from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from sqlalchemy import asc, desc # Import asc and desc for sorting
from datetime import datetime # <--- 需要导入 datetime

from ..models import db, FoodItem, User, Report, AdviceRequest # <--- 导入 AdviceRequest 模型
from ..utils.errors import forbidden, not_found, bad_request # <--- 可能需要 bad_request

admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')

# --- 权限检查装饰器 ---
def admin_required(fn):
    """检查当前用户是否为管理员"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin():
            return forbidden('需要管理员权限')
        return fn(*args, **kwargs)
    return wrapper

# --- FoodItem 管理接口 ---

@admin_api_bp.route('/food-items', methods=['GET'])
@jwt_required()
@admin_required
def get_food_items():
    """获取食物条目列表 (支持分页, 搜索, 筛选, 排序)"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_term = request.args.get('search', None, type=str)
        category_filter = request.args.get('category', None, type=str)
        sort_by = request.args.get('sort_by', 'name', type=str) # Default sort by name
        sort_order = request.args.get('sort_order', 'asc', type=str) # Default sort order asc

        # Base query
        query = FoodItem.query

        # Apply search filter (case-insensitive)
        if search_term:
            query = query.filter(FoodItem.name.ilike(f'%{search_term}%'))

        # Apply category filter
        if category_filter:
            query = query.filter(FoodItem.category == category_filter)

        # Apply sorting
        sort_column = getattr(FoodItem, sort_by, FoodItem.name) # Default to name if invalid column
        if sort_order.lower() == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        # Execute query with pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = pagination.items

        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in items],
            'pagination': {
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'current_page': pagination.page,
                'per_page': pagination.per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
    except Exception as e:
        # Log the error e
        print(f"Error fetching food items: {e}") # Basic logging
        return jsonify({'success': False, 'message': '获取食物列表失败'}), 500

@admin_api_bp.route('/food-items', methods=['POST'])
@jwt_required()
@admin_required
def create_food_item():
    """创建一个新的食物条目"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求体不能为空'}), 400

    name = data.get('name')
    category = data.get('category')

    if not name or not category:
        return jsonify({'success': False, 'message': '缺少必需字段: name, category'}), 400

    # 检查名称是否已存在 (可选，但建议)
    if FoodItem.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': f'食物名称 "{name}" 已存在'}), 409 # 409 Conflict

    try:
        new_item = FoodItem(
            name=name,
            category=category,
            description=data.get('description'),
            image_url=data.get('image_url'),
            is_recommended=data.get('is_recommended', True) # Default to True if not provided
        )
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '食物条目创建成功',
            'data': new_item.to_dict()
        }), 201 # 201 Created

    except Exception as e:
        db.session.rollback() # 回滚事务
        # Log the error e
        return jsonify({'success': False, 'message': f'创建食物条目失败: {str(e)}'}), 500

@admin_api_bp.route('/food-items/<int:item_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_food_item(item_id):
    """获取单个食物条目的详细信息"""
    try:
        item = FoodItem.query.get_or_404(item_id)
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        # Log the error e
        # get_or_404 already handles NotFoundError, so this catches other potential errors
        if "404 Not Found" in str(e): # Basic check if the exception is the 404 from get_or_404
             return not_found(f'ID为 {item_id} 的食物条目未找到')
        return jsonify({'success': False, 'message': f'获取食物条目失败: {str(e)}'}), 500

@admin_api_bp.route('/food-items/<int:item_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_food_item(item_id):
    """更新一个食物条目"""
    item = FoodItem.query.get_or_404(item_id)
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求体不能为空'}), 400

    try:
        # 更新允许修改的字段
        if 'name' in data:
            new_name = data['name']
            # 检查新名称是否与其他条目冲突 (除了自身)
            existing = FoodItem.query.filter(FoodItem.name == new_name, FoodItem.id != item_id).first()
            if existing:
                return jsonify({'success': False, 'message': f'食物名称 "{new_name}" 已被其他条目使用'}), 409
            item.name = new_name
            
        if 'category' in data:
            item.category = data['category']
        if 'description' in data:
            item.description = data['description']
        if 'image_url' in data:
            item.image_url = data['image_url']
        if 'is_recommended' in data:
            # 确保接收的是布尔值
            if isinstance(data['is_recommended'], bool):
                item.is_recommended = data['is_recommended']
            else:
                 return jsonify({'success': False, 'message': 'is_recommended 必须是布尔值 (true/false)'}), 400
                            
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '食物条目更新成功',
            'data': item.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        # Log the error e
        # Handle specific errors like IntegrityError if needed
        if "404 Not Found" in str(e): # Handle case where get_or_404 raises within try block
             return not_found(f'ID为 {item_id} 的食物条目未找到')
        return jsonify({'success': False, 'message': f'更新食物条目失败: {str(e)}'}), 500

@admin_api_bp.route('/food-items/<int:item_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_food_item(item_id):
    """删除一个食物条目"""
    try:
        item = FoodItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '食物条目删除成功'
        })
    except Exception as e:
        db.session.rollback()
        # Log the error e
        if "404 Not Found" in str(e):
             return not_found(f'ID为 {item_id} 的食物条目未找到')
        return jsonify({'success': False, 'message': f'删除食物条目失败: {str(e)}'}), 500

@admin_api_bp.route('/food-categories', methods=['GET'])
@jwt_required()
@admin_required
def get_food_categories():
    """获取所有唯一的食物类别列表"""
    try:
        # 查询数据库中所有不重复的类别，过滤掉None或空字符串，并排序
        categories = db.session.query(FoodItem.category).distinct()\
                                .filter(FoodItem.category.isnot(None))\
                                .filter(FoodItem.category != '')\
                                .order_by(FoodItem.category).all()
        # 将结果从元组列表转换为字符串列表
        category_list = [cat[0] for cat in categories]
        return jsonify({
            'success': True,
            'data': category_list
        })
    except Exception as e:
        print(f"Error fetching food categories: {e}") # Basic logging
        return jsonify({'success': False, 'message': '获取食物类别列表失败'}), 500

# --- User Management Endpoints ---

@admin_api_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """获取用户列表 (支持分页, 搜索, 筛选, 排序)"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_term = request.args.get('search', None, type=str)
        role_filter = request.args.get('role', None, type=str)
        status_filter = request.args.get('status', None, type=str) # 'active', 'inactive' or None
        sort_by = request.args.get('sort_by', 'id', type=str) # Default sort by id
        sort_order = request.args.get('sort_order', 'asc', type=str) # Default sort order asc

        # Base query
        query = User.query

        # Apply search filter (username or email, case-insensitive)
        if search_term:
            search_pattern = f'%{search_term}%'
            query = query.filter(
                db.or_(User.username.ilike(search_pattern), User.email.ilike(search_pattern))
            )

        # Apply role filter
        if role_filter:
            query = query.filter(User.role == role_filter)
            
        # Apply status filter
        if status_filter:
            if status_filter.lower() == 'active':
                query = query.filter(User.is_active == True)
            elif status_filter.lower() == 'inactive':
                query = query.filter(User.is_active == False)

        # Apply sorting
        sort_column = getattr(User, sort_by, User.id) # Default to id if invalid column
        if sort_order.lower() == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        # Execute query with pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        users = pagination.items

        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users],
            'pagination': {
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'current_page': pagination.page,
                'per_page': pagination.per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
    except Exception as e:
        print(f"Error fetching users: {e}") # Basic logging
        return jsonify({'success': False, 'message': '获取用户列表失败'}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """更新用户信息 (主要用于修改角色和状态)"""
    
    # 获取当前管理员ID，用于安全检查
    current_admin_id = get_jwt_identity()
    
    # 查找目标用户
    user_to_update = User.query.get(user_id)
    if not user_to_update:
        return not_found(f'ID为 {user_id} 的用户未找到')
        
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求体不能为空'}), 400
        
    allowed_roles = ['user', 'admin']
    updated = False # Flag to track if any change was made

    try:
        # 更新角色
        if 'role' in data:
            new_role = data['role']
            if new_role not in allowed_roles:
                return jsonify({'success': False, 'message': f'无效的角色: {new_role}。允许的角色: {allowed_roles}'}), 400
                                            
            # 安全检查：不允许管理员修改自己的角色
            if user_id == current_admin_id and user_to_update.role != new_role:
                 return forbidden('不允许修改自己的角色')
                 
            if user_to_update.role != new_role:
                user_to_update.role = new_role
                updated = True

        # 更新状态 (is_active)
        if 'is_active' in data:
            new_status = data['is_active']
            if not isinstance(new_status, bool):
                return jsonify({'success': False, 'message': 'is_active 必须是布尔值 (true/false)'}), 400
                
            # 安全检查：不允许管理员禁用自己的账号
            if user_id == current_admin_id and not new_status:
                 return forbidden('不允许禁用自己的账号')
                 
            if user_to_update.is_active != new_status:
                user_to_update.is_active = new_status
                updated = True

        # 如果有更新，则提交数据库
        if updated:
            db.session.commit()
            return jsonify({
                'success': True,
                'message': '用户信息更新成功',
                'data': user_to_update.to_dict() # 返回更新后的用户信息
            })
        else:
            # 如果没有字段被更新，也返回成功，但可以给个提示
            return jsonify({
                'success': True,
                'message': '没有需要更新的字段',
                'data': user_to_update.to_dict()
            })

    except Exception as e:
        db.session.rollback()
        print(f"Error updating user {user_id}: {e}") # Basic logging
        return jsonify({'success': False, 'message': f'更新用户信息失败: {str(e)}'}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """删除一个用户账号"""
    
    # 获取当前管理员ID
    current_admin_id = get_jwt_identity()
    
    # 安全检查：不允许删除自己
    if user_id == current_admin_id:
        return forbidden('不允许删除自己的账号')
        
    # 查找目标用户
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return not_found(f'ID为 {user_id} 的用户未找到')
        
    # 可选：更严格的安全检查，例如不允许删除其他管理员，或者至少保留一个管理员
    # if user_to_delete.is_admin():
    #     admin_count = User.query.filter_by(role='admin').count()
    #     if admin_count <= 1:
    #         return forbidden('无法删除最后一个管理员账号')
    #     # return forbidden('不允许删除其他管理员账号') # 或者直接禁止删除其他管理员

    try:
        # 删除用户 (关联的 UserProfile 应该会因为 cascade delete 而被删除)
        # 注意：如果用户还有其他重要关联数据（不由cascade处理），可能需要在这里手动处理
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '用户删除成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user {user_id}: {e}") # Basic logging
        # 检查是否是外键约束错误等特定数据库错误
        return jsonify({'success': False, 'message': f'删除用户失败: {str(e)}'}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user_details(user_id):
    """获取单个用户的详细信息 (包括 Profile)"""
    try:
        user = User.query.options(db.joinedload(User.profile)).get(user_id)
        if not user:
            return not_found(f'ID为 {user_id} 的用户未找到')
            
        user_data = user.to_dict() # Get basic user data
        # Add profile data if it exists
        if user.profile:
            user_data['profile'] = user.profile.to_dict()
        else:
            user_data['profile'] = None # Indicate no profile data
            
        return jsonify({
            'success': True,
            'data': user_data
        })
        
    except Exception as e:
        print(f"Error fetching details for user {user_id}: {e}")
        return jsonify({'success': False, 'message': '获取用户详情失败'}), 500

@admin_api_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    """管理员创建新用户账号"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求体不能为空'}), 400

    # 验证必需字段
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user') # Default role to 'user' if not provided

    if not username or not password:
        return jsonify({'success': False, 'message': '缺少必需字段: username, password'}), 400
        
    # TODO: Add more robust email validation if needed
    if email and '@' not in email:
         return jsonify({'success': False, 'message': '无效的邮箱格式'}), 400
         
    # 验证角色
    allowed_roles = ['user', 'admin']
    if role not in allowed_roles:
        return jsonify({'success': False, 'message': f'无效的角色: {role}。允许的角色: {allowed_roles}'}), 400
                            
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': f'用户名 "{username}" 已被使用'}), 409 # Conflict
    if email and User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': f'邮箱 "{email}" 已被使用'}), 409 # Conflict

    try:
        new_user = User(
            username=username,
            email=email,
            role=role,
            is_active=data.get('is_active', True) # Default to active
            # Password will be set using the setter which handles hashing
        )
        new_user.password = password # Use the password setter
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '用户创建成功',
            'data': new_user.to_dict() # Return newly created user data
        }), 201 # Created status code

    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}") # Basic logging
        return jsonify({'success': False, 'message': f'创建用户失败: {str(e)}'}), 500

# --- 用户健康报告和建议接口 (更新后) ---

@admin_api_bp.route('/users/<int:user_id>/report', methods=['GET'])
@jwt_required()
@admin_required
def get_user_health_report(user_id):
    """获取指定用户的最新健康报告"""
    # 首先检查用户是否存在
    user = User.query.get(user_id)
    if not user:
        return not_found(f'用户 {user_id} 未找到')

    try:
        # 查询该用户的最新报告 (按发布时间降序排列)
        latest_report = Report.query.filter_by(user_id=user_id)\
                                    .order_by(Report.published_at.desc())\
                                    .first()

        if not latest_report:
            # 如果没有报告，可以返回成功但数据为空，或返回404
            # 返回 404 更清晰地表明资源（报告）不存在
            return not_found(f'用户 {user_id} 的健康报告未找到')

        # 将 Report 对象转换为字典，并准备前端需要的数据结构
        report_dict = latest_report.to_dict()
        
        # 构建符合前端期望的数据结构
        response_data = {
            'report_id': report_dict.get('id'),
            'user_id': report_dict.get('user_id'),
            'userName': user.username, # 从关联的 User 对象获取用户名
            'generated_at': report_dict.get('published_at'), # 使用 published_at 作为生成时间
            # 从 report_data JSON 字段中提取具体指标
            **(report_dict.get('report_data') or {}), # 解包 report_data JSON
            # 将 report 模型的 admin_advice 映射到 admin_recommendation
            'admin_recommendation': report_dict.get('admin_advice') or '' 
            # 如果需要 admin_summary，也可以添加: 'admin_summary': report_dict.get('admin_summary')
        }

        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        print(f"Error fetching health report for user {user_id}: {e}")
        return jsonify({'success': False, 'message': '获取健康报告失败'}), 500

@admin_api_bp.route('/users/<int:user_id>/recommendation', methods=['POST'])
@jwt_required()
@admin_required
def submit_user_recommendation(user_id):
    """提交或更新指定用户 *最新报告* 的管理员建议 (admin_advice)"""
    # 检查用户是否存在
    user = User.query.get(user_id)
    if not user:
        return not_found(f'用户 {user_id} 未找到')

    data = request.get_json()
    if not data or 'recommendation' not in data:
        return jsonify({'success': False, 'message': '请求体必须包含 \'recommendation\' 字段'}), 400

    recommendation_text = data.get('recommendation')

    try:
        # 找到该用户的最新报告
        latest_report = Report.query.filter_by(user_id=user_id)\
                                    .order_by(Report.published_at.desc())\
                                    .first()

        if not latest_report:
            # 如果没有报告，则无法提交建议
            return not_found(f'无法为用户 {user_id} 提交建议，因为该用户尚无健康报告')

        # 更新最新报告的 admin_advice 字段
        latest_report.admin_advice = recommendation_text
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '建议已成功更新到最新报告'
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error submitting recommendation for user {user_id}'s report: {e}")
        return jsonify({'success': False, 'message': '提交建议失败'}), 500

# --- 新增：管理员处理建议请求接口 ---

@admin_api_bp.route('/advice-requests', methods=['GET'])
@jwt_required()
@admin_required
def get_advice_requests():
    """获取建议请求列表 (支持按状态筛选和分页)"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        # 筛选状态，默认为 'pending'，可以传 'all' 获取所有，或 'answered' 等
        status_filter = request.args.get('status', 'pending', type=str)

        # 构建基础查询
        query = AdviceRequest.query

        # 应用状态筛选
        if status_filter and status_filter.lower() != 'all':
            query = query.filter(AdviceRequest.status == status_filter.lower())
            
        # 按请求时间排序 (最新优先)
        query = query.order_by(AdviceRequest.requested_at.desc())
        
        # 执行查询与分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = pagination.items
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in items],
            'pagination': {
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'current_page': pagination.page,
                'per_page': pagination.per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })

    except Exception as e:
        print(f"获取建议请求列表时出错: {str(e)}")
        return jsonify({'success': False, 'message': '获取建议请求列表失败'}), 500

@admin_api_bp.route('/advice-requests/<int:request_id>/respond', methods=['POST'])
@jwt_required()
@admin_required
def respond_to_advice_request(request_id):
    """管理员回复一个建议请求"""
    admin_user_id = get_jwt_identity() # 获取当前管理员的ID
    data = request.get_json()
    
    if not data or 'response_text' not in data or not data['response_text'].strip():
        return bad_request('请求体必须包含非空的 \'response_text\' 字段')
        
    response_text = data.get('response_text')
    
    try:
        # 查找请求
        advice_request = AdviceRequest.query.get(request_id)
        if not advice_request:
            return not_found(f'ID 为 {request_id} 的建议请求未找到')
            
        # 检查请求是否已经是 answered 状态 (可选)
        if advice_request.status == 'answered':
             return bad_request('该请求已被回复')

        # 更新请求状态和回复内容
        advice_request.status = 'answered'
        advice_request.response_text = response_text
        advice_request.admin_id = admin_user_id
        advice_request.responded_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '建议请求已成功回复',
            'data': advice_request.to_dict() # 返回更新后的请求详情
        })

    except Exception as e:
        db.session.rollback()
        print(f"回复建议请求 {request_id} 时出错: {str(e)}")
        return jsonify({'success': False, 'message': '回复建议请求失败'}), 500

# --- 其他管理员接口将在这里添加 ---
# (User management endpoints)
# (Recommendation endpoints)

