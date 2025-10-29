from datetime import datetime
from ..database import db

class Lock(db.Model):
    __tablename__ = "locks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    step_id = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
