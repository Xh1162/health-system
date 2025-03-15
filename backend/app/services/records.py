from datetime import datetime, timedelta, date
from ..models import db, FoodRecord, ExerciseRecord, MoodRecord, HealthRecord
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
        
        record = FoodRecord(
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
        
        record = ExerciseRecord(
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
        
        record = MoodRecord(
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
        
        record = HealthRecord(
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
        food_records = FoodRecord.query.filter(
            FoodRecord.user_id == user_id,
            FoodRecord.created_at >= start_date
        ).order_by(FoodRecord.created_at.desc()).all()
        
        exercise_records = ExerciseRecord.query.filter(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.created_at >= start_date
        ).order_by(ExerciseRecord.created_at.desc()).all()
        
        mood_records = MoodRecord.query.filter(
            MoodRecord.user_id == user_id,
            MoodRecord.created_at >= start_date
        ).order_by(MoodRecord.created_at.desc()).all()
        
        health_records = HealthRecord.query.filter(
            HealthRecord.user_id == user_id,
            HealthRecord.created_at >= start_date
        ).order_by(HealthRecord.created_at.desc()).all()
        
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
            'food': FoodRecord,
            'exercise': ExerciseRecord,
            'mood': MoodRecord,
            'health': HealthRecord
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
            'food': FoodRecord,
            'exercise': ExerciseRecord,
            'mood': MoodRecord,
            'health': HealthRecord
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
        """获取记录统计信息
        
        Args:
            user_id: 用户ID
            days: 获取最近几天的统计，默认30天
            
        Returns:
            dict: 包含各类型记录统计信息的字典
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 食物记录统计
        food_count = FoodRecord.query.filter(
            FoodRecord.user_id == user_id,
            FoodRecord.created_at >= start_date,
            FoodRecord.created_at <= end_date
        ).count()
        
        # 运动记录统计
        exercise_count = ExerciseRecord.query.filter(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.created_at >= start_date,
            ExerciseRecord.created_at <= end_date
        ).count()
        
        # 运动时长统计
        exercise_duration = db.session.query(func.sum(ExerciseRecord.duration)).filter(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.created_at >= start_date,
            ExerciseRecord.created_at <= end_date
        ).scalar() or 0
        
        # 心情记录统计
        mood_count = MoodRecord.query.filter(
            MoodRecord.user_id == user_id,
            MoodRecord.created_at >= start_date,
            MoodRecord.created_at <= end_date
        ).count()
        
        # 心情类型分布
        mood_types = db.session.query(
            MoodRecord.mood_type, 
            func.count(MoodRecord.id)
        ).filter(
            MoodRecord.user_id == user_id,
            MoodRecord.created_at >= start_date,
            MoodRecord.created_at <= end_date
        ).group_by(MoodRecord.mood_type).all()
        
        mood_distribution = {mood_type: count for mood_type, count in mood_types}
        
        # 健康记录统计
        health_count = HealthRecord.query.filter(
            HealthRecord.user_id == user_id,
            HealthRecord.created_at >= start_date,
            HealthRecord.created_at <= end_date
        ).count()
        
        # 健康状况分布
        health_feelings = db.session.query(
            HealthRecord.feeling, 
            func.count(HealthRecord.id)
        ).filter(
            HealthRecord.user_id == user_id,
            HealthRecord.created_at >= start_date,
            HealthRecord.created_at <= end_date
        ).group_by(HealthRecord.feeling).all()
        
        health_distribution = {feeling: count for feeling, count in health_feelings}
        
        return {
            'total_records': food_count + exercise_count + mood_count + health_count,
            'food': {
                'count': food_count
            },
            'exercise': {
                'count': exercise_count,
                'total_duration': exercise_duration
            },
            'mood': {
                'count': mood_count,
                'distribution': mood_distribution
            },
            'health': {
                'count': health_count,
                'distribution': health_distribution
            },
            'period': {
                'days': days,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        } 