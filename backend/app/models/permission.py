from ..database import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    system = db.Column(db.String(50), nullable=False)
    module_access = db.Column(db.String(50), nullable=False)
