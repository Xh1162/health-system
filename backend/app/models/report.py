from datetime import datetime
from . import db
# Use standard JSON type for broader compatibility including SQLite
from sqlalchemy.types import JSON

class ReportRequest(db.Model):
    __tablename__ = 'report_requests' # 表名：报告申请

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True) # 关联的用户ID
    requested_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # 申请时间
    # 状态: pending (待处理), processing (处理中), completed (已完成), rejected (已拒绝)
    status = db.Column(db.String(20), default='pending', nullable=False, index=True)
    # 用户申请时可选填写的备注
    user_notes = db.Column(db.Text)
    # 可选，关联到完成的报告ID
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=True)

    # 关联关系
    user = db.relationship('User', backref=db.backref('report_requests', lazy='dynamic')) # 反向关联到User模型
    report = db.relationship('Report',
                             foreign_keys=[report_id], # Specify the foreign key column
                             backref=db.backref('request', uselist=False)) # 反向关联到Report模型

    def to_dict(self): # 转换为字典，方便API返回
        return {
            'id': self.id,
            'user_id': self.user_id,
            'requested_at': self.requested_at.isoformat(),
            'status': self.status,
            'user_notes': self.user_notes,
            'report_id': self.report_id
        }

class Report(db.Model):
    __tablename__ = 'reports' # 表名：报告

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True) # 关联的用户ID
    # 管理员完成并发布报告的时间戳
    published_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # 可选：关联回触发此报告的申请ID
    request_id = db.Column(db.Integer, db.ForeignKey('report_requests.id'), nullable=True)

    # 使用 JSON 类型存储结构化的报告数据 (统计、分析结果等)
    report_data = db.Column(JSON) # Use standard JSON for SQLite

    # 存储管理员手写的反馈/建议
    admin_summary = db.Column(db.Text) # 总体总结
    admin_advice = db.Column(db.Text)  # 具体建议

    # 可选：记录是哪个管理员生成/发布的报告
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # 关联到管理员用户的ID

    # 关联关系
    user = db.relationship('User',
                           foreign_keys=[user_id],
                           back_populates='reports') # Link to User.reports
    publisher = db.relationship('User', foreign_keys=[admin_id]) # Keep this as is for now

    def to_dict(self): # 转换为字典，方便API返回
        return {
            'id': self.id,
            'user_id': self.user_id,
            'published_at': self.published_at.isoformat(),
            'request_id': self.request_id,
            'report_data': self.report_data, # 前端需要解析这个JSON
            'admin_summary': self.admin_summary,
            'admin_advice': self.admin_advice,
            'admin_id': self.admin_id
        }

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # exercise, diet, sleep, mental
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联到用户
    user = db.relationship('User', backref=db.backref('recommendations', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        } 