from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导出db
__all__ = ['db']

# 注意：其他模型将在应用初始化时导入，以避免循环导入问题

# 导入所有模型
from .user import User, UserProfile
from .record import Record, HealthStatus
from .report import Report, Recommendation
from .admin import SystemSetting, Announcement, ActivityLog

# 导出所有模型
__all__ = [
    'db',
    'User',
    'UserProfile',
    'Record',
    'HealthStatus',
    'Report',
    'Recommendation',
    'SystemSetting',
    'Announcement',
    'ActivityLog'
] 