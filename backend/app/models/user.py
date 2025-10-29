from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225)) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    last_login=db.Column(db.DateTime,default=None)
    products = db.relationship('Product', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    status = db.Column(db.String(10), default='Inactive')
    bio = db.Column(db.Text, nullable=True)  
    image_url = db.Column(db.LargeBinary(length=(2**24 - 1))) 
    image_mime = db.Column(db.String(50), nullable=True)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
