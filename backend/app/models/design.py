from ..database import db
from datetime import datetime

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.LargeBinary(length=(2**24 - 1))) 
    image_mime = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key: link to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship (optional, for easier access to User object)
    user = db.relationship('User', backref=db.backref('designs', lazy=True))
