from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.reports import ReportService
from ..utils.errors import ValidationError
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/data', methods=['GET'])
@jwt_required()
def get_report_data():
    """获取报告数据"""
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'week')
        data = ReportService.get_report_data(user_id, period)
        
        try:
            # 获取原始食物记录数据，用于前端计算饮食丰富度
            end_date = datetime.now()
            if period == 'week':
                start_date = end_date - timedelta(days=7)
            elif period == 'month':
                start_date = end_date - timedelta(days=30)
            elif period == 'quarter':
                start_date = end_date - timedelta(days=90)
            elif period == 'year':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=7)
                
            from ..models import FoodRecord
            print(f"查询食物记录，用户ID: {user_id}, 开始日期: {start_date}, 结束日期: {end_date}")
            
            food_records = FoodRecord.query.filter(
                FoodRecord.user_id == user_id,
                FoodRecord.created_at >= start_date,
                FoodRecord.created_at <= end_date
            ).all()
            
            print(f"找到食物记录数量: {len(food_records)}")
            
            # 将食物记录转换为JSON格式
            food_records_json = []
            for record in food_records:
                try:
                    food_records_json.append({
                        'id': record.id,
                        'meal_time': record.meal_time,
                        'food_name': record.food_name,
                        'created_at': record.created_at.strftime('%Y-%m-%d')
                    })
                except Exception as record_err:
                    print(f"处理食物记录时出错: {str(record_err)}")
            
            # 添加到返回数据中
            data['foodRecords'] = food_records_json
            print(f"添加了 {len(food_records_json)} 条食物记录到响应中")
            
        except Exception as food_err:
            print(f"获取食物记录时出错: {str(food_err)}")
            # 不让食物记录错误影响整个API
            data['foodRecords'] = []
        
        return jsonify({
            'success': True,
            'data': data
        })
    except ValidationError as e:
        print(f"验证错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        import traceback
        print(f"获取报告数据失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'获取报告数据失败: {str(e)}'
        }), 500

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