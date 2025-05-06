from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导出db
__all__ = ['db']

# 注意：其他模型将在应用初始化时导入，以避免循环导入问题

# 导入所有模型
from .user import User, UserProfile
from .record import Record
from .report import Report, ReportRequest, Recommendation
from .admin import SystemSetting, Announcement, ActivityLog
from .food import FoodItem
from .manual_suggestion import ManualSuggestion
from .advice_request import AdviceRequest

# 导出所有模型
__all__ = [
    'db',
    'User',
    'UserProfile',
    'Record',
    'Report',
    'ReportRequest',
    'Recommendation',
    'SystemSetting',
    'Announcement',
    'ActivityLog',
    'FoodItem',
    'ManualSuggestion',
    'AdviceRequest'
] 