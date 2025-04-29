from datetime import datetime
from . import db

class AdviceRequest(db.Model):
    __tablename__ = 'advice_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    request_text = db.Column(db.Text, nullable=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False, index=True) # pending, viewed, answered
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # 回复的管理员ID
    response_text = db.Column(db.Text, nullable=True)
    responded_at = db.Column(db.DateTime, nullable=True)

    # 关联关系
    # 申请建议的用户
    requester = db.relationship('User', foreign_keys=[user_id], backref=db.backref('advice_requests_made', lazy='dynamic'))
    # 回复建议的管理员
    responder = db.relationship('User', foreign_keys=[admin_id], backref=db.backref('advice_requests_answered', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'requester_username': self.requester.username if self.requester else None, # 包含申请者用户名
            'request_text': self.request_text,
            'requested_at': self.requested_at.isoformat(),
            'status': self.status,
            'admin_id': self.admin_id,
            'responder_username': self.responder.username if self.responder else None, # 包含回复者用户名
            'response_text': self.response_text,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }

    def __repr__(self):
        return f'<AdviceRequest {self.id} from User {self.user_id} - Status: {self.status}>' 