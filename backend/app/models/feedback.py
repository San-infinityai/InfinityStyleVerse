from ..database import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    
    product = db.relationship('Product', backref='feedbacks')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
