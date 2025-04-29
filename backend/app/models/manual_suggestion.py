from datetime import datetime
from . import db

class ManualSuggestion(db.Model):
    __tablename__ = 'manual_suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 哪个管理员添加的
    content = db.Column(db.Text, nullable=False)  # 建议内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('manual_suggestions', lazy='dynamic'))
    admin = db.relationship('User', foreign_keys=[admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin_id': self.admin_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'admin_name': self.admin.username if self.admin else None
        }
