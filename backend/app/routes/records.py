from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from ..models import db, Record, HealthStatus
from ..utils.errors import bad_request, not_found

records_bp = Blueprint('records', __name__)

@records_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_records():
    """获取所有记录"""
    user_id = get_jwt_identity()
    days = request.args.get('days', 30, type=int)
    
    # 计算起始日期
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 查询记录
    records = Record.query.filter(
        Record.user_id == user_id,
        Record.created_at >= start_date
    ).order_by(Record.created_at.desc()).all()
    
    return jsonify([record.to_dict() for record in records])

@records_bp.route('', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def create_record():
    """创建记录"""
    try:
        # 处理OPTIONS请求
        if request.method == 'OPTIONS':
            print("收到OPTIONS预检请求，直接返回200")
            # 不添加额外的CORS头部，让Flask-CORS处理
            return '', 200
            
        # 验证JWT
        user_id = get_jwt_identity()
        if not user_id:
            print("未提供有效的JWT令牌")
            return jsonify({
                'success': False,
                'message': '未授权，请先登录'
            }), 401
            
        print(f"创建记录API被调用，用户ID: {user_id}")
        
        # 获取请求数据
        data = request.get_json()
        print(f"请求数据: {data}")
        
        if not data:
            print("无效的请求数据")
            return bad_request('无效的请求数据')
        
        record_type = data.get('type')
        if not record_type:
            print("记录类型不能为空")
            return bad_request('记录类型不能为空')
        
        # 验证记录类型
        valid_types = ['exercise', 'mood', 'health', 'food']
        if record_type not in valid_types:
            print(f"无效的记录类型: {record_type}")
            return bad_request('无效的记录类型')
        
        # 处理记录日期
        record_date = data.get('record_date')
        if record_date:
            try:
                # 将字符串转换为日期对象
                record_date = datetime.strptime(record_date, '%Y-%m-%d')
                print(f"使用用户选择的日期: {record_date}")
            except ValueError:
                print(f"无效的日期格式: {record_date}")
                record_date = datetime.utcnow()
                print(f"使用当前时间作为记录日期: {record_date}")
        else:
            record_date = datetime.utcnow()
            print(f"未提供日期，使用当前时间: {record_date}")
        
        # 创建记录
        record = Record(
            user_id=user_id,
            type=record_type,
            note=data.get('note', ''),
            record_date=record_date
        )
        
        # 根据记录类型设置特定字段
        if record_type == 'exercise':
            record.exercise_type = data.get('exercise_type')
            record.duration = data.get('duration')
            record.intensity = data.get('intensity')
        elif record_type == 'mood':
            record.mood_type = data.get('mood_type')
        elif record_type == 'health':
            record.feeling = data.get('feeling')
            # 处理健康状态
            statuses = data.get('status', [])
            if statuses:
                for status in statuses:
                    health_status = HealthStatus(status=status)
                    record.health_statuses.append(health_status)
        elif record_type == 'food':
            record.food_name = data.get('food_name')
            record.meal_time = data.get('meal_time')
        
        # 保存记录
        db.session.add(record)
        db.session.commit()
        
        # 返回成功响应
        result = record.to_dict()
        print(f"记录创建成功: {result}")
        return jsonify(result), 201
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        print(f"创建记录时发生错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'创建记录失败: {str(e)}'
        }), 500

@records_bp.route('/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_record(record_id):
    """更新记录"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return bad_request('无效的请求数据')
    
    # 查找记录
    record = Record.query.filter_by(id=record_id, user_id=user_id).first()
    if not record:
        return not_found('记录不存在或无权限')
    
    # 更新通用字段
    if 'note' in data:
        record.note = data['note']
    
    # 根据记录类型更新特定字段
    if record.type == 'exercise':
        if 'exercise_type' in data:
            record.exercise_type = data['exercise_type']
        if 'duration' in data:
            record.duration = data['duration']
        if 'intensity' in data:
            record.intensity = data['intensity']
    elif record.type == 'mood':
        if 'mood_type' in data:
            record.mood_type = data['mood_type']
    elif record.type == 'health':
        if 'feeling' in data:
            record.feeling = data['feeling']
        # 更新健康状态
        if 'status' in data:
            # 删除旧状态
            for status in record.health_statuses:
                db.session.delete(status)
            # 添加新状态
            for status in data['status']:
                health_status = HealthStatus(record_id=record.id, status=status)
                db.session.add(health_status)
    elif record.type == 'food':
        if 'food_name' in data:
            record.food_name = data['food_name']
        if 'meal_time' in data:
            record.meal_time = data['meal_time']
    
    db.session.commit()
    
    return jsonify(record.to_dict())

@records_bp.route('/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_record(record_id):
    """删除记录"""
    user_id = get_jwt_identity()
    
    # 查找记录
    record = Record.query.filter_by(id=record_id, user_id=user_id).first()
    if not record:
        return not_found('记录不存在或无权限')
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': '记录已删除'})

@records_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_records_stats():
    """获取记录统计信息"""
    user_id = get_jwt_identity()
    days = request.args.get('days', 30, type=int)
    
    # 计算起始日期
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 查询各类型记录数量
    exercise_count = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'exercise',
        Record.created_at >= start_date
    ).count()
    
    mood_count = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'mood',
        Record.created_at >= start_date
    ).count()
    
    health_count = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'health',
        Record.created_at >= start_date
    ).count()
    
    food_count = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'food',
        Record.created_at >= start_date
    ).count()
    
    # 计算总运动时间
    exercise_records = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'exercise',
        Record.created_at >= start_date
    ).all()
    
    total_exercise_minutes = sum(record.duration or 0 for record in exercise_records)
    
    # 获取最近的心情记录
    recent_moods = Record.query.filter(
        Record.user_id == user_id,
        Record.type == 'mood',
        Record.created_at >= start_date
    ).order_by(Record.created_at.desc()).limit(5).all()
    
    return jsonify({
        'total_records': exercise_count + mood_count + health_count + food_count,
        'exercise_records': exercise_count,
        'mood_records': mood_count,
        'health_records': health_count,
        'food_records': food_count,
        'exercise_minutes': total_exercise_minutes,
        'recent_moods': [
            {
                'type': mood.mood_type,
                'date': mood.created_at.isoformat()
            } for mood in recent_moods
        ]
    }) 