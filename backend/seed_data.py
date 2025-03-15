from app import create_app, db
from app.models.food import Food

def seed_foods():
    app = create_app()
    with app.app_context():
        # 清空现有数据
        Food.query.delete()
        
        # 添加示例食物
        foods = [
            Food(
                name='菠菜',
                category='蔬菜',
                calories=23,
                protein=2.9,
                fat=0.4,
                carbs=3.6,
                fiber=2.2,
                season='春季',
                region='全国',
                description='富含铁质和维生素，春季应季蔬菜',
                image_url='https://example.com/spinach.jpg'
            ),
            Food(
                name='草莓',
                category='水果',
                calories=32,
                protein=0.7,
                fat=0.3,
                carbs=7.7,
                fiber=2.0,
                season='春季',
                region='全国',
                description='富含维生素C和抗氧化物质',
                image_url='https://example.com/strawberry.jpg'
            )
        ]
        
        db.session.bulk_save_objects(foods)
        db.session.commit()
        print('示例数据添加成功！')

if __name__ == '__main__':
    seed_foods() 