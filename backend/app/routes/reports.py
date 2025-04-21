from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.reports import ReportService
from ..utils.errors import ValidationError, bad_request, not_found
from datetime import datetime, timedelta

from ..models import db, Report, Record, Recommendation

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """获取健康总结"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', 7, type=int)
        summary = ReportService.get_summary(user_id, days)
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取健康总结失败: {str(e)}'
        }), 500

@reports_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    """获取趋势分析"""
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'month')
        trends = ReportService.get_trends(user_id, period)
        
        return jsonify({
            'success': True,
            'data': trends
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取趋势分析失败: {str(e)}'
        }), 500 

# 新增的报告管理API

# 删除 / 路由
# @reports_bp.route('/', methods=['GET'])
# @jwt_required()
# def get_reports():
# ... (相关函数体也被删除)

# 删除 /<id> GET 路由
# @reports_bp.route('/<int:report_id>', methods=['GET'])
# @jwt_required()
# def get_report(report_id):
# ... (相关函数体也被删除)

# 删除 /generate 路由
# @reports_bp.route('/generate', methods=['POST'])
# @jwt_required()
# def generate_report():
# ... (相关函数体也被删除)

# 删除 /<id> DELETE 路由
# @reports_bp.route('/<int:report_id>', methods=['DELETE'])
# @jwt_required()
# def delete_report(report_id):
# ... (相关函数体也被删除) 