from flask import jsonify

def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': '请求参数错误',
            'error': str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': '未授权访问',
            'error': str(error)
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'message': '权限不足',
            'error': str(error)
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': '资源不存在',
            'error': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'message': '服务器内部错误',
            'error': str(error)
        }), 500

class APIException(Exception):
    """API异常基类"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or {})
        rv['success'] = False
        rv['message'] = self.message
        return rv

class ValidationError(APIException):
    """验证错误"""
    def __init__(self, message):
        super().__init__(message=message, status_code=400)

class AuthenticationError(APIException):
    """认证错误"""
    def __init__(self, message):
        super().__init__(message=message, status_code=401)

class PermissionError(APIException):
    """权限错误"""
    def __init__(self, message):
        super().__init__(message=message, status_code=403)

class NotFoundError(APIException):
    """资源不存在错误"""
    def __init__(self, message):
        super().__init__(message=message, status_code=404) 