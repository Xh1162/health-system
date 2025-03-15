from datetime import datetime, timedelta
import jwt
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token
from ..models import db, User
from ..utils.errors import ValidationError, AuthenticationError
from ..utils.helpers import validate_email, validate_phone, validate_password

class AuthService:
    @staticmethod
    def register(data):
        """用户注册"""
        # 验证输入
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        
        if not username or not email or not password:
            raise ValidationError("用户名、邮箱和密码不能为空")
        
        if not validate_email(email):
            raise ValidationError("邮箱格式不正确")
        
        if phone and not validate_phone(phone):
            raise ValidationError("手机号格式不正确")
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            raise ValidationError(msg)
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first():
            raise ValidationError("用户名已存在")
        if User.query.filter_by(email=email).first():
            raise ValidationError("邮箱已被注册")
        
        # 创建新用户
        try:
            user = User(username=username, email=email, password=password)
            if phone:
                user.phone = phone
            db.session.add(user)
            db.session.commit()
            
            # 使用flask_jwt_extended生成令牌
            token = create_access_token(identity=user.id)
            
            return user, token
        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"注册失败: {str(e)}")
    
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
        
    @staticmethod
    def update_password(user_id, old_password, new_password):
        """更新密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Raises:
            ValidationError: 验证失败
            AuthenticationError: 认证失败
        """
        user = User.query.get(user_id)
        if not user:
            raise AuthenticationError('用户不存在')
            
        if not user.check_password(old_password):
            raise AuthenticationError('原密码错误')
            
        if len(new_password) < 8:
            raise ValidationError('新密码长度必须至少为8个字符')
            
        user.set_password(new_password)
        db.session.commit()
        
    @staticmethod
    def reset_password(email, code, new_password):
        """重置密码
        
        Args:
            email: 邮箱
            code: 验证码
            new_password: 新密码
            
        Raises:
            ValidationError: 验证失败
            AuthenticationError: 认证失败
        """
        if not validate_email(email):
            raise ValidationError('邮箱格式不正确')
            
        user = User.query.filter_by(email=email).first()
        if not user:
            raise AuthenticationError('邮箱未注册')
            
        # TODO: 验证验证码
        
        if len(new_password) < 8:
            raise ValidationError('新密码长度必须至少为8个字符')
            
        user.set_password(new_password)
        db.session.commit()

    @staticmethod
    def update_avatar(user_id, avatar_url):
        """更新用户头像
        
        Args:
            user_id: 用户ID
            avatar_url: 头像URL
            
        Raises:
            ValidationError: 验证失败
            AuthenticationError: 认证失败
        """
        user = User.query.get(user_id)
        if not user:
            raise AuthenticationError('用户不存在')
            
        user.avatar = avatar_url
        db.session.commit()
        
        return user 