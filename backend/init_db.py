from app import create_app
from app.models import db, User, FoodRecord, ExerciseRecord, MoodRecord, HealthRecord
import random
from datetime import datetime, timedelta

def init_db():
    """初始化数据库"""
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 如果没有用户，创建测试用户
        if User.query.count() == 0:
            test_user = User(
                username='test_user',
                email='test@example.com',
                password='password123'
            )
            test_user.phone = '13800138000'
            db.session.add(test_user)
            db.session.commit()
            
            # 为测试用户创建一些示例记录
            create_sample_records(test_user.id)

def create_sample_records(user_id):
    """创建示例记录数据"""
    # 食物记录
    meal_times = ['breakfast', 'lunch', 'dinner', 'snack']
    foods = [
        '米饭', '面条', '馒头', '包子', '饺子', '鸡肉', '牛肉', '猪肉', '鱼', 
        '豆腐', '青菜', '西红柿', '黄瓜', '胡萝卜', '土豆', '水果沙拉', '牛奶', '酸奶'
    ]
    
    # 运动记录
    exercise_types = ['walk', 'run', 'bike', 'swim', 'yoga', 'gym', 'ball', 'other']
    intensities = ['light', 'medium', 'high']
    
    # 心情记录
    mood_types = ['happy', 'calm', 'sad', 'angry', 'anxious', 'tired', 'excited', 'bored']
    
    # 健康状况
    feelings = ['energetic', 'good', 'normal', 'tired']
    health_statuses = [
        'sleep_well', 'sleep_bad', 'appetite_good', 'appetite_bad', 
        'energetic', 'fatigue', 'muscle_sore', 'headache', 
        'throat', 'stomach', 'cold', 'allergy'
    ]
    
    # 生成过去30天的记录
    now = datetime.now()
    for i in range(30):
        date = now - timedelta(days=i)
        
        # 食物记录 (每天2-4条)
        for _ in range(random.randint(2, 4)):
            food_record = FoodRecord(
                user_id=user_id,
                food_name=random.choice(foods),
                meal_time=random.choice(meal_times),
                note='示例食物记录',
                created_at=date.replace(
                    hour=random.randint(6, 22),
                    minute=random.randint(0, 59)
                )
            )
            db.session.add(food_record)
        
        # 运动记录 (每天0-2条)
        for _ in range(random.randint(0, 2)):
            exercise_record = ExerciseRecord(
                user_id=user_id,
                exercise_type=random.choice(exercise_types),
                duration=random.randint(15, 120),
                intensity=random.choice(intensities),
                note='示例运动记录',
                created_at=date.replace(
                    hour=random.randint(6, 22),
                    minute=random.randint(0, 59)
                )
            )
            db.session.add(exercise_record)
        
        # 心情记录 (每天1条)
        mood_record = MoodRecord(
            user_id=user_id,
            mood_type=random.choice(mood_types),
            note='示例心情记录',
            created_at=date.replace(
                hour=random.randint(18, 22),
                minute=random.randint(0, 59)
            )
        )
        db.session.add(mood_record)
        
        # 健康状况记录 (每天1条)
        health_record = HealthRecord(
            user_id=user_id,
            feeling=random.choice(feelings),
            status=random.sample(health_statuses, random.randint(1, 3)),
            note='示例健康状况记录',
            created_at=date.replace(
                hour=random.randint(6, 10),
                minute=random.randint(0, 59)
            )
        )
        db.session.add(health_record)
    
    db.session.commit()

if __name__ == '__main__':
    init_db()
    print("数据库初始化完成！") 