from ..database import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', back_populates='role')  
    permissions = db.relationship('Permission', backref='role', lazy=True)
