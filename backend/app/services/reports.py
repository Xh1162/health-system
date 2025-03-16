from datetime import datetime, timedelta
from ..models import Record, Report, Recommendation
from ..utils.errors import ValidationError

class ReportService:
    @staticmethod
    def get_report_data(user_id, period='week'):
        """获取报告数据
        
        Args:
            user_id: 用户ID
            period: 时间周期 (week, month, quarter, year)
            
        Returns:
            dict: 包含各类统计数据的字典
        """
        # 计算时间范围
        end_date = datetime.now().date()
        if period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        elif period == 'quarter':
            start_date = end_date - timedelta(days=90)
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
        else:
            # 默认为一周
            start_date = end_date - timedelta(days=7)
        
        # 查询各类记录
        records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        # 按类型分类记录
        food_records = [r for r in records if r.type == 'food']
        exercise_records = [r for r in records if r.type == 'exercise']
        mood_records = [r for r in records if r.type == 'mood']
        health_records = [r for r in records if r.type == 'health']
        
        # 处理数据
        return {
            'period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'type': period
            },
            'food': {
                'distribution': ReportService._process_food_distribution(food_records),
                'trend': ReportService._process_food_trend(food_records)
            },
            'exercise': {
                'duration': ReportService._process_exercise_duration(exercise_records),
                'intensity': ReportService._process_exercise_intensity(exercise_records)
            },
            'mood': {
                'trend': ReportService._process_mood_trend(mood_records)
            },
            'health': {
                'stats': ReportService._process_health_stats(health_records)
            }
        }
    
    @staticmethod
    def _process_food_distribution(records):
        """处理食物分布数据"""
        print(f"处理食物分布数据，记录数量: {len(records)}")
        distribution = {}
        for record in records:
            meal_time = record.meal_time
            distribution[meal_time] = distribution.get(meal_time, 0) + 1
            
        result = [{'name': k, 'value': v} for k, v in distribution.items()]
        print(f"食物分布数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not result:
            result = [{'name': '暂无数据', 'value': 0}]
            
        return result
    
    @staticmethod
    def _process_food_trend(records):
        """处理食物趋势数据"""
        print(f"处理食物趋势数据，记录数量: {len(records)}")
        dates = []
        counts = []
        date_count = {}
        
        for record in records:
            date = record.created_at.strftime('%Y-%m-%d')
            date_count[date] = date_count.get(date, 0) + 1
            
        # 按日期排序
        sorted_dates = sorted(date_count.keys())
        dates = sorted_dates
        counts = [date_count[date] for date in sorted_dates]
        
        result = {'dates': dates, 'counts': counts}
        print(f"食物趋势数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not dates:
            today = datetime.now().strftime('%Y-%m-%d')
            result = {'dates': [today], 'counts': [0]}
            
        return result
    
    @staticmethod
    def _process_exercise_duration(records):
        """处理运动时长数据"""
        print(f"处理运动时长数据，记录数量: {len(records)}")
        dates = []
        durations = []
        date_duration = {}
        
        for record in records:
            date = record.created_at.strftime('%Y-%m-%d')
            date_duration[date] = date_duration.get(date, 0) + record.duration
            
        # 按日期排序
        sorted_dates = sorted(date_duration.keys())
        dates = sorted_dates
        durations = [date_duration[date] for date in sorted_dates]
        
        result = {'dates': dates, 'durations': durations}
        print(f"运动时长数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not dates:
            today = datetime.now().strftime('%Y-%m-%d')
            result = {'dates': [today], 'durations': [0]}
            
        return result
    
    @staticmethod
    def _process_exercise_intensity(records):
        """处理运动强度分布"""
        print(f"处理运动强度分布数据，记录数量: {len(records)}")
        intensity_count = {}
        for record in records:
            intensity = record.intensity
            intensity_count[intensity] = intensity_count.get(intensity, 0) + 1
            
        result = [{'name': k, 'value': v} for k, v in intensity_count.items()]
        print(f"运动强度分布数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not result:
            result = [{'name': '暂无数据', 'value': 0}]
            
        return result
    
    @staticmethod
    def _process_mood_trend(records):
        """处理心情趋势数据"""
        print(f"处理心情趋势数据，记录数量: {len(records)}")
        dates = []
        values = []
        date_mood = {}
        
        for record in records:
            date = record.created_at.strftime('%Y-%m-%d')
            # 这里假设mood_type可以映射到数值
            mood_values = {'happy': 5, 'calm': 4, 'normal': 3, 'sad': 2, 'angry': 1}
            date_mood[date] = mood_values.get(record.mood_type, 3)
            
        # 按日期排序
        sorted_dates = sorted(date_mood.keys())
        dates = sorted_dates
        values = [date_mood[date] for date in sorted_dates]
        
        result = {'dates': dates, 'values': values}
        print(f"心情趋势数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not dates:
            today = datetime.now().strftime('%Y-%m-%d')
            result = {'dates': [today], 'values': [3]}
            
        return result
    
    @staticmethod
    def _process_health_stats(records):
        """处理健康状况统计"""
        print(f"处理健康状况统计数据，记录数量: {len(records)}")
        dates = []
        good = []
        normal = []
        bad = []
        date_stats = {}
        
        for record in records:
            date = record.created_at.strftime('%Y-%m-%d')
            if date not in date_stats:
                date_stats[date] = {'good': 0, 'normal': 0, 'bad': 0}
                
            if record.feeling in ['energetic', 'good']:
                date_stats[date]['good'] += 1
            elif record.feeling == 'normal':
                date_stats[date]['normal'] += 1
            else:
                date_stats[date]['bad'] += 1
                
        # 按日期排序
        sorted_dates = sorted(date_stats.keys())
        dates = sorted_dates
        good = [date_stats[date]['good'] for date in sorted_dates]
        normal = [date_stats[date]['normal'] for date in sorted_dates]
        bad = [date_stats[date]['bad'] for date in sorted_dates]
        
        result = {
            'dates': dates,
            'good': good,
            'normal': normal,
            'bad': bad
        }
        print(f"健康状况统计数据结果: {result}")
        
        # 如果没有数据，添加一个默认值
        if not dates:
            today = datetime.now().strftime('%Y-%m-%d')
            result = {
                'dates': [today],
                'good': [0],
                'normal': [0],
                'bad': [0]
            }
            
        return result

    @staticmethod
    def get_summary(user_id, days=7):
        """获取健康摘要数据
        
        Args:
            user_id: 用户ID
            days: 天数，默认7天
            
        Returns:
            dict: 包含摘要数据的字典
        """
        print(f"获取健康摘要数据，用户ID: {user_id}, 天数: {days}")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取食物记录
        food_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        # 获取运动记录
        exercise_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        # 获取心情记录
        mood_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        # 获取健康记录
        health_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        print(f"记录数量 - 食物: {len(food_records)}, 运动: {len(exercise_records)}, 心情: {len(mood_records)}, 健康: {len(health_records)}")
        
        # 计算食物记录数量
        food_count = len(food_records)
        
        # 计算运动总时长
        exercise_minutes = sum(record.duration for record in exercise_records)
        
        # 计算平均心情分数
        mood_values = {'happy': 5, 'calm': 4, 'normal': 3, 'sad': 2, 'angry': 1}
        mood_scores = [mood_values.get(record.mood_type, 3) for record in mood_records]
        mood_score = sum(mood_scores) / len(mood_scores) if mood_scores else 0
        
        # 获取最常见心情
        mood_counts = {}
        for record in mood_records:
            mood_counts[record.mood_type] = mood_counts.get(record.mood_type, 0) + 1
        
        top_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else None
        mood_labels = {
            'happy': '开心',
            'calm': '平静',
            'normal': '一般',
            'sad': '难过',
            'angry': '生气'
        }
        top_mood = mood_labels.get(top_mood, top_mood) if top_mood else '暂无数据'
        
        # 计算心情趋势
        mood_trend = '上升' if len(mood_scores) >= 2 and mood_scores[-1] > mood_scores[0] else '平稳'
        
        # 计算健康评分
        health_values = {'energetic': 5, 'good': 4, 'normal': 3, 'tired': 2}
        health_scores = [health_values.get(record.feeling, 3) for record in health_records]
        health_score = sum(health_scores) / len(health_scores) if health_scores else 0
        
        # 生成健康建议
        health_tip = '保持良好的生活习惯'
        if health_score < 3:
            health_tip = '注意休息，保持良好的作息'
        elif exercise_minutes < 60:
            health_tip = '建议增加运动时间，保持身体活力'
        elif food_count < 5:
            health_tip = '注意饮食规律，保持营养均衡'
        
        result = {
            'foodCount': food_count,
            'exerciseMinutes': exercise_minutes,
            'moodScore': mood_score,
            'healthScore': health_score,
            'topMood': top_mood,
            'moodTrend': mood_trend,
            'healthTip': health_tip
        }
        
        print(f"健康摘要数据结果: {result}")
        return result
        
    @staticmethod
    def get_trends(user_id, period='month'):
        """获取趋势分析数据
        
        Args:
            user_id: 用户ID
            period: 时间周期 (week, month, quarter, year)
            
        Returns:
            dict: 包含趋势分析数据的字典
        """
        # 计算时间范围
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
            raise ValidationError("无效的时间周期")
            
        # 获取记录数据
        food_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        exercise_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        mood_records = Record.query.filter(
            Record.user_id == user_id,
            Record.created_at >= start_date,
            Record.created_at <= end_date
        ).all()
        
        # 计算食物记录趋势
        food_trend = ReportService._calculate_trend(food_records, lambda r: 1)
        
        # 计算运动时长趋势
        exercise_trend = ReportService._calculate_trend(exercise_records, lambda r: r.duration)
        
        # 计算心情趋势
        mood_values = {'happy': 5, 'calm': 4, 'normal': 3, 'sad': 2, 'angry': 1}
        mood_trend = ReportService._calculate_trend(mood_records, lambda r: mood_values.get(r.mood_type, 3))
        
        return {
            'food': food_trend,
            'exercise': exercise_trend,
            'mood': mood_trend
        }
    
    @staticmethod
    def _calculate_trend(records, value_func):
        """计算趋势
        
        Args:
            records: 记录列表
            value_func: 值提取函数
            
        Returns:
            str: 趋势描述
        """
        if not records or len(records) < 2:
            return '数据不足'
            
        # 按日期排序
        sorted_records = sorted(records, key=lambda r: r.created_at)
        
        # 计算前半部分和后半部分的平均值
        mid_point = len(sorted_records) // 2
        first_half = sorted_records[:mid_point]
        second_half = sorted_records[mid_point:]
        
        first_avg = sum(value_func(r) for r in first_half) / len(first_half)
        second_avg = sum(value_func(r) for r in second_half) / len(second_half)
        
        # 计算变化百分比
        change_percent = (second_avg - first_avg) / first_avg * 100 if first_avg > 0 else 0
        
        if change_percent > 10:
            return '显著上升'
        elif change_percent > 5:
            return '略有上升'
        elif change_percent < -10:
            return '显著下降'
        elif change_percent < -5:
            return '略有下降'
        else:
            return '保持稳定'

    @staticmethod
    def get_recent_reports(user_id, limit=3):
        """获取最近的报告
        
        Args:
            user_id: 用户ID
            limit: 获取的报告数量限制
            
        Returns:
            list: 报告列表
        """
        # 这个方法在用户仪表板中被调用
        # 返回一个空列表，实际实现会查询数据库
        return [] 