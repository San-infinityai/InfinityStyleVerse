from ..database import db
from datetime import datetime
import base64
import json

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    sale_price = db.Column(db.Float)
    discount = db.Column(db.Float)
    sizes = db.Column(db.String(100))
    colors = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    visibility = db.Column(db.String(20), default="Published")
    publish_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    esg_score = db.Column(db.Float)
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use back_populates here to pair with ProductImage.product
    images = db.relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "category": self.category,
            "description": self.description,
            "sale_price": self.sale_price,
            "discount": self.discount,
            "sizes": self.sizes.split(",") if self.sizes else [],
            "colors": self.colors.split(",") if self.colors else [],
            "tags": self.tags.split(",") if self.tags else [],
            "images": [img.id for img in self.images],
            "visibility": self.visibility,
            "publish_date": self.publish_date.isoformat() if self.publish_date else None,
            "user_id": self.user_id,
            "esg_score": self.esg_score,
            "likes": self.likes,
            "views": self.views,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


