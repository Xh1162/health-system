from datetime import datetime
from . import db
from sqlalchemy.dialects.postgresql import ARRAY # Or use db.JSON
from sqlalchemy.types import JSON # Use this for broader compatibility

class Record(db.Model):
    __tablename__ = 'records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # exercise, mood, food, body_status
    note = db.Column(db.Text)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 运动记录字段
    exercise_type = db.Column(db.String(20))  # walking, running, cycling, swimming, yoga, gym, basketball, football, other
    duration = db.Column(db.Integer)  # 分钟
    intensity = db.Column(db.String(10))  # light, medium, high
    
    # 心情记录字段
    mood_type = db.Column(db.String(20))  # happy, calm, sad, angry, anxious, tired, excited, bored
    
    # 食物记录字段
    food_name = db.Column(db.String(100))
    meal_time = db.Column(db.String(20))  # breakfast, lunch, dinner, snack
    
    # === 合并后的身体状况字段 ===
    feeling = db.Column(db.String(20), nullable=True) # Was part of health
    # Add status field (using JSON which works for SQLite, MySQL, PostgreSQL)
    status = db.Column(db.JSON, nullable=True) # Stores a list of status strings like ["sleep_well", "headache"]
    weight_kg = db.Column(db.Float, nullable=True) 
    bmi = db.Column(db.Float, nullable=True) 
    
    # 关联到用户
    user = db.relationship('User', backref=db.backref('records', lazy='dynamic'))
    
    def to_dict(self):
        record_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'note': self.note,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
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
        elif self.type == 'food':
            record_dict.update({
                'food_name': self.food_name,
                'meal_time': self.meal_time
            })
        elif self.type == 'body_status':
            record_dict.update({
                'feeling': self.feeling,
                'status': self.status, # Directly access the JSON/list field
                'weight_kg': self.weight_kg,
                'bmi': self.bmi
            })
            
        return record_dict
    
    # Remove get_health_status method
    # def get_health_status(self):
    #     return [status.status for status in self.health_statuses]

# Remove the HealthStatus model entirely
# class HealthStatus(db.Model):
#     __tablename__ = 'health_statuses'
#     
#     id = db.Column(db.Integer, primary_key=True)
#     record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     
#     record = db.relationship('Record', backref=db.backref('health_statuses', cascade='all, delete-orphan')) 