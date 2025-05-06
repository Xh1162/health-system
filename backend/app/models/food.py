from datetime import datetime
from . import db

class FoodItem(db.Model):
    __tablename__ = 'food_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True) # e.g., 'protein', 'vegetable', 'staple', 'fruit', 'snack'
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(256), nullable=True)
    is_recommended = db.Column(db.Boolean, default=True, nullable=False) # Flag to easily enable/disable for recommendations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'is_recommended': self.is_recommended,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<FoodItem {self.name}>' 