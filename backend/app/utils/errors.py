from flask import jsonify

class ValidationError(Exception):
    """验证错误"""
    pass

class AuthenticationError(Exception):
    """认证错误"""
    pass

class NotFoundError(Exception):
    """资源未找到错误"""
    pass

def bad_request(message):
    """返回400错误响应"""
    response = jsonify({'error': 'bad_request', 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    """返回401错误响应"""
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

def forbidden(message):
    """返回403错误响应"""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def not_found(message):
    """返回404错误响应"""
    response = jsonify({'error': 'not_found', 'message': message})
    response.status_code = 404
    return response

def method_not_allowed(message):
    """返回405错误响应"""
    response = jsonify({'error': 'method_not_allowed', 'message': message})
    response.status_code = 405
    return response

def internal_server_error(message):
    """返回500错误响应"""
    response = jsonify({'error': 'internal_server_error', 'message': message})
    response.status_code = 500
    return response

def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        return bad_request('无效的请求')
    
    @app.errorhandler(401)
    def handle_unauthorized(e):
        return unauthorized('未授权访问')
    
    @app.errorhandler(403)
    def handle_forbidden(e):
        return forbidden('禁止访问')
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return not_found('资源未找到')
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return method_not_allowed('不允许的方法')
    
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return internal_server_error('服务器内部错误')
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return bad_request(str(e))
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(e):
        return unauthorized(str(e))
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        return not_found(str(e)) 