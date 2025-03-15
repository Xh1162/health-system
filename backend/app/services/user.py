from ..models import db, User
from ..utils.errors import ValidationError

class UserService:
    @staticmethod
    def get_user_info(user_id):
        """获取用户信息"""
        user = User.query.get(user_id)
        if not user:
            raise ValidationError("用户不存在")
        return user

    @staticmethod
    def update_user_info(user_id, data):
        """更新用户信息"""
        user = User.query.get(user_id)
        if not user:
            raise ValidationError("用户不存在")

        # 更新可修改的字段
        allowed_fields = ['nickname', 'gender', 'age', 'height', 'weight']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"更新用户信息失败: {str(e)}") 