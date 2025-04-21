from datetime import datetime, timedelta
from ..models import Record, Report, Recommendation
from ..utils.errors import ValidationError

class ReportService:
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
        
        try:
            # 获取食物记录
            food_records = Record.query.filter(
                Record.user_id == user_id,
                Record.type == 'food',
                Record.created_at >= start_date,
                Record.created_at <= end_date
            ).all()
            
            # 获取运动记录
            exercise_records = Record.query.filter(
                Record.user_id == user_id,
                Record.type == 'exercise',
                Record.created_at >= start_date,
                Record.created_at <= end_date
            ).all()
            
            # 获取心情记录
            mood_records = Record.query.filter(
                Record.user_id == user_id,
                Record.type == 'mood',
                Record.created_at >= start_date,
                Record.created_at <= end_date
            ).all()
            
            # 获取健康记录
            health_records = Record.query.filter(
                Record.user_id == user_id,
                Record.type == 'health',
                Record.created_at >= start_date,
                Record.created_at <= end_date
            ).all()
            
            print(f"记录数量 - 食物: {len(food_records)}, 运动: {len(exercise_records)}, 心情: {len(mood_records)}, 健康: {len(health_records)}")
            
            # 计算食物记录数量
            food_count = len(food_records)
            
            # 计算运动总时长（处理空值）
            exercise_minutes = sum(record.duration or 0 for record in exercise_records)
            
            # 分析膳食分布
            meal_distribution = {}
            for record in food_records:
                meal_time = record.meal_time
                if meal_time:
                    meal_distribution[meal_time] = meal_distribution.get(meal_time, 0) + 1
            
            # 计算百分比
            total_meals = sum(meal_distribution.values()) if meal_distribution else 1
            for meal in meal_distribution:
                meal_distribution[meal] = round((meal_distribution[meal] / total_meals) * 100)
            
            # 确保包含所有膳食类型
            for meal in ['breakfast', 'lunch', 'dinner', 'snack']:
                if meal not in meal_distribution:
                    meal_distribution[meal] = 0
            
            # 分析食物类别
            food_categories = {
                'staple': 0,
                'protein': 0,
                'vegetables': 0,
                'snacks': 0
            }
            
            # 分析食物类别（这里简化处理，实际中可能需要根据食物名称或类型来分类）
            for record in food_records:
                category = record.category if hasattr(record, 'category') else None
                if category:
                    if category in food_categories:
                        food_categories[category] += 1
                    else:
                        food_categories['staple'] += 1  # 默认归类为主食
            
            # 如果没有足够的分类数据，使用默认值
            if sum(food_categories.values()) < 3:
                food_categories = {
                    'staple': 30,
                    'protein': 25,
                    'vegetables': 35,
                    'snacks': 10
                }
            else:
                # 计算百分比
                total_categories = sum(food_categories.values())
                for cat in food_categories:
                    food_categories[cat] = round((food_categories[cat] / total_categories) * 100)
            
            # 计算规律度（这里简化处理，根据每日进餐次数的一致性来估算）
            daily_meals = {}
            for record in food_records:
                date = record.created_at.strftime('%Y-%m-%d')
                if date not in daily_meals:
                    daily_meals[date] = set()
                if record.meal_time:
                    daily_meals[date].add(record.meal_time)
            
            # 计算平均每日进餐次数
            meal_counts = [len(meals) for meals in daily_meals.values()]
            avg_meals = sum(meal_counts) / len(meal_counts) if meal_counts else 0
            
            # 计算规律度：每日进餐次数的稳定性
            if not meal_counts or avg_meals == 0:
                regularity_rate = 50  # 默认值
            else:
                # 计算标准差
                variance = sum((x - avg_meals) ** 2 for x in meal_counts) / len(meal_counts)
                std_dev = variance ** 0.5
                # 规律度 = 100 - (标准差/平均值) * 100，但最低不小于0
                regularity_rate = max(0, min(100, 100 - (std_dev / avg_meals) * 50))
                regularity_rate = round(regularity_rate)
            
            # 计算平均心情分数（改进心情值处理）
            mood_values = {
                'happy': 5, 
                'excited': 5,
                'calm': 4, 
                'relaxed': 4,
                'normal': 3, 
                'neutral': 3,
                'sad': 2, 
                'tired': 2,
                'angry': 1, 
                'anxious': 1,
                'stressed': 1
            }
            
            valid_mood_scores = []
            for record in mood_records:
                if record.mood_type:
                    score = mood_values.get(record.mood_type.lower())
                    if score is not None:
                        valid_mood_scores.append(score)
            
            mood_score = sum(valid_mood_scores) / len(valid_mood_scores) if valid_mood_scores else 3
            
            # 获取最常见心情（改进心情统计）
            mood_counts = {}
            for record in mood_records:
                if record.mood_type:
                    mood_type = record.mood_type.lower()
                    mood_counts[mood_type] = mood_counts.get(mood_type, 0) + 1
            
            top_mood = None
            if mood_counts:
                top_mood = max(mood_counts.items(), key=lambda x: x[1])[0]
            
            mood_labels = {
                'happy': '开心',
                'excited': '兴奋',
                'calm': '平静',
                'relaxed': '放松',
                'normal': '一般',
                'neutral': '一般',
                'sad': '难过',
                'tired': '疲惫',
                'angry': '生气',
                'anxious': '焦虑',
                'stressed': '压力'
            }
            
            top_mood = mood_labels.get(top_mood, '暂无数据') if top_mood else '暂无数据'
            
            # 计算心情趋势（改进趋势计算）
            if len(valid_mood_scores) >= 2:
                # 计算最近3天和之前的平均分数
                recent_scores = valid_mood_scores[-3:] if len(valid_mood_scores) > 3 else valid_mood_scores
                older_scores = valid_mood_scores[:-3] if len(valid_mood_scores) > 3 else []
                
                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores) if older_scores else recent_avg
                
                if recent_avg > older_avg + 0.5:
                    mood_trend = '上升'
                elif recent_avg < older_avg - 0.5:
                    mood_trend = '下降'
                else:
                    mood_trend = '平稳'
            else:
                mood_trend = '数据不足'
            
            # 计算健康评分（改进健康评分计算）
            health_values = {
                'energetic': 5,
                'good': 4,
                'normal': 3,
                'tired': 2,
                'sick': 1
            }
            
            valid_health_scores = []
            for record in health_records:
                if record.feeling:
                    score = health_values.get(record.feeling.lower())
                    if score is not None:
                        valid_health_scores.append(score)
            
            health_score = sum(valid_health_scores) / len(valid_health_scores) if valid_health_scores else 3
            
            # 生成健康建议（改进建议生成逻辑）
            health_tips = []
            
            if health_score < 3:
                health_tips.append('注意休息，保持良好的作息')
            if exercise_minutes < 60:
                health_tips.append('建议增加运动时间，保持身体活力')
            if food_count < 5:
                health_tips.append('注意饮食规律，保持营养均衡')
            
            health_tip = health_tips[0] if health_tips else '继续保持良好的生活习惯'
            
            result = {
                'foodCount': food_count,
                'exerciseMinutes': exercise_minutes,
                'moodScore': round(mood_score, 2),
                'healthScore': round(health_score, 2),
                'topMood': top_mood,
                'moodTrend': mood_trend,
                'healthTip': health_tip,
                'hasData': bool(food_records or exercise_records or mood_records or health_records),
                'mealDistribution': meal_distribution,
                'foodCategories': food_categories,
                'regularityRate': regularity_rate
            }
            
            print(f"健康摘要数据结果: {result}")
            return result
            
        except Exception as e:
            print(f"获取健康摘要数据时发生错误: {str(e)}")
            # 返回一个带有错误信息的结果
            return {
                'error': True,
                'message': '获取数据时发生错误，请稍后重试',
                'details': str(e)
            }
        
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