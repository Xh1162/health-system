from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.reports import ReportService
from ..utils.errors import ValidationError, bad_request, not_found
from datetime import datetime, timedelta

from ..models import db, Report, Record, Recommendation

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

# 新增的报告管理API

@reports_bp.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    """获取用户的所有报告"""
    user_id = get_jwt_identity()
    
    # 查询用户的所有报告
    reports = Report.query.filter_by(user_id=user_id).order_by(Report.created_at.desc()).all()
    
    return jsonify([report.to_dict() for report in reports])

@reports_bp.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """获取特定报告详情"""
    user_id = get_jwt_identity()
    
    # 查询特定报告
    report = Report.query.filter_by(id=report_id, user_id=user_id).first()
    if not report:
        return not_found('报告不存在或无权限')
    
    # 获取报告详情，包括建议
    report_data = report.to_dict()
    report_data['recommendations'] = [rec.to_dict() for rec in report.recommendations]
    
    return jsonify(report_data)

@reports_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_report():
    """生成健康报告"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return bad_request('无效的请求数据')
    
    report_type = data.get('type', 'weekly')
    if report_type not in ['daily', 'weekly', 'monthly']:
        return bad_request('无效的报告类型')
    
    # 计算报告时间范围
    end_date = datetime.utcnow()
    if report_type == 'daily':
        start_date = end_date - timedelta(days=1)
        title = f"每日健康报告 - {end_date.strftime('%Y-%m-%d')}"
    elif report_type == 'weekly':
        start_date = end_date - timedelta(days=7)
        title = f"每周健康报告 - {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}"
    else:  # monthly
        start_date = end_date - timedelta(days=30)
        title = f"每月健康报告 - {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}"
    
    # 查询时间范围内的记录
    records = Record.query.filter(
        Record.user_id == user_id,
        Record.created_at >= start_date,
        Record.created_at <= end_date
    ).all()
    
    # 如果没有记录，返回错误
    if not records:
        return bad_request('所选时间范围内没有记录，无法生成报告')
    
    # 分析记录数据
    exercise_records = [r for r in records if r.type == 'exercise']
    mood_records = [r for r in records if r.type == 'mood']
    health_records = [r for r in records if r.type == 'health']
    food_records = [r for r in records if r.type == 'food']
    
    # 计算统计数据
    total_exercise_minutes = sum(record.duration or 0 for record in exercise_records)
    avg_exercise_intensity = sum(record.intensity or 0 for record in exercise_records) / len(exercise_records) if exercise_records else 0
    
    # 分析心情
    mood_distribution = {}
    for record in mood_records:
        mood_type = record.mood_type
        if mood_type in mood_distribution:
            mood_distribution[mood_type] += 1
        else:
            mood_distribution[mood_type] = 1
    
    dominant_mood = max(mood_distribution.items(), key=lambda x: x[1])[0] if mood_distribution else "未知"
    
    # 创建报告
    report = Report(
        user_id=user_id,
        title=title,
        type=report_type,
        start_date=start_date,
        end_date=end_date,
        summary=f"在过去的{(end_date - start_date).days}天中，您进行了{len(exercise_records)}次运动，总计{total_exercise_minutes}分钟。"
                f"您的主要心情是{dominant_mood}，记录了{len(food_records)}次饮食和{len(health_records)}次健康状况。"
    )
    
    db.session.add(report)
    db.session.flush()  # 获取报告ID
    
    # 生成建议
    recommendations = []
    
    # 运动建议
    if total_exercise_minutes < 150 and report_type in ['weekly', 'monthly']:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='exercise',
                content='您的运动时间不足，建议每周至少进行150分钟中等强度有氧运动。'
            )
        )
    elif avg_exercise_intensity < 3:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='exercise',
                content='您的运动强度较低，可以尝试增加一些高强度间歇训练来提高效果。'
            )
        )
    
    # 心情建议
    if dominant_mood in ['sad', 'anxious', 'stressed']:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='mood',
                content='您最近的心情偏向负面，建议尝试冥想、深呼吸或寻求专业心理咨询。'
            )
        )
    
    # 健康状况建议
    health_issues = []
    for record in health_records:
        for status in record.health_statuses:
            health_issues.append(status.status)
    
    if 'headache' in health_issues:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='health',
                content='您最近出现头痛症状，建议保持充足睡眠，减少屏幕时间，必要时咨询医生。'
            )
        )
    
    if 'fatigue' in health_issues:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='health',
                content='您最近感到疲劳，建议检查睡眠质量，均衡饮食，适当补充维生素。'
            )
        )
    
    # 添加通用建议
    if not recommendations:
        recommendations.append(
            Recommendation(
                report_id=report.id,
                category='general',
                content='继续保持良好的健康习惯，定期记录您的健康状况。'
            )
        )
    
    # 保存建议
    for recommendation in recommendations:
        db.session.add(recommendation)
    
    db.session.commit()
    
    # 返回生成的报告
    report_data = report.to_dict()
    report_data['recommendations'] = [rec.to_dict() for rec in recommendations]
    
    return jsonify(report_data), 201

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    """删除报告"""
    user_id = get_jwt_identity()
    
    # 查找报告
    report = Report.query.filter_by(id=report_id, user_id=user_id).first()
    if not report:
        return not_found('报告不存在或无权限')
    
    # 删除关联的建议
    Recommendation.query.filter_by(report_id=report_id).delete()
    
    # 删除报告
    db.session.delete(report)
    db.session.commit()
    
    return jsonify({'message': '报告已删除'}) 