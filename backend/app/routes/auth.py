from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from ..services.auth import AuthService
from ..utils.errors import ValidationError, AuthenticationError
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import time

auth_bp = Blueprint('auth', __name__)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        user, token = AuthService.register(data)
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'data': {
                'token': token,
                'user': user.to_dict()
            }
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user, token = AuthService.login(username, password)
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'token': token,
                'user': user.to_dict()
            }
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500

@auth_bp.route('/password', methods=['POST'])
def update_password():
    """更新密码"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        AuthService.update_password(user_id, old_password, new_password)
        
        return jsonify({
            'success': True,
            'message': '密码更新成功'
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'密码更新失败: {str(e)}'
        }), 500

@auth_bp.route('/password/reset', methods=['POST'])
def reset_password():
    """重置密码"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        AuthService.reset_password(email, code, new_password)
        
        return jsonify({
            'success': True,
            'message': '密码重置成功'
        })
    except (ValidationError, AuthenticationError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'密码重置失败: {str(e)}'
        }), 500

@auth_bp.route('/avatar/<int:user_id>', methods=['POST'])
@jwt_required()
def update_avatar(user_id):
    """更新用户头像"""
    try:
        # 验证用户身份
        current_user_id = get_jwt_identity()
        print(f"当前用户ID: {current_user_id}, 请求更新的用户ID: {user_id}")
        print(f"当前用户ID类型: {type(current_user_id)}, 请求更新的用户ID类型: {type(user_id)}")
        
        # 确保用户ID是整数
        current_user_id = int(current_user_id)
        
        if current_user_id != user_id:
            print(f"用户ID不匹配: {current_user_id} != {user_id}")
            raise AuthenticationError("无权修改其他用户的头像")

        print("请求内容类型:", request.content_type)
        print("请求文件:", request.files)
        print("请求数据:", request.form)
        print("请求头:", request.headers)

        # 检查请求中是否包含文件
        if 'avatar' not in request.files:
            print("未找到avatar文件字段")
            raise ValidationError("未找到头像文件")
            
        file = request.files['avatar']
        
        if not file or not file.filename:
            print("文件对象为空或文件名为空")
            raise ValidationError("文件上传失败或文件名为空")
            
        print("文件信息:", {
            'filename': file.filename,
            'content_type': getattr(file, 'content_type', None),
            'mimetype': getattr(file, 'mimetype', None)
        })
        
        # 检查文件类型
        allowed_mimetypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']
        if file.mimetype not in allowed_mimetypes:
            print(f"不支持的文件类型: {file.mimetype}")
            raise ValidationError(f"不支持的文件类型: {file.mimetype}，请上传 PNG、JPG、JPEG 或 GIF 格式的图片")
            
        # 确保上传目录存在
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        print("上传目录:", upload_folder)
        
        # 生成安全的文件名
        extension = file.mimetype.split('/')[-1]
        if extension == 'jpeg':
            extension = 'jpg'
        filename = f"avatar_{user_id}_{int(time.time())}.{extension}"
        file_path = os.path.join(upload_folder, filename)
        
        try:
            file.save(file_path)
            print("文件已保存到:", file_path)
        except Exception as e:
            print("文件保存失败:", str(e))
            import traceback
            print(traceback.format_exc())
            raise ValidationError(f"文件保存失败: {str(e)}")
        
        # 更新用户头像URL
        avatar_url = f"/static/uploads/avatars/{filename}"
        user = AuthService.update_avatar(user_id, avatar_url)
        
        return jsonify({
            'success': True,
            'message': '头像更新成功',
            'data': {
                'avatar_url': avatar_url,
                'user': user.to_dict()
            }
        })
    except (ValidationError, AuthenticationError) as e:
        print("头像上传错误:", str(e))
        return jsonify({
            'success': False,
            'message': str(e)
        }), 422
    except Exception as e:
        import traceback
        print("头像上传异常:", str(e))
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'头像更新失败: {str(e)}'
        }), 500 