from datetime import datetime, timedelta
import jwt
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token
from ..models import db, User
from ..utils.errors import ValidationError, AuthenticationError
from ..utils.helpers import validate_email, validate_phone, validate_password

class AuthService:
    @staticmethod
    def login(username, password):
        """用户登录"""
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                raise AuthenticationError("用户不存在")
            
            if not user.check_password(password):
                raise AuthenticationError("密码错误")
            
            if not user.is_active:
                raise AuthenticationError("账号已被禁用")
            
            # 使用flask_jwt_extended生成令牌
            token = create_access_token(identity=user.id)
            
            return user, token
        except (AuthenticationError, Exception) as e:
            raise AuthenticationError(str(e))
    
    @staticmethod
    def get_user_by_token(token):
        """通过令牌获取用户信息"""
        try:
            # 使用flask_jwt_extended解码令牌
            payload = decode_token(token)
            user_id = payload['sub']  # flask_jwt_extended使用'sub'存储identity
            
            user = User.query.get(user_id)
            if not user:
                return None
            return user
        except Exception:
            return None 