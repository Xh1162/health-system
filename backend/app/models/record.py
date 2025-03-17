from datetime import datetime
from . import db

class Record(db.Model):
    __tablename__ = 'records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # exercise, mood, health, food
    note = db.Column(db.Text)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 运动记录字段
    exercise_type = db.Column(db.String(20))  # walking, running, cycling, swimming, yoga, gym, basketball, football, other
    duration = db.Column(db.Integer)  # 分钟
    intensity = db.Column(db.String(10))  # light, medium, high
    
    # 心情记录字段
    mood_type = db.Column(db.String(20))  # happy, calm, sad, angry, anxious, tired, excited, bored
    
    # 健康记录字段
    feeling = db.Column(db.String(20))  # energetic, good, normal, tired
    
    # 食物记录字段
    food_name = db.Column(db.String(100))
    meal_time = db.Column(db.String(20))  # breakfast, lunch, dinner, snack
    
    # 关联到用户
    user = db.relationship('User', backref=db.backref('records', lazy='dynamic'))
    
    def to_dict(self):
        record_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'note': self.note,
            'record_date': self.record_date.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
        
        # 根据记录类型添加特定字段
        if self.type == 'exercise':
            record_dict.update({
                'exercise_type': self.exercise_type,
                'duration': self.duration,
                'intensity': self.intensity
            })
        elif self.type == 'mood':
            record_dict.update({
                'mood_type': self.mood_type
            })
        elif self.type == 'health':
            record_dict.update({
                'feeling': self.feeling,
                'status': self.get_health_status()
            })
        elif self.type == 'food':
            record_dict.update({
                'food_name': self.food_name,
                'meal_time': self.meal_time
            })
            
        return record_dict
    
    def get_health_status(self):
        # 从健康状态关联表获取状态列表
        return [status.status for status in self.health_statuses]


class HealthStatus(db.Model):
    __tablename__ = 'health_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # sleep_well, sleep_bad, headache, fever, etc.
    
    # 关联到健康记录
    record = db.relationship('Record', backref=db.backref('health_statuses', cascade='all, delete-orphan')) 