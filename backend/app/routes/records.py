from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.records import RecordService
from ..utils.errors import ValidationError, NotFoundError

records_bp = Blueprint('records', __name__)

@records_bp.route('/food', methods=['POST'])
@jwt_required()
def create_food_record():
    """创建食物记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        record = RecordService.create_food_record(user_id, data)
        
        return jsonify({
            'success': True,
            'message': '食物记录已保存',
            'data': record.to_dict()
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建记录失败: {str(e)}'
        }), 500

@records_bp.route('/exercise', methods=['POST'])
@jwt_required()
def create_exercise_record():
    """创建运动记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        record = RecordService.create_exercise_record(user_id, data)
        
        return jsonify({
            'success': True,
            'message': '运动记录已保存',
            'data': record.to_dict()
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建记录失败: {str(e)}'
        }), 500

@records_bp.route('/mood', methods=['POST'])
@jwt_required()
def create_mood_record():
    """创建心情记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        record = RecordService.create_mood_record(user_id, data)
        
        return jsonify({
            'success': True,
            'message': '心情记录已保存',
            'data': record.to_dict()
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建记录失败: {str(e)}'
        }), 500

@records_bp.route('/health', methods=['POST'])
@jwt_required()
def create_health_record():
    """创建健康记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        record = RecordService.create_health_record(user_id, data)
        
        return jsonify({
            'success': True,
            'message': '健康状况已记录',
            'data': record.to_dict()
        })
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建记录失败: {str(e)}'
        }), 500

@records_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_records():
    """获取所有记录"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', 7, type=int)
        records = RecordService.get_all_records(user_id, days)
        
        return jsonify({
            'success': True,
            'data': records
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取记录失败: {str(e)}'
        }), 500

@records_bp.route('/<string:record_type>/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_record(record_type, record_id):
    """更新记录"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        record = RecordService.update_record(user_id, record_type, record_id, data)
        
        return jsonify({
            'success': True,
            'message': '记录更新成功',
            'data': record.to_dict()
        })
    except (ValidationError, NotFoundError) as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新记录失败: {str(e)}'
        }), 500

@records_bp.route('/<string:record_type>/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_record(record_type, record_id):
    """删除记录"""
    try:
        user_id = get_jwt_identity()
        RecordService.delete_record(user_id, record_type, record_id)
        
        return jsonify({
            'success': True,
            'message': '记录删除成功'
        })
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除记录失败: {str(e)}'
        }), 500

@records_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_records_stats():
    """获取记录统计信息"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', 30, type=int)
        stats = RecordService.get_records_stats(user_id, days)
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500 