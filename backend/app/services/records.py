from datetime import datetime, timedelta, date
from ..models import db, Record
from ..utils.errors import ValidationError, NotFoundError
from sqlalchemy import func

class RecordService:
    @staticmethod
    def create_food_record(user_id, data):
        """创建食物记录"""
        food_name = data.get('food_name')
        meal_time = data.get('meal_time')
        
        if not food_name or not meal_time:
            raise ValidationError("食物名称和用餐时间不能为空")
        
        # 处理record_date，如果没有提供则使用当前日期
        record_date_str = data.get('record_date')
        if record_date_str:
            try:
                record_date = datetime.strptime(record_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("日期格式无效")
        else:
            record_date = date.today()
        
        record = Record(
            user_id=user_id,
            food_name=food_name,
            meal_time=meal_time,
            note=data.get('note'),
            record_date=record_date
        )
        
        db.session.add(record)
        db.session.commit()
        
        return record
    
    @staticmethod
    def create_exercise_record(user_id, data):
        """创建运动记录"""
        exercise_type = data.get('exercise_type')
        duration = data.get('duration')
        intensity = data.get('intensity')
        
        if not exercise_type or not duration or not intensity:
            raise ValidationError("运动类型、时长和强度不能为空")
        
        # 处理record_date，如果没有提供则使用当前日期
        record_date_str = data.get('record_date')
        if record_date_str:
            try:
                record_date = datetime.strptime(record_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("日期格式无效")
        else:
            record_date = date.today()
        
        record = Record(
            user_id=user_id,
            exercise_type=exercise_type,
            duration=duration,
            intensity=intensity,
            note=data.get('note'),
            record_date=record_date
        )
        
        db.session.add(record)
        db.session.commit()
        
        return record
    
    @staticmethod
    def create_mood_record(user_id, data):
        """创建心情记录"""
        mood_type = data.get('mood_type')
        
        if not mood_type:
            raise ValidationError("心情类型不能为空")
        
        # 处理record_date，如果没有提供则使用当前日期
        record_date_str = data.get('record_date')
        if record_date_str:
            try:
                record_date = datetime.strptime(record_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("日期格式无效")
        else:
            record_date = date.today()
        
        record = Record(
            user_id=user_id,
            mood_type=mood_type,
            note=data.get('note'),
            record_date=record_date
        )
        
        db.session.add(record)
        db.session.commit()
        
        return record
    
    @staticmethod
    def create_health_record(user_id, data):
        """创建健康记录"""
        feeling = data.get('feeling')
        status = data.get('status', [])
        
        if not feeling:
            raise ValidationError("身体感觉不能为空")
        
        # 处理record_date，如果没有提供则使用当前日期
        record_date_str = data.get('record_date')
        if record_date_str:
            try:
                record_date = datetime.strptime(record_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("日期格式无效")
        else:
            record_date = date.today()
        
        record = Record(
            user_id=user_id,
            feeling=feeling,
            status=status,
            note=data.get('note'),
            record_date=record_date
        )
        
        db.session.add(record)
        db.session.commit()
        
        return record
    
    @staticmethod
    def get_all_records(user_id, days=7):
        """获取用户的所有记录
        
        Args:
            user_id: 用户ID
            days: 获取最近几天的记录，默认7天
            
        Returns:
            dict: 包含所有类型记录的字典
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 只使用created_at字段进行查询，不使用record_date
        food_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date
        ).order_by(Record.created_at.desc()).all()
        
        exercise_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date
        ).order_by(Record.created_at.desc()).all()
        
        mood_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date
        ).order_by(Record.created_at.desc()).all()
        
        health_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date
        ).order_by(Record.created_at.desc()).all()
        
        return {
            'food_records': [record.to_dict() for record in food_records],
            'exercise_records': [record.to_dict() for record in exercise_records],
            'mood_records': [record.to_dict() for record in mood_records],
            'health_records': [record.to_dict() for record in health_records]
        }
    
    @staticmethod
    def update_record(user_id, record_type, record_id, data):
        """更新记录
        
        Args:
            user_id: 用户ID
            record_type: 记录类型 (food, exercise, mood, health)
            record_id: 记录ID
            data: 更新数据
            
        Returns:
            更新后的记录对象
        """
        record_models = {
            'food': Record,
            'exercise': Record,
            'mood': Record,
            'health': Record
        }
        
        if record_type not in record_models:
            raise ValidationError(f"无效的记录类型: {record_type}")
            
        record = record_models[record_type].query.filter_by(id=record_id, user_id=user_id).first()
        if not record:
            raise NotFoundError(f"找不到ID为{record_id}的{record_type}记录")
            
        # 移除对record_date的处理
        if 'record_date' in data:
            del data['record_date']  # 删除record_date字段，避免尝试更新它
        
        # 根据记录类型更新不同字段
        if record_type == 'food':
            if 'food_name' in data:
                record.food_name = data['food_name']
            if 'meal_time' in data:
                record.meal_time = data['meal_time']
        elif record_type == 'exercise':
            if 'exercise_type' in data:
                record.exercise_type = data['exercise_type']
            if 'duration' in data:
                record.duration = data['duration']
            if 'intensity' in data:
                record.intensity = data['intensity']
        elif record_type == 'mood':
            if 'mood_type' in data:
                record.mood_type = data['mood_type']
        elif record_type == 'health':
            if 'feeling' in data:
                record.feeling = data['feeling']
            if 'status' in data:
                record.status = data['status']
            
        # 所有记录类型都可以更新note字段
        if 'note' in data:
            record.note = data['note']
            
        db.session.commit()
        return record
    
    @staticmethod
    def delete_record(user_id, record_type, record_id):
        """删除记录
        
        Args:
            user_id: 用户ID
            record_type: 记录类型 (food, exercise, mood, health)
            record_id: 记录ID
        """
        record_models = {
            'food': Record,
            'exercise': Record,
            'mood': Record,
            'health': Record
        }
        
        if record_type not in record_models:
            raise ValidationError("无效的记录类型")
            
        record = record_models[record_type].query.filter_by(
            id=record_id,
            user_id=user_id
        ).first()
        
        if not record:
            raise NotFoundError("记录不存在")
            
        db.session.delete(record)
        db.session.commit()
        
    @staticmethod
    def get_records_stats(user_id, days=30):
        """获取记录统计信息"""
        # 这个方法在用户仪表板中被调用
        # 返回一个简单的统计对象
        return {
            'total_records': 0,
            'exercise_records': 0,
            'mood_records': 0,
            'health_records': 0,
            'food_records': 0,
            'exercise_minutes': 0,
            'recent_moods': []
        } 