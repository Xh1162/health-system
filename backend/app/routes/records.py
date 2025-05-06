from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from ..models import db, Record
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
        valid_types = ['exercise', 'mood', 'health', 'food', 'body_status']
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
        elif record_type == 'body_status':
            weight = data.get('weight_kg')
            bmi_val = data.get('bmi')
            if weight is not None:
                try:
                    record.weight_kg = float(weight)
                except (ValueError, TypeError):
                    print(f"无效的体重值: {weight}")
                    # 可以选择返回错误或忽略无效值，这里选择忽略
                    pass
            if bmi_val is not None:
                try:
                    record.bmi = float(bmi_val)
                except (ValueError, TypeError):
                    print(f"无效的BMI值: {bmi_val}")
                    # 选择忽略无效值
                    pass
        
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

@records_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends_data():
    """获取指定时间范围和数据类型的趋势数据"""
    user_id = get_jwt_identity()
    
    # 获取查询参数
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date') # 默认为今天
        # 需要的数据类型，逗号分隔，例如: weight_kg,mood,exercise_duration
        data_types_str = request.args.get('data_types', '') 
        
        # 解析日期
        end_date = datetime.utcnow().date() # 默认结束日期为今天
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return bad_request('结束日期格式无效，请使用 YYYY-MM-DD')
        
        start_date = None # 默认为无开始日期限制 (或可以设置一个默认范围)
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return bad_request('开始日期格式无效，请使用 YYYY-MM-DD')
        
        # 解析需要的数据类型
        if not data_types_str:
            return bad_request('必须通过 data_types 参数指定至少一种数据类型')
        data_types = [dt.strip() for dt in data_types_str.split(',') if dt.strip()]
        valid_data_types = ['weight_kg', 'bmi', 'mood', 'exercise_duration'] # 可支持的趋势类型
        requested_types = [dt for dt in data_types if dt in valid_data_types]
        if not requested_types:
            return bad_request(f'不支持的数据类型。支持的类型: {valid_data_types}')

        # 构建基础查询
        query = Record.query.filter(Record.user_id == user_id)
        # 应用日期范围 (注意要查询 record_date 而不是 created_at)
        # 将 date 对象转换为 datetime 对象以便与 DateTime 列比较
        if start_date:
             query = query.filter(Record.record_date >= datetime.combine(start_date, datetime.min.time()))
        # 包含结束日期当天的数据
        query = query.filter(Record.record_date < datetime.combine(end_date + timedelta(days=1), datetime.min.time()))

        # 按日期排序，方便处理
        query = query.order_by(Record.record_date.asc())
        
        # 查询数据库
        records = query.all()
        
        # 处理结果
        trends_data = {dtype: [] for dtype in requested_types} # 初始化结果字典
        
        for record in records:
            record_date_str = record.record_date.strftime('%Y-%m-%d')
            
            if 'weight_kg' in requested_types and record.type == 'body_status' and record.weight_kg is not None:
                trends_data['weight_kg'].append({'date': record_date_str, 'value': record.weight_kg})
                
            if 'bmi' in requested_types and record.type == 'body_status' and record.bmi is not None:
                trends_data['bmi'].append({'date': record_date_str, 'value': record.bmi})
                
            if 'mood' in requested_types and record.type == 'mood' and record.mood_type:
                 # 对于心情，我们直接返回值（字符串），前端可以进行映射或展示
                trends_data['mood'].append({'date': record_date_str, 'value': record.mood_type})
                
            if 'exercise_duration' in requested_types and record.type == 'exercise' and record.duration is not None:
                trends_data['exercise_duration'].append({'date': record_date_str, 'value': record.duration})

        # 对于 exercise_duration，我们可能需要按天聚合（如果一天有多条记录）
        if 'exercise_duration' in trends_data:
            from collections import defaultdict
            aggregated_duration = defaultdict(float)
            for item in trends_data['exercise_duration']:
                aggregated_duration[item['date']] += item['value']
            trends_data['exercise_duration'] = [{'date': d, 'value': v} for d, v in sorted(aggregated_duration.items())]
            
        return jsonify({
            'success': True,
            'data': trends_data
        })
        
    except Exception as e:
        print(f"获取趋势数据时发生错误: {str(e)}")
        import traceback
        traceback.print_exc() # 打印详细错误堆栈
        return jsonify({
            'success': False,
            'message': f'获取趋势数据失败: {str(e)}'
        }), 500 