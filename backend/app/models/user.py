from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(256), default='/default-avatar.png')
    role = db.Column(db.String(20), default='user')  # 'user' 或 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def password(self):
        raise AttributeError('密码不可读')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'avatar': self.avatar,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # 个人信息
    height = db.Column(db.Float)  # 身高(cm)
    weight = db.Column(db.Float)  # 体重(kg)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))  # male, female, other
    
    # 健康目标
    weight_goal = db.Column(db.Float)  # 目标体重
    activity_level = db.Column(db.String(20))  # low, medium, high
    
    # 关联到用户
    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade='all, delete-orphan'))
    
    def to_dict(self):
        return {
            'height': self.height,
            'weight': self.weight,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender,
            'weight_goal': self.weight_goal,
            'activity_level': self.activity_level
        } 