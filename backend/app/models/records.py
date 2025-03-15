from datetime import datetime
from .user import db

class FoodRecord(db.Model):
    __tablename__ = 'food_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    meal_time = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner, snack
    note = db.Column(db.Text)
    record_date = db.Column(db.Date, nullable=False)  # 用户选择的记录日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('food_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_name': self.food_name,
            'meal_time': self.meal_time,
            'note': self.note,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ExerciseRecord(db.Model):
    __tablename__ = 'exercise_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # 分钟
    intensity = db.Column(db.String(20), nullable=False)  # light, medium, high
    note = db.Column(db.Text)
    record_date = db.Column(db.Date, nullable=False)  # 用户选择的记录日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('exercise_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exercise_type': self.exercise_type,
            'duration': self.duration,
            'intensity': self.intensity,
            'note': self.note,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MoodRecord(db.Model):
    __tablename__ = 'mood_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_type = db.Column(db.String(20), nullable=False)  # happy, calm, sad, angry, anxious, etc.
    note = db.Column(db.Text)
    record_date = db.Column(db.Date, nullable=False)  # 用户选择的记录日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('mood_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'mood_type': self.mood_type,
            'note': self.note,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feeling = db.Column(db.String(20), nullable=False)  # energetic, good, normal, tired
    status = db.Column(db.JSON)  # 存储多个健康状态标签
    note = db.Column(db.Text)
    record_date = db.Column(db.Date, nullable=False)  # 用户选择的记录日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('health_records', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'feeling': self.feeling,
            'status': self.status,
            'note': self.note,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 